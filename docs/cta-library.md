# CTA library and A/B protocol

Version 1.0, 2026-11-18. Every variant below is tagged `[C#]`; the send queue records the tag so replies can be attributed.

## Why this exists

The first-contact email has one job: earn a reply. Not a sale, not a click. So the CTA is a question a busy owner can answer in four words, and every variant is tested against the same offer (a free audit of their site).

## Segment A - local businesses (restaurants, cafes, salons, clinics)

- **C1 Hidden** (loss aversion, the default): "When someone asks ChatGPT where to eat in {city}, does it name you, or are you invisible in the answer?"
- **C2 Tourist** (specific demand): "A visitor asks AI for the best {cuisine} in {city} tonight. Right now it cannot read your menu, so it names someone else."
- **C3 Peer proof** (social proof): "{n} of {total} {city} {category} we tested name zero AI crawlers in robots.txt. Yours is one of them."
- **C4 Specific fix** (competence): "Your site has no llms.txt and names zero AI crawlers. That is a two-hour fix, and I will send you the six steps."
- **C5 Zero risk** (reciprocity): "I will send the findings either way, no call needed. Reply 'send it' and it is in your inbox today."

## Segment B - SEO agencies

- **B1 Hidden**: "Does your client show up when AI is asked for {service} in {city}, or does it name a competitor?"
- **B2 Peer proof**: "{n} of {total} agencies we tested cannot be read by AI crawlers, including yours."
- **B3 Specific fix**: "{site}/llms.txt returns 404 and robots.txt names {k} of 5 AI crawlers."
- **B4 Free sample**: "Name one client site and I will send the audit, findings only, no deck."

## Subject line bank

Short, lower case, no exclamation, no emoji, under 55 characters:
`does AI name your restaurant?` / `{business} is invisible to ChatGPT` / `{city} {category}: {n} of {total} fail` / `no llms.txt on {domain}` / `quick question about {business}`

## A/B protocol

1. Assign variants in rotation by row order, so no variant is clustered in time.
2. Minimum 20 sends per variant before judging. Below that, a 10% difference is noise.
3. Primary metric: reply rate. Secondary: audit-request rate. Opens are not measurable (no pixel in cold email, by policy).
4. Winner is adopted for the segment, and the losers are kept in the library with a dated note rather than deleted.
5. Log every send in `send_queue.csv` with columns `variant`, `sent_at`, `message_id`, and every reply in `replies.csv` with `variant`, `reply_type` (interested / not now / no / bounce).

## Compliance

Local commercial email needs a real postal address in the body and a working opt-out. We have neither yet: **do not send at volume until an address is supplied.** Until then, the opt-out line alone is used and volume stays at 5 a day.
