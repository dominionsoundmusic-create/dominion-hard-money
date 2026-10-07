#!/usr/bin/env python3
"""One-time clean-up of the extracted sources (run after extract.py).

* em and en dashes in visible copy become commas, colons or "to"
* legacy per-page <style> blocks are dropped (site.css replaces them)
* blog posts: the in-article "Common questions" block is removed when the
  same questions are carried by the page's <faq> block
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString

ROOT = Path(__file__).resolve().parents[2]
PAGES = ROOT / "_src" / "pages"

SOFT = {"which", "who", "where", "when", "while", "though", "although", "and", "but", "or", "so", "not",
        "rather", "because", "including", "especially", "even", "usually", "often", "plus", "then", "than",
        "with", "without", "before", "after", "until", "unless", "whether", "if", "nor", "yet", "instead",
        "typically", "commonly", "sometimes", "mostly", "mainly", "largely", "partly", "since"}

NUM = r"(?:\$?\d[\d,.]*(?:%|k|K|M|MM)?)"


def _single_all(s, single):
    out, pos = [], 0
    for m in re.finditer(r"\s*[\u2014\u2013]\s*", s):
        before = s[pos:m.start()]
        out.append(before)
        prev = "".join(out)
        after = s[m.end():]
        res = single(_M(prev, after))
        # single() returns prev-with-punctuation + after; we only need the joint
        joint = res[len(prev.rstrip()):len(res) - len(after)] if res.endswith(after) else " "
        out = [prev.rstrip() + joint]
        pos = m.end()
    out.append(s[pos:])
    return "".join(out)


class _M:
    def __init__(self, before, after):
        self._g = (None, before, after)

    def group(self, i):
        return self._g[i]


def fix_dashes(s: str) -> str:
    if not s:
        return s
    s = s.replace("&mdash;", "—").replace("&ndash;", "–").replace("&#8212;", "—").replace("&#8211;", "–")
    # numeric ranges: 600–649, $150–$300, 70–75%, 12–24 months
    s = re.sub(rf"({NUM})\s*[–—]\s*({NUM})", r"\1 to \2", s)
    # word ranges without spaces: Jan–Mar
    s = re.sub(r"(\w)[–](\w)", r"\1 to \2", s)
    # paired em dashes inside one sentence: A — B — C  ->  A, B, C
    s = re.sub(r"\s*[—–]\s*([^—–.!?]{1,140}?)\s*[—–]\s*", r", \1, ", s)

    def single(m):
        before, after = m.group(1), m.group(2)
        word = re.match(r"[A-Za-z']+", after)
        w = word.group(0).lower() if word else ""
        if not before.strip():
            return after
        if w in SOFT or w.endswith(("ed", "ing")):
            return before.rstrip() + ", " + after
        return before.rstrip() + ": " + after

    s = re.sub(r"(\S?)\s*[\u2014\u2013]\s*", lambda m: single(_Ctx(m, s)), s) if False else _single_all(s, single)
    s = s.replace(",,", ",").replace(", .", ".").replace(":,", ":").replace(", :", ":")
    s = re.sub(r",\s*([.?!;:])", r"\1", s)
    return s


def fix_soup(soup):
    for node in list(soup.find_all(string=True)):
        if node.parent and node.parent.name in ("script", "style"):
            continue
        if re.search("[—–]", node):
            node.replace_with(NavigableString(fix_dashes(str(node))))


FM_KEYS = ("title", "description", "og_title", "og_description", "h1", "lede", "hero_alt", "hero_caption",
           "cta", "faq_heading", "byline")


def main() -> int:
    n = 0
    for p in sorted(PAGES.rglob("*.src.html")):
        raw = p.read_text(encoding="utf-8")
        head, _, body = raw[4:].partition("\n---\n")
        lines = []
        for line in head.splitlines():
            k, _, v = line.partition(":")
            if k.strip() in FM_KEYS or k.strip() == "crumbs":
                v = fix_dashes(v)
            lines.append(f"{k}:{v}" if _ else line)
        # page assets: keep scripts, drop legacy styles
        def pa(m):
            scripts = re.findall(r"(?is)<script\b.*?</script>", m.group(1))
            return ("<page-assets>\n" + "\n".join(scripts) + "\n</page-assets>") if scripts else ""
        body = re.sub(r"(?is)<page-assets>(.*?)</page-assets>", pa, body)
        soup = BeautifulSoup(body, "html.parser")
        fix_soup(soup)
        if p.parent.name == "blog" and soup.find("faq"):
            art = soup.find("article")
            if art:
                for h2 in art.find_all("h2"):
                    if re.search(r"(?i)common questions|frequently asked|questions", h2.get_text()):
                        # remove h2 and following h3/p until a non-faq element or article end
                        nxt = h2.find_next_sibling()
                        h2.decompose()
                        while nxt is not None and nxt.name in ("h3", "p") and not (nxt.name == "p" and nxt.find("a") and "Submit" in nxt.get_text()):
                            nn = nxt.find_next_sibling()
                            if nxt.name == "p" and nn is not None and nn.name not in ("h3", "p"):
                                # last answer paragraph before the CTA box / sourcing line
                                nxt.decompose()
                                break
                            nxt.decompose()
                            nxt = nn
                        break
        out = "---\n" + "\n".join(lines) + "\n---\n" + str(soup)
        if out != raw:
            p.write_text(out, encoding="utf-8")
            n += 1
    print(f"normalized {n} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
