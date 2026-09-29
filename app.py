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
  .stencil svg{width:44px;height:44px}

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
  .prow .pbtn{flex:1;justify-content:center;text-align:center}

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

  #stage{flex:1;position:relative;overflow:hidden;
    background:repeating-conic-gradient(#0a1020 0 25%,#0b1220 0 50%) 50%/24px 24px;
    padding-top:44px}
  #canvas-holder{position:absolute;top:44px;left:0;transform-origin:0 0;
    will-change:transform}

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
    font-family:ui-monospace,monospace;font-size:.7rem;
    display:flex;align-items:center;padding:0 6px}

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

  <aside id="sidebar">
    <button class="tbtn active" data-tool="select">
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
      <span>↗️</span><span class="tip">Polyline — Enter to finish</span>
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
      <div class="stencil" data-stencil="cement"><span>⬜</span>Cement Floor</div>
      <div class="stencil" data-stencil="gravel"><span>🪨</span>Gravel Pad</div>
      <div class="stencil" data-stencil="wall"><span>🧱</span>Wall</div>
    </div>
  </div>

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
      <div><b style="color:#a5b4fc">Finish polyline:</b> Enter</div>
      <div><b style="color:#a5b4fc">Diag:</b> Ctrl+Shift+D</div>
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
  KEY: 'telecom_site_v2',
  KEY_CTR: 'telecom_site_ctr_v2',
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
const CW = 1600, CH = 1000;
const M2PX = 20;             // 1 m = 20 px default drawing scale

const PALETTE = ['#334155','#64748b','#94a3b8','#cbd5e1','#f8fafc','#000000',
                 '#dc2626','#ea580c','#ca8a04','#16a34a','#0891b2','#2563eb',
                 '#7c3aed','#db2777','#a16207','#0f766e','#475569','#a3a3a3'];

/* =====================================================================
   4. FABRIC PROTOTYPE — tight selection boxes (Option A)
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
   5. ★ TOP-VIEW ENGINEERING SYMBOLS
   Every stencil is drawn from the TOP (plan view) the way it appears
   on a real telecom site drawing. All dimensions in metres → px.
   ===================================================================== */

/* ---- Drawing primitives ---- */
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
  return g;
}

/* Hatch fill for concrete (diagonal 45° lines) */
function hatchRect(x,y,w,h, opt){
  opt = opt || {};
  const spacing = opt.spacing || 8;
  const color = opt.hatch || '#94a3b8';
  const g = [];
  // background
  g.push(mkRect(x,y,w,h, Object.assign({
    fill: opt.fill || 'rgba(226,232,240,0.6)',
    stroke: opt.stroke || '#0f172a', strokeWidth: opt.strokeWidth || 1.5,
  }, opt.extra || {})));
  // diagonal hatch lines clipped to rect
  const diag = w + h;
  for (let i = -h; i < diag; i += spacing){
    const x1 = x + i, y1 = y;
    const x2 = x + i + h, y2 = y + h;
    // simple clip: only draw segment where it intersects rect
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

const STENCILS = {

  /* ==================== GATE & FENCE ==================== */
  gate_2door(){
    const W = 4*M2PX, H = 4;
    const g = [];
    // piers at each end
    g.push(mkRect(0, 0, H, H, { fill:'#64748b', stroke:'#0f172a', strokeWidth:1.5 }));
    g.push(mkRect(W-H, 0, H, H, { fill:'#64748b', stroke:'#0f172a', strokeWidth:1.5 }));
    // rails (top view — thin lines)
    g.push(mkLine(H, H/2, W-H, H/2, { stroke:'#0f172a', strokeWidth:2 }));
    // left door leaf (open) — arc
    const leafL = new fabric.Path(`M ${H} ${H/2} L ${H} ${H/2 - W*0.45}`,
      { stroke:'#0f172a', strokeWidth:1, fill:'', selectable:false, evented:false });
    g.push(leafL);
    const arcL = new fabric.Path(
      `M ${H} ${H/2 - W*0.45} A ${W*0.45} ${W*0.45} 0 0 1 ${H + W*0.45} ${H/2}`,
      { stroke:'#0891b2', strokeWidth:0.8, fill:'', strokeDashArray:[3,2],
        selectable:false, evented:false });
    g.push(arcL);
    // right door leaf
    const leafR = new fabric.Path(`M ${W-H} ${H/2} L ${W-H} ${H/2 - W*0.45}`,
      { stroke:'#0f172a', strokeWidth:1, fill:'', selectable:false, evented:false });
    g.push(leafR);
    const arcR = new fabric.Path(
      `M ${W-H} ${H/2 - W*0.45} A ${W*0.45} ${W*0.45} 0 0 0 ${W-H - W*0.45} ${H/2}`,
      { stroke:'#0891b2', strokeWidth:0.8, fill:'', strokeDashArray:[3,2],
        selectable:false, evented:false });
    g.push(arcR);
    // label + dim
    g.push(mkText('GATE 2-DOOR', W/2 - 34, -16, 9, { fill:'#7c2d12' }));
    g.push(mkText(`${(W/M2PX).toFixed(1)}m`, W/2 - 10, H + 4, 8, { fill:'#0891b2' }));
    return mkGroup(g, 'Gate');
  },
  fence(){
    const W = 5*M2PX, H = 3;
    const g = [
      mkLine(0, H/2, W, H/2, { stroke:'#0f172a', strokeWidth:1.5 }),
      mkLine(0, 0, 0, H, { stroke:'#64748b', strokeWidth:3 }),
      mkLine(W, 0, W, H, { stroke:'#64748b', strokeWidth:3 }),
    ];
    // tick marks
    for (let x = 0; x <= W; x += 10){
      g.push(mkLine(x, H/2 - 2, x, H/2 + 2, { stroke:'#0f172a', strokeWidth:0.8 }));
    }
    return mkGroup(g, 'Fence');
  },

  /* ==================== CABIN / SHELTER ==================== */
  cabin(){
    // Outdoor telecom shelter — top view with hatched roof outline, door, vents
    const W = 4*M2PX, H = 3*M2PX;
    const g = [];
    // outer wall
    g.push(mkRect(0, 0, W, H, { fill:'#f1f5f9', stroke:'#0f172a', strokeWidth:2 }));
    // wall thickness (inner outline)
    g.push(mkRect(5, 5, W-10, H-10, { fill:'transparent', stroke:'#475569',
      strokeWidth:1, strokeDashArray:[4,2] }));
    // door swing
    const dw = 22, dx = W - dw - 4, dy = H/2 - 11;
    g.push(mkRect(dx, dy, dw, 22, { fill:'#94a3b8', stroke:'#0f172a' }));
    g.push(new fabric.Path(`M ${dx} ${dy} A 22 22 0 0 0 ${dx + 22} ${dy}`,
      { stroke:'#0891b2', strokeWidth:0.8, fill:'', strokeDashArray:[2,2],
        selectable:false, evented:false }));
    // AC unit on side
    g.push(mkRect(6, 6, 24, 12, { fill:'#dbeafe', stroke:'#1e3a8a', strokeWidth:1 }));
    g.push(mkText('AC', 14, 9, 7, { fill:'#1e3a8a' }));
    // Cable entry
    g.push(mkRect(W-24, H-14, 18, 8, { fill:'#fef3c7', stroke:'#a16207', strokeWidth:1 }));
    g.push(mkText('ENTRY', W-24, H-6, 6, { fill:'#7c2d12' }));
    // Title
    g.push(mkText('SHELTER', W/2-26, H/2 - 5, 11, { fontWeight:'700' }));
    g.push(mkText(`${(W/M2PX).toFixed(1)} × ${(H/M2PX).toFixed(1)}m`,
      W/2 - 24, -14, 8, { fill:'#0891b2' }));
    return mkGroup(g, 'Shelter');
  },
  stairs(){
    // Top view: parallel treads with direction arrow
    const steps = 8, tw = 30, th = 8;
    const g = [];
    for (let i = 0; i < steps; i++){
      g.push(mkRect(0, i*th, tw, th, { fill:'#cbd5e1', stroke:'#334155', strokeWidth:1 }));
    }
    // Direction arrow
    g.push(mkLine(tw/2, steps*th - 4, tw/2, 4,
      { stroke:'#0891b2', strokeWidth:1.2 }));
    g.push(new fabric.Triangle({ left: tw/2 - 3, top: 0, width: 6, height: 8,
      fill:'#0891b2', angle: 0, selectable:false, evented:false }));
    g.push(mkText('STAIRS', tw + 4, steps*th/2 - 5, 8, { fill:'#0891b2' }));
    return mkGroup(g, 'Stairs');
  },

  /* ==================== CABINETS (top view) ==================== */
  odc(){
    // ODC cabinet with double doors — plan view
    const W = 1.2*M2PX, H = 2.2*M2PX;
    const g = [
      mkRect(0, 0, W, H, { fill:'#f8fafc', stroke:'#0f172a', strokeWidth:2 }),
      mkLine(W/2, 0, W/2, H, { stroke:'#0f172a', strokeWidth:1, strokeDashArray:[3,2] }),
      // corner bolts
      mkCircle(2, 2, 2, { fill:'#64748b', stroke:'none' }),
      mkCircle(W-4, 2, 2, { fill:'#64748b', stroke:'none' }),
      mkCircle(2, H-4, 2, { fill:'#64748b', stroke:'none' }),
      mkCircle(W-4, H-4, 2, { fill:'#64748b', stroke:'none' }),
      mkText('ODC', W/2 - 15, H/2 - 5, 9, { fontWeight:'700' }),
    ];
    // door swing arcs
    g.push(new fabric.Path(`M 0 0 A ${W/2} ${W/2} 0 0 1 ${W/2} ${W/2}`,
      { stroke:'#0891b2', strokeWidth:0.7, fill:'', strokeDashArray:[2,2],
        selectable:false, evented:false }));
    g.push(mkText(`${(W/M2PX).toFixed(1)}×${(H/M2PX).toFixed(1)}`,
      4, H + 3, 7, { fill:'#0891b2' }));
    return mkGroup(g, 'ODC');
  },
  cab1(){
    const W = 0.6*M2PX, H = 2.2*M2PX;
    const g = [
      mkRect(0, 0, W, H, { fill:'#e2e8f0', stroke:'#0f172a', strokeWidth:1.8 }),
      mkLine(2, 2, 2, H-2, { stroke:'#475569', strokeWidth:0.8 }),
      mkText('1B', W/2-8, H/2-4, 8, { fontWeight:'700' }),
    ];
    return mkGroup(g, '1-Bay');
  },
  cab2(){
    const W = 1.2*M2PX, H = 2.2*M2PX;
    const g = [
      mkRect(0, 0, W, H, { fill:'#e2e8f0', stroke:'#0f172a', strokeWidth:1.8 }),
      mkLine(W/2, 2, W/2, H-2, { stroke:'#475569', strokeWidth:0.8 }),
      mkText('2B', W/2-8, H/2-4, 8, { fontWeight:'700' }),
    ];
    return mkGroup(g, '2-Bay');
  },
  cab3(){
    const W = 1.8*M2PX, H = 2.2*M2PX;
    const g = [
      mkRect(0, 0, W, H, { fill:'#e2e8f0', stroke:'#0f172a', strokeWidth:1.8 }),
      mkLine(W/3, 2, W/3, H-2, { stroke:'#475569', strokeWidth:0.8 }),
      mkLine(2*W/3, 2, 2*W/3, H-2, { stroke:'#475569', strokeWidth:0.8 }),
      mkText('3B', W/2-8, H/2-4, 8, { fontWeight:'700' }),
    ];
    return mkGroup(g, '3-Bay');
  },

  /* ==================== TOWER (top view) ==================== */
  tower4(){
    // 4-leg self-supporting tower — top view showing all legs and X bracing
    const S = 4*M2PX;
    const g = [];
    // foundation pads under each leg
    const pad = 14;
    [[0,0],[S,0],[0,S],[S,S]].forEach(([cx,cy]) => {
      g.push(mkRect(cx - pad/2, cy - pad/2, pad, pad,
        { fill:'#94a3b8', stroke:'#0f172a', strokeWidth:1 }));
    });
    // 4 legs
    [[0,0],[S,0],[0,S],[S,S]].forEach(([cx,cy]) => {
      g.push(mkCircle(cx, cy, 5, { fill:'#1e293b', stroke:'#0f172a', strokeWidth:1 }));
    });
    // outer square (legs connected by lattice)
    g.push(mkLine(0, 0, S, 0, { stroke:'#0f172a', strokeWidth:1.2 }));
    g.push(mkLine(S, 0, S, S, { stroke:'#0f172a', strokeWidth:1.2 }));
    g.push(mkLine(S, S, 0, S, { stroke:'#0f172a', strokeWidth:1.2 }));
    g.push(mkLine(0, S, 0, 0, { stroke:'#0f172a', strokeWidth:1.2 }));
    // X bracing on each face
    g.push(mkLine(0, 0, S, S, { stroke:'#0f172a', strokeWidth:0.8,
      strokeDashArray:[4,3] }));
    g.push(mkLine(S, 0, 0, S, { stroke:'#0f172a', strokeWidth:0.8,
      strokeDashArray:[4,3] }));
    // interior mast
    g.push(mkCircle(S/2, S/2, 8, { fill:'#334155', stroke:'#0f172a', strokeWidth:1.5 }));
    // label
    g.push(mkText('4-LEG TOWER', S/2-38, -18, 10, { fontWeight:'700' }));
    g.push(mkText(`${(S/M2PX).toFixed(1)} × ${(S/M2PX).toFixed(1)}m`,
      S/2-22, S + 4, 8, { fill:'#0891b2' }));
    return mkGroup(g, '4-Leg Tower');
  },
  tower3(){
    const S = 3.5*M2PX;
    const h = S * 0.866;              // triangle height
    const A = { x:S/2, y:0 }, B = { x:0, y:h }, C = { x:S, y:h };
    const g = [];
    // foundation pads
    [A,B,C].forEach(p => {
      g.push(mkRect(p.x - 7, p.y - 7, 14, 14,
        { fill:'#94a3b8', stroke:'#0f172a', strokeWidth:1 }));
    });
    // triangle
    g.push(mkLine(A.x, A.y, B.x, B.y, { stroke:'#0f172a', strokeWidth:1.2 }));
    g.push(mkLine(B.x, B.y, C.x, C.y, { stroke:'#0f172a', strokeWidth:1.2 }));
    g.push(mkLine(C.x, C.y, A.x, A.y, { stroke:'#0f172a', strokeWidth:1.2 }));
    // legs
    [A,B,C].forEach(p => g.push(mkCircle(p.x, p.y, 5,
      { fill:'#1e293b', stroke:'#0f172a' })));
    // X bracing
    g.push(mkLine(A.x, A.y, (B.x+C.x)/2, (B.y+C.y)/2,
      { stroke:'#0f172a', strokeWidth:0.8, strokeDashArray:[4,3] }));
    g.push(mkLine(B.x, B.y, (A.x+C.x)/2, (A.y+C.y)/2,
      { stroke:'#0f172a', strokeWidth:0.8, strokeDashArray:[4,3] }));
    g.push(mkLine(C.x, C.y, (A.x+B.x)/2, (A.y+B.y)/2,
      { stroke:'#0f172a', strokeWidth:0.8, strokeDashArray:[4,3] }));
    // centre
    g.push(mkCircle(S/2, h/2 + 4, 7,
      { fill:'#334155', stroke:'#0f172a' }));
    g.push(mkText('3-LEG TOWER', S/2-38, -18, 10, { fontWeight:'700' }));
    return mkGroup(g, '3-Leg Tower');
  },
  towerfoot(){
    // Concrete footing with anchor bolt pattern (plan view)
    const S = 1.2*M2PX;
    const g = [];
    g.push(...hatchRect(0, 0, S, S, { spacing:6, hatch:'#64748b' }));
    // anchor bolt circle pattern
    const cx = S/2, cy = S/2, r = S*0.32;
    g.push(mkCircle(cx, cy, r, { fill:'transparent', stroke:'#0f172a',
      strokeWidth:0.8, strokeDashArray:[2,2] }));
    for (let i = 0; i < 8; i++){
      const a = (i / 8) * Math.PI * 2;
      g.push(mkCircle(cx + Math.cos(a)*r, cy + Math.sin(a)*r, 2,
        { fill:'#1e293b', stroke:'none' }));
    }
    g.push(mkText('FOOTING', cx - 22, cy - 4, 8, { fontWeight:'700' }));
    return mkGroup(g, 'Footing');
  },
  guy(){
    const S = 1*M2PX;
    const g = [
      // Guy anchor block (concrete)
      mkRect(0, 0, S, S, { fill:'#a8a29e', stroke:'#44403c', strokeWidth:1.5 }),
      mkCircle(S/2, S/2, S*0.25, { fill:'#fef3c7', stroke:'#a16207', strokeWidth:1 }),
      mkCircle(S/2, S/2, 2, { fill:'#1e293b' }),
      mkText('GUY', S/2 - 12, S + 3, 8, { fontWeight:'700' }),
    ];
    return mkGroup(g, 'Guy Anchor');
  },

  /* ==================== POWER ==================== */
  genset(){
    // Generator: concrete pad + enclosure with radiator, exhaust, control panel
    const padW = 4*M2PX, padH = 2.4*M2PX;
    const genW = 3.4*M2PX, genH = 1.6*M2PX;
    const gx = (padW - genW)/2, gy = (padH - genH)/2;
    const g = [];
    // concrete pad — hatched
    g.push(...hatchRect(0, 0, padW, padH, { spacing:8, hatch:'#94a3b8' }));
    // enclosure
    g.push(mkRect(gx, gy, genW, genH,
      { fill:'#fef3c7', stroke:'#78350f', strokeWidth:2 }));
    // radiator (right end)
    g.push(mkRect(gx + genW - 20, gy + 4, 16, genH - 8,
      { fill:'#fdba74', stroke:'#7c2d12', strokeWidth:1 }));
    for (let y = gy + 6; y < gy + genH - 6; y += 4){
      g.push(mkLine(gx + genW - 19, y, gx + genW - 5, y,
        { stroke:'#7c2d12', strokeWidth:0.6 }));
    }
    // control panel (left end)
    g.push(mkRect(gx + 4, gy + 4, 14, genH - 8,
      { fill:'#dbeafe', stroke:'#1e3a8a', strokeWidth:1 }));
    // exhaust stub (top)
    g.push(mkCircle(gx + genW*0.55, gy - 4, 4,
      { fill:'#94a3b8', stroke:'#334155', strokeWidth:1 }));
    // labels
    g.push(mkText('GENSET', gx + genW/2 - 24, gy + genH/2 - 4, 10,
      { fontWeight:'700', fill:'#7c2d12' }));
    g.push(mkText('RAD', gx + genW - 20, gy + genH + 3, 7, { fill:'#7c2d12' }));
    g.push(mkText('CP', gx + 2, gy + genH + 3, 7, { fill:'#1e3a8a' }));
    g.push(mkText(`${(padW/M2PX).toFixed(1)}×${(padH/M2PX).toFixed(1)}m`,
      padW/2 - 24, padH + 4, 8, { fill:'#0891b2' }));
    return mkGroup(g, 'Generator');
  },
  fuel(){
    // Cylindrical fuel tank — top view as circles (outer shell, inner shell)
    const R = 0.7*M2PX;
    const g = [];
    // bund wall (dashed)
    g.push(mkCircle(R, R, R*1.35,
      { fill:'transparent', stroke:'#94a3b8', strokeWidth:1,
        strokeDashArray:[4,3] }));
    // outer shell
    g.push(mkCircle(R, R, R,
      { fill:'#fecaca', stroke:'#7f1d1d', strokeWidth:2 }));
    // inner shell (wall thickness)
    g.push(mkCircle(R, R, R*0.9,
      { fill:'transparent', stroke:'#7f1d1d', strokeWidth:1 }));
    // fill port + vent + level gauge
    g.push(mkCircle(R, R - R*0.55, R*0.12,
      { fill:'#7f1d1d', stroke:'none' }));     // fill port
    g.push(mkCircle(R + R*0.55, R, R*0.12,
      { fill:'#0891b2', stroke:'none' }));     // level gauge
    g.push(mkCircle(R, R + R*0.55, R*0.12,
      { fill:'#334155', stroke:'none' }));     // vent
    // label
    g.push(mkText('FUEL TANK', R - 30, R - 4, 9,
      { fontWeight:'700', fill:'#7f1d1d' }));
    g.push(mkText(`Ø${(2*R/M2PX).toFixed(1)}m`, R - 18, R + 10, 7,
      { fill:'#0891b2' }));
    return mkGroup(g, 'Fuel Tank');
  },
  transformer(){
    // Distribution transformer (plan view): tank + HV/LV bushings + radiator fins
    const W = 1.6*M2PX, H = 1.6*M2PX;
    const g = [];
    // tank
    g.push(mkRect(0, 0, W, H,
      { fill:'#fef3c7', stroke:'#78350f', strokeWidth:2 }));
    // internal coil circles
    g.push(mkCircle(W/2, H/2, W*0.28,
      { fill:'transparent', stroke:'#78350f', strokeWidth:1, strokeDashArray:[3,2] }));
    // HV bushings (3 circles on top)
    for (let i = 0; i < 3; i++){
      const x = W*0.25 + i * W*0.25;
      g.push(mkCircle(x, -4, 3, { fill:'#dc2626', stroke:'#7f1d1d', strokeWidth:1 }));
    }
    // LV bushings (2 circles below)
    for (let i = 0; i < 2; i++){
      const x = W*0.33 + i * W*0.34;
      g.push(mkCircle(x, H + 4, 3,
        { fill:'#2563eb', stroke:'#1e3a8a', strokeWidth:1 }));
    }
    // radiator fins (left)
    for (let i = 0; i < 5; i++){
      g.push(mkLine(-2 - i*2, 4, -2 - i*2, H - 4,
        { stroke:'#78350f', strokeWidth:0.8 }));
    }
    // labels
    g.push(mkText('TRANSFORMER', W/2 - 34, H/2 - 4, 8,
      { fontWeight:'700', fill:'#78350f' }));
    g.push(mkText('HV', W/2 - 6, -18, 7, { fill:'#dc2626' }));
    g.push(mkText('LV', W/2 - 6, H + 10, 7, { fill:'#2563eb' }));
    return mkGroup(g, 'Transformer');
  },
  battery(){
    // Battery bank — row of cells with polarity marks
    const W = 2.6*M2PX, H = 0.7*M2PX;
    const cells = 4;
    const cw = W / cells;
    const g = [];
    for (let i = 0; i < cells; i++){
      g.push(mkRect(i*cw, 0, cw, H,
        { fill:'#dbeafe', stroke:'#1e3a8a', strokeWidth:1.2 }));
      // +/- terminals
      g.push(mkCircle(i*cw + 4, 4, 2, { fill:'#dc2626', stroke:'none' }));
      g.push(mkCircle(i*cw + cw - 4, 4, 2, { fill:'#1e293b', stroke:'none' }));
      // cell number
      g.push(mkText(String(i + 1), i*cw + cw/2 - 3, H/2 - 3, 8,
        { fill:'#1e3a8a' }));
    }
    g.push(mkText('BATTERY BANK', W/2 - 32, H + 3, 8,
      { fontWeight:'700', fill:'#1e3a8a' }));
    return mkGroup(g, 'Battery');
  },

  /* ==================== COOLING ==================== */
  aircon(){
    // Split AC outdoor unit — top view with fan circle and grille
    const W = 1.0*M2PX, H = 0.6*M2PX;
    const cx = W*0.65, cy = H/2;
    const r = Math.min(W, H) * 0.35;
    const g = [
      mkRect(0, 0, W, H, { fill:'#e0f2fe', stroke:'#0369a1', strokeWidth:1.8 }),
    ];
    // fan
    g.push(mkCircle(cx, cy, r,
      { fill:'#bae6fd', stroke:'#0369a1', strokeWidth:1 }));
    g.push(mkCircle(cx, cy, r*0.2,
      { fill:'#0369a1', stroke:'#0369a1', strokeWidth:0.5 }));
    // fan blades
    for (let i = 0; i < 4; i++){
      const a = (i/4) * Math.PI * 2;
      g.push(mkLine(cx, cy,
        cx + Math.cos(a)*r*0.85, cy + Math.sin(a)*r*0.85,
        { stroke:'#0369a1', strokeWidth:0.8 }));
    }
    // condenser coils (left side lines)
    for (let x = 4; x < W*0.35; x += 3){
      g.push(mkLine(x, 3, x, H - 3,
        { stroke:'#0369a1', strokeWidth:0.6 }));
    }
    g.push(mkText('AC', W*0.18 - 8, H/2 - 3, 8,
      { fontWeight:'700', fill:'#0c4a6e' }));
    return mkGroup(g, 'Aircon');
  },

  /* ==================== CABLE INFRASTRUCTURE ==================== */
  cabletray(){
    // Ladder-type cable tray — two side rails + rungs (top view)
    const W = 4*M2PX, H = 0.4*M2PX;
    const g = [
      mkLine(0, 0, W, 0, { stroke:'#475569', strokeWidth:2 }),
      mkLine(0, H, W, H, { stroke:'#475569', strokeWidth:2 }),
    ];
    for (let x = 4; x < W; x += 6){
      g.push(mkLine(x, 1, x, H - 1,
        { stroke:'#475569', strokeWidth:0.8 }));
    }
    g.push(mkText('CABLE TRAY', 8, -12, 8,
      { fontWeight:'700', fill:'#334155' }));
    g.push(mkText(`${(W/M2PX).toFixed(1)}m`, W - 22, H + 3, 7,
      { fill:'#0891b2' }));
    return mkGroup(g, 'Cable Tray');
  },
  openrack(){
    // 19" open rack — side view (top-down: narrow footprint)
    const W = 0.6*M2PX, H = 2.2*M2PX;
    const g = [
      mkRect(0, 0, W, H, { fill:'#f8fafc', stroke:'#0f172a', strokeWidth:1.8 }),
      // rails
      mkLine(2, 2, 2, H-2, { stroke:'#475569', strokeWidth:1.5 }),
      mkLine(W-2, 2, W-2, H-2, { stroke:'#475569', strokeWidth:1.5 }),
    ];
    // U-slots
    for (let y = 6; y < H - 6; y += 5){
      g.push(mkLine(3, y, W-3, y, { stroke:'#94a3b8', strokeWidth:0.5 }));
    }
    g.push(mkText('RACK', W/2 - 12, H/2 - 3, 7, { fontWeight:'700' }));
    return mkGroup(g, 'Open Rack');
  },
  hframe(){
    // H-frame — vertical posts + horizontal arms (front view)
    const W = 2*M2PX, H = 2.5*M2PX;
    const g = [
      // posts
      mkRect(2, 0, 4, H, { fill:'#334155', stroke:'#0f172a', strokeWidth:1 }),
      mkRect(W-6, 0, 4, H, { fill:'#334155', stroke:'#0f172a', strokeWidth:1 }),
      // crossbeam
      mkRect(0, H/2 - 3, W, 6, { fill:'#334155', stroke:'#0f172a', strokeWidth:1 }),
      // splice closures (circles)
      mkCircle(W*0.3, H*0.25, 5, { fill:'#fbbf24', stroke:'#92400e', strokeWidth:1 }),
      mkCircle(W*0.7, H*0.25, 5, { fill:'#fbbf24', stroke:'#92400e', strokeWidth:1 }),
      mkCircle(W*0.3, H*0.75, 5, { fill:'#fbbf24', stroke:'#92400e', strokeWidth:1 }),
      mkCircle(W*0.7, H*0.75, 5, { fill:'#fbbf24', stroke:'#92400e', strokeWidth:1 }),
      mkText('H-FRAME', W/2 - 22, H + 3, 8, { fontWeight:'700' }),
    ];
    return mkGroup(g, 'H-Frame');
  },

  /* ==================== SITE SURFACE ==================== */
  grass(){
    // Top view: light green fill with grass tufts and no border
    const W = 8*M2PX, H = 6*M2PX;
    const g = [
      mkRect(0, 0, W, H, {
        fill:'rgba(132,204,22,0.18)', stroke:'#65a30d',
        strokeWidth:1, strokeDashArray:[6,4]
      }),
    ];
    for (let i = 0; i < 80; i++){
      const x = Math.random()*W, y = Math.random()*H;
      g.push(mkLine(x, y, x + 2, y - 4,
        { stroke:'#65a30d', strokeWidth:0.8 }));
      g.push(mkLine(x + 2, y, x + 4, y - 3,
        { stroke:'#84cc16', strokeWidth:0.8 }));
    }
    g.push(mkText('GRASS AREA', W/2 - 32, H/2 - 4, 10,
      { fontWeight:'700', fill:'#3f6212', opacity:0.5 }));
    g.push(mkText(`${(W/M2PX).toFixed(1)} × ${(H/M2PX).toFixed(1)}m`,
      W/2 - 26, -14, 8, { fill:'#0891b2' }));
    return mkGroup(g, 'Grass');
  },
  cement(){
    // Concrete slab — light gray with subtle cross-hatch dots (broom finish top-view)
    const W = 8*M2PX, H = 6*M2PX;
    const g = [
      mkRect(0, 0, W, H, {
        fill:'rgba(203,213,225,0.55)', stroke:'#64748b',
        strokeWidth:1.5, strokeDashArray:[6,3]
      }),
    ];
    // Expansion joints
    for (let x = W/4; x < W; x += W/4){
      g.push(mkLine(x, 0, x, H, { stroke:'#94a3b8', strokeWidth:0.8,
        strokeDashArray:[4,3] }));
    }
    for (let y = H/3; y < H; y += H/3){
      g.push(mkLine(0, y, W, y, { stroke:'#94a3b8', strokeWidth:0.8,
        strokeDashArray:[4,3] }));
    }
    g.push(mkText('CEMENT SLAB', W/2 - 40, H/2 - 5, 11,
      { fontWeight:'700', fill:'#475569', opacity:0.55 }));
    g.push(mkText(`${(W/M2PX).toFixed(1)} × ${(H/M2PX).toFixed(1)}m`,
      W/2 - 26, -14, 8, { fill:'#0891b2' }));
    return mkGroup(g, 'Cement Slab');
  },
  gravel(){
    // Gravel pad — random gray dots
    const W = 6*M2PX, H = 4*M2PX;
    const g = [
      mkRect(0, 0, W, H, {
        fill:'rgba(168,162,158,0.25)', stroke:'#78716c', strokeWidth:1
      }),
    ];
    for (let i = 0; i < 120; i++){
      const x = Math.random()*W, y = Math.random()*H;
      g.push(mkCircle(x, y, 0.8 + Math.random()*1.2,
        { fill:'#78716c', stroke:'none', opacity:0.65 }));
    }
    return mkGroup(g, 'Gravel');
  },
  wall(){
    // Wall section — double parallel lines with brick pattern (top view)
    const W = 5*M2PX, H = 6;
    const g = [
      mkRect(0, 0, W, H, { fill:'#a8a29e', stroke:'#44403c', strokeWidth:1.5 }),
    ];
    // brick joints
    for (let x = 8; x < W; x += 8){
      g.push(mkLine(x, 0, x, H, { stroke:'#44403c', strokeWidth:0.5 }));
    }
    g.push(mkLine(0, H/2, W, H/2, { stroke:'#44403c', strokeWidth:0.5 }));
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
      opt.target.set({ perPixelTargetFind:true, padding:2 });
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
   9. POINTER HANDLERS
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
  if (currentTool === 'select'){
    if (opt.target && opt.e.altKey && !opt.target.isBackground){
      const orig = opt.target;
      orig.clone(c => {
        c.set({ left:orig.left, top:orig.top, evented:true, selectable:true,
                perPixelTargetFind:true, padding:2 });
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
    const label = new fabric.IText($('text-value').value || 'TEXT', {
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

  if (showDims && (activeShape.type === 'line' || activeShape._isDimension)){
    addDimensionLabel(activeShape);
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
    padding: 2, selectable:true, evented:true,
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
  if (!fn){ toast('Unknown stencil', 'err'); pendingStencil = null; return; }
  try {
    const grp = fn();
    grp.set({
      left:x, top:y, originX:'center', originY:'center',
      perPixelTargetFind:true, padding:2,
    });
    canvas.add(grp);
    canvas.setActiveObject(grp);
    canvas.renderAll();
    toast('Placed: ' + id.replace(/_/g,' '));
  } catch(e){
    toast('Stencil failed: ' + e.message, 'err');
  }
  pendingStencil = null;
  setTool('select');
  $('stencil-panel').classList.remove('open');
}

/* =====================================================================
   11. TOOLS
   ===================================================================== */
function setTool(tool){
  if (currentTool === 'polyline' && polyPreview) finalizePolyline();
  pendingStencil = null;
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
  canvas.setActiveObject(polyPreview);
  canvas.requestRenderAll();
  markDirty(); refreshPanels();
  polyPreview = null; polyPoints = [];
  toast('Polyline finished');
}

/* Stencil panel */
$('tbtn-stencil').onclick = () => $('stencil-panel').classList.toggle('open');
document.querySelectorAll('.stencil').forEach(el => {
  el.onclick = () => {
    pendingStencil = el.dataset.stencil;
    toast(`Click on canvas to place: ${el.dataset.stencil.replace(/_/g,' ')}`);
  };
});

/* =====================================================================
   12. HELPERS
   ===================================================================== */
function hexWithAlpha(hex, alpha){
  if (!hex || hex[0] !== '#') return hex;
  let h = hex.slice(1);
  if (h.length === 3) h = h.split('').map(c=>c+c).join('');
  const r = parseInt(h.slice(0,2),16), g = parseInt(h.slice(2,4),16), b = parseInt(h.slice(4,6),16);
  return `rgba(${r},${g},${b},${alpha})`;
}

/* =====================================================================
   13. HISTORY
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
        o.set({ perPixelTargetFind:true, padding:2 });
      });
      canvas.renderAll();
      refreshPanels();
    });
  } catch(e){ toast('Restore failed: ' + e.message, 'err'); }
}

/* =====================================================================
   14. ACTIONS
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
   15. IMAGE
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
$('tb-paste').onclick = () => { document.body.focus(); toast('Press Ctrl+V'); };
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
   16. VIEW
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
   17. PANELS
   ===================================================================== */
function refreshPanels(){ updateHud(); updateStorageInfo(); }
function updateHud(){
  const n = canvas.getObjects().filter(o => !o.isBackground).length;
  const chip = $('hud-count');
  chip.textContent = n + ' object' + (n===1?'':'s');
  chip.classList.remove('warn','err');
  if (n > 800) chip.classList.add('err');
  else if (n > 300) chip.classList.add('warn');
}
function updateStorageInfo(){
  const el = $('storage-info');
  if (!Storage.available()){ el.textContent = 'storage: unavailable'; return; }
  el.textContent = 'storage: ' + (Storage.bytes()/1024).toFixed(1) + ' KB';
}

/* =====================================================================
   18. EXPORT
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
      version: 1, kind: 'telecom_site_layout',
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
          canvas.renderAll(); refreshPanels();
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
   19. SAVE / RESTORE
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
      });
      canvas.renderAll(); refreshPanels();
      const n = canvas.getObjects().filter(o => !o.isBackground).length;
      toast(`Restored session (${n} object${n===1?'':'s'})`);
    });
    return true;
  } catch(e){ toast('Restore failed', 'err'); return false; }
}

/* =====================================================================
   20. KEYBOARD
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
   21. DIAGNOSTICS
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
    'Stencils: ' + Object.keys(STENCILS).length,
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
   22. TOOLBAR BINDINGS
   ===================================================================== */
$('tb-new').onclick = () => {
  if (!confirm('New site plan? Unsaved work will be lost.')) return;
  canvas.getObjects().forEach(o => canvas.remove(o));
  canvas.setBackgroundImage(null, canvas.renderAll.bind(canvas));
  canvas.setWidth(CW); canvas.setHeight(CH);
  fileName = 'Untitled Site Plan'; $('file-label').textContent = fileName;
  // NOTE: no drop-hint re-show — it's removed permanently
  fitView(); refreshPanels();
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
   23. HEIGHT SYNC
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
   24. BOOT — drop-hint is removed permanently
   ===================================================================== */
(async function boot(){
  try {
    Boot.show('Loading graphics library…');
    await loadFabric();

    Boot.show('Initializing canvas…');
    initCanvas();
    tightenSelectionBoxes();
    buildPalette();

    // ★ Remove the drop-hint element entirely — it no longer exists in DOM
    const hint = document.getElementById('drop-hint');
    if (hint) hint.remove();

    setTimeout(() => fitView(), 100);

    Boot.show('Restoring session…');
    setTimeout(() => {
      loadLocal();
      Boot.ready();
      toast('Ready — open 📦 stencils to place equipment');
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
