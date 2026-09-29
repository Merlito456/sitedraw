import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Cable Routing Studio Pro",
    page_icon="🔌",
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
<title>Cable Routing Studio Pro</title>
<style>
  *{box-sizing:border-box;-webkit-user-select:none;user-select:none}
  html,body{margin:0;height:100%;overflow:hidden;
    font-family:system-ui,-apple-system,"Segoe UI",sans-serif;
    background:#0b1220;color:#e2e8f0;font-size:13px}
  #app{display:flex;height:100vh}

  /* ---------- BOOT / ERROR OVERLAY ---------- */
  #boot{position:fixed;inset:0;z-index:9999;background:#0b1220;
    display:flex;flex-direction:column;align-items:center;justify-content:center;
    color:#8b9dc3;transition:opacity .3s}
  #boot.hidden{opacity:0;pointer-events:none}
  #boot .spinner{width:36px;height:36px;border:3px solid #1f2a44;
    border-top-color:#6366f1;border-radius:50%;animation:spin .8s linear infinite;
    margin-bottom:14px}
  @keyframes spin{to{transform:rotate(360deg)}}
  #boot .err{color:#f87171;font-size:.85rem;max-width:520px;
    text-align:center;line-height:1.6;padding:20px;background:#1c1414;
    border:1px solid #7f1d1d;border-radius:12px;margin-top:12px}
  #boot .err b{color:#fca5a5;display:block;margin-bottom:6px;font-size:1rem}
  #boot .err code{background:#0b1220;padding:2px 6px;border-radius:4px;
    font-family:ui-monospace,monospace;color:#fbbf24}

  /* ---------- SIDEBAR ---------- */
  #sidebar{width:300px;background:#131a2b;border-right:1px solid #1f2a44;
    overflow-y:auto;flex-shrink:0;padding:10px 12px 60px}
  #sidebar::-webkit-scrollbar{width:8px}
  #sidebar::-webkit-scrollbar-thumb{background:#27344f;border-radius:4px}
  #sidebar h3{margin:14px 0 6px;font-size:.7rem;text-transform:uppercase;
    letter-spacing:.09em;color:#7c8db5;font-weight:700}
  #sidebar h3:first-child{margin-top:4px}
  .section{background:#0f1626;border:1px solid #1f2a44;border-radius:10px;
    padding:10px;margin-bottom:8px}

  .btn{display:flex;align-items:center;gap:8px;width:100%;padding:8px 10px;
    margin:3px 0;background:#1c2640;color:#e2e8f0;border:1px solid #2a3a5c;
    border-radius:8px;font-size:.82rem;cursor:pointer;text-align:left;
    transition:.12s;font-family:inherit}
  .btn:hover{background:#243256;border-color:#3b4d75}
  .btn.active{background:linear-gradient(90deg,#2563eb,#7c3aed);
    border-color:transparent;color:#fff;font-weight:600;
    box-shadow:0 3px 12px rgba(99,102,241,.35)}
  .btn.danger:hover{background:#7f1d1d;border-color:#dc2626;color:#fecaca}
  .btn .k{margin-left:auto;font-size:.65rem;color:#7c8db5;
    background:#0b1220;padding:1px 6px;border-radius:4px}
  .btn.active .k{color:#c7d2fe;background:rgba(255,255,255,.15)}
  .row{display:flex;gap:6px}
  .row .btn{flex:1;justify-content:center;text-align:center}

  input[type="color"]{width:100%;height:30px;border:none;background:transparent;
    cursor:pointer;border-radius:6px}
  input[type="range"]{width:100%;accent-color:#6366f1}
  input[type="text"],input[type="number"],select{width:100%;padding:6px 8px;
    border-radius:6px;border:1px solid #2a3a5c;background:#0b1220;
    color:#e2e8f0;font-size:.82rem;font-family:inherit}
  input:focus,select:focus{outline:none;border-color:#6366f1;
    box-shadow:0 0 0 2px rgba(99,102,241,.2)}
  label{font-size:.72rem;color:#8b9dc3;display:flex;
    justify-content:space-between;align-items:center;margin:6px 0 3px}
  label span.val{color:#a5b4fc;font-weight:600}

  .swatches{display:grid;grid-template-columns:repeat(6,1fr);gap:4px;margin-top:4px}
  .swatch{aspect-ratio:1;border-radius:5px;cursor:pointer;
    border:2px solid transparent;transition:.1s}
  .swatch:hover{transform:scale(1.1)}
  .swatch.sel{border-color:#fff;box-shadow:0 0 0 2px #6366f1}

  /* ---------- STAGE ---------- */
  #stage{flex:1;position:relative;overflow:hidden;
    background:repeating-conic-gradient(#111a2e 0 25%,#0b1220 0 50%) 50%/22px 22px}
  #canvas-holder{position:absolute;left:0;top:0;
    transform-origin:0 0;will-change:transform}
  #drop-hint{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);
    display:flex;flex-direction:column;align-items:center;justify-content:center;
    padding:40px 60px;border:3px dashed #2a3a5c;border-radius:20px;
    color:#8b9dc3;font-size:1rem;text-align:center;
    pointer-events:none;z-index:5;max-width:520px}
  #drop-hint b{color:#a5b4fc;font-size:1.15rem;display:block;margin:6px 0}
  #drop-hint .icon{font-size:3.5rem;margin-bottom:8px}
  #drop-hint .sub{font-size:.82rem;color:#66748f;margin-top:8px;line-height:1.5}

  #topbar{position:absolute;top:12px;left:50%;transform:translateX(-50%);
    display:flex;gap:6px;background:rgba(19,26,43,.92);
    backdrop-filter:blur(12px);border:1px solid #2a3a5c;
    padding:6px;border-radius:12px;z-index:20;
    box-shadow:0 8px 24px rgba(0,0,0,.4)}
  #topbar button{background:transparent;border:none;color:#8b9dc3;
    padding:6px 12px;border-radius:7px;cursor:pointer;font-size:.8rem;
    font-family:inherit;display:flex;align-items:center;gap:5px;transition:.12s}
  #topbar button:hover{background:#1c2640;color:#e2e8f0}
  #topbar button.active{background:#2563eb;color:#fff}

  #hud{position:absolute;bottom:12px;right:14px;display:flex;gap:8px;
    align-items:center;z-index:10}
  #hud .chip{background:rgba(19,26,43,.92);backdrop-filter:blur(12px);
    border:1px solid #2a3a5c;padding:6px 12px;border-radius:8px;
    font-size:.72rem;color:#a5b4fc;font-family:ui-monospace,monospace}
  #hud .chip.warn{border-color:#f59e0b;color:#fbbf24}
  #hud .chip.err{border-color:#dc2626;color:#fca5a5}

  #legend,#layers{background:rgba(19,26,43,.94);backdrop-filter:blur(12px);
    border:1px solid #2a3a5c;border-radius:12px;padding:10px 14px;
    z-index:15;box-shadow:0 8px 24px rgba(0,0,0,.4);font-size:.75rem}
  #legend{position:absolute;top:12px;right:14px;min-width:180px;
    max-width:240px;max-height:60vh;overflow-y:auto}
  #layers{position:absolute;bottom:12px;left:14px;max-width:280px;
    max-height:240px;overflow-y:auto}
  #legend h4,#layers h4{margin:0 0 8px;font-size:.72rem;
    text-transform:uppercase;letter-spacing:.08em;color:#7c8db5;
    display:flex;justify-content:space-between;align-items:center}
  #legend .item{display:flex;align-items:center;gap:8px;padding:4px 0;
    border-bottom:1px solid #1a2338}
  #legend .item:last-child{border-bottom:none}
  #legend .dot{width:10px;height:10px;border-radius:50%;flex-shrink:0}
  #legend .name{flex:1;color:#c8d3e8;font-weight:500;
    overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  #legend .cnt{color:#66748f;font-family:ui-monospace,monospace;font-size:.7rem}

  #layers .layer{display:flex;align-items:center;gap:8px;padding:3px 6px;
    border-radius:5px;cursor:pointer;transition:.12s}
  #layers .layer:hover{background:#1c2640}
  #layers .layer.sel{background:#2563eb;color:#fff}
  #layers .lyr-icon{width:14px;text-align:center;font-size:.85rem}
  #layers .lyr-name{flex:1;overflow:hidden;text-overflow:ellipsis;
    white-space:nowrap}

  #toast{position:fixed;bottom:24px;left:50%;
    transform:translateX(-50%) translateY(100px);
    background:#1c2640;border:1px solid #3b4d75;color:#e2e8f0;
    padding:10px 20px;border-radius:10px;font-size:.82rem;
    box-shadow:0 10px 30px rgba(0,0,0,.5);
    transition:transform .25s ease;z-index:100;pointer-events:none;
    max-width:80vw}
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
  <div id="boot-msg">Loading Cable Routing Studio…</div>
  <div id="boot-err" style="display:none" class="err"></div>
</div>

<div id="app" style="display:none">
  <aside id="sidebar">
    <h3>📤 Image Source</h3>
    <div class="section">
      <input type="file" id="file-input" accept="image/*" style="display:none">
      <button class="btn" id="btn-open">📁 <span>Open image</span></button>
      <button class="btn" id="btn-paste">📋 <span>Paste (Ctrl+V)</span></button>
      <button class="btn" id="btn-rmimg">🔄 <span>Remove image</span></button>
      <label>Background opacity <span class="val" id="op-val">100%</span></label>
      <input type="range" id="opacity" min="10" max="100" value="100">
    </div>

    <h3>🖌️ Drawing Tools</h3>
    <div class="section">
      <button class="btn active" data-tool="pen">🖊️ <span>Pen</span><span class="k">P</span></button>
      <button class="btn" data-tool="line">📏 <span>Line</span><span class="k">L</span></button>
      <button class="btn" data-tool="rect">⬛ <span>Rectangle</span><span class="k">R</span></button>
      <button class="btn" data-tool="circle">⭕ <span>Circle</span><span class="k">C</span></button>
      <button class="btn" data-tool="text">🔤 <span>Text</span><span class="k">T</span></button>
      <button class="btn" data-tool="select">🖱️ <span>Select</span><span class="k">V</span></button>
      <button class="btn" data-tool="erase">🧹 <span>Eraser</span><span class="k">E</span></button>
    </div>

    <h3>🎨 Stroke & Fill</h3>
    <div class="section">
      <label>Palette</label>
      <div class="swatches" id="palette"></div>
      <label>Stroke color</label>
      <input type="color" id="stroke-color" value="#ef4444">
      <label>Stroke width <span class="val" id="sw-val">4px</span></label>
      <input type="range" id="stroke-width" min="1" max="25" value="4">
      <label><span>Enable fill</span>
        <input type="checkbox" id="fill-enabled" style="width:auto"></label>
      <input type="color" id="fill-color" value="#ef4444">
    </div>

    <h3>🔤 Text</h3>
    <div class="section">
      <input type="text" id="text-value" value="Outlet A" maxlength="80">
      <label>Font size <span class="val" id="fs-val">22px</span></label>
      <input type="range" id="font-size" min="10" max="72" value="22">
      <div class="row">
        <button class="btn" id="btn-autonum" style="flex:1">🔢 <span>Auto #</span></button>
        <button class="btn" id="btn-resetctr" style="flex:1">↺ <span>Reset</span></button>
      </div>
      <label>Next ID <span class="val" id="counter-val">C-01</span></label>
    </div>

    <h3>🧲 Snap & Grid</h3>
    <div class="section">
      <label><span>Snap to grid</span>
        <input type="checkbox" id="snap-grid" style="width:auto"></label>
      <label>Grid size <span class="val" id="grid-val">20px</span></label>
      <input type="range" id="grid-size" min="5" max="100" value="20">
      <label><span>Snap to endpoints</span>
        <input type="checkbox" id="snap-end" checked style="width:auto"></label>
      <label><span>Show grid</span>
        <input type="checkbox" id="show-grid" style="width:auto"></label>
    </div>

    <h3>📏 Measurements</h3>
    <div class="section">
      <label>px → meters</label>
      <input type="number" id="scale-m" value="0.05" step="0.001" min="0.0001">
      <label>Unit</label>
      <input type="text" id="unit-label" value="m" maxlength="6">
      <label><span>Show lengths</span>
        <input type="checkbox" id="show-length" checked style="width:auto"></label>
    </div>

    <h3>🔧 Actions</h3>
    <div class="section">
      <div class="row">
        <button class="btn" id="btn-undo">↩️ <span>Undo</span></button>
        <button class="btn" id="btn-redo">↪️ <span>Redo</span></button>
      </div>
      <div class="row">
        <button class="btn" id="btn-dup">📋 <span>Copy</span></button>
        <button class="btn" id="btn-del">🗑️ <span>Delete</span></button>
      </div>
      <button class="btn danger" id="btn-clear">💥 <span>Clear drawings</span></button>
    </div>

    <h3>💾 Export</h3>
    <div class="section">
      <label>PNG resolution</label>
      <select id="png-scale">
        <option value="1">1× (screen)</option>
        <option value="2" selected>2× (recommended)</option>
        <option value="3">3× (print)</option>
        <option value="4">4× (poster)</option>
      </select>
      <button class="btn" id="btn-png" style="margin-top:8px">🖼️ <span>Download PNG</span></button>
      <button class="btn" id="btn-json">📄 <span>Download JSON</span></button>
      <button class="btn" id="btn-loadjson">📂 <span>Load JSON…</span></button>
      <input type="file" id="json-input" accept=".json" style="display:none">
    </div>

    <h3>🛡️ Session</h3>
    <div class="section">
      <div style="font-size:.72rem;color:#8b9dc3;line-height:1.6;margin-bottom:6px">
        Autosaved locally every action. Restore survives refresh.
      </div>
      <div class="row">
        <button class="btn" id="btn-export-session">💼 <span>Backup</span></button>
        <button class="btn" id="btn-reset-session">🧨 <span>Reset</span></button>
      </div>
      <div id="storage-info" style="font-size:.7rem;color:#66748f;
        font-family:ui-monospace,monospace;margin-top:6px;text-align:center">
        storage: —
      </div>
    </div>

    <h3>❓ Help</h3>
    <div class="section" style="font-size:.72rem;color:#8b9dc3;line-height:1.6">
      <div><b style="color:#a5b4fc">Zoom:</b> Ctrl + scroll</div>
      <div><b style="color:#a5b4fc">Pan:</b> Space + drag</div>
      <div><b style="color:#a5b4fc">Fit:</b> press <b>F</b></div>
      <div><b style="color:#a5b4fc">Diag:</b> press <b>Ctrl+Shift+D</b></div>
    </div>
  </aside>

  <main id="stage">
    <div id="canvas-holder"><canvas id="c"></canvas></div>

    <div id="drop-hint">
      <div class="icon">📐</div>
      <b>Drop a floor plan or paste a screenshot</b>
      <div class="sub">
        Press <b style="color:#a5b4fc">Ctrl+V</b> anywhere ·<br>
        drag &amp; drop · or click <b style="color:#a5b4fc">Open image</b>
      </div>
    </div>

    <div id="topbar">
      <button id="zoom-fit">🎯 Fit</button>
      <button id="zoom-in">＋</button>
      <button id="zoom-out">－</button>
      <button id="zoom-lvl" style="pointer-events:none;min-width:52px;justify-content:center">100%</button>
      <button id="toggle-legend" class="active">📊 Legend</button>
      <button id="toggle-layers" class="active">🧱 Layers</button>
    </div>

    <div id="legend">
      <h4>Cable Legend <button id="legend-close" style="background:none;
        border:none;color:#7c8db5;cursor:pointer;font-size:.9rem">✕</button></h4>
      <div id="legend-items"></div>
    </div>

    <div id="layers">
      <h4>Layers <span id="lyr-count" style="color:#66748f"></span></h4>
      <div id="layers-list"></div>
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
   0. GLOBAL ERROR BOUNDARY
   ===================================================================== */
const Boot = {
  show(msg){ document.getElementById('boot-msg').textContent = msg; },
  error(title, detail){
    const b = document.getElementById('boot');
    b.classList.remove('hidden');
    document.getElementById('boot-msg').style.display = 'none';
    const e = document.getElementById('boot-err');
    e.style.display = 'block';
    e.innerHTML = `<b>⚠️ ${title}</b>${detail}`;
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
  console.error('[unhandled promise]', e.reason);
  try { toast('Async error: ' + (e.reason?.message || e.reason), 'err'); } catch(_) {}
});

/* =====================================================================
   1. FABRIC.JS LOADER WITH CDN FALLBACK CHAIN
   ===================================================================== */
const FABRIC_CDNS = [
  'https://cdn.jsdelivr.net/npm/fabric@5.3.0/dist/fabric.min.js',
  'https://unpkg.com/fabric@5.3.0/dist/fabric.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/fabric.js/5.3.0/fabric.min.js',
];

function loadFabric(i = 0){
  return new Promise((resolve, reject) => {
    if (window.fabric) return resolve();
    if (i >= FABRIC_CDNS.length){
      return reject(new Error('All Fabric.js CDNs failed'));
    }
    Boot.show(`Loading graphics library (${i+1}/${FABRIC_CDNS.length})…`);
    const s = document.createElement('script');
    s.src = FABRIC_CDNS[i];
    s.async = true;
    const timer = setTimeout(() => { s.onerror(); }, 8000);
    s.onload = () => { clearTimeout(timer); window.fabric ? resolve() : reject(new Error('Script loaded but fabric undefined')); };
    s.onerror = () => { clearTimeout(timer); s.remove(); loadFabric(i+1).then(resolve, reject); };
    document.head.appendChild(s);
  });
}

/* =====================================================================
   2. SAFE STORAGE WRAPPER (localStorage can throw or be corrupt)
   ===================================================================== */
const Storage = {
  KEY_DATA: 'cable_studio_v2',
  KEY_CTR:  'cable_studio_ctr_v2',
  KEY_QUAR: 'cable_studio_quarantine',

  available(){
    try {
      const k = '__t' + Math.random();
      localStorage.setItem(k, '1');
      localStorage.removeItem(k);
      return true;
    } catch(_) { return false; }
  },
  get(key){
    try { return localStorage.getItem(key); } catch(_) { return null; }
  },
  set(key, val){
    try { localStorage.setItem(key, val); return true; }
    catch(e){
      // quota exceeded → quarantine the payload
      try { localStorage.setItem(this.KEY_QUAR, JSON.stringify({
        ts: Date.now(), size: String(val).length, err: String(e)
      })); } catch(_){}
      return false;
    }
  },
  del(key){ try { localStorage.removeItem(key); } catch(_){} },
  bytes(){
    if (!this.available()) return 0;
    let t = 0;
    for (let i = 0; i < localStorage.length; i++){
      const k = localStorage.key(i);
      t += (k.length + (localStorage.getItem(k) || '').length) * 2;
    }
    return t;
  }
};

/* =====================================================================
   3. SCHEMA VALIDATION FOR IMPORTED JSON
   ===================================================================== */
function validateImport(obj){
  if (!obj || typeof obj !== 'object') return { ok:false, msg:'Not a JSON object' };
  const fab = obj.fabric || obj;
  if (!fab || typeof fab !== 'object') return { ok:false, msg:'Missing fabric payload' };
  if (!Array.isArray(fab.objects)) return { ok:false, msg:'Missing objects array' };
  if (fab.objects.length > 5000) return { ok:false, msg:'Too many objects (>5000)' };
  const okTypes = ['path','line','rect','circle','i-text','text','textbox','group','image'];
  for (const o of fab.objects){
    if (!o || typeof o !== 'object') return { ok:false, msg:'Object entry invalid' };
    if (o.type && !okTypes.includes(o.type) &&
        !o.isBackground && !o._isAnnotation){
      // Just warn, don't reject — Fabric may have newer types
      console.warn('[import] unknown type', o.type);
    }
  }
  if (typeof fab.width !== 'number' && typeof fab.width !== 'undefined'){
    return { ok:false, msg:'Canvas width must be numeric' };
  }
  return { ok:true };
}

/* =====================================================================
   4. IMAGE DOWNSCALE GUARD (avoid 20K×20K browser freezes)
   ===================================================================== */
const MAX_IMAGE_DIM = 4096;
function downscaleIfNeeded(dataUrl){
  return new Promise((resolve) => {
    const im = new Image();
    im.onload = () => {
      const w = im.width, h = im.height;
      if (w <= MAX_IMAGE_DIM && h <= MAX_IMAGE_DIM){
        return resolve({ dataUrl, w, h, scaled:false });
      }
      const k = MAX_IMAGE_DIM / Math.max(w, h);
      const nw = Math.round(w * k), nh = Math.round(h * k);
      const cv = document.createElement('canvas');
      cv.width = nw; cv.height = nh;
      cv.getContext('2d').drawImage(im, 0, 0, nw, nh);
      resolve({ dataUrl: cv.toDataURL('image/png'), w:nw, h:nh, scaled:true, from:{w,h} });
    };
    im.onerror = () => resolve({ dataUrl, w:0, h:0, scaled:false, err:true });
    im.src = dataUrl;
  });
}

/* =====================================================================
   5. UI HELPERS
   ===================================================================== */
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
   6. STATE
   ===================================================================== */
let canvas, currentTool = 'pen', drawing = false, startPt = null, activeShape = null;
let undoStack = [], redoStack = [];
let cableCounter = 0;
let view = { zoom: 1, x: 0, y: 0 };
let spaceDown = false, panning = false, panStart = null;
let pasteLock = 0;             // debounce
let lastSel = null;
const CW = 1400, CH = 900;
const PALETTE = ['#ef4444','#f97316','#eab308','#22c55e','#06b6d4','#3b82f6',
                 '#8b5cf6','#ec4899','#78716c','#111827','#10b981','#f43f5e'];
const CABLE_COLORS = {
  '#ef4444':'Data / CAT6','#f97316':'Fire Alarm','#eab308':'Fiber',
  '#22c55e':'CCTV / IP','#06b6d4':'Voice','#3b82f6':'Power',
  '#8b5cf6':'Access Control','#ec4899':'Wireless AP','#78716c':'Spare',
  '#111827':'Conduit','#10b981':'Grounding','#f43f5e':'Emergency',
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
  canvas.on('object:added',    () => { markDirty(); refreshPanels(); });
  canvas.on('object:modified', () => { markDirty(); refreshPanels(); });
  canvas.on('object:removed',  () => { refreshPanels(); });
  canvas.on('selection:created', refreshPanels);
  canvas.on('selection:updated', refreshPanels);
  canvas.on('selection:cleared', () => { lastSel = null; refreshPanels(); });

  canvas.on('mouse:down', opt => {
    if (currentTool === 'erase' && opt.target){
      canvas.remove(opt.target);
      toast('Erased');
    }
  });
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
  cx.strokeStyle = '#e5e7eb'; cx.lineWidth = 1;
  cx.beginPath();
  cx.moveTo(size - .5, 0); cx.lineTo(size - .5, size);
  cx.moveTo(0, size - .5); cx.lineTo(size, size - .5);
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
  if ($('snap-end').checked && currentTool !== 'pen'){
    const TOL = 14;
    let best = null, bestD = TOL;
    for (const o of canvas.getObjects()){
      if (o === activeShape || o.isBackground) continue;
      let pts = [];
      if (o.type === 'line') pts = [{x:o.x1,y:o.y1},{x:o.x2,y:o.y2}];
      else if (o.type === 'rect'){
        const l = o.left, t = o.top, w = o.width * o.scaleX, h = o.height * o.scaleY;
        pts = [{x:l,y:t},{x:l+w,y:t},{x:l,y:t+h},{x:l+w,y:t+h}];
      } else if (o.type === 'circle'){
        pts = [{x:o.left,y:o.top},{x:o.left+2*o.radius,y:o.top+2*o.radius}];
      } else {
        const b = o.getBoundingRect(true, true);
        pts = [{x:b.left,y:b.top},{x:b.left+b.width,y:b.top},
               {x:b.left,y:b.top+b.height},{x:b.left+b.width,y:b.top+b.height}];
      }
      for (const pt of pts){
        const tp = fabric.util.transformPoint(pt, o.calcTransformMatrix());
        const d = Math.hypot(tp.x - p.x, tp.y - p.y);
        if (d < bestD){ bestD = d; best = tp; }
      }
    }
    if (best){ x = best.x; y = best.y; }
  }
  return { x, y };
}

/* =====================================================================
   10. DRAW
   ===================================================================== */
function onDown(opt){
  if (spaceDown){
    panning = true;
    panStart = { x: opt.e.clientX, y: opt.e.clientY };
    return;
  }
  if (currentTool === 'select' || currentTool === 'erase') return;

  const p = snapPt(canvas.getPointer(opt.e));
  drawing = true; startPt = p;

  const sColor = $('stroke-color').value;
  const sWidth = Math.max(1, parseInt($('stroke-width').value) || 4);
  const fEnabled = $('fill-enabled').checked;
  const fColor = fEnabled ? $('fill-color').value + '55' : 'transparent';

  if (currentTool === 'pen'){
    activeShape = new fabric.Path(`M ${p.x} ${p.y}`, {
      stroke: sColor, strokeWidth: sWidth, fill: '',
      strokeLineCap: 'round', strokeLineJoin: 'round',
      selectable: false, evented: false,
    });
    canvas.add(activeShape);
  } else if (currentTool === 'line'){
    activeShape = new fabric.Line([p.x,p.y,p.x,p.y], {
      stroke: sColor, strokeWidth: sWidth,
      selectable: false, evented: false,
    });
    canvas.add(activeShape);
  } else if (currentTool === 'rect'){
    activeShape = new fabric.Rect({
      left: p.x, top: p.y, width: 1, height: 1,
      fill: fColor, stroke: sColor, strokeWidth: sWidth,
      selectable: false, evented: false,
    });
    canvas.add(activeShape);
  } else if (currentTool === 'circle'){
    activeShape = new fabric.Circle({
      left: p.x, top: p.y, radius: 1,
      fill: fColor, stroke: sColor, strokeWidth: sWidth,
      selectable: false, evented: false, originX:'left', originY:'top',
    });
    canvas.add(activeShape);
  } else if (currentTool === 'text'){
    const label = new fabric.IText($('text-value').value || 'Label', {
      left: p.x, top: p.y,
      fill: sColor, fontSize: parseInt($('font-size').value),
      fontFamily: 'system-ui, sans-serif', fontWeight: '600',
    });
    canvas.add(label); canvas.setActiveObject(label);
    markDirty(); refreshPanels();
    drawing = false; activeShape = null;
    toast('Text added');
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
  if (!drawing || !activeShape) return;

  const p = snapPt(raw);

  if (currentTool === 'pen'){
    activeShape.path.push(['L', p.x, p.y]);
    activeShape.dirty = true;
  } else if (currentTool === 'line'){
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

  if (currentTool === 'line' && $('show-length').checked){
    const m = $('measure');
    const dx = p.x - startPt.x, dy = p.y - startPt.y;
    const px = Math.hypot(dx, dy);
    const meters = (px * parseFloat($('scale-m').value || 0.05)).toFixed(2);
    m.textContent = `${meters} ${$('unit-label').value}  ·  ${Math.round(px)}px`;
    m.style.left = (opt.e.clientX + 14) + 'px';
    m.style.top  = (opt.e.clientY + 14) + 'px';
    m.style.display = 'block';
  }
  canvas.requestRenderAll();
}

function onUp(){
  if (panning){ panning = false; panStart = null; return; }
  if (!drawing) return;
  drawing = false;
  $('measure').style.display = 'none';

  if (!activeShape){ return; }

  // Reject zero-size accidental clicks
  try {
    if (activeShape.type === 'line'){
      const len = Math.hypot(activeShape.x2 - activeShape.x1,
                             activeShape.y2 - activeShape.y1);
      if (len < 3){ canvas.remove(activeShape); activeShape = null; return; }
    }
    if (activeShape.type === 'rect'){
      if (activeShape.width < 3 || activeShape.height < 3){
        canvas.remove(activeShape); activeShape = null; return;
      }
    }
    if (activeShape.type === 'circle'){
      if (activeShape.radius < 3){ canvas.remove(activeShape); activeShape = null; return; }
    }
  } catch(_) {}

  activeShape.set({ selectable: true, evented: true });
  canvas.setActiveObject(activeShape);

  if (activeShape.type === 'line' && $('show-length').checked){
    const dx = activeShape.x2 - activeShape.x1;
    const dy = activeShape.y2 - activeShape.y1;
    const len = Math.hypot(dx, dy) * parseFloat($('scale-m').value || 0.05);
    const mid = { x:(activeShape.x1 + activeShape.x2)/2,
                  y:(activeShape.y1 + activeShape.y2)/2 };
    const txt = new fabric.IText(len.toFixed(2) + ' ' + $('unit-label').value, {
      left: mid.x, top: mid.y - 14,
      fontSize: 12, fill: activeShape.stroke,
      fontFamily: 'ui-monospace, monospace',
      backgroundColor: 'rgba(255,255,255,.85)',
      padding: 2, selectable: true, evented: true,
    });
    txt._isAnnotation = true;
    canvas.add(txt);
  }

  activeShape = null;
  canvas.requestRenderAll();
  markDirty(); refreshPanels();
}

/* =====================================================================
   11. TOOLS
   ===================================================================== */
function setTool(tool){
  currentTool = tool;
  document.querySelectorAll('[data-tool]').forEach(b =>
    b.classList.toggle('active', b.dataset.tool === tool));
  canvas.selection = tool === 'select';
  canvas.forEachObject(o => {
    o.selectable = tool === 'select';
    o.evented = tool !== 'pen';
  });
  document.body.style.cursor = tool === 'select' ? 'default' : 'crosshair';
}
document.querySelectorAll('[data-tool]').forEach(b => {
  b.onclick = () => setTool(b.dataset.tool);
});

/* =====================================================================
   12. PALETTE
   ===================================================================== */
function buildPalette(){
  const wrap = $('palette');
  wrap.innerHTML = '';
  PALETTE.forEach(c => {
    const sw = document.createElement('div');
    sw.className = 'swatch';
    sw.style.background = c;
    if (c.toLowerCase() === $('stroke-color').value.toLowerCase())
      sw.classList.add('sel');
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
   13. HISTORY
   ===================================================================== */
const MAX_HISTORY = 80;
const MAX_HISTORY_BYTES = 4_000_000; // ~4 MB of JSON strings

function serialize(){
  try {
    return JSON.stringify({
      v: 2,
      fabric: canvas.toJSON(['selectable','evented','isBackground',
                             '_isCable','_isAnnotation']),
    });
  } catch(e){
    console.warn('serialize failed', e);
    return '{"v":2,"fabric":{"objects":[]}}';
  }
}

let saveTimer;
function markDirty(){
  clearTimeout(saveTimer);
  saveTimer = setTimeout(saveLocal, 800);
  pushHistory();
}

function pushHistory(){
  const j = serialize();
  if (undoStack[undoStack.length - 1] === j) return;
  undoStack.push(j);
  // Byte cap
  while (undoStack.length > MAX_HISTORY ||
         undoStack.reduce((a,s)=>a+s.length,0) > MAX_HISTORY_BYTES){
    undoStack.shift();
  }
  redoStack = [];
  updateHud();
}

function undo(){
  if (undoStack.length < 2){ toast('Nothing to undo', 'warn'); return; }
  redoStack.push(undoStack.pop());
  applySnapshot(undoStack[undoStack.length - 1]);
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
        o.selectable = currentTool === 'select';
        o.evented = currentTool !== 'pen';
      });
      canvas.renderAll();
      refreshPanels();
    });
  } catch(e){
    toast('Snapshot restore failed: ' + e.message, 'err');
  }
}

/* =====================================================================
   14. ACTIONS
   ===================================================================== */
function clearAll(){
  const n = canvas.getObjects().length;
  if (!n){ toast('Nothing to clear', 'warn'); return; }
  if (!confirm(`Clear ${n} object(s)?`)) return;
  canvas.getObjects().forEach(o => canvas.remove(o));
  refreshPanels(); toast('Cleared');
}
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
      c.set({ left: (o.left || 0) + 20, top: (o.top || 0) + 20 });
      canvas.add(c);
    });
  });
  canvas.discardActiveObject();
  refreshPanels(); toast('Duplicated');
}
function autoNumberNext(){
  cableCounter++;
  $('text-value').value = 'C-' + String(cableCounter).padStart(2, '0');
  $('counter-val').textContent = 'C-' + String(cableCounter + 1).padStart(2, '0');
  Storage.set(Storage.KEY_CTR, String(cableCounter));
  toast('Next: ' + $('text-value').value);
}
function resetCounter(){
  cableCounter = 0;
  $('counter-val').textContent = 'C-01';
  Storage.set(Storage.KEY_CTR, '0');
  toast('Counter reset');
}

/* =====================================================================
   15. IMAGE LOADING WITH GUARDRAILS
   ===================================================================== */
async function loadImage(dataUrl, name){
  if (!dataUrl || typeof dataUrl !== 'string' || !dataUrl.startsWith('data:image')){
    toast('Invalid image data', 'err'); return;
  }
  try {
    const r = await downscaleIfNeeded(dataUrl);
    if (r.err){ toast('Could not decode image', 'err'); return; }
    if (r.scaled){
      toast(`Downscaled ${r.from.w}×${r.from.h} → ${r.w}×${r.h}`, 'warn');
    }
    fabric.Image.fromURL(r.dataUrl, img => {
      const s = Math.min(CW / img.width, CH / img.height, 1);
      img.set({
        left: 0, top: 0, scaleX: s, scaleY: s,
        selectable: false, evented: false, isBackground: true,
        opacity: parseInt($('opacity').value) / 100,
      });
      canvas.setWidth(img.width * s);
      canvas.setHeight(img.height * s);
      canvas.setBackgroundImage(img, canvas.renderAll.bind(canvas));
      $('drop-hint').style.display = 'none';
      fitView();
      toast(`Loaded ${name || 'image'} (${img.width}×${img.height})`);
    }, { crossOrigin: 'anonymous' });
  } catch(e){
    toast('Image load failed: ' + e.message, 'err');
  }
}

$('file-input').onchange = e => {
  const f = e.target.files[0];
  if (!f) return;
  if (f.size > 30 * 1024 * 1024){
    toast('File too large (>30 MB)', 'err'); return;
  }
  const r = new FileReader();
  r.onerror = () => toast('File read failed', 'err');
  r.onload = ev => loadImage(ev.target.result, f.name);
  r.readAsDataURL(f);
};

document.addEventListener('paste', e => {
  const now = Date.now();
  if (now - pasteLock < 500) return;   // debounce duplicate events
  const items = (e.clipboardData || {}).items || [];
  for (const it of items){
    if (it.kind === 'file' && it.type.startsWith('image/')){
      pasteLock = now;
      const r = new FileReader();
      r.onload = ev => loadImage(ev.target.result, 'pasted');
      r.onerror = () => toast('Paste read failed', 'err');
      r.readAsDataURL(it.getAsFile());
      e.preventDefault();
      return;
    }
  }
});

document.addEventListener('dragover', e => e.preventDefault());
document.addEventListener('drop', e => {
  e.preventDefault();
  const f = e.dataTransfer.files[0];
  if (!f) return;
  if (!f.type.startsWith('image/')){ toast('Drop an image file', 'warn'); return; }
  if (f.size > 30 * 1024 * 1024){ toast('File too large (>30 MB)', 'err'); return; }
  const r = new FileReader();
  r.onerror = () => toast('Drop read failed', 'err');
  r.onload = ev => loadImage(ev.target.result, f.name);
  r.readAsDataURL(f);
});

function clearImage(){
  canvas.setBackgroundImage(null, canvas.renderAll.bind(canvas));
  canvas.setWidth(CW); canvas.setHeight(CH);
  $('drop-hint').style.display = 'flex';
  toast('Image removed');
}
function focusPaste(){ document.body.focus(); toast('Press Ctrl+V / ⌘+V'); }

$('opacity').oninput = e => {
  $('op-val').textContent = e.target.value + '%';
  const bg = canvas.backgroundImage;
  if (bg){ bg.set('opacity', parseInt(e.target.value) / 100); canvas.renderAll(); }
};

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
  cx = cx ?? stage.width / 2;
  cy = cy ?? stage.height / 2;
  const prev = view.zoom;
  view.zoom = Math.max(0.1, Math.min(8, view.zoom * f));
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
  zoomBy(e.deltaY < 0 ? 1.1 : 1 / 1.1, e.clientX - r.left, e.clientY - r.top);
}, { passive: false });

$('stage').addEventListener('mousedown', e => {
  if (spaceDown && e.button === 0){
    panning = true;
    panStart = { x: e.clientX, y: e.clientY };
    e.preventDefault();
  }
});
window.addEventListener('mouseup', () => {
  if (panning){ panning = false; panStart = null; }
});
window.addEventListener('mousemove', e => {
  if (!panning || !panStart) return;
  view.x += e.clientX - panStart.x;
  view.y += e.clientY - panStart.y;
  panStart = { x: e.clientX, y: e.clientY };
  applyView();
});

/* =====================================================================
   17. PANELS
   ===================================================================== */
function refreshPanels(){ refreshLegend(); refreshLayers(); updateHud(); updateStorageInfo(); }

function refreshLegend(){
  const items = {};
  canvas.getObjects().forEach(o => {
    if (o.isBackground || o._isAnnotation) return;
    const col = String(o.stroke || o.fill || '#666').toLowerCase();
    const key = col.startsWith('#') ? col.slice(0, 7) : col;
    items[key] = (items[key] || 0) + 1;
  });
  const wrap = $('legend-items');
  wrap.innerHTML = '';
  const keys = Object.keys(items);
  if (!keys.length){
    wrap.innerHTML = '<div style="color:#66748f;font-size:.72rem;padding:4px 0">No cables yet</div>';
    return;
  }
  keys.forEach(k => {
    const el = document.createElement('div');
    el.className = 'item';
    el.innerHTML = `<span class="dot" style="background:${k}"></span>
                    <span class="name">${CABLE_COLORS[k] || 'Cable'}</span>
                    <span class="cnt">${items[k]}</span>`;
    wrap.appendChild(el);
  });
}

function refreshLayers(){
  const objs = canvas.getObjects().filter(o => !o.isBackground);
  const list = $('layers-list');
  list.innerHTML = '';
  $('lyr-count').textContent = '(' + objs.length + ')';
  const active = canvas.getActiveObject();
  objs.slice().reverse().forEach(o => {
    const el = document.createElement('div');
    el.className = 'layer' + (active === o ? ' sel' : '');
    const icon = { path:'🖊️', line:'📏', rect:'⬛', circle:'⭕',
                   'i-text':'🔤', text:'🔤', textbox:'🔤', group:'📦' }[o.type] || '▪';
    const name = (o.text || CABLE_COLORS[String(o.stroke || '').toLowerCase()] || o.type || '?').slice(0, 22);
    el.innerHTML = `<span class="lyr-icon">${icon}</span>
                    <span class="lyr-name">${name}</span>`;
    el.onclick = () => { canvas.setActiveObject(o); canvas.renderAll(); refreshLayers(); };
    el.ondblclick = () => { o.visible = false; canvas.renderAll(); refreshLayers(); toast('Hidden'); };
    list.appendChild(el);
  });
  if (!objs.length){
    list.innerHTML = '<div style="color:#66748f;font-size:.7rem;padding:4px 0">No objects</div>';
  }
}

function updateHud(){
  const n = canvas.getObjects().filter(o => !o.isBackground).length;
  const chip = $('hud-count');
  chip.textContent = n + ' object' + (n === 1 ? '' : 's');
  chip.classList.remove('warn', 'err');
  if (n > 800) chip.classList.add('err');
  else if (n > 300) chip.classList.add('warn');
}

function updateStorageInfo(){
  const bytes = Storage.bytes();
  const el = $('storage-info');
  if (!Storage.available()){ el.textContent = 'storage: unavailable'; return; }
  el.textContent = 'storage: ' + (bytes / 1024).toFixed(1) + ' KB';
}

function toggleLegend(){
  const l = $('legend');
  const show = l.style.display === 'none';
  l.style.display = show ? 'block' : 'none';
  $('toggle-legend').classList.toggle('active', show);
}
function toggleLayers(){
  const l = $('layers');
  const show = l.style.display === 'none';
  l.style.display = show ? 'block' : 'none';
  $('toggle-layers').classList.toggle('active', show);
}

/* =====================================================================
   18. EXPORT
   ===================================================================== */
function download(blob, name){
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = name;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 4000);
}

function exportPNG(){
  try {
    const scale = Math.max(1, Math.min(4, parseInt($('png-scale').value) || 1));
    const sel = canvas.getActiveObject();
    canvas.discardActiveObject();
    canvas.renderAll();

    const gridOn = $('show-grid').checked;
    const savedBgColor = canvas.backgroundColor;
    if (gridOn){ canvas.setBackgroundColor('transparent', () => {}); canvas.renderAll(); }

    const url = canvas.toDataURL({ format:'png', multiplier:scale, quality:1 });

    if (gridOn){ drawGridOverlay(); canvas.backgroundColor = savedBgColor; }
    if (sel) canvas.setActiveObject(sel);
    canvas.renderAll();

    fetch(url).then(r => r.blob()).then(b => {
      download(b, `cable_routing_${scale}x_${Date.now()}.png`);
      toast(`PNG exported at ${scale}×`);
    }).catch(e => toast('Export failed: ' + e.message, 'err'));
  } catch(e){
    toast('Export error: ' + e.message, 'err');
  }
}

function exportJSON(){
  try {
    const data = {
      version: 2,
      exported: new Date().toISOString(),
      canvas: { width: canvas.getWidth(), height: canvas.getHeight() },
      scale: { m_per_px: parseFloat($('scale-m').value || 0.05),
               unit: $('unit-label').value || 'm' },
      counter: cableCounter,
      fabric: canvas.toJSON(['selectable','evented','isBackground',
                             '_isCable','_isAnnotation']),
    };
    download(new Blob([JSON.stringify(data, null, 2)], { type:'application/json' }),
             'annotations_' + Date.now() + '.json');
    toast('JSON exported');
  } catch(e){
    toast('JSON export failed: ' + e.message, 'err');
  }
}

function loadJSON(){ $('json-input').click(); }
$('json-input').onchange = e => {
  const f = e.target.files[0];
  if (!f) return;
  if (f.size > 50 * 1024 * 1024){ toast('JSON too large (>50 MB)', 'err'); return; }
  const r = new FileReader();
  r.onerror = () => toast('JSON read failed', 'err');
  r.onload = ev => {
    let parsed;
    try { parsed = JSON.parse(ev.target.result); }
    catch(err){ toast('Invalid JSON: ' + err.message, 'err'); return; }
    const v = validateImport(parsed);
    if (!v.ok){ toast('Import rejected: ' + v.msg, 'err'); return; }
    if (parsed.scale){
      $('scale-m').value = parsed.scale.m_per_px ?? 0.05;
      $('unit-label').value = parsed.scale.unit || 'm';
    }
    if (typeof parsed.counter === 'number'){
      cableCounter = parsed.counter;
      $('counter-val').textContent = 'C-' + String(cableCounter + 1).padStart(2, '0');
    }
    const bg = canvas.backgroundImage;
    try {
      canvas.loadFromJSON(parsed.fabric || parsed, () => {
        if (bg) canvas.setBackgroundImage(bg, canvas.renderAll.bind(canvas));
        canvas.renderAll();
        refreshPanels();
        toast('Annotations loaded');
      });
    } catch(err){
      toast('Load failed: ' + err.message, 'err');
    }
  };
  r.readAsText(f);
};

/* =====================================================================
   19. STORAGE / AUTOSAVE
   ===================================================================== */
function saveLocal(){
  if (!Storage.available()) return;
  const ok = Storage.set(Storage.KEY_DATA, serialize());
  Storage.set(Storage.KEY_CTR, String(cableCounter));
  if (!ok) toast('Autosave failed — storage full', 'warn');
  updateStorageInfo();
}

function loadLocal(){
  if (!Storage.available()) return false;
  const j = Storage.get(Storage.KEY_DATA);
  if (!j) return false;
  let parsed;
  try { parsed = JSON.parse(j); }
  catch(e){
    // Corrupt — quarantine & wipe
    Storage.set(Storage.KEY_QUAR, j.slice(0, 2000));
    Storage.del(Storage.KEY_DATA);
    toast('Corrupt session cleared', 'warn');
    return false;
  }
  const v = validateImport(parsed);
  if (!v.ok){
    Storage.del(Storage.KEY_DATA);
    toast('Session rejected: ' + v.msg, 'warn');
    return false;
  }
  const cnt = parseInt(Storage.get(Storage.KEY_CTR) || '0');
  if (!Number.isNaN(cnt)) cableCounter = cnt;
  $('counter-val').textContent = 'C-' + String(cableCounter + 1).padStart(2, '0');

  try {
    canvas.loadFromJSON(parsed.fabric || parsed, () => {
      canvas.renderAll();
      refreshPanels();
      const n = canvas.getObjects().filter(o => !o.isBackground).length;
      toast(`Session restored (${n} object${n === 1 ? '' : 's'})`);
    });
    return true;
  } catch(e){
    toast('Restore failed: ' + e.message, 'err');
    return false;
  }
}

/* =====================================================================
   20. KEYBOARD
   ===================================================================== */
document.addEventListener('keydown', e => {
  const editing = e.target.tagName === 'INPUT' || e.target.isContentEditable;

  // Diagnostics: Ctrl+Shift+D
  if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key.toLowerCase() === 'd'){
    e.preventDefault();
    runDiagnostics();
    return;
  }

  if (editing) return;

  if (e.code === 'Space'){
    spaceDown = true;
    document.body.style.cursor = 'grab';
    e.preventDefault();
  }

  const k = e.key.toLowerCase();
  if (e.ctrlKey || e.metaKey){
    if (k === 'z'){ e.preventDefault(); e.shiftKey ? redo() : undo(); }
    else if (k === 'y'){ e.preventDefault(); redo(); }
    else if (k === 'd'){ e.preventDefault(); duplicateSel(); }
    else if (k === 'a'){
      e.preventDefault();
      canvas.discardActiveObject();
      const objs = canvas.getObjects().filter(o => !o.isBackground);
      if (!objs.length){ toast('Nothing to select', 'warn'); return; }
      const sel = new fabric.ActiveSelection(objs, { canvas });
      canvas.setActiveObject(sel); canvas.renderAll();
    }
    return;
  }

  if (e.key === 'Delete' || e.key === 'Backspace'){ e.preventDefault(); deleteSel(); }
  else if (k === 'v') setTool('select');
  else if (k === 'p') setTool('pen');
  else if (k === 'l') setTool('line');
  else if (k === 'r') setTool('rect');
  else if (k === 'c') setTool('circle');
  else if (k === 't') setTool('text');
  else if (k === 'e') setTool('erase');
  else if (k === 'f') fitView();
  else if (k === 'escape'){ canvas.discardActiveObject(); canvas.renderAll(); }
});
document.addEventListener('keyup', e => {
  if (e.code === 'Space'){
    spaceDown = false;
    document.body.style.cursor = currentTool === 'select' ? 'default' : 'crosshair';
  }
});
// Cleanup if window loses focus mid-draw
window.addEventListener('blur', () => {
  spaceDown = false; panning = false; panStart = null;
  if (drawing){ drawing = false; $('measure').style.display = 'none'; }
});
document.addEventListener('visibilitychange', () => {
  if (document.hidden){
    spaceDown = false; panning = false; drawing = false;
    $('measure').style.display = 'none';
  }
});

/* =====================================================================
   21. DIAGNOSTICS
   ===================================================================== */
function runDiagnostics(){
  const lines = [];
  lines.push('Cable Routing Studio — Diagnostics');
  lines.push('Time: ' + new Date().toISOString());
  lines.push('Fabric.js: ' + (window.fabric ? '✓ ' + fabric.version : '✗ MISSING'));
  lines.push('localStorage: ' + (Storage.available() ? '✓ available' : '✗ blocked'));
  lines.push('Storage bytes: ' + Storage.bytes());
  lines.push('Canvas: ' + canvas.getWidth() + '×' + canvas.getHeight());
  lines.push('Objects: ' + canvas.getObjects().length);
  lines.push('Undo depth: ' + undoStack.length);
  lines.push('Redo depth: ' + redoStack.length);
  lines.push('View: zoom=' + view.zoom.toFixed(2) + ' x=' + Math.round(view.x) + ' y=' + Math.round(view.y));
  lines.push('User agent: ' + navigator.userAgent);
  if (Storage.get(Storage.KEY_QUAR)){
    lines.push('⚠ Last quarantine: ' + Storage.get(Storage.KEY_QUAR));
  }
  const txt = lines.join('\n');
  console.log(txt);
  try {
    download(new Blob([txt], { type:'text/plain' }), 'diagnostics_' + Date.now() + '.txt');
    toast('Diagnostics downloaded');
  } catch(e){ toast('Diag: see console', 'warn'); }
}

/* =====================================================================
   22. SESSION BACKUP / RESET
   ===================================================================== */
$('btn-export-session').onclick = () => exportJSON();
$('btn-reset-session').onclick = () => {
  if (!confirm('Reset local session? This clears autosaved work.')) return;
  Storage.del(Storage.KEY_DATA);
  Storage.del(Storage.KEY_CTR);
  Storage.del(Storage.KEY_QUAR);
  toast('Session reset');
  updateStorageInfo();
};

/* =====================================================================
   23. BINDINGS
   ===================================================================== */
$('stroke-width').oninput = e => $('sw-val').textContent = e.target.value + 'px';
$('font-size').oninput    = e => $('fs-val').textContent = e.target.value + 'px';
$('grid-size').oninput    = e => { $('grid-val').textContent = e.target.value + 'px'; drawGridOverlay(); };
$('show-grid').onchange   = drawGridOverlay;
$('stroke-color').oninput = () => {
  document.querySelectorAll('.swatch').forEach(s => {
    s.classList.toggle('sel',
      s.style.background === $('stroke-color').value ||
      s.style.backgroundColor === $('stroke-color').value);
  });
};

$('btn-open').onclick = () => $('file-input').click();
$('btn-paste').onclick = focusPaste;
$('btn-rmimg').onclick = clearImage;
$('btn-undo').onclick = undo;
$('btn-redo').onclick = redo;
$('btn-dup').onclick = duplicateSel;
$('btn-del').onclick = deleteSel;
$('btn-clear').onclick = clearAll;
$('btn-autonum').onclick = autoNumberNext;
$('btn-resetctr').onclick = resetCounter;
$('btn-png').onclick = exportPNG;
$('btn-json').onclick = exportJSON;
$('btn-loadjson').onclick = loadJSON;
$('zoom-fit').onclick = fitView;
$('zoom-in').onclick = () => zoomBy(1.2);
$('zoom-out').onclick = () => zoomBy(1 / 1.2);
$('toggle-legend').onclick = toggleLegend;
$('toggle-layers').onclick = toggleLayers;
$('legend-close').onclick = toggleLegend;

/* =====================================================================
   24. IFRAME / STREAMLIT HEIGHT SYNC
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
setInterval(syncFrameHeight, 3000);   // periodic safety net

/* =====================================================================
   25. BOOT SEQUENCE
   ===================================================================== */
(async function boot(){
  try {
    Boot.show('Loading graphics library…');
    await loadFabric();

    Boot.show('Initializing canvas…');
    initCanvas();
    buildPalette();
    $('counter-val').textContent = 'C-01';

    setTimeout(() => fitView(), 100);

    Boot.show('Restoring session…');
    setTimeout(() => {
      const restored = loadLocal();
      if (!restored) toast('Ready — paste or drop a floor plan');
      Boot.ready();
      // Warn on unsaved work
      window.addEventListener('beforeunload', e => {
        if (drawing){ e.preventDefault(); e.returnValue = ''; }
      });
    }, 200);

  } catch(e){
    console.error('[boot]', e);
    Boot.error('Startup failed',
      `Could not initialize the app.<br><br>
       <code>${e.message}</code><br><br>
       Try: <br>
       • Refresh the page<br>
       • Disable ad-blockers for this site<br>
       • Check browser console (F12) for details`);
  }
})();
</script>
</body>
</html>
"""

components.html(APP_HTML, height=1000, scrolling=False)
