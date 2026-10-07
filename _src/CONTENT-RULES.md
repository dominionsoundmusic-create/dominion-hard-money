# Content rules for the Playbook 2.0 rebuild (read all of it before editing)

You are editing page SOURCES in `_src/pages/**/*.src.html`. Never edit the generated
`.html` files at the repo root; `python3 _src/build.py` writes those. After editing your
pages run `python3 _src/build.py --check --only <dir/>` for each page (for example
`--only fix-and-flip-loans/` or `--only hard-money-lenders/atlanta-ga.html`) and fix every
PROBLEM it prints for your pages. Never run the build without `--only` (other people are
building in parallel).

## The business (this decides wording everywhere)
* Dominion Hard Money is a brand of Dominion Digital Group (Maurice Johnson). It brings real
  estate investors (borrowers) to a third-party private lender. It does NOT lend its own money.
* NEVER describe Dominion or Maurice as licensed, a licensed broker, a lender, "the lender",
  or use "broker" as his title. Never write "we lend", "we fund", "our loans", "our funds",
  "our capital", "we finance", "our rates". Say "our lending partners", "the lender",
  "the lending partner's team". Approved line: "Dominion Hard Money does not lend its own
  funds; it arranges financing through third-party lending partners."
* NEVER name the lending partner (no "Cogo", no "Cogo Capital") anywhere on the site.
* Never promise approval, a rate, or a closing time. Say the lender decides. "Typically",
  "commonly", "in the market" ranges are fine when sourced; "you will close in 7 days" is not.
* Never invent licenses, reviews, testimonials, ratings, funded-deal counts, dollar totals,
  years in business, team members, guarantees, awards or statistics.
* Avoid the words "guaranteed"/"guarantee" entirely (even "not guaranteed": write "at the
  lender's discretion" or "only if the lender agrees"). Avoid "approval in ...".

## Lending partner terms you may state (checked against the lender's own pages, Oct 7 2026)
Use ONLY these for "our lending partners'" programs. Anything else lender-specific that you
cannot confirm on cogocapital.com today must be removed or turned into a general market
statement ("lenders commonly...", with a source).
* Fix and flip / rehab / bridge / short-term construction:
  - Standard pricing starts at **12.99% interest plus 2.99 points**. Lead with this.
  - **10.99% plus 1.99 points** is loyalty pricing for borrowers who have paid off two loans
    with the lending partner in good standing. You may mention it AFTER the standard
    pricing and always with that condition. Never lead with it, never use it as the headline.
  - Minimum loan amount $50,000. Minimum credit score 600.
  - Up to 70% of value (after-repair value) and up to 100% of cost (purchase plus rehab),
    whichever limit binds first. Leverage depends on experience documented over the past
    three years.
  - Non-owner-occupied investment property only, held in an entity (LLC or corporation).
* DSCR rental (30-year): no minimum credit score; 30-year fixed; up to 80% LTV on purchase or
  rate-and-term refinance and up to 75% on cash-out; loan size $50,000 to $2 million per
  property. Do NOT state a lending-partner DSCR rate (the lender's pages conflict); market
  DSCR rate ranges with a dated source are fine.
* NOT verifiable today, so remove when presented as the lending partner's term: maximum loan
  size on short-term loans (for example "$2,000,000"), loan terms of "12 to 24 months",
  minimum after-repair value ($100,000 / $150,000), renovation budget caps ($40,000), lists of
  restricted counties or states, "37 states", commercial loan terms, construction rate "from
  8.5%", any lending-partner closing time. Where the page says "the lender's guidelines say X"
  and X is in this list, rewrite to tell the investor to confirm that limit with the lender
  for their deal (no number).
* Where live copy already handles a term carefully and it matches the list, keep its wording.

## Writing rules
* No em dashes or en dashes anywhere in visible copy (the build fails on them). Use commas,
  colons, periods, and "to" for ranges.
* No eyebrow labels above headings.
* US spelling ("program", not "programme").
* Keep the researched substance. Improve it, do not water it down. Do not copy paragraphs
  between pages with names swapped: each page is written for its own keyword.
* Keep each page's existing good content, figures, tables and internal links.

## FAQs (every page except privacy, terms, disclaimer, cookie policy, 404)
* 3 to 6 Q&As inside the `<faq> ... </faq>` block at the end of the source: each is
  `<h3>question?</h3>` then one or more `<p>` answers. The build makes the visible accordion
  AND the FAQPage JSON-LD from this one block, so never add FAQ JSON-LD by hand.
* Questions phrased the way an investor types them ("Can I get a hard money loan with a 580
  credit score?"). If a page has more than 6, keep the 6 best and make sure anything
  important in the dropped ones is already covered in the body.

## Sources (every guide, program, state and city page)
* Add a `<sources> <li>...</li> </sources>` block (after `<faq>`). Each `<li>` is a link to a
  primary or reputable source that supports a specific fact on the page, e.g.
  `<li><a href="https://...">Publisher, title</a>, what it supports (accessed Oct 2026)</li>`.
* Verify facts with WebSearch/WebFetch. Statutes, tax rates, agency data, market reports:
  check them. If you cannot verify a claim, remove it or soften it to what you can verify.
  Do not cite cogocapital.com (the lender is never named on the site); lending-partner terms
  need no citation.
* Facts must be current: if a page cites "2025" data and newer data exists, update it.

## Images
* The hero image comes from front matter `hero_img:` (a name from the catalog below or
  `/images/...`), with `hero_alt:` describing what the photo actually shows.
* The build guarantees two in-body photos. To choose them yourself, add
  `<photo src="name" alt="accurate description" caption="optional sentence"></photo>` between
  sections. Alt text must describe the actual photo; never claim a photo shows a specific
  city or property unless it does.
* Catalog (name: what it shows): 1, 2, 3, 4: aerial suburban neighborhoods with distant
  skylines; 5, 6, 7, 8: interior rooms mid-renovation (framing, new windows, ladder);
  rehab-in-progress: same kind of interior; flip-hero: renovated two-story house with sign;
  hardmoney-hero: one-story house under renovation, van in drive; construction-hero: new
  wood-framed house; duplex: brick two-unit rental; dscr-hero: one-story rental house;
  dscr-lenders-hero: brick duplex; documents-hero: papers, pen and coffee on a desk;
  rates-hero: calculator, keys and model house; vetting-hero: hands holding a document by a
  laptop; near-me-hero: man on a phone call at a kitchen table; credit-hero: man in a
  driveway looking at a house; bridge-hero: two small white houses in autumn;
  business-hero, commercial-hero: brick main-street storefronts; and state photos
  alabama-hero, atlanta-hero, colorado-hero, connecticut-hero, florida-hero, georgia-hero,
  houston-hero, indiana-hero, maryland-hero, massachusetts-hero, michigan-hero,
  missouri-hero (Gateway Arch), ohio-hero, pennsylvania-hero, south-carolina-hero,
  tampa-hero, texas-hero, virginia-hero, washington-hero.

## Front matter keys you may edit
title, description (about 150 to 160 characters, no dashes), og_title, og_description, h1,
lede (first sentence becomes the hero line; keep it short and specific), hero_img, hero_alt,
cta (primary button label), cta2 (`Label|/url` for the second hero button, pick a relevant
internal page), crumbs (JSON list of [name, url] pairs, last one with ""), faq_heading,
break_title / break_text (the navy call-to-action band, optional, page-specific wording).
Do not touch `form:`, `form_city`, `form_state`, `canonical`.

## Report
When done, write `_src/notes/<your-group>.json`: a list of objects
`{"page": "path/", "target_keyword": "...", "supporting_keywords": [...],
"ubersuggest_priority": "high|medium|low", "changes": "one line",
"removed_unverifiable": ["..."], "sources_added": n}`.
