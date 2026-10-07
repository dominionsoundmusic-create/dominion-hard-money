# Decisions made during the Playbook 2.0 rebuild (October 7, 2026)

Maurice was not available during this run, so every judgment call is written down here.
One line each, newest topics at the bottom of each section.

## Architecture (Playbook Prompts 2 to 3)
- The playbook is written for an AI Studio SSR (TanStack Start) project. This site is static HTML
  served from the repo root by Netlify, which is already fully server-rendered: every title,
  description, canonical, heading, body copy and JSON-LD block is in the raw HTML. The playbook's
  SSR checks were applied to the static HTML; no framework was introduced (Prompt 2 says do not
  convert the framework).
- A small Python generator was added: `_src/build.py`. Page sources are `_src/pages/**/*.src.html`
  (front matter + body). Output is written to the same root paths as before, so Netlify settings do
  not change (no build command, no publish folder). `_src/*` is already 404'd in `_redirects`.
- `_src/tools/extract.py` and `_src/tools/normalize.py` were one-time tools used to pull the live
  pages into sources; they are kept for the record and are not needed again.
- Shared assets: one stylesheet `/assets/site.css`, one script `/assets/site.js` (menu and language
  picker), one self-hosted variable font `/assets/fonts/inter-var-latin.woff2` (Inter, SIL OFL,
  license alongside). Headings use Georgia (system font, no download).
- Images: the existing 45 photos are reused. The build writes width-based WebP copies to
  `/images/w/` (480, 800, 1200 and full width) and every `<img>` gets srcset, width, height and
  `loading="lazy"` (hero: eager with `fetchpriority="high"` and a preload). Originals are kept.
- The Google Translate language picker is kept (it was added on purpose), but Google's script now
  loads only after a visitor picks a language other than English, which removes it from every
  English page load.
- `forms/deal-inquiry.html` (the hidden Netlify form registration) is left byte-for-byte unchanged.
- A real `404.html` was added (noindex). Netlify serves it automatically for missing URLs.

## URLs and redirects
- All 115 HTML files still exist at the same paths. No page was renamed, merged or dropped, and no
  redirect was added. Every existing `_redirects` and `_headers` rule is unchanged.
- `about.html` and `about/` were near-duplicates (both "About"). Instead of a redirect, `about/` now
  covers how a deal moves through the process, and `about.html` covers who Dominion is. Both are
  in the sitemap with self-canonicals.
- `about/`, `contact/` and `faq/` were missing from `sitemap.xml`; they are now listed. Thank-you
  pages and 404 stay out of the sitemap (noindex).
- Seven live pages had their head and hero overwritten by a copy of another page's hero on Sep 23
  (visible raw FAQ JSON on the page, wrong H1 "Private Money Lenders Near Me" on hard-money-loans,
  hard-money-lender, real-estate-investor-loans, rehab-loans, private-money-lender, about, contact,
  faq). Their real bodies were recovered from the live HTML and each now has its own title and H1.

## Forms (unchanged in behavior)
- Form names (`deal-inquiry`, `free-books`, `hm-contact`, `lending-guide`), field names and ids,
  the backend endpoint constant `W`, the thank-you pages and the submit logic are unchanged. The
  three deal-form variants (standard, homepage, apply page) keep their own field sets and scripts.
- Visible option text that contained dashes now reads "Yes, LLC or corporation", but the option's
  `value` attribute keeps the exact original text, so submitted data is identical to before.
- Button labels changed only where they contained a dash ("Submit Inquiry: Get Funded Fast" became
  "Submit My Deal", because "get funded fast" also read as a promise).
- A link to the privacy policy and terms was added under each deal form.

## Lending terms
- cogocapital.com is blocked by this environment's network policy, so the lender's pages could not be
  opened directly. Terms were checked against the search engine's current index of the lender's own
  pages (cogocapital.com) on Oct 7 2026; see docs/fact-check.md. Maurice should open the lender's
  fix-and-flip and DSCR pages once and confirm the list below.
- Used everywhere: short-term programs from 12.99% plus 2.99 points (standard, per Maurice's brief);
  10.99% plus 1.99 points only as loyalty pricing after two paid-off loans, never as the lead;
  minimum loan $50,000; minimum credit 600; up to 70% of value and 100% of cost; DSCR 30-year fixed,
  no minimum credit score, up to 80% LTV (75% cash-out), up to $2 million per property (the lender's pages conflict on the DSCR minimum: $50,000, $75,000 or $100,000, so no minimum is stated).
- Removed because the lender's pages conflict or could not be confirmed today: "$50K to $2M" and
  "12 to 24 month" terms on short-term loans, "37 states", minimum after-repair value, the $40,000
  first-timer renovation cap, county caps, the construction "from 8.5%" title, a lending-partner
  DSCR rate, and "we respond within 24 hours" (a promise).
- The free PDF guide (`private-lending-guide/files/...pdf`) was not edited (it is a designed PDF). It
  already leads with 12.99% + 2.99 points; it also mentions a 50% cap in six counties. Maurice should
  re-check that page of the PDF against the lender's current guidelines.

## Copy rules
- All em and en dashes were removed from visible copy (build fails if one returns). The one
  exception is the Jesse Duplantis line, kept exactly as written with its "— Jesse Duplantis"
  credit, on the homepage where it appeared before (CLAUDE.md rule 4 overrides the dash rule).
- The "John 3:16" line that sat above the header on 94 pages now sits in the header on every page.
- Eyebrow labels ("kicker" lines above H1s, "hero badge") were removed.
- "licensed" now appears only in the legal pages, about attorneys and about other parties' broker
  licenses ("consult a licensed attorney"); Dominion is never described as licensed.
- The disclaimer said terms are "not guaranteed"; it now says they "do not apply automatically".
- FAQs: every page except privacy, terms, disclaimer, cookie policy and 404 has 3 to 6 visible Q&As;
  the visible accordion and the FAQPage JSON-LD are generated from the same block, so they cannot
  drift apart. Pages that had 7 or 8 kept their best 6.
- The FAQ page itself keeps its full set of questions as normal content grouped by topic, with the
  six most common ones in the FAQ block.
- Blog posts keep their text. Their in-article "Common questions" block moved into the standard FAQ
  section (same questions, same answers); the article H1 became the page H1 (some older posts had
  no H1 at all).
- Homepage FAQ "How fast can a hard money deal close?" was replaced by a rate question, because
  every answer to it reads as a closing-time promise.

## Weekly news automation
- `weekly_news.py` still takes the style, header and footer from the newest post (now also the
  shared head block), so new posts automatically match the redesign. It now renders the new hero
  (H1, breadcrumb, photo) and two in-body photos from a fixed pool of existing images.
- `blog/index.html` keeps the same entry format; the list now sits between `<!--posts-->` and
  `<!--/posts-->` markers, and `rebuild_index` uses those markers.
- One existing test (`test_topic_restating_a_recent_title_is_rejected`) was already failing before
  the rebuild because the post it named had aged out of the six-post lookback. It now builds its
  cases from whatever the recent posts are. One test was added (every image in a new post exists).
- Automated posts do not get FAQs: adding them would change the model's output contract and its
  guards. Flagged for Maurice.

## Design
- Header and footer navy (#0a1628) with gold (#c9a84c) accents, matching the logo. Body sections are
  white. Each page has one navy break (a call to action) and one gold break (the deal form on a white
  card, or a call to action). No pale tints.
- Hero photo is full-bleed behind the H1 with a dark fade on the text side; long ledes are split so
  the hero carries one short statement and the rest opens the body.
