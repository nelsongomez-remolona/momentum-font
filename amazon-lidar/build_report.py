"""Assemble a self-contained HTML report from the pipeline outputs in output/.
Embeds the rendered PNGs as data URIs and the ranked candidates as a table.

    python build_report.py            # -> output/report.html
"""

from __future__ import annotations

import base64
import json
import os

OUT = "output"


def data_uri(path: str) -> str:
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:image/png;base64,{b64}"


def main():
    with open(os.path.join(OUT, "dem.json")) as f:
        meta = json.load(f)
    with open(os.path.join(OUT, "candidates.geojson")) as f:
        fc = json.load(f)

    b = meta["bbox"]
    mpp = meta["meters_per_px"]
    h, w = meta["shape"]
    cands = []
    for feat in fc["features"]:
        lon, lat = feat["geometry"]["coordinates"]
        p = feat["properties"]
        cands.append({"lat": lat, "lon": lon, **p})
    cands.sort(key=lambda c: c["score"], reverse=True)

    imgs = {name: data_uri(os.path.join(OUT, f"{name}.png"))
            for name in ("dem", "hillshade", "lrm", "candidates")}

    n_mound = sum(1 for c in cands if c["kind"] == "mound")
    n_ring = sum(1 for c in cands if c["kind"] == "ring")

    rows = "\n".join(
        f'<tr class="{c["kind"]}">'
        f'<td class="num">{i}</td>'
        f'<td><span class="kind kind--{c["kind"]}">{c["kind"]}</span></td>'
        f'<td class="num">{c["lat"]:.5f}</td>'
        f'<td class="num">{c["lon"]:.5f}</td>'
        f'<td class="num">{c["diameter_m"]:.0f}</td>'
        f'<td class="num">{c["amplitude_m"]:.1f}</td>'
        f'<td class="num">{c["regularity"]:.2f}</td>'
        f'<td class="num strong">{c["score"]:.1f}</td>'
        f'</tr>'
        for i, c in enumerate(cands, 1))

    area_km2 = (abs(b["east"] - b["west"]) * 111.32 *
                abs(b["north"] - b["south"]) * 111.32 *
                abs(__import__("math").cos(__import__("math").radians(
                    0.5 * (b["north"] + b["south"])))))

    html = TEMPLATE.format(
        img_dem=imgs["dem"], img_hs=imgs["hillshade"],
        img_lrm=imgs["lrm"], img_cand=imgs["candidates"],
        west=f'{b["west"]:.3f}', south=f'{b["south"]:.3f}',
        east=f'{b["east"]:.3f}', north=f'{b["north"]:.3f}',
        mpp=f"{mpp:.0f}", w=w, h=h, area=f"{area_km2:.0f}",
        n_total=len(cands), n_mound=n_mound, n_ring=n_ring, rows=rows)

    out_path = os.path.join(OUT, "report.html")
    with open(out_path, "w") as f:
        f.write(html)
    print(f"wrote {out_path} ({os.path.getsize(out_path)//1024} KB)")


TEMPLATE = r"""<title>Amazon LiDAR Survey — Acre Transect</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  :root {{
    --bg:#E6E7E1; --surface:#F2F3EE; --surface-2:#EAEBE4;
    --ink:#1B211C; --muted:#5C6159; --line:#D2D5CB;
    --earth:#B4532A; --water:#2E6E8E;
    --shadow:0 1px 2px rgba(20,30,20,.06), 0 8px 30px rgba(20,30,20,.07);
    --mono:ui-monospace,"SF Mono",SFMono-Regular,"Cascadia Mono",Menlo,Consolas,monospace;
    --sans:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{
      --bg:#0F1411; --surface:#161C17; --surface-2:#1B221C;
      --ink:#E7E9E1; --muted:#98A08E; --line:#28312A;
      --earth:#D9743F; --water:#5BA6C9;
      --shadow:0 1px 2px rgba(0,0,0,.4), 0 10px 34px rgba(0,0,0,.5);
    }}
  }}
  :root[data-theme="light"] {{
    --bg:#E6E7E1; --surface:#F2F3EE; --surface-2:#EAEBE4;
    --ink:#1B211C; --muted:#5C6159; --line:#D2D5CB;
    --earth:#B4532A; --water:#2E6E8E;
    --shadow:0 1px 2px rgba(20,30,20,.06), 0 8px 30px rgba(20,30,20,.07);
  }}
  :root[data-theme="dark"] {{
    --bg:#0F1411; --surface:#161C17; --surface-2:#1B221C;
    --ink:#E7E9E1; --muted:#98A08E; --line:#28312A;
    --earth:#D9743F; --water:#5BA6C9;
    --shadow:0 1px 2px rgba(0,0,0,.4), 0 10px 34px rgba(0,0,0,.5);
  }}

  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--ink);
    font-family:var(--sans); line-height:1.6;
    -webkit-font-smoothing:antialiased; }}
  .wrap {{ max-width:1080px; margin:0 auto; padding:clamp(20px,5vw,64px) clamp(16px,4vw,40px); }}

  .eyebrow {{ font-family:var(--mono); font-size:12px; letter-spacing:.22em;
    text-transform:uppercase; color:var(--muted); margin:0 0 14px; }}
  h1 {{ font-family:var(--sans); font-weight:800; letter-spacing:-.02em;
    text-wrap:balance; line-height:1.02; margin:0;
    font-size:clamp(34px,7vw,64px); }}
  h1 .fade {{ color:var(--muted); }}
  .lede {{ max-width:60ch; color:var(--muted); font-size:clamp(15px,2vw,18px);
    margin:18px 0 0; }}

  /* spec strip */
  .specs {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
    gap:1px; background:var(--line); border:1px solid var(--line);
    border-radius:12px; overflow:hidden; margin:32px 0 8px; box-shadow:var(--shadow); }}
  .spec {{ background:var(--surface); padding:16px 18px; }}
  .spec dt {{ font-family:var(--mono); font-size:11px; letter-spacing:.14em;
    text-transform:uppercase; color:var(--muted); margin:0 0 6px; }}
  .spec dd {{ margin:0; font-family:var(--mono); font-size:16px; font-weight:600;
    font-variant-numeric:tabular-nums; }}
  .spec dd small {{ color:var(--muted); font-weight:400; }}

  /* honesty callout */
  .flag {{ display:flex; gap:16px; align-items:flex-start; margin:36px 0;
    padding:20px 22px; border-radius:12px;
    background:var(--surface); border:1px solid var(--line);
    border-left:4px solid var(--earth); box-shadow:var(--shadow); }}
  .flag .mark {{ font-family:var(--mono); font-weight:700; color:var(--earth);
    font-size:13px; letter-spacing:.1em; white-space:nowrap; padding-top:2px; }}
  .flag p {{ margin:0; font-size:14.5px; color:var(--ink); }}
  .flag strong {{ color:var(--ink); }}

  h2 {{ font-size:13px; font-family:var(--mono); letter-spacing:.16em;
    text-transform:uppercase; color:var(--muted); font-weight:600;
    margin:52px 0 4px; padding-bottom:12px; border-bottom:1px solid var(--line);
    display:flex; justify-content:space-between; align-items:baseline; }}
  h2 .hint {{ letter-spacing:.02em; text-transform:none; }}

  /* processing chain */
  .chain {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(230px,1fr));
    gap:16px; margin:26px 0; }}
  figure {{ margin:0; background:var(--surface); border:1px solid var(--line);
    border-radius:12px; overflow:hidden; box-shadow:var(--shadow); }}
  figure img {{ display:block; width:100%; height:auto; background:#888; }}
  figcaption {{ padding:12px 14px 14px; }}
  .stage {{ font-family:var(--mono); font-size:11px; letter-spacing:.14em;
    text-transform:uppercase; color:var(--muted); }}
  .stage b {{ color:var(--earth); }}
  figcaption .title {{ font-weight:700; font-size:15px; margin:3px 0 4px; }}
  figcaption p {{ margin:0; font-size:13px; color:var(--muted); line-height:1.5; }}

  .feature {{ margin:26px 0; }}
  .feature img {{ width:100%; height:auto; display:block; border-radius:12px;
    border:1px solid var(--line); box-shadow:var(--shadow); background:#888; }}
  .legend {{ display:flex; gap:22px; flex-wrap:wrap; margin:14px 2px 0;
    font-family:var(--mono); font-size:12.5px; color:var(--muted); }}
  .legend span {{ display:inline-flex; align-items:center; gap:8px; }}
  .dot {{ width:11px; height:11px; border-radius:50%; border:2px solid; }}
  .dot--earth {{ border-color:var(--earth); }}
  .dot--water {{ border-color:var(--water); }}

  /* table */
  .scroll {{ overflow-x:auto; margin:24px 0; border:1px solid var(--line);
    border-radius:12px; box-shadow:var(--shadow); }}
  table {{ border-collapse:collapse; width:100%; min-width:640px;
    font-family:var(--mono); font-size:13.5px; }}
  thead th {{ text-align:right; padding:14px 16px; background:var(--surface-2);
    font-size:11px; letter-spacing:.1em; text-transform:uppercase;
    color:var(--muted); font-weight:600; border-bottom:1px solid var(--line);
    position:sticky; top:0; }}
  thead th:nth-child(2) {{ text-align:left; }}
  tbody td {{ padding:11px 16px; border-bottom:1px solid var(--line);
    background:var(--surface); }}
  tbody tr:last-child td {{ border-bottom:0; }}
  .num {{ text-align:right; font-variant-numeric:tabular-nums; }}
  td.strong {{ font-weight:700; }}
  .kind {{ display:inline-block; padding:2px 9px; border-radius:100px;
    font-size:11px; letter-spacing:.06em; text-transform:uppercase; font-weight:600; }}
  .kind--mound {{ color:var(--earth); background:color-mix(in srgb,var(--earth) 15%,transparent); }}
  .kind--ring {{ color:var(--water); background:color-mix(in srgb,var(--water) 15%,transparent); }}
  tbody tr.mound td:first-child {{ box-shadow:inset 3px 0 var(--earth); }}
  tbody tr.ring  td:first-child {{ box-shadow:inset 3px 0 var(--water); }}

  .prose p {{ max-width:66ch; color:var(--ink); }}
  .prose a {{ color:var(--earth); }}
  .steps {{ counter-reset:s; list-style:none; padding:0; max-width:66ch; }}
  .steps li {{ counter-increment:s; position:relative; padding:0 0 14px 40px; color:var(--ink); }}
  .steps li::before {{ content:counter(s,decimal-leading-zero); position:absolute; left:0; top:0;
    font-family:var(--mono); font-size:12px; color:var(--earth); font-weight:700;
    padding-top:3px; letter-spacing:.05em; }}

  footer {{ margin-top:56px; padding-top:20px; border-top:1px solid var(--line);
    font-family:var(--mono); font-size:12px; color:var(--muted);
    display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px; }}

  @media (prefers-reduced-motion:no-preference) {{
    .reveal {{ animation:rise .7s cubic-bezier(.2,.7,.2,1) both; }}
    @keyframes rise {{ from {{ opacity:0; transform:translateY(10px); }} }}
  }}
</style>

<div class="wrap">
  <header class="reveal">
    <p class="eyebrow">Remote-sensing survey · screening pass</p>
    <h1>Reading the ground<br><span class="fade">beneath the Amazon.</span></h1>
    <p class="lede">An automated pass over a transect of the Acre "geoglyph" belt
      in western Brazil — pulling open elevation data, stripping the natural
      landform away, and flagging the shapes that don't look natural.</p>
  </header>

  <dl class="specs reveal">
    <div class="spec"><dt>Region</dt><dd>Acre, BR</dd></div>
    <div class="spec"><dt>Extent</dt><dd>{west}, {south}<br><small>{east}, {north}</small></dd></div>
    <div class="spec"><dt>Datum</dt><dd>WGS84</dd></div>
    <div class="spec"><dt>Source</dt><dd>SRTM<small> / terrain-tiles</small></dd></div>
    <div class="spec"><dt>Resolution</dt><dd>~{mpp} m<small>/px</small></dd></div>
    <div class="spec"><dt>Grid</dt><dd>{w}×{h}<small> · ~{area} km²</small></dd></div>
  </dl>

  <div class="flag">
    <span class="mark">READ ME</span>
    <p>These are <strong>screening candidates, not discoveries.</strong> The
    input is ~30&nbsp;m <em>surface</em> elevation (canopy included) — not the
    sub-metre, canopy-removed LiDAR real finds are made from. At this resolution
    a 1–2&nbsp;m earthwork is invisible; only the largest enclosures leave a
    trace, and most hits below are natural river relief. The value here is the
    <strong>method</strong>, which runs unchanged on real bare-earth LiDAR.</p>
  </div>

  <h2>Processing chain <span class="hint">elevation → anomaly</span></h2>
  <div class="chain">
    <figure><img src="{img_dem}" alt="Raw elevation grid">
      <figcaption><span class="stage"><b>01</b> · Fetch</span>
        <div class="title">Elevation</div>
        <p>Stitched terrain tiles. Broad basin — river valleys dominate.</p></figcaption></figure>
    <figure><img src="{img_hs}" alt="Hillshade">
      <figcaption><span class="stage"><b>02</b> · Shade</span>
        <div class="title">Hillshade</div>
        <p>Simulated low sun. The dendritic drainage network resolves.</p></figcaption></figure>
    <figure><img src="{img_lrm}" alt="Local relief model">
      <figcaption><span class="stage"><b>03</b> · Detrend</span>
        <div class="title">Local relief</div>
        <p>Terrain minus its own low-pass. Red rises, blue cuts.</p></figcaption></figure>
    <figure><img src="{img_cand}" alt="Detected candidates on hillshade">
      <figcaption><span class="stage"><b>04</b> · Screen</span>
        <div class="title">Candidates</div>
        <p>Compact, round anomalies ringed by class.</p></figcaption></figure>
  </div>

  <h2>Candidate map <span class="hint">{n_total} flagged</span></h2>
  <div class="feature">
    <img src="{img_cand}" alt="Candidate structures over hillshade">
    <div class="legend">
      <span><span class="dot dot--earth"></span>Mound / platform — positive relief ({n_mound})</span>
      <span><span class="dot dot--water"></span>Ring / ditched enclosure — negative relief ({n_ring})</span>
    </div>
  </div>

  <h2>Ranked readout <span class="hint">by anomaly score</span></h2>
  <div class="scroll">
    <table>
      <thead><tr>
        <th>#</th><th>Class</th><th>Lat</th><th>Lon</th>
        <th>⌀ m</th><th>Amp m</th><th>Reg</th><th>Score</th>
      </tr></thead>
      <tbody>
        {rows}
      </tbody>
    </table>
  </div>

  <h2>Method</h2>
  <div class="prose">
    <ol class="steps">
      <li><strong>Fetch.</strong> A bounding box is converted to Web-Mercator
        tiles; each Terrarium-encoded PNG is decoded to metres and stitched into
        one georeferenced grid.</li>
      <li><strong>Detrend (Local Relief Model).</strong> Subtracting a Gaussian
        low-pass of the terrain removes valleys and regional slope, leaving the
        low-amplitude bumps and ditches where earthworks live.</li>
      <li><strong>Screen.</strong> Relief anomalies are thresholded against a
        robust background (median/MAD), filtered by real-world size and
        roundness, scored, and written out as WGS84 GeoJSON.</li>
      <li><strong>Verify — not done here.</strong> Every hit needs high-res
        imagery, site databases, and ultimately ground survey. LiDAR finds;
        it does not confirm.</li>
    </ol>
    <p>The detector is resolution-agnostic — thresholds are in metres — so the
      same code finds far smaller features when handed genuine
      <code>--geotiff</code> bare-earth LiDAR.</p>
  </div>

  <footer>
    <span>Acre transect · SRTM 30 m · screening pass</span>
    <span>coords WGS84 lon/lat · not confirmed sites</span>
  </footer>
</div>
"""

if __name__ == "__main__":
    main()
