# GitHub lead engine

Status: v1, run 2026-11-18. Discovery and qualification only.

## What this is, and what it is not

GitHub is used here as a **lead source and proof layer**, not as a place to advertise.
GitHub's Acceptable Use Policies prohibit spam, unsolicited advertising and bulk
@mentions. Posting marketing copy into other people's repos or @mentioning strangers
to promote a product gets an organisation suspended, and a suspended org loses the
Pages site and the repo that the outreach depends on. So the engine never posts
marketing into other repos. Contact happens by email, through the outreach pipeline.

## Pipeline

1. **Scan.** Repository search across eight queries (llms.txt in readme, generative
   engine optimization, AI visibility, topic:ai-seo, topic:generative-engine-optimization,
   topic:geo-seo, seo agency, topic:seo-tools), filtered to repos pushed in the last 90 days.
2. **Resolve the human.** For each owner, pull the profile: website (blog field), X handle,
   follower count, last push. Drop owners over 20k followers (not a boutique buyer) and
   owners with no resolvable website.
3. **Qualify or skip.** Hard gate: the site must return HTTP 200 and its text must mention
   SEO, AEO, GEO, content marketing or an agency offer. Everything else is dropped, not
   queued. This gate removes roughly two thirds of raw hits.
4. **Audit the site.** Fetch robots.txt, llms.txt and the homepage. Record: robots status,
   llms.txt status, how many of seven named AI crawlers appear, visible text length
   (a JS shell scores near zero), and any email found in the page.
5. **Score.** Hook severity, buyer fit, ability to pay, reachability, timing, per the
   decision matrix in `outreach-decision-matrix.md`. Route: 22-25 A, 17-21 B, 12-16 C,
   under 12 reject with the reason logged.
6. **Table.** Output is a private CSV in the agent workspace. It is never committed:
   it contains third-party contact details.

## Result of the first run

188 owners scanned, 85 passed the website and topic gate, 3 A, 42 B, 40 C.
Genuine agency or tool buyers among them: a handful (SE Ranking, RankSpot, Houtini,
Rebelytics). The rest are indie developers with a personal site. That ratio is the
finding: **GitHub's population is not the ICP.** Boutique SEO agencies publish on
their own domains and on LinkedIn, not in repos.

## How it should be used

- As a secondary source, run weekly, feeding only the A and B rows into the email pipeline.
- As the proof layer: every prospect email links a dated, reproducible audit page.
- Never as a broadcast channel. No @mentions, no issue spam, no identical comments.

## Versioning

Every change to this engine or the matrix bumps `VERSION` and adds a line to
`PATCH_NOTES.md`. Scoring changes must be re-run against the last CSV so tier movement
is visible rather than assumed.
