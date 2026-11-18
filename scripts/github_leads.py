#!/usr/bin/env python3
"""GitHub lead engine: discover repos/users, qualify their websites, score with the outreach matrix.
Discovery only. Contact happens by email through the outreach pipeline, never by @mention spam."""
import os,json,re,csv,ssl,urllib.request,urllib.error,concurrent.futures as cf
from datetime import datetime,timezone,timedelta
GH=os.environ.get('GITHUB_ACCESS_TOKEN','')
QUERIES=[
 'llms.txt in:readme pushed:>2026-08-20',
 '"generative engine optimization" in:readme pushed:>2026-08-20',
 '"AI visibility" in:description pushed:>2026-08-20',
 'topic:ai-seo','topic:generative-engine-optimization','topic:geo-seo',
 'seo agency in:description pushed:>2026-08-20',
 'topic:seo-tools pushed:>2026-08-20',
]
UA={'User-Agent':'AIO-LeadEngine/1.0'}
def gh(u):
    try:
        r=urllib.request.urlopen(urllib.request.Request(u,headers={**UA,'Authorization':f'Bearer {GH}','Accept':'application/vnd.github+json'}),timeout=25)
        return json.load(r)
    except Exception: return {}
def fetch(url):
    try:
        r=urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=12,context=ssl.create_default_context())
        return r.status,r.read(80000).decode('utf-8','replace')
    except urllib.error.HTTPError as e: return e.code,''
    except Exception: return 0,''
def domain_of(u):
    if not u: return ''
    u=u.strip()
    if not u.startswith('http'): u='https://'+u
    m=re.match(r'https?://([^/]+)',u)
    return m.group(1).lower().replace('www.','') if m else ''
CRAWLERS=['GPTBot','OAI-SearchBot','ChatGPT-User','ClaudeBot','PerplexityBot','Google-Extended','CCBot']
seen={}
for q in QUERIES:
    d=gh('https://api.github.com/search/repositories?q='+urllib.parse.quote(q)+'&sort=updated&per_page=30')
    for it in d.get('items',[]):
        o=it['owner']['login']
        if o.lower() in ('ai-index-optimizer',): continue
        seen.setdefault(o,{'repo':it['full_name'],'homepage':it.get('homepage') or '','desc':(it.get('description') or '')[:160],'pushed':it.get('pushed_at','')})
print('owners discovered:',len(seen))
rows=[]
def probe(o):
    u=gh('https://api.github.com/users/'+o)
    if not u or u.get('followers',0)>20000: return None
    site=domain_of(u.get('blog') or seen[o]['homepage'])
    if not site or 'github.io' in site and not u.get('blog'): return None
    base='https://'+site
    rs,robots=fetch(base+'/robots.txt'); ls,llms=fetch(base+'/llms.txt'); hs,home=fetch(base+'/')
    if hs!=200: return None
    text=re.sub(r'<script.*?</script>|<style.*?</style>','',home,flags=re.S)
    text=re.sub(r'<[^>]+>',' ',text); text=re.sub(r'\s+',' ',text).strip()
    title=(re.search(r'<title[^>]*>(.*?)</title>',home,re.S) or [None,''])[1].strip()[:110]
    hits=[c for c in CRAWLERS if c in robots]
    socials=[s for s in ('x.com','twitter.com','linkedin.com','youtube.com') if s in home.lower()]
    recent=seen[o]['pushed'][:10]
    try: fresh=(datetime.now(timezone.utc)-datetime.fromisoformat(seen[o]['pushed'].replace('Z','+00:00'))).days
    except Exception: fresh=999
    blob=(title+' '+seen[o]['desc']+' '+text[:3000]).lower()
    if not any(k in blob for k in ('seo','search engine','aeo','geo ','generative engine','content marketing','marketing agency','growth agency','link building')):
        return None
    mails=set(re.findall(r'[\w.+-]+@[\w-]+\.[\w.]{2,}',home))
    mails={m for m in mails if not m.lower().endswith(('.png','.jpg','.svg','sentry.io','example.com'))}
    hook=5 if (hits and ls!=200) else 4 if ls!=200 else 3 if len(hits)==0 else 2 if len(hits)<3 else 1
    fit=5 if any(k in blob for k in ('ai seo','geo','generative','llm','ai visibility')) else 3 if 'seo' in blob else 1
    pay=3 if any(k in home.lower() for k in ('pricing','retainer','/plans')) else 2
    reach=3 if u.get('email') else 2
    timing=5 if fresh<=30 else 3 if fresh<=90 else 1
    total=hook+fit+pay+reach+timing
    tier='A' if total>=22 else 'B' if total>=17 else 'C' if total>=12 else 'X'
    return dict(owner=o,kind=u.get('type',''),site=site,title=title,followers=u.get('followers',0),
        twitter=u.get('twitter_username') or '',socials=len(socials),robots=rs,llms=ls,crawlers=len(hits),
        text_len=len(text),repo=seen[o]['repo'],last_push=recent,score=total,tier=tier,
        hook=f"llms.txt {ls}, {len(hits)}/7 AI crawlers named, {len(text)} chars visible text",
        email=(sorted(mails)[0] if mails else ''))
with cf.ThreadPoolExecutor(max_workers=10) as ex:
    for r in ex.map(probe,list(seen)):
        if r: rows.append(r)
rows.sort(key=lambda r:-r['score'])
with open('github_leads_v2.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys()) if rows else ['owner']); w.writeheader(); w.writerows(rows)
from collections import Counter
print('qualified:',len(rows),Counter(r['tier'] for r in rows))
for r in rows[:12]:
    print(f"{r['tier']} {r['score']:>2} {r['owner'][:22]:<22} {r['site'][:30]:<30} llms={r['llms']} crawlers={r['crawlers']}/7 txt={r['text_len']} push={r['last_push']}")
