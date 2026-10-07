#!/usr/bin/env python3
"""Build dominionhardmoney.com from _src/ into plain .html files at the repo root.

    python3 _src/build.py            build every page, sitemap.xml, blog index
    python3 _src/build.py --check    build, then fail on any rule violation

Netlify serves the repository root as-is (no build command), so the output of
this script IS the site. Sources live in _src/pages/<path>.src.html: a small
front-matter block (key: value per line) followed by the page body. Custom
tags in a body:

    <deal-form></deal-form>   the deal-inquiry form (variant from `form:`)
    <faq> <h3>Q</h3><p>A</p> ... </faq>   visible FAQ + FAQPage JSON-LD
    <sources> <li>...</li> ... </sources> numbered Sources list
    <page-assets> <style>/<script> </page-assets>   page-only CSS/JS
    <photo src="name" alt="..." caption="..."></photo>  responsive WebP figure

_src/ is never served: _redirects 404s /_src/*.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import sys
from datetime import date
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "_src"
PAGES = SRC / "pages"
FORMS = SRC / "forms"
SITE = "https://dominionhardmoney.com"
TODAY = date.today().isoformat()
WIDTHS = (480, 800, 1200, 1600)

DISCLOSURE = (
    "Dominion Hard Money does not lend its own funds; it arranges financing "
    "through third-party lending partners."
)
EXEMPT_FAQ = {"privacy-policy.html", "terms.html", "disclaimer.html", "cookie-policy.html", "404.html"}

# --------------------------------------------------------------------------
# Image catalog. Alt text describes what is actually in each photo.
# --------------------------------------------------------------------------
IMAGES = {
    "1": "Aerial view of a palm-lined Florida neighborhood of tile-roof homes with a city skyline on the horizon",
    "2": "Aerial view over rows of suburban homes and green trees toward a distant waterfront skyline",
    "3": "Aerial view of a sunny residential neighborhood with a downtown skyline in the distance",
    "4": "Aerial view of a long straight street of single-family homes leading toward a bay and skyline",
    "5": "An empty room mid-renovation with fresh drywall, a new window and a stepladder",
    "6": "A gutted living room with exposed wall framing, new windows and a stepladder on drop cloths",
    "7": "An interior under renovation with open stud walls, new windows and tools on the floor",
    "8": "A room being rebuilt with a framed ceiling, a new window and a ladder in the corner",
    "alabama-hero": "A sunny, oak-shaded street of craftsman bungalows with deep front porches",
    "atlanta-hero": "A tree-lined Atlanta street of porch-front houses with the Midtown skyline beyond",
    "bridge-hero": "Two small white houses on a quiet tree-lined street in autumn",
    "business-hero": "A row of two-story brick storefront buildings on a small-town main street",
    "colorado-hero": "A suburban street of ranch homes running toward the Rocky Mountain foothills",
    "commercial-hero": "A corner block of brick commercial buildings with shops at street level",
    "connecticut-hero": "A New England street of large brick and clapboard houses under bare trees",
    "construction-hero": "A new wood-framed house under construction on a cleared lot",
    "credit-hero": "A man standing in a driveway looking at a modest one-story house",
    "documents-hero": "A stack of papers and a pen beside a coffee cup on a sunlit desk",
    "dscr-hero": "A one-story rental house with a green lawn on a suburban street",
    "dscr-lenders-hero": "A two-story brick duplex with two front doors and trimmed hedges",
    "duplex": "A two-unit brick rental house with two front doors and a small front yard",
    "flip-hero": "A freshly renovated two-story house with new landscaping and a for-sale sign",
    "florida-hero": "Aerial view of waterfront Florida homes along a canal with boats at the docks",
    "georgia-hero": "Aerial view of a wooded Georgia subdivision with a city skyline far off",
    "hardmoney-hero": "A single-story house under renovation with a contractor van in the driveway",
    "houston-hero": "A wide oak-lined residential street of low brick ranch homes",
    "indiana-hero": "A Midwestern street of older frame houses with front porches and big trees",
    "maryland-hero": "A row of brick rowhouses with marble front steps on a city street",
    "massachusetts-hero": "A street of tall triple-decker houses with stacked front porches",
    "michigan-hero": "A brick two-story house with an iron fence on a residential street",
    "missouri-hero": "A street of red brick houses with the Gateway Arch in the background",
    "near-me-hero": "An investor on a phone call at a kitchen table with a laptop and notes",
    "ohio-hero": "A tree-lined sidewalk running past older houses in autumn color",
    "pennsylvania-hero": "A hillside street of narrow brick rowhouses with a river valley beyond",
    "rates-hero": "A calculator, house keys and a small model house on a desk with loan papers",
    "rehab-in-progress": "A room mid-renovation with framing exposed, new windows and a ladder",
    "south-carolina-hero": "A quiet Southern street of porch-front houses under mature trees",
    "tampa-hero": "Aerial view of a Tampa-area neighborhood with the downtown skyline on the horizon",
    "texas-hero": "Aerial view of a Texas subdivision of brick ranch homes and wide lots",
    "vetting-hero": "Hands holding a printed document beside an open laptop on a wooden desk",
    "virginia-hero": "A brick townhouse street with iron stair railings and leafy trees",
    "washington-hero": "A Pacific Northwest street of craftsman houses with evergreen trees",
    "private-lending-guide-cover": "Cover of The Real Estate Investor's Guide to Private Lending",
}

# Topic pools for in-body photos when a page has fewer than two.
POOLS = {
    "flip": ["6", "rehab-in-progress", "flip-hero", "7", "8", "5"],
    "rehab": ["7", "8", "rehab-in-progress", "hardmoney-hero", "6"],
    "construction": ["construction-hero", "8", "5", "documents-hero"],
    "dscr": ["duplex", "dscr-lenders-hero", "dscr-hero", "rates-hero"],
    "rates": ["rates-hero", "documents-hero", "duplex", "6"],
    "bridge": ["bridge-hero", "documents-hero", "hardmoney-hero", "5"],
    "commercial": ["commercial-hero", "business-hero", "documents-hero"],
    "credit": ["credit-hero", "documents-hero", "rates-hero"],
    "vetting": ["vetting-hero", "near-me-hero", "documents-hero", "rates-hero"],
    "state": ["documents-hero", "duplex", "rehab-in-progress", "rates-hero", "6"],
    "blog": ["documents-hero", "rates-hero", "rehab-in-progress", "duplex", "6", "vetting-hero", "7", "flip-hero"],
    "default": ["documents-hero", "rehab-in-progress", "duplex", "rates-hero"],
}

NAV = [
    ("/hard-money-loans/", "Hard Money Loans"),
    ("/fix-and-flip-loans/", "Fix and Flip"),
    ("/bridge-loans/", "Bridge"),
    ("/dscr-loans/", "DSCR Rental"),
    ("/private-money-lender/", "Private Money"),
    ("/states.html", "Locations"),
    ("/blog/", "Blog"),
    ("/books/", "Books"),
]

FOOT = [
    ("Loan programs", [
        ("/hard-money-loans/", "Hard money loans"), ("/fix-and-flip-loans/", "Fix and flip loans"),
        ("/bridge-loans/", "Bridge loans"), ("/dscr-loans/", "DSCR rental loans"),
        ("/rehab-loans/", "Rehab loans"), ("/hard-money-construction-loan/", "Construction loans"),
        ("/cash-out-refinance/", "Cash-out refinance"), ("/commercial-hard-money/", "Commercial hard money"),
        ("/investment-property-loans/", "Investment property loans"), ("/real-estate-investor-loans/", "Real estate investor loans"),
        ("/hard-money-lenders-for-business/", "Business-purpose loans"),
    ]),
    ("Guides", [
        ("/what-is-a-hard-money-loan/", "What is a hard money loan?"), ("/what-is-hard-money-financing/", "How hard money financing works"),
        ("/hard-money-rates/", "Hard money rates"), ("/hard-money-requirements/", "Hard money requirements"),
        ("/hard-money-calculator/", "Hard money calculator"), ("/finding-a-hard-money-lender/", "Finding a hard money lender"),
        ("/hard-money-lender/", "What a hard money lender does"), ("/hard-money-lender-bad-credit/", "Hard money and bad credit"),
        ("/hard-money-lenders-near-me/", "Hard money lenders near me"), ("/fix-and-flip-loans-for-beginners/", "First flip financing"),
        ("/fix-and-flip-loans-near-me/", "Fix and flip loans near me"),
    ]),
    ("Rental and DSCR", [
        ("/what-is-a-dscr-loan/", "What is a DSCR loan?"), ("/dscr-loan-rates/", "DSCR loan rates"),
        ("/dscr-loan-requirements/", "DSCR loan requirements"), ("/dscr-loan-lenders/", "DSCR loan lenders"),
        ("/dscr-loan-no-money-down/", "DSCR with no money down"), ("/investment-property-loan-rates/", "Investment property loan rates"),
        ("/investment-property-loan-requirements/", "Investment property loan requirements"),
        ("/private-money-lenders-near-me/", "Private money lenders near me"), ("/landlord-costs-by-state/", "Landlord costs by state"),
    ]),
    ("Company", [
        ("/about.html", "About"), ("/contact/", "Contact"), ("/faq/", "FAQ"), ("/states.html", "States and cities"),
        ("/blog/", "Blog"), ("/books/", "Books"), ("/books/free/", "Free landlord books"),
        ("/private-lending-guide/", "Free private lending guide"), ("/apply.html", "Submit a deal"),
    ]),
    ("Legal", [
        ("/privacy-policy.html", "Privacy policy"), ("/terms.html", "Terms of service"),
        ("/disclaimer.html", "Disclaimer"), ("/cookie-policy.html", "Cookie policy"),
    ]),
]

LANG_MENU = (
    "<div class=\"hml\" id=\"hml\"><button type=\"button\" class=\"hml-btn\" id=\"hmlBtn\" aria-haspopup=\"listbox\" aria-expanded=\"false\" aria-label=\"Choose language\">"
    "<span class=\"hml-f\" id=\"hmlFlag\">{us}</span><span id=\"hmlCode\">EN</span>"
    "<svg class=\"hml-car\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"3\" stroke-linecap=\"round\" aria-hidden=\"true\"><polyline points=\"6 9 12 15 18 9\"/></svg></button>"
    "<div class=\"hml-menu\" id=\"hmlMenu\" role=\"listbox\">{items}</div></div>"
)
FLAGS = {
    "en": ("EN", "English", "<svg viewBox='0 0 60 40' aria-hidden='true'><rect width='60' height='40' fill='#B22234'/><g fill='#fff'><rect y='3.1' width='60' height='3.1'/><rect y='9.2' width='60' height='3.1'/><rect y='15.4' width='60' height='3.1'/><rect y='21.5' width='60' height='3.1'/><rect y='27.7' width='60' height='3.1'/><rect y='33.8' width='60' height='3.1'/></g><rect width='26' height='21.5' fill='#3C3B6E'/></svg>"),
    "es": ("ES", "Espa&ntilde;ol", "<svg viewBox='0 0 60 40' aria-hidden='true'><rect width='20' height='40' fill='#006847'/><rect x='20' width='20' height='40' fill='#fff'/><rect x='40' width='20' height='40' fill='#CE1126'/><ellipse cx='30' cy='20' rx='4.4' ry='3.8' fill='none' stroke='#8C6239' stroke-width='1.5'/></svg>"),
    "zh-CN": ("ZH", "&#20013;&#25991;", "<svg viewBox='0 0 60 40' aria-hidden='true'><rect width='60' height='40' fill='#DE2910'/><path fill='#FFDE00' d='M10 6l1.9 5.9H18l-5 3.6 1.9 5.9-5-3.7-5 3.7 1.9-5.9-5-3.6h6.1z'/></svg>"),
    "vi": ("VI", "Ti&#7871;ng Vi&#7879;t", "<svg viewBox='0 0 60 40' aria-hidden='true'><rect width='60' height='40' fill='#DA251D'/><path fill='#FF0' d='M30 10.5l2.8 8.6h9l-7.3 5.3 2.8 8.6-7.3-5.3-7.3 5.3 2.8-8.6-7.3-5.3h9z'/></svg>"),
    "ko": ("KO", "&#54620;&#44397;&#50612;", "<svg viewBox='0 0 60 40' aria-hidden='true'><rect width='60' height='40' fill='#fff'/><path d='M30 12a8 8 0 010 16 8 8 0 010-16z' fill='#CD2E3A'/><path d='M30 12a8 8 0 000 16 4 4 0 010-8 4 4 0 000-8z' fill='#0047A0'/></svg>"),
    "ru": ("RU", "&#1056;&#1091;&#1089;&#1089;&#1082;&#1080;&#1081;", "<svg viewBox='0 0 60 40' aria-hidden='true'><rect width='60' height='13.3' fill='#fff'/><rect y='13.3' width='60' height='13.3' fill='#0039A6'/><rect y='26.6' width='60' height='13.4' fill='#D52B1E'/></svg>"),
    "pt": ("PT", "Portugu&ecirc;s", "<svg viewBox='0 0 60 40' aria-hidden='true'><rect width='60' height='40' fill='#009B3A'/><path d='M30 5l25 15-25 15L5 20z' fill='#FEDF00'/><circle cx='30' cy='20' r='8' fill='#002776'/></svg>"),
}


def lang_menu() -> str:
    items = "".join(
        f"<button type=\"button\" class=\"hml-i\" role=\"option\" data-l=\"{k}\" data-s=\"{v[0]}\"><span class=\"hml-f\">{v[2]}</span>{v[1]}</button>"
        for k, v in FLAGS.items())
    return LANG_MENU.format(us=FLAGS["en"][2], items=items)


# --------------------------------------------------------------------------
# Images
# --------------------------------------------------------------------------
_img_cache: dict = {}


def image_info(src: str):
    """Return (srcset, fallback, width, height) for a site image, building
    WebP derivatives on first use. Raises if the file is missing."""
    if src in _img_cache:
        return _img_cache[src]
    path = ROOT / src.lstrip("/")
    if not path.exists():
        raise SystemExit(f"missing image: {src}")
    from PIL import Image
    with Image.open(path) as im:
        w, h = im.size
        stem = path.stem
        sub = path.parent.relative_to(ROOT / "images").as_posix() if path.is_relative_to(ROOT / "images") else "root"
        outdir = ROOT / "images" / "w" / ("" if sub == "." else sub)
        outdir.mkdir(parents=True, exist_ok=True)
        widths = [x for x in WIDTHS if x < w] + [w if w <= 1920 else 1920]
        parts = []
        for tw in widths:
            out = outdir / f"{stem}-{tw}.webp"
            if not out.exists():
                th = round(h * tw / w)
                im.convert("RGB").resize((tw, th), Image.LANCZOS).save(out, "WEBP", quality=74, method=6)
            parts.append((("/" + out.relative_to(ROOT).as_posix()), tw))
    srcset = ", ".join(f"{u} {tw}w" for u, tw in parts)
    fallback = next((u for u, tw in parts if tw >= 800), parts[-1][0])
    _img_cache[src] = (srcset, fallback, w, h)
    return _img_cache[src]


def resolve_image(name: str) -> str:
    if name.startswith("/"):
        return name
    for ext in (".jpg", ".png"):
        if (ROOT / "images" / f"{name}{ext}").exists():
            return f"/images/{name}{ext}"
    raise SystemExit(f"unknown image name: {name}")


def img_html(src: str, alt: str, *, eager=False, sizes="(min-width: 760px) 736px, 100vw", cls="") -> str:
    srcset, fallback, w, h = image_info(src)
    load = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{fallback}" srcset="{srcset}" sizes="{sizes}" width="{w}" height="{h}" '
            f'{load} alt="{html.escape(alt, quote=True)}">')


def figure_html(name: str, alt: str | None = None, caption: str = "") -> str:
    src = resolve_image(name)
    alt = alt or IMAGES.get(Path(src).stem, "")
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return f'<figure class="pic">{img_html(src, alt)}{cap}</figure>'


# --------------------------------------------------------------------------
# Sources
# --------------------------------------------------------------------------
def parse_source(path: Path):
    raw = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n?(.*)\Z", raw, re.S)
    if not m:
        raise SystemExit(f"{path}: no front matter")
    fm = {}
    for line in m.group(1).splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        k, _, v = line.partition(":")
        v = v.strip()
        if v.startswith(("[", "{")):
            v = json.loads(v)
        fm[k.strip()] = v
    return fm, m.group(2)


def out_rel(src: Path) -> str:
    rel = src.relative_to(PAGES).as_posix()
    return rel[: -len(".src.html")] + ".html"


def url_of(rel: str) -> str:
    if rel == "index.html":
        return SITE + "/"
    if rel.endswith("/index.html"):
        return SITE + "/" + rel[: -len("index.html")]
    return SITE + "/" + rel


def pool_for(rel: str) -> list[str]:
    r = rel
    if r.startswith("blog/"):
        return POOLS["blog"]
    if r.startswith("hard-money-lenders/"):
        return POOLS["state"]
    for key, names in (("construction", "construction"), ("rehab", "rehab"), ("flip", "flip"), ("dscr", "dscr"),
                       ("rate", "rates"), ("bridge", "bridge"), ("commercial", "commercial"), ("business", "commercial"),
                       ("credit", "credit"), ("near-me", "vetting"), ("finding", "vetting"), ("private", "vetting"),
                       ("rental", "dscr"), ("landlord", "dscr"), ("investment-property", "dscr")):
        if key in r:
            return POOLS[names]
    return POOLS["default"]


# --------------------------------------------------------------------------
# Text rules
# --------------------------------------------------------------------------
DASH_RE = re.compile("[—–]|&mdash;|&ndash;|&#8212;|&#8211;")


def visible_text(soup) -> str:
    s = BeautifulSoup(str(soup), "html.parser")
    for t in s(["script", "style", "noscript"]):
        t.decompose()
    return s.get_text(" ")


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------
def css_version() -> str:
    return hashlib.md5((ROOT / "assets" / "site.css").read_bytes() + (ROOT / "assets" / "site.js").read_bytes()).hexdigest()[:8]


def header_html() -> str:
    links = "".join(f'<a href="{u}">{t}</a>' for u, t in NAV)
    return (
        '<header><div class="topline"><div class="container">John 3:16</div></div>'
        '<div class="bar container"><a class="logo" href="/"><img src="/images/dominion-logo.svg" alt="Dominion Hard Money home" width="218" height="64"></a>'
        '<button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>'
        f'<nav id="site-nav" aria-label="Main">{links}<a class="nav-cta" href="/apply.html">Submit a Deal</a></nav>'
        f'{lang_menu()}</div></header>'
    )


def footer_html() -> str:
    cols = []
    for title, links in FOOT:
        lis = "".join(f'<li><a href="{u}">{t}</a></li>' for u, t in links)
        cols.append(f'<div><p class="fh">{title}</p><ul>{lis}</ul></div>')
    return (
        '<footer><div class="container">'
        '<div class="flogo"><a href="/"><img src="/images/dominion-logo.svg" alt="Dominion Hard Money" width="218" height="64" loading="lazy"></a></div>'
        f'<div class="fcols">{"".join(cols)}</div>'
        '<div class="legal">'
        f'<p>{DISCLOSURE} All loans are for business purposes only and secured by non-owner-occupied investment property, held in a business entity. '
        'Not a commitment to lend. All loans subject to underwriting, property review, and approval by the lender. Rates and terms vary by deal and borrower profile and are subject to change without notice. The 12.99% plus 2.99 points figure is the lending partner\'s standard starting price for short-term loans; the lender adjusts final pricing after underwriting for credit, loan size and experience.</p>'
        '<p>Not available in all states. Not available in Nevada, Utah, South Dakota, or Vermont. Loans in California, Oregon, Idaho, Arizona, North Dakota, Minnesota, New York, New Jersey, and North Carolina are subject to additional licensing requirements. '
        'Rate and fee information is provided for general informational purposes only. Equal housing opportunity.</p>'
        f'<p>&copy; {date.today().year} Dominion Hard Money, a Dominion Digital Group brand &middot; dominionhardmoney.com</p>'
        '</div></div></footer>'
    )


SHARED_STYLE = "<style>:root{color-scheme:light}</style>"


def head_html(fm, rel, ld, hero_src, page_css, cssv) -> str:
    url = fm.get("canonical") or url_of(rel)
    title = fm["title"]
    desc = fm.get("description", "")
    ogt = fm.get("og_title") or title
    ogd = fm.get("og_description") or desc
    ogimg = fm.get("og_image") or (SITE + hero_src if hero_src else SITE + "/images/hardmoney-hero.jpg")
    robots = fm.get("robots") or "index, follow"
    pre = ""
    if hero_src:
        srcset, _, _, _ = image_info(hero_src)
        pre = f'<link rel="preload" as="image" imagesrcset="{srcset}" imagesizes="100vw" fetchpriority="high">'
    gsv = fm.get("google_site_verification")
    gsv = f'<meta name="google-site-verification" content="{gsv}">' if gsv else ""
    lds = "".join(f'<script type="application/ld+json">{json.dumps(d, ensure_ascii=False)}</script>' for d in ld)
    e = lambda s: html.escape(s, quote=True)
    return (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f'{gsv}<title>{html.escape(title, quote=False)}</title>\n'
        f'<meta name="description" content="{e(desc)}">\n'
        f'<meta name="robots" content="{e(robots)}">\n'
        f'<link rel="canonical" href="{e(url)}">\n'
        f'<meta property="og:type" content="{e(fm.get("og_type") or "website")}"><meta property="og:site_name" content="Dominion Hard Money">'
        f'<meta property="og:title" content="{e(ogt)}"><meta property="og:description" content="{e(ogd)}">'
        f'<meta property="og:url" content="{e(url)}"><meta property="og:image" content="{e(ogimg)}">'
        f'<meta name="twitter:card" content="summary_large_image">\n'
        '<!-- shared-head -->'
        '<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="apple-touch-icon" href="/apple-touch-icon.png">'
        '<link rel="preload" href="/assets/fonts/inter-var-latin.woff2" as="font" type="font/woff2" crossorigin>'
        f'<link rel="stylesheet" href="/assets/site.css?v={cssv}">'
        f'<script src="/assets/site.js?v={cssv}" defer></script>'
        '<!-- /shared-head -->\n'
        f'{SHARED_STYLE}\n{pre}{page_css}{lds}\n</head>\n'
    )


def crumbs_html(crumbs) -> tuple[str, dict | None]:
    if not crumbs:
        return "", None
    items, ld = [], []
    for i, (name, href) in enumerate(crumbs, 1):
        name_h = html.escape(html.unescape(name), quote=False)
        if href:
            path = href.replace(SITE, "") or "/"
            items.append(f'<li><a href="{path}">{name_h}</a></li>')
            ld.append({"@type": "ListItem", "position": i, "name": html.unescape(name), "item": SITE + path})
        else:
            items.append(f'<li aria-current="page">{name_h}</li>')
            ld.append({"@type": "ListItem", "position": i, "name": html.unescape(name)})
    return (f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(items)}</ol></nav>',
            {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": ld})


def split_lede(lede: str) -> tuple[str, str]:
    """Hero gets one short statement; a long lede's remainder opens the body."""
    plain = BeautifulSoup(lede, "html.parser").get_text()
    if len(plain) <= 200:
        return lede, ""
    m = re.search(r"(?<=[.?!])\s+(?=[A-Z\"])", lede)
    if not m or m.start() > 260:
        return lede, ""
    return lede[: m.start()], lede[m.end():]


def hero_html(fm, rel, has_form) -> tuple[str, str, str, dict | None]:
    hero_src = resolve_image(fm.get("hero_img") or "hardmoney-hero")
    alt = fm.get("hero_alt") or IMAGES.get(Path(hero_src).stem, "")
    sub, rest = split_lede(fm.get("lede", ""))
    crumbs, crumb_ld = crumbs_html(fm.get("crumbs"))
    cta = fm.get("cta") or ("Get your deal reviewed" if has_form else "Submit a deal")
    cta_href = fm.get("cta_href") or ("#apply" if has_form else "/apply.html")
    cta2 = fm.get("cta2") or "See loan programs|/hard-money-loans/"
    c2l, _, c2h = cta2.partition("|")
    byline = f'<p class="byline">{fm["byline"]}</p>' if fm.get("byline") else ""
    btns = f'<div class="ctas"><a class="btn" href="{cta_href}">{cta}</a><a class="btn ghost" href="{c2h}">{c2l}</a></div>'
    if fm.get("no_hero_ctas"):
        btns = ""
    h = (
        f'<section class="hero">{img_html(hero_src, alt, eager=True, sizes="100vw", cls="hero-bg")}'
        f'<div class="hero-in container"><div class="hero-copy">{crumbs}<h1>{fm.get("h1", "MISSING H1")}</h1>{byline}'
        f'{f"<p class=sub>{sub}</p>" if sub else ""}{btns}</div></div></section>'
    )
    if fm.get("duplantis"):
        h = ('<div class="quote-bar"><p>&ldquo;I believe the unbelievable, I receive the impossible, because it&rsquo;s doable.&rdquo; '
             '<span>&mdash; Jesse Duplantis</span></p></div>') + h
    return h, rest, hero_src, crumb_ld


def form_html(fm) -> str:
    variant = fm.get("form", "deal")
    tpl = (FORMS / f"{variant}.html").read_text(encoding="utf-8")
    sub_tail = ("we do not place loans on a home you will live in." if fm.get("form_sub_variant") == "place"
                else "our lending partners do not finance a home you will live in.")
    rep = {
        "{{form_heading}}": fm.get("form_heading") or "Get your deal reviewed",
        "{{sub_tail}}": sub_tail,
        "{{addr_value}}": html.escape(fm.get("form_city", ""), quote=True),
        "{{source_city}}": fm.get("form_city", ""),
        "{{source_state}}": fm.get("form_state", ""),
    }
    for k, v in rep.items():
        tpl = tpl.replace(k, v)
    return tpl


def faq_block(faq_tag, fm) -> tuple[str, dict | None]:
    items = []
    q, parts = None, []
    for el in faq_tag.children:
        if isinstance(el, NavigableString):
            continue
        if el.name == "h3":
            if q is not None:
                items.append((q, parts))
            q, parts = el, []
        elif q is not None:
            parts.append(el)
    if q is not None:
        items.append((q, parts))
    if not items:
        return "", None, 0
    det, ld = [], []
    for i, (qel, parts) in enumerate(items):
        qh = "".join(str(c) for c in qel.contents)
        ah = "".join(str(p) for p in parts)
        qt = re.sub(r"\s+", " ", qel.get_text(" ", strip=True))
        at = re.sub(r"\s+", " ", " ".join(p.get_text(" ", strip=True) for p in parts)).strip()
        at = re.sub(r"\s+([,.;:?!])", r"\1", at)
        det.append(f'<details{" open" if i == 0 else ""}><summary><h3>{qh}</h3></summary><div>{ah}</div></details>')
        ld.append({"@type": "Question", "name": qt, "acceptedAnswer": {"@type": "Answer", "text": at}})
    heading = fm.get("faq_heading") or "Questions investors ask"
    sec = f'<section class="sec" id="faq"><div class="col"><h2>{heading}</h2></div><div class="faq col">{"".join(det)}</div></section>'
    return sec, {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": ld}, len(items)


def sources_block(tag) -> str:
    lis = "".join(str(li) for li in tag.find_all("li"))
    return f'<section class="sec sources" id="sources"><div class="col"><h2>Sources</h2><ol>{lis}</ol></div></section>'


def navy_break(fm, has_form) -> str:
    if fm.get("break_html"):
        inner = fm["break_html"]
    else:
        href = "#apply" if has_form else "/apply.html"
        title = fm.get("break_title") or "Have a deal on the table?"
        text = fm.get("break_text") or ("Send the address, the numbers and your exit. Our lending partner's team reviews it and tells you whether it fits "
                                        "and on what terms. The lender makes every credit decision.")
        inner = (f'<div class="break-cta"><div><h2>{title}</h2><p>{text}</p></div>'
                 f'<div class="ctas"><a class="btn" href="{href}">Send my deal</a><a class="btn ghost" href="/hard-money-calculator/">Run the numbers</a></div></div>')
    return f'<section class="break navy"><div class="col wide">{inner}</div></section>'


def gold_break(fm, has_form, form) -> str:
    if has_form:
        return f'<section class="break gold" id="deal">{form}</section>'
    title = fm.get("gold_title") or "Ready when your next deal is"
    text = fm.get("gold_text") or "Tell us about the property and the plan. The lending partner's team reviews it and comes back on whether it fits."
    return (f'<section class="break gold"><div class="col wide"><div class="break-cta"><div><h2>{title}</h2><p>{text}</p></div>'
            f'<div class="ctas"><a class="btn navy" href="/apply.html">Submit a deal</a><a class="btn line" href="/contact/">Ask a question</a></div></div></div></section>')


def wrap_tables(soup):
    for t in soup.find_all("table"):
        if t.parent and "tablewrap" in (t.parent.get("class") or []):
            continue
        w = soup.new_tag("div", attrs={"class": "tablewrap"})
        t.wrap(w)


def convert_images(soup, rel):
    count = 0
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if src.startswith("http") or src.endswith(".svg") or "/images/w/" in src:
            if "/images/w/" in src:
                count += 1
            continue
        if not src.startswith("/"):
            raise SystemExit(f"{rel}: relative image src {src}")
        alt = img.get("alt") or IMAGES.get(Path(src).stem, "")
        if not alt:
            raise SystemExit(f"{rel}: image without alt {src}")
        new = BeautifulSoup(img_html(src, alt, cls=" ".join(img.get("class") or [])), "html.parser").img
        img.replace_with(new)
        count += 1
    for ph in soup.find_all("photo"):
        fig = BeautifulSoup(figure_html(ph.get("src"), ph.get("alt"), ph.get("caption", "")), "html.parser").figure
        ph.replace_with(fig)
        count += 1
    return count


def render(src: Path, cssv: str, report: list) -> tuple[str, str]:
    fm, body = parse_source(src)
    rel = out_rel(src)
    soup = BeautifulSoup(body, "html.parser")

    page_css, page_js = "", ""
    pa = soup.find("page-assets")
    if pa:
        for el in pa.find_all("style"):
            page_css += str(el)
        for el in pa.find_all("script"):
            page_js += str(el)
        pa.decompose()

    faq_html, faq_ld, nfaq = "", None, 0
    fq = soup.find("faq")
    if fq:
        faq_html, faq_ld, nfaq = faq_block(fq, fm)
        fq.decompose()
    src_html = ""
    st = soup.find("sources")
    if st:
        src_html = sources_block(st)
        st.decompose()

    gold_custom = ""
    gb = soup.find("gold-band")
    if gb:
        gold_custom = f'<section class="break gold"{(" id=" + chr(34) + gb["id"] + chr(34)) if gb.get("id") else ""}><div class="col">{"".join(str(c) for c in gb.contents)}</div></section>'
        gb.decompose()
    has_form = soup.find("deal-form") is not None
    form = form_html(fm) if has_form else ""
    df = soup.find("deal-form")
    if df:
        df.decompose()

    raw_mode = fm.get("layout") == "raw"
    if not raw_mode:
        wrap_tables(soup)
    n_imgs = convert_images(soup, rel)

    # Top-level blocks: loose elements are grouped into legacy sections.
    blocks, loose = [], []
    for el in list(soup.contents):
        if isinstance(el, NavigableString):
            if el.strip():
                loose.append(str(el))
            continue
        if el.name == "section" or (raw_mode and el.name in ("div", "figure")):
            if loose:
                blocks.append('<section class="legacy">' + "".join(loose) + "</section>")
                loose = []
            blocks.append(str(el))
        else:
            loose.append(str(el))
    if loose:
        blocks.append('<section class="legacy">' + "".join(loose) + "</section>")

    hero, rest, hero_src, crumb_ld = hero_html(fm, rel, has_form)
    lead_offset = 0
    if rest:
        blocks.insert(0, f'<section class="rail"><p class="lead">{rest}</p></section>')
        lead_offset = 1

    # Make sure the page carries at least two in-body photos.
    if not fm.get("no_auto_images"):
        pool = [n for n in pool_for(rel) if resolve_image(n) != hero_src]
        used = set(re.findall(r"/images/w/([a-z0-9-]+)-\d+\.webp", "".join(blocks)))
        pool = [n for n in pool if n not in used]
        want = max(0, 2 - n_imgs)
        slots = [1 + lead_offset, 4 + lead_offset]
        for k in range(want):
            name = pool[k % len(pool)]
            at = min(slots[k] + k, len(blocks))
            blocks.insert(at, figure_html(name))
            n_imgs += 1

    # Color rhythm: hero, white, navy break, white, gold break (form), white.
    if len(blocks) >= 6:
        nav_at = max(2, round(len(blocks) * 0.4))
    else:
        nav_at = min(2, len(blocks))
    if not fm.get("no_breaks"):
        blocks.insert(nav_at, navy_break(fm, has_form))
    main = '<main id="main">' + "".join(blocks)
    if gold_custom:
        main += gold_custom
    elif not fm.get("no_breaks") or has_form:
        main += gold_break(fm, has_form, form)
    main += faq_html + src_html
    if fm.get("show_disclosure", "yes") != "no":
        main += f'<section class="sec"><div class="col"><p class="disclose">{DISCLOSURE} All financing is arranged for business purposes only and secured by non-owner-occupied investment property. Not a commitment to lend. All loans subject to underwriting, property review, and approval by the lender. Terms vary by property, borrower experience, and exit strategy.</p></div></section>'
    main += "</main>"

    ld = []
    if rel == "index.html":
        ld.append({"@context": "https://schema.org", "@type": "Organization", "name": "Dominion Hard Money",
                   "url": SITE + "/", "logo": SITE + "/images/dominion-logo.svg",
                   "description": "Dominion Hard Money brings real estate investors to third-party private lending partners. It does not lend its own funds.",
                   "parentOrganization": {"@type": "Organization", "name": "Dominion Digital Group"}})
    if crumb_ld:
        ld.append(crumb_ld)
    if faq_ld:
        ld.append(faq_ld)
    extra = PAGES / (rel[:-5] + ".ld.json")
    if extra.exists():
        ld.extend(json.loads(extra.read_text(encoding="utf-8")))

    doc = (head_html(fm, rel, ld, hero_src, page_css, cssv)
           + '<body>\n<a class="skip" href="#main">Skip to content</a>\n'
           + header_html() + "\n" + hero + "\n" + main + "\n" + footer_html() + "\n"
           + page_js + "\n</body>\n</html>\n")
    report.append({"rel": rel, "faqs": nfaq, "imgs": n_imgs, "form": has_form, "fm": fm})
    return rel, doc


# --------------------------------------------------------------------------
# Blog index and sitemap (formats kept compatible with weekly_news.py)
# --------------------------------------------------------------------------
ENTRY_RE = re.compile(r'<div class="post"><a href="(?P<url>[^"]+)">(?P<title>.*?)</a><p>(?P<blurb>.*?)</p></div>', re.S)
POST_RE = re.compile(r"^(?P<slug>.+)-(?P<ts>\d{13})\.html$")


def blog_entries(previous_index: str) -> str:
    known = {m.group("url"): (m.group("title"), m.group("blurb")) for m in ENTRY_RE.finditer(previous_index)}
    posts = []
    for p in (ROOT / "blog").glob("*.html"):
        m = POST_RE.match(p.name)
        if m:
            posts.append((int(m.group("ts")), p))
    posts.sort(reverse=True)
    out = []
    for ts, p in posts:
        url = f"{SITE}/blog/{p.name}"
        if url in known:
            t, b = known[url]
        else:
            raw = p.read_text(encoding="utf-8")
            t = html.escape(html.unescape(re.search(r"<title>(.*?)</title>", raw, re.S).group(1)).split("|")[0].strip(), quote=False)
            b = html.escape(re.search(r'<meta name="description" content="([^"]*)"', raw).group(1), quote=False)
        out.append(f'<div class="post"><a href="{url}">{t}</a><p>{b}</p></div>')
    return "".join(out)


URL_RE = re.compile(r"\s*<url><loc>(?P<loc>[^<]+)</loc><lastmod>(?P<lastmod>[^<]+)</lastmod></url>")


def sitemap_key(loc: str) -> str:
    return loc[:-1] + "/index.html" if loc.endswith("/") else loc


def write_sitemap(report):
    old = {}
    sm = ROOT / "sitemap.xml"
    if sm.exists():
        old = {m.group("loc"): m.group("lastmod") for m in URL_RE.finditer(sm.read_text(encoding="utf-8"))}
    entries = {}
    for r in report:
        fm = r["fm"]
        if "noindex" in (fm.get("robots") or ""):
            continue
        can = fm.get("canonical") or url_of(r["rel"])
        if can != url_of(r["rel"]):
            continue  # a page that defers to another canonical is not listed
        entries[can] = TODAY
    for p in (ROOT / "blog").glob("*.html"):
        if POST_RE.match(p.name):
            entries.setdefault(f"{SITE}/blog/{p.name}", old.get(f"{SITE}/blog/{p.name}", TODAY))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc in sorted(entries, key=sitemap_key):
        lines.append(f"  <url><loc>{loc}</loc><lastmod>{entries[loc]}</lastmod></url>")
    lines.append("</urlset>")
    sm.write_text("\n".join(lines) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------
def check(rel: str, doc: str, r: dict, problems: list):
    soup = BeautifulSoup(doc, "html.parser")
    h1s = soup.find_all("h1")
    if len(h1s) != 1:
        problems.append(f"{rel}: {len(h1s)} h1")
    body = soup.body
    txt = visible_text(body)
    txt = txt.replace("— Jesse Duplantis", "")
    for m in DASH_RE.finditer(txt):
        problems.append(f"{rel}: dash in visible text: ...{txt[max(0, m.start() - 50):m.end() + 30]!r}")
        break
    for attr in ("title",):
        pass
    t = soup.title.get_text() if soup.title else ""
    d = soup.find("meta", attrs={"name": "description"})
    for label, val in (("title", t), ("description", d.get("content", "") if d else "")):
        if DASH_RE.search(val):
            problems.append(f"{rel}: dash in {label}")
    base = Path(rel).name
    if base not in EXEMPT_FAQ and rel != "404.html" and not (3 <= r["faqs"] <= 6):
        problems.append(f"{rel}: {r['faqs']} FAQs")
    if r["imgs"] < 2:
        problems.append(f"{rel}: only {r['imgs']} in-body images")
    for img in body.find_all("img"):
        if not img.get("alt") and img.get("alt") != "":
            problems.append(f"{rel}: img without alt")
        if not (img.get("width") and img.get("height")):
            problems.append(f"{rel}: img without dimensions {img.get('src')}")
    for a in body.find_all("a", href=True):
        h = a["href"]
        if h.startswith(SITE):
            h = h[len(SITE):] or "/"
        if not h.startswith("/") or h.startswith("//"):
            continue
        path = h.split("#")[0].split("?")[0]
        if not path:
            continue
        if not resolves(path):
            problems.append(f"{rel}: broken link {a['href']}")
    faqsec = soup.find(id="faq")
    if faqsec is not None:
        qs = {re.sub(r"\W+", " ", h.get_text()).strip().lower() for h in faqsec.find_all("h3")}
        for h in body.find_all(["h3", "h4"]):
            if h.find_parent(id="faq") is None and re.sub(r"\W+", " ", h.get_text()).strip().lower() in qs:
                problems.append(f"{rel}: FAQ question repeated in the body: {h.get_text()[:60]!r}")
    low = txt.lower()
    for phrase in ("we lend", "our loans", "we fund", "guaranteed", "approval in", "licensed broker", "we are licensed"):
        mm = re.search(r"\b" + re.escape(phrase) + r"\b", low)
        if mm:
            i = mm.start()
            problems.append(f"{rel}: phrase {phrase!r}: ...{txt[max(0, i - 60):i + 60]!r}")


REDIRECTS = None


def resolves(path: str) -> bool:
    global REDIRECTS
    if REDIRECTS is None:
        REDIRECTS = []
        for line in (ROOT / "_redirects").read_text().splitlines():
            parts = line.split()
            if len(parts) >= 2 and not line.startswith("#"):
                REDIRECTS.append(parts[0])
    p = ROOT / path.lstrip("/")
    if path.endswith("/"):
        if (p / "index.html").exists():
            return True
    elif p.is_file() or (p.with_suffix(".html").is_file() if not p.suffix else False) or (p / "index.html").is_file():
        return True
    for frm in REDIRECTS:
        if frm == path or (frm.endswith("*") and path.startswith(frm[:-1])):
            return True
    return False


def main(argv) -> int:
    unknown = [a for a in argv if a.startswith("-") and a not in ("--check", "--only")]
    if unknown:
        print(__doc__)
        return 2
    cssv = css_version()
    report, problems, outputs = [], [], []
    index_src = PAGES / "blog" / "index.src.html"
    prev_index = (ROOT / "blog" / "index.html").read_text(encoding="utf-8") if (ROOT / "blog" / "index.html").exists() else ""
    only = None
    if "--only" in argv:
        only = argv[argv.index("--only") + 1].split(",")
    for src in sorted(PAGES.rglob("*.src.html")):
        if src == index_src:
            continue
        if only is not None and not any(out_rel(src).startswith(o.strip("/")) or out_rel(src) == o for o in only):
            continue
        rel, doc = render(src, cssv, report)
        (ROOT / rel).parent.mkdir(parents=True, exist_ok=True)
        (ROOT / rel).write_text(doc, encoding="utf-8")
        outputs.append((rel, doc))
    # Blog index last, so it sees every post on disk.
    if index_src.exists() and (only is None or "blog/index.html" in only):
        text = index_src.read_text(encoding="utf-8").replace("<!--posts--><!--/posts-->", "<!--posts-->" + blog_entries(prev_index) + "<!--/posts-->", 1)
        tmp = PAGES / "blog" / ".index.tmp.src.html"
        tmp.write_text(text, encoding="utf-8")
        try:
            _, doc = render(tmp, cssv, report)
        finally:
            tmp.unlink()
        report[-1]["rel"] = "blog/index.html"
        (ROOT / "blog" / "index.html").write_text(doc, encoding="utf-8")
        outputs.append(("blog/index.html", doc))
    if only is None:
        write_sitemap(report)
    print(f"built {len(outputs)} pages")
    if "--check" in argv:
        for (rel, doc), r in zip(outputs, report):
            check(rel, doc, r, problems)
        for p in problems:
            print("PROBLEM", p)
        print(f"{len(problems)} problems")
        return 1 if problems else 0
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
