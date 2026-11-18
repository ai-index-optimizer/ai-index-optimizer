#!/usr/bin/env python3
"""Local business lead engine: OpenStreetMap -> website -> contact email -> AI visibility audit -> CTA variant.
No Maps API key needed. Emails are only taken from the business's own site."""
import json,re,csv,ssl,urllib.request,urllib.error,urllib.parse,concurrent.futures as cf,sys
UA={'User-Agent':'Mozilla/5.0 (compatible; AIO-Audit/1.0)'}
CRAWL=['GPTBot','OAI-SearchBot','ClaudeBot','PerplexityBot','Google-Extended']
def get(u,timeout=15,limit=90000):
    try:
        r=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=timeout,context=ssl.create_default_context())
        return r.status,r.read(limit).decode('utf-8','replace')
    except urllib.error.HTTPError as e: return e.code,''
    except Exception: return 0,''
MIRRORS=['https://overpass.kumi.systems/api/interpreter','https://overpass-api.de/api/interpreter','https://overpass.private.coffee/api/interpreter']
def osm(bbox,limit=40):
    q=f'[out:json][timeout:60];(node["amenity"~"restaurant|cafe|bar|bakery"]["website"]({bbox});way["amenity"~"restaurant|cafe|bar|bakery"]["website"]({bbox}););out center {limit};'
    b=''
    for base in MIRRORS:
        s,b=get(base+'?data='+urllib.parse.quote(q),70)
        if s==200 and b.strip().startswith('{'): break
        s=0
    if s!=200: print('overpass unavailable, last status',s); return []
    out=[]
    for e in json.loads(b).get('elements',[]):
        t=e.get('tags',{}); w=t.get('website') or t.get('contact:website') or ''
        if not w: continue
        out.append(dict(name=t.get('name',''),site=w,city=t.get('addr:city',''),phone=t.get('phone','') or t.get('contact:phone',''),cuisine=t.get('cuisine','')))
    return out
BAD=('.png','.jpg','.jpeg','.svg','.webp','sentry','wixpress','example.com','domain.com')
def emails_on(base,paths=('', '/contact','/contact-us','/about','/about-us')):
    found=[]
    for p in paths:
        s,h=get(base+p.rstrip('/')+'/' if p else base+'/')
        if s!=200: continue
        for m in re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',h):
            m=m.strip('.').lower()
            if any(b in m for b in BAD): continue
            if m not in found: found.append(m)
        if found: break
    return found
def owner_name(base):
    s,h=get(base+'/about')
    if s!=200: s,h=get(base+'/')
    for pat in [r'(?:owner|founder|chef)[^<]{0,20}(?:is|:)\s*([A-Z][a-z]+ [A-Z][a-z]+)',r'"founder"\s*:\s*\{[^}]*"name"\s*:\s*"([^"]+)"']:
        m=re.search(pat,h)
        if m: return m.group(1)[:40]
    return ''
def probe(b):
    base=b['site'] if b['site'].startswith('http') else 'https://'+b['site']
    base=base.rstrip('/')
    host=urllib.parse.urlparse(base).netloc.replace('www.','')
    hs,home=get(base+'/')
    if hs!=200: return None
    text=re.sub(r'<script.*?</script>|<style.*?</style>','',home,flags=re.S)
    text=re.sub(r'<[^>]+>',' ',text); text=re.sub(r'\s+',' ',text).strip()
    rs,robots=get(base+'/robots.txt'); ls,llms=get(base+'/llms.txt')
    hits=[c for c in CRAWL if c in robots]
    mails=emails_on(base)
    mails=[m for m in mails if host.split('.')[0] in m] or mails
    if not mails: return None
    return dict(business=b['name'],host=host,site=base,email=mails[0],city=b['city'],cuisine=b['cuisine'],
        owner=owner_name(base),robots=rs,llms=ls,crawlers=len(hits),text_len=len(text),
        hook=f"llms.txt {ls if ls else 'missing'}, {len(hits)}/5 AI crawlers named, {len(text)} chars of visible text")
if __name__=='__main__':
    bbox=sys.argv[1] if len(sys.argv)>1 else '30.20,-97.80,30.32,-97.68'
    cands=osm(bbox)
    print('OSM businesses with a website:',len(cands))
    rows=[]
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        for r in ex.map(probe,cands):
            if r: rows.append(r)
    rows.sort(key=lambda r:(r['llms']==200, -r['text_len']))
    with open('local_leads.csv','w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys()) if rows else ['business']); w.writeheader(); w.writerows(rows)
    print('with a contact email on their own site:',len(rows),'| owner name found:',sum(1 for r in rows if r['owner']))
    for r in rows[:10]: print(f"{r['business'][:26]:<26} {r['host'][:28]:<28} {r['email'][:32]:<32} llms={r['llms']} crawl={r['crawlers']}/5 txt={r['text_len']}")
