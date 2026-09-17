#!/usr/bin/env python3
"""Generate one researched news post for the Dominion Hard Money blog.

Run weekly by .github/workflows/weekly-news.yml. The script researches a
subject with live web search, drafts a post, then puts the draft through three
mandatory guards. Every guard fails closed: on any failure nothing is written
to the working tree and the process exits non-zero, so the week is skipped
rather than published as a weak or non-compliant post.

Nothing is written until all guards have passed.
"""

from __future__ import annotations

import html
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
BLOG = REPO / "blog"
INDEX = BLOG / "index.html"
SITEMAP = REPO / "sitemap.xml"

SITE = "https://dominionhardmoney.com"
MODEL = "claude-opus-5"

# Verified against the bundled claude-api reference, not recalled: the current
# dated web search variant, supported on claude-opus-5, no beta header. It runs
# code execution internally, so code_execution must NOT also be declared.
WEB_SEARCH_TOOL = {"type": "web_search_20260209", "name": "web_search", "max_uses": 12}

DISCLOSURE = (
    "Dominion Hard Money does not lend its own funds; it arranges financing "
    "through third-party lending partners."
)

# Dominion is not a lender and never calls itself a broker.
BANNED = [
    "we lend",
    "we fund",
    "our funds",
    "our capital",
    "we finance",
    "we are licensed",
    "guaranteed approval",
    "brokerage",
    "we broker",
]
NEVER_NAME = ["cogo capital", "cogo"]

# The Submit Your Deal call to action the existing posts already use, rendered
# with the gold .cta-box the post stylesheet defines.
CTA_HEADING = "Ready to Work With a Team That's Built for Investors?"
CTA_BODY = (
    "Submit your deal and get a straightforward review from a team that places "
    "investor financing every day."
)
CTA_HREF = SITE
CTA_LABEL = "Submit Your Deal"

ALLOWED_TAGS = {"p", "h2", "h3", "strong", "em", "ul", "ol", "li", "a", "br"}

LOOKBACK = 6


class Skip(Exception):
    """A guard rejected the draft. Commit nothing, exit non-zero."""


def fail(reason: str) -> None:
    raise Skip(reason)


# --------------------------------------------------------------------------
# Reading what is already published
# --------------------------------------------------------------------------

POST_RE = re.compile(r"^(?P<slug>.+)-(?P<ts>\d{13})\.html$")


def post_files() -> list[tuple[int, str, Path]]:
    """Every published post as (timestamp, slug, path), newest first."""
    found = []
    for path in BLOG.glob("*.html"):
        m = POST_RE.match(path.name)
        if m:
            found.append((int(m.group("ts")), m.group("slug"), path))
    found.sort(key=lambda row: row[0], reverse=True)
    return found


def strip_tags(fragment: str) -> str:
    text = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", fragment)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def article_of(raw: str) -> str:
    m = re.search(r"(?is)<article\b[^>]*>(.*?)</article>", raw)
    if m:
        return m.group(1)
    # Older posts were truncated before their closing tag; fall back to the
    # body region so the anti-sameness read still sees real copy.
    m = re.search(r'(?is)<article\b[^>]*>(.*?)(?=<footer\b|</body>)', raw)
    return m.group(1) if m else ""


def title_of(raw: str) -> str:
    m = re.search(r"(?is)<title>(.*?)</title>", raw)
    if not m:
        return ""
    return html.unescape(m.group(1)).split("|")[0].strip()


def opening_of(raw: str) -> str:
    for para in re.findall(r"(?is)<p\b[^>]*>(.*?)</p>", article_of(raw)):
        text = strip_tags(para)
        if len(text) > 80:
            return text
    return ""


def recent_posts(limit: int = LOOKBACK) -> list[dict]:
    out = []
    for _ts, slug, path in post_files()[:limit]:
        raw = path.read_text(encoding="utf-8")
        out.append(
            {
                "slug": slug,
                "title": title_of(raw),
                "opening": opening_of(raw),
            }
        )
    return out


# --------------------------------------------------------------------------
# Drafting
# --------------------------------------------------------------------------

FIELDS = ["TITLE", "SLUG", "META", "BLURB", "TOPIC", "SOURCING", "STAT", "BODY"]

SYSTEM = f"""You write the weekly news post for the Dominion Hard Money blog.

Dominion Hard Money is NOT a lender and is NOT a broker. It arranges financing
for real estate investors through third-party lending partners. Never write that
Dominion lends, funds, finances, brokers, or is licensed, and never write about
its own funds or capital. Never name Cogo Capital or any lending partner.

Audience: working real estate investors. House voice is plain, specific and
unsentimental. Short declarative sentences. No hype, no filler openers, no
"in today's market". Lead with the fact, then what it changes for the reader's
underwriting. It is fine to say a number is bad news.

Every post must be built on live data you looked up with web search this run,
not on anything you remember. Research first, then write. At least one concrete
statistic must carry a named source and a date, both stated in the prose.

Write the article body as an HTML fragment using only these tags:
{", ".join(sorted(ALLOWED_TAGS))}. Open with one or two paragraphs of lede, then
use <h2> section headings. Do not include an <h1>, a title, a byline, a call to
action, a closing sourcing note, or a disclosure. Those are added around your
text. Aim for 700 to 1100 words.

Reply with exactly these delimited fields and nothing else:

===TITLE===
The headline. Plain sentence case, no colons-and-subtitle formula.
===SLUG===
lowercase-hyphenated-slug derived from the title, at most 70 characters
===META===
One meta description sentence, 140 to 160 characters.
===BLURB===
One sentence for the blog index, at most 130 characters.
===TOPIC===
Six to twelve words naming the specific subject, for a duplicate check.
===SOURCING===
One sentence naming where the figures came from and how current they are.
===STAT===
value: the headline statistic exactly as it appears in your prose
source: the organisation that published it, exactly as named in your prose
date: the period it covers, exactly as written in your prose
===BODY===
The HTML fragment.
"""


def build_prompt(previous: list[dict]) -> str:
    lines = [
        "Here are the last six posts on the blog. Read the titles and opening",
        "paragraphs, then pick a DIFFERENT subject. Not a variation, not the",
        "same subject from another angle, not the same underlying data with a",
        "new headline. A different subject.",
        "",
    ]
    for i, post in enumerate(previous, 1):
        lines.append(f"--- Post {i} ---")
        lines.append(f"Title: {post['title']}")
        lines.append(f"Opening: {post['opening']}")
        lines.append("")
    lines += [
        "Now search the web for what has actually happened recently in real",
        "estate investor financing: rates, lending volume, flipping and rental",
        "returns, delinquency, construction and housing supply, regulation, or",
        "anything else that changes how an investor underwrites a deal this",
        "month. Prefer named primary sources that publish on a schedule.",
        "",
        "Pick the one story that is most useful to an investor right now and",
        "write this week's post about it, in the required field format.",
    ]
    return "\n".join(lines)


def draft(previous: list[dict]) -> dict:
    import anthropic

    client = anthropic.Anthropic()
    messages = [{"role": "user", "content": build_prompt(previous)}]

    # web_search can return stop_reason "pause_turn" on a long research turn;
    # hand the partial turn back to continue it.
    for _ in range(8):
        with client.messages.stream(
            model=MODEL,
            max_tokens=16000,
            system=SYSTEM,
            messages=messages,
            tools=[WEB_SEARCH_TOOL],
            thinking={"type": "adaptive"},
            output_config={"effort": "high"},
        ) as stream:
            response = stream.get_final_message()

        if response.stop_reason == "refusal":
            fail("model declined the request (stop_reason: refusal)")
        if response.stop_reason == "max_tokens":
            fail("draft hit max_tokens and is truncated")
        if response.stop_reason != "pause_turn":
            break
        messages.append({"role": "assistant", "content": response.content})
    else:
        fail("web search did not settle after 8 continuations")

    text = "\n".join(
        block.text for block in response.content if getattr(block, "type", "") == "text"
    ).strip()
    if not text:
        fail("model returned no text")
    return parse_fields(text)


def parse_fields(text: str) -> dict:
    parts = re.split(r"(?m)^===([A-Z]+)===\s*$", text)
    fields: dict[str, str] = {}
    for name, value in zip(parts[1::2], parts[2::2]):
        fields[name] = value.strip()
    missing = [f for f in FIELDS if not fields.get(f)]
    if missing:
        fail(f"draft is missing required fields: {', '.join(missing)}")
    return fields


# --------------------------------------------------------------------------
# Guard 1: anti-sameness
# --------------------------------------------------------------------------

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "can", "did", "do",
    "does", "for", "from", "has", "have", "how", "in", "is", "it", "its", "much",
    "no", "not", "of", "on", "one", "or", "that", "the", "their", "then", "there",
    "they", "this", "to", "up", "was", "were", "what", "when", "which", "who",
    "why", "will", "with", "you", "your",
}


def stem(word: str) -> str:
    """Crude suffix stripping so 'national' matches 'nationally' and
    'flip' matches 'flipping'. Good enough for a duplicate check."""
    if len(word) > 4 and word.endswith("ies"):
        word = word[:-3] + "y"
    elif len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
        word = word[:-1]
    if len(word) > 4 and word.endswith("ly"):
        word = word[:-2]
    if len(word) > 5 and word.endswith("ing"):
        word = word[:-3]
    elif len(word) > 4 and word.endswith("ed"):
        word = word[:-2]
    # "flipping" -> "flipp" -> "flip"
    if len(word) > 3 and word[-1] == word[-2] and word[-1] not in "aeiou":
        word = word[:-1]
    return word


def tokens(text: str) -> set[str]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {stem(w) for w in words if len(w) > 2 and w not in STOPWORDS}


def guard_anti_sameness(fields: dict, previous: list[dict], slug: str) -> None:
    new_title = tokens(fields["TITLE"])
    new_topic = tokens(fields["TOPIC"])
    if not new_title:
        fail("new title has no content words to compare")

    for post in previous:
        if slug == post["slug"]:
            fail(f"slug collides with an existing post: {slug}")

        old_title = tokens(post["title"])
        if not old_title:
            continue

        shared = new_title & old_title
        union = new_title | old_title
        jaccard = len(shared) / len(union) if union else 0.0
        if jaccard >= 0.40 or len(shared) >= 3:
            fail(
                f"title overlaps a recent post ({len(shared)} shared words, "
                f"jaccard {jaccard:.2f}): {post['title']!r} -- "
                f"shared: {', '.join(sorted(shared))}"
            )

        if new_topic:
            topic_shared = new_topic & old_title
            if len(topic_shared) / len(new_topic) >= 0.60:
                fail(
                    f"topic restates a recent title: {post['title']!r} -- "
                    f"shared: {', '.join(sorted(topic_shared))}"
                )

            # The same subject told in different words: measure the topic
            # against everything the old post says up front, not its title
            # alone. A false positive here costs a skipped week, which is the
            # outcome we want when in doubt.
            covered = old_title | tokens(post["opening"])
            shared_cover = new_topic & covered
            if len(shared_cover) / len(new_topic) >= 0.50:
                fail(
                    "topic is already covered by a recent post: "
                    f"{post['title']!r} -- shared: {', '.join(sorted(shared_cover))}"
                )


# --------------------------------------------------------------------------
# Guard 2: hard specific
# --------------------------------------------------------------------------

MONTHS = (
    "January|February|March|April|May|June|July|August|September|October|"
    "November|December"
)
DATE_RE = re.compile(
    r"(?ix)"
    r"(Q[1-4]\s+\d{4})"
    r"|((first|second|third|fourth)\s+quarter\s+(of\s+)?\d{4})"
    rf"|(({MONTHS})\s+\d{{1,2}},?\s+\d{{4}})"
    rf"|(({MONTHS})\s+\d{{4}})"
    r"|(\d{4}-\d{2}-\d{2})"
    r"|(week\s+of\s+\w+\s+\d{1,2},?\s+\d{4})"
)


def parse_stat(block: str) -> dict:
    stat = {}
    for line in block.splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip().lower()
            if key in ("value", "source", "date"):
                stat[key] = value.strip()
    for key in ("value", "source", "date"):
        if not stat.get(key):
            fail(f"STAT block is missing '{key}'")
    return stat


def guard_hard_specific(fields: dict, body_text: str) -> None:
    stat = parse_stat(fields["STAT"])
    haystack = body_text.lower()

    number = re.search(r"\d[\d,]*(?:\.\d+)?", stat["value"])
    if not number:
        fail(f"STAT value carries no number: {stat['value']!r}")
    if number.group(0).lower() not in haystack:
        fail(
            f"the cited figure {number.group(0)!r} does not appear in the "
            "article body"
        )

    if len(stat["source"]) < 3:
        fail(f"STAT source is not a name: {stat['source']!r}")
    if stat["source"].lower() not in haystack:
        fail(f"the named source {stat['source']!r} does not appear in the article body")

    if not DATE_RE.search(stat["date"]):
        fail(f"STAT date is not a recognisable date or period: {stat['date']!r}")
    if stat["date"].lower() not in haystack:
        fail(f"the date {stat['date']!r} does not appear in the article body")

    if not DATE_RE.search(body_text):
        fail("article body states no date alongside its figures")
    if len(re.findall(r"\d", body_text)) < 5:
        fail("article body is not carrying real numbers")


# --------------------------------------------------------------------------
# Guard 3: compliance
# --------------------------------------------------------------------------


def guard_compliance(article_html: str, article_text: str) -> None:
    haystack = article_text.lower()
    for phrase in BANNED:
        if phrase in haystack:
            i = haystack.find(phrase)
            fail(
                f"banned phrase {phrase!r} in draft: "
                f"...{article_text[max(0, i - 70):i + len(phrase) + 70].strip()}..."
            )
    for name in NEVER_NAME:
        if name in haystack:
            fail(f"draft names {name!r}, which must never appear in a post")
    if DISCLOSURE.lower() not in haystack:
        fail("required disclosure is missing from the article body")


def guard_markup(body: str) -> None:
    for tag in set(re.findall(r"</?([a-zA-Z0-9]+)", body)):
        if tag.lower() not in ALLOWED_TAGS:
            fail(f"draft body uses a disallowed tag: <{tag}>")
    if re.search(r"(?i)\son[a-z]+\s*=", body):
        fail("draft body carries an inline event handler attribute")
    if re.search(r"(?i)javascript:", body):
        fail("draft body carries a javascript: URL")
    if "<h1" in body.lower():
        fail("draft body contains an <h1>; the title belongs in the hero <h2>")


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------


def skeleton() -> tuple[str, str, str]:
    """Style, header and footer lifted verbatim from the newest post."""
    posts = post_files()
    if not posts:
        fail("no existing post to take the skeleton from")
    raw = posts[0][2].read_text(encoding="utf-8")

    style = re.search(r"(?is)<style>.*?</style>", raw)
    header = re.search(r"(?is)<header>.*?</header>", raw)
    footer = re.search(r"(?is)<footer>.*?</footer>", raw)
    if not (style and header and footer):
        fail(f"could not read the skeleton out of {posts[0][2].name}")
    return style.group(0), header.group(0), footer.group(0)


def slugify(raw: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", raw.lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)[:70].strip("-")
    if not slug:
        fail("could not build a slug from the draft")
    return slug


def render_post(fields: dict, slug: str, ts: int) -> str:
    style, header, footer = skeleton()
    published = datetime.fromtimestamp(ts / 1000, tz=timezone.utc)
    pubdate = f"{published:%B} {published.day}, {published.year}"
    # quote=False in text contexts so apostrophes stay literal, the way the
    # existing posts write them. The meta description is an attribute, so it
    # keeps the quote escaping.
    title = html.escape(fields["TITLE"], quote=False)
    canonical = f"{SITE}/blog/{slug}-{ts}.html"
    body = "\n".join(
        ("  " + line.strip() if line.strip() else "")
        for line in fields["BODY"].strip().splitlines()
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | Dominion Hard Money</title>
<meta name="description" content="{html.escape(fields["META"], quote=True)}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">
{style}
</head>
<body>
{header}
<div class="hero">
<h2>{title}</h2>
<div class="meta">Published {pubdate} &bull; Dominion Hard Money</div>
</div>
<div class="content">
<a href="/blog" class="back">&larr; Back to Blog</a>
<article class="blog-post">

{body}

  <div class="cta-box">
    <h3>{html.escape(CTA_HEADING, quote=False)}</h3>
    <p>{html.escape(CTA_BODY, quote=False)}</p>
    <a href="{CTA_HREF}">{CTA_LABEL}</a>
  </div>

  <p>{html.escape(fields["SOURCING"], quote=False)} {DISCLOSURE}</p>

</article>

</div>
{footer}
</body>
</html>
"""


# --------------------------------------------------------------------------
# blog/index.html
# --------------------------------------------------------------------------

ENTRY_RE = re.compile(
    r'<div class="post"><a href="(?P<url>[^"]+)">(?P<title>.*?)</a>'
    r"<p>(?P<blurb>.*?)</p></div>",
    re.S,
)


def rebuild_index(new_blurbs: dict[str, str]) -> str:
    raw = INDEX.read_text(encoding="utf-8")
    known = {
        m.group("url"): (m.group("title"), m.group("blurb"))
        for m in ENTRY_RE.finditer(raw)
    }

    entries = []
    for ts, slug, path in post_files():  # already newest first
        url = f"{SITE}/blog/{slug}-{ts}.html"
        if url in known:
            title, blurb = known[url]
        else:
            title = html.escape(title_of(path.read_text(encoding="utf-8")), quote=False)
            blurb = new_blurbs.get(url, "")
        if not title or not blurb:
            fail(f"no index title or blurb available for {path.name}")
        entries.append(f'<div class="post"><a href="{url}">{title}</a><p>{blurb}</p></div>')

    rebuilt, count = re.subn(
        r'(?s)(<p class="lede">.*?</p>)(.*?)(</div><footer>)',
        lambda m: m.group(1) + "".join(entries) + m.group(3),
        raw,
        count=1,
    )
    if count != 1:
        fail("could not locate the post list in blog/index.html")
    return rebuilt


# --------------------------------------------------------------------------
# sitemap.xml
# --------------------------------------------------------------------------

URL_RE = re.compile(
    r"\s*<url><loc>(?P<loc>[^<]+)</loc><lastmod>(?P<lastmod>[^<]+)</lastmod></url>"
)


def sitemap_key(loc: str) -> str:
    # Reproduces the file's existing order: byte sort of the loc with a
    # trailing slash normalised to /index.html.
    return loc[:-1] + "/index.html" if loc.endswith("/") else loc


def rebuild_sitemap(today: str) -> str:
    raw = SITEMAP.read_text(encoding="utf-8")
    entries: dict[str, str] = {}
    for m in URL_RE.finditer(raw):
        entries[m.group("loc")] = m.group("lastmod")

    if not entries:
        fail("could not parse sitemap.xml")

    prefix = f"{SITE}/blog/"
    live = {
        f"{prefix}{slug}-{ts}.html": None for ts, slug, _path in post_files()
    }

    # Drop blog post URLs whose file is gone; keep everything else untouched.
    for loc in list(entries):
        if loc.startswith(prefix) and loc != prefix and loc not in live:
            del entries[loc]

    # Add every post on disk that the sitemap is missing.
    for loc in live:
        entries.setdefault(loc, today)

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc in sorted(entries, key=sitemap_key):
        lines.append(f"  <url><loc>{loc}</loc><lastmod>{entries[loc]}</lastmod></url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------


def main() -> int:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ANTHROPIC_API_KEY is not set", file=sys.stderr)
        return 1

    try:
        previous = recent_posts()
        if len(previous) < LOOKBACK:
            fail(f"expected {LOOKBACK} previous posts to compare against, found {len(previous)}")

        fields = draft(previous)
        slug = slugify(fields["SLUG"])
        ts = int(time.time() * 1000)

        guard_anti_sameness(fields, previous, slug)
        guard_markup(fields["BODY"])

        post_html = render_post(fields, slug, ts)
        article = article_of(post_html)
        article_text = strip_tags(article)

        guard_hard_specific(fields, article_text)
        guard_compliance(article, article_text)

        # All guards passed. Only now does anything touch the working tree.
        path = BLOG / f"{slug}-{ts}.html"
        if path.exists():
            fail(f"{path.name} already exists")
        path.write_text(post_html, encoding="utf-8")

        url = f"{SITE}/blog/{slug}-{ts}.html"
        INDEX.write_text(
            rebuild_index({url: html.escape(fields["BLURB"], quote=False)}),
            encoding="utf-8",
        )

        published = datetime.fromtimestamp(ts / 1000, tz=timezone.utc)
        SITEMAP.write_text(rebuild_sitemap(f"{published:%Y-%m-%d}"), encoding="utf-8")

        print(f"title:  {fields['TITLE']}")
        print(f"file:   blog/{path.name}")
        print(f"topic:  {fields['TOPIC']}")
        print("guards: anti-sameness, hard specific, compliance -- all passed")
        return 0

    except Skip as exc:
        print(f"SKIPPING THIS WEEK: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
