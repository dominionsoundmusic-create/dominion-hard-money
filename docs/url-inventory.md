# URL inventory (Step 0 audit)

Counted with `find . -name '*.html'` on the `build` branch at commit b22012b (before the rebuild),
not from the sitemap: **115 HTML files**. Every URL below keeps working at the same path after
the rebuild. The sitemap listed 109 of them before the rebuild.

Also served and kept: `_redirects` (all rules kept), `_headers` (all rules kept), `robots.txt`,
`sitemap.xml`, `favicon.svg`, `favicon.ico`, `apple-touch-icon.png`, `book-cover-800.jpg/.webp`,
`images/` (45 photos plus `images/books/`), `books/free/files/*` if present.

New paths added by the rebuild (nothing renamed or dropped): `/404.html` (not-found page),
`/assets/site.css`, `/assets/site.js`, `/assets/fonts/inter-var-latin.woff2`, `/images/w/*.webp`
(resized WebP copies of the existing photos). Generator sources live in `/_src/`, which `_redirects`
returns as 404.

| URL | File | Type | In sitemap before |
|---|---|---|---|
| `/about.html` | `about.html` | page | yes |
| `/about/` | `about/index.html` | page | no |
| `/apply.html` | `apply.html` | page | yes |
| `/blog/bank-repossessions-jumped-42-percent-in-august-1790098215830.html` | `blog/bank-repossessions-jumped-42-percent-in-august-1790098215830.html` | blog post | yes |
| `/blog/building-a-relationship-with-a-private-lender-1785937888333.html` | `blog/building-a-relationship-with-a-private-lender-1785937888333.html` | blog post | yes |
| `/blog/common-reasons-hard-money-deals-fall-through-1786452716886.html` | `blog/common-reasons-hard-money-deals-fall-through-1786452716886.html` | blog post | yes |
| `/blog/hard-money-vs-conventional-financing-for-investors-1786279019409.html` | `blog/hard-money-vs-conventional-financing-for-investors-1786279019409.html` | blog post | yes |
| `/blog/how-fast-can-you-close-on-a-fix-and-flip-loan-1786970754857.html` | `blog/how-fast-can-you-close-on-a-fix-and-flip-loan-1786970754857.html` | blog post | yes |
| `/blog/how-much-down-payment-do-hard-money-lenders-require-1786024209346.html` | `blog/how-much-down-payment-do-hard-money-lenders-require-1786024209346.html` | blog post | yes |
| `/blog/how-to-calculate-arv-and-maximum-allowable-offer-1786366364135.html` | `blog/how-to-calculate-arv-and-maximum-allowable-offer-1786366364135.html` | blog post | yes |
| `/blog/` | `blog/index.html` | page | yes |
| `/blog/investor-money-cheaper-than-homeowner-mortgage-1789200000000.html` | `blog/investor-money-cheaper-than-homeowner-mortgage-1789200000000.html` | blog post | yes |
| `/blog/national-flipping-returns-rose-texas-did-not-1789390800000.html` | `blog/national-flipping-returns-rose-texas-did-not-1789390800000.html` | blog post | yes |
| `/blog/rents-stopped-falling-while-resale-supply-kept-piling-up-1790706368709.html` | `blog/rents-stopped-falling-while-resale-supply-kept-piling-up-1790706368709.html` | blog post | yes |
| `/blog/what-is-a-hard-money-loan-and-who-uses-one-1786192498048.html` | `blog/what-is-a-hard-money-loan-and-who-uses-one-1786192498048.html` | blog post | yes |
| `/blog/what-lenders-look-for-in-a-fix-and-flip-deal-1786106947058.html` | `blog/what-lenders-look-for-in-a-fix-and-flip-deal-1786106947058.html` | blog post | yes |
| `/books/free/` | `books/free/index.html` | page | yes |
| `/books/free/thanks/` | `books/free/thanks/index.html` | thank-you | no |
| `/books/` | `books/index.html` | page | yes |
| `/bridge-loans/` | `bridge-loans/index.html` | page | yes |
| `/cash-out-refinance/` | `cash-out-refinance/index.html` | page | yes |
| `/commercial-hard-money/` | `commercial-hard-money/index.html` | page | yes |
| `/contact/` | `contact/index.html` | page | no |
| `/cookie-policy.html` | `cookie-policy.html` | legal | yes |
| `/disclaimer.html` | `disclaimer.html` | legal | yes |
| `/dscr-loan-lenders/` | `dscr-loan-lenders/index.html` | page | yes |
| `/dscr-loan-no-money-down/` | `dscr-loan-no-money-down/index.html` | page | yes |
| `/dscr-loan-rates/` | `dscr-loan-rates/index.html` | page | yes |
| `/dscr-loan-requirements/` | `dscr-loan-requirements/index.html` | page | yes |
| `/dscr-loans/` | `dscr-loans/index.html` | page | yes |
| `/faq/` | `faq/index.html` | page | no |
| `/finding-a-hard-money-lender/` | `finding-a-hard-money-lender/index.html` | page | yes |
| `/fix-and-flip-loans-for-beginners/` | `fix-and-flip-loans-for-beginners/index.html` | page | yes |
| `/fix-and-flip-loans-near-me/` | `fix-and-flip-loans-near-me/index.html` | page | yes |
| `/fix-and-flip-loans/` | `fix-and-flip-loans/index.html` | page | yes |
| `/forms/deal-inquiry.html` | `forms/deal-inquiry.html` | form registration (hidden) | no |
| `/hard-money-calculator/` | `hard-money-calculator/index.html` | page | yes |
| `/hard-money-construction-loan/` | `hard-money-construction-loan/index.html` | page | yes |
| `/hard-money-lender-bad-credit/` | `hard-money-lender-bad-credit/index.html` | page | yes |
| `/hard-money-lender/` | `hard-money-lender/index.html` | page | yes |
| `/hard-money-lenders-for-business/` | `hard-money-lenders-for-business/index.html` | page | yes |
| `/hard-money-lenders-near-me/` | `hard-money-lenders-near-me/index.html` | page | yes |
| `/hard-money-lenders/alabama/` | `hard-money-lenders/alabama/index.html` | state page | yes |
| `/hard-money-lenders/alaska/` | `hard-money-lenders/alaska/index.html` | state page | yes |
| `/hard-money-lenders/arkansas/` | `hard-money-lenders/arkansas/index.html` | state page | yes |
| `/hard-money-lenders/atlanta-ga.html` | `hard-money-lenders/atlanta-ga.html` | city page | yes |
| `/hard-money-lenders/austin-tx.html` | `hard-money-lenders/austin-tx.html` | city page | yes |
| `/hard-money-lenders/cincinnati-oh.html` | `hard-money-lenders/cincinnati-oh.html` | city page | yes |
| `/hard-money-lenders/cleveland-oh.html` | `hard-money-lenders/cleveland-oh.html` | city page | yes |
| `/hard-money-lenders/colorado/` | `hard-money-lenders/colorado/index.html` | state page | yes |
| `/hard-money-lenders/columbus-oh.html` | `hard-money-lenders/columbus-oh.html` | city page | yes |
| `/hard-money-lenders/connecticut/` | `hard-money-lenders/connecticut/index.html` | state page | yes |
| `/hard-money-lenders/dallas-tx.html` | `hard-money-lenders/dallas-tx.html` | city page | yes |
| `/hard-money-lenders/delaware/` | `hard-money-lenders/delaware/index.html` | state page | yes |
| `/hard-money-lenders/denver-co.html` | `hard-money-lenders/denver-co.html` | city page | yes |
| `/hard-money-lenders/el-paso-tx.html` | `hard-money-lenders/el-paso-tx.html` | city page | yes |
| `/hard-money-lenders/florida/` | `hard-money-lenders/florida/index.html` | state page | yes |
| `/hard-money-lenders/georgia/` | `hard-money-lenders/georgia/index.html` | state page | yes |
| `/hard-money-lenders/hawaii/` | `hard-money-lenders/hawaii/index.html` | state page | yes |
| `/hard-money-lenders/houston-tx.html` | `hard-money-lenders/houston-tx.html` | city page | yes |
| `/hard-money-lenders/illinois/` | `hard-money-lenders/illinois/index.html` | state page | yes |
| `/hard-money-lenders/indiana/` | `hard-money-lenders/indiana/index.html` | state page | yes |
| `/hard-money-lenders/indianapolis-in.html` | `hard-money-lenders/indianapolis-in.html` | city page | yes |
| `/hard-money-lenders/iowa/` | `hard-money-lenders/iowa/index.html` | state page | yes |
| `/hard-money-lenders/jacksonville-fl.html` | `hard-money-lenders/jacksonville-fl.html` | city page | yes |
| `/hard-money-lenders/kansas/` | `hard-money-lenders/kansas/index.html` | state page | yes |
| `/hard-money-lenders/kentucky/` | `hard-money-lenders/kentucky/index.html` | state page | yes |
| `/hard-money-lenders/louisiana/` | `hard-money-lenders/louisiana/index.html` | state page | yes |
| `/hard-money-lenders/maine/` | `hard-money-lenders/maine/index.html` | state page | yes |
| `/hard-money-lenders/maryland/` | `hard-money-lenders/maryland/index.html` | state page | yes |
| `/hard-money-lenders/massachusetts/` | `hard-money-lenders/massachusetts/index.html` | state page | yes |
| `/hard-money-lenders/michigan/` | `hard-money-lenders/michigan/index.html` | state page | yes |
| `/hard-money-lenders/mississippi/` | `hard-money-lenders/mississippi/index.html` | state page | yes |
| `/hard-money-lenders/missouri/` | `hard-money-lenders/missouri/index.html` | state page | yes |
| `/hard-money-lenders/nebraska/` | `hard-money-lenders/nebraska/index.html` | state page | yes |
| `/hard-money-lenders/new-hampshire/` | `hard-money-lenders/new-hampshire/index.html` | state page | yes |
| `/hard-money-lenders/new-mexico/` | `hard-money-lenders/new-mexico/index.html` | state page | yes |
| `/hard-money-lenders/ohio/` | `hard-money-lenders/ohio/index.html` | state page | yes |
| `/hard-money-lenders/oklahoma/` | `hard-money-lenders/oklahoma/index.html` | state page | yes |
| `/hard-money-lenders/orlando-fl.html` | `hard-money-lenders/orlando-fl.html` | city page | yes |
| `/hard-money-lenders/pennsylvania/` | `hard-money-lenders/pennsylvania/index.html` | state page | yes |
| `/hard-money-lenders/philadelphia-pa.html` | `hard-money-lenders/philadelphia-pa.html` | city page | yes |
| `/hard-money-lenders/pittsburgh-pa.html` | `hard-money-lenders/pittsburgh-pa.html` | city page | yes |
| `/hard-money-lenders/rhode-island/` | `hard-money-lenders/rhode-island/index.html` | state page | yes |
| `/hard-money-lenders/san-antonio-tx.html` | `hard-money-lenders/san-antonio-tx.html` | city page | yes |
| `/hard-money-lenders/south-carolina/` | `hard-money-lenders/south-carolina/index.html` | state page | yes |
| `/hard-money-lenders/tampa-fl.html` | `hard-money-lenders/tampa-fl.html` | city page | yes |
| `/hard-money-lenders/tennessee/` | `hard-money-lenders/tennessee/index.html` | state page | yes |
| `/hard-money-lenders/texas/` | `hard-money-lenders/texas/index.html` | state page | yes |
| `/hard-money-lenders/virginia/` | `hard-money-lenders/virginia/index.html` | state page | yes |
| `/hard-money-lenders/washington-dc/` | `hard-money-lenders/washington-dc/index.html` | state page | yes |
| `/hard-money-lenders/washington/` | `hard-money-lenders/washington/index.html` | state page | yes |
| `/hard-money-lenders/west-virginia/` | `hard-money-lenders/west-virginia/index.html` | state page | yes |
| `/hard-money-lenders/wisconsin/` | `hard-money-lenders/wisconsin/index.html` | state page | yes |
| `/hard-money-lenders/wyoming/` | `hard-money-lenders/wyoming/index.html` | state page | yes |
| `/hard-money-loans/` | `hard-money-loans/index.html` | page | yes |
| `/hard-money-rates/` | `hard-money-rates/index.html` | page | yes |
| `/hard-money-requirements/` | `hard-money-requirements/index.html` | page | yes |
| `/` | `index.html` | page | yes |
| `/investment-property-loan-rates/` | `investment-property-loan-rates/index.html` | page | yes |
| `/investment-property-loan-requirements/` | `investment-property-loan-requirements/index.html` | page | yes |
| `/investment-property-loans/` | `investment-property-loans/index.html` | page | yes |
| `/landlord-costs-by-state/` | `landlord-costs-by-state/index.html` | page | yes |
| `/privacy-policy.html` | `privacy-policy.html` | legal | yes |
| `/private-lending-guide/` | `private-lending-guide/index.html` | page | yes |
| `/private-lending-guide/thanks/` | `private-lending-guide/thanks/index.html` | thank-you | no |
| `/private-money-lender/` | `private-money-lender/index.html` | page | yes |
| `/private-money-lenders-near-me/` | `private-money-lenders-near-me/index.html` | page | yes |
| `/real-estate-investor-loans/` | `real-estate-investor-loans/index.html` | page | yes |
| `/rehab-loans/` | `rehab-loans/index.html` | page | yes |
| `/states.html` | `states.html` | page | yes |
| `/terms.html` | `terms.html` | legal | yes |
| `/what-is-a-dscr-loan/` | `what-is-a-dscr-loan/index.html` | page | yes |
| `/what-is-a-hard-money-loan/` | `what-is-a-hard-money-loan/index.html` | page | yes |
| `/what-is-hard-money-financing/` | `what-is-hard-money-financing/index.html` | page | yes |
