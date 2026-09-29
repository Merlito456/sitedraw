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
  #boot .err b{color:#fca5a5;display:block;margin-bottom:6px;font-size:1rem}
  #boot .err code{background:#0b1220;padding:2px 6px;border-radius:4px;
    font-family:ui-monospace,monospace;color:#fbbf24}

  #app{display:flex;height:100vh}

  /* ---------- TOP TOOLBAR ---------- */
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
  #topstrip button.active{background:#2563eb;color:#fff;border-color:#3b82f6}
  #topstrip .filelabel{color:#7c8db5;font-size:.72rem;margin-left:auto;
    display:flex;gap:8px;align-items:center}

  /* ---------- LEFT SIDEBAR (tools) ---------- */
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

  /* ---------- STENCIL PANEL ---------- */
  #stencil-panel{position:absolute;top:52px;left:52px;width:260px;
    background:#0f1626;border:1px solid #1f2a44;border-radius:0 0 10px 0;
    z-index:25;max-height:calc(100vh - 60px);overflow-y:auto;
    padding:10px;display:none}
  #stencil-panel.open{display:block}
  #stencil-panel h4{margin:8px 0 6px;font-size:.68rem;text-transform:uppercase;
    letter-spacing:.08em;color:#7c8db5}
  #stencil-panel h4:first-child{margin-top:2px}
  .stencil-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:6px}
  .stencil{background:#131a2b;border:1px solid #1f2a44;border-radius:8px;
    padding:8px 6px;cursor:pointer;transition:.12s;text-align:center;
    color:#c8d3e8;font-size:.7rem;line-height:1.25}
  .stencil:hover{background:#1c2640;border-color:#3b82f6;
    transform:translateY(-1px);box-shadow:0 4px 10px rgba(0,0,0,.3)}
  .stencil .ico{font-size:1.5rem;display:block;margin-bottom:4px}
  .stencil .nm{color:#8b9dc3;font-size:.66rem}

  /* ---------- RIGHT SIDEBAR (properties) ---------- */
  #props{width:280px;background:#0f1626;border-left:1px solid #1f2a44;
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
  .prow .pbtn{flex:1;justify-content:center}
  .prow .pbtn .k{margin-left:4px;font-size:.62rem;color:#7c8db5;
    background:#0b1220;padding:1px 5px;border-radius:4px}

  input[type="color"]{width:100%;height:28px;border:none;background:transparent;
    cursor:pointer;border-radius:6px}
  input[type="range"]{width:100%;accent-color:#6366f1}
  input[type="text"],input[type="number"],select{width:100%;padding:5px 8px;
    border-radius:6px;border:1px solid #2a3a5c;background:#0b1220;
    color:#e2e8f0;font-size:.76rem;font-family:inherit}
  input:focus,select:focus{outline:none;border-color:#6366f1;
    box-shadow:0 0 0 2px rgba(99,102,241,.2)}
  label{font-size:.68rem;color:#8b9dc3;display:flex;
    justify-content:space-between;align-items:center;margin:5px 0 2px}
  label span.val{color:#a5b4fc;font-weight:600}

  .swatches{display:grid;grid-template-columns:repeat(6,1fr);gap:3px;margin-top:4px}
  .swatch{aspect-ratio:1;border-radius:4px;cursor:pointer;
    border:2px solid transparent;transition:.1s}
  .swatch:hover{transform:scale(1.08)}
  .swatch.sel{border-color:#fff;box-shadow:0 0 0 2px #6366f1}

  /* ---------- CANVAS ---------- */
  #stage{flex:1;position:relative;overflow:hidden;
    background:repeating-conic-gradient(#0a1020 0 25%,#0b1220 0 50%) 50%/24px 24px;
    padding-top:44px}
  #canvas-holder{position:absolute;top:44px;left:0;transform-origin:0 0;
    will-change:transform}
  #drop-hint{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);
    display:flex;flex-direction:column;align-items:center;justify-content:center;
    padding:40px 60px;border:3px dashed #2a3a5c;border-radius:20px;
    color:#8b9dc3;font-size:1rem;text-align:center;pointer-events:none;
    z-index:5;max-width:560px}
  #drop-hint b{color:#a5b4fc;font-size:1.15rem;display:block;margin:6px 0}
  #drop-hint .icon{font-size:3.5rem;margin-bottom:8px}
  #drop-hint .sub{font-size:.82rem;color:#66748f;margin-top:8px;line-height:1.5}

  /* ---------- CANVAS FLOATING TOOLBAR (zoom) ---------- */
  #canvastools{position:absolute;bottom:14px;right:300px;display:flex;gap:6px;
    background:rgba(19,26,43,.92);backdrop-filter:blur(12px);
    border:1px solid #2a3a5c;padding:5px;border-radius:10px;z-index:20;
    box-shadow:0 8px 24px rgba(0,0,0,.4)}
  #canvastools button{background:transparent;border:none;color:#8b9dc3;
    padding:5px 10px;border-radius:6px;cursor:pointer;font-size:.76rem;
    font-family:inherit;display:flex;align-items:center;gap:4px;transition:.12s}
  #canvastools button:hover{background:#1c2640;color:#e2e8f0}
  #canvastools button.active{background:#2563eb;color:#fff}
  #zoom-lvl{min-width:52px;justify-content:center;color:#a5b4fc;
    font-family:ui-monospace,monospace;font-size:.7rem}

  #hud{position:absolute;bottom:14px;left:64px;display:flex;gap:6px;
    align-items:center;z-index:10}
  #hud .chip{background:rgba(19,26,43,.92);backdrop-filter:blur(12px);
    border:1px solid #2a3a5c;padding:5px 10px;border-radius:7px;
    font-size:.68rem;color:#a5b4fc;font-family:ui-monospace,monospace}
  #hud .chip.warn{border-color:#f59e0b;color:#fbbf24}
  #hud .chip.err{border-color:#dc2626;color:#fca5a5}

  #toast{position:fixed;bottom:24px;left:50%;
    transform:translateX(-50%) translateY(100px);
    background:#1c2640;border:1px solid #3b4d75;color:#e2e8f0;
    padding:10px 20px;border-radius:10px;font-size:.8rem;
    box-shadow:0 10px 30px rgba(0,0,0,.5);transition:transform .25s ease;
    z-index:100;pointer-events:none;max-width:80vw}
  #toast.show{transform:translateX(-50%) translateY(0)}
  #toast.err{background:#3b1212;border-color:#7f1d1d;color:#fecaca}
  #toast.warn{background:#3b2a12;border-color:#b45309;color:#fde68a}

  #measure{position:fixed;background:#1c2640;border:1px solid #6366f1;
    padding:4px 8px;border-radius:6px;font-size:.72rem;color:#c7d2fe;
    font-family:ui-monospace,monospace;pointer-events:none;z-index:200;
    display:none}
</style>
</head>
<body>

<div id="boot">
  <div class="spinner"></div>
  <div id="boot-msg">Loading Telecom Studio…</div>
  <div id="boot-err" style="display:none" class="err"></div>
</div>

<div id="app" style="display:none">

  <!-- ==================== TOP TOOLBAR ==================== -->
  <div id="topstrip">
    <div class="logo">📡 Telecom Site Studio</div>
    <div class="sep"></div>
    <button id="tb-new" title="New site plan">🆕 New</button>
    <button id="tb-open" title="Open image">📁 Open Image</button>
    <button id="tb-paste" title="Paste">📋 Paste</button>
    <button id="tb-load-json" title="Load layout">📂 Load Layout</button>
    <button id="tb-save-json" title="Save layout">💾 Save Layout</button>
    <div class="sep"></div>
    <button id="tb-undo" title="Undo Ctrl+Z">↩️</button>
    <button id="tb-redo" title="Redo Ctrl+Y">↪️</button>
    <div class="sep"></div>
    <button id="tb-zoom-fit" title="Fit (F)">🎯 Fit</button>
    <button id="tb-zoom-in" title="Zoom in">＋</button>
    <button id="tb-zoom-out" title="Zoom out">－</button>
    <div class="sep"></div>
    <button id="tb-export-png" title="Export PNG">🖼️ PNG</button>
    <button id="tb-print" title="Print (A3)">🖨️ Print</button>
    <div class="filelabel">
      <span id="file-label">Untitled Site Plan</span>
    </div>
  </div>

  <!-- ==================== LEFT TOOL SIDEBAR ==================== -->
  <aside id="sidebar">
    <button class="tbtn active" data-tool="select" title="">
      <span>🖱️</span><span class="tip">Select / Move (V)</span>
    </button>
    <button class="tbtn" data-tool="pan">
      <span>✋</span><span class="tip">Pan view (H)</span>
    </button>
    <div class="sep"></div>
    <button class="tbtn" id="tbtn-stencil">
      <span>📦</span><span class="tip">Telecom Stencils</span>
    </button>
    <button class="tbtn" data-tool="pen">
      <span>✏️</span><span class="tip">Freehand (P)</span>
    </button>
    <button class="tbtn" data-tool="line">
      <span>📏</span><span class="tip">Line (L)</span>
    </button>
    <button class="tbtn" data-tool="polyline">
      <span>↗️</span><span class="tip">Polyline — click to add points</span>
    </button>
    <button class="tbtn" data-tool="rect">
      <span>⬛</span><span class="tip">Rectangle (R)</span>
    </button>
    <button class="tbtn" data-tool="circle">
      <span>⭕</span><span class="tip">Circle (C)</span>
    </button>
    <button class="tbtn" data-tool="text">
      <span>🔤</span><span class="tip">Text (T)</span>
    </button>
    <div class="sep"></div>
    <button class="tbtn" data-tool="dim-h">
      <span>↔️</span><span class="tip">Horizontal dimension</span>
    </button>
    <button class="tbtn" data-tool="dim-v">
      <span>↕️</span><span class="tip">Vertical dimension</span>
    </button>
    <div class="sep"></div>
    <button class="tbtn" data-tool="erase">
      <span>🧹</span><span class="tip">Eraser (E)</span>
    </button>
  </aside>

  <!-- ==================== STENCIL PANEL ==================== -->
  <div id="stencil-panel">
    <h4>🚪 Gate & Access</h4>
    <div class="stencil-grid">
      <div class="stencil" data-stencil="gate_2door">
        <span class="ico">🚪</span><span class="nm">Gate (2-Door)</span>
      </div>
      <div class="stencil" data-stencil="fence">
        <span class="ico">🔲</span><span class="nm">Boundary Fence</span>
      </div>
    </div>

    <h4>🏢 Cabin / Shelter</h4>
    <div class="stencil-grid">
      <div class="stencil" data-stencil="cabin">
        <span class="ico">🏠</span><span class="nm">Cabin / Shelter</span>
      </div>
      <div class="stencil" data-stencil="stairs">
        <span class="ico">🪜</span><span class="nm">Cement Stairs</span>
      </div>
    </div>

    <h4>🗄️ Cabinets</h4>
    <div class="stencil-grid">
      <div class="stencil" data-stencil="odc">
        <span class="ico">🗄️</span><span class="nm">ODC Cabinet</span>
      </div>
      <div class="stencil" data-stencil="cab1">
        <span class="ico">🗃️</span><span class="nm">1-Bay Cabinet</span>
      </div>
      <div class="stencil" data-stencil="cab2">
        <span class="ico">🗃️</span><span class="nm">2-Bay Cabinet</span>
      </div>
      <div class="stencil" data-stencil="cab3">
        <span class="ico">🗃️</span><span class="nm">3-Bay Cabinet</span>
      </div>
    </div>

    <h4>📡 Tower</h4>
    <div class="stencil-grid">
      <div class="stencil" data-stencil="tower4">
        <span class="ico">📡</span><span class="nm">4-Leg Tower</span>
      </div>
      <div class="stencil" data-stencil="tower3">
        <span class="ico">📡</span><span class="nm">3-Leg Tower</span>
      </div>
      <div class="stencil" data-stencil="towerfoot">
        <span class="ico">🔩</span><span class="nm">Tower Footprint</span>
      </div>
      <div class="stencil" data-stencil="guy">
        <span class="ico">⚓</span><span class="nm">Guy Anchor</span>
      </div>
    </div>

    <h4>⚡ Power</h4>
    <div class="stencil-grid">
      <div class="stencil" data-stencil="genset">
        <span class="ico">🔌</span><span class="nm">Generator + Pad</span>
      </div>
      <div class="stencil" data-stencil="fuel">
        <span class="ico">⛽</span><span class="nm">Fuel Tank</span>
      </div>
      <div class="stencil" data-stencil="transformer">
        <span class="ico">⚡</span><span class="nm">Transformer</span>
      </div>
      <div class="stencil" data-stencil="battery">
        <span class="ico">🔋</span><span class="nm">Battery Bank</span>
      </div>
    </div>

    <h4>❄️ Cooling</h4>
    <div class="stencil-grid">
      <div class="stencil" data-stencil="aircon">
        <span class="ico">❄️</span><span class="nm">Air Conditioner</span>
      </div>
    </div>

    <h4>🛣️ Cable Infrastructure</h4>
    <div class="stencil-grid">
      <div class="stencil" data-stencil="cabletray">
        <span class="ico">🛤️</span><span class="nm">Cable Tray</span>
      </div>
      <div class="stencil" data-stencil="openrack">
        <span class="ico">🗂️</span><span class="nm">Open Rack</span>
      </div>
      <div class="stencil" data-stencil="hframe">
        <span class="ico">🪜</span><span class="nm">H-Frame</span>
      </div>
    </div>

    <h4>🌱 Site Surface</h4>
    <div class="stencil-grid">
      <div class="stencil" data-stencil="grass">
        <span class="ico">🌱</span><span class="nm">Grass Area</span>
      </div>
      <div class="stencil" data-stencil="cement">
        <span class="ico">⬜</span><span class="nm">Cement Floor</span>
      </div>
      <div class="stencil" data-stencil="gravel">
        <span class="ico">🪨</span><span class="nm">Gravel Pad</span>
      </div>
      <div class="stencil" data-stencil="wall">
        <span class="ico">🧱</span><span class="nm">Wall</span>
      </div>
    </div>
  </div>

  <!-- ==================== RIGHT PROPERTIES SIDEBAR ==================== -->
  <aside id="props">
    <h3>🎨 Style</h3>
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

    <h3>🔤 Text</h3>
    <div class="psection">
      <input type="text" id="text-value" value="SITE" maxlength="80">
      <label>Font size <span class="val" id="fs-val">16px</span></label>
      <input type="range" id="font-size" min="8" max="72" value="16">
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

    <h3>🔧 Selection Actions</h3>
    <div class="psection">
      <div class="prow">
        <button class="pbtn" id="btn-dup">📋 <span>Copy</span></button>
        <button class="pbtn" id="btn-del">🗑️ <span>Delete</span></button>
      </div>
      <div class="prow">
        <button class="pbtn" id="btn-rot90">↻ <span>Rot 90</span></button>
        <button class="pbtn" id="btn-flip">⇋ <span>Flip</span></button>
      </div>
      <button class="pbtn" id="btn-clear">💥 <span>Clear drawings</span></button>
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
      <div><b style="color:#a5b4fc">Zoom:</b> Ctrl + scroll</div>
      <div><b style="color:#a5b4fc">Pan:</b> Space + drag or H</div>
      <div><b style="color:#a5b4fc">Fit:</b> F</div>
      <div><b style="color:#a5b4fc">Ortho:</b> Shift while drawing</div>
      <div><b style="color:#a5b4fc">Duplicate:</b> Alt + drag</div>
      <div><b style="color:#a5b4fc">Diag:</b> Ctrl+Shift+D</div>
    </div>
  </aside>

  <!-- ==================== CANVAS STAGE ==================== -->
  <main id="stage">
    <div id="canvas-holder"><canvas id="c"></canvas></div>

    <div id="drop-hint">
      <div class="icon">📐</div>
      <b>Start a site layout</b>
      <div class="sub">
        Drop or paste a site plan image ·<br>
        or open the <b style="color:#a5b4fc">📦 Stencil library</b> to place equipment ·<br>
        or draw from scratch with the tools on the left
      </div>
    </div>

    <div id="canvastools">
      <button id="ct-zoom-fit" title="Fit (F)">🎯</button>
      <button id="ct-zoom-out">－</button>
      <span id="zoom-lvl" style="display:flex;align-items:center">100%</span>
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
   0. ERROR BOUNDARY + BOOT
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
   1. FABRIC LOADER (with fallback CDNs)
   ===================================================================== */
const FABRIC_CDNS = [
  'https://cdn.jsdelivr.net/npm/fabric@5.3.0/dist/fabric.min.js',
  'https://unpkg.com/fabric@5.3.0/dist/fabric.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/fabric.js/5.3.0/fabric.min.js',
];
function loadFabric(i = 0){
  return new Promise((resolve, reject) => {
    if (window.fabric) return resolve();
    if (i >= FABRIC_CDNS.length) return reject(new Error('All CDNs failed'));
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
  KEY: 'telecom_site_v1',
  KEY_CTR: 'telecom_site_ctr_v1',
  available(){
    try { const k = '__t'+Math.random(); localStorage.setItem(k,'1');
          localStorage.removeItem(k); return true; } catch(_) { return false; }
  },
  get(k){ try { return localStorage.getItem(k); } catch(_) { return null; } },
  set(k, v){ try { localStorage.setItem(k, v); return true; } catch(e){ return false; } },
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
   3. GLOBAL STATE
   ===================================================================== */
let canvas;
let currentTool = 'select';
let pendingStencil = null;     // stencil id awaiting click to place
let drawing = false, startPt = null, activeShape = null, drawMoved = false;
let polyPoints = [];           // polyline in-progress
let polyPreview = null;
let undoStack = [], redoStack = [];
let cableCounter = 0;
let view = { zoom: 1, x: 0, y: 0 };
let spaceDown = false, panning = false, panStart = null;
let pasteLock = 0;
let shiftAxis = null, shiftOrigin = null;
let ortho = false;
let showDims = true;
let fileName = 'Untitled Site Plan';
const CW = 1600, CH = 1000;

const PALETTE = ['#334155','#64748b','#94a3b8','#cbd5e1','#f8fafc','#000000',
                 '#dc2626','#ea580c','#ca8a04','#16a34a','#0891b2','#2563eb',
                 '#7c3aed','#db2777','#a16207','#0f766e','#475569','#a3a3a3'];

/* =====================================================================
   4. FABRIC SETTINGS (Option A tight selection boxes)
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
   5. ★ TELECOM STENCIL LIBRARY
   Each factory returns an array of fabric objects (groupable) OR a single
   fabric.Group. Dimensions in metres are converted with M2PX below.
   ===================================================================== */
const M2PX = 20;   // 1 metre = 20 px on default canvas

function mkLine(x1,y1,x2,y2, opt){
  return new fabric.Line([x1,y1,x2,y2], Object.assign({
    stroke: '#1e293b', strokeWidth: 1.5, selectable: true, evented: true,
    strokeLineCap: 'round'
  }, opt || {}));
}
function mkRect(x,y,w,h, opt){
  return new fabric.Rect(Object.assign({
    left: x, top: y, width: w, height: h,
    fill: 'rgba(148,163,184,0.4)', stroke: '#1e293b', strokeWidth: 1.5,
    selectable: true, evented: true
  }, opt || {}));
}
function mkCircle(cx,cy,r, opt){
  return new fabric.Circle(Object.assign({
    left: cx - r, top: cy - r, radius: r,
    fill: 'rgba(148,163,184,0.4)', stroke: '#1e293b', strokeWidth: 1.5,
    selectable: true, evented: true, originX: 'left', originY: 'top'
  }, opt || {}));
}
function mkText(s, x, y, size, opt){
  return new fabric.IText(s, Object.assign({
    left: x, top: y, fontSize: size || 11,
    fill: '#0f172a', fontFamily: 'system-ui, sans-serif',
    selectable: true, evented: true
  }, opt || {}));
}
function mkGroup(objs, label){
  const g = new fabric.Group(objs, { selectable: true, evented: true });
  if (label) g._stencilLabel = label;
  return g;
}

/* ---- Stencil factories (dimensions in metres → px via M2PX) ---- */
const STENCILS = {

  /* ---------- GATE & FENCE ---------- */
  gate_2door(){
    const W = 4*M2PX, H = 0.4*M2PX;
    const bg = mkRect(0, 0, W, H, { fill: '#fde68a', stroke: '#a16207' });
    const l1 = mkLine(0, 0, 0, H, { stroke:'#a16207', strokeWidth:2 });
    const l2 = mkLine(W, 0, W, H, { stroke:'#a16207', strokeWidth:2 });
    const m1 = mkLine(W/2, 0, W/2, H, { stroke:'#a16207', strokeWidth:1, strokeDashArray:[2,2] });
    const swing1 = mkLine(0, H/2, W/2, H/2, { stroke:'#a16207', strokeWidth:1, strokeDashArray:[3,2] });
    const swing2 = mkLine(W/2, H/2, W, H/2, { stroke:'#a16207', strokeWidth:1, strokeDashArray:[3,2] });
    const t = mkText('GATE', W/2 - 18, H/2 - 6, 10, { fill:'#7c2d12', fontWeight:'700' });
    return mkGroup([bg, l1, l2, m1, swing1, swing2, t], 'Gate');
  },
  fence(){
    const W = 6*M2PX, H = 8;
    const g = [];
    for (let x = 0; x <= W; x += 8){
      g.push(mkLine(x, 0, x, H, { stroke: '#475569', strokeWidth: 1 }));
    }
    g.push(mkLine(0, H/2, W, H/2, { stroke: '#475569', strokeWidth: 1 }));
    return mkGroup(g, 'Fence');
  },

  /* ---------- CABIN / SHELTER ---------- */
  cabin(){
    const W = 4*M2PX, H = 3*M2PX;
    const bg = mkRect(0, 0, W, H, { fill:'#e2e8f0', stroke:'#334155', strokeWidth:2 });
    const door = mkRect(W-24, H-20, 20, 18, { fill:'#94a3b8', stroke:'#334155' });
    const t = mkText('SHELTER', 8, 8, 11, { fontWeight:'700', fill:'#0f172a' });
    const dimW = mkText(`${4.0}m`, W/2 - 12, -16, 9, { fill:'#0891b2' });
    const dimH = mkText(`${3.0}m`, W + 4, H/2 - 4, 9, { fill:'#0891b2' });
    return mkGroup([bg, door, t, dimW, dimH], 'Shelter');
  },
  stairs(){
    const steps = 8, w = 40, h = 8;
    const g = [];
    for (let i = 0; i < steps; i++){
      g.push(mkRect(0, i*h, w - i*3, h, { fill:'#cbd5e1', stroke:'#475569' }));
    }
    const t = mkText('STAIRS', 6, steps*h + 4, 10, { fontWeight:'700' });
    g.push(t);
    return mkGroup(g, 'Stairs');
  },

  /* ---------- CABINETS ---------- */
  odc(){
    const W = 1.2*M2PX, H = 2.2*M2PX;
    return mkGroup([
      mkRect(0, 0, W, H, { fill:'#f1f5f9', stroke:'#0f172a', strokeWidth:2 }),
      mkRect(2, 2, W-4, H-4, { fill:'transparent', stroke:'#475569', strokeDashArray:[3,2] }),
      mkText('ODC', W/2-14, H/2-6, 10, { fontWeight:'700' }),
    ], 'ODC');
  },
  cab1(){
    const W = 0.6*M2PX, H = 2.2*M2PX;
    return mkGroup([
      mkRect(0, 0, W, H, { fill:'#e2e8f0', stroke:'#334155', strokeWidth:2 }),
      mkText('1B', W/2-8, H/2-6, 9, { fontWeight:'700' }),
    ], '1-Bay');
  },
  cab2(){
    const W = 1.2*M2PX, H = 2.2*M2PX;
    return mkGroup([
      mkRect(0, 0, W, H, { fill:'#e2e8f0', stroke:'#334155', strokeWidth:2 }),
      mkLine(W/2, 0, W/2, H, { stroke:'#334155', strokeWidth:1 }),
      mkText('2B', W/2-10, H/2-6, 9, { fontWeight:'700' }),
    ], '2-Bay');
  },
  cab3(){
    const W = 1.8*M2PX, H = 2.2*M2PX;
    return mkGroup([
      mkRect(0, 0, W, H, { fill:'#e2e8f0', stroke:'#334155', strokeWidth:2 }),
      mkLine(W/3, 0, W/3, H, { stroke:'#334155', strokeWidth:1 }),
      mkLine(2*W/3, 0, 2*W/3, H, { stroke:'#334155', strokeWidth:1 }),
      mkText('3B', W/2-10, H/2-6, 9, { fontWeight:'700' }),
    ], '3-Bay');
  },

  /* ---------- TOWER ---------- */
  tower4(){
    // Classic 4-leg self-support tower footprint + legs at corners
    const S = 4*M2PX;                 // tower base 4m x 4m
    const g = [];
    // Outer square
    g.push(mkRect(0, 0, S, S, { fill:'rgba(226,232,240,0.35)',
      stroke:'#0f172a', strokeWidth:2 }));
    // X braces
    g.push(mkLine(0, 0, S, S, { stroke:'#0f172a', strokeWidth:1, strokeDashArray:[4,3] }));
    g.push(mkLine(S, 0, 0, S, { stroke:'#0f172a', strokeWidth:1, strokeDashArray:[4,3] }));
    // Corner leg pads
    const legPads = [[0,0],[S,0],[0,S],[S,S]];
    legPads.forEach(([x,y]) => {
      g.push(mkCircle(x, y, 6, { fill:'#334155', stroke:'#0f172a', strokeWidth:1.5 }));
    });
    // Centre mast
    g.push(mkCircle(S/2, S/2, 8, { fill:'#1e293b', stroke:'#0f172a' }));
    // Labels
    g.push(mkText('4-LEG TOWER', S/2-40, -18, 11, { fontWeight:'700' }));
    g.push(mkText('4.0m', S/2-12, S + 4, 9, { fill:'#0891b2' }));
    return mkGroup(g, '4-Leg Tower');
  },
  tower3(){
    const S = 3.5*M2PX;
    const g = [];
    // Triangle footprint
    const A = { x: S/2, y: 0 }, B = { x: 0, y: S*0.87 }, C = { x: S, y: S*0.87 };
    g.push(mkLine(A.x, A.y, B.x, B.y, { stroke:'#0f172a', strokeWidth:2 }));
    g.push(mkLine(B.x, B.y, C.x, C.y, { stroke:'#0f172a', strokeWidth:2 }));
    g.push(mkLine(C.x, C.y, A.x, A.y, { stroke:'#0f172a', strokeWidth:2 }));
    // Legs
    [A,B,C].forEach(p => g.push(mkCircle(p.x, p.y, 6,
      { fill:'#334155', stroke:'#0f172a', strokeWidth:1.5 })));
    g.push(mkText('3-LEG TOWER', S/2-42, S*0.87 + 8, 10, { fontWeight:'700' }));
    return mkGroup(g, '3-Leg Tower');
  },
  towerfoot(){
    // Single tower leg footing (concrete pad + bolts)
    const S = 1.2*M2PX;
    const g = [
      mkRect(0, 0, S, S, { fill:'#cbd5e1', stroke:'#0f172a', strokeWidth:1.5 }),
      mkCircle(S/2, S/2, 6, { fill:'#334155', stroke:'#0f172a' }),
      mkLine(S/2-8, S/2, S/2+8, S/2, { stroke:'#0f172a', strokeWidth:1 }),
      mkLine(S/2, S/2-8, S/2, S/2+8, { stroke:'#0f172a', strokeWidth:1 }),
    ];
    return mkGroup(g, 'Footing');
  },
  guy(){
    const S = 1*M2PX;
    return mkGroup([
      mkCircle(S/2, S/2, S/2 - 2, { fill:'#fef3c7', stroke:'#a16207', strokeWidth:1.5 }),
      mkText('G', S/2-5, S/2-5, 11, { fontWeight:'700', fill:'#a16207' }),
    ], 'Guy Anchor');
  },

  /* ---------- POWER ---------- */
  genset(){
    const W = 3.5*M2PX, H = 1.5*M2PX;   // generator enclosure
    const pad = 4*M2PX, padH = 2*M2PX;  // concrete base pad
    const g = [
      mkRect(0, 0, pad, padH, { fill:'#cbd5e1', stroke:'#334155',
        strokeWidth:1, strokeDashArray:[3,2] }),
      mkRect((pad - W)/2, (padH - H)/2, W, H,
        { fill:'#fef3c7', stroke:'#a16207', strokeWidth:2 }),
      mkText('GENSET', (pad - W)/2 + 8, (padH - H)/2 + H/2 - 6, 11,
        { fontWeight:'700', fill:'#7c2d12' }),
      mkText(`${(pad/M2PX).toFixed(1)}m`, pad/2 - 12, padH + 4, 9, { fill:'#0891b2' }),
    ];
    return mkGroup(g, 'Generator');
  },
  fuel(){
    const R = 0.6*M2PX;
    const g = [
      mkCircle(R, R, R, { fill:'#fecaca', stroke:'#991b1b', strokeWidth:2 }),
      mkCircle(R, R, R*0.6, { fill:'transparent', stroke:'#991b1b',
        strokeWidth:1, strokeDashArray:[3,2] }),
      mkText('FUEL', R - 14, R - 5, 10, { fontWeight:'700', fill:'#7f1d1d' }),
    ];
    return mkGroup(g, 'Fuel Tank');
  },
  transformer(){
    const W = 1.5*M2PX, H = 1.5*M2PX;
    const g = [
      mkRect(0, 0, W, H, { fill:'#fef3c7', stroke:'#78350f', strokeWidth:2 }),
      mkText('TX', W/2-10, H/2-6, 12, { fontWeight:'700', fill:'#78350f' }),
      mkText('KVA', W/2-14, H/2 + 8, 8, { fill:'#78350f' }),
    ];
    return mkGroup(g, 'Transformer');
  },
  battery(){
    const W = 2.5*M2PX, H = 0.8*M2PX;
    const cells = [];
    const cw = W / 4;
    for (let i = 0; i < 4; i++){
      cells.push(mkRect(i*cw + 1, 1, cw - 2, H - 2,
        { fill:'#dbeafe', stroke:'#1e3a8a' }));
    }
    cells.push(mkText('BATTERY BANK', 4, H/2 - 5, 9, { fontWeight:'700', fill:'#1e3a8a' }));
    return mkGroup(cells, 'Battery');
  },

  /* ---------- COOLING ---------- */
  aircon(){
    const W = 1.0*M2PX, H = 0.6*M2PX;
    const g = [
      mkRect(0, 0, W, H, { fill:'#e0f2fe', stroke:'#0369a1', strokeWidth:2 }),
      mkText('AC', W/2-8, H/2-5, 10, { fontWeight:'700', fill:'#0c4a6e' }),
    ];
    return mkGroup(g, 'Aircon');
  },

  /* ---------- CABLE INFRASTRUCTURE ---------- */
  cabletray(){
    const W = 4*M2PX, H = 0.4*M2PX;
    const g = [
      mkRect(0, 0, W, H, { fill:'#e2e8f0', stroke:'#475569', strokeWidth:1.5 }),
    ];
    for (let x = 4; x < W; x += 6){
      g.push(mkLine(x, 0, x, H, { stroke:'#475569', strokeWidth:0.8 }));
    }
    g.push(mkText('CABLE TRAY', 8, H + 4, 9, { fontWeight:'700', fill:'#334155' }));
    return mkGroup(g, 'Cable Tray');
  },
  openrack(){
    const W = 0.6*M2PX, H = 2.2*M2PX;
    const g = [
      mkRect(0, 0, W, H, { fill:'#f8fafc', stroke:'#0f172a', strokeWidth:2 }),
      mkLine(4, 4, W-4, 4, { stroke:'#334155', strokeWidth:1 }),
      mkLine(4, H-4, W-4, H-4, { stroke:'#334155', strokeWidth:1 }),
      mkText('RACK', W/2-14, H/2-5, 8, { fontWeight:'700' }),
    ];
    return mkGroup(g, 'Open Rack');
  },
  hframe(){
    const W = 2*M2PX, H = 2.5*M2PX;
    const g = [
      mkLine(6, 0, 6, H, { stroke:'#334155', strokeWidth:3 }),
      mkLine(W-6, 0, W-6, H, { stroke:'#334155', strokeWidth:3 }),
      mkLine(6, H/2, W-6, H/2, { stroke:'#334155', strokeWidth:3 }),
      mkLine(6, H*0.15, W-6, H*0.15, { stroke:'#334155', strokeWidth:1.5 }),
      mkLine(6, H*0.85, W-6, H*0.85, { stroke:'#334155', strokeWidth:1.5 }),
      mkText('H-FRAME', W/2-24, H + 4, 9, { fontWeight:'700' }),
    ];
    return mkGroup(g, 'H-Frame');
  },

  /* ---------- SITE SURFACE ---------- */
  grass(){
    const W = 8*M2PX, H = 6*M2PX;
    const g = [];
    for (let i = 0; i < 60; i++){
      const x = Math.random()*W, y = Math.random()*H;
      g.push(mkLine(x, y, x + 3, y - 5, { stroke:'#65a30d', strokeWidth:1 }));
      g.push(mkLine(x + 3, y, x + 6, y - 4, { stroke:'#84cc16', strokeWidth:1 }));
    }
    g.push(mkRect(0, 0, W, H, {
      fill:'rgba(132,204,22,0.10)', stroke:'#65a30d',
      strokeWidth:1, strokeDashArray:[4,3], selectable:true
    }));
    g.push(mkText('GRASS', W/2-22, H/2-6, 11,
      { fontWeight:'700', fill:'#3f6212', opacity:0.7 }));
    return mkGroup(g, 'Grass');
  },
  cement(){
    const W = 8*M2PX, H = 6*M2PX;
    const g = [
      mkRect(0, 0, W, H, {
        fill:'rgba(203,213,225,0.5)', stroke:'#64748b',
        strokeWidth:1.5, strokeDashArray:[6,3]
      }),
      mkText('CEMENT', W/2-30, H/2-6, 12,
        { fontWeight:'700', fill:'#475569', opacity:0.65 }),
    ];
    return mkGroup(g, 'Cement Floor');
  },
  gravel(){
    const W = 6*M2PX, H = 4*M2PX;
    const g = [];
    for (let i = 0; i < 90; i++){
      const x = Math.random()*W, y = Math.random()*H;
      const r = 1 + Math.random()*2;
      g.push(mkCircle(x, y, r,
        { fill:'#a8a29e', stroke:'#78716c', strokeWidth:0.5 }));
    }
    g.push(mkRect(0, 0, W, H, {
      fill:'rgba(168,162,158,0.2)', stroke:'#78716c', strokeWidth:1
    }));
    return mkGroup(g, 'Gravel');
  },
  wall(){
    const W = 5*M2PX, H = 0.4*M2PX;
    const g = [
      mkRect(0, 0, W, H, { fill:'#a8a29e', stroke:'#44403c', strokeWidth:2 }),
    ];
    for (let x = 0; x < W; x += 8){
      g.push(mkLine(x, 0, x, H, { stroke:'#44403c', strokeWidth:0.5 }));
    }
    return mkGroup(g, 'Wall');
  },
};

/* =====================================================================
   6. CANVAS INIT
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
      opt.target.set({ perPixelTargetFind: true, padding: 2 });
    }
    markDirty(); refreshPanels();
  });
  canvas.on('object:modified', () => { markDirty(); refreshPanels(); });
  canvas.on('object:removed',  () => { refreshPanels(); });
  canvas.on('selection:created', refreshPanels);
  canvas.on('selection:updated', refreshPanels);
  canvas.on('selection:cleared', refreshPanels);

  canvas.on('mouse:dblclick', opt => {
    const t = opt.target;
    if (t && (t.type === 'i-text' || t.type === 'text' || t.type === 'textbox')){
      t.enterEditing(); t.selectAll();
    }
  });

  drawGridOverlay();
}

/* =====================================================================
   7. GRID
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
  cx.moveTo(size - .5, 0); cx.lineTo(size - .5, size);
  cx.moveTo(0, size - .5); cx.lineTo(size, size - .5);
  cx.stroke();
  canvas.setBackgroundColor({ source: pc, repeat: 'repeat' },
                            canvas.renderAll.bind(canvas));
}

/* =====================================================================
   8. SNAP
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
      if (o === activeShape || o.isBackground) continue;
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
   9. MAIN POINTER HANDLERS
   ===================================================================== */
function onDown(opt){
  // Pan
  if (spaceDown || currentTool === 'pan'){
    panning = true;
    panStart = { x: opt.e.clientX, y: opt.e.clientY };
    return;
  }

  // Eraser
  if (currentTool === 'erase'){
    if (opt.target && !opt.target.isBackground){ canvas.remove(opt.target); toast('Erased'); }
    return;
  }

  // ★ STENCIL PLACEMENT — highest priority
  if (pendingStencil){
    const p = canvas.getPointer(opt.e);
    placeStencil(pendingStencil, p.x, p.y);
    return;
  }

  // Selection
  if (currentTool === 'select'){
    if (opt.target && opt.e.altKey && !opt.target.isBackground){
      const orig = opt.target;
      orig.clone(c => {
        c.set({ left: orig.left, top: orig.top, evented: true, selectable: true,
                perPixelTargetFind: true, padding: 2 });
        canvas.add(c);
        canvas.setActiveObject(c);
        canvas.renderAll();
        toast('Duplicated');
      });
    }
    return;
  }

  // Gate: don't draw on existing objects
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
  const fBase = $('fill-color').value;
  const fColor = fEnabled ? hexWithAlpha(fBase, fOpacity) : 'transparent';

  // Polyline special handling
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

  drawing = true; drawMoved = false; startPt = p;
  shiftAxis = null; shiftOrigin = p;

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
    const label = new fabric.IText($('text-value').value || 'TEXT', {
      left:p.x, top:p.y, fill:sColor,
      fontSize: parseInt($('font-size').value),
      fontFamily:'system-ui, sans-serif', fontWeight:'600',
    });
    canvas.add(label);
    canvas.setActiveObject(label);
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

  // Polyline preview
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

  // Shift / Ortho axis-lock
  const orthoOn = opt.e.shiftKey || $('ortho').checked || ortho;
  if (orthoOn && (currentTool === 'line' || currentTool === 'rect' ||
      currentTool === 'circle' || currentTool === 'dim-h' || currentTool === 'dim-v')){
    const dx = Math.abs(p.x - startPt.x);
    const dy = Math.abs(p.y - startPt.y);
    if (currentTool === 'dim-h' || currentTool === 'dim-v'){
      if (currentTool === 'dim-h') p = { x: p.x, y: startPt.y };
      else                         p = { x: startPt.x, y: p.y };
    } else {
      if (!shiftAxis) shiftAxis = dx > dy ? 'x' : 'y';
      if (shiftAxis === 'x') p = { x: p.x, y: startPt.y };
      else                    p = { x: startPt.x, y: p.y };
    }
  } else if (!orthoOn){
    shiftAxis = null;
  }

  if (!drawMoved && Math.hypot(p.x - startPt.x, p.y - startPt.y) > 6){
    drawMoved = true;
  }

  if (currentTool === 'pen'){
    activeShape.path.push(['L', p.x, p.y]);
    activeShape.dirty = true;
  } else if (currentTool === 'line' || currentTool === 'dim-h' || currentTool === 'dim-v'){
    activeShape.set({ x2: p.x, y2: p.y });
  } else if (currentTool === 'rect'){
    activeShape.set({
      left: Math.min(startPt.x, p.x), top: Math.min(startPt.y, p.y),
      width: Math.abs(p.x - startPt.x), height: Math.abs(p.y - startPt.y),
    });
  } else if (currentTool === 'circle'){
    const r = Math.hypot(p.x - startPt.x, p.y - startPt.y);
    activeShape.set({ left: startPt.x - r, top: startPt.y - r, radius: r });
  }

  // Live measurement
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

  // Reject tiny geometry
  try {
    if (activeShape.type === 'line'){
      const len = Math.hypot(activeShape.x2 - activeShape.x1,
                             activeShape.y2 - activeShape.y1);
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
  canvas.setActiveObject(activeShape);

  // Auto measurement label on lines/dims
  if (showDims && (activeShape.type === 'line' ||
      activeShape._isDimension)){
    addDimensionLabel(activeShape);
  }
  if (activeShape._isDimension){
    activeShape.set({ stroke:'#0891b2', strokeDashArray: null });
  }

  activeShape = null; shiftAxis = null;
  canvas.requestRenderAll();
  markDirty(); refreshPanels();
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
    padding: 2, selectable: true, evented: true,
    angle: (Math.abs(angle) > 90 ? angle + 180 : angle),
  });
  txt._isAnnotation = true;
  canvas.add(txt);
}

/* =====================================================================
   10. STENCIL PLACEMENT
   ===================================================================== */
function placeStencil(id, x, y){
  const fn = STENCILS[id];
  if (!fn){ toast('Unknown stencil: ' + id, 'err'); pendingStencil = null; return; }
  try {
    const grp = fn();
    grp.set({
      left: x, top: y,
      originX: 'center', originY: 'center',
      perPixelTargetFind: true, padding: 2,
    });
    canvas.add(grp);
    canvas.setActiveObject(grp);
    canvas.renderAll();
    toast('Placed: ' + id.replace(/_/g, ' '));
  } catch(e){
    toast('Stencil failed: ' + e.message, 'err');
  }
  pendingStencil = null;
  // Auto-return to select
  setTool('select');
  // Close stencil panel
  $('stencil-panel').classList.remove('open');
}

/* =====================================================================
   11. TOOL SWITCHING
   ===================================================================== */
function setTool(tool){
  // Cancel polyline in progress
  if (currentTool === 'polyline' && polyPreview){
    finalizePolyline();
  }
  pendingStencil = null;
  currentTool = tool;
  document.querySelectorAll('.tbtn[data-tool]').forEach(b =>
    b.classList.toggle('active', b.dataset.tool === tool));
  canvas.selection = tool === 'select';
  canvas.forEachObject(o => { o.evented = true; });
  document.body.style.cursor = (tool === 'select') ? 'default'
    : (tool === 'pan') ? 'grab' : 'crosshair';
  if (tool === 'polyline'){
    toast('Polyline: click points, double-click or Esc to finish');
  }
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
  polyPreview.set({ selectable:true, evented:true });
  canvas.setActiveObject(polyPreview);
  canvas.requestRenderAll();
  markDirty(); refreshPanels();
  polyPreview = null; polyPoints = [];
  toast('Polyline finished');
}

/* =====================================================================
   12. STENCIL PANEL TOGGLE
   ===================================================================== */
$('tbtn-stencil').onclick = () => {
  $('stencil-panel').classList.toggle('open');
};
document.querySelectorAll('.stencil').forEach(el => {
  el.onclick = () => {
    const id = el.dataset.stencil;
    pendingStencil = id;
    toast(`Click on canvas to place: ${id.replace(/_/g,' ')}`);
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

/* =====================================================================
   14. HISTORY
   ===================================================================== */
const MAX_HISTORY = 80, MAX_BYTES = 4_000_000;
function serialize(){
  try {
    return JSON.stringify({
      v: 1,
      canvas: { w: canvas.getWidth(), h: canvas.getHeight() },
      fabric: canvas.toJSON(['selectable','evented','isBackground',
                             '_isCable','_isAnnotation','_isDimension']),
    });
  } catch(e){ return '{"v":1,"fabric":{"objects":[]}}'; }
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
        o.set({ perPixelTargetFind: true, padding: 2 });
      });
      canvas.renderAll();
      refreshPanels();
    });
  } catch(e){ toast('Restore failed: ' + e.message, 'err'); }
}

/* =====================================================================
   15. ACTIONS
   ===================================================================== */
function deleteSel(){
  const objs = canvas.getActiveObjects();
  if (!objs.length){ toast('Nothing selected', 'warn'); return; }
  objs.forEach(o => canvas.remove(o));
  canvas.discardActiveObject();
  refreshPanels(); toast('Deleted ' + objs.length);
}
function duplicateSel(){
  const objs = canvas.getActiveObjects();
  if (!objs.length){ toast('Nothing selected', 'warn'); return; }
  objs.forEach(o => {
    o.clone(c => {
      c.set({ left:(o.left||0)+20, top:(o.top||0)+20,
              perPixelTargetFind:true, padding:2 });
      canvas.add(c);
    });
  });
  canvas.discardActiveObject();
  refreshPanels(); toast('Duplicated');
}
function rotate90(){
  const o = canvas.getActiveObject();
  if (!o){ toast('Select an object', 'warn'); return; }
  o.rotate((o.angle || 0) + 90);
  o.setCoords();
  canvas.renderAll();
  markDirty();
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
  refreshPanels(); toast('Cleared');
}

/* =====================================================================
   16. IMAGE LOADING
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
        selectable:false, evented:false, isBackground:true,
        opacity: 0.6,
      });
      canvas.setWidth(img.width * s);
      canvas.setHeight(img.height * s);
      canvas.setBackgroundImage(img, canvas.renderAll.bind(canvas));
      $('drop-hint').style.display = 'none';
      fitView();
      toast(`Loaded ${name || 'image'}`);
    });
  } catch(e){ toast('Image load failed: ' + e.message, 'err'); }
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
  document.body.focus();
  toast('Press Ctrl+V / ⌘+V');
};
document.addEventListener('paste', e => {
  const now = Date.now();
  if (now - pasteLock < 500) return;
  const items = (e.clipboardData || {}).items || [];
  for (const it of items){
    if (it.kind === 'file' && it.type.startsWith('image/')){
      pasteLock = now;
      const r = new FileReader();
      r.onload = ev => loadImage(ev.target.result, 'pasted');
      r.readAsDataURL(it.getAsFile());
      e.preventDefault(); return;
    }
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
   17. VIEW / ZOOM
   ===================================================================== */
function applyView(){
  $('canvas-holder').style.transform =
    `translate(${view.x}px, ${view.y}px) scale(${view.zoom})`;
  $('zoom-lvl').textContent = Math.round(view.zoom * 100) + '%';
}
function zoomBy(f, cx, cy){
  const stage = $('stage').getBoundingClientRect();
  cx = cx ?? stage.width / 2;
  cy = cy ?? stage.height / 2;
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
  const z = Math.min((stage.width - 80) / cw, (stage.height - 80) / ch);
  view.zoom = z;
  view.x = (stage.width - cw * z) / 2;
  view.y = (stage.height - ch * z) / 2;
  applyView();
}
$('stage').addEventListener('wheel', e => {
  if (!e.ctrlKey) return;
  e.preventDefault();
  const r = $('stage').getBoundingClientRect();
  zoomBy(e.deltaY < 0 ? 1.1 : 1/1.1, e.clientX - r.left, e.clientY - r.top);
}, { passive: false });
$('stage').addEventListener('mousedown', e => {
  if ((spaceDown || currentTool === 'pan') && e.button === 0){
    panning = true;
    panStart = { x: e.clientX, y: e.clientY };
    e.preventDefault();
  }
});
window.addEventListener('mouseup', () => { if (panning){ panning = false; panStart = null; } });
window.addEventListener('mousemove', e => {
  if (!panning || !panStart) return;
  view.x += e.clientX - panStart.x;
  view.y += e.clientY - panStart.y;
  panStart = { x: e.clientX, y: e.clientY };
  applyView();
});

/* =====================================================================
   18. PANELS
   ===================================================================== */
function refreshPanels(){ updateHud(); updateStorageInfo(); }
function updateHud(){
  const n = canvas.getObjects().filter(o => !o.isBackground).length;
  const chip = $('hud-count');
  chip.textContent = n + ' object' + (n === 1 ? '' : 's');
  chip.classList.remove('warn', 'err');
  if (n > 800) chip.classList.add('err');
  else if (n > 300) chip.classList.add('warn');
}
function updateStorageInfo(){
  const el = $('storage-info');
  if (!Storage.available()){ el.textContent = 'storage: unavailable'; return; }
  el.textContent = 'storage: ' + (Storage.bytes()/1024).toFixed(1) + ' KB';
}

/* =====================================================================
   19. EXPORT
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
      version: 1,
      kind: 'telecom_site_layout',
      exported: new Date().toISOString(),
      canvas: { width: canvas.getWidth(), height: canvas.getHeight() },
      scale: { m_per_px: parseFloat($('scale-m').value || 0.05),
               unit: $('unit-label').value || 'm' },
      file_name: fileName,
      fabric: canvas.toJSON(['selectable','evented','isBackground',
                             '_isCable','_isAnnotation','_isDimension','_stencilLabel']),
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
          });
          canvas.renderAll();
          refreshPanels();
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
   20. SAVE / RESTORE SESSION
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
  try { parsed = JSON.parse(j); } catch(e){
    Storage.del(Storage.KEY); return false;
  }
  const fab = parsed.fabric || parsed;
  if (!fab || !Array.isArray(fab.objects)){ Storage.del(Storage.KEY); return false; }
  try {
    canvas.loadFromJSON(fab, () => {
      canvas.forEachObject(o => {
        o.evented = true;
        o.set({ perPixelTargetFind:true, padding:2 });
      });
      canvas.renderAll();
      refreshPanels();
      const n = canvas.getObjects().filter(o => !o.isBackground).length;
      toast(`Restored session (${n} object${n===1?'':'s'})`);
    });
    return true;
  } catch(e){ toast('Restore failed', 'err'); return false; }
}

/* =====================================================================
   21. KEYBOARD
   ===================================================================== */
document.addEventListener('keydown', e => {
  const editing = e.target.tagName === 'INPUT' || e.target.isContentEditable;
  if ((e.ctrlKey||e.metaKey) && e.shiftKey && e.key.toLowerCase()==='d'){
    e.preventDefault(); runDiagnostics(); return;
  }
  if (editing) return;
  if (e.code === 'Space'){ spaceDown = true;
    document.body.style.cursor = 'grab'; e.preventDefault(); }

  const k = e.key.toLowerCase();
  if (e.ctrlKey || e.metaKey){
    if (k === 'z'){ e.preventDefault(); e.shiftKey ? redo() : undo(); }
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
    pendingStencil = null;
    canvas.discardActiveObject(); canvas.renderAll();
  }
  else if (k === 'enter'){
    if (polyPreview) finalizePolyline();
  }
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
   22. DIAGNOSTICS
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
    'Stencils available: ' + Object.keys(STENCILS).length,
    'Undo: ' + undoStack.length + ' / Redo: ' + redoStack.length,
    'View: zoom=' + view.zoom.toFixed(2) + ' x='+Math.round(view.x)+' y='+Math.round(view.y),
    'UA: ' + navigator.userAgent,
  ];
  const txt = lines.join('\n');
  console.log(txt);
  try {
    download(new Blob([txt], { type:'text/plain' }),
             'diagnostics_'+Date.now()+'.txt');
    toast('Diagnostics downloaded');
  } catch(e){ toast('See console', 'warn'); }
}

/* =====================================================================
   23. TOOLBAR BINDINGS
   ===================================================================== */
$('tb-new').onclick = () => {
  if (!confirm('New site plan? Unsaved work will be lost.')) return;
  canvas.getObjects().forEach(o => canvas.remove(o));
  canvas.setBackgroundImage(null, canvas.renderAll.bind(canvas));
  canvas.setWidth(CW); canvas.setHeight(CH);
  fileName = 'Untitled Site Plan'; $('file-label').textContent = fileName;
  $('drop-hint').style.display = 'flex';
  fitView(); refreshPanels();
  toast('New plan started');
};
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
$('tb-paste').onclick = () => { document.body.focus(); toast('Press Ctrl+V'); };
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

/* Right sidebar bindings */
$('stroke-width').oninput = e => $('sw-val').textContent = e.target.value + 'px';
$('font-size').oninput    = e => $('fs-val').textContent = e.target.value + 'px';
$('fill-opacity').oninput = e => $('fill-op-val').textContent = e.target.value + '%';
$('grid-size').oninput    = e => { $('grid-val').textContent = e.target.value + 'px'; drawGridOverlay(); };
$('show-grid').onchange   = drawGridOverlay;
$('btn-dup').onclick = duplicateSel;
$('btn-del').onclick = deleteSel;
$('btn-rot90').onclick = rotate90;
$('btn-flip').onclick = flipSel;
$('btn-clear').onclick = clearAll;
$('btn-backup').onclick = exportJSON;
$('btn-reset').onclick = () => {
  if (!confirm('Reset session?')) return;
  Storage.del(Storage.KEY); Storage.del(Storage.KEY_CTR);
  toast('Session reset'); updateStorageInfo();
};

/* Palette */
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
   24. STREAMLIT HEIGHT SYNC
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
   25. BOOT
   ===================================================================== */
(async function boot(){
  try {
    Boot.show('Loading graphics library…');
    await loadFabric();

    Boot.show('Initializing canvas…');
    initCanvas();
    tightenSelectionBoxes();
    buildPalette();
    $('counter-val') && ($('counter-val').textContent = 'C-01');

    setTimeout(() => fitView(), 100);

    Boot.show('Restoring session…');
    setTimeout(() => {
      const restored = loadLocal();
      if (!restored) toast('Ready — try a stencil from 📦 or open an image');
      Boot.ready();
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
