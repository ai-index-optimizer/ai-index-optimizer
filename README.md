# AI Index Optimizer

AI visibility audits for SEO agencies. We test whether AI crawlers can actually reach a site, then generate the fixes that make pages citable in ChatGPT, Claude, Gemini and Perplexity answers.

Live product: https://ai-index-optimizer.com
Demo video (73s, narrated): https://base44.app/api/apps/6aa0e7df26e5fa37f7ec9c7b/files/mp/public/6aa0e7df26e5fa37f7ec9c7b/f8514cebf_ai-index-optimizer-demo.mp4

## The problem

A page can rank in Google and still be invisible in AI answers. Assistants only read what their crawlers are allowed to fetch, and only quote what they can parse. When GPTBot, OAI-SearchBot, ClaudeBot or PerplexityBot are blocked in `robots.txt`, when there is no `llms.txt`, or when structured data is missing or stale, classic SEO work does not move the needle.

## What the audit checks

1. **Crawler access** - whether each named AI crawler is allowed by `robots.txt`, reachable through the CDN or firewall, and not sitting behind a login wall or bot challenge.
2. **Access files** - whether `/llms.txt`, `/llms.json` and `/ai-access.json` exist, parse, and describe the site the way assistants read it.
3. **Schema and metadata** - title tags, meta descriptions, heading structure and JSON-LD that decide whether a page can be quoted.
4. **Per-provider visibility** - what each provider can see, reported separately rather than as one blended score.

## What it produces

- A prioritised fix list per domain.
- Deployable `robots.txt` crawler directives and an `llms.txt` file.
- Corrected JSON-LD and metadata.

Samples of the generated files are in [`samples/`](samples/), and the method is documented in [`docs/`](docs/).

## Pricing

| Plan | Price | Domains |
|---|---|---|
| Free | $0/mo | 1, one full audit |
| Starter | $39/mo | 3, unlimited rescans |
| Growth | $99/mo | 10, branded reports |
| Agency | $299/mo | 30, white-label, bulk scans |

## Status

Working audit engine and live product. Multi-language routing in progress. The service is proprietary; this repository documents the product and its method, not the engine source.

Contact: hello@ai-index-optimizer.com
