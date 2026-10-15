import html
D="google.com maps.apple.com bing.com facebook.com yelp.com bbb.org mapquest.com yellowpages.com superpages.com dexknows.com nextdoor.com manta.com merchantcircle.com hotfrog.com foursquare.com chamberofcommerce.com cybo.com bizapedia.com brownbook.net localstack.com n49.com yellowbook.com yellowbot.com ezlocal.com showmelocal.com".split()
M=["site search","URL pattern","phone","browser ladder"]
WALLS=["captcha","login required","blocked (HTTP 403)"]
B={"scc":dict(name="Senior Care Consulting",other="Nacke Media",nm="Example Senior Care Co",addr="100 Example St, Faketown, ST 00000",ph="(555) 010-0100",
  st="f f a f x a f f x a f f a x f f a f a x f f a f a".split(),
  bad={"yelp.com":("n","Example Senior Care LLC",),"mapquest.com":("p","(555) 010-0199"),"manta.com":("a","200 Sample Ave, Faketown, ST 00000")}),
 "nm":dict(name="Nacke Media",other="Senior Care Consulting",nm="Example Media Co",addr="300 Demo Blvd, Faketown, ST 00000",ph="(555) 010-0200",
  st="f f f a x f a f f a x f a f f a f x f a f a f x a".split(),
  bad={"facebook.com":("p","(555) 010-0299"),"bbb.org":("a","301 Demo Blvd, Faketown, ST 00000"),"hotfrog.com":("n","Example Media Company")})}
CSS="""*{box-sizing:border-box}body{font:16px/1.4 system-ui,sans-serif;margin:0;padding:12px;background:#f5f6f8;color:#1a1a1a}h1{font-size:1.4rem;margin:.2em 0}
.banner{background:#fff3cd;border:1px solid #e0c36a;padding:8px;border-radius:6px;font-size:.85rem;margin:8px 0}
.card{display:block;background:#fff;border-radius:10px;padding:14px;margin:12px 0;text-decoration:none;color:inherit;box-shadow:0 1px 3px #0002}
.row{background:#fff;border-radius:8px;padding:10px;margin:8px 0;box-shadow:0 1px 2px #0002}.row h3{margin:0 0 6px;font-size:1rem}
.chip{display:inline-block;padding:2px 10px;border-radius:12px;font-size:.8rem;font-weight:600;color:#fff}
.found{background:#1e8e3e}.absent{background:#b06000}.cant{background:#6b6b6b}.ok{color:#1e8e3e}.no{color:#c5221f;font-weight:700}
.meta{font-size:.8rem;color:#555;margin-top:6px}a{color:#0b57d0;word-break:break-all}.counts span{margin-right:12px}"""
def page(t,body):
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(t)}</title><style>{CSS}</style></head><body>{body}</body></html>'
BAN='<div class="banner">PROTOTYPE &mdash; fake data. Every listing, address and phone below is invented (555 numbers, example.com).</div>'
cnt={}
for k,b in B.items():
    rows=[];c=dict(f=0,a=0,x=0)
    for i,d in enumerate(D):
        s=b["st"][i];c[s]+=1
        ts=f"2026-10-15 {9+i//10:02d}:{(i*7)%60:02d} CT";m=M[i%4]
        if s=="f":
            bad=b["bad"].get(d);nm,ad,ph=b["nm"],b["addr"],b["ph"];fl=[1,1,1]
            if bad:
                if bad[0]=="n":nm=bad[1];fl[0]=0
                elif bad[0]=="p":ph=bad[1];fl[2]=0
                else:ad=bad[1];fl[1]=0
            t=lambda v:'<span class="ok">&#10003;</span>' if v else '<span class="no">&#10007;</span>'
            url=f"https://example.com/fake/{d}/{k}"
            det=f'<div><a href="{url}">{url}</a></div><div>Name: {html.escape(nm)} {t(fl[0])}</div><div>Address: {html.escape(ad)} {t(fl[1])}</div><div>Phone: {ph} {t(fl[2])}</div>'
            chip='<span class="chip found">found</span>'
        elif s=="a":
            chip='<span class="chip absent">absent</span>'
            det=f'<div>Positive control: search proven working &mdash; found {b["other"]} in same run.</div>'
        else:
            chip='<span class="chip cant">couldn\'t check</span>'
            det=f'<div>Wall: {WALLS[i%3]}</div>'
        rows.append(f'<div class="row"><h3>{d} {chip}</h3>{det}<div class="meta">Method: {m} &middot; Last checked: {ts}</div></div>')
    cnt[k]=c
    can=f'<div class="meta">Canonical (fake): {b["nm"]} &middot; {b["addr"]} &middot; {b["ph"]}</div>'
    open(f"{k}.html","w",encoding="utf-8").write(page(b["name"],f'<a href="index.html">&larr; Home</a><h1>{b["name"]}</h1>{BAN}{can}<p class="counts"><span>{c["f"]} found</span><span>{c["a"]} absent</span><span>{c["x"]} couldn\'t check</span></p>'+"".join(rows)))
cards="".join(f'<a class="card" href="{k}.html"><h2>{b["name"]}</h2><div class="counts"><span><b>{cnt[k]["f"]}</b> found</span><span><b>{cnt[k]["a"]}</b> absent</span><span><b>{cnt[k]["x"]}</b> couldn\'t check</span></div></a>' for k,b in B.items())
open("index.html","w",encoding="utf-8").write(page("Citation Engine prototype",f'<h1>Citation Engine</h1>{BAN}{cards}'))
print(cnt)
