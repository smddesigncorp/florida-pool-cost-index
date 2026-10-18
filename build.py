import json,os,html,re
D=json.load(open('data.json')); OUT='site'; os.makedirs(OUT,exist_ok=True)
E=html.escape
def money(v): return "${:,.0f}".format(v)
# ---------- Brand: logo mark (pool with tile edge, sun, waves) ----------
MARK_DEFS='''<defs><linearGradient id="fpciW" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5fe0ec"/><stop offset="1" stop-color="#0a86a8"/></linearGradient></defs>'''
MARK_BODY='''<rect x="3" y="3" width="58" height="58" rx="16" fill="#fff"/><rect x="3" y="3" width="58" height="58" rx="16" fill="none" stroke="#0a7ea4" stroke-width="3" stroke-dasharray="7 3"/><rect x="9" y="9" width="46" height="46" rx="11" fill="url(#fpciW)"/><circle cx="43" cy="21" r="7" fill="#ffd23f"/><path d="M15 35q4.5-5 9 0t9 0t9 0t9 0" fill="none" stroke="#fff" stroke-width="3.6" stroke-linecap="round"/><path d="M15 45q4.5-5 9 0t9 0t9 0t9 0" fill="none" stroke="#e0fbff" stroke-width="3.6" stroke-linecap="round" opacity=".85"/>'''
def mark(size=44,cls="logo-mark"): return f'<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 64 64" aria-hidden="true" focusable="false">{MARK_DEFS}{MARK_BODY}</svg>'
LOGO_SVG=f'''<svg xmlns="http://www.w3.org/2000/svg" width="420" height="64" viewBox="0 0 420 64" role="img" aria-label="Florida Pool Cost Index">{MARK_DEFS}{MARK_BODY}<text x="76" y="30" font-family="Nunito, 'Trebuchet MS', Arial, sans-serif" font-size="24" font-weight="900" fill="#073b52">Florida Pool</text><text x="76" y="54" font-family="Nunito, 'Trebuchet MS', Arial, sans-serif" font-size="20" font-weight="800" fill="#0a7ea4">Cost Index</text></svg>'''
FAV_SVG=f'<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">{MARK_DEFS}{MARK_BODY}</svg>'
APPLE_SVG=f'<svg xmlns="http://www.w3.org/2000/svg" width="180" height="180" viewBox="0 0 64 64"><rect width="64" height="64" fill="#fdf6ea"/><g transform="translate(4 4) scale(.875)">{MARK_DEFS}{MARK_BODY}</g></svg>'
def write_brand_assets():
    open(os.path.join(OUT,'logo.svg'),'w').write(LOGO_SVG)
    open(os.path.join(OUT,'favicon.svg'),'w').write(FAV_SVG)
    try:
        import cairosvg,io
        from PIL import Image
        cairosvg.svg2png(bytestring=APPLE_SVG.encode(),write_to=os.path.join(OUT,'apple-touch-icon.png'),output_width=180,output_height=180)
        png=cairosvg.svg2png(bytestring=FAV_SVG.encode(),output_width=64,output_height=64)
        Image.open(io.BytesIO(png)).convert('RGBA').save(os.path.join(OUT,'favicon.ico'),sizes=[(32,32),(16,16)])
    except ImportError:
        print("cairosvg/Pillow not installed: favicon.ico and apple-touch-icon.png left as-is")
# Caustic light pattern (pool-floor ripples) as an inline SVG data URI
CAUSTIC="url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='120' viewBox='0 0 160 120'%3E%3Cg fill='none' stroke='%23ffffff' stroke-width='3' stroke-linecap='round' opacity='.55'%3E%3Cpath d='M-5 20c15-12 30 8 45-2s25-14 40 0 30 6 40-4 25 2 45 6'/%3E%3Cpath d='M-5 62c18 10 28-12 46-4s22 16 38 4 28-10 42 0 24 6 44-2'/%3E%3Cpath d='M-5 102c14-8 26 10 42 2s30-14 44-2 26 8 40-2 22-4 44 4'/%3E%3Cpath d='M30 0c-6 14 10 22 4 36s-12 22-2 34 4 30 0 50' opacity='.6'/%3E%3Cpath d='M110 0c8 12-8 24 0 38s14 22 2 34-6 28 0 48' opacity='.6'/%3E%3C/g%3E%3C/svg%3E\")"
WAVE='<svg viewBox="0 0 1440 70" preserveAspectRatio="none" aria-hidden="true" focusable="false"><path d="M0 34c120 26 240 26 360 6s240-34 360-14 240 40 360 26 240-30 360-20v38H0z" fill="#fdf6ea"/><path d="M0 50c160-18 300 14 460 6s300-30 470-14 330 26 510 8" fill="none" stroke="#bdeef3" stroke-width="3"/></svg>'
DIVIDER='<div class="wave-div" aria-hidden="true"><svg viewBox="0 0 600 24" preserveAspectRatio="none" focusable="false"><path d="M0 12q25-12 50 0t50 0t50 0t50 0t50 0t50 0t50 0t50 0t50 0t50 0t50 0t50 0" fill="none" stroke="#38c6d6" stroke-width="3" stroke-linecap="round"/></svg></div>'
SUN='<svg class="deco-sun" viewBox="0 0 100 100" aria-hidden="true" focusable="false"><g stroke="#ffb703" stroke-width="5" stroke-linecap="round"><path d="M50 4v12M50 84v12M4 50h12M84 50h12M17 17l9 9M74 74l9 9M17 83l9-9M74 26l9-9"/></g><circle cx="50" cy="50" r="22" fill="#ffd23f"/></svg>'
PALM='<svg class="deco-palm" viewBox="0 0 120 160" aria-hidden="true" focusable="false"><path d="M62 60c-4 30-2 62 6 96" stroke="#7a5230" stroke-width="7" fill="none" stroke-linecap="round"/><g fill="#2a9d6f"><path d="M62 58c-14-22-38-26-56-16 22-2 38 6 56 16z"/><path d="M62 58c12-22 36-28 54-18-22-2-38 6-54 18z"/><path d="M62 58c-24-6-44 6-50 26 14-14 30-20 50-26z"/><path d="M62 58c22-8 44 2 52 22-16-12-32-18-52-22z"/><path d="M62 58c-2-20 8-38 24-46-10 16-16 30-24 46z"/></g></svg>'
CSS="""*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font-family:Nunito,'Trebuchet MS',system-ui,sans-serif;font-size:16.5px;line-height:1.6;color:#16324a;background:#fdf6ea}
a{color:#08708f;font-weight:700;text-decoration-thickness:2px;text-underline-offset:3px}a:hover{color:#c2410c}
:focus-visible{outline:3px solid #ff8a5b;outline-offset:2px;border-radius:6px}
h1,h2,h3{color:#073b52;line-height:1.2;font-weight:900}h1{font-size:clamp(30px,5vw,50px);margin:.2em 0 .35em;letter-spacing:-.5px}
h2{font-size:26px;margin:.2em 0 .6em}h3{font-size:20px;margin:.2em 0 .7em}
.card h2,.card h3{padding-bottom:12px;background:repeating-linear-gradient(90deg,#ff7a59 0 14px,#fff 14px 18px,#16b6c8 18px 32px,#fff 32px 36px) left bottom/100% 4px no-repeat}
.skip{position:absolute;left:-999px}.skip:focus{left:12px;top:12px;background:#fff;padding:8px 14px;z-index:9;border-radius:999px}
/* header */
.site-header{background:#fff;position:relative;box-shadow:0 2px 14px rgba(7,59,82,.08)}
.site-header::after{content:"";display:block;height:8px;background:repeating-linear-gradient(90deg,#0a86a8 0 16px,#5fe0ec 16px 18px,#e6fbfd 18px 34px,#5fe0ec 34px 36px)}
.hwrap{max-width:1120px;margin:auto;padding:12px 18px;display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:#073b52;margin-right:auto}
.brand .wm{display:flex;flex-direction:column;line-height:1.02}.brand .wm b{font-size:21px;font-weight:900;color:#073b52}.brand .wm span{font-size:15px;font-weight:800;color:#0a7ea4;letter-spacing:.5px}
nav.pills{display:flex;gap:6px;flex-wrap:wrap}
nav.pills a{display:inline-block;padding:7px 14px;border-radius:999px;background:#e6f7f9;color:#0b4f66;text-decoration:none;font-size:14.5px;font-weight:800;white-space:nowrap;transition:transform .15s,background .15s}
nav.pills a:hover{background:#c9f0f4;transform:translateY(-1px);color:#073b52}nav.pills a.on{background:#08708f;color:#fff}
nav.pills a.cta,.btn{background:#ffd23f;color:#3d2c00;box-shadow:0 3px 0 #e0a800}nav.pills a.cta:hover,.btn:hover{background:#ffdf6b;color:#3d2c00}
/* hero */
.hero{position:relative;overflow:hidden;background:CAUSTIC 0 0/220px 165px,radial-gradient(circle at 15% 20%,rgba(255,255,255,.55),transparent 40%),linear-gradient(170deg,#c6f4f7 0%,#8ee3ec 55%,#5fd3e2 100%);animation:ripple 30s linear infinite}
@keyframes ripple{to{background-position:220px 165px,0 0,0 0}}@media (prefers-reduced-motion:reduce){.hero{animation:none}}
.hero .in{position:relative;z-index:2;max-width:1120px;margin:auto;padding:46px 18px 70px}.hero.small .in{padding:30px 18px 58px}.hero.small h1{font-size:clamp(28px,4.2vw,40px);max-width:820px}
.hero h1{max-width:760px;color:#06324a}.hero p.lead{max-width:640px;font-size:19px;color:#0f3d52;font-weight:600;margin:0 0 22px}
.hero .wave{position:absolute;left:0;right:0;bottom:-1px;height:60px;z-index:1}.hero .wave svg{width:100%;height:100%;display:block}
.deco-sun{position:absolute;right:6%;top:22px;width:110px;z-index:1;opacity:.95}.deco-palm{position:absolute;right:calc(6% + 70px);bottom:24px;width:120px;z-index:1;opacity:.9}.hero.small .deco-sun{width:80px;top:16px}.hero.small .deco-palm{display:none}
.btns{display:flex;gap:10px;flex-wrap:wrap}
.btn,.btn2{display:inline-flex;align-items:center;gap:8px;padding:12px 22px;border-radius:999px;font-weight:900;text-decoration:none;font-size:16.5px}
.btn2{background:#fff;color:#08708f;box-shadow:0 3px 0 #9fdde6}.btn2:hover{color:#073b52;background:#f2fdff}
main{max-width:1120px;margin:auto;padding:8px 18px 30px}
/* cards */
.card{position:relative;background:#fff;border-radius:24px;padding:24px 24px 22px;margin:22px 0;box-shadow:0 10px 30px rgba(7,59,82,.09),0 2px 6px rgba(7,59,82,.05);overflow:hidden}
.card::before{content:"";position:absolute;left:0;right:0;top:0;height:7px;background:repeating-linear-gradient(90deg,#16b6c8 0 18px,#e6fbfd 18px 20px,#7fe1ea 20px 38px,#e6fbfd 38px 40px)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(300px,100%),1fr));gap:18px}.grid>.card{margin:0}
.stat{display:flex;flex-direction:column;align-items:flex-start;gap:6px;transition:transform .15s}.stat:hover{transform:translateY(-3px)}
.stat .ico{width:50px;height:50px;border-radius:16px;display:grid;place-items:center;font-size:26px;background:#e6f7f9}
.stat:nth-child(6n+2) .ico{background:#fff4cc}.stat:nth-child(6n+3) .ico{background:#ffe6dc}.stat:nth-child(6n+4) .ico{background:#e4f7ec}.stat:nth-child(6n+5) .ico{background:#efe6fb}
.stat:nth-child(6n+2)::before{background:repeating-linear-gradient(90deg,#ffc83d 0 18px,#fff8e1 18px 20px)}.stat:nth-child(6n+3)::before{background:repeating-linear-gradient(90deg,#ff8a5b 0 18px,#fff1ea 18px 20px)}
.stat .muted{font-weight:700;color:#3f5a6c}
.big{font-size:34px;font-weight:900;color:#08708f;line-height:1.1;letter-spacing:-.5px}
.stat-row{margin:6px 0 4px}.stat-row .card{padding-top:22px}
.muted{color:#4b6475;font-size:14px}
.tag{display:inline-block;font-size:12px;font-weight:800;padding:3px 10px;border-radius:999px;vertical-align:middle;border:1.5px solid transparent;line-height:1.4}
.official{background:#ddf6e7;color:#14532d;border-color:#9fdcb8}.third{background:#fff1c2;color:#5c4300;border-color:#f2d36b}.est{background:#e3eef7;color:#27425a;border-color:#b6cde1}
.pending{background:#ffe3d6;color:#8a2c0d;border-color:#ffb899}.builder{background:#efe4fb;color:#4c1d95;border-color:#cdb4f0}
.disc{background:#fff6ec;border:2px dashed #ffc9a3;box-shadow:none}.disc::before{display:none}
/* tables */
.tw{overflow-x:auto;border-radius:18px;border:2px solid #cdeff3;margin:6px 0 12px;-webkit-overflow-scrolling:touch}
table{border-collapse:collapse;width:100%;min-width:520px}
th{background:#0a7ea4;color:#fff;font-weight:800;font-size:14px;padding:11px 12px;text-align:left}th .tag{margin-left:4px}
td{padding:10px 12px;font-size:15px;border-top:1px solid #e3f4f6}tr:nth-child(even) td{background:#f0fbfc}tr:hover td{background:#fff8e1}
th a{color:#fff}
/* forms */
input,select{font:inherit;padding:11px 14px;border:2px solid #bfe8ee;border-radius:14px;margin:4px 6px 10px 0;background:#fff;color:#16324a}input:focus,select:focus{border-color:#16b6c8;outline:none;box-shadow:0 0 0 4px rgba(22,182,200,.2)}
button{font:inherit;font-weight:900;background:#08708f;color:#fff;border:0;padding:11px 22px;border-radius:999px;cursor:pointer;box-shadow:0 3px 0 #05506a}button:hover{background:#0a86a8}button:disabled{background:#b9c9d2;box-shadow:none;cursor:not-allowed;color:#32485a}
#res ul{background:#f0fbfc;border-radius:16px;padding:14px 14px 14px 34px}
.chips{display:flex;flex-wrap:wrap;gap:10px}.chips a{padding:10px 18px;border-radius:999px;background:#e6f7f9;color:#0b4f66;text-decoration:none;font-weight:800;border:2px solid #bfe8ee}.chips a:hover{background:#fff4cc;border-color:#ffd23f}
.wave-div{height:24px;margin:6px auto;max-width:360px;opacity:.85}.wave-div svg{width:100%;height:100%;display:block}
ul li{margin:4px 0}
/* footer */
footer{position:relative;margin-top:30px;background:linear-gradient(180deg,#0a86a8,#075f7c);color:#e8fbff;text-align:center;font-size:13.5px;padding:44px 18px 28px}
footer::before{content:"";position:absolute;left:0;right:0;top:-1px;height:24px;background:CAUSTICFOOT}
footer .fbrand{display:flex;justify-content:center;align-items:center;gap:8px;font-weight:900;font-size:16px;color:#fff;margin-bottom:8px}footer a{color:#fff}
footer .tag{margin:2px 0}
@media (max-width:700px){body{font-size:16px}.hwrap{padding:10px 14px}nav.pills{flex-wrap:nowrap;overflow-x:auto;width:100%;padding-bottom:4px;scrollbar-width:none}nav.pills::-webkit-scrollbar{display:none}
.hero .in{padding:30px 16px 60px}.deco-palm{display:none}.deco-sun{width:64px;right:12px;top:10px;opacity:.7}.hero h1{padding-right:40px}.hero p.lead{font-size:17px}
.card{border-radius:20px;padding:20px 16px 18px}.big{font-size:30px}main{padding:4px 14px 24px}input,select{width:100%}}"""
FOOTWAVE="url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1440 24' preserveAspectRatio='none'%3E%3Cpath d='M0 0h1440v8c-120 14-240 14-360 4S840-2 720 8 480 22 360 14 120 0 0 10z' fill='%23fdf6ea'/%3E%3C/svg%3E\") 0 0/100% 100% no-repeat"
CSS=CSS.replace("CAUSTICFOOT",FOOTWAVE).replace("CAUSTIC",CAUSTIC)

CSS+=""".upl{text-align:center;background:linear-gradient(180deg,#e9fbfd,#fff 70%);border:3px dashed #7fd8e4;box-shadow:0 12px 34px rgba(10,134,168,.14)}
.upl-in{max-width:640px;margin:auto;padding:8px 0}
.upl-ico{width:78px;height:78px;margin:6px auto 10px;border-radius:24px;display:grid;place-items:center;font-size:40px;background:#fff4cc;box-shadow:0 4px 0 #ffd23f}
.card.upl h2{background:none;padding-bottom:0;font-size:clamp(24px,3.6vw,32px)}
.upl-lead{font-size:18px;font-weight:600;color:#0f3d52;margin:0 0 18px}
.upl-btn{font-size:19px;padding:15px 30px}.upl-sub{margin:10px 0 14px}
.upl-types{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin:0 0 16px}.upl-types span{background:#e6f7f9;color:#0b4f66;border:2px solid #bfe8ee;border-radius:999px;padding:4px 14px;font-weight:800;font-size:14px}
.upl-priv{background:#ddf6e7;border:1.5px solid #9fdcb8;color:#14532d;border-radius:16px;padding:12px 16px;margin:0;font-size:15px}
.grid2{grid-template-columns:repeat(auto-fit,minmax(min(320px,100%),1fr))}ul.ticks{list-style:none;padding:0;margin:0}ul.ticks li{position:relative;padding-left:30px;margin:8px 0}ul.ticks li::before{content:"✓";position:absolute;left:0;top:1px;width:22px;height:22px;border-radius:50%;background:#16b6c8;color:#fff;font-weight:900;font-size:13px;display:grid;place-items:center}
@media (max-width:700px){.upl-btn{width:100%;justify-content:center}.upl-lead{font-size:16.5px}}"""
NAV=[("index.html","Home"),("counties.html","Counties"),("the-villages.html","The Villages"),("pool-types.html","Pool types"),("enclosure-styles.html","Enclosure styles"),("submit.html","Share a quote"),("methodology.html","Methodology")]
DISC="Not legal, financial, or contracting advice. Figures are labeled by source; confirm pricing with licensed contractors."
HEAD_LINKS='''<link rel="icon" href="favicon.ico" sizes="32x32"><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="apple-touch-icon.png"><meta name="theme-color" content="#0a86a8">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&amp;display=swap" rel="stylesheet">'''
def hero_html(inner,small=False):
    return f'<section class="hero{" small" if small else ""}">{SUN}{"" if small else PALM}<div class="in">{inner}</div><div class="wave">{WAVE}</div></section>'
def page(fn,title,body,extra="",hero=None):
    cur="counties.html" if fn.startswith("county-") else fn
    nav="".join(f'<a href="{h}"'+(' class="cta"' if h=="submit.html" and cur!=h else '')+(' class="on" aria-current="page"' if h==cur else '')+f'>{t}</a>' for h,t in NAV)
    if hero is None:
        m=re.match(r'\s*(<h1>.*?</h1>)',body,re.S)
        if m: hero=hero_html(m.group(1),small=True); body=body[m.end():]
        else: hero=""
    body=body.replace("<table>",'<div class="tw"><table>').replace("</table>","</table></div>")
    open(os.path.join(OUT,fn),'w').write(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)} | Florida Pool Cost Index</title>{HEAD_LINKS}<link rel="stylesheet" href="style.css"></head><body>
<a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="hwrap"><a class="brand" href="index.html" aria-label="Florida Pool Cost Index, home">{mark()}<span class="wm"><b>Florida Pool</b><span>Cost Index</span></span></a><nav class="pills" aria-label="Main">{nav}</nav></div></header>{hero}<main id="main">{body}</main>
<footer><div class="fbrand">{mark(28,"fmark")}Florida Pool Cost Index</div>{E(DISC)}<br>Not a quote or bid. Data labeled by source: <span class="tag official">Official permit data</span> <span class="tag third">Third-party aggregate</span> <span class="tag est">Published estimate</span> <span class="tag pending">Pending</span> · Updated {D['updated']}</footer>{extra}</body></html>""")
open(os.path.join(OUT,'style.css'),'w').write(CSS)
write_brand_assets()
LP=D['lake_permits']; P26=LP['periods']['2026 (Jan 1 - Sep 30)']; P25=LP['periods']['2025 (full year)']
def est_table(keys):
    rows=""
    for e in D['estimators']:
        for k,v in e['items'].items():
            if k in keys: rows+=f"<tr><td>{E(k.replace('_',' '))}</td><td>{money(v[0])} – {money(v[1])}</td><td><a href='{e['url']}' target='_blank'>{E(e['name'])}</a></td></tr>"
    return f"<table><tr><th>Item</th><th>Published range</th><th>Source <span class='tag est'>Published estimate</span></th></tr>{rows}</table>"
def lake_block():
    r=""
    for per,v in LP['periods'].items():
        en=v['enclosure'];po=v['pool']
        r+=f"<tr><td>{per}</td><td>Screen enclosure (residential)</td><td>{en['count']}</td><td>{money(en['median'])}</td><td>{money(en['p25'])} – {money(en['p75'])}</td></tr>"
        r+=f"<tr><td>{per}</td><td>Inground pool (residential)</td><td>{po['count']}</td><td colspan=2>Not usable as a price: {po['share_under_5000']} permits declared under $5,000</td></tr>"
    return f"""<div class="card"><h3>Declared permit job values <span class="tag official">Official permit data</span></h3>
<table><tr><th>Period</th><th>Permit type</th><th>Permits</th><th>Median declared value</th><th>Middle half (25th–75th pct)</th></tr>{r}</table>
<p class="muted">Source: <a href="{LP['url']}" target="_blank">{E(LP['source'])}</a>, pulled {LP['pulled']}. Coverage: {E(LP['coverage'])} Values are what was declared on the permit, not contract prices. Only county-level aggregates are shown; no addresses or personal names are stored or published.</p></div>"""
OP=D.get('orlando_permits')
def orl_block():
    en=OP['enclosure'];po=OP['pool']
    r=f"<tr><td>Screen enclosure</td><td>{en['count']}</td><td>{money(en['median'])}</td><td>{money(en['p25'])} – {money(en['p75'])}</td><td>{money(en['min'])} – {money(en['max'])}</td></tr>"
    r+=f"<tr><td>Inground pool (residential)</td><td>{po['count']}</td><td>{money(po['median'])}</td><td>{money(po['p25'])} – {money(po['p75'])}</td><td>{po['share_under_5000']} declared under $5,000</td></tr>"
    return f"""<div class="card"><h3>City of Orlando declared permit values, {E(OP['period'])} <span class="tag official">Official permit data</span></h3>
<table><tr><th>Permit type</th><th>Permits</th><th>Median declared value</th><th>Middle half (25th–75th pct)</th><th>Range / notes</th></tr>{r}</table>
<p class="muted">Source: <a href="{OP['url']}" target="_blank">{E(OP['source'])}</a>, pulled {OP['pulled']}. Coverage: {E(OP['coverage'])} {E(OP['method'])} Values are what was declared on the permit, not contract prices, and may or may not include permit fees.</p></div>"""
def tp_block(slug):
    rows=[t for t in D['third_party_permit_aggregates'] if t['county']==slug]
    if not rows: return ""
    r="".join(f"<tr><td>{t['period']}</td><td>{t['permits']}</td><td>{money(t['total'])}</td><td>{money(t['total']/t['permits'])}</td><td><a href='{t['url']}' target='_blank'>HBWeekly</a></td></tr>" for t in rows)
    return f"""<div class="card"><h3>New pool permits, monthly <span class="tag third">Third-party aggregate</span></h3><table><tr><th>Month</th><th>Permits</th><th>Total declared value</th><th>Average (computed)</th><th>Source</th></tr>{r}</table>
<p class="muted">Reported by HBWeekly from permit data; the average is total ÷ permits, computed here. Declared values may not equal contract prices.</p></div>"""
quotes_block='<div class="card"><h3>Submitted quotes <span class="tag pending">Pending</span></h3><p>No homeowner quotes yet. <a href="submit.html">Share yours</a> to unlock detailed breakdowns.</p></div>'
BC=D['builder_contributed']; BS=BC['summary']
def bcalc(slug=None): return BS[slug or 'all']['stats']
BLAB=[("pool_base","Pool base line item (shell, standard equipment, permits, taxes)"),("total_all","Total project, new gunite pools"),
 ("total_nospa","Total project, pool only (no spa)"),("total_spa","Total project, pool + spa"),("spa","Spa add-on line item"),
 ("encl_dome","Screen enclosure line item: dome roof"),("encl_mansard","Screen enclosure line item: mansard roof"),
 ("encl_other","Screen enclosure + solid roof section (combined)")]
def fmtstat(s):
    if not s: return "<td>0</td><td>—</td><td>—</td>"
    med=money(s['median']) if s['median'] is not None else "<span class='muted'>n&lt;3: no median</span>"
    rng=f"{money(s['min'])} – {money(s['max'])}" if s['n']>1 else money(s['min'])
    return f"<td>{s['n']}</td><td>{med}</td><td>{rng}</td>"
def bd_block(slug=None,title_extra=""):
    st=bcalc(slug)
    rows="".join(f"<tr><td>{E(l)}</td>{fmtstat(st[k])}</tr>" for k,l in BLAB if st[k])
    stat_counts=BS[slug or 'all']['status_counts']
    sc=", ".join(f"{v} {k}" for k,v in sorted(stat_counts.items()))
    if not rows:
        body="<p>No builder-contributed quotes for this area yet.</p>"
    else:
        body=f"<table><tr><th>Line item</th><th>Quotes</th><th>Median</th><th>Range</th></tr>{rows}</table><p><b>Permits included:</b> {E(BC['permits_note'])} Compare against quotes that also include permits.</p><p class='muted'>Statuses: {E(sc)}. {E(BC['caveat'])} A renovation quote (no new pool) is excluded from pool totals but its enclosure figure is used. Figures with fewer than 3 quotes show the raw range only.</p>"
    return f'<div class="card"><h3>Builder-contributed quotes (anonymized){title_extra} <span class="tag builder">Builder-contributed</span></h3>{body}</div>'

# HOME
check="""<div class="card" id="check"><h2><span aria-hidden="true">🔍 </span>Is my quote fair?</h2><p>Compare your quote with published Florida ranges, builder-contributed quotes (anonymized), and official Lake County enclosure permit values.</p>
<select id="kind"><option value="gunite">Gunite (concrete) pool</option><option value="fiberglass">Fiberglass pool</option><option value="pool_spa">Pool + spa</option><option value="enclosure">Screen enclosure only</option></select>
<select id="county"><option value="">County (optional)</option>COUNTYOPTS</select>
<input id="price" type="number" placeholder="Quote total $"><button onclick="chk()">Check</button><div id="res"></div>
<p class="muted">Published ranges are estimates, not bids. Builder-contributed figures are one builder's quotes (small sample, mixed statuses); medians are shown only with 3+ quotes. Builder-contributed pool and screen enclosure prices include permitting costs; compare quotes that include permits. Once enough homeowner quotes are shared, this uses submitted quotes by county.</p></div>
<script>const EST=ESTJSON;const LAKE=LAKEJSON;const BCQ=BCJSON;
function f(n){return '$'+Math.round(n).toLocaleString()}
function chk(){const k=document.getElementById('kind').value,p=+document.getElementById('price').value,c=document.getElementById('county').value;let out='';
if(!p){document.getElementById('res').innerHTML='<p>Enter your quote amount.</p>';return}
EST.forEach(e=>{const r=e.items[k]||(k!=='enclosure'&&k!=='pool_spa'?e.items.inground_any:null);if(r){const pos=p<r[0]?'below':p>r[1]?'above':'within';out+=`<li><b>${pos}</b> ${f(r[0])}–${f(r[1])} (<a href="${e.url}" target="_blank">${e.name}</a>)</li>`}});
if(k==='enclosure'&&c==='orange'){const O=ORLJSON;const pos=p<O.p25?'below the middle half':p>O.p75?'above the middle half':'within the middle half';out+=`<li><b>${pos}</b> of City of Orlando declared enclosure permit values ${f(O.p25)}–${f(O.p75)}, median ${f(O.median)} (official, ${O.count} permits, Jan–Sep 2026)</li>`}
if(k==='enclosure'&&c==='lake'){const pos=p<LAKE.p25?'below the middle half':p>LAKE.p75?'above the middle half':'within the middle half';out+=`<li><b>${pos}</b> of Lake County declared enclosure permit values ${f(LAKE.p25)}–${f(LAKE.p75)}, median ${f(LAKE.median)} (official, Jan–Sep 2026)</li>`}
const bk={gunite:'total_nospa',fiberglass:null,pool_spa:'total_spa',enclosure:'encl_dome'}[k];
function bline(s,where,lab){if(!s)return '';const pos=p<s.min?'below':p>s.max?'above':'within';const med=s.median!==null?`, median ${f(s.median)}`:' (fewer than 3 quotes: range only)';return `<li><b>${pos}</b> the range of ${s.n} builder-contributed ${lab} quote${s.n>1?'s':''} ${where}: ${f(s.min)}–${f(s.max)}${med}</li>`}
if(bk){const lab={total_nospa:'pool-only total',total_spa:'pool + spa total',encl_dome:'dome screen enclosure'}[bk];if(c&&BCQ[c])out+=bline(BCQ[c][bk],'in this county',lab);out+=bline(BCQ.all[bk],'across all counties',lab);
if(k==='enclosure'&&BCQ.all.encl_mansard){const s=BCQ.all.encl_mansard;out+=`<li>Mansard screen enclosure: ${s.n} builder-contributed quote${s.n>1?'s':''}, ${f(s.min)}${s.n>1?'–'+f(s.max):''} (range only)</li>`}}
if(k==='fiberglass')out+='<li class="muted">No builder-contributed fiberglass quotes yet (all contributed pools are gunite).</li>';
if(bk)out+='<li class="muted"><b>Note:</b> builder-contributed pool and screen enclosure prices include permitting costs. Make sure the quote you are checking also includes permits (or add them) before comparing.</li>';
document.getElementById('res').innerHTML=out?'<ul>'+out+'</ul>':'<p>No published range for this combination yet.</p>'}</script>"""
copts="".join(f'<option value="{c["slug"]}">{E(c["name"])}</option>' for c in D['counties'])
check=check.replace("COUNTYOPTS",copts).replace("ESTJSON",json.dumps([{"name":e["name"],"url":e["url"],"items":e["items"]} for e in D['estimators']])).replace("LAKEJSON",json.dumps(P26['enclosure'])).replace("ORLJSON",json.dumps(OP['enclosure'])).replace("BCJSON",json.dumps(dict([("all",bcalc(None))]+[(c['slug'],bcalc(c['slug'])) for c in D['counties']])))
BH=bcalc(None)
HERO=hero_html('<h1>What Florida Pools and Screen Enclosures Really Cost</h1><p class="lead">Real quotes shared by Florida homeowners, official permit data, and published estimates, each clearly labeled. Starting in Central Florida.</p><div class="btns"><a class="btn" href="#check"><span aria-hidden="true">🏊</span> Check my quote</a><a class="btn2" href="submit.html"><span aria-hidden="true">✍️</span> Share a quote</a></div>')
def ico(e): return f'<span class="ico" aria-hidden="true">{e}</span>'
home=f"""<div class="grid"><div class="card stat">{ico("🏡")}<div class="muted">Lake County screen enclosures, median declared permit value (Jan–Sep 2026)</div><div class="big">{money(P26['enclosure']['median'])}</div><span class="tag official">Official permit data</span> <span class="muted">{P26['enclosure']['count']} permits</span></div>
<div class="card stat">{ico("🌊")}<div class="muted">Florida fiberglass pool, published range</div><div class="big">$45k–$110k</div><span class="tag est">Published estimate</span> <span class="muted">EstimateFlorida</span></div>
<div class="card stat">{ico("💧")}<div class="muted">Florida gunite pool, published range</div><div class="big">$55k–$150k</div><span class="tag est">Published estimate</span> <span class="muted">EstimateFlorida</span></div>
<div class="card stat">{ico("🏊")}<div class="muted">New gunite pool total project, builder-contributed quotes (Apr–Oct 2026)</div><div class="big">{money(BH['total_all']['median'])} median</div><span class="tag builder">Builder-contributed</span> <span class="muted">{BH['total_all']['n']} quotes, {money(BH['total_all']['min'])}–{money(BH['total_all']['max'])}; one builder, mixed statuses; permits included</span></div>
<div class="card stat">{ico("⛱️")}<div class="muted">Dome screen enclosure line item, builder-contributed quotes</div><div class="big">{money(BH['encl_dome']['median'])} median</div><span class="tag builder">Builder-contributed</span> <span class="muted">{BH['encl_dome']['n']} quotes, {money(BH['encl_dome']['min'])}–{money(BH['encl_dome']['max'])}; permits included</span></div>
<div class="card stat">{ico("✍️")}<div class="muted">Homeowner-submitted quotes</div><div class="big">0</div><span class="tag pending">Pending</span> <a href="submit.html">Share yours</a></div></div>
{DIVIDER}{check}{DIVIDER}<div class="card"><h2><span aria-hidden="true">🌴 </span>Counties</h2><div class="chips">{''.join(f'<a href="county-{c["slug"]}.html">{E(c["name"])}</a>' for c in D['counties'])}<a href="the-villages.html">The Villages</a></div></div>
<div class="card"><h3><span aria-hidden="true">☀️ </span>Newsletter</h3><p>Monthly Florida Pool &amp; Enclosure Cost Index. <i>(Placeholder: signup not connected yet.)</i></p><input type="email" placeholder="you@example.com" disabled><button disabled>Subscribe</button></div>
<div class="card disc">{E(DISC)} <a href="methodology.html">Read the methodology</a>.</div>"""
page("index.html","Home",home,hero=HERO)
# COUNTIES
def county_stats(s):
    cards=[]
    if s=='lake': cards.append(("🏡","Screen enclosures, median declared permit value (Jan–Sep 2026)",money(P26['enclosure']['median']),'<span class="tag official">Official permit data</span>',f"{P26['enclosure']['count']} permits"))
    if s=='orange': cards.append(("🏡",f"City of Orlando screen enclosures, median declared permit value, {E(OP['period'])}",money(OP['enclosure']['median']),'<span class="tag official">Official permit data</span>',f"{OP['enclosure']['count']} permits"))
    st=bcalc(s)
    for k,emo,lab in [("total_all","🏊","New gunite pool total project, builder-contributed median"),("pool_base","💧","Pool base line item, builder-contributed median"),("encl_dome","⛱️","Dome screen enclosure line item, builder-contributed median")]:
        v=st.get(k)
        if v and v['median'] is not None: cards.append((emo,lab,money(v['median']),'<span class="tag builder">Builder-contributed</span>',f"{v['n']} quotes, {money(v['min'])}–{money(v['max'])}; permits included"))
    if not cards: return ""
    return '<div class="grid stat-row">'+"".join(f'<div class="card stat">{ico(e)}<div class="muted">{l}</div><div class="big">{v}</div>{t} <span class="muted">{n}</span></div>' for e,l,v,t,n in cards)+'</div>'
page("counties.html","Counties","<h1>Counties</h1>"+"".join(f'<div class="card"><a href="county-{c["slug"]}.html"><b>{E(c["name"])}</b></a><br><span class="muted">Permit data: {E(c["status"])}</span></div>' for c in D['counties']))
for c in D['counties']:
    s=c['slug']; body=f"<h1>{E(c['name'])} pool &amp; screen enclosure costs</h1>"
    body+=county_stats(s)
    if s=='lake': body+=lake_block()+'<p>Includes the Lake County side of <a href="the-villages.html">The Villages</a> only where permits were issued by the county.</p>'
    if s=='orange': body+=orl_block()
    if s!='lake': body+=f'<div class="card"><h3>Official permit data{" (unincorporated Orange County)" if s=="orange" else ""} <span class="tag pending">Pending</span></h3><p>{E(c["status"])}.</p>'+(f'<p class="muted">Portal: <a href="{c["portal"]}" target="_blank">{c["portal"]}</a></p>' if c['portal'] else '')+'</div>'
    body+=bd_block(s)+bd_block(None,' – all counties')+tp_block(s)+quotes_block
    body+=f'<div class="card"><h3>Statewide published ranges</h3>{est_table(["fiberglass","gunite","pool_spa","enclosure","inground_any","enclosure_16x32","permits_engineering"])}</div>'
    body+='<div class="card"><h3>Get 3 quotes</h3><p><i>Placeholder: not live. Listed builders will be shown here; paid placements will be clearly marked.</i></p></div>'
    page(f"county-{s}.html",c['name'],body)
# VILLAGES
arc="https://www.districtgov.org/wp-content/uploads/2025/04/VCCDD-LL-LC-ARC-Manual-revised-2024.pdf"
vil=f"""<h1>The Villages: pool &amp; screen enclosure costs and rules</h1>
<div class="card"><h3>Rules for screen enclosures (Lady Lake / Lake County portion)</h3><ul>
<li>Architectural Review Committee approval is required before work starts; a separate city/county building permit is still needed.</li>
<li>Approved roof styles: mansard, dome, hip, gable-hip, gambrel.</li><li>Frame and screen: black, bronze, or white.</li>
<li>Must be in the rear or side quadrant, not in easements, and no taller than the existing roof peak.</li><li>Pool equipment concealed from the street and kept two feet from property lines.</li></ul>
<p class="muted">Source: <a href="{arc}" target="_blank">Architectural Review Manual, Lady Lake/Lake County portion</a>; <a href="https://www.districtgov.org/how-to/faqs/" target="_blank">District FAQs</a>. Sumter and Marion portions have their own manuals (not yet summarized).</p></div>
{tp_block('sumter').replace('New pool permits, monthly','Sumter County new pool permits (most of The Villages), monthly')}
<div class="card"><p>Lake County enclosure permit values: see <a href="county-lake.html">Lake County</a> (unincorporated + Montverde only; Lady Lake issues its own permits).</p></div>{quotes_block}<div class="card"><h3>Builder-contributed quotes (anonymized)</h3><p>None of the builder-contributed quotes are in The Villages.</p></div>"""
page("the-villages.html","The Villages",vil)
# POOL TYPES
pt="<h1>Pool types</h1>"
pt+=f'<div class="card"><h2>Gunite (concrete / shotcrete)</h2>{est_table(["gunite"])}</div>'
pt+=f'<div class="card"><h2>Fiberglass</h2>{est_table(["fiberglass"])}</div>'
pt+='<div class="card"><h2>Vinyl liner</h2><p><span class="tag pending">Pending</span> No Florida-specific published range collected yet.</p></div>'
pt+=f'<div class="card"><h2>Pool + spa</h2>{est_table(["pool_spa"])}</div>'+quotes_block
page("pool-types.html","Pool types",pt)
# ENCLOSURE STYLES
es=f"""<h1>Screen enclosure styles &amp; screen types</h1><div class="card"><h3>What enclosures cost (published)</h3>{est_table(["enclosure","enclosure_16x32"])}
<ul class="muted"><li>ExpertBuildCalc: $8–$22 per sq ft of footprint.</li><li>BuildMat Insight: standard screen (110 mph) $18–$24/sq ft; HVHZ coastal $28–$38/sq ft.</li><li>AutomatedEstimating: wind-borne debris/HVHZ zones can add 15–30% to the aluminum portion.</li></ul></div>
{lake_block()}
<div class="card"><h3>Styles</h3><table><tr><th>Style</th><th>Price data</th><th>Notes</th></tr>
<tr><td>Mansard</td><td>MANSARDCELL</td><td>Approved in The Villages (Lady Lake/Lake County portion)</td></tr>
<tr><td>Dome</td><td>DOMECELL</td><td>Approved in The Villages</td></tr>
<tr><td>Gable / gable-hip</td><td><span class="tag pending">Pending</span></td><td>Gable-hip approved in The Villages</td></tr>
<tr><td>Hip</td><td><span class="tag pending">Pending</span></td><td>Approved in The Villages</td></tr>
<tr><td>Flat / under-truss</td><td><span class="tag pending">Pending</span></td><td>Not on The Villages approved list</td></tr></table>
<p class="muted">Style-level prices will come from submitted quotes.</p></div>
<div class="card"><h3>Screen types</h3><p>Standard, no-see-um (finer mesh), privacy and pet screens. <span class="tag pending">Pending</span> price differences, to be filled in from submitted quotes.</p></div>"""
_ba=bcalc(None)
_sw=D['statewide_third_party'][0]
es=es.replace("<div class=\"card\"><h3>Styles</h3>",f"<div class='card'><h3>Statewide screen enclosure permit values <span class='tag third'>Third-party aggregate</span></h3><p>{_sw['with_value']:,} Florida permits with a declared value (through {_sw['through']}): median {money(_sw['median'])}, middle half {E(_sw['middle_half'])}.</p><p class='muted'>Source: <a href='{_sw['url']}' target='_blank'>{E(_sw['name'])}</a>. {E(_sw['note'])}</p></div>"+orl_block()+"<div class=\"card\"><h3>Styles</h3>",1)
def _cell(s): return ("<span class='tag builder'>Builder-contributed</span> "+(f"{s['n']} quotes, median {money(s['median'])}, {money(s['min'])}–{money(s['max'])}" if s['median'] is not None else f"{s['n']} quote{'s' if s['n']>1 else ''}, {money(s['min'])}"+(f"–{money(s['max'])}" if s['n']>1 else "")+" (range only)")) if s else "<span class='tag pending'>Pending</span>"
es=es.replace("MANSARDCELL",_cell(_ba['encl_mansard'])).replace("DOMECELL",_cell(_ba['encl_dome'])).replace("<p class=\"muted\">Style-level prices will come from submitted quotes.</p>","<p class=\"muted\">Builder-contributed figures are screen enclosure line items from one builder's quotes (small sample, mixed statuses); no document states a screen type. More style-level prices will come from submitted quotes.</p>")
page("enclosure-styles.html","Enclosure styles",es)
# SUBMIT
UPLOAD_URL="https://www.dropbox.com/request/c7250kquamtlmkfmr8h9"  # Dropbox file request -> /Florida Pool Cost Index/Quote Uploads (private to the owner)
sub=f"""<h1>Share a quote</h1>
<section class="card upl" aria-labelledby="upl-h"><div class="upl-in">
<div class="upl-ico" aria-hidden="true">📄</div>
<h2 id="upl-h">Upload your quote files</h2>
<p class="upl-lead">Got a pool or screen enclosure quote? Snap a photo or grab the PDF and drop it in. It takes about a minute, and you don't need an account.</p>
<a class="btn upl-btn" href="{UPLOAD_URL}" target="_blank" rel="noopener"><span aria-hidden="true">⬆️</span> Upload your quote files</a>
<p class="muted upl-sub">Opens a secure Dropbox upload page in a new tab.</p>
<div class="upl-types" aria-label="Accepted file types"><span>PDF</span><span>JPG</span><span>PNG</span><span>HEIC (iPhone photos)</span></div>
<p class="upl-priv"><span aria-hidden="true">🔒</span> <b>Your files go privately to the site owner.</b> They're never published. We only add anonymized totals to the county averages.</p>
</div></section>
<div class="grid grid2">
<div class="card"><h3>What to upload</h3><ul class="ticks">
<li>The full quote or proposal (a PDF, or clear photos of every page)</li>
<li>Pool quotes, screen enclosure quotes, or both</li>
<li>Quotes you signed, are still thinking about, or turned down</li>
<li>Feel free to <b>black out names, addresses and phone numbers</b> first</li></ul></div>
<div class="card"><h3>Helpful details</h3><p>If these aren't already on the quote, you can put them in the file name, or upload a photo of a quick handwritten or typed note:</p><ul class="ticks">
<li>County and community</li><li>Month of the quote</li><li><b>Permits included? (yes / no / unsure)</b></li><li>Status: quoted, signed or completed</li></ul></div>
</div>
<div class="card"><h3>What happens next</h3><p>We review each quote by hand and take out any personal info. It counts toward county figures once there are enough quotes to share without identifying anyone. Your shared quotes unlock detailed breakdowns by county, pool type, enclosure style and screen type. Builder names stay private.</p></div>"""
page("submit.html","Share a quote",sub)
# METHODOLOGY
src="".join(f"<li><a href='{e['url']}' target='_blank'>{E(e['name'])}</a>{(' – '+E(e['note'])) if e.get('note') else ''}</li>" for e in D['estimators'])
cst="".join(f"<tr><td>{E(c['name'])}</td><td>{E(c['status'])}</td></tr>" for c in D['counties'])
meth=f"""<h1>Methodology</h1><div class="card disc"><h3>Not advice</h3><p>{E(DISC)}</p></div>
<div class="card"><h3>Data labels</h3><ul><li><span class="tag official">Official permit data</span> County-published permit reports. Declared job values, which may be below contract prices. County-level aggregates only.</li>
<li><span class="tag third">Third-party aggregate</span> Permit totals reported by others (e.g., HBWeekly).</li><li><span class="tag est">Published estimate</span> Ranges from online estimators; not real quotes.</li>
<li><span class="tag builder">Builder-contributed</span> Anonymized quotes contributed by a Florida builder: line items exactly as written in each proposal, county-level only, labeled and filterable. Currently one builder's quotes (small sample, statuses mixed: quoted, signed, lost). Their pool and screen enclosure prices include permitting costs, so compare them with quotes that also include permits. Medians shown only with 3+ quotes; otherwise the raw range. A renovation quote (no new pool) is excluded from pool totals but its enclosure figure is used. Enclosure figures that bundle a solid roof section are shown separately.</li><li><span class="tag pending">Pending</span> Not yet collected.</li></ul></div>
<div class="card"><h3>Important caveat on pool permit values</h3><p>In Lake County, most residential inground pool permits declare nominal job values (2026 Jan–Sep: {P26['pool']['share_under_5000']} under $5,000), so they're not used as pool prices. Screen enclosure permit values look like real prices and are shown.</p></div>
<div class="card"><h3>Permit data status by county</h3><table>{cst}</table></div><div class="card"><h3>Published estimate sources</h3><ul>{src}</ul></div>
<div class="card"><h3>Verification of submitted quotes</h3><p>Unverified → document-verified (reviewed by hand, personal info removed) → permit-matched. Spam checks, plausibility flags, no self-submitted builder quotes, dispute process.</p></div>"""
page("methodology.html","Methodology",meth)
print("built",len(os.listdir(OUT)),"files")
