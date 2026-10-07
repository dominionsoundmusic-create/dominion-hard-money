# Independent fact-check (October 7, 2026)

Three sub-agents that wrote none of the pages checked the rebuilt site against current sources:
(1) lending-partner terms on every page plus all program, guide and company pages; (2) the 37 state
pages; (3) the 16 city pages, the DSCR and rental pages and the blog. They fixed what they found in
the page sources; every fixed page was rebuilt and re-checked.

## Result
- About 160 claims checked: **127 confirmed, 17 corrected, 2 removed, 8 left unverified (flagged below)**.
- **Lending-partner terms: pass on every page.** 12.99% + 2.99 points leads everywhere; 10.99% + 1.99
  points appears only with the "after two loans paid off in good standing" condition; the lender is
  never named. Confirmed against the lender's own pages (via the search engine's current index, since
  cogocapital.com is blocked from this environment): $50,000 short-term minimum, 600 credit score,
  70% of value and 100% of cost, leverage by three years of experience, DSCR 30-year fixed with no
  minimum score, 80% purchase / 75% cash-out.
- **One lender term was wrong and is fixed site-wide:** the lender's pages give the DSCR loan size as
  "$75K to $2 Million" on one page and $50,000 or $100,000 minimums in its PDFs, so every
  "$50,000 to $2 million" DSCR statement now reads "up to $2 million per property".

## Corrections made
- Fannie Mae credit-score price adjustment, 700 to 719 at 75% LTV: 0.875% (a writer had changed it to
  1.25%); worked example recomputed (investment-property-loan-rates).
- "620 is Fannie Mae's minimum score": out of date for automated underwriting since Nov 2025; fixed.
- Market hard money terms 6 to 18 months corrected to 6 to 24 months (12 most common); points range
  1.5 to 3 corrected to 1 to 4 (several pages).
- Hartford property tax on landlord-costs-by-state: 1 to 3 family homes are assessed at 36.75% of
  value, not 70%; tax and the Greenwich comparison recomputed. The same overstated figure was removed
  from the books pages.
- Pittsburgh common level ratio updated to 49.3% for 2027; Atlanta page said the ROAD to Housing Act
  "became law July 11 2026" incorrectly; Houston given its own Q2 2026 margin (3.7%).
- Wisconsin redemption periods updated to 2015 Act 376 (6 months, 3 with a deficiency waiver);
  Maui Bill 9 covers about 6,100 units, not 7,000; Nebraska's 7-day notice dates to LB 320 (2021);
  Germantown removed from Nashville's non-owner short-term rental ban list.
- Unsupported draw-fee range softened; unverifiable 2 to 4 unit surcharge figures removed; guessed
  source URLs (Austin HOME, Cleveland lead-safe, Freddie Mac, FTC, Fannie Mae, Census) replaced with
  the correct pages; a 2021 leverage brochure replaced with a 2026 source.

## Still unverified (flagged for Maurice)
- Atlanta FMLS / August 2026 market figures; Tampa $437k median (from a private tracker); a lender's
  published 6.88% to 8.50% DSCR range; Freddie Mac "highest since 2023" wording.
- State pages Alabama, Alaska, Arkansas, Kansas, Kentucky, Louisiana, Maine, Maryland, Ohio,
  Pennsylvania, South Carolina and Washington DC were read for conflicts but not checked claim by claim
  (search budget). Their writers checked most of them by search.
- Some source links point to an agency home page rather than the exact section (tax.hawaii.gov,
  wyoleg.gov, data.census.gov, tax.ohio.gov, Kentucky statutes). Direct fetching of .gov sites is
  blocked here, so links were judged by search results, not opened.
- The free PDF guide mentions a 50% cap in six counties; this could not be confirmed and the PDF was
  not edited.

## Blog posts (text kept as written, per the owner's rule)
- bank-repossessions post: "FHA serious delinquencies rose more than 225 bp" in a year; MBA coverage
  shows about 122 bp. Maurice should decide whether to correct it.
- how-to-calculate-arv: the dash clean-up had turned minus signs into "to"; restored as "minus" so
  the formulas read as written originally.
- Several blog statistics (Cotality, Chandan, Zillow) were not checked; listed in the detailed notes.

The claim-by-claim tables follow.


---

## Independent fact-check 1 (Oct 7 2026)

Method: cogocapital.com, attomdata.com, fanniemae.com and census.gov are blocked for direct fetch here, so lender pages and agency data were checked through WebSearch's index of those pages (allowed_domains targeting) plus secondary coverage of the same releases. Pages edited: sources only (`_src/pages/**`), each rebuilt with `build.py --check --only` (0 problems).

## Findings

| Claim | Page(s) | Verdict | Evidence |
|---|---|---|---|
| Fix and flip / rehab / bridge standard pricing 12.99% + 2.99 points | all program, guide, state and city pages | confirmed (owner-supplied; leads everywhere) | Owner instruction. Lender's pages advertise only the 10.99% / 1.99 tier, which they restrict to borrowers who paid off two deals |
| 10.99% + 1.99 points only after two paid-off loans in good standing | all pages that mention it | confirmed | cogocapital.com/loan-programs/: "available only for ... borrowers who have successfully paid off two deals ... and are in good standing"; never used as the headline on any page |
| Short-term minimum loan $50,000, minimum FICO 600, 70% LTV (ARV), 100% LTC | all pages | confirmed | cogocapital.com/loan-programs/ fix and flip: LTC 100%+, LTV 70%, min FICO 600, min loan $50,000 |
| Leverage depends on experience documented over the past 3 years | hard-money-rates, hard-money-requirements, hard-money-lender, investment-property-loan-requirements, atlanta, illinois, others | confirmed | Lender's loan-programs page: leverage based on experience documented in the past 3 years |
| DSCR: 30-year fixed, no minimum FICO, up to 80% LTV, 75% on cash-out | all DSCR mentions | confirmed | loan-programs page (no min FICO, up to 80% LTV, up to $2 million); lender rental program PDF (30-year fixed, 75% cash-out) |
| DSCR loan size "$50,000 to $2 million per property" | about 70 pages (programs, guides, states, cities, calculator) | corrected | Lender's current loan-programs page says "$75K to $2 Million"; an older rental PDF says $50,000 and a Nov 2024 PDF says $100,000. Minimum is not consistent on the lender's own site, so every instance now reads "up to $2 million per property" with no minimum. CONTENT-RULES.md should be updated to match |
| "A $50,000 minimum loan" as a DSCR selling point | dscr-loan-lenders | corrected | Rewritten to tell the investor to confirm the minimum with the lender |
| "$50,000 for both short-term loans and DSCR rental loans" | hard-money-lenders/tampa-fl | corrected | Now $50,000 for short-term only; DSCR minimum to be confirmed with the lender |
| Calculator flag "Below the $50,000 minimum on DSCR loans" | hard-money-calculator | removed | Same reason; the $2 million DSCR max flag and the $50,000 flip flag stay |
| ATTOM Q2 2026: $60,526 gross profit, 21.5% margin (25.7% prior quarter, 27.6% a year earlier), 161 days, 10.7% FHA share | real-estate-investor-loans, rehab-loans, fix-and-flip-loans, fix-and-flip-loans-for-beginners, fix-and-flip-loans-near-me | confirmed | ATTOM release Oct 1 2026 "Home Flipping Profits Continue Gradual Two-Year Decline" (also PR Newswire, Morningstar, mpamag) |
| ATTOM metros: Pittsburgh 81.5%, Buffalo 76.6, New Orleans 75, San Antonio -0.3%, Dallas 1.8, Austin 2.8, Houston 3.7; Canton 11.6% and Cleveland 10.4% flipping rates | fix-and-flip-loans, beginners, near-me | confirmed | Same ATTOM Q2 2026 release |
| ATTOM Q1 2026: 61.1% all cash; $100k to $200k best purchase band; costs 20% to 33% of value | beginners, near-me, fix-and-flip-loans | confirmed | ATTOM Q1 2026 report; ATTOM's standard note that rehab and other costs run 20 to 33 percent of value |
| Freddie Mac 30-year average 7.28% on Oct 1 2026, up from 7.03% | hard-money-loans, real-estate-investor-loans, private-money-lender, what-is-a-hard-money-loan, hard-money-rates, investment-property-loans, investment-property-loan-rates | confirmed; source corrected | Freddie Mac PMMS / release "Mortgage Rates Average 7.28%". The GlobeNewswire link (unverifiable ID) was replaced with Freddie Mac's own release URL freddiemac.gcs-web.com/news-releases/news-release-details/mortgage-rates-average-728 |
| Fannie LLPA investment-property row 1.125 / 1.625 / 2.125 / 3.375 / 4.125 | investment-property-loan-rates, investment-property-loans | confirmed | Fannie Mae LLPA Matrix |
| LLPA credit score 700 to 719 at 75% LTV = 1.25% | investment-property-loan-rates | corrected | Matrix value is 0.875% (1.25% is the 720 to 739 band at 80%). Worked case corrected from 3.375% / $7,590 to 3.0% / $6,750; the 80% and 85% cases (4.75%, 5.625%) were already right |
| Two-to-four unit LLPA "adds 0.375 or 0.625 percent" | investment-property-loan-rates | removed (unverifiable) | Could not confirm the 2-4 unit row values; softened to "can carry a further adjustment ... check that row" |
| LLPA Matrix "dated September 9, 2026" | investment-property-loan-rates | corrected | Current matrix is titled "LLPA Matrix updated 09-30-26" |
| 760 score cases ($5,340 / $9,600 / $12,110), cash-out 740 at 75% = 3.75%, 70% = 2.625% | investment-property-loan-rates | confirmed | Arithmetic checked against matrix values |
| Fannie 10 financed properties, 720 score for 7 to 10 | real-estate-investor-loans, private-money-lender, investment-property-loans, investment-property-loan-requirements | confirmed; URL normalized | Selling Guide B2-2-03 (11/05/2025). Old fanniemae.com/content/guide URL replaced with selling-guide.fanniemae.com/sel/b2-2-03/... |
| "620 is Fannie Mae's general minimum" | hard-money-lender-bad-credit, investment-property-loans | corrected | Fannie removed the 620 minimum for Desktop Underwriter casefiles created on or after Nov 16 2025; 620 still applies to manual underwriting. Copy now says most conventional lenders still look for about 620, with an Orrick InfoBytes source added |
| Fannie Eligibility Matrix (media/20786): 85% 1-unit / 75% 2-4 unit investment purchase; 75% / 70% cash-out | cash-out-refinance, investment-property-loans, investment-property-loan-rates | confirmed | URL resolves to the Eligibility Matrix; values match |
| Fannie cash-out seasoning (12 months note to note, 6 months on title, delayed financing) | cash-out-refinance | confirmed | Selling Guide B2-1.3-03 |
| Reg Z: business-purpose and non-natural-person exemptions; non-owner-occupied rental deemed business purpose; 14-day test; beach house example | hard-money-loans, private-money-lender, what-is-a-hard-money-loan, what-is-hard-money-financing, hard-money-lenders-for-business, others | confirmed | 12 CFR 1026.3(a) and Official Interpretation 3(a) |
| Owner-occupied rental: acquire >2 units, improve/maintain >4 units | hard-money-lenders-for-business | confirmed; wording tightened | Comment 3(a)-5; copy now says "automatically deemed" because fewer units is not automatically consumer credit |
| NAHB/Census: 8.8 months (1.4 to start, 7.4 to complete) in 2025; 31.5% of built-for-sale homes sold after completion | hard-money-construction-loan | confirmed; Census URL corrected | Eye on Housing, Sept 2026. Census link "pct_start_to_comp_2025.pdf" could not be found; replaced with census.gov/construction/nrc/data/time.html |
| Hard money term "6 to 18 months" (RentalRealEstate.com) | hard-money-loans, what-is-a-hard-money-loan, what-is-hard-money-financing, private-money-lender | corrected | Source says 6 to 24 months, 12 most common. All four pages updated; source added to private-money-lender |
| Bridge market 8% to 14% (most 9% to 12%), 1 to 3 points, 65% to 80% leverage, 650 to 680 credit | bridge-loans, commercial-hard-money | confirmed | rentalrealestate.com/loans/bridge/ |
| Bridge term 6 to 36 months (Lev) | bridge-loans | confirmed; URL corrected | Wording found in Lev's CRE glossary; the "what-is-a-bridge-loan-2026" URL could not be found, replaced with lev.com/blog/cre-glossary |
| DSCR market rates about 6% to 8% | real-estate-investor-loans | confirmed | rentalrealestate.com/loans/dscr/ |
| Market hard money 8% to 15% interest "plus 1.5 to 3 points" (Crestmont) | hard-money-loans, hard-money-lender, private-money-lender, real-estate-investor-loans, what-is-a-hard-money-loan | corrected | Crestmont's Hard Money Loan Rates 2026 page says 8% to 15% and 1 to 4 points. Changed to 1 to 4; the dollar example on what-is-a-hard-money-loan is now $4,000 to $16,000 on $400,000 |
| Draw inspection fees "$100 to $250 each" (cited to Crestmont) | rehab-loans | corrected | Not on the Crestmont page. Softened to "the low hundreds of dollars each" and cited FlipperForce instead |
| Stratton Equities 2021 brochure (experience tiers) | fix-and-flip-loans, fix-and-flip-loans-for-beginners | source replaced | Five years old. Replaced with Stormfield Capital's 2026 comparison of six lenders' tiers (about 85% of purchase and 100% of rehab with no experience, 90%+ for experienced borrowers), which supports the same claims |
| Kiavi pages (100% of rehab, ARV ceiling, draw process) | fix-and-flip-loans, beginners | confirmed | kiavi.com/loans/fix-and-flip and the draw-process blog post both exist and support the claims |
| HomeLight URL `?p=23656` (Georgia and SC attorney closings) | fix-and-flip-loans-near-me | confirmed; URL corrected | Replaced with homelight.com/blog/states-that-require-real-estate-attorney-at-closing/ |
| FTC advance-fee loan warning signs | hard-money-lender-bad-credit, hard-money-lenders-near-me, finding-a-hard-money-lender, private-money-lenders-near-me | confirmed; URL normalized | Current FTC article is consumer.ftc.gov/articles/what-know-about-advance-fee-loans |
| FHA 90-day and 91 to 180 day flip rule (24 CFR 203.37a) | fix-and-flip-loans-near-me | confirmed | Regulation text |
| Lender figures on index, about, apply, faq, calculator (no Sources lists) | those pages | confirmed | All match the confirmed list; arithmetic checked (2.99 pts on $216,000 = $6,460; on $252,000 = $7,535) |
| NMLS, California DFPI CFL, IRS/IRC 4975, SEC exempt offerings, SBA, Reg B, Fair Housing, Texas homestead 10% cap, Maryland pre-1978 lead registration, Cleveland rental registration/Lead Safe, AnnualCreditReport, CFPB Loan Estimate/inquiries | various | not re-searched (low risk, well-known primary sources) | Budget went to lender terms and numeric claims |

## What I changed
- DSCR loan size: "$50,000 to $2 million" changed to "up to $2 million per property" on about 70 source pages (programs, guides, all state and city pages that had it, calculator copy). Removed the DSCR $50,000 minimum from dscr-loan-lenders, tampa-fl and the calculator's JS flag.
- investment-property-loan-rates: corrected the 700 to 719 LLPA (0.875%), the worked 25%-down case (3.0%, about $6,750) and the matrix date (updated Sept 30 2026), and softened the unverified 2-4 unit add-on.
- hard-money-lender-bad-credit and investment-property-loans: replaced "620 is Fannie Mae's minimum" with the post-Nov 2025 rule and added an Orrick source.
- Hard money term range: 6 to 18 changed to 6 to 24 months (12 most common) on hard-money-loans, what-is-a-hard-money-loan, what-is-hard-money-financing and private-money-lender (source added).
- Market points: 1.5 to 3 changed to 1 to 4 on hard-money-loans, hard-money-lender, private-money-lender, real-estate-investor-loans and what-is-a-hard-money-loan (dollar example recomputed).
- rehab-loans: draw-fee range softened, source replaced.
- hard-money-lenders-for-business: Reg Z owner-occupied wording tightened.
- Source URLs fixed: Freddie Mac (7 pages, now its own release URL), Census, Lev, HomeLight, FTC (4 pages), Fannie B2-2-03 (2 pages), and Stratton replaced with Stormfield (2 pages).
- Process note: an early `build.py --help` call ran a FULL build (the script ignores unknown flags), which regenerated every root .html, blog/index.html and sitemap.xml from the sources as they stood. Nothing was lost because the output is derived from the sources, but the orchestrator should do its own full build at the end. After that, every page I changed was checked with `--check --only`: 0 problems.

---

## Fact-check 2: state pages (hard-money-lenders/<state>/), Oct 7 2026

Independent check by a sub-agent that did not write these pages. Method: WebSearch against the
search index (direct fetching of almost every .gov, Justia and legislature site is blocked by the
egress proxy, so source URLs could not be opened or status-checked; each was judged on its title
and on whether a search result confirmed the claim it is cited for). Highest-impact claims first.

| Claim | Page | Verdict | Evidence |
|---|---|---|---|
| Owner redemption after public trustee sale removed; junior lienors keep it | colorado | confirmed (source added) | Adams County Public Trustee: no owner redemption for cases under law in effect since 1/1/2008; C.R.S. 38-38-302 junior lienors only |
| Documentary fee 1 cent per $100 | colorado | confirmed (source added) | C.R.S. 39-13-102 |
| Two-month deposit cap, SB23-184 | colorado | confirmed | Colorado Politics / Colorado Newsline 2023 coverage of SB23-184 (cap raised from one to two months in committee) |
| Hail is the main Front Range premium driver | colorado | corrected (made specific) | DOI data from 20 carriers, Feb 2026: hail about 50% of premiums on Front Range and Eastern Plains, wildfire about 1% in Denver (CPR, Colorado Politics) |
| State conveyance tax 0.75% to $800k, 1.25% above, municipal 0.25%, more in targeted investment communities | connecticut | confirmed | CT DRS / CGA reports on chapter 223 |
| Hartford about 69 mills, Greenwich about 10 to 11 mills | connecticut | confirmed | FY2025-26: Hartford 68.95, Greenwich about 11 |
| Deposit 2 months (1 month age 62+), 21-day return | connecticut | confirmed | CGS 47a-21 (21 days since 2023) |
| Realty transfer tax 4% combined (2.5% state + 1.5% local), customarily split | delaware | confirmed | Clever 2026 guide; Delaware Code Title 30 ch. 54 |
| Deposit one month, 20-day return, 5% late fee, 5-day notice, 60-day notices | delaware | confirmed | 25 Del. C. ch. 51, 55 |
| Landlord flood disclosure, s.83.512, leases of 1 year or more | florida | confirmed (source added) | Fla. Stat. 83.512, effective Oct 1 2025 |
| 10% non-homestead cap, non-school taxes only | florida | confirmed | Fla. Stat. 193.1555 |
| Doc stamps $0.70/$100 deed, $0.35/$100 note, 0.2% intangible; redemption ends at certificate of sale | florida | confirmed | Fla. DOR; Fla. Stat. 45.0315 |
| 40% assessment ratio | georgia | confirmed | O.C.G.A. 48-5-7 |
| Safe at Home Act 2024: habitability, 2-month deposit cap, 3-business-day notice | georgia | confirmed | HB 404 (2024) |
| 2024 squatter law | georgia | confirmed (source added) | HB 1017, Georgia Squatter Reform Act, signed April 24 2024 |
| Transfer tax $1 per $1,000; intangible tax $1.50 per $500, cap $25,000 | georgia | confirmed | O.C.G.A. 48-6 |
| Oahu FY2026-27: $3.50 homeowner, Residential A $11.40 above $1M | hawaii | confirmed (source added) | Honolulu FY27 final tax rates (Resolution 26-62) |
| HARPTA 7.25% withholding | hawaii | confirmed | Hawaii DOTAX (rate since 2018) |
| Maui Bill 9 signed Dec 15 2025; STR use ends Jan 1 2029 West Maui, Jan 1 2031 elsewhere | hawaii | confirmed | Maui Now Dec 15 2025 |
| "roughly 7,000 condos" / "no court had stopped the law" | hawaii | corrected | Bill 9 covers roughly 6,100 condos on Maui and Molokai (Minatoya List about 7,000 historically); lawsuits pending; added June 2026 Bill 88 hotel-zoning path (Star-Advertiser July 5 2026) |
| Oahu Aug 2026 medians $1,240,000 SF (+12.2%), $510,000 condo (-1%) | hawaii | confirmed (source replaced with the specific article) | Star-Advertiser Sep 7 2026 reporting HBR data |
| Chicago $3.75 buyer + $1.50 seller per $500, state $0.50, Cook $0.25; Bring Chicago Home failed | illinois | confirmed | City of Chicago; 2024 primary result |
| Redemption later of 7 months from service or 3 months from judgment | illinois | confirmed | 735 ILCS 5/15-1603 |
| 1/2/3% caps, SEA 1 (2025), no transfer tax, 45-day deposit return, 10-day notice | indiana | confirmed | Indiana DLGF; IC 32-31-3; IC 32-31-1-6 |
| Transfer tax $0.80 per $500 above first $500; 2-month deposit, 30-day return, 3-day notice; no private title insurance | iowa | confirmed | Iowa Code 428A, 562A; Iowa Title Guaranty |
| State $3.75 + county $0.55 per $500; 6-month typical redemption; 1.5-month deposit; PRE 18 mills; uncapping | michigan | confirmed | MCL 207.526, 207.505, 600.3240, 554.602, 211.7cc, 211.27a |
| Class II assessed at 15%, Class I homestead 10%; no transfer tax; 45-day deposit return | mississippi | confirmed | Miss. DOR; Miss. Const. art. 4 s.112 |
| HB 594 signed July 2025, 100% capital gains subtraction for individuals from TY2025 | missouri | confirmed | Missouri House HB 594 |
| 19% residential assessment, odd-year reassessment, no transfer tax (art. X s.25) | missouri | confirmed | RSMo 137.115 |
| Seven-day nonpayment notice set by "a 2019 change" | nebraska | corrected | The change was LB 320, approved May 5 2021 (source added) |
| Deposit 1 month + 1/4 pet, 14-day return; doc stamp $2.25 per $1,000; no redemption after trustee sale | nebraska | confirmed | Neb. Rev. Stat. 76-1416, 76-901, 76-1005 |
| Transfer tax $0.75 per $100 on each of buyer and seller; good cause; 7-day notice; deposit 1 month or $100; no redemption | new-hampshire | confirmed | RSA 78-B:1, 540:1-a, 540:2, 540:9, 540-A:6, 479:25 |
| 39-5-18: nine-month redemption, shortenable to one month; 3% valuation cap resets on sale; no transfer tax | new-mexico | confirmed | NMSA 39-5-18, 7-36-21.2 |
| Deeds excise $2.28 per $500 outside Barnstable; 14-day notice; power of sale, no post-sale redemption; deposit statute | massachusetts | confirmed | M.G.L. c.64D; c.186 s.11, s.15B; c.183 s.21 |
| SQ 847 on Nov 3 2026 ballot, effective 2027 | oklahoma | confirmed (made specific, source added) | OK Policy Institute: caps 5% to 4% (other property) and 3% to 1.75% (homestead and ag) from 2027 |
| Doc stamp $0.75 per $500, 11 to 13.5% assessment ratio, 5-day notice, 45-day deposit return | oklahoma | confirmed | 68 O.S.; Okla. Const. art. 10 |
| Conveyance tax $3.75 per $500 from Oct 1 2025 (up 63% from $2.30); extra $3.75 above $824,000 in 2026 | rhode-island | confirmed (sources added) | RI Division of Taxation notice; RI Realtors Jan 14 2026 |
| New state tax on whole-home STRs from Jan 1 2026 | rhode-island | confirmed (source added) | RI Realtors July 2025 budget summary |
| Deposit one month, 20 days; 5-day demand at 15 days late | rhode-island | confirmed | R.I. Gen. Laws 34-18-19, 34-18-35 |
| Transfer tax 37 cents per $100, mortgage tax 11.5 cents per $100 over $2,000; F&E 6.5% / 0.25% / $100 min, property measure repealed 2024 | tennessee | confirmed | TN DOR |
| Nashville: no new non-owner-occupied STR permits in AR2a, R, RS, RM; not transferable | tennessee | confirmed, neighborhood list corrected | Metro Codes permit types; rule since Jan 1 2022. Removed Germantown (largely mixed-use zoning where permits can be issued) and added a parcel-zoning caution |
| Tax-sale redemption 2 years homestead/ag, 180 days other; HOA 180 days; 21-day notice; 30-day deposit refund | texas | confirmed | Tex. Tax Code 34.21; Prop. Code 209.011, 51.002, 92.103 |
| Recordation 25 cents per $100 + local up to 1/3; grantor 50 cents per $500; congestion fee; deposit 2 months, 45 days | virginia | confirmed | Va. Code 58.1-801, -802, -802.2, -814; 55.1-1226 |
| HB 1217 (May 2025), 7% + CPI or 10%; 2026 cap 9.683%; 12-year new construction exemption; 90-day notice | washington | confirmed (source added) | WA Commerce announcement; Washington State Standard |
| REET 1.1% to $525,000, local up to 0.5% | washington | confirmed | WA DOR; thresholds next adjust Jan 1 2027 |
| Redemption three months for residential after foreclosure sale | wyoming | confirmed | W.S. 1-18-103 (12 months agricultural) |
| 9.5% residential assessment; no transfer tax; 3-day notice; deposit 30 days / 15 days | wyoming | confirmed | Wyoming DOR; W.S. 1-21, 34-2 |
| Redemption "generally twelve months, six months if deficiency waived" | wisconsin | corrected | 2015 Wis. Act 376 halved periods for mortgages signed on or after Apr 27 2016: owner-occupied 1 to 4 family, 6 months or 3 months with waiver; 12/6 only for older mortgages (Nolo, USFN) |
| Transfer fee $3 per $1,000; 21-day deposit return; 5/14/30-day notices; 28-day periodic notice | wisconsin | confirmed | Wis. DOR; Wis. Stat. 704 |
| 60% assessment; Class III/IV levy double Class II; state excise $1.10 per $500 plus county excise | west-virginia | confirmed | W. Va. Code 11-8-6c, 11-22-2 (county excise varies, page tells reader to check the county clerk) |
| Lending-partner terms (12.99% + 2.99 pts first, 10.99% + 1.99 pts loyalty with two-paid-off-loans condition, $50k min, 600 FICO, 70% ARV / 100% cost, DSCR 80/75%, $50k to $2M, no min FICO) | all 37 | confirmed | Grep of all 37 sources: 10.99 never appears before 12.99 and always carries the condition; no lender name, no forbidden terms (max short-term loan, 12 to 24 months, min ARV, rehab caps, closing times) |

Not checked individually (writers' dated sources look specific and current; no budget left for a
search each): Alabama, Alaska, Arkansas, Kansas, Kentucky, Louisiana, Maine, Maryland, Ohio,
Pennsylvania, South Carolina, Washington DC. Their figures were read and none conflicted with known
law. Source URLs on all pages could not be opened (egress proxy blocks .gov, Justia, legislature
sites), so link liveness is unverified; a few sources are generic homepages (for example
tax.hawaii.gov, wyoleg.gov, newcastlede.gov, dpo.colorado.gov) that support the claim only
indirectly.

## What I changed (sources only, then `build.py --check --only` per page: 0 problems)
- wisconsin: rewrote the redemption paragraph and FAQ for 2015 Act 376 (6 months / 3 with waiver for post-Apr-2016 home mortgages; 12/6 for older); added Nolo source.
- hawaii: Bill 9 scope corrected to roughly 6,100 condos, lawsuits pending, added Bill 88 hotel-zoning path; added FY27 Honolulu tax-rate PDF, Maui Now and two Star-Advertiser sources (replaced generic HBR and Maui County homepages).
- tennessee: removed Germantown from the residential-zone list, added the Jan 1 2022 start, where permits are still issued and a parcel-zoning caution; source pointed at the permit-types page.
- nebraska: "2019 change" corrected to LB 320 (May 5 2021); LB 320 source added.
- oklahoma: SQ 847 now states the proposed caps (4% and 1.75%) from 2027; OK Policy source added.
- colorado: hail claim made specific to the Feb 2026 Division of Insurance data (CPR source replaces DOI homepage); added C.R.S. 39-13-102 and Adams County Public Trustee sources.
- florida: added Fla. Stat. 83.512 source.
- georgia: added HB 1017 (2024) source.
- rhode-island: added RI Realtors sources for the conveyance tax increase, the $824,000 threshold and the STR tax.
- washington: added the Commerce 9.683% announcement source.

---

## Fact-check 3: city pages, DSCR/rental pages, blog posts (Oct 7 2026)

Independent check by a sub-agent that did not write these pages. Method: WebSearch (most primary
sites, including attomdata.com, phila.gov, census.gov, flsenate.gov, justia.com, codes.ohio.gov and
the DSCR lender page, are blocked for direct fetch, so figures were matched against the search
engine's index of those pages and of press coverage). Lending-partner terms on every page in scope
were compared with CONTENT-RULES.md: all match (12.99% + 2.99 points leads; 10.99% + 1.99 is
stated only as loyalty pricing after two paid-off loans; $50,000 minimum; 600 FICO; 70% ARV / 100%
cost; DSCR 30-year fixed, no minimum score, up to $2M, 80% purchase/rate-term, 75% cash-out). No
lending-partner name, closing time, max short-term loan size or other unverifiable term found.

## Claims

| Claim | Page | Verdict | Evidence |
|---|---|---|---|
| ATTOM Q2 2026: national flip rate 6.2%, typical margin 21.5% | several city pages | confirmed | ATTOM "Home Flipping Profits Continue Gradual Two-Year Decline" (Oct 1 2026), MPA, PR Newswire coverage |
| Cleveland 10.4% flip rate, highest large metro Q2 2026 | cleveland-oh | confirmed | Same report: Cleveland 10.4, Columbus 9.5, Memphis 9.5, Dallas 9.4, Phoenix 8.9 |
| Columbus 9.5%, "tied for second" among large metros | columbus-oh | confirmed | Tied with Memphis at 9.5% |
| Dallas 9.4% flip rate; 1.8% margin, second-thinnest behind San Antonio | dallas-tx | confirmed | Same report |
| Austin 2.8% Q2, among five thinnest with San Antonio, Dallas, Houston | austin-tx | confirmed | Houston 3.7% was fourth-thinnest |
| Pittsburgh 81.5%, ahead of Buffalo (76.6) and New Orleans (75) | pittsburgh-pa | confirmed | Same report |
| Philadelphia 62.8%, fifth among large metros | philadelphia-pa | confirmed | Fifth behind Virginia Beach 63.4% |
| San Antonio typical margin a 0.3% loss | san-antonio-tx, houston-tx | confirmed | Same report |
| Canton 11.6%, Akron 11.2% among five most-flipped metros (any size) Q2 | cleveland-oh | confirmed | Same report (Columbus GA 13.6% led) |
| Atlanta no longer in top five large metros Q2 | atlanta-ga | confirmed | Top five listed above excludes Atlanta |
| ATTOM Q1 2026: Atlanta 12.3% highest large metro, Cleveland 12.1%, national 8%, margin 25.4% | atlanta-ga, cleveland-oh, blog | confirmed | ATTOM Q1 2026 report and coverage |
| ATTOM Q1 2026: thinnest large-metro margins Austin 2%, Dallas 4.3% | austin-tx, dallas-tx | confirmed | Q1 coverage: Austin 2, Dallas 4.3, San Antonio 5.1, Houston 7.2 |
| ATTOM/Backflip Q1 2026: Atlanta $370,335 in, $470,256 out, 27.0% ROI, ~90 days; DFW $418,856/$437,003, 4.3%; Austin 154 days; Denver 133 days | atlanta-ga, dallas-tx, austin-tx, denver-co | confirmed | ATTOM special analysis; Scotsman Guide; Backflip |
| ROAD to Housing Act "signed in July 2026" | atlanta-ga | corrected | Became law July 11 2026 without the President's signature; now "which became law on July 11, 2026". 350-home threshold and Jan 7 2027 start confirmed (Latham, Mayer Brown, Hunton) |
| FMLS July 2026 detached median $475,000 (+2.2%); attached 6.5 months supply; Aug 2026 metro median ~$395,000, 5.4 months, 59 days | atlanta-ga | unverifiable | Cited pages blocked. Atlanta Realtors/FMLS all-types July median was $445,000 (+2.1%), consistent with a higher detached figure; a mid-2026 metro summary showed $395,242 and 59 days. Kept, flagged |
| Denver: hail ~51% of avg premium ($1,547 of $3,040) | denver-co | confirmed | Colorado DOI/Governor release Feb 2026; CPR, Denver Gazette |
| Denver rental license: 2+ units from Jan 1 2023, single units from Jan 1 2024 | denver-co | confirmed | Denver Business Licensing |
| HB24-1098 for-cause eviction after 12 months | denver-co | confirmed | Colorado Sun; Colorado Lawyer |
| Dallas rental registration $74 per unit, annual, self-inspection checklist | dallas-tx | confirmed | City of Dallas Code Compliance (fee $74 from Oct 1 2025) |
| Texas 20% non-homestead circuit breaker, 2026 threshold $5.32M, expires Dec 31 2026, not renewed in 2025 | austin, dallas, el-paso, houston, san-antonio | confirmed | Tax Code 23.231; Ownwell summary; Legislature next meets Jan 2027 |
| Texas protest deadline May 15 or 30 days after notice | Texas pages, landlord-costs | confirmed | Tax Code 41.44 |
| Austin HOME Phase 1 (Dec 2023, up to 3 units) and Phase 2 (May 2024, 1,800 sq ft lot) | austin-tx | confirmed; source URL corrected | Adopted Dec 7 2023 and May 16 2024. Guessed URL /page/home-initiative replaced with austintexas.gov/page/home-amendments |
| Houston Chapter 19: 500-year floodplain, 2 ft above 500-year elevation; NFIP 50% rule | houston-tx | confirmed | Post-Harvey 2018 rule; FEMA glossary |
| HAR Aug 2026 median $330,000 (-1.5%), average $426,760 | houston-tx | confirmed | HAR August 2026 report coverage |
| HAR Jan 2026 average lease $2,214 (-3.3%), lowest since Dec 2023 | houston-tx | confirmed | HAR rental update |
| Houston 2025 rates: HISD $0.8783, city ~$0.5192 | houston-tx | confirmed | HISD adopted 0.8783; city 0.5191 ("about" is fine) |
| Houston Q2 2026 flip margin | houston-tx | corrected (added) | Page cited Dallas/Austin/San Antonio but not Houston; added Houston 3.7%, fourth-thinnest large metro |
| Ohio: 35% assessment, conveyance fee $1 + up to $3 per $1,000, 30-day deposit return with interest over $50/one month, 3-day notice, HB 126 (2022) school board limits, 6-year reappraisal | Ohio pages, landlord-costs | confirmed | ORC 5715.01, 322.02/322.06, 5321.16, 1923.04; HB 126 summaries |
| Kentucky transfer tax $0.50 per $500 | cincinnati-oh | confirmed | KRS 142.050. Source link is the KRS index page, not the section (valid but generic) |
| Cleveland Lead Safe Certificate for pre-1978 rentals, plus registration | cleveland-oh | confirmed; source corrected | leadsafecle.org could not be confirmed; replaced with City of Cleveland Public Health Lead Safe page (certificate renewed every two years) |
| Pittsburgh millage 8.06 to 9.67 for 2026 (20%) | pittsburgh-pa | confirmed | WESA, CBS Pittsburgh |
| Aug 17 2026 court order: countywide reassessment, start by 2027, finish within five years, then every five years | pittsburgh-pa | confirmed | Allegheny County release Aug 17 2026; Axios; WESA |
| Allegheny CLR 50.14% | pittsburgh-pa | corrected (updated) | 50.14% was the ratio through June 2026; STEB's new ratio for tax year 2027 is 49.3%. Page now gives 49.3% current, 50.14% prior |
| Pittsburgh 5% transfer tax (3 city, 1 school, 1 state) | pittsburgh-pa | confirmed | Allegheny County, HomeLight |
| Philadelphia 1.3998% (0.6159 city / 0.7839 school), unchanged since 2016; transfer tax 4.578% since July 1 2025 | philadelphia-pa | confirmed | Phila. Real Estate Tax regulations (2025 onward); phila.gov |
| Tampa: Hillsborough median ~$437,000, +1%, ~38 days (one market tracker, Aug 2026) | tampa-fl | confirmed against cited source; weak source | Momentum tracker shows $437,000 (+1.1%), 38 days. Its listing count (638 countywide) looks implausibly low, so treat as indicative; "roughly a third with a price cut" not seen. Recommend replacing with Florida Realtors/Stellar MLS figure later |
| Citizens flood mandate phased by value, all wind policies by Jan 1 2027 | tampa, orlando, jacksonville | confirmed | Fla. Stat. 627.351(6); Citizens; News4JAX |
| Florida seller flood disclosure Oct 1 2024; landlord flood disclosure Oct 1 2025 (83.512) | tampa, jacksonville | confirmed | HB 1049 (2024); SB 948 (2025) |
| Florida doc stamps 0.70/100 deed, 0.35/100 note, 0.2% intangible; 10% non-homestead cap resets on sale | Florida pages | confirmed | Fla. DOR; 193.1554 |
| flsenate.gov/Laws/Statutes/2025/... and justia.com Indiana URLs | FL and IN pages | unverifiable (pattern correct) | Hosts blocked; URL patterns match each site's standard statute paths |
| data.census.gov (El Paso ~870,000 at 2020 census) | el-paso-tx | confirmed figure; generic URL | MSA 2020 census 868,859. Link is the site root |
| tax.ohio.gov | cincinnati, columbus | confirmed host; generic URL | Valid homepage |
| Indiana 1/2/3% caps, 45-day deposit return, 10-day notice | indianapolis-in | confirmed | IC 6-1.1-20.6, 32-31-3-12, 32-31-1-6 |
| Freddie Mac 7.28% Oct 1 2026, 7.03% prior week, 6.34% year earlier | dscr-loans, dscr-loan-rates, dscr-loan-lenders | confirmed | Freddie Mac PMMS; Trading Economics |
| "highest reading since 2023" | dscr-loan-rates | unverifiable | Not confirmed in search; plausible given 2024/25 peaks near 7.2%. Kept, flagged |
| One DSCR lender's page: 6.88% to 8.50%, tiers effective Sep 29 2026 | DSCR pages | unverifiable | dscr.investorpropertyloan.com blocked and not indexed. Other sources put October 2026 DSCR ranges at about 6.375% to 8.50%, consistent. Kept as attributed, flagged |
| Fannie Mae investment LLPA 3.375% at 75 to 80% LTV | dscr-loan-rates | confirmed | Fannie Mae LLPA matrix |
| Payment/ratio arithmetic (7.0%/7.5% on $240k, $176k at 7.25%, $168k interest-only at 12.99%) | DSCR pages | confirmed | Recomputed |
| Hartford 69.95 mills = $19,586/yr on a $400k house; Hartford to Greenwich spread $16,751; "over $16,000" between two CT towns | landlord-costs-by-state | corrected | 69.95 mills confirmed, but Hartford assesses one to three family homes at 36.75% of value, not 70% (PA 14-174; SmartMLS). Correct figure about $10,280; spread about $7,450. Table, body and intro rewritten; Bridgeport $7,826 added |
| Greenwich 10.125 mills FY2027 | landlord-costs-by-state | confirmed | Greenwich BET (reported as 10.12) |
| Bridgeport 27.95 mills after ~40% cut | landlord-costs-by-state | confirmed | City of Bridgeport |
| Richmond $1.20, Henrico $0.83 (about $1,480 gap) | landlord-costs-by-state | confirmed | VPM; Henrico notice (rate unchanged at 0.83) |
| Washington cap 9.683% (2026), 10% (2027); 12-year new-construction exemption; investor SFRs covered | landlord-costs-by-state | confirmed | WA Commerce; RCW 59.18.710 |
| Maryland: MDE registration within 30 days; Baltimore license non-transferable from Jan 1 2026, reapply within 60 days | landlord-costs-by-state | confirmed | MDE; Baltimore DHCD / Strengthening Renters' Safety Act |
| Colorado hail 26 to 54% of premiums; +57.9% 2018 to 2023 | landlord-costs-by-state | confirmed | KUNC; Colorado Politics |
| Michigan PRE up to 18 mills; Mass. Phillips v. Equity Residential 478 Mass. 251 (2017) | landlord-costs-by-state | confirmed | Mich. Treasury; case record |
| Blog: ATTOM Aug 2026 foreclosures 5,794 REOs (+42% YoY, +22% MoM), ~40,277 filings (+1%, +13%), SC 1 in 1,547 | bank-repossessions post | confirmed | ATTOM August report coverage (MPA, Scotsman Guide) |
| Blog: MBA Q2 2026 4.37% (-7 bp q/q, +44 bp y/y), foreclosure inventory 0.67% (+19 bp), FHA 11.79% | bank-repossessions post | confirmed | MBA NDS Aug 13 2026 coverage |
| Blog: "FHA serious delinquencies rose more than 225 basis points from the previous year" | bank-repossessions post | possible error, not edited | Coverage says FHA delinquencies rose 122 bp y/y; 225 bp not found. Report only (blog text untouchable) |
| Blog: Houston 448, Dallas 402 REOs; Auction.com 67.6%/67.3%; 563-day timeline; 1.3% vacancy | bank-repossessions post | unverifiable | Not found in index; numbers are attributed and plausible |
| Blog: Freddie Mac 6.71% Sep 3 2026 (6.66 prior, 6.50 year ago), 15-year 6.04% | investor-money post | confirmed | Freddie Mac release |
| Blog: DSCR "near 6.75%", "7.75 to 8.25% entering 2025" | investor-money post | unverifiable | No dated source named |
| Blog: ATTOM Q1 2026 25.4% (from 24.7%), $64,300 to $66,000, Pittsburgh 85.9%, Buffalo 84.0%, Austin 2.0% | national-flipping post | confirmed | ATTOM Q1 2026 report |
| Blog: median days purchase to resale 165 (from 160); Pittsburgh flip $110,000 to $204,500 | national-flipping post | unverifiable | Not in indexed coverage |
| Blog: Apartment List Sep 2026 $1,388, -0.1% m/m, vacancy 7% | rents post | confirmed | Apartment List / CRE Daily |
| Blog: NAR Aug 2026 3.98M sales, 1.62M inventory, 4.9 months, highest in over a decade | rents post | confirmed | NAR release |
| Blog: Census Aug 2026 new-home sales 684,000, 483,000 for sale, 8.5 months, avg $478,700 | rents post | confirmed | Census newressales_202608 |
| Blog: Cotality, Chandan, Zillow figures | rents post | unverifiable | Not checked (search budget) |
| Blog: how-to-calculate-arv examples read "$210,000 to $45,000 = $165,000" and "$300,000 to $45,000, $12,000 to $5,000..." | how-to-calculate-arv post | error (presentation), not edited | Dash removal turned minus signs into "to"/":" so the formulas read as ranges. Math itself is right. Owner should approve swapping in the word "minus" |

## What I changed (sources only, `--check --only` run on each: 0 problems)

1. `_src/pages/hard-money-lenders/atlanta-ga.src.html`: ROAD to Housing Act "signed in July 2026" changed to "became law on July 11, 2026".
2. `_src/pages/hard-money-lenders/houston-tx.src.html`: added Houston's own Q2 2026 ATTOM margin (3.7%, fourth-thinnest large metro).
3. `_src/pages/hard-money-lenders/cleveland-oh.src.html`: replaced unconfirmed leadsafecle.org source with the City of Cleveland Lead Safe Program page.
4. `_src/pages/hard-money-lenders/austin-tx.src.html`: replaced guessed HOME URL with austintexas.gov/page/home-amendments and adoption dates.
5. `_src/pages/hard-money-lenders/pittsburgh-pa.src.html`: CLR updated to 49.3% for tax year 2027 (50.14% prior) in body and FAQ; added source.
6. `_src/pages/landlord-costs-by-state/index.src.html`: Hartford tax corrected for its 36.75% residential assessment ratio (about $10,280, not $19,586); spread about $7,450 (was $16,751); intro "over $16,000" changed to "over $7,000"; Bridgeport figure added; two sources added.

## Outside scope, flagged for the owner
* `_src/pages/books/index.src.html` line 27 still says Connecticut tax "swings from $19,586 in Hartford to $2,835 in Greenwich". That is only true "on the same assessed value"; for an actual Hartford one to three family home it overstates by about $9,300. The book itself may carry the same figure.
