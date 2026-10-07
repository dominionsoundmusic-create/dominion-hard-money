#!/usr/bin/env python3
"""One-time extraction of the live pages into editable sources (_src/pages).

Run once at the start of the Playbook 2.0 rebuild. Every live .html page is
split into a front-matter block (title, description, hero, crumbs, form) and
a body. The shared chrome (scripture bar, header, translate widget, footer,
duplicate disclosure) is dropped because build.py renders it from one place.
Forms are replaced by a <deal-form> placeholder; their markup and script are
kept verbatim in _src/forms so field names and the endpoint never change.

Kept in the repo for the record; build.py is what runs from now on.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, Comment

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "_src"
OUT = SRC / "pages"
SITE = "https://dominionhardmoney.com"

SKIP = {"forms/deal-inquiry.html"}


def text(el) -> str:
    return re.sub(r"\s+", " ", el.get_text(" ", strip=True)) if el else ""


def inner(el) -> str:
    return "".join(str(c) for c in el.contents).strip() if el else ""


def meta(soup, **kw):
    el = soup.find("meta", attrs=kw)
    return el.get("content", "").strip() if el else ""


def route_of(rel: str) -> str:
    return "/" + (rel[: -len("index.html")] if rel.endswith("index.html") else rel)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    report = []
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith(("_src/", ".github/", "docs/")) or rel in SKIP:
            continue
        raw = path.read_text(encoding="utf-8")
        fm, body, extra = extract(rel, raw)
        dest = OUT / (rel[:-5] + ".src.html")
        dest.parent.mkdir(parents=True, exist_ok=True)
        lines = ["---"]
        for k, v in fm.items():
            if v in (None, "", []):
                continue
            if isinstance(v, (list, dict)):
                v = json.dumps(v, ensure_ascii=False)
            lines.append(f"{k}: {v}")
        lines.append("---")
        dest.write_text("\n".join(lines) + "\n" + body.strip() + "\n", encoding="utf-8")
        if extra:
            (OUT / (rel[:-5] + ".ld.json")).write_text(
                json.dumps(extra, ensure_ascii=False, indent=1), encoding="utf-8")
        report.append(rel)
    print(f"extracted {len(report)} pages")
    return 0


def extract(rel: str, raw: str):
    # Seven pages carry a pasted second copy of the head and hero (Sep 23
    # 2026 accident). Keep only what follows the last duplicated hero figure.
    clobbered = ("Private Money Lenders Near Me: Where Local" in raw
                 and not rel.startswith("private-money-lenders-near-me"))
    soup = BeautifulSoup(raw, "html.parser")
    fm: dict = {}
    t = soup.find("title")
    fm["title"] = text(t)
    fm["description"] = meta(soup, name="description")
    fm["og_title"] = meta(soup, property="og:title")
    fm["og_description"] = meta(soup, property="og:description")
    fm["og_type"] = meta(soup, property="og:type")
    fm["og_image"] = meta(soup, property="og:image")
    fm["robots"] = meta(soup, name="robots")
    can = soup.find("link", rel="canonical")
    fm["canonical"] = can.get("href") if can else SITE + route_of(rel)
    gsv = meta(soup, name="google-site-verification")
    if gsv:
        fm["google_site_verification"] = gsv

    faqs, extra = [], []
    for s in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(s.string or "")
        except Exception:
            # the clobbered pages carry FAQ JSON pasted as visible text
            continue
        items = data if isinstance(data, list) else [data]
        for d in items:
            if d.get("@type") == "FAQPage":
                for q in d.get("mainEntity", []):
                    faqs.append((q["name"], q["acceptedAnswer"]["text"]))
            elif d.get("@type") not in ("FinancialService",):
                extra.append(d)
    body = soup.body
    if body is None:
        return fm, "", extra

    # Drop chrome.
    for c in body.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()
    for sel in ["header", "footer", "#gt-bar", "#google_translate_element", ".scripture-bar", "nav.nav"]:
        for el in body.select(sel):
            el.decompose()
    for el in body.find_all("div", style=True):
        if text(el) in ("John 3:16",):
            el.decompose()
    for el in body.find_all("div", style=True):
        if "Jesse Duplantis" in text(el):
            fm["duplantis"] = "yes"
            el.decompose()
    for el in body.find_all("nav"):
        crumbs = []
        for a in el.find_all(["a", "span"], recursive=False):
            crumbs.append([text(a), a.get("href", "")] if a.name == "a" else [text(a), ""])
        if crumbs and crumbs[0][0] == "Home":
            fm["crumbs"] = crumbs
        el.decompose()
    for el in body.select(".crumb"):
        crumbs = [[text(a), a.get("href", "")] for a in el.find_all("a")]
        fm.setdefault("crumbs", crumbs)
        el.decompose()

    # Scripts: deal form + translate are rebuilt; anything else is page logic.
    page_scripts = []
    deal_script = None
    for s in body.find_all("script"):
        src = s.string or ""
        if "googleTranslateElementInit" in src or "translate.google" in src or "hml" in src[:200]:
            s.decompose()
        elif 'var W="https://dominion-demo-backend' in src:
            deal_script = src
            s.decompose()
        elif s.get("type") == "application/ld+json":
            s.decompose()
        else:
            page_scripts.append(str(s))
            s.decompose()
    for s in body.find_all("style"):
        page_scripts.insert(0, str(s))
        s.decompose()

    # Hero.
    hero = body.find(class_="hero") or body.find(class_="page-hero") or body.find(class_="bk-hero") or body.find(class_="plg-hero")
    if clobbered:
        heroes = body.find_all("div", class_="hero")
        hero = heroes[-1] if heroes else hero
    if hero is not None:
        h = hero.find(["h1", "h2"])
        fm["h1"] = inner(h) if h else ""
        lede = hero.find("p", class_="lede") or hero.find("p")
        if lede is not None and lede.find("a", class_="cta") is None:
            fm["lede"] = inner(lede)
        cta = hero.find("a", class_="cta")
        if cta is not None:
            fm["cta"] = text(cta)
        m = hero.find(class_="meta")
        if m is not None:
            fm["byline"] = inner(m)
        nxt = hero.find_next_sibling()
        if nxt is not None and nxt.name == "figure" and "wide" in (nxt.get("class") or []):
            img = nxt.find("img")
            fm["hero_img"] = img.get("src")
            fm["hero_alt"] = img.get("alt", "")
            cap = nxt.find("figcaption")
            if cap:
                fm["hero_caption"] = inner(cap)
            nxt.decompose()
        if clobbered:
            # everything before the real content is pasted junk
            for prev in list(hero.find_all_previous()):
                if prev.parent is not None and prev.name not in ("body", "html"):
                    pass
            node = body.contents[0] if body.contents else None
            while node is not None and node is not hero:
                n2 = node.next_sibling
                node.extract()
                node = n2
            fm["REPAIR"] = "head and hero were clobbered on the live page; rewrite title, h1 and lede"
        hero.decompose()

    # Deal form.
    apply = body.find("div", id="apply") or (body.find("form", id="dealForm").find_parent("div", class_="section") if body.find("form", id="dealForm") else None)
    if apply is not None:
        variant = "deal"
        if "ffirst" in str(apply):
            variant = "deal-home" if rel == "index.html" else "deal-apply"
        fm["form"] = variant
        if deal_script and 'source_city:"' in deal_script:
            m = re.search(r'source_city:"([^"]*)",source_state:"([^"]*)"', deal_script)
            if m and m.group(1):
                fm["form_city"], fm["form_state"] = m.group(1), m.group(2)
        sub = apply.find("p", class_="apply-sub")
        if sub and "we do not place loans" in str(sub):
            fm["form_sub_variant"] = "place"
        save_form(variant, apply, deal_script)
        ph = soup.new_tag("deal-form")
        apply.replace_with(ph)
    for el in body.find_all("div", class_="callout"):
        if "Working a deal right now" in text(el):
            el.decompose()
    for el in body.find_all("p", style=True):
        if text(el).startswith("Dominion Hard Money does not lend its own funds"):
            el.decompose()

    # Visible FAQ section -> <faq>.
    faq_html = ""
    for sec in body.find_all(["section", "div"]):
        fq = sec.find("div", class_="faq", recursive=False)
        if fq is not None:
            h2 = sec.find("h2")
            if h2:
                fm["faq_heading"] = text(h2)
            faq_html = render_faq_from_visible(fq)
            sec.decompose()
            break
    if not faq_html and faqs:
        faq_html = "\n".join(f"<h3>{html.escape(q)}</h3>\n<p>{html.escape(a)}</p>" for q, a in faqs)
        fm["faq_from_jsonld"] = "yes"
    fm["faq_count_jsonld"] = str(len(faqs))

    out = str(body)
    out = re.sub(r"^<body[^>]*>|</body>$", "", out.strip()).strip()
    if page_scripts:
        out += "\n<page-assets>\n" + "\n".join(page_scripts) + "\n</page-assets>"
    if faq_html:
        out += "\n<faq>\n" + faq_html + "\n</faq>"
    return fm, out, extra


def render_faq_from_visible(fq) -> str:
    parts = []
    for el in fq.children:
        if getattr(el, "name", None) in ("h3", "p", "ul", "ol"):
            parts.append(str(el))
    return "\n".join(parts)


SAVED = set()


def save_form(variant, apply, script):
    if variant in SAVED:
        return
    SAVED.add(variant)
    d = SRC / "forms"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{variant}.html").write_text(str(apply) + "\n<script>" + (script or "") + "</script>\n", encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
