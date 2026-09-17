#!/usr/bin/env python3
"""Tests for weekly_news.py.

Run from the repository root:

    python .github/scripts/test_weekly_news.py

No network and no API key required: the model call is stubbed, so what is
under test is everything around it -- the four fail-closed checks, the
rendering, and the index and sitemap rebuilds.

Each test runs against a throwaway copy of blog/ and sitemap.xml, so the
working tree is never touched.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import os
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def load_module(sandbox: Path):
    """Fresh copy of weekly_news, pointed at a sandbox instead of the repo."""
    spec = importlib.util.spec_from_file_location("weekly_news", HERE / "weekly_news.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["weekly_news"] = mod
    spec.loader.exec_module(mod)
    mod.REPO = sandbox
    mod.BLOG = sandbox / "blog"
    mod.INDEX = sandbox / "blog" / "index.html"
    mod.SITEMAP = sandbox / "sitemap.xml"
    return mod


BODY = """  <p>Mortgage delinquency among investor-owned properties moved this quarter, and the direction is not the one most operators assumed.</p>

  <h2>What the data says</h2>

  <p>The Mortgage Bankers Association put the seriously delinquent rate on investor loans at 3.8 percent in Q2 2026, up from 3.1 percent a year earlier.</p>

  <p>That is a meaningful move in a portfolio of any size.</p>

  <h2>What it changes</h2>

  <p>Price the reserve, not the optimism. Two extra months of carry is the cheapest insurance available.</p>
"""

GOOD = {
    "TITLE": "Investor Loan Delinquency Is Climbing Again",
    "SLUG": "investor-loan-delinquency-is-climbing-again",
    "META": (
        "Seriously delinquent investor mortgages hit 3.8 percent in Q2 2026. "
        "What the rise means for reserves and underwriting on your next deal."
    ),
    "BLURB": "Seriously delinquent investor mortgages hit 3.8 percent, up from 3.1 a year earlier.",
    "TOPIC": "rising delinquency rates on investor owned mortgages",
    "SOURCING": "Figures are from the Mortgage Bankers Association's Q2 2026 delinquency survey.",
    "STAT": "value: 3.8 percent\nsource: Mortgage Bankers Association\ndate: Q2 2026",
    "BODY": BODY,
}


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(REPO / "blog", self.tmp / "blog")
        shutil.copy2(REPO / "sitemap.xml", self.tmp / "sitemap.xml")
        self.mod = load_module(self.tmp)
        os.environ.setdefault("ANTHROPIC_API_KEY", "test-key-not-used")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def publish(self, **patch):
        """Run the whole pipeline with the model call stubbed out."""
        fields = dict(GOOD)
        fields.update(patch)
        self.mod.draft = lambda previous: dict(fields)
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = self.mod.main()
        return rc, out.getvalue(), err.getvalue()

    def assertSkipped(self, **patch):
        rc, _out, err = self.publish(**patch)
        self.assertEqual(rc, 1, "expected the week to be skipped")
        self.assertIn("SKIPPING THIS WEEK", err)
        return err

    def assertPublished(self, **patch):
        rc, out, err = self.publish(**patch)
        self.assertEqual(rc, 0, f"expected a published post, got: {err}")
        return out

    def new_post(self):
        posts = sorted(self.tmp.glob("blog/*.html"), key=lambda p: p.stat().st_mtime)
        return [p for p in posts if p.name != "index.html"][-1]


# ---------------------------------------------------------------------------


class TestFieldParsing(Base):
    REPLY = (
        "===TITLE===\nT\n===SLUG===\ns\n===META===\nm\n===BLURB===\nb\n"
        "===TOPIC===\nt\n===SOURCING===\nx\n===STAT===\nvalue: 1\nsource: S\n"
        "date: Q2 2026\n===BODY===\n<p>x</p>\n"
    )

    def test_well_formed_reply_parses(self):
        fields = self.mod.parse_fields(self.REPLY)
        for name in self.mod.FIELDS:
            self.assertIn(name, fields)

    def test_each_missing_field_is_rejected(self):
        for name in self.mod.FIELDS:
            with self.subTest(field=name):
                broken = re.sub(rf"===({name})===\n[^=]*", "", self.REPLY)
                with self.assertRaises(self.mod.Skip):
                    self.mod.parse_fields(broken)

    def test_empty_field_is_rejected(self):
        with self.assertRaises(self.mod.Skip):
            self.mod.parse_fields(self.REPLY.replace("===SOURCING===\nx", "===SOURCING===\n"))

    def test_prose_instead_of_fields_is_rejected(self):
        with self.assertRaises(self.mod.Skip):
            self.mod.parse_fields("Sure! Here is this week's post about delinquency.")


class TestSearchEvidence(Base):
    """web_search failures arrive as HTTP 200 with an error object, so a
    silently failed search must not be mistaken for a successful one."""

    class Block:
        def __init__(self, **kw):
            self.__dict__.update(kw)

    def result(self, n):
        return self.Block(
            type="web_search_tool_result",
            content=[self.Block(type="web_search_result") for _ in range(n)],
        )

    def error(self, code, as_dict=False):
        content = {"error_code": code} if as_dict else self.Block(error_code=code)
        return self.Block(type="web_search_tool_result", content=content)

    def check(self, blocks):
        evidence = {"results": 0, "hits": 0, "errors": []}
        self.mod.collect_search_evidence(blocks, evidence)
        self.mod.guard_search_ran(evidence)
        return evidence

    def test_no_search_block_at_all_is_rejected(self):
        with self.assertRaises(self.mod.Skip) as ctx:
            self.check([self.Block(type="text", text="...")])
        self.assertIn("never ran", str(ctx.exception))

    def test_error_object_is_rejected(self):
        for code in ("max_uses_exceeded", "unavailable", "too_many_requests"):
            with self.subTest(code=code), self.assertRaises(self.mod.Skip) as ctx:
                self.check([self.error(code)])
            self.assertIn(code, str(ctx.exception))

    def test_error_delivered_as_dict_is_rejected(self):
        with self.assertRaises(self.mod.Skip):
            self.check([self.error("unavailable", as_dict=True)])

    def test_search_that_returned_nothing_is_rejected(self):
        with self.assertRaises(self.mod.Skip):
            self.check([self.result(0)])

    def test_unrecognised_error_shape_is_rejected(self):
        with self.assertRaises(self.mod.Skip):
            self.check([self.Block(type="web_search_tool_result", content=None)])

    def test_successful_search_is_accepted(self):
        self.assertEqual(self.check([self.result(3)])["hits"], 3)

    def test_one_error_among_successes_is_accepted(self):
        evidence = self.check([self.error("max_uses_exceeded"), self.result(5)])
        self.assertEqual(evidence["hits"], 5)
        self.assertEqual(evidence["errors"], ["max_uses_exceeded"])

    def test_evidence_accumulates_across_paused_turns(self):
        evidence = {"results": 0, "hits": 0, "errors": []}
        self.mod.collect_search_evidence([self.result(2)], evidence)
        self.mod.collect_search_evidence([self.error("max_uses_exceeded")], evidence)
        self.mod.collect_search_evidence([self.result(3)], evidence)
        self.assertEqual((evidence["results"], evidence["hits"]), (3, 5))
        self.mod.guard_search_ran(evidence)


class TestAntiSameness(Base):
    def test_near_copy_of_a_recent_title_is_rejected(self):
        self.assertSkipped(
            TITLE="National Flipping Returns Rose But Texas Did Not Follow", SLUG="a1"
        )

    def test_same_subject_reworded_is_rejected(self):
        self.assertSkipped(
            TITLE="Why Texas Flipping Returns Trail the National Number", SLUG="a2"
        )

    def test_restating_another_recent_post_is_rejected(self):
        self.assertSkipped(
            TITLE="Investor Money Is Cheaper Than a Homeowner Mortgage Again", SLUG="a3"
        )
        self.assertSkipped(
            TITLE="How Fast Can You Close a Fix and Flip Loan Today", SLUG="a4"
        )

    def test_slug_collision_is_rejected(self):
        self.assertSkipped(SLUG="national-flipping-returns-rose-texas-did-not")

    def test_topic_restating_a_recent_title_is_rejected(self):
        self.assertSkipped(TOPIC="common reasons hard money deals fall through")
        self.assertSkipped(TOPIC="calculating ARV and the maximum allowable offer formula")

    def test_topic_already_covered_by_an_opening_is_rejected(self):
        self.assertSkipped(
            TOPIC="flipping returns rose nationally while Texas metros lagged badly"
        )

    def test_genuinely_different_subjects_still_publish(self):
        cases = [
            ("Landlord Insurance Premiums Jumped Again This Year", "b1",
             "rising landlord insurance premiums on rental portfolios"),
            ("Single Family Permits Fell for a Fourth Straight Month", "b2",
             "declining single family building permit volume nationally"),
            ("Property Tax Appeals Are Winning More Often", "b3",
             "success rates on commercial property tax appeals"),
            ("Rent Growth Stalled in the Sun Belt", "b4",
             "stalling apartment rent growth across Sun Belt metros"),
            ("Foreclosure Auction Volume Is Rising Off a Low Base", "b5",
             "foreclosure auction inventory available to investors"),
        ]
        for title, slug, topic in cases:
            with self.subTest(title=title):
                self.assertPublished(TITLE=title, SLUG=slug, TOPIC=topic)


class TestHardSpecific(Base):
    def test_missing_stat_component_is_rejected(self):
        self.assertSkipped(STAT="value: 3.8 percent\nsource: Mortgage Bankers Association")
        self.assertSkipped(STAT="source: Mortgage Bankers Association\ndate: Q2 2026")

    def test_source_absent_from_the_body_is_rejected(self):
        self.assertSkipped(
            STAT="value: 3.8 percent\nsource: Zillow Research\ndate: Q2 2026"
        )

    def test_figure_absent_from_the_body_is_rejected(self):
        self.assertSkipped(
            STAT="value: 9.9 percent\nsource: Mortgage Bankers Association\ndate: Q2 2026"
        )

    def test_vague_date_is_rejected(self):
        for bad in ("recently", "this quarter", "last year"):
            with self.subTest(date=bad):
                self.assertSkipped(
                    STAT=f"value: 3.8 percent\nsource: Mortgage Bankers Association\ndate: {bad}"
                )

    def test_body_with_no_numbers_is_rejected(self):
        self.assertSkipped(
            BODY="<p>Rates feel high right now and nobody is happy about it at all today.</p>"
        )

    def test_recognised_date_formats(self):
        for good in ("Q2 2026", "September 3, 2026", "August 2026", "2026-09-03",
                     "second quarter of 2026"):
            with self.subTest(date=good):
                self.assertIsNotNone(self.mod.DATE_RE.search(good))


class TestCompliance(Base):
    def test_every_banned_phrase_is_rejected(self):
        for phrase in self.mod.BANNED:
            with self.subTest(phrase=phrase):
                err = self.assertSkipped(
                    BODY=BODY.replace("That is a", f"Because {phrase}, that is a", 1)
                )
                self.assertIn(phrase, err)

    def test_banned_phrase_is_case_insensitive(self):
        self.assertSkipped(BODY=BODY.replace("That is a", "We Lend on these, so that is a", 1))

    def test_cogo_capital_is_never_named(self):
        self.assertSkipped(
            BODY=BODY.replace("Mortgage Bankers Association", "Cogo Capital", 1)
        )

    def test_published_post_carries_the_disclosure_in_the_article_body(self):
        self.assertPublished()
        article = self.mod.article_of(self.new_post().read_text(encoding="utf-8"))
        self.assertIn(self.mod.DISCLOSURE, self.mod.strip_tags(article))

    def test_guard_rejects_an_article_without_the_disclosure(self):
        # Exercised against guard_compliance directly. Going through the
        # renderer cannot fail this check, because the template injects the
        # same constant the guard looks for -- so this is the only place the
        # disclosure rule is actually put under test.
        article = "<p>A post with figures but no disclosure at all.</p>"
        with self.assertRaises(self.mod.Skip) as ctx:
            self.mod.guard_compliance(article, self.mod.strip_tags(article))
        self.assertIn("disclosure", str(ctx.exception))

    def test_guard_accepts_an_article_carrying_the_disclosure(self):
        article = f"<p>A post with figures. {self.mod.DISCLOSURE}</p>"
        self.mod.guard_compliance(article, self.mod.strip_tags(article))

    def test_a_disclosure_variant_does_not_satisfy_the_guard(self):
        # What the Sept 14 post actually says in its body: "we arrange"
        # rather than "it arranges". Close is not good enough.
        variant = (
            "<p>Dominion Hard Money does not lend its own funds; we arrange "
            "financing for real estate investors through third-party lending "
            "partners.</p>"
        )
        with self.assertRaises(self.mod.Skip):
            self.mod.guard_compliance(variant, self.mod.strip_tags(variant))


class TestMarkup(Base):
    def test_disallowed_tags_are_rejected(self):
        for snippet in ("<script>alert(1)</script>", "<iframe src=x></iframe>",
                        "<style>p{}</style>", "<h1>Second heading</h1>"):
            with self.subTest(snippet=snippet):
                self.assertSkipped(BODY=BODY + snippet)

    def test_inline_event_handler_is_rejected(self):
        self.assertSkipped(BODY=BODY.replace("<p>Th", "<p onclick='x()'>Th", 1))

    def test_javascript_url_is_rejected(self):
        self.assertSkipped(BODY=BODY + '<p><a href="javascript:alert(1)">x</a></p>')


class TestRendering(Base):
    def setUp(self):
        super().setUp()
        self.assertPublished()
        self.post = self.new_post()
        self.html = self.post.read_text(encoding="utf-8")

    def test_byline_date_matches_the_filename_timestamp(self):
        ts = int(re.search(r"-(\d{13})\.html$", self.post.name).group(1))
        from datetime import datetime, timezone

        stamp = datetime.fromtimestamp(ts / 1000, tz=timezone.utc)
        self.assertIn(f"Published {stamp:%B} {stamp.day}, {stamp.year} &bull;", self.html)

    def test_canonical_matches_the_filename_and_keeps_html(self):
        canonical = re.search(r'rel="canonical" href="([^"]+)"', self.html).group(1)
        self.assertTrue(canonical.endswith(self.post.name))
        self.assertTrue(canonical.endswith(".html"))

    def test_filename_shape(self):
        self.assertRegex(self.post.name, r"^[a-z0-9-]+-\d{13}\.html$")

    def test_no_h1_in_the_article(self):
        self.assertNotIn("<h1", self.mod.article_of(self.html).lower())

    def test_gold_cta_box_with_submit_your_deal(self):
        self.assertIn('<div class="cta-box">', self.html)
        self.assertIn("Submit Your Deal", self.html)

    def test_skeleton_matches_the_previous_newest_post(self):
        reference = (REPO / "blog" / "national-flipping-returns-rose-texas-did-not-1789390800000.html")
        ref = reference.read_text(encoding="utf-8")
        for pattern in (r"(?is)<style>.*?</style>", r"(?is)<header>.*?</header>",
                        r"(?is)<footer>.*?</footer>"):
            self.assertEqual(
                re.search(pattern, ref).group(0),
                re.search(pattern, self.html).group(0),
            )

    def test_apostrophes_stay_literal_in_text(self):
        self.assertNotIn("&#x27;", self.html)

    def test_tags_balance(self):
        for tag in ("div", "article", "p", "h2", "h3", "header", "footer", "html", "body"):
            with self.subTest(tag=tag):
                self.assertEqual(
                    len(re.findall(rf"<{tag}[\s>]", self.html)),
                    len(re.findall(rf"</{tag}>", self.html)),
                )


class TestIndexRebuild(Base):
    def test_new_post_is_first_and_existing_blurbs_survive(self):
        before = (REPO / "blog" / "index.html").read_text(encoding="utf-8")
        old_entries = self.mod.ENTRY_RE.findall(before)

        self.assertPublished()
        after = self.mod.INDEX.read_text(encoding="utf-8")
        new_entries = self.mod.ENTRY_RE.findall(after)

        self.assertEqual(len(new_entries), len(old_entries) + 1)
        self.assertIn(GOOD["TITLE"], new_entries[0][1])
        self.assertIn("3.8 percent", new_entries[0][2])

        # Every pre-existing entry survives byte for byte.
        for entry in old_entries:
            self.assertIn(entry, new_entries)

    def test_entries_are_ordered_newest_first(self):
        self.assertPublished()
        after = self.mod.INDEX.read_text(encoding="utf-8")
        stamps = [
            int(re.search(r"-(\d{13})\.html", url).group(1))
            for url, _title, _blurb in self.mod.ENTRY_RE.findall(after)
        ]
        self.assertEqual(stamps, sorted(stamps, reverse=True))


class TestSitemap(Base):
    def test_new_post_is_added_and_non_blog_entries_are_untouched(self):
        before = self.mod.SITEMAP.read_text(encoding="utf-8")
        self.assertPublished()
        after = self.mod.SITEMAP.read_text(encoding="utf-8")

        non_blog = lambda text: [l for l in text.splitlines() if "/blog/" not in l]
        self.assertEqual(non_blog(before), non_blog(after))
        self.assertIn(self.new_post().name, after)

    def test_existing_order_is_reproduced(self):
        self.assertPublished()
        locs = re.findall(r"<loc>([^<]+)</loc>", self.mod.SITEMAP.read_text(encoding="utf-8"))
        self.assertEqual(locs, sorted(locs, key=self.mod.sitemap_key))

    def test_rebuild_is_idempotent(self):
        first = self.mod.rebuild_sitemap("2026-09-17")
        self.mod.SITEMAP.write_text(first, encoding="utf-8")
        self.assertEqual(first, self.mod.rebuild_sitemap("2026-09-24"))

    def test_posts_missing_from_the_sitemap_are_reconciled(self):
        rebuilt = self.mod.rebuild_sitemap("2026-09-17")
        for _ts, slug, path in self.mod.post_files():
            self.assertIn(path.name, rebuilt, f"{slug} missing from the sitemap")

    def test_deleted_posts_are_dropped(self):
        victim = self.mod.BLOG / "building-a-relationship-with-a-private-lender-1785937888333.html"
        victim.unlink()
        self.assertNotIn(victim.name, self.mod.rebuild_sitemap("2026-09-17"))


class TestFailClosed(Base):
    def test_a_rejected_draft_writes_nothing(self):
        def snapshot():
            return {
                p.relative_to(self.tmp).as_posix(): p.read_bytes()
                for p in sorted(self.tmp.rglob("*")) if p.is_file()
            }

        before = snapshot()
        self.assertSkipped(BODY=BODY.replace("That is a", "Because we lend, that is a", 1))
        self.assertEqual(before, snapshot(), "a rejected draft must not touch the tree")

    def test_missing_api_key_exits_non_zero(self):
        key = os.environ.pop("ANTHROPIC_API_KEY", None)
        try:
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(self.mod.main(), 1)
        finally:
            if key is not None:
                os.environ["ANTHROPIC_API_KEY"] = key


if __name__ == "__main__":
    unittest.main(verbosity=2)
