import json,os,html
D=json.load(open('data.json')); OUT='site'; os.makedirs(OUT,exist_ok=True)
E=html.escape
def money(v): return "${:,.0f}".format(v)
CSS="""*{box-sizing:border-box}body{margin:0;font-family:system-ui,sans-serif;color:#13222f;background:#f4f8fb}
header{background:#0a5a7d;color:#fff;padding:14px 20px}header a{color:#fff;text-decoration:none;margin-right:14px;font-size:14px}
header .brand{font-size:21px;font-weight:700;display:block;margin-bottom:6px}main{max-width:1050px;margin:auto;padding:16px}
.card{background:#fff;border:1px solid #d7e2ea;border-radius:8px;padding:16px;margin:14px 0}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px}
.tag{display:inline-block;font-size:11px;font-weight:700;padding:2px 8px;border-radius:10px;color:#fff;vertical-align:middle}
.official{background:#1e8449}.third{background:#7d6608}.est{background:#5d6d7e}.pending{background:#a04000}.builder{background:#6c3483}
table{border-collapse:collapse;width:100%}td,th{border-bottom:1px solid #e3eaf0;padding:7px;text-align:left;font-size:14px}
.big{font-size:28px;font-weight:700}.muted{color:#5b6b78;font-size:13px}.disc{background:#fdf2e9;border-color:#f0b27a}
input,select{padding:8px;border:1px solid #c5d2dc;border-radius:6px;margin:4px 6px 8px 0}button{background:#0a5a7d;color:#fff;border:0;padding:9px 16px;border-radius:6px;cursor:pointer}
footer{text-align:center;color:#6b7b88;font-size:12px;padding:20px}"""
NAV=[("index.html","Home"),("counties.html","Counties"),("the-villages.html","The Villages"),("pool-types.html","Pool types"),("enclosure-styles.html","Enclosure styles"),("submit.html","Share a quote"),("methodology.html","Methodology")]
DISC="Not legal, financial, or contracting advice. Figures are labeled by source; confirm pricing with licensed contractors."
def page(fn,title,body,extra=""):
    nav="".join(f'<a href="{h}">{t}</a>' for h,t in NAV)
    open(os.path.join(OUT,fn),'w').write(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)} | Florida Pool Cost Index</title><link rel="stylesheet" href="style.css"></head><body>
<header><a class="brand" href="index.html">Florida Pool Cost Index</a>{nav}</header><main>{body}</main>
<footer>{E(DISC)}<br>Not a quote or bid. Data labeled by source: <span class="tag official">Official permit data</span> <span class="tag third">Third-party aggregate</span> <span class="tag est">Published estimate</span> <span class="tag pending">Pending</span> · Updated {D['updated']}</footer>{extra}</body></html>""")
open(os.path.join(OUT,'style.css'),'w').write(CSS)
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
check="""<div class="card"><h2>Is my quote fair?</h2><p>Compare your quote with published Florida ranges, builder-contributed quotes (anonymized), and official Lake County enclosure permit values.</p>
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
home=f"""<h1>What Florida Pools and Screen Enclosures Really Cost</h1><p>Real quotes shared by Florida homeowners, official permit data, and published estimates, each clearly labeled. Starting in Central Florida.</p>
<div class="grid"><div class="card"><div class="muted">Lake County screen enclosures, median declared permit value (Jan–Sep 2026)</div><div class="big">{money(P26['enclosure']['median'])}</div><span class="tag official">Official permit data</span> <span class="muted">{P26['enclosure']['count']} permits</span></div>
<div class="card"><div class="muted">Florida fiberglass pool, published range</div><div class="big">$45k–$110k</div><span class="tag est">Published estimate</span> <span class="muted">EstimateFlorida</span></div>
<div class="card"><div class="muted">Florida gunite pool, published range</div><div class="big">$55k–$150k</div><span class="tag est">Published estimate</span> <span class="muted">EstimateFlorida</span></div>
<div class="card"><div class="muted">New gunite pool total project, builder-contributed quotes (Apr–Oct 2026)</div><div class="big">{money(BH['total_all']['median'])} median</div><span class="tag builder">Builder-contributed</span> <span class="muted">{BH['total_all']['n']} quotes, {money(BH['total_all']['min'])}–{money(BH['total_all']['max'])}; one builder, mixed statuses; permits included</span></div>
<div class="card"><div class="muted">Dome screen enclosure line item, builder-contributed quotes</div><div class="big">{money(BH['encl_dome']['median'])} median</div><span class="tag builder">Builder-contributed</span> <span class="muted">{BH['encl_dome']['n']} quotes, {money(BH['encl_dome']['min'])}–{money(BH['encl_dome']['max'])}; permits included</span></div>
<div class="card"><div class="muted">Homeowner-submitted quotes</div><div class="big">0</div><span class="tag pending">Pending</span> <a href="submit.html">Share yours</a></div></div>
{check}<div class="card"><h2>Counties</h2><div class="grid">{''.join(f'<a href="county-{c["slug"]}.html">{E(c["name"])}</a>' for c in D['counties'])}<a href="the-villages.html">The Villages</a></div></div>
<div class="card"><h3>Newsletter</h3><p>Monthly Florida Pool &amp; Enclosure Cost Index. <i>(Placeholder: signup not connected yet.)</i></p><input type="email" placeholder="you@example.com" disabled><button disabled>Subscribe</button></div>
<div class="card disc">{E(DISC)} <a href="methodology.html">Read the methodology</a>.</div>"""
page("index.html","Home",home)
# COUNTIES
page("counties.html","Counties","<h1>Counties</h1>"+"".join(f'<div class="card"><a href="county-{c["slug"]}.html"><b>{E(c["name"])}</b></a><br><span class="muted">Permit data: {E(c["status"])}</span></div>' for c in D['counties']))
for c in D['counties']:
    s=c['slug']; body=f"<h1>{E(c['name'])} pool &amp; screen enclosure costs</h1>"
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
sub="""<h1>Share a quote</h1><div class="card"><p><b>Placeholder.</b> Intake will be a Google Form (not created yet). Sharing a quote unlocks detailed breakdowns by county, pool type, enclosure style and screen type.</p>
<p>What we'll ask: county &amp; community, quote month, pool type/size/features, deck, enclosure style/size/screen type, total and line-item prices, what's included, <b>permits included? (yes / no / unsure)</b>, status (quoted/signed/completed). Builder name optional. Optional quote document upload for "verified" status. Documents stay private and are deleted after review.</p>
<button disabled>Open the form (coming soon)</button></div>"""
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
