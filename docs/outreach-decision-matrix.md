# Cold outreach decision matrix

Purpose: score every prospect before contact, so agents send fewer, better emails and never invent urgency.

## Gate 1 - hard filters (any failure = excluded, no exceptions)
1. A contact email is visible on the prospect's own website, with the source URL recorded.
2. The prospect is an agency or consultancy selling SEO, content or growth, 2-25 staff.
3. They manage client sites (services page or case studies confirm it).
4. English-language site, business contact only.
5. The hook is a fact we fetched today: a 404, a missing file, a wrong token, a JS shell, a cross-domain sitemap.
6. No prior contact in the last 30 days, unless this is the scheduled follow-up.

## Gate 2 - scoring (1-5 each)
- *Hook severity*: 5 = AI crawler blocked or site unreadable to fetchers; 3 = llms.txt missing or wrong; 1 = cosmetic.
- *Buyer fit*: 5 = sells AI search or GEO explicitly; 3 = sells technical SEO; 1 = general marketing.
- *Ability to pay*: 5 = published retainers or a pricing page; 3 = case studies only; 1 = no commercial signal.
- *Reachability*: 5 = named human; 3 = role inbox; 1 = form only.
- *Timing*: 5 = published about AI search in the last 60 days; 1 = no recent activity.

## Gate 3 - routing
- 22-25: *A tier*. Send the personalised email with a private audit report link within 24 hours.
- 17-21: *B tier*. Send the short email, no report.
- 12-16: *C tier*. Hold, revisit only if the site changes.
- Under 12: *Reject* and log the reason.

## Cadence and safety
- Maximum 10 first contacts per day per sending domain, unique copy per prospect.
- Follow-up 1 on day 3, follow-up 2 on day 7, then close. One thread per prospect.
- No identical body text across prospects. No bulk CC or BCC. Stop on any bounce or complaint.
- Every send is logged with the prospect id, hook evidence, subject, and message id.

## Automation
1. Agent audits a domain and stores the findings as JSON.
2. Report page is generated from the JSON, unlisted and prospect-specific.
3. Email quotes one finding and links the report.
4. Replies are triaged: interested, not now, no. Only "interested" becomes a lead.
