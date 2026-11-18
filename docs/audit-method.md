# Audit method

Each domain is checked against the same fixed set of tests so results are comparable across a client list.

## 1. Crawler access

For every crawler in the matrix we fetch `robots.txt` with that crawler's user agent and record the effective decision for the homepage and a sample of deep pages. A rule that allows `/` but disallows the paths that carry the content is recorded as blocked, not allowed.

Tests:
- Is the crawler named explicitly, or only covered by `User-agent: *`?
- Does any `Disallow` rule match the pages worth citing?
- Does the response come back 200 to an unauthenticated fetch, or is it a challenge page (403/429 with an interstitial)?
- Does the CDN or WAF serve a different `robots.txt` to non-browser user agents?

## 2. Access files

- `/llms.txt` present, parseable as Markdown, with a summary and linked sections.
- `/llms.json` and `/ai-access.json` present and consistent with `llms.txt`.
- Content matches what the site actually publishes (no stale page list).

## 3. Schema and metadata

- Title and meta description present, unique, and descriptive of the page rather than the brand.
- One clear `h1`, headings in order.
- JSON-LD valid and consistent with visible content. A `Product` block whose price differs from the page is a fail.

## 4. Scoring

Each test is pass, partial or fail. The visibility score weights crawler access highest, because a blocked crawler makes every other fix irrelevant.

## Known limits

- Results describe what an unauthenticated crawler receives today, not what a provider's index contains.
- Provider behaviour changes without notice; re-run before quoting a number to a client.
