import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Telecom Site Layout Studio",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
  #MainMenu, header, footer {visibility: hidden; height: 0;}
  .block-container {padding: 0 !important; max-width: 100% !important;}
  iframe {border: none; display: block; width: 100%;}
  [data-testid="stAppViewContainer"] > .main {padding: 0;}
</style>
""", unsafe_allow_html=True)

APP_HTML = r"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Telecom Site Layout Studio</title>
<script src="https://cdn.jsdelivr.net/npm/fabric@5.3.0/dist/fabric.min.js"></script>
<style>
  *{box-sizing:border-box;-webkit-user-select:none;user-select:none}
  html,body{margin:0;height:100%;overflow:hidden;
    font-family:system-ui,-apple-system,"Segoe UI",sans-serif;
    background:#0b1220;color:#e2e8f0;font-size:12.5px}
  #boot{position:fixed;inset:0;z-index:9999;background:#0b1220;
    display:flex;flex-direction:column;align-items:center;justify-content:center;
    color:#8b9dc3;transition:opacity .3s}
  #boot.hidden{opacity:0;pointer-events:none}
  #boot .spinner{width:36px;height:36px;border:3px solid #1f2a44;
    border-top-color:#6366f1;border-radius:50%;animation:spin .8s linear infinite;
    margin-bottom:14px}
  @keyframes spin{to{transform:rotate(360deg)}}
  #boot .err{color:#f87171;font-size:.85rem;max-width:520px;text-align:center;
    line-height:1.6;padding:20px;background:#1c1414;border:1px solid #7f1d1d;
    border-radius:12px;margin-top:12px}
  #app{display:flex;height:100vh}
  #topstrip{position:absolute;top:0;left:0;right:0;height:44px;
    background:#0d1524;border-bottom:1px solid #1f2a44;
    display:flex;align-items:center;padding:0 10px;gap:4px;z-index:30}
  #topstrip .logo{color:#a5b4fc;font-weight:700;font-size:.85rem;
    margin-right:12px;display:flex;align-items:center;gap:6px}
  #topstrip .sep{width:1px;height:22px;background:#1f2a44;margin:0 6px}
  #topstrip button{background:transparent;border:1px solid transparent;color:#8b9dc3;
    padding:5px 10px;border-radius:6px;cursor:pointer;font-size:.76rem;
    font-family:inherit;display:flex;align-items:center;gap:5px;transition:.12s}
  #topstrip button:hover{background:#1c2640;color:#e2e8f0}
  #topstrip .filelabel{color:#7c8db5;font-size:.72rem;margin-left:auto;
    display:flex;gap:8px;align-items:center}
  #sidebar{width:52px;background:#0f1626;border-right:1px solid #1f2a44;
    flex-shrink:0;display:flex;flex-direction:column;align-items:center;
    padding-top:52px;gap:3px;z-index:20;overflow-y:auto}
  #sidebar::-webkit-scrollbar{width:6px}
  #sidebar::-webkit-scrollbar-thumb{background:#27344f;border-radius:3px}
  .tbtn{width:40px;height:40px;background:transparent;border:1px solid transparent;
    color:#8b9dc3;border-radius:8px;cursor:pointer;font-size:1.1rem;
    display:flex;align-items:center;justify-content:center;transition:.12s;
    position:relative;font-family:inherit}
  .tbtn:hover{background:#1c2640;color:#e2e8f0}
  .tbtn.active{background:linear-gradient(135deg,#2563eb,#7c3aed);color:#fff;
    box-shadow:0 3px 10px rgba(99,102,241,.35)}
  .tbtn .tip{position:absolute;left:52px;background:#1c2640;color:#e2e8f0;
    padding:4px 10px;border-radius:6px;font-size:.7rem;white-space:nowrap;
    opacity:0;pointer-events:none;transition:.15s;border:1px solid #2a3a5c;
    z-index:100}
  .tbtn:hover .tip{opacity:1}
  .tbtn.sep{margin-top:6px;position:relative}
  .tbtn.sep::before{content:'';position:absolute;top:-3px;left:6px;right:6px;
    height:1px;background:#1f2a44}
  #stencil-panel{position:absolute;top:52px;left:52px;width:280px;
    background:#0f1626;border:1px solid #1f2a44;border-radius:0 0 10px 0;
    z-index:25;max-height:calc(100vh - 60px);overflow-y:auto;
    padding:10px;display:none}
  #stencil-panel.open{display:block}
  #stencil-panel::-webkit-scrollbar{width:6px}
  #stencil-panel::-webkit-scrollbar-thumb{background:#27344f;border-radius:3px}
  #stencil-panel h4{margin:10px 0 6px;font-size:.66rem;text-transform:uppercase;
    letter-spacing:.08em;color:#7c8db5}
  #stencil-panel h4:first-child{margin-top:2px}
  .stencil-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:6px}
  .stencil{background:#131a2b;border:1px solid #1f2a44;border-radius:8px;
    padding:10px 6px;cursor:pointer;transition:.12s;text-align:center;
    color:#c8d3e8;font-size:.7rem;line-height:1.25;
    display:flex;flex-direction:column;align-items:center;gap:4px}
  .stencil:hover{background:#1c2640;border-color:#3b82f6;
    transform:translateY(-1px);box-shadow:0 4px 10px rgba(0,0,0,.3)}
  #props{width:290px;background:#0f1626;border-left:1px solid #1f2a44;
    padding:60px 12px 20px;overflow-y:auto;flex-shrink:0;z-index:15}
  #props::-webkit-scrollbar{width:6px}
  #props::-webkit-scrollbar-thumb{background:#27344f;border-radius:3px}
  #props h3{margin:14px 0 6px;font-size:.68rem;text-transform:uppercase;
    letter-spacing:.08em;color:#7c8db5;font-weight:700}
  #props h3:first-child{margin-top:0}
  .psection{background:#131a2b;border:1px solid #1f2a44;border-radius:10px;
    padding:10px;margin-bottom:8px}
  .pbtn{display:flex;align-items:center;gap:6px;width:100%;padding:7px 10px;
    margin:3px 0;background:#1c2640;color:#e2e8f0;border:1px solid #2a3a5c;
    border-radius:7px;font-size:.76rem;cursor:pointer;text-align:left;
    transition:.12s;font-family:inherit}
  .pbtn:hover{background:#243256;border-color:#3b4d75}
  .pbtn.danger:hover{background:#7f1d1d;border-color:#dc2626;color:#fecaca}
  .prow{display:flex;gap:5px}
  .prow .pbtn{flex:1;justify-content:center;text-align:center}
  input[type="color"]{width:100%;height:28px;border:none;background:transparent;
    cursor:pointer;border-radius:6px}
  input[type="range"]{width:100%;accent-color:#6366f1}
  input[type="text"],input[type="number"],select,textarea{width:100%;padding:5px 8px;
    border-radius:6px;border:1px solid #2a3a5c;background:#0b1220;
    color:#e2e8f0;font-size:.76rem;font-family:inherit}
  input:focus,select:focus,textarea:focus{outline:none;border-color:#6366f1;
    box-shadow:0 0 0 2px rgba(99,102,241,.2)}
  textarea{resize:vertical;min-height:52px}
  label{font-size:.68rem;color:#8b9dc3;display:flex;
    justify-content:space-between;align-items:center;margin:5px 0 2px}
  label span.val{color:#a5b4fc;font-weight:600}
  .swatches{display:grid;grid-template-columns:repeat(6,1fr);gap:3px;margin-top:4px}
  .swatch{aspect-ratio:1;border-radius:4px;cursor:pointer;
    border:2px solid transparent;transition:.1s}
  .swatch:hover{transform:scale(1.08)}
  .swatch.sel{border-color:#fff;box-shadow:0 0 0 2px #6366f1}
  #stage{flex:1;position:relative;overflow:hidden;
    background:repeating-conic-gradient(#0a1020 0 25%,#0b1220 0 50%) 50%/24px 24px;
    padding-top:44px}
  #canvas-holder{position:absolute;top:44px;left:0;transform-origin:0 0;
    will-change:transform}
  #canvastools{position:absolute;bottom:14px;right:310px;display:flex;gap:6px;
    background:rgba(19,26,43,.92);backdrop-filter:blur(12px);
    border:1px solid #2a3a5c;padding:5px;border-radius:10px;z-index:20;
    box-shadow:0 8px 24px rgba(0,0,0,.4)}
  #canvastools button{background:transparent;border:none;color:#8b9dc3;
    padding:5px 10px;border-radius:6px;cursor:pointer;font-size:.76rem;
    font-family:inherit;display:flex;align-items:center;gap:4px;transition:.12s}
  #canvastools button:hover{background:#1c2640;color:#e2e8f0}
  #canvastools button.active{background:#2563eb;color:#fff}
  #zoom-lvl{min-width:52px;justify-content:center;color:#a5b4fc;
    font-family:ui-monospace,monospace;font-size:.7rem;
    display:flex;align-items:center;padding:0 6px}
  #hud{position:absolute;bottom:14px;left:64px;display:flex;gap:6px;
    align-items:center;z-index:10}
  #hud .chip{background:rgba(19,26,43,.92);backdrop-filter:blur(12px);
    border:1px solid #2a3a5c;padding:5px 10px;border-radius:7px;
    font-size:.68rem;color:#a5b4fc;font-family:ui-monospace,monospace}
  #hud .chip.warn{border-color:#f59e0b;color:#fbbf24}
  #hud .chip.err{border-color:#dc2626;color:#fca5a5}
  #hud .chip.ok{border-color:#22c55e;color:#86efac}
  #toast{position:fixed;bottom:24px;left:50%;
    transform:translateX(-50%) translateY(100px);
    background:#1c2640;border:1px solid #3b4d75;color:#e2e8f0;
    padding:10px 20px;border-radius:10px;font-size:.8rem;
    box-shadow:0 10px 30px rgba(0,0,0,.5);transition:transform .25s ease;
    z-index:100;pointer-events:none;max-width:80vw}
  #toast.show{transform:translateX(-50%) translateY(0)}
  #toast.err{background:#3b1212;border-color:#7f1d1d;color:#fecaca}
  #toast.warn{background:#3b2a12;border-color:#b45309;color:#fde68a}
  #toast.ok{background:#0f2417;border-color:#15803d;color:#bbf7d0}
  #measure{position:fixed;background:#1c2640;border:1px solid #6366f1;
    padding:4px 8px;border-radius:6px;font-size:.72rem;color:#c7d2fe;
    font-family:ui-monospace,monospace;pointer-events:none;z-index:200;
    display:none}
  .sel-only{display:none}
  .sel-only.on{display:block}
  .empty-note{color:#7c8db5;font-size:.72rem;line-height:1.5;
    padding:8px;background:#0b1220;border-radius:6px;border:1px dashed #2a3a5c}
</style>
</head>
<body>

<div id="boot">
  <div class="spinner"></div>
  <div id="boot-msg">Loading Telecom Studio…</div>
  <div id="boot-err" style="display:none" class="err"></div>
</div>

<div id="app" style="display:none">
  <div id="topstrip">
    <div class="logo">📡 Telecom Site Studio</div>
    <div class="sep"></div>
    <button id="tb-new" title="New site plan">🆕 New</button>
    <button id="tb-open" title="Open image">📁 Open Image</button>
    <button id="tb-paste" title="Paste image">📋 Paste Img</button>
    <button id="tb-load-json" title="Load layout">📂 Load Layout</button>
    <button id="tb-save-json" title="Save layout">💾 Save Layout</button>
    <div class="sep"></div>
    <button id="tb-copy" title="Copy (Ctrl+C)">📄 Copy</button>
    <button id="tb-paste-obj" title="Paste (Ctrl+V)">📋 Paste</button>
    <button id="tb-cut" title="Cut (Ctrl+X)">✂️ Cut</button>
    <div class="sep"></div>
    <button id="tb-undo" title="Undo Ctrl+Z">↩️</button>
    <button id="tb-redo" title="Redo Ctrl+Y">↪️</button>
    <div class="sep"></div>
    <button id="tb-zoom-fit" title="Fit (F)">🎯 Fit</button>
    <button id="tb-zoom-in">＋</button>
    <button id="tb-zoom-out">－</button>
    <div class="sep"></div>
    <button id="tb-export-png" title="Export PNG">🖼️ PNG</button>
    <button id="tb-print" title="Print (A3)">🖨️ Print</button>
    <div class="filelabel">
      <span id="file-label">Untitled Site Plan</span>
    </div>
  </div>

  <aside id="sidebar">
    <button class="tbtn active" data-tool="select"><span>🖱️</span><span class="tip">Select / Move (V)</span></button>
    <button class="tbtn" data-tool="pan"><span>✋</span><span class="tip">Pan (H)</span></button>
    <div class="sep"></div>
    <button class="tbtn" id="tbtn-stencil"><span>📦</span><span class="tip">Stencils</span></button>
    <button class="tbtn" data-tool="pen"><span>✏️</span><span class="tip">Freehand (P)</span></button>
    <button class="tbtn" data-tool="line"><span>📏</span><span class="tip">Line (L)</span></button>
    <button class="tbtn" data-tool="polyline"><span>↗️</span><span class="tip">Polyline (Enter)</span></button>
    <button class="tbtn" data-tool="rect"><span>⬛</span><span class="tip">Rectangle (R)</span></button>
    <button class="tbtn" data-tool="circle"><span>⭕</span><span class="tip">Circle (C)</span></button>
    <button class="tbtn" data-tool="text"><span>🔤</span><span class="tip">Text (T)</span></button>
    <div class="sep"></div>
    <button class="tbtn" data-tool="dim-h"><span>↔️</span><span class="tip">H-Dimension</span></button>
    <button class="tbtn" data-tool="dim-v"><span>↕️</span><span class="tip">V-Dimension</span></button>
    <div class="sep"></div>
    <button class="tbtn" data-tool="erase"><span>🧹</span><span class="tip">Eraser (E)</span></button>
  </aside>

  <div id="stencil-panel">
    <h4>🚪 Gate & Access</h4>
    <div class="stencil-grid">
      <div class="stencil" data-stencil="gate_2door"><span>🚪</span>Gate (2-Door)</div>
      <div class="stencil" data-stencil="fence"><span>🔲</span>Boundary Fence</div>
    </div>
    <h4>🏢 Cabin / Shelter</h4>
    <div class="stencil-grid">
      <div class="stencil" data-stencil="cabin"><span>🏠</span>Shelter</div>
      <div class="stencil" data-stencil="stairs"><span>🪜</span>Cement Stairs</div>
    </div>
    <h4>🗄️ Cabinets</h4>
    <div class="stencil-grid">
      <div class="stencil" data-stencil="odc"><span>🗄️</span>ODC</div>
      <div class="stencil" data-stencil="cab1"><span>🗃️</span>1-Bay</div>
      <div class="stencil" data-stencil="cab2"><span>🗃️</span>2-Bay</div>
      <div class="stencil" data-stencil="cab3"><span>🗃️</span>3-Bay</div>
    </div>
    <h4>📡 Tower</h4>
    <div class="stencil-grid">
      <div class="stencil" data-stencil="tower4"><span>📡</span>4-Leg Tower</div>
      <div class="stencil" data-stencil="tower3"><span>📡</span>3-Leg Tower</div>
      <div class="stencil" data-stencil="towerfoot"><span>🔩</span>Footing</div>
      <div class="stencil" data-stencil="guy"><span>⚓</span>Guy Anchor</div>
    </div>
    <h4>⚡ Power</h4>
    <div class="stencil-grid">
      <div class="stencil" data-stencil="genset"><span>🔌</span>Generator+Pad</div>
      <div class="stencil" data-stencil="fuel"><span>⛽</span>Fuel Tank</div>
      <div class="stencil" data-stencil="transformer"><span>⚡</span>Transformer</div>
      <div class="stencil" data-stencil="battery"><span>🔋</span>Battery Bank</div>
    </div>
    <h4>🛠️ Pads & Bases</h4>
    <div class="stencil-grid">
      <div class="stencil" data-stencil="basepad"><span>⬛</span>Cement Basepad</div>
      <div class="stencil" data-stencil="basepad_gen"><span>🟧</span>Gen Basepad</div>
      <div class="stencil" data-stencil="basepad_tx"><span>🟨</span>TX Basepad</div>
      <div class="stencil" data-stencil="basepad_ac"><span>🟦</span>AC Basepad</div>
    </div>
    <h4>❄️ Cooling</h4>
    <div class="stencil-grid">
      <div class="stencil" data-stencil="aircon"><span>❄️</span>Air Conditioner</div>
    </div>
    <h4>🛣️ Cable Infrastructure</h4>
    <div class="stencil-grid">
      <div class="stencil" data-stencil="cabletray"><span>🛤️</span>Cable Tray</div>
      <div class="stencil" data-stencil="openrack"><span>🗂️</span>Open Rack</div>
      <div class="stencil" data-stencil="hframe"><span>🪜</span>H-Frame</div>
    </div>
    <h4>🌱 Site Surface</h4>
    <div class="stencil-grid">
      <div class="stencil" data-stencil="grass"><span>🌱</span>Grass Area</div>
      <div class="stencil" data-stencil="cement"><span>⬜</span>Cement Slab</div>
      <div class="stencil" data-stencil="gravel"><span>🪨</span>Gravel Pad</div>
      <div class="stencil" data-stencil="wall"><span>🧱</span>Wall</div>
    </div>
    <h4>🔤 Labels</h4>
    <div class="stencil-grid">
      <div class="stencil" data-stencil="label_equipment"><span>🏷️</span>Equip Label</div>
      <div class="stencil" data-stencil="label_cable"><span>🆔</span>Cable Label</div>
      <div class="stencil" data-stencil="label_zone"><span>📛</span>Zone Label</div>
      <div class="stencil" data-stencil="label_note"><span>📝</span>Note</div>
    </div>
  </div>

  <aside id="props">
    <h3>🎨 Draw Style</h3>
    <div class="psection">
      <label>Palette</label>
      <div class="swatches" id="palette"></div>
      <label>Stroke color</label>
      <input type="color" id="stroke-color" value="#334155">
      <label>Stroke width <span class="val" id="sw-val">2px</span></label>
      <input type="range" id="stroke-width" min="1" max="12" value="2">
      <label><span>Enable fill</span>
        <input type="checkbox" id="fill-enabled" style="width:auto" checked></label>
      <input type="color" id="fill-color" value="#94a3b8">
      <label>Fill opacity <span class="val" id="fill-op-val">40%</span></label>
      <input type="range" id="fill-opacity" min="0" max="100" value="40">
    </div>

    <h3>🔤 Text Tool</h3>
    <div class="psection">
      <input type="text" id="text-value" value="LABEL" maxlength="80">
      <label>Font size <span class="val" id="fs-val">16px</span></label>
      <input type="range" id="font-size" min="8" max="72" value="16">
    </div>

    <h3>⚙️ Selected Object</h3>
    <div class="psection" id="sel-empty">
      <div class="empty-note">
        Nothing selected. Click an object on the canvas to edit it here.
      </div>
    </div>

    <div class="psection sel-only" id="sel-props">
      <div style="display:flex;justify-content:space-between;align-items:center;
        margin-bottom:6px;font-size:.72rem;color:#a5b4fc">
        <span id="sel-type">Object</span>
        <span id="sel-uid" style="font-family:ui-monospace,monospace;
          color:#66748f;font-size:.65rem"></span>
      </div>

      <div class="sel-only" id="row-stroke">
        <label>Stroke color</label>
        <input type="color" id="sel-stroke-color">
      </div>
      <div class="sel-only" id="row-strokew">
        <label>Stroke width <span class="val" id="sel-sw-val">2px</span></label>
        <input type="range" id="sel-stroke-width" min="0" max="20" value="2">
      </div>
      <div class="sel-only" id="row-fill">
        <label><span>Fill enabled</span>
          <input type="checkbox" id="sel-fill-enabled" style="width:auto"></label>
        <input type="color" id="sel-fill-color">
        <label>Fill opacity <span class="val" id="sel-fillop-val">40%</span></label>
        <input type="range" id="sel-fill-opacity" min="0" max="100" value="40">
      </div>
      <div class="sel-only" id="row-text">
        <label>Text content</label>
        <textarea id="sel-text" rows="2"></textarea>
      </div>
      <div class="sel-only" id="row-fontsize">
        <label>Font size <span class="val" id="sel-fs-val">16px</span></label>
        <input type="range" id="sel-font-size" min="6" max="120" value="16">
      </div>
      <div class="sel-only" id="row-fontstyle">
        <label><span>Bold</span>
          <input type="checkbox" id="sel-bold" style="width:auto"></label>
        <label><span>Italic</span>
          <input type="checkbox" id="sel-italic" style="width:auto"></label>
      </div>
      <div class="sel-only" id="row-opacity">
        <label>Opacity <span class="val" id="sel-op-val">100%</span></label>
        <input type="range" id="sel-opacity" min="5" max="100" value="100">
      </div>
      <div class="sel-only" id="row-angle">
        <label>Rotation <span class="val" id="sel-angle-val">0°</span></label>
        <input type="range" id="sel-angle" min="-180" max="180" value="0">
      </div>
      <div class="sel-only" id="row-geom">
        <label>Position & Size</label>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:4px">
          <input type="number" id="sel-x" placeholder="X" step="1">
          <input type="number" id="sel-y" placeholder="Y" step="1">
          <input type="number" id="sel-w" placeholder="W" step="1">
          <input type="number" id="sel-h" placeholder="H" step="1">
        </div>
        <div class="prow" style="margin-top:5px">
          <button class="pbtn" id="sel-lock-ratio">🔒 <span>Ratio</span></button>
          <button class="pbtn" id="sel-reset-size">↺ <span>Reset</span></button>
        </div>
      </div>
      <div class="sel-only" id="row-actions">
        <div class="prow" style="margin-top:6px">
          <button class="pbtn" id="sel-front">⬆ <span>Front</span></button>
          <button class="pbtn" id="sel-back">⬇ <span>Back</span></button>
        </div>
        <div class="prow">
          <button class="pbtn" id="sel-copy">📄 <span>Copy</span></button>
          <button class="pbtn" id="sel-paste">📋 <span>Paste</span></button>
        </div>
        <div class="prow">
          <button class="pbtn" id="sel-dup">📑 <span>Duplicate</span></button>
          <button class="pbtn danger" id="sel-del">🗑️ <span>Delete</span></button>
        </div>
      </div>
    </div>

    <h3>🧲 Snap</h3>
    <div class="psection">
      <label><span>Snap to grid</span>
        <input type="checkbox" id="snap-grid" style="width:auto"></label>
      <label>Grid size <span class="val" id="grid-val">20px</span></label>
      <input type="range" id="grid-size" min="5" max="100" value="20">
      <label><span>Snap to objects</span>
        <input type="checkbox" id="snap-end" checked style="width:auto"></label>
      <label><span>Show grid</span>
        <input type="checkbox" id="show-grid" style="width:auto" checked></label>
      <label><span>Orthogonal (H/V)</span>
        <input type="checkbox" id="ortho" style="width:auto"></label>
    </div>

    <h3>📏 Scale & Units</h3>
    <div class="psection">
      <label>Drawing scale (1px = ? m)</label>
      <input type="number" id="scale-m" value="0.05" step="0.001" min="0.001">
      <label>Unit</label>
      <input type="text" id="unit-label" value="m" maxlength="6">
      <label><span>Show measurements</span>
        <input type="checkbox" id="show-length" style="width:auto" checked></label>
    </div>

    <h3>🛡️ Session</h3>
    <div class="psection">
      <div class="prow">
        <button class="pbtn" id="btn-backup">💼 <span>Backup</span></button>
        <button class="pbtn danger" id="btn-reset">🧨 <span>Reset</span></button>
      </div>
      <div id="storage-info" style="font-size:.66rem;color:#66748f;
        font-family:ui-monospace,monospace;margin-top:6px;text-align:center">
        storage: —
      </div>
    </div>

    <h3>❓ Help</h3>
    <div class="psection" style="font-size:.68rem;color:#8b9dc3;line-height:1.7">
      <div><b style="color:#a5b4fc">Copy:</b> Ctrl+C</div>
      <div><b style="color:#a5b4fc">Paste:</b> Ctrl+V (offsets +20px)</div>
      <div><b style="color:#a5b4fc">Cut:</b> Ctrl+X</div>
      <div><b style="color:#a5b4fc">Duplicate:</b> Ctrl+D or Alt+drag</div>
      <div><b style="color:#a5b4fc">Zoom:</b> Ctrl + scroll</div>
      <div><b style="color:#a5b4fc">Pan:</b> Space + drag or H</div>
      <div><b style="color:#a5b4fc">Fit:</b> F</div>
      <div><b style="color:#a5b4fc">Finish polyline:</b> Enter</div>
    </div>
  </aside>

  <main id="stage">
    <div id="canvas-holder"><canvas id="c"></canvas></div>
    <div id="canvastools">
      <button id="ct-zoom-fit" title="Fit (F)">🎯</button>
      <button id="ct-zoom-out">－</button>
      <span id="zoom-lvl">100%</span>
      <button id="ct-zoom-in">＋</button>
      <button id="ct-toggle-ortho" title="Orthogonal mode (Shift)">📐 Ortho</button>
      <button id="ct-toggle-dim" title="Auto-dimension labels" class="active">📏 Dims</button>
    </div>
    <div id="hud">
      <div class="chip" id="hud-xy">x: 0  y: 0</div>
      <div class="chip" id="hud-count">0 objects</div>
    </div>
    <div id="measure"></div>
    <div id="toast"></div>
  </main>
</div>

<script>
/* =====================================================================
   0. BOOT + ERROR BOUNDARY
   ===================================================================== */
const Boot = {
  show(m){ document.getElementById('boot-msg').textContent = m; },
  error(t, d){
    const b = document.getElementById('boot');
    b.classList.remove('hidden');
    document.getElementById('boot-msg').style.display = 'none';
    const e = document.getElementById('boot-err');
    e.style.display = 'block';
    e.innerHTML = `<b>⚠️ ${t}</b>${d}`;
  },
  ready(){
    document.getElementById('app').style.display = 'flex';
    const b = document.getElementById('boot');
    b.classList.add('hidden');
    setTimeout(() => b.remove(), 400);
  }
};
window.addEventListener('error', e => {
  console.error('[uncaught]', e.error || e.message);
  try { toast('Error: ' + (e.message || 'unknown'), 'err'); } catch(_) {}
});
window.addEventListener('unhandledrejection', e => {
  console.error('[promise]', e.reason);
  try { toast('Async error: ' + (e.reason?.message || e.reason), 'err'); } catch(_) {}
});
const $ = id => document.getElementById(id);
let toastTimer;
function toast(msg, kind){
  const t = $('toast');
  t.className = '';
  if (kind) t.classList.add(kind);
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove('show'), 2000);
}

/* =====================================================================
   1. FABRIC LOADER
   ===================================================================== */
const FABRIC_CDNS = [
  'https://cdn.jsdelivr.net/npm/fabric@5.3.0/dist/fabric.min.js',
  'https://unpkg.com/fabric@5.3.0/dist/fabric.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/fabric.js/5.3.0/fabric.min.js',
];
function loadFabric(i = 0){
  return new Promise((resolve, reject) => {
    if (window.fabric) return resolve();
    if (i >= FABRIC_CDNS.length) return reject(new Error('CDNs failed'));
    Boot.show(`Loading graphics library (${i+1}/${FABRIC_CDNS.length})…`);
    const s = document.createElement('script');
    s.src = FABRIC_CDNS[i]; s.async = true;
    const tm = setTimeout(() => s.onerror(), 8000);
    s.onload = () => { clearTimeout(tm); window.fabric ? resolve() : reject(new Error('no fabric')); };
    s.onerror = () => { clearTimeout(tm); s.remove(); loadFabric(i+1).then(resolve, reject); };
    document.head.appendChild(s);
  });
}

/* =====================================================================
   2. STORAGE
   ===================================================================== */
const Storage = {
  KEY: 'telecom_site_v4',
  KEY_CTR: 'telecom_site_ctr_v4',
  available(){
    try { const k='__t'+Math.random(); localStorage.setItem(k,'1');
          localStorage.removeItem(k); return true; } catch(_){ return false; }
  },
  get(k){ try { return localStorage.getItem(k); } catch(_){ return null; } },
  set(k,v){ try { localStorage.setItem(k,v); return true; } catch(e){ return false; } },
  del(k){ try { localStorage.removeItem(k); } catch(_){} },
  bytes(){
    if (!this.available()) return 0;
    let t = 0;
    for (let i = 0; i < localStorage.length; i++){
      const k = localStorage.key(i);
      t += (k.length + (localStorage.getItem(k)||'').length) * 2;
    }
    return t;
  }
};

/* =====================================================================
   3. STATE
   ===================================================================== */
let canvas;
let currentTool = 'select';
let pendingStencil = null;
let pendingLabelId = null;
let drawing = false, startPt = null, activeShape = null, drawMoved = false;
let polyPoints = [], polyPreview = null;
let undoStack = [], redoStack = [];
let cableCounter = 0;
let view = { zoom: 1, x: 0, y: 0 };
let spaceDown = false, panning = false, panStart = null;
let pasteLock = 0;
let shiftAxis = null;
let ortho = false;
let showDims = true;
let fileName = 'Untitled Site Plan';
let uidCounter = 1;
let lockRatio = false;
let clipboard = [];     // ★ internal clipboard for copy/paste
let clipboardOffset = 0;
const CW = 1600, CH = 1000;
const M2PX = 20;

const PALETTE = ['#334155','#64748b','#94a3b8','#cbd5e1','#f8fafc','#000000',
                 '#dc2626','#ea580c','#ca8a04','#16a34a','#0891b2','#2563eb',
                 '#7c3aed','#db2777','#a16207','#0f766e','#475569','#a3a3a3'];

const CUSTOM_PROPS = ['selectable','evented','isBackground',
                      '_isCable','_isAnnotation','_isDimension',
                      '_stencilLabel','_isStencilLabel','_labelKind',
                      '_uid','_originalWidth','_originalHeight','_boundTo'];

/* =====================================================================
   4. FABRIC PROTOTYPE
   ===================================================================== */
function tightenSelectionBoxes(){
  fabric.Object.prototype.set({
    padding: 2,
    transparentCorners: true,
    cornerColor: '#6366f1',
    cornerStrokeColor: '#ffffff',
    cornerSize: 8,
    cornerStyle: 'circle',
    borderColor: '#6366f1',
    borderScaleFactor: 1,
    borderOpacityWhenMoving: 0.6,
    perPixelTargetFind: true,
  });
}

/* =====================================================================
   5. SYMBOL PRIMITIVES
   ===================================================================== */
function uid(){ return 'o' + (uidCounter++); }
function mkLine(x1,y1,x2,y2, opt){
  return new fabric.Line([x1,y1,x2,y2], Object.assign({
    stroke:'#0f172a', strokeWidth:1.5, selectable:true, evented:true,
    strokeLineCap:'round'
  }, opt||{}));
}
function mkRect(x,y,w,h, opt){
  return new fabric.Rect(Object.assign({
    left:x, top:y, width:w, height:h,
    fill:'rgba(203,213,225,0.5)', stroke:'#0f172a', strokeWidth:1.5,
    selectable:true, evented:true
  }, opt||{}));
}
function mkCircle(cx,cy,r, opt){
  return new fabric.Circle(Object.assign({
    left:cx-r, top:cy-r, radius:r,
    fill:'rgba(203,213,225,0.5)', stroke:'#0f172a', strokeWidth:1.5,
    selectable:true, evented:true, originX:'left', originY:'top'
  }, opt||{}));
}
function mkText(s,x,y,size, opt){
  return new fabric.IText(s, Object.assign({
    left:x, top:y, fontSize:size||10,
    fill:'#0f172a', fontFamily:'system-ui, sans-serif',
    fontWeight:'600', selectable:true, evented:true
  }, opt||{}));
}
function mkGroup(objs, label){
  const g = new fabric.Group(objs, { selectable:true, evented:true });
  if (label) g._stencilLabel = label;
  g._uid = uid();
  return g;
}
function hatchRect(x,y,w,h, opt){
  opt = opt || {};
  const spacing = opt.spacing || 8;
  const color = opt.hatch || '#94a3b8';
  const g = [];
  g.push(mkRect(x,y,w,h, Object.assign({
    fill: opt.fill || 'rgba(226,232,240,0.6)',
    stroke: opt.stroke || '#0f172a', strokeWidth: opt.strokeWidth || 1.5,
  }, opt.extra || {})));
  const diag = w + h;
  for (let i = -h; i < diag; i += spacing){
    const x1 = x + i, y1 = y;
    const x2 = x + i + h, y2 = y + h;
    const sx = Math.max(x, Math.min(x1, x+w));
    const ex = Math.max(x, Math.min(x2, x+w));
    if (sx === ex) continue;
    const t1 = (sx - x1) / (x2 - x1 || 1);
    const t2 = (ex - x1) / (x2 - x1 || 1);
    const sy = y1 + t1 * (y2 - y1);
    const ey = y1 + t2 * (y2 - y1);
    if (sy < y-0.5 || sy > y+h+0.5) continue;
    g.push(mkLine(sx, Math.max(y, sy), ex, Math.min(y+h, ey),
      { stroke: color, strokeWidth: 0.7, opacity: 0.7 }));
  }
  return g;
}
function makeDetachedLabel(text, x, y, opt){
  opt = opt || {};
  const lbl = new fabric.IText(text, {
    left: x, top: y,
    fontSize: opt.fontSize || 10,
    fill: opt.fill || '#0f172a',
    fontFamily: 'system-ui, sans-serif',
    fontWeight: opt.fontWeight || '700',
    backgroundColor: opt.bg || 'rgba(255,255,255,0.85)',
    padding: 3,
    selectable: true, evented: true,
  });
  lbl._isStencilLabel = true;
  lbl._labelKind = opt.kind || 'equipment';
  lbl._uid = uid();
  lbl._boundTo = opt.boundTo || null;
  return lbl;
}

/* =====================================================================
   6. ★ STENCIL LIBRARY
   ===================================================================== */
const STENCILS = {

  gate_2door(){
    const W = 4*M2PX, H = 4;
    const parts = [];
    parts.push(mkRect(0, 0, H, H, { fill:'#64748b', stroke:'#0f172a' }));
    parts.push(mkRect(W-H, 0, H, H, { fill:'#64748b', stroke:'#0f172a' }));
    parts.push(mkLine(H, H/2, W-H, H/2, { stroke:'#0f172a', strokeWidth:2 }));
    parts.push(new fabric.Path(`M ${H} ${H/2} L ${H} ${H/2 - W*0.45}`,
      { stroke:'#0f172a', strokeWidth:1, fill:'', selectable:false }));
    parts.push(new fabric.Path(
      `M ${H} ${H/2 - W*0.45} A ${W*0.45} ${W*0.45} 0 0 1 ${H + W*0.45} ${H/2}`,
      { stroke:'#0891b2', strokeWidth:0.8, fill:'', strokeDashArray:[3,2], selectable:false }));
    parts.push(new fabric.Path(`M ${W-H} ${H/2} L ${W-H} ${H/2 - W*0.45}`,
      { stroke:'#0f172a', strokeWidth:1, fill:'', selectable:false }));
    parts.push(new fabric.Path(
      `M ${W-H} ${H/2 - W*0.45} A ${W*0.45} ${W*0.45} 0 0 0 ${W-H - W*0.45} ${H/2}`,
      { stroke:'#0891b2', strokeWidth:0.8, fill:'', strokeDashArray:[3,2], selectable:false }));
    return { group: mkGroup(parts, 'Gate'), labels: [
      { text:'GATE 2-DOOR', x: 0, y: -18, kind:'equipment' }
    ]};
  },
  fence(){
    const W = 5*M2PX, H = 3;
    const parts = [
      mkLine(0, H/2, W, H/2, { stroke:'#0f172a', strokeWidth:1.5 }),
      mkLine(0, 0, 0, H, { stroke:'#64748b', strokeWidth:3 }),
      mkLine(W, 0, W, H, { stroke:'#64748b', strokeWidth:3 }),
    ];
    for (let x = 0; x <= W; x += 10){
      parts.push(mkLine(x, H/2 - 2, x, H/2 + 2, { stroke:'#0f172a', strokeWidth:0.8 }));
    }
    return { group: mkGroup(parts, 'Fence'), labels: [] };
  },

  cabin(){
    const W = 4*M2PX, H = 3*M2PX;
    const parts = [];
    parts.push(mkRect(0, 0, W, H, { fill:'#f1f5f9', stroke:'#0f172a', strokeWidth:2 }));
    parts.push(mkRect(5, 5, W-10, H-10, { fill:'transparent', stroke:'#475569',
      strokeWidth:1, strokeDashArray:[4,2] }));
    const dw = 22, dx = W - dw - 4, dy = H/2 - 11;
    parts.push(mkRect(dx, dy, dw, 22, { fill:'#94a3b8', stroke:'#0f172a' }));
    parts.push(new fabric.Path(`M ${dx} ${dy} A 22 22 0 0 0 ${dx + 22} ${dy}`,
      { stroke:'#0891b2', strokeWidth:0.8, fill:'', strokeDashArray:[2,2], selectable:false }));
    parts.push(mkRect(6, 6, 24, 12, { fill:'#dbeafe', stroke:'#1e3a8a' }));
    parts.push(mkText('AC', 14, 9, 7, { fill:'#1e3a8a', selectable:false }));
    parts.push(mkRect(W-24, H-14, 18, 8, { fill:'#fef3c7', stroke:'#a16207' }));
    parts.push(mkText('ENTRY', W-24, H-6, 6, { fill:'#7c2d12', selectable:false }));
    return { group: mkGroup(parts, 'Shelter'), labels: [
      { text:'SHELTER', x: 0, y: -18, kind:'equipment' },
      { text:`${(W/M2PX).toFixed(1)}×${(H/M2PX).toFixed(1)}m`, x: 0, y: H + 6, kind:'dim' }
    ]};
  },
  stairs(){
    const steps = 8, tw = 30, th = 8;
    const parts = [];
    for (let i = 0; i < steps; i++){
      parts.push(mkRect(0, i*th, tw, th, { fill:'#cbd5e1', stroke:'#334155' }));
    }
    parts.push(mkLine(tw/2, steps*th - 4, tw/2, 4, { stroke:'#0891b2', strokeWidth:1.2 }));
    parts.push(new fabric.Triangle({ left: tw/2 - 3, top: 0, width: 6, height: 8,
      fill:'#0891b2', selectable:false }));
    return { group: mkGroup(parts, 'Stairs'), labels: [
      { text:'STAIRS', x: tw + 6, y: steps*th/2 - 6, kind:'equipment' }
    ]};
  },

  odc(){
    const W = 1.2*M2PX, H = 2.2*M2PX;
    const parts = [
      mkRect(0, 0, W, H, { fill:'#f8fafc', stroke:'#0f172a', strokeWidth:2 }),
      mkLine(W/2, 0, W/2, H, { stroke:'#0f172a', strokeWidth:1, strokeDashArray:[3,2] }),
      mkCircle(2, 2, 2, { fill:'#64748b', stroke:'none' }),
      mkCircle(W-4, 2, 2, { fill:'#64748b', stroke:'none' }),
      mkCircle(2, H-4, 2, { fill:'#64748b', stroke:'none' }),
      mkCircle(W-4, H-4, 2, { fill:'#64748b', stroke:'none' }),
    ];
    return { group: mkGroup(parts, 'ODC'), labels: [
      { text:'ODC', x: 0, y: -16, kind:'equipment' }
    ]};
  },
  cab1(){ return cabGeneric(1, '1-Bay'); },
  cab2(){ return cabGeneric(2, '2-Bay'); },
  cab3(){ return cabGeneric(3, '3-Bay'); },

  tower4(){
    const S = 4*M2PX;
    const parts = [];
    const pad = 14;
    [[0,0],[S,0],[0,S],[S,S]].forEach(([cx,cy]) => {
      parts.push(mkRect(cx - pad/2, cy - pad/2, pad, pad,
        { fill:'#94a3b8', stroke:'#0f172a' }));
    });
    [[0,0],[S,0],[0,S],[S,S]].forEach(([cx,cy]) => {
      parts.push(mkCircle(cx, cy, 5, { fill:'#1e293b', stroke:'#0f172a' }));
    });
    parts.push(mkLine(0, 0, S, 0, { stroke:'#0f172a', strokeWidth:1.2 }));
    parts.push(mkLine(S, 0, S, S, { stroke:'#0f172a', strokeWidth:1.2 }));
    parts.push(mkLine(S, S, 0, S, { stroke:'#0f172a', strokeWidth:1.2 }));
    parts.push(mkLine(0, S, 0, 0, { stroke:'#0f172a', strokeWidth:1.2 }));
    parts.push(mkLine(0, 0, S, S, { stroke:'#0f172a', strokeWidth:0.8, strokeDashArray:[4,3] }));
    parts.push(mkLine(S, 0, 0, S, { stroke:'#0f172a', strokeWidth:0.8, strokeDashArray:[4,3] }));
    parts.push(mkCircle(S/2, S/2, 8, { fill:'#334155', stroke:'#0f172a', strokeWidth:1.5 }));
    return { group: mkGroup(parts, '4-Leg Tower'), labels: [
      { text:'4-LEG TOWER', x: 0, y: -22, kind:'equipment' },
      { text:`${(S/M2PX).toFixed(1)}m × ${(S/M2PX).toFixed(1)}m`, x: 0, y: S + 6, kind:'dim' }
    ]};
  },
  tower3(){
    const S = 3.5*M2PX;
    const h = S * 0.866;
    const A = { x:S/2, y:0 }, B = { x:0, y:h }, C = { x:S, y:h };
    const parts = [];
    [A,B,C].forEach(p => {
      parts.push(mkRect(p.x - 7, p.y - 7, 14, 14, { fill:'#94a3b8', stroke:'#0f172a' }));
    });
    parts.push(mkLine(A.x, A.y, B.x, B.y, { stroke:'#0f172a', strokeWidth:1.2 }));
    parts.push(mkLine(B.x, B.y, C.x, C.y, { stroke:'#0f172a', strokeWidth:1.2 }));
    parts.push(mkLine(C.x, C.y, A.x, A.y, { stroke:'#0f172a', strokeWidth:1.2 }));
    [A,B,C].forEach(p => parts.push(mkCircle(p.x, p.y, 5, { fill:'#1e293b', stroke:'#0f172a' })));
    parts.push(mkLine(A.x, A.y, (B.x+C.x)/2, (B.y+C.y)/2,
      { stroke:'#0f172a', strokeWidth:0.8, strokeDashArray:[4,3] }));
    parts.push(mkLine(B.x, B.y, (A.x+C.x)/2, (A.y+C.y)/2,
      { stroke:'#0f172a', strokeWidth:0.8, strokeDashArray:[4,3] }));
    parts.push(mkLine(C.x, C.y, (A.x+B.x)/2, (A.y+B.y)/2,
      { stroke:'#0f172a', strokeWidth:0.8, strokeDashArray:[4,3] }));
    parts.push(mkCircle(S/2, h/2 + 4, 7, { fill:'#334155', stroke:'#0f172a' }));
    return { group: mkGroup(parts, '3-Leg Tower'), labels: [
      { text:'3-LEG TOWER', x: 0, y: -22, kind:'equipment' }
    ]};
  },
  towerfoot(){
    const S = 1.2*M2PX;
    const parts = [];
    parts.push(...hatchRect(0, 0, S, S, { spacing:6, hatch:'#64748b' }));
    const cx = S/2, cy = S/2, r = S*0.32;
    parts.push(mkCircle(cx, cy, r, { fill:'transparent', stroke:'#0f172a',
      strokeWidth:0.8, strokeDashArray:[2,2] }));
    for (let i = 0; i < 8; i++){
      const a = (i / 8) * Math.PI * 2;
      parts.push(mkCircle(cx + Math.cos(a)*r, cy + Math.sin(a)*r, 2,
        { fill:'#1e293b', stroke:'none' }));
    }
    return { group: mkGroup(parts, 'Footing'), labels: [
      { text:'FOOTING', x: 0, y: -16, kind:'equipment' }
    ]};
  },
  guy(){
    const S = 1*M2PX;
    const parts = [
      mkRect(0, 0, S, S, { fill:'#a8a29e', stroke:'#44403c', strokeWidth:1.5 }),
      mkCircle(S/2, S/2, S*0.25, { fill:'#fef3c7', stroke:'#a16207', strokeWidth:1 }),
      mkCircle(S/2, S/2, 2, { fill:'#1e293b' }),
    ];
    return { group: mkGroup(parts, 'Guy Anchor'), labels: [
      { text:'GUY', x: 0, y: S + 4, kind:'equipment' }
    ]};
  },

  genset(){
    const padW = 4*M2PX, padH = 2.4*M2PX;
    const genW = 3.4*M2PX, genH = 1.6*M2PX;
    const gx = (padW - genW)/2, gy = (padH - genH)/2;
    const parts = [];
    parts.push(...hatchRect(0, 0, padW, padH, { spacing:8, hatch:'#94a3b8' }));
    parts.push(mkRect(gx, gy, genW, genH,
      { fill:'#fef3c7', stroke:'#78350f', strokeWidth:2 }));
    parts.push(mkRect(gx + genW - 20, gy + 4, 16, genH - 8,
      { fill:'#fdba74', stroke:'#7c2d12', strokeWidth:1 }));
    for (let y = gy + 6; y < gy + genH - 6; y += 4){
      parts.push(mkLine(gx + genW - 19, y, gx + genW - 5, y,
        { stroke:'#7c2d12', strokeWidth:0.6 }));
    }
    parts.push(mkRect(gx + 4, gy + 4, 14, genH - 8,
      { fill:'#dbeafe', stroke:'#1e3a8a', strokeWidth:1 }));
    parts.push(mkCircle(gx + genW*0.55, gy - 4, 4,
      { fill:'#94a3b8', stroke:'#334155', strokeWidth:1 }));
    parts.push(mkText('GENSET', gx + genW/2 - 24, gy + genH/2 - 4, 10,
      { fontWeight:'700', fill:'#7c2d12', selectable:false }));
    return { group: mkGroup(parts, 'Generator'), labels: [
      { text:'GENERATOR + PAD', x: 0, y: -22, kind:'equipment' },
      { text:`${(padW/M2PX).toFixed(1)}×${(padH/M2PX).toFixed(1)}m`,
        x: 0, y: padH + 6, kind:'dim' }
    ]};
  },
  fuel(){
    const R = 0.7*M2PX;
    const parts = [];
    parts.push(mkCircle(R, R, R*1.35,
      { fill:'transparent', stroke:'#94a3b8', strokeWidth:1, strokeDashArray:[4,3] }));
    parts.push(mkCircle(R, R, R, { fill:'#fecaca', stroke:'#7f1d1d', strokeWidth:2 }));
    parts.push(mkCircle(R, R, R*0.9, { fill:'transparent', stroke:'#7f1d1d', strokeWidth:1 }));
    parts.push(mkCircle(R, R - R*0.55, R*0.12, { fill:'#7f1d1d', stroke:'none' }));
    parts.push(mkCircle(R + R*0.55, R, R*0.12, { fill:'#0891b2', stroke:'none' }));
    parts.push(mkCircle(R, R + R*0.55, R*0.12, { fill:'#334155', stroke:'none' }));
    parts.push(mkText('FUEL', R - 16, R - 4, 9,
      { fontWeight:'700', fill:'#7f1d1d', selectable:false }));
    return { group: mkGroup(parts, 'Fuel Tank'), labels: [
      { text:'FUEL TANK', x: 0, y: -R*1.5 - 6, kind:'equipment' },
      { text:`Ø${(2*R/M2PX).toFixed(1)}m`, x: 0, y: R*1.5 + 6, kind:'dim' }
    ]};
  },
  transformer(){
    const W = 1.6*M2PX, H = 1.6*M2PX;
    const parts = [];
    parts.push(mkRect(0, 0, W, H, { fill:'#fef3c7', stroke:'#78350f', strokeWidth:2 }));
    parts.push(mkCircle(W/2, H/2, W*0.28,
      { fill:'transparent', stroke:'#78350f', strokeWidth:1, strokeDashArray:[3,2] }));
    for (let i = 0; i < 3; i++){
      parts.push(mkCircle(W*0.25 + i*W*0.25, -4, 3,
        { fill:'#dc2626', stroke:'#7f1d1d', strokeWidth:1 }));
    }
    for (let i = 0; i < 2; i++){
      parts.push(mkCircle(W*0.33 + i*W*0.34, H + 4, 3,
        { fill:'#2563eb', stroke:'#1e3a8a', strokeWidth:1 }));
    }
    for (let i = 0; i < 5; i++){
      parts.push(mkLine(-2 - i*2, 4, -2 - i*2, H - 4,
        { stroke:'#78350f', strokeWidth:0.8 }));
    }
    parts.push(mkText('TX', W/2 - 8, H/2 - 4, 9,
      { fontWeight:'700', fill:'#78350f', selectable:false }));
    return { group: mkGroup(parts, 'Transformer'), labels: [
      { text:'TRANSFORMER', x: 0, y: -22, kind:'equipment' },
      { text:'HV', x: -20, y: -16, kind:'mark', fill:'#dc2626', fontSize:8 },
      { text:'LV', x: -20, y: H + 10, kind:'mark', fill:'#2563eb', fontSize:8 }
    ]};
  },
  battery(){
    const W = 2.6*M2PX, H = 0.7*M2PX;
    const cells = 4, cw = W/cells;
    const parts = [];
    for (let i = 0; i < cells; i++){
      parts.push(mkRect(i*cw, 0, cw, H,
        { fill:'#dbeafe', stroke:'#1e3a8a', strokeWidth:1.2 }));
      parts.push(mkCircle(i*cw + 4, 4, 2, { fill:'#dc2626', stroke:'none' }));
      parts.push(mkCircle(i*cw + cw - 4, 4, 2, { fill:'#1e293b', stroke:'none' }));
      parts.push(mkText(String(i+1), i*cw + cw/2 - 3, H/2 - 3, 8,
        { fill:'#1e3a8a', selectable:false }));
    }
    return { group: mkGroup(parts, 'Battery Bank'), labels: [
      { text:'BATTERY BANK', x: 0, y: -18, kind:'equipment' }
    ]};
  },

  /* ★ NEW: CEMENT BASEPADS */
  basepad(){
    const W = 3*M2PX, H = 3*M2PX;
    const parts = [];
    parts.push(...hatchRect(0, 0, W, H, {
      spacing: 10, hatch:'#94a3b8',
      fill:'rgba(203,213,225,0.65)',
      stroke:'#334155', strokeWidth: 2
    }));
    // Corner markers
    const c = 10;
    parts.push(mkLine(0, 0, c, 0, { stroke:'#0f172a', strokeWidth:2.5 }));
    parts.push(mkLine(0, 0, 0, c, { stroke:'#0f172a', strokeWidth:2.5 }));
    parts.push(mkLine(W, 0, W-c, 0, { stroke:'#0f172a', strokeWidth:2.5 }));
    parts.push(mkLine(W, 0, W, c, { stroke:'#0f172a', strokeWidth:2.5 }));
    parts.push(mkLine(0, H, c, H, { stroke:'#0f172a', strokeWidth:2.5 }));
    parts.push(mkLine(0, H, 0, H-c, { stroke:'#0f172a', strokeWidth:2.5 }));
    parts.push(mkLine(W, H, W-c, H, { stroke:'#0f172a', strokeWidth:2.5 }));
    parts.push(mkLine(W, H, W, H-c, { stroke:'#0f172a', strokeWidth:2.5 }));
    return { group: mkGroup(parts, 'Cement Basepad'), labels: [
      { text:'CEMENT BASEPAD', x: 0, y: -20, kind:'equipment' },
      { text:`${(W/M2PX).toFixed(1)} × ${(H/M2PX).toFixed(1)} m`,
        x: 0, y: H + 6, kind:'dim' }
    ]};
  },
  basepad_gen(){
    const W = 4*M2PX, H = 2.6*M2PX;
    const parts = [];
    parts.push(...hatchRect(0, 0, W, H, {
      spacing: 9, hatch:'#94a3b8',
      fill:'rgba(254,243,199,0.55)',
      stroke:'#78350f', strokeWidth: 2
    }));
    parts.push(mkText('GEN PAD', W/2 - 30, H/2 - 4, 9,
      { fontWeight:'700', fill:'#78350f', selectable:false }));
    return { group: mkGroup(parts, 'Gen Basepad'), labels: [
      { text:'GENERATOR BASEPAD', x: 0, y: -20, kind:'equipment' },
      { text:`${(W/M2PX).toFixed(1)}×${(H/M2PX).toFixed(1)}m`,
        x: 0, y: H + 6, kind:'dim' }
    ]};
  },
  basepad_tx(){
    const W = 2.2*M2PX, H = 2.2*M2PX;
    const parts = [];
    parts.push(...hatchRect(0, 0, W, H, {
      spacing: 8, hatch:'#b45309',
      fill:'rgba(254,243,199,0.65)',
      stroke:'#78350f', strokeWidth: 2
    }));
    parts.push(mkText('TX PAD', W/2 - 24, H/2 - 4, 9,
      { fontWeight:'700', fill:'#78350f', selectable:false }));
    return { group: mkGroup(parts, 'TX Basepad'), labels: [
      { text:'TRANSFORMER BASEPAD', x: 0, y: -20, kind:'equipment' }
    ]};
  },
  basepad_ac(){
    const W = 1.4*M2PX, H = 1*M2PX;
    const parts = [];
    parts.push(...hatchRect(0, 0, W, H, {
      spacing: 6, hatch:'#0ea5e9',
      fill:'rgba(224,242,254,0.7)',
      stroke:'#0369a1', strokeWidth: 1.5
    }));
    return { group: mkGroup(parts, 'AC Basepad'), labels: [
      { text:'AC BASEPAD', x: 0, y: -16, kind:'equipment' }
    ]};
  },

  aircon(){
    const W = 1.0*M2PX, H = 0.6*M2PX;
    const cx = W*0.65, cy = H/2, r = Math.min(W,H)*0.35;
    const parts = [
      mkRect(0, 0, W, H, { fill:'#e0f2fe', stroke:'#0369a1', strokeWidth:1.8 }),
      mkCircle(cx, cy, r, { fill:'#bae6fd', stroke:'#0369a1', strokeWidth:1 }),
      mkCircle(cx, cy, r*0.2, { fill:'#0369a1', stroke:'#0369a1', strokeWidth:0.5 }),
    ];
    for (let i = 0; i < 4; i++){
      const a = (i/4)*Math.PI*2;
      parts.push(mkLine(cx, cy, cx + Math.cos(a)*r*0.85, cy + Math.sin(a)*r*0.85,
        { stroke:'#0369a1', strokeWidth:0.8 }));
    }
    for (let x = 4; x < W*0.35; x += 3){
      parts.push(mkLine(x, 3, x, H-3, { stroke:'#0369a1', strokeWidth:0.6 }));
    }
    return { group: mkGroup(parts, 'Aircon'), labels: [
      { text:'AIRCON', x: 0, y: -16, kind:'equipment' }
    ]};
  },

  cabletray(){
    const W = 4*M2PX, H = 0.4*M2PX;
    const parts = [
      mkLine(0, 0, W, 0, { stroke:'#475569', strokeWidth:2 }),
      mkLine(0, H, W, H, { stroke:'#475569', strokeWidth:2 }),
    ];
    for (let x = 4; x < W; x += 6){
      parts.push(mkLine(x, 1, x, H-1, { stroke:'#475569', strokeWidth:0.8 }));
    }
    return { group: mkGroup(parts, 'Cable Tray'), labels: [
      { text:'CABLE TRAY', x: 0, y: -14, kind:'equipment' },
      { text:`${(W/M2PX).toFixed(1)}m`, x: 0, y: H + 6, kind:'dim' }
    ]};
  },
  openrack(){
    const W = 0.6*M2PX, H = 2.2*M2PX;
    const parts = [
      mkRect(0, 0, W, H, { fill:'#f8fafc', stroke:'#0f172a', strokeWidth:1.8 }),
      mkLine(2, 2, 2, H-2, { stroke:'#475569', strokeWidth:1.5 }),
      mkLine(W-2, 2, W-2, H-2, { stroke:'#475569', strokeWidth:1.5 }),
    ];
    for (let y = 6; y < H-6; y += 5){
      parts.push(mkLine(3, y, W-3, y, { stroke:'#94a3b8', strokeWidth:0.5 }));
    }
    return { group: mkGroup(parts, 'Open Rack'), labels: [
      { text:'RACK', x: 0, y: -16, kind:'equipment' }
    ]};
  },
  hframe(){
    const W = 2*M2PX, H = 2.5*M2PX;
    const parts = [
      mkRect(2, 0, 4, H, { fill:'#334155', stroke:'#0f172a', strokeWidth:1 }),
      mkRect(W-6, 0, 4, H, { fill:'#334155', stroke:'#0f172a', strokeWidth:1 }),
      mkRect(0, H/2 - 3, W, 6, { fill:'#334155', stroke:'#0f172a', strokeWidth:1 }),
      mkCircle(W*0.3, H*0.25, 5, { fill:'#fbbf24', stroke:'#92400e', strokeWidth:1 }),
      mkCircle(W*0.7, H*0.25, 5, { fill:'#fbbf24', stroke:'#92400e', strokeWidth:1 }),
      mkCircle(W*0.3, H*0.75, 5, { fill:'#fbbf24', stroke:'#92400e', strokeWidth:1 }),
      mkCircle(W*0.7, H*0.75, 5, { fill:'#fbbf24', stroke:'#92400e', strokeWidth:1 }),
    ];
    return { group: mkGroup(parts, 'H-Frame'), labels: [
      { text:'H-FRAME', x: 0, y: H + 6, kind:'equipment' }
    ]};
  },

  grass(){
    const W = 8*M2PX, H = 6*M2PX;
    const parts = [
      mkRect(0, 0, W, H, {
        fill:'rgba(132,204,22,0.18)', stroke:'#65a30d',
        strokeWidth:1, strokeDashArray:[6,4] })
    ];
    for (let i = 0; i < 80; i++){
      const x = Math.random()*W, y = Math.random()*H;
      parts.push(mkLine(x, y, x+2, y-4, { stroke:'#65a30d', strokeWidth:0.8 }));
      parts.push(mkLine(x+2, y, x+4, y-3, { stroke:'#84cc16', strokeWidth:0.8 }));
    }
    return { group: mkGroup(parts, 'Grass Area'), labels: [
      { text:'GRASS AREA', x: 0, y: -16, kind:'equipment' }
    ]};
  },
  cement(){
    const W = 8*M2PX, H = 6*M2PX;
    const parts = [
      mkRect(0, 0, W, H, {
        fill:'rgba(203,213,225,0.55)', stroke:'#64748b',
        strokeWidth:1.5, strokeDashArray:[6,3] })
    ];
    for (let x = W/4; x < W; x += W/4){
      parts.push(mkLine(x, 0, x, H, { stroke:'#94a3b8', strokeWidth:0.8, strokeDashArray:[4,3] }));
    }
    for (let y = H/3; y < H; y += H/3){
      parts.push(mkLine(0, y, W, y, { stroke:'#94a3b8', strokeWidth:0.8, strokeDashArray:[4,3] }));
    }
    return { group: mkGroup(parts, 'Cement Slab'), labels: [
      { text:'CEMENT SLAB', x: 0, y: -16, kind:'equipment' }
    ]};
  },
  gravel(){
    const W = 6*M2PX, H = 4*M2PX;
    const parts = [
      mkRect(0, 0, W, H, {
        fill:'rgba(168,162,158,0.25)', stroke:'#78716c', strokeWidth:1 })
    ];
    for (let i = 0; i < 120; i++){
      const x = Math.random()*W, y = Math.random()*H;
      parts.push(mkCircle(x, y, 0.8 + Math.random()*1.2,
        { fill:'#78716c', stroke:'none', opacity:0.65 }));
    }
    return { group: mkGroup(parts, 'Gravel Pad'), labels: [
      { text:'GRAVEL', x: 0, y: -16, kind:'equipment' }
    ]};
  },
  wall(){
    const W = 5*M2PX, H = 6;
    const parts = [
      mkRect(0, 0, W, H, { fill:'#a8a29e', stroke:'#44403c', strokeWidth:1.5 })
    ];
    for (let x = 8; x < W; x += 8){
      parts.push(mkLine(x, 0, x, H, { stroke:'#44403c', strokeWidth:0.5 }));
    }
    parts.push(mkLine(0, H/2, W, H/2, { stroke:'#44403c', strokeWidth:0.5 }));
    return { group: mkGroup(parts, 'Wall'), labels: [] };
  },
};

function cabGeneric(bays, name){
  const W = (0.6*bays)*M2PX, H = 2.2*M2PX;
  const parts = [
    mkRect(0, 0, W, H, { fill:'#e2e8f0', stroke:'#0f172a', strokeWidth:1.8 })
  ];
  for (let i = 1; i < bays; i++){
    parts.push(mkLine(i*W/bays, 2, i*W/bays, H-2,
      { stroke:'#475569', strokeWidth:0.8 }));
  }
  parts.push(mkText(bays+'B', W/2 - 8, H/2 - 4, 8,
    { fontWeight:'700', selectable:false }));
  return { group: mkGroup(parts, name), labels: [
    { text: name.toUpperCase(), x: 0, y: -16, kind:'equipment' }
  ]};
}

const LABEL_STENCILS = {
  label_equipment: { text: 'EQUIPMENT', kind:'equipment', fontSize: 12, fill: '#0f172a' },
  label_cable:     { text: 'C-01', kind:'cable', fontSize: 11, fill: '#dc2626',
                     bg: 'rgba(255,241,242,0.9)' },
  label_zone:      { text: 'ZONE A', kind:'zone', fontSize: 16, fill: '#7c3aed',
                     bg: 'rgba(243,232,255,0.9)' },
  label_note:      { text: 'NOTE: ...', kind:'note', fontSize: 11, fill: '#334155',
                     bg: 'rgba(241,245,249,0.95)' },
};

/* =====================================================================
   7. CANVAS INIT
   ===================================================================== */
function initCanvas(){
  canvas = new fabric.Canvas('c', {
    width: CW, height: CH,
    backgroundColor: '#ffffff',
    selection: true,
    preserveObjectStacking: true,
    stopContextMenu: true,
    fireRightClick: true,
    enableRetinaScaling: true,
  });

  canvas.on('mouse:down',  onDown);
  canvas.on('mouse:move',  onMove);
  canvas.on('mouse:up',    onUp);

  canvas.on('object:added', opt => {
    if (opt.target && !opt.target.isBackground){
      opt.target.set({ perPixelTargetFind:true, padding:2 });
      if (!opt.target._uid) opt.target._uid = uid();
    }
    markDirty(); refreshPanels();
  });
  canvas.on('object:modified', () => { markDirty(); refreshPanels(); syncSelectionPanel(); });
  canvas.on('object:removed',  () => { refreshPanels(); });
  canvas.on('selection:created', () => { refreshPanels(); syncSelectionPanel(); });
  canvas.on('selection:updated', () => { refreshPanels(); syncSelectionPanel(); });
  canvas.on('selection:cleared', () => { refreshPanels(); syncSelectionPanel(); });

  // ★ Live refresh of the panel while dragging/resizing
  canvas.on('object:moving',  () => syncSelectionPanelLight());
  canvas.on('object:scaling', () => syncSelectionPanelLight());
  canvas.on('object:rotating',() => syncSelectionPanelLight());

  canvas.on('mouse:dblclick', opt => {
    const t = opt.target;
    if (t && (t.type === 'i-text' || t.type === 'text' || t.type === 'textbox')){
      t.enterEditing(); t.selectAll();
    }
  });

  drawGridOverlay();
}

/* =====================================================================
   8. GRID
   ===================================================================== */
function drawGridOverlay(){
  const showGrid = $('show-grid').checked;
  const size = Math.max(4, Math.min(200, parseInt($('grid-size').value) || 20));
  if (!showGrid){
    canvas.setBackgroundColor('#ffffff', canvas.renderAll.bind(canvas));
    return;
  }
  const pc = document.createElement('canvas');
  pc.width = pc.height = size;
  const cx = pc.getContext('2d');
  cx.fillStyle = '#ffffff'; cx.fillRect(0, 0, size, size);
  cx.strokeStyle = '#e2e8f0'; cx.lineWidth = 1;
  cx.beginPath();
  cx.moveTo(size-.5, 0); cx.lineTo(size-.5, size);
  cx.moveTo(0, size-.5); cx.lineTo(size, size-.5);
  cx.stroke();
  canvas.setBackgroundColor({ source: pc, repeat: 'repeat' },
                            canvas.renderAll.bind(canvas));
}

/* =====================================================================
   9. SNAP
   ===================================================================== */
function snapPt(p){
  let x = p.x, y = p.y;
  if ($('snap-grid').checked){
    const g = Math.max(4, parseInt($('grid-size').value) || 20);
    x = Math.round(x / g) * g;
    y = Math.round(y / g) * g;
  }
  if ($('snap-end').checked && currentTool !== 'pen' && currentTool !== 'polyline'){
    const TOL = 12;
    let best = null, bestD = TOL;
    for (const o of canvas.getObjects()){
      if (o === activeShape || o.isBackground || o._isStencilLabel) continue;
      const b = o.getBoundingRect(true, true);
      const pts = [
        {x:b.left,y:b.top},{x:b.left+b.width,y:b.top},
        {x:b.left,y:b.top+b.height},{x:b.left+b.width,y:b.top+b.height},
        {x:b.left+b.width/2,y:b.top+b.height/2},
      ];
      for (const pt of pts){
        const d = Math.hypot(pt.x - x, pt.y - y);
        if (d < bestD){ bestD = d; best = pt; }
      }
    }
    if (best){ x = best.x; y = best.y; }
  }
  return { x, y };
}

/* =====================================================================
   10. POINTER HANDLERS
   ===================================================================== */
function onDown(opt){
  if (spaceDown || currentTool === 'pan'){
    panning = true;
    panStart = { x: opt.e.clientX, y: opt.e.clientY };
    return;
  }
  if (currentTool === 'erase'){
    if (opt.target && !opt.target.isBackground){ canvas.remove(opt.target); toast('Erased'); }
    return;
  }
  if (pendingStencil){
    const p = canvas.getPointer(opt.e);
    placeStencil(pendingStencil, p.x, p.y);
    return;
  }
  if (pendingLabelId){
    const p = canvas.getPointer(opt.e);
    placeLabel(pendingLabelId, p.x, p.y);
    return;
  }
  if (currentTool === 'select'){
    if (opt.target && opt.e.altKey && !opt.target.isBackground){
      const orig = opt.target;
      orig.clone(c => {
        c.set({ left:(orig.left||0)+20, top:(orig.top||0)+20,
                evented:true, selectable:true,
                perPixelTargetFind:true, padding:2, _uid: uid() });
        canvas.add(c); canvas.setActiveObject(c); canvas.renderAll();
        toast('Duplicated');
      });
    }
    return;
  }
  if (opt.target && !opt.target.isBackground) return;
  const active = canvas.getActiveObject();
  if (active && active.isEditing) return;
  if (active) canvas.discardActiveObject();

  const raw = canvas.getPointer(opt.e);
  let p = snapPt(raw);

  const sColor = $('stroke-color').value;
  const sWidth = Math.max(1, parseInt($('stroke-width').value) || 2);
  const fEnabled = $('fill-enabled').checked;
  const fOpacity = parseInt($('fill-opacity').value) / 100;
  const fColor = fEnabled ? hexWithAlpha($('fill-color').value, fOpacity) : 'transparent';

  if (currentTool === 'polyline'){
    if (!polyPreview){
      polyPoints = [p];
      polyPreview = new fabric.Polyline(polyPoints, {
        fill:'', stroke:sColor, strokeWidth:sWidth,
        strokeLineCap:'round', strokeLineJoin:'round',
        selectable:false, evented:false,
      });
      canvas.add(polyPreview);
    } else {
      polyPoints.push(p);
      polyPreview.set({ points: polyPoints.map(pt => ({x:pt.x,y:pt.y})) });
      polyPreview.setCoords();
      canvas.requestRenderAll();
    }
    return;
  }

  drawing = true; drawMoved = false; startPt = p; shiftAxis = null;

  if (currentTool === 'pen'){
    activeShape = new fabric.Path(`M ${p.x} ${p.y}`, {
      stroke:sColor, strokeWidth:sWidth, fill:'',
      strokeLineCap:'round', strokeLineJoin:'round',
      selectable:false, evented:false,
    });
    canvas.add(activeShape);
  } else if (currentTool === 'line' || currentTool === 'dim-h' || currentTool === 'dim-v'){
    activeShape = new fabric.Line([p.x, p.y, p.x, p.y], {
      stroke: currentTool.startsWith('dim') ? '#0891b2' : sColor,
      strokeWidth: sWidth, selectable:false, evented:false,
    });
    activeShape._isDimension = currentTool.startsWith('dim');
    canvas.add(activeShape);
  } else if (currentTool === 'rect'){
    activeShape = new fabric.Rect({
      left:p.x, top:p.y, width:1, height:1,
      fill:fColor, stroke:sColor, strokeWidth:sWidth,
      selectable:false, evented:false,
    });
    canvas.add(activeShape);
  } else if (currentTool === 'circle'){
    activeShape = new fabric.Circle({
      left:p.x, top:p.y, radius:1,
      fill:fColor, stroke:sColor, strokeWidth:sWidth,
      selectable:false, evented:false, originX:'left', originY:'top',
    });
    canvas.add(activeShape);
  } else if (currentTool === 'text'){
    const label = new fabric.IText($('text-value').value || 'LABEL', {
      left:p.x, top:p.y, fill:sColor,
      fontSize: parseInt($('font-size').value),
      fontFamily:'system-ui, sans-serif', fontWeight:'600',
    });
    canvas.add(label); canvas.setActiveObject(label);
    markDirty(); refreshPanels();
    drawing = false; activeShape = null;
    setTimeout(() => setTool('select'), 60);
  }
}

function onMove(opt){
  const raw = canvas.getPointer(opt.e);
  $('hud-xy').textContent = `x: ${Math.round(raw.x)}  y: ${Math.round(raw.y)}`;

  if (panning && panStart){
    view.x += opt.e.clientX - panStart.x;
    view.y += opt.e.clientY - panStart.y;
    panStart = { x: opt.e.clientX, y: opt.e.clientY };
    applyView();
    return;
  }
  if (currentTool === 'polyline' && polyPreview){
    const p = snapPt(raw);
    const pts = polyPoints.concat([p]);
    polyPreview.set({ points: pts.map(pt => ({x:pt.x,y:pt.y})) });
    canvas.requestRenderAll();
    updateMeasureHUD(opt, polyPoints[polyPoints.length - 1], p);
    return;
  }
  if (!drawing || !activeShape) return;

  let p = snapPt(raw);
  const orthoOn = opt.e.shiftKey || $('ortho').checked || ortho;

  if (orthoOn && (currentTool === 'line' || currentTool === 'rect' ||
      currentTool === 'circle' || currentTool === 'dim-h' || currentTool === 'dim-v')){
    const dx = Math.abs(p.x - startPt.x);
    const dy = Math.abs(p.y - startPt.y);
    if (currentTool === 'dim-h' || currentTool === 'dim-v'){
      if (currentTool === 'dim-h') p = { x:p.x, y:startPt.y };
      else                         p = { x:startPt.x, y:p.y };
    } else {
      if (!shiftAxis) shiftAxis = dx > dy ? 'x' : 'y';
      if (shiftAxis === 'x') p = { x:p.x, y:startPt.y };
      else                    p = { x:startPt.x, y:p.y };
    }
  } else if (!orthoOn){ shiftAxis = null; }

  if (!drawMoved && Math.hypot(p.x - startPt.x, p.y - startPt.y) > 6) drawMoved = true;

  if (currentTool === 'pen'){
    activeShape.path.push(['L', p.x, p.y]);
    activeShape.dirty = true;
  } else if (currentTool === 'line' || currentTool === 'dim-h' || currentTool === 'dim-v'){
    activeShape.set({ x2:p.x, y2:p.y });
  } else if (currentTool === 'rect'){
    activeShape.set({
      left: Math.min(startPt.x, p.x), top: Math.min(startPt.y, p.y),
      width: Math.abs(p.x - startPt.x), height: Math.abs(p.y - startPt.y),
    });
  } else if (currentTool === 'circle'){
    const r = Math.hypot(p.x - startPt.x, p.y - startPt.y);
    activeShape.set({ left: startPt.x - r, top: startPt.y - r, radius: r });
  }

  if ($('show-length').checked && (currentTool === 'line' ||
      currentTool === 'dim-h' || currentTool === 'dim-v' ||
      currentTool === 'rect' || currentTool === 'circle')){
    updateMeasureHUD(opt, startPt, p);
  }
  canvas.requestRenderAll();
}

function updateMeasureHUD(opt, a, b){
  const m = $('measure');
  const dx = b.x - a.x, dy = b.y - a.y;
  const px = Math.hypot(dx, dy);
  const meters = (px * parseFloat($('scale-m').value || 0.05)).toFixed(2);
  m.textContent = `${meters} ${$('unit-label').value}  ·  ${Math.round(px)}px`;
  m.style.left = (opt.e.clientX + 14) + 'px';
  m.style.top  = (opt.e.clientY + 14) + 'px';
  m.style.display = 'block';
}

function onUp(){
  if (panning){ panning = false; panStart = null; return; }
  if (!drawing) return;
  drawing = false;
  $('measure').style.display = 'none';
  if (!activeShape){ shiftAxis = null; return; }

  const isPen = activeShape.type === 'path';
  if (!drawMoved && !isPen){
    canvas.remove(activeShape); activeShape = null; shiftAxis = null; return;
  }
  if (isPen && activeShape.path.length < 3 && !drawMoved){
    canvas.remove(activeShape); activeShape = null; return;
  }
  try {
    if (activeShape.type === 'line'){
      const len = Math.hypot(activeShape.x2 - activeShape.x1, activeShape.y2 - activeShape.y1);
      if (len < 3){ canvas.remove(activeShape); activeShape = null; shiftAxis = null; return; }
    }
    if (activeShape.type === 'rect' &&
        (activeShape.width < 3 || activeShape.height < 3)){
      canvas.remove(activeShape); activeShape = null; shiftAxis = null; return;
    }
    if (activeShape.type === 'circle' && activeShape.radius < 3){
      canvas.remove(activeShape); activeShape = null; shiftAxis = null; return;
    }
  } catch(_) {}

  activeShape.set({ selectable:true, evented:true, perPixelTargetFind:true, padding:2 });
  activeShape._uid = uid();
  canvas.setActiveObject(activeShape);

  if (showDims && (activeShape.type === 'line' || activeShape._isDimension)){
    addDimensionLabel(activeShape);
  }
  activeShape = null; shiftAxis = null;
  canvas.requestRenderAll();
  markDirty(); refreshPanels();
  syncSelectionPanel();
}

function addDimensionLabel(line){
  const dx = line.x2 - line.x1, dy = line.y2 - line.y1;
  const px = Math.hypot(dx, dy);
  const meters = (px * parseFloat($('scale-m').value || 0.05)).toFixed(2);
  const mid = { x:(line.x1 + line.x2)/2, y:(line.y1 + line.y2)/2 };
  const angle = Math.atan2(dy, dx) * 180 / Math.PI;
  const txt = new fabric.IText(meters + ' ' + $('unit-label').value, {
    left: mid.x, top: mid.y - 14,
    fontSize: 10, fill: '#0891b2',
    fontFamily: 'ui-monospace, monospace',
    backgroundColor: 'rgba(255,255,255,.9)',
    padding: 2, selectable:true, evented:true,
    angle: (Math.abs(angle) > 90 ? angle + 180 : angle),
  });
  txt._isAnnotation = true;
  txt._uid = uid();
  canvas.add(txt);
}

/* =====================================================================
   11. STENCIL PLACEMENT
   ===================================================================== */
function placeStencil(id, x, y){
  const fn = STENCILS[id];
  if (!fn){ toast('Unknown stencil', 'err'); pendingStencil = null; return; }
  try {
    const { group, labels } = fn();
    group.set({
      left:x, top:y, originX:'center', originY:'center',
      perPixelTargetFind:true, padding:2,
    });
    canvas.add(group);

    if (labels && labels.length){
      const b = group.getBoundingRect(true, true);
      labels.forEach((L) => {
        const lx = b.left + b.width/2 + L.x;
        const ly = b.top + (L.y !== undefined ? L.y : 0) + (L.y < 0 ? 0 : b.height);
        const opt = Object.assign({ boundTo: group._uid, kind: L.kind }, L);
        const lbl = makeDetachedLabel(L.text, lx - 30, ly, opt);
        canvas.add(lbl);
      });
    }
    canvas.setActiveObject(group);
    canvas.renderAll();
    toast('Placed: ' + id.replace(/_/g,' '));
  } catch(e){
    toast('Stencil failed: ' + e.message, 'err');
    console.error(e);
  }
  pendingStencil = null;
  setTool('select');
  $('stencil-panel').classList.remove('open');
}

function placeLabel(id, x, y){
  const def = LABEL_STENCILS[id];
  if (!def){ toast('Unknown label', 'err'); pendingLabelId = null; return; }
  const lbl = makeDetachedLabel(def.text, x - 40, y - 10, {
    fontSize: def.fontSize, fill: def.fill,
    bg: def.bg, kind: def.kind,
  });
  canvas.add(lbl);
  canvas.setActiveObject(lbl);
  canvas.renderAll();
  toast('Label placed — drag, double-click to edit');
  pendingLabelId = null;
  setTool('select');
  $('stencil-panel').classList.remove('open');
}

/* =====================================================================
   12. TOOLS
   ===================================================================== */
function setTool(tool){
  if (currentTool === 'polyline' && polyPreview) finalizePolyline();
  pendingStencil = null;
  pendingLabelId = null;
  currentTool = tool;
  document.querySelectorAll('.tbtn[data-tool]').forEach(b =>
    b.classList.toggle('active', b.dataset.tool === tool));
  canvas.selection = tool === 'select';
  canvas.forEachObject(o => { o.evented = true; });
  document.body.style.cursor = (tool === 'select') ? 'default'
    : (tool === 'pan') ? 'grab' : 'crosshair';
}
document.querySelectorAll('.tbtn[data-tool]').forEach(b => {
  b.onclick = () => setTool(b.dataset.tool);
});
function finalizePolyline(){
  if (!polyPreview || polyPoints.length < 2){
    if (polyPreview) canvas.remove(polyPreview);
    polyPreview = null; polyPoints = [];
    return;
  }
  polyPreview.set({ selectable:true, evented:true, perPixelTargetFind:true, padding:2 });
  polyPreview._uid = uid();
  canvas.setActiveObject(polyPreview);
  canvas.requestRenderAll();
  markDirty(); refreshPanels();
  polyPreview = null; polyPoints = [];
  toast('Polyline finished');
}
$('tbtn-stencil').onclick = () => $('stencil-panel').classList.toggle('open');
document.querySelectorAll('.stencil').forEach(el => {
  el.onclick = () => {
    const id = el.dataset.stencil;
    if (id in LABEL_STENCILS){
      pendingLabelId = id;
      toast(`Click on canvas to place: ${id.replace(/_/g,' ')}`);
    } else {
      pendingStencil = id;
      toast(`Click on canvas to place: ${id.replace(/_/g,' ')}`);
    }
  };
});

/* =====================================================================
   13. HELPERS
   ===================================================================== */
function hexWithAlpha(hex, alpha){
  if (!hex || hex[0] !== '#') return hex;
  let h = hex.slice(1);
  if (h.length === 3) h = h.split('').map(c=>c+c).join('');
  const r = parseInt(h.slice(0,2),16), g = parseInt(h.slice(2,4),16), b = parseInt(h.slice(4,6),16);
  return `rgba(${r},${g},${b},${alpha})`;
}
function rgbaToHex(rgba){
  if (!rgba) return '#000000';
  if (typeof rgba !== 'string') return '#000000';
  if (rgba[0] === '#'){
    let h = rgba.slice(1);
    if (h.length === 3) h = h.split('').map(c=>c+c).join('');
    return '#' + h.slice(0,6);
  }
  const m = rgba.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
  if (!m) return '#000000';
  return '#' + [m[1],m[2],m[3]].map(v => (+v).toString(16).padStart(2,'0')).join('');
}
function hexAlphaOf(rgba){
  if (!rgba || typeof rgba !== 'string') return 1;
  if (rgba[0] === '#') return 1;
  const m = rgba.match(/rgba\([^)]+,\s*([\d.]+)\s*\)/);
  return m ? parseFloat(m[1]) : 1;
}

/* =====================================================================
   14. ★ LIVE SELECTION PANEL (FIXED)
   ===================================================================== */
let suppressPanelSync = false;   // ← prevents feedback loop when panel drives canvas

function showSelField(id, on){
  const el = $(id);
  if (!el) return;
  el.classList.toggle('on', !!on);
}

function syncSelectionPanelLight(){
  // Fast refresh of X/Y/W/H/angle only while dragging
  const o = canvas.getActiveObject();
  if (!o) return;
  if ($('sel-x') !== document.activeElement)
    $('sel-x').value = Math.round(o.left || 0);
  if ($('sel-y') !== document.activeElement)
    $('sel-y').value = Math.round(o.top || 0);
  if ($('sel-w') !== document.activeElement)
    $('sel-w').value = Math.round((o.width || 0) * (o.scaleX || 1));
  if ($('sel-h') !== document.activeElement)
    $('sel-h').value = Math.round((o.height || 0) * (o.scaleY || 1));
  if ($('sel-angle') !== document.activeElement){
    const ang = Math.round(o.angle || 0);
    $('sel-angle').value = ang;
    $('sel-angle-val').textContent = ang + '°';
  }
}

function syncSelectionPanel(){
  if (suppressPanelSync) return;
  const objs = canvas.getActiveObjects();
  const o = objs[0];
  const multi = objs.length > 1;
  const empty = $('sel-empty');
  const props = $('sel-props');

  if (!o){
    empty.style.display = 'block';
    props.style.display = 'none';
    return;
  }
  empty.style.display = 'none';
  props.style.display = 'block';

  const typeLabel = multi ? `${objs.length} objects selected`
                          : (o._isStencilLabel ? 'Label'
                            : o._isAnnotation ? 'Dimension label'
                            : o.type);
  $('sel-type').textContent = typeLabel;
  $('sel-uid').textContent = o._uid || '';

  const isText = ['i-text','text','textbox'].includes(o.type);
  const isLine = o.type === 'line' || o.type === 'path' || o.type === 'polyline';
  const isShape = ['rect','circle','triangle','polygon','ellipse','group'].includes(o.type);
  const hasStroke = o.stroke != null && o.stroke !== '' && o.stroke !== 'transparent';
  const hasFill = o.fill != null && o.fill !== '' && o.fill !== 'transparent';

  showSelField('row-stroke',  hasStroke || isShape || isLine || isText);
  showSelField('row-strokew', isShape || isLine || isText);
  showSelField('row-fill',    !isText);
  showSelField('row-text',    isText);
  showSelField('row-fontsize',isText);
  showSelField('row-fontstyle',isText);
  showSelField('row-opacity', true);
  showSelField('row-angle',   true);
  showSelField('row-geom',    true);
  showSelField('row-actions', true);

  // ★ Populate — only touch elements that are NOT currently focused
  const safeSet = (id, v) => { if ($(id) !== document.activeElement) $(id).value = v; };

  safeSet('sel-stroke-color', rgbaToHex(o.stroke));
  const sw = Math.max(0, Math.round(o.strokeWidth || 0));
  safeSet('sel-stroke-width', sw);
  $('sel-sw-val').textContent = sw + 'px';

  safeSet('sel-fill-color', rgbaToHex(o.fill));
  $('sel-fill-enabled').checked = hasFill;
  const fo = Math.round(hexAlphaOf(o.fill) * 100);
  safeSet('sel-fill-opacity', fo);
  $('sel-fillop-val').textContent = fo + '%';

  if (isText){
    if ($('sel-text') !== document.activeElement) $('sel-text').value = o.text || '';
    const fs = o.fontSize || 16;
    safeSet('sel-font-size', fs);
    $('sel-fs-val').textContent = fs + 'px';
    $('sel-bold').checked = String(o.fontWeight) === '700' || String(o.fontWeight) === 'bold';
    $('sel-italic').checked = o.fontStyle === 'italic';
  }

  const op = Math.round((o.opacity == null ? 1 : o.opacity) * 100);
  safeSet('sel-opacity', op);
  $('sel-op-val').textContent = op + '%';

  const ang = Math.round(o.angle || 0);
  safeSet('sel-angle', ang);
  $('sel-angle-val').textContent = ang + '°';

  safeSet('sel-x', Math.round(o.left || 0));
  safeSet('sel-y', Math.round(o.top || 0));
  safeSet('sel-w', Math.round((o.width || 0) * (o.scaleX || 1)));
  safeSet('sel-h', Math.round((o.height || 0) * (o.scaleY || 1)));
  $('sel-lock-ratio').classList.toggle('active', lockRatio);
}

function applyToSelection(fn){
  const objs = canvas.getActiveObjects();
  if (!objs.length) return;
  suppressPanelSync = true;
  objs.forEach(fn);
  canvas.requestRenderAll();
  suppressPanelSync = false;
  markDirty();
}

/* ---- Live bindings (FIXED) ---- */
$('sel-stroke-color').addEventListener('input', e => {
  const v = e.target.value;
  applyToSelection(o => o.set('stroke', v));
  syncSelectionPanelLight();
});
$('sel-stroke-width').addEventListener('input', e => {
  const v = parseInt(e.target.value);
  $('sel-sw-val').textContent = v + 'px';
  applyToSelection(o => o.set('strokeWidth', v));
});
$('sel-fill-enabled').addEventListener('change', e => {
  const on = e.target.checked;
  const hex = $('sel-fill-color').value;
  const a = parseInt($('sel-fill-opacity').value) / 100;
  applyToSelection(o => {
    if (o.type === 'i-text' || o.type === 'text' || o.type === 'textbox') return;
    o.set('fill', on ? hexWithAlpha(hex, a) : 'transparent');
  });
  syncSelectionPanelLight();
});
$('sel-fill-color').addEventListener('input', e => {
  const hex = e.target.value;
  const a = parseInt($('sel-fill-opacity').value) / 100;
  applyToSelection(o => {
    if (o.type === 'i-text' || o.type === 'text' || o.type === 'textbox') return;
    if (o.fill === 'transparent') return;
    o.set('fill', hexWithAlpha(hex, a));
  });
});
$('sel-fill-opacity').addEventListener('input', e => {
  const a = parseInt(e.target.value) / 100;
  $('sel-fillop-val').textContent = e.target.value + '%';
  const hex = $('sel-fill-color').value;
  applyToSelection(o => {
    if (o.type === 'i-text' || o.type === 'text' || o.type === 'textbox') return;
    if (o.fill === 'transparent') return;
    o.set('fill', hexWithAlpha(hex, a));
  });
});
$('sel-text').addEventListener('input', e => {
  const v = e.target.value;
  applyToSelection(o => {
    if (o.type === 'i-text' || o.type === 'text' || o.type === 'textbox'){
      o.set('text', v);
      if (o.initDimensions) o.initDimensions();
    }
  });
});
$('sel-font-size').addEventListener('input', e => {
  const v = parseInt(e.target.value);
  $('sel-fs-val').textContent = v + 'px';
  applyToSelection(o => {
    if (o.type === 'i-text' || o.type === 'text' || o.type === 'textbox'){
      o.set('fontSize', v);
      if (o.initDimensions) o.initDimensions();
      o.setCoords();
    }
  });
});
$('sel-bold').addEventListener('change', e => {
  const v = e.target.checked ? '700' : '400';
  applyToSelection(o => {
    if (o.type === 'i-text' || o.type === 'text' || o.type === 'textbox'){
      o.set('fontWeight', v);
      if (o.initDimensions) o.initDimensions();
    }
  });
});
$('sel-italic').addEventListener('change', e => {
  const v = e.target.checked ? 'italic' : 'normal';
  applyToSelection(o => {
    if (o.type === 'i-text' || o.type === 'text' || o.type === 'textbox'){
      o.set('fontStyle', v);
      if (o.initDimensions) o.initDimensions();
    }
  });
});
$('sel-opacity').addEventListener('input', e => {
  const v = parseInt(e.target.value) / 100;
  $('sel-op-val').textContent = e.target.value + '%';
  applyToSelection(o => o.set('opacity', v));
});
$('sel-angle').addEventListener('input', e => {
  const v = parseInt(e.target.value);
  $('sel-angle-val').textContent = v + '°';
  applyToSelection(o => { o.rotate(v); o.setCoords(); });
});
$('sel-x').addEventListener('change', e => {
  const v = parseFloat(e.target.value);
  applyToSelection(o => o.set('left', v));
  syncSelectionPanel();
});
$('sel-y').addEventListener('change', e => {
  const v = parseFloat(e.target.value);
  applyToSelection(o => o.set('top', v));
  syncSelectionPanel();
});
$('sel-w').addEventListener('change', e => {
  const v = parseFloat(e.target.value);
  applyToSelection(o => {
    const baseW = o.width || 1;
    const newScaleX = v / baseW;
    if (lockRatio) o.set({ scaleX: newScaleX, scaleY: newScaleX });
    else o.set('scaleX', newScaleX);
    o.setCoords();
  });
});
$('sel-h').addEventListener('change', e => {
  const v = parseFloat(e.target.value);
  applyToSelection(o => {
    const baseH = o.height || 1;
    const newScaleY = v / baseH;
    if (lockRatio) o.set({ scaleX: newScaleY, scaleY: newScaleY });
    else o.set('scaleY', newScaleY);
    o.setCoords();
  });
});
$('sel-lock-ratio').onclick = () => {
  lockRatio = !lockRatio;
  $('sel-lock-ratio').classList.toggle('active', lockRatio);
};
$('sel-reset-size').onclick = () => {
  applyToSelection(o => { o.set({ scaleX:1, scaleY:1 }); o.setCoords(); });
  syncSelectionPanel();
  toast('Size reset');
};
$('sel-front').onclick = () => {
  const o = canvas.getActiveObject();
  if (o){ canvas.bringToFront(o); markDirty(); }
};
$('sel-back').onclick = () => {
  const o = canvas.getActiveObject();
  if (o){ canvas.sendToBack(o); markDirty(); }
};
$('sel-copy').onclick = () => copySelection();
$('sel-paste').onclick = () => pasteClipboard();
$('sel-dup').onclick = duplicateSel;
$('sel-del').onclick = deleteSel;

/* =====================================================================
   15. ★ COPY / PASTE
   ===================================================================== */
function copySelection(){
  const objs = canvas.getActiveObjects();
  if (!objs.length){ toast('Nothing selected', 'warn'); return false; }
  clipboard = [];
  let pending = objs.length;
  objs.forEach(o => {
    o.clone(c => {
      c.set({ _uid: uid() });
      clipboard.push(c);
      if (--pending === 0){
        clipboardOffset = 0;
        toast(`Copied ${clipboard.length} object${clipboard.length===1?'':'s'}`, 'ok');
      }
    }, CUSTOM_PROPS);
  });
  return true;
}

function pasteClipboard(){
  if (!clipboard.length){ toast('Clipboard empty', 'warn'); return; }
  clipboardOffset += 20;
  const pasted = [];
  let pending = clipboard.length;
  clipboard.forEach(src => {
    src.clone(c => {
      c.set({
        left: (src.left || 0) + clipboardOffset,
        top:  (src.top  || 0) + clipboardOffset,
        perPixelTargetFind: true,
        padding: 2,
        evented: true,
        selectable: true,
        _uid: uid(),
      });
      c.setCoords();
      canvas.add(c);
      pasted.push(c);
      if (--pending === 0){
        canvas.discardActiveObject();
        if (pasted.length === 1){
          canvas.setActiveObject(pasted[0]);
        } else {
          const sel = new fabric.ActiveSelection(pasted, { canvas });
          canvas.setActiveObject(sel);
        }
        canvas.requestRenderAll();
        refreshPanels();
        syncSelectionPanel();
        toast(`Pasted ${pasted.length} object${pasted.length===1?'':'s'}`, 'ok');
      }
    }, CUSTOM_PROPS);
  });
}

function cutSelection(){
  if (!copySelection()){
    return;
  }
  setTimeout(() => {
    const objs = canvas.getActiveObjects();
    objs.forEach(o => canvas.remove(o));
    canvas.discardActiveObject();
    canvas.renderAll();
    refreshPanels();
    syncSelectionPanel();
    toast('Cut', 'ok');
  }, 30);
}

/* =====================================================================
   16. HISTORY
   ===================================================================== */
const MAX_HISTORY = 80, MAX_BYTES = 4_000_000;
function serialize(){
  try {
    return JSON.stringify({
      v: 4,
      canvas: { w: canvas.getWidth(), h: canvas.getHeight() },
      fabric: canvas.toJSON(CUSTOM_PROPS),
    });
  } catch(e){ return '{"v":4,"fabric":{"objects":[]}}'; }
}
let saveTimer;
function markDirty(){
  clearTimeout(saveTimer);
  saveTimer = setTimeout(saveLocal, 800);
  pushHistory();
}
function pushHistory(){
  const j = serialize();
  if (undoStack[undoStack.length-1] === j) return;
  undoStack.push(j);
  while (undoStack.length > MAX_HISTORY ||
         undoStack.reduce((a,s)=>a+s.length,0) > MAX_BYTES){
    undoStack.shift();
  }
  redoStack = [];
  updateHud();
}
function undo(){
  if (undoStack.length < 2){ toast('Nothing to undo', 'warn'); return; }
  redoStack.push(undoStack.pop());
  applySnapshot(undoStack[undoStack.length-1]);
  toast('Undo');
}
function redo(){
  if (!redoStack.length){ toast('Nothing to redo', 'warn'); return; }
  const j = redoStack.pop();
  undoStack.push(j);
  applySnapshot(j);
  toast('Redo');
}
function applySnapshot(j){
  const bg = canvas.backgroundImage;
  try {
    canvas.loadFromJSON(j, () => {
      if (bg) canvas.setBackgroundImage(bg, canvas.renderAll.bind(canvas));
      canvas.forEachObject(o => {
        o.evented = true;
        o.set({ perPixelTargetFind:true, padding:2 });
        if (!o._uid) o._uid = uid();
      });
      canvas.renderAll();
      refreshPanels();
      syncSelectionPanel();
    });
  } catch(e){ toast('Restore failed: ' + e.message, 'err'); }
}

/* =====================================================================
   17. ACTIONS
   ===================================================================== */
function deleteSel(){
  const objs = canvas.getActiveObjects();
  if (!objs.length){ toast('Nothing selected', 'warn'); return; }
  objs.forEach(o => canvas.remove(o));
  canvas.discardActiveObject();
  refreshPanels(); syncSelectionPanel(); toast('Deleted ' + objs.length);
}
function duplicateSel(){
  const objs = canvas.getActiveObjects();
  if (!objs.length){ toast('Nothing selected', 'warn'); return; }
  const newOnes = [];
  let pending = objs.length;
  objs.forEach(o => {
    o.clone(c => {
      c.set({ left:(o.left||0)+20, top:(o.top||0)+20,
              perPixelTargetFind:true, padding:2, _uid: uid() });
      canvas.add(c);
      newOnes.push(c);
      if (--pending === 0){
        canvas.discardActiveObject();
        if (newOnes.length === 1) canvas.setActiveObject(newOnes[0]);
        else canvas.setActiveObject(new fabric.ActiveSelection(newOnes, { canvas }));
        canvas.renderAll();
        refreshPanels();
        syncSelectionPanel();
      }
    }, CUSTOM_PROPS);
  });
  toast('Duplicated');
}
function rotate90(){
  const o = canvas.getActiveObject();
  if (!o){ toast('Select an object', 'warn'); return; }
  o.rotate((o.angle || 0) + 90);
  o.setCoords();
  canvas.renderAll();
  markDirty(); syncSelectionPanel();
}
function flipSel(){
  const o = canvas.getActiveObject();
  if (!o){ toast('Select an object', 'warn'); return; }
  o.set('flipX', !o.flipX);
  canvas.renderAll();
  markDirty();
}
function clearAll(){
  const n = canvas.getObjects().length;
  if (!n){ toast('Nothing to clear', 'warn'); return; }
  if (!confirm(`Clear ${n} object(s)?`)) return;
  canvas.getObjects().forEach(o => canvas.remove(o));
  refreshPanels(); syncSelectionPanel(); toast('Cleared');
}

/* =====================================================================
   18. IMAGE
   ===================================================================== */
const MAX_IMAGE_DIM = 4096;
function downscaleIfNeeded(dataUrl){
  return new Promise(resolve => {
    const im = new Image();
    im.onload = () => {
      const w = im.width, h = im.height;
      if (w <= MAX_IMAGE_DIM && h <= MAX_IMAGE_DIM)
        return resolve({ dataUrl, w, h, scaled:false });
      const k = MAX_IMAGE_DIM / Math.max(w, h);
      const nw = Math.round(w*k), nh = Math.round(h*k);
      const cv = document.createElement('canvas');
      cv.width = nw; cv.height = nh;
      cv.getContext('2d').drawImage(im, 0, 0, nw, nh);
      resolve({ dataUrl: cv.toDataURL('image/png'), w:nw, h:nh,
                scaled:true, from:{ w, h } });
    };
    im.onerror = () => resolve({ err:true });
    im.src = dataUrl;
  });
}
async function loadImage(dataUrl, name){
  if (!dataUrl || !dataUrl.startsWith('data:image')){
    toast('Invalid image', 'err'); return;
  }
  try {
    const r = await downscaleIfNeeded(dataUrl);
    if (r.err){ toast('Decode failed', 'err'); return; }
    if (r.scaled) toast(`Downscaled to ${r.w}×${r.h}`, 'warn');
    fabric.Image.fromURL(r.dataUrl, img => {
      const s = Math.min(CW / img.width, CH / img.height, 1);
      img.set({
        left:0, top:0, scaleX:s, scaleY:s,
        selectable:false, evented:false, isBackground:true, opacity:0.6,
      });
      canvas.setWidth(img.width * s);
      canvas.setHeight(img.height * s);
      canvas.setBackgroundImage(img, canvas.renderAll.bind(canvas));
      fitView();
      toast(`Loaded ${name || 'image'}`);
    });
  } catch(e){ toast('Load failed: ' + e.message, 'err'); }
}
$('tb-open').onclick = () => {
  const inp = document.createElement('input');
  inp.type = 'file'; inp.accept = 'image/*';
  inp.onchange = e => {
    const f = e.target.files[0]; if (!f) return;
    const r = new FileReader();
    r.onload = ev => loadImage(ev.target.result, f.name);
    r.readAsDataURL(f);
  };
  inp.click();
};
$('tb-paste').onclick = () => {
  // Image paste — triggers via paste event
  document.body.focus();
  toast('Press Ctrl+V to paste image from clipboard');
};
$('tb-copy').onclick = copySelection;
$('tb-paste-obj').onclick = pasteClipboard;
$('tb-cut').onclick = cutSelection;

/* Image paste handler */
document.addEventListener('paste', e => {
  const now = Date.now();
  const items = (e.clipboardData || {}).items || [];
  // Image branch
  for (const it of items){
    if (it.kind === 'file' && it.type.startsWith('image/')){
      if (now - pasteLock < 500) return;
      pasteLock = now;
      const r = new FileReader();
      r.onload = ev => loadImage(ev.target.result, 'pasted');
      r.readAsDataURL(it.getAsFile());
      e.preventDefault();
      return;
    }
  }
  // Object paste branch (no image → paste internal clipboard)
  const editing = e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' ||
                  e.target.isContentEditable;
  if (!editing && clipboard.length){
    // Handled by keyboard shortcut too — but this ensures Ctrl+V works reliably
  }
});

document.addEventListener('dragover', e => e.preventDefault());
document.addEventListener('drop', e => {
  e.preventDefault();
  const f = e.dataTransfer.files[0];
  if (!f || !f.type.startsWith('image/')) return;
  const r = new FileReader();
  r.onload = ev => loadImage(ev.target.result, f.name);
  r.readAsDataURL(f);
});

/* =====================================================================
   19. VIEW
   ===================================================================== */
function applyView(){
  $('canvas-holder').style.transform =
    `translate(${view.x}px, ${view.y}px) scale(${view.zoom})`;
  $('zoom-lvl').textContent = Math.round(view.zoom * 100) + '%';
}
function zoomBy(f, cx, cy){
  const stage = $('stage').getBoundingClientRect();
  cx = cx ?? stage.width/2; cy = cy ?? stage.height/2;
  const prev = view.zoom;
  view.zoom = Math.max(0.1, Math.min(10, view.zoom * f));
  const k = view.zoom / prev;
  view.x = cx - (cx - view.x) * k;
  view.y = cy - (cy - view.y) * k;
  applyView();
}
function fitView(){
  const stage = $('stage').getBoundingClientRect();
  const cw = canvas.getWidth(), ch = canvas.getHeight();
  const z = Math.min((stage.width-80)/cw, (stage.height-80)/ch);
  view.zoom = z;
  view.x = (stage.width - cw*z)/2;
  view.y = (stage.height - ch*z)/2;
  applyView();
}
$('stage').addEventListener('wheel', e => {
  if (!e.ctrlKey) return;
  e.preventDefault();
  const r = $('stage').getBoundingClientRect();
  zoomBy(e.deltaY < 0 ? 1.1 : 1/1.1, e.clientX - r.left, e.clientY - r.top);
}, { passive:false });
$('stage').addEventListener('mousedown', e => {
  if ((spaceDown || currentTool === 'pan') && e.button === 0){
    panning = true;
    panStart = { x:e.clientX, y:e.clientY };
    e.preventDefault();
  }
});
window.addEventListener('mouseup', () => { if (panning){ panning = false; panStart = null; } });
window.addEventListener('mousemove', e => {
  if (!panning || !panStart) return;
  view.x += e.clientX - panStart.x;
  view.y += e.clientY - panStart.y;
  panStart = { x:e.clientX, y:e.clientY };
  applyView();
});

/* =====================================================================
   20. PANELS
   ===================================================================== */
function refreshPanels(){ updateHud(); updateStorageInfo(); }
function updateHud(){
  const n = canvas.getObjects().filter(o => !o.isBackground).length;
  const chip = $('hud-count');
  chip.textContent = n + ' object' + (n===1?'':'s') +
    (clipboard.length ? ' · 📋' + clipboard.length : '');
  chip.classList.remove('warn','err','ok');
  if (n > 800) chip.classList.add('err');
  else if (n > 300) chip.classList.add('warn');
  else if (clipboard.length) chip.classList.add('ok');
}
function updateStorageInfo(){
  const el = $('storage-info');
  if (!Storage.available()){ el.textContent = 'storage: unavailable'; return; }
  el.textContent = 'storage: ' + (Storage.bytes()/1024).toFixed(1) + ' KB';
}

/* =====================================================================
   21. EXPORT
   ===================================================================== */
function download(blob, name){
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = name;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 4000);
}
function exportPNG(scale){
  try {
    scale = scale || 2;
    const sel = canvas.getActiveObject();
    canvas.discardActiveObject();
    canvas.renderAll();
    const gridOn = $('show-grid').checked;
    const savedBgColor = canvas.backgroundColor;
    if (gridOn){ canvas.setBackgroundColor('transparent', ()=>{}); canvas.renderAll(); }
    const url = canvas.toDataURL({ format:'png', multiplier:scale, quality:1 });
    if (gridOn){ drawGridOverlay(); canvas.backgroundColor = savedBgColor; }
    if (sel) canvas.setActiveObject(sel);
    canvas.renderAll();
    fetch(url).then(r => r.blob()).then(b => {
      download(b, `site_layout_${scale}x_${Date.now()}.png`);
      toast(`PNG exported at ${scale}×`);
    });
  } catch(e){ toast('Export error: ' + e.message, 'err'); }
}
function exportJSON(){
  try {
    const data = {
      version: 4, kind: 'telecom_site_layout',
      exported: new Date().toISOString(),
      canvas: { width: canvas.getWidth(), height: canvas.getHeight() },
      scale: { m_per_px: parseFloat($('scale-m').value || 0.05),
               unit: $('unit-label').value || 'm' },
      file_name: fileName,
      fabric: canvas.toJSON(CUSTOM_PROPS),
    };
    download(new Blob([JSON.stringify(data, null, 2)], { type:'application/json' }),
             (fileName || 'site_layout').replace(/\s+/g,'_') + '.json');
    toast('Layout saved');
  } catch(e){ toast('Save failed: ' + e.message, 'err'); }
}
function loadJSONDialog(){
  const inp = document.createElement('input');
  inp.type = 'file'; inp.accept = '.json';
  inp.onchange = e => {
    const f = e.target.files[0]; if (!f) return;
    const r = new FileReader();
    r.onload = ev => {
      let parsed;
      try { parsed = JSON.parse(ev.target.result); }
      catch(err){ toast('Invalid JSON: ' + err.message, 'err'); return; }
      const fab = parsed.fabric || parsed;
      if (!fab || !Array.isArray(fab.objects)){
        toast('Not a valid layout file', 'err'); return;
      }
      if (parsed.scale){
        $('scale-m').value = parsed.scale.m_per_px ?? 0.05;
        $('unit-label').value = parsed.scale.unit || 'm';
      }
      if (parsed.file_name){ fileName = parsed.file_name; $('file-label').textContent = fileName; }
      const bg = canvas.backgroundImage;
      try {
        canvas.loadFromJSON(fab, () => {
          if (bg) canvas.setBackgroundImage(bg, canvas.renderAll.bind(canvas));
          canvas.forEachObject(o => {
            o.evented = true;
            o.set({ perPixelTargetFind:true, padding:2 });
            if (!o._uid) o._uid = uid();
          });
          canvas.renderAll(); refreshPanels(); syncSelectionPanel();
          toast('Layout loaded');
        });
      } catch(err){ toast('Load failed: ' + err.message, 'err'); }
    };
    r.readAsText(f);
  };
  inp.click();
}
function printPlan(){
  toast('Preparing print…');
  const sel = canvas.getActiveObject();
  canvas.discardActiveObject();
  const url = canvas.toDataURL({ format:'png', multiplier:2 });
  if (sel) canvas.setActiveObject(sel);
  const w = window.open('', '_blank');
  w.document.write(`<html><head><title>${fileName}</title>
    <style>body{margin:0;display:flex;align-items:center;justify-content:center;
      min-height:100vh;background:#f8fafc;font-family:system-ui}
    img{max-width:100%;max-height:100vh;box-shadow:0 4px 12px rgba(0,0,0,.2)}
    @page{size:A3 landscape;margin:10mm}
    </style></head><body><img src="${url}" onload="window.print()"/></body></html>`);
  w.document.close();
}

/* =====================================================================
   22. SAVE / RESTORE
   ===================================================================== */
function saveLocal(){
  if (!Storage.available()) return;
  Storage.set(Storage.KEY, serialize());
  Storage.set(Storage.KEY_CTR, String(cableCounter));
  updateStorageInfo();
}
function loadLocal(){
  if (!Storage.available()) return false;
  const j = Storage.get(Storage.KEY);
  if (!j) return false;
  let parsed;
  try { parsed = JSON.parse(j); } catch(e){ Storage.del(Storage.KEY); return false; }
  const fab = parsed.fabric || parsed;
  if (!fab || !Array.isArray(fab.objects)){ Storage.del(Storage.KEY); return false; }
  try {
    canvas.loadFromJSON(fab, () => {
      canvas.forEachObject(o => {
        o.evented = true;
        o.set({ perPixelTargetFind:true, padding:2 });
        if (!o._uid) o._uid = uid();
      });
      canvas.renderAll(); refreshPanels(); syncSelectionPanel();
      const n = canvas.getObjects().filter(o => !o.isBackground).length;
      toast(`Restored session (${n} object${n===1?'':'s'})`);
    });
    return true;
  } catch(e){ toast('Restore failed', 'err'); return false; }
}

/* =====================================================================
   23. KEYBOARD
   ===================================================================== */
document.addEventListener('keydown', e => {
  const editing = e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' ||
                  e.target.isContentEditable;

  if ((e.ctrlKey||e.metaKey) && e.shiftKey && e.key.toLowerCase()==='d'){
    e.preventDefault(); runDiagnostics(); return;
  }
  if (editing) return;

  if (e.code === 'Space'){ spaceDown = true;
    document.body.style.cursor = 'grab'; e.preventDefault(); }

  const k = e.key.toLowerCase();
  if (e.ctrlKey || e.metaKey){
    if (k === 'c'){ e.preventDefault(); copySelection(); }
    else if (k === 'v'){ e.preventDefault(); pasteClipboard(); }
    else if (k === 'x'){ e.preventDefault(); cutSelection(); }
    else if (k === 'z'){ e.preventDefault(); e.shiftKey ? redo() : undo(); }
    else if (k === 'y'){ e.preventDefault(); redo(); }
    else if (k === 'd'){ e.preventDefault(); duplicateSel(); }
    else if (k === 's'){ e.preventDefault(); exportJSON(); }
    else if (k === 'o'){ e.preventDefault(); loadJSONDialog(); }
    else if (k === 'a'){
      e.preventDefault();
      canvas.discardActiveObject();
      const objs = canvas.getObjects().filter(o => !o.isBackground);
      if (!objs.length) return;
      const sel = new fabric.ActiveSelection(objs, { canvas });
      canvas.setActiveObject(sel); canvas.renderAll();
      syncSelectionPanel();
    }
    return;
  }
  if (e.key === 'Delete' || e.key === 'Backspace'){ e.preventDefault(); deleteSel(); }
  else if (k === 'v') setTool('select');
  else if (k === 'h') setTool('pan');
  else if (k === 'p') setTool('pen');
  else if (k === 'l') setTool('line');
  else if (k === 'r') setTool('rect');
  else if (k === 'c') setTool('circle');
  else if (k === 't') setTool('text');
  else if (k === 'e') setTool('erase');
  else if (k === 'f') fitView();
  else if (k === 'escape'){
    if (polyPreview) finalizePolyline();
    pendingStencil = null; pendingLabelId = null;
    canvas.discardActiveObject(); canvas.renderAll();
    syncSelectionPanel();
  }
  else if (k === 'enter'){ if (polyPreview) finalizePolyline(); }
});
document.addEventListener('keyup', e => {
  if (e.code === 'Space'){ spaceDown = false;
    document.body.style.cursor = currentTool === 'select' ? 'default'
      : currentTool === 'pan' ? 'grab' : 'crosshair'; }
});
window.addEventListener('blur', () => {
  spaceDown = false; panning = false; panStart = null;
  if (drawing){ drawing = false; $('measure').style.display = 'none'; }
});

/* =====================================================================
   24. DIAGNOSTICS
   ===================================================================== */
function runDiagnostics(){
  const lines = [
    'Telecom Site Layout Studio — Diagnostics',
    'Time: ' + new Date().toISOString(),
    'Fabric.js: ' + (window.fabric ? '✓ '+fabric.version : '✗'),
    'localStorage: ' + (Storage.available() ? '✓' : '✗'),
    'Storage bytes: ' + Storage.bytes(),
    'Canvas: ' + canvas.getWidth()+'×'+canvas.getHeight(),
    'Objects: ' + canvas.getObjects().length,
    'Labels: ' + canvas.getObjects().filter(o=>o._isStencilLabel).length,
    'Stencils: ' + Object.keys(STENCILS).length,
    'Clipboard: ' + clipboard.length,
    'Undo: ' + undoStack.length + ' / Redo: ' + redoStack.length,
    'UA: ' + navigator.userAgent,
  ];
  const txt = lines.join('\n');
  console.log(txt);
  try {
    download(new Blob([txt], { type:'text/plain' }), 'diagnostics_'+Date.now()+'.txt');
    toast('Diagnostics downloaded');
  } catch(e){ toast('See console', 'warn'); }
}

/* =====================================================================
   25. TOOLBAR BINDINGS
   ===================================================================== */
$('tb-new').onclick = () => {
  if (!confirm('New site plan? Unsaved work will be lost.')) return;
  canvas.getObjects().forEach(o => canvas.remove(o));
  canvas.setBackgroundImage(null, canvas.renderAll.bind(canvas));
  canvas.setWidth(CW); canvas.setHeight(CH);
  clipboard = [];
  fileName = 'Untitled Site Plan'; $('file-label').textContent = fileName;
  fitView(); refreshPanels(); syncSelectionPanel();
  toast('New plan started');
};
$('tb-load-json').onclick = loadJSONDialog;
$('tb-save-json').onclick = exportJSON;
$('tb-undo').onclick = undo;
$('tb-redo').onclick = redo;
$('tb-zoom-fit').onclick = fitView;
$('tb-zoom-in').onclick = () => zoomBy(1.2);
$('tb-zoom-out').onclick = () => zoomBy(1/1.2);
$('tb-export-png').onclick = () => exportPNG(2);
$('tb-print').onclick = printPlan;
$('ct-zoom-fit').onclick = fitView;
$('ct-zoom-in').onclick = () => zoomBy(1.2);
$('ct-zoom-out').onclick = () => zoomBy(1/1.2);
$('ct-toggle-ortho').onclick = () => {
  ortho = !ortho;
  $('ct-toggle-ortho').classList.toggle('active', ortho);
  toast('Orthogonal ' + (ortho ? 'ON' : 'OFF'));
};
$('ct-toggle-dim').onclick = () => {
  showDims = !showDims;
  $('ct-toggle-dim').classList.toggle('active', showDims);
  toast('Auto-dims ' + (showDims ? 'ON' : 'OFF'));
};

$('stroke-width').oninput = e => $('sw-val').textContent = e.target.value + 'px';
$('font-size').oninput    = e => $('fs-val').textContent = e.target.value + 'px';
$('fill-opacity').oninput = e => $('fill-op-val').textContent = e.target.value + '%';
$('grid-size').oninput    = e => { $('grid-val').textContent = e.target.value + 'px'; drawGridOverlay(); };
$('show-grid').onchange   = drawGridOverlay;
$('btn-backup').onclick = exportJSON;
$('btn-reset').onclick = () => {
  if (!confirm('Reset session?')) return;
  Storage.del(Storage.KEY); Storage.del(Storage.KEY_CTR);
  toast('Session reset'); updateStorageInfo();
};
function buildPalette(){
  const wrap = $('palette');
  wrap.innerHTML = '';
  PALETTE.forEach(c => {
    const sw = document.createElement('div');
    sw.className = 'swatch';
    sw.style.background = c;
    sw.onclick = () => {
      $('stroke-color').value = c;
      $('fill-color').value = c;
      document.querySelectorAll('.swatch').forEach(s => s.classList.remove('sel'));
      sw.classList.add('sel');
    };
    wrap.appendChild(sw);
  });
}

/* =====================================================================
   26. HEIGHT SYNC
   ===================================================================== */
function syncFrameHeight(){
  try {
    if (window.Streamlit && window.Streamlit.setFrameHeight){
      window.Streamlit.setFrameHeight(document.body.scrollHeight || window.innerHeight);
    }
  } catch(_){}
}
if (typeof ResizeObserver !== 'undefined'){
  new ResizeObserver(syncFrameHeight).observe(document.body);
}
window.addEventListener('resize', syncFrameHeight);
setInterval(syncFrameHeight, 3000);

/* =====================================================================
   27. BOOT
   ===================================================================== */
(async function boot(){
  try {
    Boot.show('Loading graphics library…');
    await loadFabric();

    Boot.show('Initializing canvas…');
    initCanvas();
    tightenSelectionBoxes();
    buildPalette();
    const hint = document.getElementById('drop-hint');
    if (hint) hint.remove();

    setTimeout(() => fitView(), 100);
    Boot.show('Restoring session…');
    setTimeout(() => {
      loadLocal();
      Boot.ready();
      syncSelectionPanel();
      toast('Ready — Ctrl+C / Ctrl+V to copy objects', 'ok');
    }, 200);
  } catch(e){
    console.error('[boot]', e);
    Boot.error('Startup failed',
      `Could not initialize.<br><br><code>${e.message}</code><br><br>
       Refresh · disable ad-blockers · check F12 console.`);
  }
})();
</script>
</body>
</html>
"""

components.html(APP_HTML, height=1000, scrolling=False)
