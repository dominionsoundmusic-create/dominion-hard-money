# Dominion Hard Money (dominionhardmoney.com): PLAYBOOK 2.0 REBUILD, INSTRUCTIONS FOR CLAUDE CODE

You are rebuilding Maurice Johnson's live lead-generation site dominionhardmoney.com by running
Dominic & Dalton's Website Builder Prompt Playbook 2.0 (PLAYBOOK.md), Prompts 1 to 20, in full.
The site is LIVE on `main`. You work only on the branch `build`.

## RUN STRAIGHT THROUGH. DO NOT STOP.
Maurice is not watching this session and cannot approve anything. Do NOT pause at the end of each
playbook phase, do NOT ask "continue?", do NOT wait for input. Make reasonable decisions yourself,
write them down in docs/decisions.md, and keep going until Prompt 20 is finished and every check
below passes. The only reason to stop early is if something would require paying money, deploying,
changing Netlify, merging to main, or changing a repository other than this one.

## What the business is (read twice)
- Dominion Hard Money is a brand of Dominion Digital Group (Maurice Johnson). It brings real estate
  investors (borrowers) to a third-party private lender. It does NOT lend its own money.
- Maurice is NOT licensed and does not need to be. NEVER describe him or the brand as licensed, a
  licensed broker, a lender, or "the lender". Avoid using "broker" as his title in copy. The approved
  wording is: "Dominion Hard Money does not lend its own funds; it arranges financing through
  third-party lending partners." Keep the existing disclosures and state notices the live pages carry.
- Loan terms: before writing ANY rate, points, LTV, loan size, FICO, term or property-type limit,
  check the lender's own current website (cogocapital.com, the specific loan-program page). Standard
  fix-and-flip/bridge pricing is 12.99% + 2.99 points; the 10.99% / 1.99 figure is loyalty pricing
  after two paid-off loans, so never lead with it. If a term cannot be verified today, leave it out.
  Where the live pages already handle a term carefully, keep their wording unless the lender's site
  now says something different.

## Step 0: audit what is live (before writing anything)
- Count the real .html files with `find` (not the sitemap). List every URL in docs/url-inventory.md.
- EVERY existing URL must keep working at the same path after the rebuild. Do not rename or drop
  pages. If two pages truly duplicate each other, keep both URLs and add a 301 in `_redirects` only
  with a one-line reason in docs/decisions.md.
- Read `_redirects` and `_headers` and keep every rule.

## Things that MUST keep working (do not break)
1. The site is served straight from the repository ROOT (no build command, no publish folder).
   Keep it that way: finished pages are plain .html files at their current paths. If you use a
   generator (for example the build.py system from the repo dominionsoundmusic-create/tree-service-
   houston-tx), its OUTPUT must be written to the repo root paths, and the generator sources must
   live in a folder Netlify will not serve as pages (for example `_src/`), with a `_redirects` or
   `_headers` rule so it is never publicly visible.
2. The weekly news automation: `.github/workflows/weekly-news.yml`, `.github/scripts/` and its 53
   tests. It writes a new post into `blog/` and rebuilds the blog index and `sitemap.xml` every
   Tuesday. Do not move `blog/`, do not change the post file pattern, and if you change the blog
   index or sitemap format, update the script so its tests still pass (`python -m pytest
   .github/scripts`). Existing blog posts may get the new header/footer but their text stays.
3. The lead forms. The deal-inquiry form posts to Netlify forms AND to
   https://dominion-demo-backend.onrender.com/hard-money-lead (the `W` constant). Netlify forms in
   use: `free-books`, `hm-contact`, `lending-guide`, plus the deal-inquiry form. Keep every form
   name, field name, endpoint and thank-you page exactly as they are. Restyle only.
4. The Jesse Duplantis line that sits at the top of Dominion pages: "I believe the unbelievable, I
   receive the impossible, because it's doable." credited "— Jesse Duplantis". Keep it exactly as
   written wherever it appears now (do not reword it, do not add "with God").
5. The `/books/` pages and the free book offer.

## Keywords
There is no new Ubersuggest file for this rebuild. Build docs/keyword-plan.md from: each live
page's title, H1 and target topic; the city/state pages already live; and the playbook's own
keyword steps. Every live page gets one target keyword and supporting keywords. Note in
docs/keyword-plan.md which pages would benefit most from fresh Ubersuggest data so Maurice can pull
it later. Do NOT create new city or state pages in this run; improve the ones that exist.

## Design (Maurice's standing rules)
- Hero photo stretches edge to edge across the page behind the headline, dark fade on the text side.
- Text sits in a centered reading column (text itself left-aligned), not left-justified to the page.
- Mostly WHITE sections with occasional color breaks: hero, white, a navy/brand-color break, white,
  a second-color break that suits the brand. No pale off-white tints. No white-on-white: forms,
  cards and boxes need clear contrast.
- Speed: WebP images with width-based srcset, self-hosted font, lazy-loaded in-body images, no
  layout shift. Reuse the 45 photos in `images/` first. Any new photo needed goes in
  docs/image-list.md with file name, size and one Artistly prompt (bright, clearly visible,
  investor/real-estate scenes, no text, no logos, no recognizable faces). Missing images must never
  show as broken.

## Hard rules for every page
1. Never invent licenses, reviews, testimonials, ratings, funded-deal counts, dollar totals, years in
   business, team members, guarantees, awards or statistics.
2. Never promise approval, a rate, or a closing time. Say the lender decides.
3. No em dashes or en dashes in visible copy (use commas, colons, periods, "to" for ranges). No
   eyebrow labels above headings.
4. Every page except privacy, terms, disclaimer, cookie policy and 404 has 3 to 6 FAQs written the way
   investors ask, shown visibly AND as FAQPage JSON-LD (keep any good Q&A already on the page).
5. Every page has the full-width hero plus at least two in-body images, each with filename, alt,
   width, height and loading="lazy" (hero eager).
6. Facts must be real and current. Research on the web, cite sources in a Sources list on each
   guide page, leave out anything you cannot verify. Each page is written for its own keyword: never
   reuse paragraphs between pages with names swapped. Keep the researched substance the live pages
   already have; improve it, do not water it down.

## Before you finish (all must pass)
- Every URL in docs/url-inventory.md returns a page (check locally with a static server), plus
  `_redirects` targets exist.
- `python -m pytest .github/scripts` passes.
- Grep the site for: em/en dashes in visible text, "licensed", "we lend", "our loans", "we fund",
  "guaranteed", "approval in", "10.99%" used as the headline rate. Fix every hit (a disclosure saying
  Dominion is NOT a lender is fine).
- No horizontal overflow at 1440, 1024, 768 and 390 px wide.
- Independent fact-check: start a separate sub-agent that did not write the pages, have it check
  every loan term against the lender's current site and every other factual claim and source, fix
  what it finds, and record the result in docs/fact-check.md.
- docs/image-list.md lists every image still needed.

## Git
- Work on `build`. Commit as you go with clear messages. Push to origin `build` at the end.
- Do NOT merge to main, do NOT touch Netlify, do NOT deploy, do NOT pay for anything.

## Final report (5 lines max, Maurice reads on his phone)
Pages rebuilt (count), checks passed, fact-check result, how many images still need Artistly, and the
one thing Maurice must do next.
