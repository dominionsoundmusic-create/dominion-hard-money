# Playbook 2.0 handoff (Prompt 20)

## Readiness
Built and checked on the `build` branch only. Not merged, not deployed, Netlify untouched.
Ready for Maurice's review; launch blockers below are decisions, not defects.

## Checks actually run (Oct 7 2026)
| Check | Result |
|---|---|
| `python3 _src/build.py --check` (115 pages: one H1, no em/en dashes, 3 to 6 FAQs except legal/404, 2+ in-body images with dimensions, alt text, internal links resolve, banned phrases) | 0 problems |
| `python -m pytest .github/scripts` | 54 passed (53 original + 1 new) |
| Every URL in docs/url-inventory.md plus /404.html served by a local static server | 116 of 116 return 200 |
| `_redirects` targets exist | all 11 exist; every rule unchanged |
| Horizontal overflow at 1440, 1024, 768, 390 px (Chromium) | 0 issues on all 116 URLs |
| Broken images, JavaScript errors, failed local requests | none |
| Mobile menu, Escape to close, FAQ accordion, language menu, deal-form validation on 3 form variants | work; no form was submitted |
| Raw HTML contains title, description, canonical, Open Graph, JSON-LD (Breadcrumb, FAQPage, Organization on home) | yes, static HTML |
| Site-wide grep: licensed, we lend, our loans, we fund, guaranteed, approval in, 10.99% as lead, lender name | clean ("licensed" only about attorneys and lead inspectors) |
| Independent fact-check | see docs/fact-check.md |

## Not verified here
- Real form delivery (Netlify forms and the backend endpoint): not submitted, by rule. Markup, names,
  ids, endpoint and scripts are unchanged from the live site.
- Netlify-specific behavior (pretty URLs, `_headers`, `_redirects`, 404 handling) is assumed from
  Netlify's documented defaults; check on a Netlify deploy preview of `build`.
- Google Translate picker (loads Google's script only after a language is chosen).

## How to edit from now on
Edit `_src/pages/<path>.src.html`, run `python3 _src/build.py --check`, commit the source and the
regenerated `.html`. Rules for writers: `_src/CONTENT-RULES.md`.

## Remaining inputs from Maurice
1. Open the lending partner's fix and flip and DSCR pages once and confirm the term list in
   docs/decisions.md (this environment could not open cogocapital.com directly).
2. 28 regional hero photos in docs/image-list.md (optional; generic photos are in place).
3. Blog post FHA "225 bp" figure, and the PDF guide's county-cap page (docs/fact-check.md).
4. Fresh Ubersuggest data for the pages marked high in docs/keyword-plan.md.
