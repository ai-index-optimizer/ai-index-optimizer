# Domain-match gate

Every cold email must pass `gate.py` before it is sent. The gate answers one question: can we prove this address belongs to the business we audited?

## Verdict order
1. **pass, domain match** - the email domain is the audited site's registrable domain, or a subdomain of it.
2. **pass, published on site** - a live fetch of the audited site's homepage and contact/about pages contains the address. The evidence URL is stored with the row.
3. **pass, manual override** - listed in `gate_allowlist.csv` with a written reason and approver.
4. **block** - everything else: placeholder addresses, junk strings scraped from CSS or asset filenames, a domain belonging to a different business that does not publish the address, and free mailboxes with no proof of ownership.

## Files
- `gate_report.csv` - every address judged, with verdict, reason, evidence URL and timestamp.
- `send_ready.csv` - passes only. **Sends come from this file and nothing else.**
- `gate_allowlist.csv` - the only way to override a block. Requires a reason.

## Run
`python3 gate.py` (defaults to the five lead files) or `python3 gate.py file1.csv file2.csv`

## Result of the first run, 18 Nov 2026 22:20 UTC
89 addresses judged: 77 pass, 12 blocked.

21 addresses passed only because they are published on the audited site, including free mailboxes such as jamandtoast30024@gmail.com and craigjeffress@aol.com. Those are legitimate: the business publishes them on its own site.

Blocked: two placeholder rows (example@mail.com), four junk strings scraped from CSS or asset names (wght@8..60, katex@0.13.24, portrait-risu@2x.webp, you@company.com, you@yourbusiness.com), one unprovable free mailbox (cmf0732@yahoo.com), and two GitHub prospects whose real domain differs from the audited subdomain (loudface.co vs a vercel.app preview, lastagencyhere.com vs another vercel.app preview).

## Correction
The Bloom Room address gerson@thesuwaneesocial.com was reported on 18 Nov as a domain mismatch. The live check disproves that: the address is published on bloomroomsocial.com itself, same owner, two businesses. It passes. The earlier call was wrong and is logged in BUG_LOG.
