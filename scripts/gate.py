#!/usr/bin/env python3
"""Domain-match gate for cold email.

A prospect may only be emailed when we can prove the address belongs to the
business we audited. Three ways to prove it, in order:
  1. the email domain is the audited site's domain
  2. the address is published on the audited site (live fetch, evidence URL kept)
  3. an explicit manual override in gate_allowlist.csv, with a reason
Anything else is blocked. Run before every send batch.

Outputs: gate_report.csv (every address judged) and send_ready.csv (passes only).
"""
import csv, sys, re, datetime, concurrent.futures, requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
FREE = {"gmail.com","googlemail.com","yahoo.com","yahoo.co.uk","hotmail.com","outlook.com","live.com",
        "msn.com","aol.com","icloud.com","me.com","mac.com","mail.com","gmx.com","gmx.de","proton.me",
        "protonmail.com","zoho.com","yandex.com","comcast.net","att.net","verizon.net","sbcglobal.net","rocketmail.com"}
PLACEHOLDER = {"example.com","example.org","example.net","domain.com","yourdomain.com","email.com",
               "test.com","mail.com","sample.com","website.com","yourbusiness.com","company.com"}
MULTI = {"co.uk","org.uk","ac.uk","com.au","net.au","co.nz","co.za","co.in","com.br","com.mx","co.jp","ne.jp","com.np"}
EMAIL_RE = re.compile(r"^[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}$")

def reg_domain(d):
    d = (d or "").strip().lower().rstrip(".")
    if not d: return ""
    if "://" in d: d = urlparse(d).netloc
    d = d.split("?")[0].split("/")[0].split(":")[0]
    if d.startswith("www."): d = d[4:]
    parts = [p for p in d.split(".") if p]
    if len(parts) >= 3 and ".".join(parts[-2:]) in MULTI: return ".".join(parts[-3:])
    return ".".join(parts[-2:]) if len(parts) >= 2 else d

def clean_email(e):
    e = (e or "").strip().lower().strip(".,;:<>()[]'\"")
    if not e or e.count("@") != 1: return ""
    if not EMAIL_RE.match(e): return ""
    dom = e.split("@")[1]
    if dom in PLACEHOLDER: return ""
    if re.search(r"@[0-9]", e) or re.search(r"\.(png|jpe?g|gif|webp|svg|css|js)$", e): return ""
    if re.search(r"@[0-9.]+$", dom): return ""
    if e.split("@")[0] in {"you","your","name","email","test","example","user"}: return ""
    return e

def site_pages(domain):
    urls = [f"https://{domain}/"]
    try:
        r = requests.get(urls[0], headers={"User-Agent": UA}, timeout=12, allow_redirects=True)
        if r.status_code < 400:
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.find_all("a", href=True):
                h = a["href"].lower()
                if any(k in h for k in ["contact","about","team","hello","impressum"]):
                    full = requests.compat.urljoin(r.url, a["href"])
                    if reg_domain(urlparse(full).netloc) == reg_domain(domain) and full not in urls:
                        urls.append(full)
                if len(urls) >= 4: break
    except Exception:
        pass
    return urls[:4]

def published_on_site(domain, email):
    """Return the URL where the address appears on the audited site, else ''."""
    if not domain: return ""
    for u in site_pages(domain):
        try:
            r = requests.get(u, headers={"User-Agent": UA}, timeout=12, allow_redirects=True)
            if r.status_code >= 400: continue
            text = r.text.lower()
            if email in text or email.replace("@", "%40") in text:
                return r.url
        except Exception:
            continue
    return ""

def judge(row, overrides):
    email = clean_email(row["email"]); site = row["site"]
    if not email:
        return "block", "no valid email address (empty, placeholder or junk string)", ""
    if not site:
        return "block", "no audited site on record", ""
    sdom, edom = reg_domain(site), email.split("@")[1]
    if edom == sdom or edom.endswith("." + sdom) or sdom.endswith("." + edom):
        return "pass", "email domain matches the audited site", ""
    ev = published_on_site(sdom, email)
    if ev:
        return "pass", f"address published on the audited site ({'free mailbox' if edom in FREE else 'different domain'})", ev
    if email in overrides:
        return "pass", "manual override: " + overrides[email], ""
    if edom in FREE:
        return "block", f"free mailbox and not published on {sdom}: cannot prove it belongs to this business", ""
    return "block", f"email domain {edom} does not match audited site {sdom} and the address is not published there", ""

def load(path):
    rows = []
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        for r in csv.DictReader(f):
            site = r.get("domain") or r.get("site") or r.get("host") or ""
            rows.append({"source": path,
                         "name": r.get("business") or r.get("owner") or site,
                         "site": site, "email": r.get("email") or ""})
    return rows

def main(files):
    overrides = {}
    try:
        with open("gate_allowlist.csv", newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                overrides[r["email"].strip().lower()] = r.get("reason", "")
    except FileNotFoundError:
        pass
    rows = [r for p in files for r in load(p) if (r["email"] or "").strip()]
    out = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        for r, (verdict, reason, ev) in zip(rows, ex.map(lambda x: judge(x, overrides), rows)):
            r.update(verdict=verdict, reason=reason, evidence_url=ev,
                     checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"))
            out.append(r)
    fields = ["source","name","site","email","verdict","reason","evidence_url","checked_at"]
    for name, keep in (("gate_report.csv", out), ("send_ready.csv", [r for r in out if r["verdict"] == "pass"])):
        with open(name, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(keep)
    passed = [r for r in out if r["verdict"] == "pass"]
    print(f"judged {len(out)}: {len(passed)} pass, {len(out)-len(passed)} blocked")
    print("\nBLOCKED:")
    for r in out:
        if r["verdict"] == "block":
            print(f"  {r['email'][:40]:<40} {r['site'][:28]:<28} {r['reason'][:70]}")

if __name__ == "__main__":
    main(sys.argv[1:] or ["local_leads_atlanta.csv","local_leads_atlanta2.csv","local_leads_savannah.csv","send_queue.csv","github_leads_v2.csv"])
