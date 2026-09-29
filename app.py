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
  iframe {border: none; display: block;}
  [data-testid="stAppViewContainer"] > .main {padding: 0;}
</style>
""", unsafe_allow_html=True)

APP_HTML = r"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Cable Routing Studio Pro</title>
<script src="https://cdn.jsdelivr.net/npm/fabric@5.3.0/dist/fabric.min.js"></script>
<style>
  *{box-sizing:border-box;-webkit-user-select:none;user-select:none}
  html,body{margin:0;height:100%;overflow:hidden;
    font-family:system-ui,-apple-system,"Segoe UI",sans-serif;
    background:#0b1220;color:#e2e8f0;font-size:13px}
  #app{display:flex;height:100vh}

  /* ---------- SIDEBAR ---------- */
  #sidebar{width:290px;background:#131a2b;border-right:1px solid #1f2a44;
    overflow-y:auto;flex-shrink:0;padding:10px 12px 60px}
  #sidebar::-webkit-scrollbar{width:8px}
  #sidebar::-webkit-scrollbar-thumb{background:#27344f;border-radius:4px}
  #sidebar h3{margin:14px 0 6px;font-size:.7rem;text-transform:uppercase;
    letter-spacing:.09em;color:#7c8db5;font-weight:700;display:flex;
    align-items:center;gap:6px}
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
  .btn .k{margin-left:auto;font-size:.65rem;color:#7c8db5;
    background:#0b1220;padding:1px 6px;border-radius:4px}
  .btn.active .k{color:#c7d2fe;background:rgba(255,255,255,.15)}
  .row{display:flex;gap:6px}
  .row .btn{flex:1;justify-content:center;text-align:center}

  input[type="color"]{width:100%;height:30px;border:none;background:transparent;
    cursor:pointer;border-radius:6px}
  input[type="range"]{width:100%;accent-color:#6366f1}
  input[type="text"],input[type="number"]{width:100%;padding:6px 8px;
    border-radius:6px;border:1px solid #2a3a5c;background:#0b1220;
    color:#e2e8f0;font-size:.82rem;font-family:inherit}
  input[type="text"]:focus,input[type="number"]:focus{
    outline:none;border-color:#6366f1;box-shadow:0 0 0 2px rgba(99,102,241,.2)}
  label{font-size:.72rem;color:#8b9dc3;display:block;margin:6px 0 3px;
    display:flex;justify-content:space-between;align-items:center}
  label span.val{color:#a5b4fc;font-weight:600}

  .swatches{display:grid;grid-template-columns:repeat(6,1fr);gap:4px;margin-top:4px}
  .swatch{aspect-ratio:1;border-radius:5px;cursor:pointer;
    border:2px solid transparent;transition:.1s}
  .swatch:hover{transform:scale(1.1)}
  .swatch.sel{border-color:#fff;box-shadow:0 0 0 2px #6366f1}

  /* ---------- CANVAS AREA ---------- */
  #stage{flex:1;position:relative;overflow:hidden;
    background:repeating-conic-gradient(#111a2e 0 25%,#0b1220 0 50%) 50%/22px 22px}
  #canvas-holder{position:absolute;left:0;top:0;
    transform-origin:0 0;transition:transform .08s linear}
  #drop-hint{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);
    display:flex;flex-direction:column;align-items:center;justify-content:center;
    padding:40px 60px;border:3px dashed #2a3a5c;border-radius:20px;
    color:#8b9dc3;font-size:1rem;text-align:center;
    pointer-events:none;z-index:5;max-width:520px}
  #drop-hint b{color:#a5b4fc;font-size:1.15rem;display:block;margin:6px 0}
  #drop-hint .icon{font-size:3.5rem;margin-bottom:8px}
  #drop-hint .sub{font-size:.82rem;color:#66748f;margin-top:8px;line-height:1.5}

  /* ---------- TOP BAR ---------- */
  #topbar{position:absolute;top:12px;left:50%;transform:translateX(-50%);
    display:flex;gap:6px;background:rgba(19,26,43,.92);
    backdrop-filter:blur(12px);border:1px solid #2a3a5c;
    padding:6px;border-radius:12px;z-index:20;
    box-shadow:0 8px 24px rgba(0,0,0,.4)}
  #topbar button{background:transparent;border:none;color:#8b9dc3;
    padding:6px 12px;border-radius:7px;cursor:pointer;font-size:.8rem;
    font-family:inherit;display:flex;align-items:center;gap:5px;
    transition:.12s}
  #topbar button:hover{background:#1c2640;color:#e2e8f0}
  #topbar button.active{background:#2563eb;color:#fff}

  /* ---------- HUD ---------- */
  #hud{position:absolute;bottom:12px;right:14px;display:flex;gap:8px;
    align-items:center;z-index:10}
  #hud .chip{background:rgba(19,26,43,.92);backdrop-filter:blur(12px);
    border:1px solid #2a3a5c;padding:6px 12px;border-radius:8px;
    font-size:.72rem;color:#a5b4fc;font-family:ui-monospace,monospace}
  #hud button{background:rgba(19,26,43,.92);backdrop-filter:blur(12px);
    border:1px solid #2a3a5c;color:#a5b4fc;width:34px;height:34px;
    border-radius:8px;cursor:pointer;font-size:1rem;transition:.12s}
  #hud button:hover{background:#1c2640;color:#fff}

  /* ---------- LEGEND ---------- */
  #legend{position:absolute;top:12px;right:14px;
    background:rgba(19,26,43,.94);backdrop-filter:blur(12px);
    border:1px solid #2a3a5c;border-radius:12px;padding:10px 14px;
    min-width:180px;max-width:240px;z-index:15;
    box-shadow:0 8px 24px rgba(0,0,0,.4);font-size:.75rem;
    max-height:60vh;overflow-y:auto}
  #legend h4{margin:0 0 8px;font-size:.72rem;text-transform:uppercase;
    letter-spacing:.08em;color:#7c8db5;display:flex;
    justify-content:space-between;align-items:center}
  #legend h4 button{background:none;border:none;color:#7c8db5;
    cursor:pointer;font-size:.9rem;padding:0 4px}
  #legend .item{display:flex;align-items:center;gap:8px;padding:4px 0;
    border-bottom:1px solid #1a2338}
  #legend .item:last-child{border-bottom:none}
  #legend .dot{width:10px;height:10px;border-radius:50%;flex-shrink:0}
  #legend .name{flex:1;color:#c8d3e8;font-weight:500;
    overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  #legend .cnt{color:#66748f;font-family:ui-monospace,monospace;font-size:.7rem}

  /* ---------- LAYERS ---------- */
  #layers{position:absolute;bottom:12px;left:14px;
    background:rgba(19,26,43,.94);backdrop-filter:blur(12px);
    border:1px solid #2a3a5c;border-radius:12px;padding:8px 10px;
    max-width:280px;max-height:240px;overflow-y:auto;z-index:10;
    font-size:.75rem;box-shadow:0 8px 24px rgba(0,0,0,.4)}
  #layers h4{margin:0 0 6px;font-size:.7rem;text-transform:uppercase;
    letter-spacing:.08em;color:#7c8db5}
  #layers .layer{display:flex;align-items:center;gap:8px;padding:3px 6px;
    border-radius:5px;cursor:pointer;transition:.12s}
  #layers .layer:hover{background:#1c2640}
  #layers .layer.sel{background:#2563eb;color:#fff}
  #layers .layer .lyr-icon{width:14px;text-align:center;font-size:.85rem}
  #layers .layer .lyr-name{flex:1;overflow:hidden;text-overflow:ellipsis;
    white-space:nowrap}

  /* ---------- TOAST ---------- */
  #toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%) translateY(100px);
    background:#1c2640;border:1px solid #3b4d75;color:#e2e8f0;
    padding:10px 20px;border-radius:10px;font-size:.82rem;
    box-shadow:0 10px 30px rgba(0,0,0,.5);transition:transform .25s ease;
    z-index:100;pointer-events:none}
  #toast.show{transform:translateX(-50%) translateY(0)}

  /* ---------- MEASURE TOOLTIP ---------- */
  #measure{position:fixed;background:#1c2640;border:1px solid #6366f1;
    padding:4px 8px;border-radius:6px;font-size:.72rem;color:#c7d2fe;
    font-family:ui-monospace,monospace;pointer-events:none;z-index:200;
    display:none}
</style>
</head>
<body>

<div id="app">

  <!-- ============================= SIDEBAR ============================= -->
  <aside id="sidebar">

    <h3>📤 Image Source</h3>
    <div class="section">
      <input type="file" id="file-input" accept="image/*" style="display:none">
      <button class="btn" onclick="document.getElementById('file-input').click()">
        📁 <span>Open image</span>
      </button>
      <button class="btn" onclick="focusPaste()">
        📋 <span>Paste (Ctrl+V)</span>
      </button>
      <button class="btn" onclick="clearImage()">
        🔄 <span>Remove image</span>
      </button>
      <label>Background opacity <span class="val" id="op-val">100%</span></label>
      <input type="range" id="opacity" min="10" max="100" value="100">
    </div>

    <h3>🖌️ Drawing Tools</h3>
    <div class="section">
      <button class="btn active" data-tool="pen">
        🖊️ <span>Pen / Cable Route</span><span class="k">P</span>
      </button>
      <button class="btn" data-tool="line">
        📏 <span>Line</span><span class="k">L</span>
      </button>
      <button class="btn" data-tool="rect">
        ⬛ <span>Rectangle</span><span class="k">R</span>
      </button>
      <button class="btn" data-tool="circle">
        ⭕ <span>Circle</span><span class="k">C</span>
      </button>
      <button class="btn" data-tool="text">
        🔤 <span>Text Label</span><span class="k">T</span>
      </button>
      <button class="btn" data-tool="select">
        🖱️ <span>Select / Move</span><span class="k">V</span>
      </button>
      <button class="btn" data-tool="erase">
        🧹 <span>Eraser</span><span class="k">E</span>
      </button>
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
        <input type="checkbox" id="fill-enabled" style="width:auto">
      </label>
      <input type="color" id="fill-color" value="#ef444433">
    </div>

    <h3>🔤 Text Settings</h3>
    <div class="section">
      <input type="text" id="text-value" value="Outlet A" placeholder="Label text">
      <label>Font size <span class="val" id="fs-val">22px</span></label>
      <input type="range" id="font-size" min="10" max="72" value="22">
      <div class="row">
        <button class="btn" onclick="autoNumberNext()" style="flex:1">
          🔢 <span>Auto #</span>
        </button>
        <button class="btn" onclick="resetCounter()" style="flex:1">
          ↺ <span>Reset</span>
        </button>
      </div>
      <label>Next ID <span class="val" id="counter-val">C-01</span></label>
    </div>

    <h3>🧲 Snap & Grid</h3>
    <div class="section">
      <label><span>Snap to grid</span>
        <input type="checkbox" id="snap-grid" style="width:auto">
      </label>
      <label>Grid size <span class="val" id="grid-val">20px</span></label>
      <input type="range" id="grid-size" min="5" max="100" value="20">
      <label><span>Snap to endpoints</span>
        <input type="checkbox" id="snap-end" checked style="width:auto">
      </label>
      <label><span>Show grid overlay</span>
        <input type="checkbox" id="show-grid" style="width:auto">
      </label>
    </div>

    <h3>📏 Measurements</h3>
    <div class="section">
      <label>Scale (px → meters)</label>
      <input type="number" id="scale-m" value="0.05" step="0.001" min="0.001">
      <label>Unit label</label>
      <input type="text" id="unit-label" value="m" maxlength="6">
      <label><span>Show lengths on segments</span>
        <input type="checkbox" id="show-length" checked style="width:auto">
      </label>
    </div>

    <h3>🔧 Actions</h3>
    <div class="section">
      <div class="row">
        <button class="btn" onclick="undo()" title="Ctrl+Z">
          ↩️ <span>Undo</span>
        </button>
        <button class="btn" onclick="redo()" title="Ctrl+Y">
          ↪️ <span>Redo</span>
        </button>
      </div>
      <div class="row">
        <button class="btn" onclick="duplicateSel()" title="Ctrl+D">
          📋 <span>Duplicate</span>
        </button>
        <button class="btn" onclick="deleteSel()" title="Del">
          🗑️ <span>Delete</span>
        </button>
      </div>
      <button class="btn" onclick="clearAll()">
        💥 <span>Clear all drawings</span>
      </button>
    </div>

    <h3>💾 Export</h3>
    <div class="section">
      <label>PNG resolution</label>
      <select id="png-scale" style="width:100%;padding:6px 8px;border-radius:6px;
        border:1px solid #2a3a5c;background:#0b1220;color:#e2e8f0;font-size:.82rem">
        <option value="1">1× (screen)</option>
        <option value="2" selected>2× (recommended)</option>
        <option value="3">3× (print)</option>
        <option value="4">4× (poster)</option>
      </select>
      <button class="btn" onclick="exportPNG()" style="margin-top:8px">
        🖼️ <span>Download PNG</span>
      </button>
      <button class="btn" onclick="exportJSON()">
        📄 <span>Download JSON</span>
      </button>
      <button class="btn" onclick="loadJSON()">
        📂 <span>Load JSON…</span>
      </button>
      <input type="file" id="json-input" accept=".json" style="display:none">
    </div>

    <h3>❓ Help</h3>
    <div class="section" style="font-size:.72rem;color:#8b9dc3;line-height:1.6">
      <div><b style="color:#a5b4fc">Zoom:</b> Ctrl + scroll</div>
      <div><b style="color:#a5b4fc">Pan:</b> Space + drag</div>
      <div><b style="color:#a5b4fc">Fit:</b> press <b>F</b></div>
      <div><b style="color:#a5b4fc">Multi-select:</b> drag box in Select</div>
    </div>

  </aside>

  <!-- ============================= STAGE ============================= -->
  <main id="stage">
    <div id="canvas-holder">
      <canvas id="c"></canvas>
    </div>

    <div id="drop-hint">
      <div class="icon">📐</div>
      <b>Drop a floor plan or paste a screenshot</b>
      <div class="sub">
        Press <b style="color:#a5b4fc">Ctrl+V</b> anywhere to paste ·<br>
        drag &amp; drop an image file ·<br>
        or click <b style="color:#a5b4fc">Open image</b> in the sidebar
      </div>
    </div>

    <div id="topbar">
      <button id="zoom-fit" onclick="fitView()" title="Fit to screen">🎯 Fit</button>
      <button onclick="zoomBy(1.2)">＋</button>
      <button onclick="zoomBy(1/1.2)">－</button>
      <button id="zoom-lvl" style="pointer-events:none;min-width:52px;justify-content:center">100%</button>
      <button id="toggle-legend" onclick="toggleLegend()" class="active">📊 Legend</button>
      <button id="toggle-layers" onclick="toggleLayers()" class="active">🧱 Layers</button>
    </div>

    <div id="legend">
      <h4>Cable Legend <button onclick="toggleLegend()" title="Hide">✕</button></h4>
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
   GLOBAL STATE
   ===================================================================== */
const $ = id => document.getElementById(id);
let canvas, currentTool = 'pen', drawing = false, startPt = null, activeShape = null;
let undoStack = [], redoStack = [], isDirty = false;
let cableCounter = 0;
let legendItems = {};  // {color: {count, name}}
let view = { zoom: 1, x: 0, y: 0 };
let spaceDown = false, panning = false, panStart = null;
const CW = 1400, CH = 900;
const PALETTE = [
  '#ef4444', '#f97316', '#eab308', '#22c55e', '#06b6d4',
  '#3b82f6', '#8b5cf6', '#ec4899', '#78716c', '#111827',
  '#10b981', '#f43f5e'
];
const CABLE_COLORS = {
  '#ef4444': 'Data / CAT6',
  '#f97316': 'Fire Alarm',
  '#eab308': 'Fiber',
  '#22c55e': 'CCTV / IP',
  '#06b6d4': 'Voice',
  '#3b82f6': 'Power',
  '#8b5cf6': 'Access Control',
  '#ec4899': 'Wireless AP',
  '#78716c': 'Spare',
  '#111827': 'Conduit',
  '#10b981': 'Grounding',
  '#f43f5e': 'Emergency',
};

/* =====================================================================
   TOAST
   ===================================================================== */
let toastTimer;
function toast(msg){
  const t = $('toast');
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove('show'), 1800);
}

/* =====================================================================
   CANVAS INIT
   ===================================================================== */
function initCanvas(){
  canvas = new fabric.Canvas('c', {
    width: CW, height: CH,
    backgroundColor: '#ffffff',
    selection: true,
    preserveObjectStacking: true,
    stopContextMenu: true,
    fireRightClick: true,
  });

  canvas.on('mouse:down',  onDown);
  canvas.on('mouse:move',  onMove);
  canvas.on('mouse:up',    onUp);
  canvas.on('object:added',    () => { markDirty(); refreshPanels(); });
  canvas.on('object:modified', () => { markDirty(); refreshPanels(); });
  canvas.on('object:removed',  () => { refreshPanels(); });
  canvas.on('selection:created', refreshPanels);
  canvas.on('selection:updated', refreshPanels);
  canvas.on('selection:cleared', refreshPanels);

  // Eraser
  canvas.on('mouse:down', opt => {
    if (currentTool === 'erase' && opt.target) {
      canvas.remove(opt.target);
      toast('Erased');
    }
  });

  // Double-click text to edit
  canvas.on('mouse:dblclick', opt => {
    if (opt.target && (opt.target.type === 'i-text' || opt.target.type === 'text')) {
      opt.target.enterEditing();
      opt.target.selectAll();
    }
  });

  // Background grid (procedural, not an object)
  drawGridOverlay();
}

/* =====================================================================
   GRID OVERLAY
   ===================================================================== */
function drawGridOverlay(){
  const showGrid = $('show-grid').checked;
  const size = parseInt($('grid-size').value);
  if (!showGrid){ canvas.setBackgroundColor('#ffffff', canvas.renderAll.bind(canvas)); return; }
  // Use a pattern via a temporary canvas
  const pc = document.createElement('canvas');
  pc.width = pc.height = size;
  const pcx = pc.getContext('2d');
  pcx.fillStyle = '#ffffff'; pcx.fillRect(0,0,size,size);
  pcx.strokeStyle = '#e5e7eb'; pcx.lineWidth = 1;
  pcx.beginPath(); pcx.moveTo(size-.5,0); pcx.lineTo(size-.5,size);
  pcx.moveTo(0,size-.5); pcx.lineTo(size,size-.5); pcx.stroke();
  canvas.setBackgroundColor({source: pc, repeat: 'repeat'},
                            canvas.renderAll.bind(canvas));
}

/* =====================================================================
   SNAP HELPERS
   ===================================================================== */
function snapPt(p){
  let x = p.x, y = p.y;
  if ($('snap-grid').checked){
    const g = parseInt($('grid-size').value);
    x = Math.round(x/g)*g; y = Math.round(y/g)*g;
  }
  if ($('snap-end').checked && currentTool !== 'pen'){
    // Snap to nearest existing endpoint within 12px
    const TOL = 12;
    let best = null, bestD = TOL;
    canvas.getObjects().forEach(o => {
      if (o === activeShape || o.isBackground) return;
      const pts = [];
      if (o.type === 'line'){
        pts.push({x:o.x1,y:o.y1},{x:o.x2,y:o.y2});
      } else if (o.type === 'rect'){
        const l=o.left, t=o.top, w=o.width*o.scaleX, h=o.height*o.scaleY;
        pts.push({x:l,y:t},{x:l+w,y:t},{x:l,y:t+h},{x:l+w,y:t+h});
      } else if (o.type === 'circle'){
        pts.push({x:o.left,y:o.top},{x:o.left+2*o.radius,y:o.top+2*o.radius});
      } else if (o.type === 'path'){
        const b = o.getBoundingRect(true,true);
        pts.push({x:b.left,y:b.top},
                 {x:b.left+b.width,y:b.top},
                 {x:b.left,y:b.top+b.height},
                 {x:b.left+b.width,y:b.top+b.height});
      }
      // Apply object transform
      pts.forEach(pt => {
        const tp = fabric.util.transformPoint(pt, o.calcTransformMatrix());
        const d = Math.hypot(tp.x - p.x, tp.y - p.y);
        if (d < bestD){ bestD = d; best = tp; }
      });
    });
    if (best){ x = best.x; y = best.y; }
  }
  return {x, y};
}

/* =====================================================================
   DRAWING
   ===================================================================== */
function onDown(opt){
  if (spaceDown){ panStart = {x:opt.e.clientX, y:opt.e.clientY}; panning = true; return; }
  if (currentTool === 'select' || currentTool === 'erase') return;

  const raw = canvas.getPointer(opt.e);
  const p = snapPt(raw);
  drawing = true; startPt = p;

  const sColor = $('stroke-color').value;
  const sWidth = parseInt($('stroke-width').value);
  const fEnabled = $('fill-enabled').checked;
  const fColor = fEnabled ? $('fill-color').value : 'transparent';

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
    activeShape._isCable = true;
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
      selectable: false, evented: false,
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
    toast('Text added — double-click to edit');
  }
}

function onMove(opt){
  const raw = canvas.getPointer(opt.e);
  $('hud-xy').textContent = `x: ${Math.round(raw.x)}  y: ${Math.round(raw.y)}`;

  if (panning && panStart){
    view.x += opt.e.clientX - panStart.x;
    view.y += opt.e.clientY - panStart.y;
    panStart = {x: opt.e.clientX, y: opt.e.clientY};
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
      left: Math.min(startPt.x,p.x), top: Math.min(startPt.y,p.y),
      width: Math.abs(p.x - startPt.x), height: Math.abs(p.y - startPt.y),
    });
  } else if (currentTool === 'circle'){
    const r = Math.hypot(p.x-startPt.x, p.y-startPt.y);
    activeShape.set({ left: startPt.x - r, top: startPt.y - r,
                      radius: r, originX:'left', originY:'top' });
  }

  // Live length tooltip
  if (currentTool === 'line' && $('show-length').checked){
    const m = $('measure');
    const len_px = Math.hypot(p.x - startPt.x, p.y - startPt.y);
    const meters = (len_px * parseFloat($('scale-m').value)).toFixed(2);
    m.textContent = `${meters} ${$('unit-label').value}  ·  ${Math.round(len_px)}px`;
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

  if (activeShape){
    activeShape.set({ selectable: true, evented: true });
    canvas.setActiveObject(activeShape);

    // Attach length info to line objects
    if (activeShape.type === 'line' && $('show-length').checked){
      const dx = activeShape.x2 - activeShape.x1;
      const dy = activeShape.y2 - activeShape.y1;
      const len = Math.hypot(dx, dy) * parseFloat($('scale-m').value);
      const mid = {x: (activeShape.x1 + activeShape.x2)/2, y: (activeShape.y1 + activeShape.y2)/2};
      const txt = new fabric.IText(len.toFixed(2) + ' ' + $('unit-label').value, {
        left: mid.x, top: mid.y - 14,
        fontSize: 12, fill: activeShape.stroke,
        fontFamily: 'ui-monospace, monospace',
        backgroundColor: 'rgba(255,255,255,.85)',
        padding: 2,
        selectable: true, evented: true,
      });
      txt._isAnnotation = true;
      txt._attachedTo = activeShape;
      canvas.add(txt);
    }

    activeShape = null;
    canvas.requestRenderAll();
    markDirty();
    refreshPanels();
    toast('Shape added');
  }
}

/* =====================================================================
   TOOL SWITCHING
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
  toast('Tool: ' + tool);
}
document.querySelectorAll('[data-tool]').forEach(btn => {
  btn.onclick = () => setTool(btn.dataset.tool);
});

/* =====================================================================
   PALETTE
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
   HISTORY
   ===================================================================== */
function markDirty(){
  isDirty = true;
  clearTimeout(window._saveTimer);
  window._saveTimer = setTimeout(saveLocal, 800);
  pushHistory();
}
function serialize(){
  return JSON.stringify({
    v: 1,
    fabric: canvas.toJSON(['selectable','evented','isBackground','_isCable','_isAnnotation']),
  });
}
function pushHistory(){
  const j = serialize();
  if (undoStack[undoStack.length-1] === j) return;
  undoStack.push(j);
  if (undoStack.length > 80) undoStack.shift();
  redoStack = [];
  updateHud();
}
function undo(){
  if (undoStack.length < 2){ toast('Nothing to undo'); return; }
  redoStack.push(undoStack.pop());
  applySnapshot(undoStack[undoStack.length-1]);
  toast('Undo');
}
function redo(){
  if (!redoStack.length){ toast('Nothing to redo'); return; }
  const j = redoStack.pop();
  undoStack.push(j);
  applySnapshot(j);
  toast('Redo');
}
function applySnapshot(j){
  const bg = canvas.backgroundImage;
  canvas.loadFromJSON(j, () => {
    if (bg) canvas.setBackgroundImage(bg, canvas.renderAll.bind(canvas));
    canvas.forEachObject(o => {
      o.selectable = currentTool === 'select';
      o.evented = currentTool !== 'pen';
    });
    canvas.renderAll();
    refreshPanels();
  });
}

/* =====================================================================
   ACTIONS
   ===================================================================== */
function clearAll(){
  if (!confirm('Clear all drawings? (background image stays)')) return;
  canvas.getObjects().forEach(o => canvas.remove(o));
  refreshPanels(); toast('Cleared');
}
function deleteSel(){
  const objs = canvas.getActiveObjects();
  if (!objs.length){ toast('Nothing selected'); return; }
  objs.forEach(o => canvas.remove(o));
  canvas.discardActiveObject();
  refreshPanels(); toast('Deleted ' + objs.length);
}
function duplicateSel(){
  const objs = canvas.getActiveObjects();
  if (!objs.length){ toast('Nothing selected'); return; }
  objs.forEach(o => {
    o.clone(c => {
      c.set({ left: o.left + 20, top: o.top + 20 });
      canvas.add(c);
    });
  });
  canvas.discardActiveObject();
  refreshPanels(); toast('Duplicated');
}
function autoNumberNext(){
  cableCounter++;
  $('text-value').value = 'C-' + String(cableCounter).padStart(2,'0');
  $('counter-val').textContent = 'C-' + String(cableCounter + 1).padStart(2,'0');
  toast('Next: ' + $('text-value').value);
}
function resetCounter(){
  cableCounter = 0;
  $('counter-val').textContent = 'C-01';
  toast('Counter reset');
}

/* =====================================================================
   IMAGE
   ===================================================================== */
function loadImage(dataUrl, name){
  fabric.Image.fromURL(dataUrl, img => {
    const s = Math.min(CW/img.width, CH/img.height, 1);
    img.set({ left:0, top:0, scaleX:s, scaleY:s,
      selectable:false, evented:false, isBackground:true,
      opacity: parseInt($('opacity').value)/100 });
    canvas.setWidth(img.width * s);
    canvas.setHeight(img.height * s);
    canvas.setBackgroundImage(img, canvas.renderAll.bind(canvas));
    $('drop-hint').style.display = 'none';
    fitView();
    toast('Loaded: ' + (name || 'image') + ' (' + Math.round(img.width) + '×' + Math.round(img.height) + ')');
  });
}
$('file-input').onchange = e => {
  const f = e.target.files[0]; if (!f) return;
  const r = new FileReader();
  r.onload = ev => loadImage(ev.target.result, f.name);
  r.readAsDataURL(f);
};
document.addEventListener('paste', e => {
  const items = (e.clipboardData || {}).items || [];
  for (const it of items){
    if (it.kind === 'file' && it.type.startsWith('image/')){
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
  if (bg){
    bg.set('opacity', parseInt(e.target.value)/100);
    canvas.renderAll();
  }
};

/* =====================================================================
   VIEW / ZOOM / PAN
   ===================================================================== */
function applyView(){
  const h = $('canvas-holder');
  h.style.transform = `translate(${view.x}px, ${view.y}px) scale(${view.zoom})`;
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
  zoomBy(e.deltaY < 0 ? 1.1 : 1/1.1, e.clientX - r.left, e.clientY - r.top);
}, { passive: false });
$('stage').addEventListener('mousedown', e => {
  if (spaceDown && e.button === 0){
    panning = true;
    panStart = {x: e.clientX, y: e.clientY};
    e.preventDefault();
  }
});
window.addEventListener('mouseup', () => { panning = false; panStart = null; });
window.addEventListener('mousemove', e => {
  if (!panning || !panStart) return;
  view.x += e.clientX - panStart.x;
  view.y += e.clientY - panStart.y;
  panStart = {x: e.clientX, y: e.clientY};
  applyView();
});

/* =====================================================================
   PANELS: LEGEND + LAYERS
   ===================================================================== */
function refreshPanels(){
  refreshLegend();
  refreshLayers();
  updateHud();
}
function refreshLegend(){
  const items = {};
  canvas.getObjects().forEach(o => {
    if (o.isBackground || o._isAnnotation) return;
    const col = (o.stroke || o.fill || '#666').toLowerCase();
    const key = col.startsWith('#') ? col.slice(0,7) : col;
    if (!items[key]) items[key] = 0;
    items[key]++;
  });
  const wrap = $('legend-items');
  wrap.innerHTML = '';
  Object.keys(items).forEach(k => {
    const name = CABLE_COLORS[k] || 'Cable';
    const el = document.createElement('div');
    el.className = 'item';
    el.innerHTML = `<span class="dot" style="background:${k}"></span>
                    <span class="name">${name}</span>
                    <span class="cnt">${items[k]}</span>`;
    wrap.appendChild(el);
  });
  if (!Object.keys(items).length){
    wrap.innerHTML = '<div style="color:#66748f;font-size:.72rem;padding:4px 0">No cables yet</div>';
  }
}
function refreshLayers(){
  const objs = canvas.getObjects().filter(o => !o.isBackground);
  const list = $('layers-list');
  list.innerHTML = '';
  $('lyr-count').textContent = '(' + objs.length + ')';
  objs.slice().reverse().forEach(o => {
    const el = document.createElement('div');
    el.className = 'layer' + (canvas.getActiveObject() === o ? ' sel' : '');
    const icon = { 'path':'🖊️','line':'📏','rect':'⬛','circle':'⭕',
                   'i-text':'🔤','text':'🔤' }[o.type] || '▪';
    const name = o.text ? o.text.slice(0,18)
                        : (CABLE_COLORS[(o.stroke||'').toLowerCase()] || o.type);
    el.innerHTML = `<span class="lyr-icon">${icon}</span>
                    <span class="lyr-name">${name}</span>`;
    el.onclick = () => {
      canvas.setActiveObject(o);
      canvas.renderAll();
      refreshLayers();
    };
    el.ondblclick = () => { o.visible = false; canvas.renderAll(); refreshLayers(); };
    list.appendChild(el);
  });
  if (!objs.length){
    list.innerHTML = '<div style="color:#66748f;font-size:.7rem;padding:4px 0">No objects</div>';
  }
}
function updateHud(){
  const n = canvas.getObjects().filter(o => !o.isBackground).length;
  $('hud-count').textContent = n + ' object' + (n === 1 ? '' : 's');
}
function toggleLegend(){
  const l = $('legend');
  const v = l.style.display === 'none';
  l.style.display = v ? 'block' : 'none';
  $('toggle-legend').classList.toggle('active', v);
}
function toggleLayers(){
  const l = $('layers');
  const v = l.style.display === 'none';
  l.style.display = v ? 'block' : 'none';
  $('toggle-layers').classList.toggle('active', v);
}

/* =====================================================================
   EXPORT
   ===================================================================== */
function download(blob, name){
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = name;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 4000);
}

function exportPNG(){
  const scale = parseInt($('png-scale').value);
  // Temporarily deselect to avoid selection handles in export
  const sel = canvas.getActiveObject();
  canvas.discardActiveObject();
  canvas.renderAll();

  // Hide grid during export
  const gridWasOn = $('show-grid').checked;
  let savedBg = canvas.backgroundImage;
  if (gridWasOn && savedBg){
    canvas.backgroundColor = 'transparent';
    canvas.renderAll();
  }

  const url = canvas.toDataURL({ format:'png', multiplier:scale, quality:1 });

  // Restore
  if (gridWasOn) drawGridOverlay();
  if (sel) canvas.setActiveObject(sel);
  canvas.renderAll();

  fetch(url).then(r => r.blob()).then(b => {
    download(b, `cable_routing_${scale}x_${Date.now()}.png`);
    toast(`PNG exported at ${scale}×`);
  });
}

function exportJSON(){
  const data = {
    version: 1,
    exported: new Date().toISOString(),
    canvas: { width: canvas.getWidth(), height: canvas.getHeight() },
    scale: { m_per_px: parseFloat($('scale-m').value),
             unit: $('unit-label').value },
    fabric: canvas.toJSON(['selectable','evented','isBackground','_isCable','_isAnnotation']),
  };
  download(new Blob([JSON.stringify(data, null, 2)], {type:'application/json'}),
           'annotations_' + Date.now() + '.json');
  toast('JSON exported');
}

function loadJSON(){ $('json-input').click(); }
$('json-input').onchange = e => {
  const f = e.target.files[0]; if (!f) return;
  const r = new FileReader();
  r.onload = ev => {
    try {
      const d = JSON.parse(ev.target.result);
      if (d.scale){
        $('scale-m').value = d.scale.m_per_px;
        $('unit-label').value = d.scale.unit;
      }
      canvas.loadFromJSON(d.fabric || d, () => {
        canvas.renderAll();
        refreshPanels();
        toast('Annotations loaded');
      });
    } catch (err){ toast('Invalid JSON: ' + err.message); }
  };
  r.readAsText(f);
};

/* =====================================================================
   LOCALSTORAGE AUTOSAVE
   ===================================================================== */
function saveLocal(){
  try {
    localStorage.setItem('cable_studio_v1', serialize());
    localStorage.setItem('cable_studio_counter', String(cableCounter));
  } catch(e){ /* quota */ }
}
function loadLocal(){
  try {
    const j = localStorage.getItem('cable_studio_v1');
    if (!j) return false;
    const cnt = localStorage.getItem('cable_studio_counter');
    if (cnt) cableCounter = parseInt(cnt);
    $('counter-val').textContent = 'C-' + String(cableCounter + 1).padStart(2,'0');
    canvas.loadFromJSON(j, () => {
      canvas.renderAll();
      refreshPanels();
      toast('Session restored');
    });
    return true;
  } catch(e){ return false; }
}

/* =====================================================================
   KEYBOARD SHORTCUTS
   ===================================================================== */
document.addEventListener('keydown', e => {
  if (e.target.tagName === 'INPUT' || e.target.isContentEditable) return;

  if (e.code === 'Space'){ spaceDown = true; document.body.style.cursor = 'grab'; e.preventDefault(); }

  const k = e.key.toLowerCase();
  if (e.ctrlKey || e.metaKey){
    if (k === 'z'){ e.preventDefault(); e.shiftKey ? redo() : undo(); }
    else if (k === 'y'){ e.preventDefault(); redo(); }
    else if (k === 'd'){ e.preventDefault(); duplicateSel(); }
    else if (k === 'a'){ e.preventDefault();
      canvas.discardActiveObject();
      const objs = canvas.getObjects().filter(o => !o.isBackground);
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
  if (e.code === 'Space'){ spaceDown = false;
    document.body.style.cursor = currentTool === 'select' ? 'default' : 'crosshair'; }
});

/* =====================================================================
   EVENT BINDINGS
   ===================================================================== */
$('stroke-width').oninput = e => $('sw-val').textContent = e.target.value + 'px';
$('font-size').oninput    = e => $('fs-val').textContent = e.target.value + 'px';
$('grid-size').oninput    = e => { $('grid-val').textContent = e.target.value + 'px'; drawGridOverlay(); };
$('stroke-color').oninput = e => {
  document.querySelectorAll('.swatch').forEach(s =>
    s.classList.toggle('sel',
      s.style.background === $('stroke-color').value ||
      s.style.backgroundColor === $('stroke-color').value));
};
$('show-grid').onchange = drawGridOverlay;

/* =====================================================================
   BOOT
   ===================================================================== */
initCanvas();
buildPalette();
$('counter-val').textContent = 'C-01';

// Fit view after layout settles
setTimeout(() => { fitView(); }, 100);
window.addEventListener('resize', () => { /* keep view */ });

// Try restoring session
setTimeout(() => {
  if (!loadLocal()) toast('Ready — paste or drop a floor plan');
}, 200);
</script>
</body>
</html>
"""

components.html(APP_HTML, height=1000, scrolling=False)
