import streamlit as st
import streamlit.components.v1 as components
import os, tempfile

st.set_page_config(
    page_title="Cable Routing (client-side)",
    page_icon="🔌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hide Streamlit chrome — the component owns the whole UI
st.markdown("""
<style>
  #MainMenu, header, footer {visibility:hidden;}
  .block-container {padding: 0 !important; max-width: 100% !important;}
  iframe {border: none;}
</style>
""", unsafe_allow_html=True)

# =====================================================================
# The entire app lives in this HTML string. Streamlit just serves it.
# =====================================================================
APP_HTML = r"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Cable Routing Studio</title>
<script src="https://cdn.jsdelivr.net/npm/fabric@5.3.0/dist/fabric.min.js"></script>
<style>
  * { box-sizing: border-box; }
  body { margin:0; font-family: system-ui, -apple-system, sans-serif; background:#0f172a; color:#e2e8f0; }
  #app { display:flex; height:100vh; }

  /* ---- Sidebar ---- */
  #sidebar { width:260px; background:#1e293b; padding:14px; overflow-y:auto; flex-shrink:0; }
  #sidebar h3 { margin: 12px 0 6px; font-size:.8rem; text-transform:uppercase;
                letter-spacing:.06em; color:#94a3b8; }
  .btn { display:block; width:100%; padding:8px 10px; margin:4px 0; background:#334155;
         color:#e2e8f0; border:1px solid #475569; border-radius:8px; font-size:.85rem;
         cursor:pointer; text-align:left; transition:.15s; }
  .btn:hover { background:#475569; }
  .btn.active { background:linear-gradient(90deg,#2563eb,#7c3aed); border-color:transparent; color:#fff; font-weight:600; }
  .row { display:flex; gap:6px; }
  .row .btn { flex:1; text-align:center; }
  input[type="color"] { width:100%; height:32px; border:none; background:transparent; cursor:pointer; }
  input[type="range"] { width:100%; }
  input[type="text"], input[type="number"] { width:100%; padding:6px 8px; border-radius:6px;
    border:1px solid #475569; background:#0f172a; color:#e2e8f0; font-size:.85rem; }
  label { font-size:.75rem; color:#94a3b8; display:block; margin:8px 0 3px; }

  /* ---- Canvas area ---- */
  #stage { flex:1; position:relative; overflow:auto; background:
    repeating-conic-gradient(#1e293b 0 25%, #0f172a 0 50%) 50% / 24px 24px; }
  #canvas-wrap { position:relative; margin:20px auto; width:max-content; }
  #drop-hint { position:absolute; inset:40px; display:flex; flex-direction:column;
    align-items:center; justify-content:center; border:3px dashed #475569;
    border-radius:16px; color:#94a3b8; font-size:1.1rem; text-align:center;
    pointer-events:none; }
  #drop-hint b { color:#a5b4fc; }
  #status { position:fixed; bottom:12px; right:16px; background:#1e293b; padding:6px 12px;
    border-radius:8px; font-size:.75rem; color:#94a3b8; border:1px solid #334155; }
  #paste-fab { position:fixed; top:12px; right:16px; background:linear-gradient(90deg,#2563eb,#7c3aed);
    color:#fff; padding:10px 16px; border-radius:10px; font-weight:600; cursor:pointer;
    box-shadow:0 4px 12px rgba(0,0,0,.35); border:none; font-size:.85rem; }
  #paste-fab:hover { opacity:.9; }
</style>
</head>
<body>
<div id="app">

  <!-- ================= SIDEBAR ================= -->
  <aside id="sidebar">
    <h3>📤 Image</h3>
    <input type="file" id="file-input" accept="image/*" style="display:none">
    <button class="btn" onclick="document.getElementById('file-input').click()">📁 Open image…</button>
    <button class="btn" onclick="focusPaste()">📋 Paste (Ctrl+V)</button>
    <button class="btn" onclick="clearImage()">🔄 Remove image</button>

    <h3>🖌️ Tool</h3>
    <button class="btn active" data-tool="pen">🖊️ Pen (free draw)</button>
    <button class="btn" data-tool="line">📏 Line</button>
    <button class="btn" data-tool="rect">⬛ Rectangle</button>
    <button class="btn" data-tool="circle">⭕ Circle</button>
    <button class="btn" data-tool="text">🔤 Text</button>
    <button class="btn" data-tool="select">🖱️ Select / Move</button>
    <button class="btn" data-tool="erase">🧹 Eraser (click object)</button>

    <h3>🎨 Style</h3>
    <label>Stroke color</label>
    <input type="color" id="stroke-color" value="#ef4444">
    <label>Stroke width: <span id="sw-val">4</span>px</label>
    <input type="range" id="stroke-width" min="1" max="25" value="4">
    <label>Fill color</label>
    <input type="color" id="fill-color" value="#ef4444">
    <label><input type="checkbox" id="fill-enabled"> Enable fill</label>

    <h3>🔤 Text</h3>
    <input type="text" id="text-value" value="Outlet A" placeholder="Label text">
    <label>Font size: <span id="fs-val">22</span>px</label>
    <input type="range" id="font-size" min="10" max="72" value="22">

    <h3>🔧 Actions</h3>
    <div class="row">
      <button class="btn" onclick="undo()">↩️ Undo</button>
      <button class="btn" onclick="redo()">↪️ Redo</button>
    </div>
    <button class="btn" onclick="clearAll()">🗑️ Clear drawings</button>

    <h3>💾 Export (browser-side)</h3>
    <button class="btn" onclick="exportPNG()">⬇️ Download PNG</button>
    <button class="btn" onclick="exportJSON()">⬇️ Download JSON</button>
    <button class="btn" onclick="loadJSON()">📂 Load JSON…</button>
    <input type="file" id="json-input" accept=".json" style="display:none">
    <button class="btn" onclick="sendToStreamlit()">💾 Save to Streamlit</button>
  </aside>

  <!-- ================= CANVAS ================= -->
  <main id="stage">
    <div id="canvas-wrap">
      <canvas id="c"></canvas>
      <div id="drop-hint">
        📁 Drag &amp; drop a floor plan here<br>
        <b>or press Ctrl+V</b> to paste a screenshot<br>
        <span style="font-size:.85rem">or click “Open image…” in the sidebar</span>
      </div>
    </div>
  </main>

  <button id="paste-fab" onclick="focusPaste()">📋 Paste image</button>
  <div id="status">Ready</div>
</div>

<script>
/* =====================================================================
   STATE
   ===================================================================== */
let canvas, bgImage = null, currentTool = 'pen', drawing = false;
let startPt = null, activeShape = null;
let undoStack = [], redoStack = [];
const CANVAS_W = 1400, CANVAS_H = 900;

const $ = id => document.getElementById(id);
const setStatus = msg => { $('status').textContent = msg; };

/* =====================================================================
   CANVAS INIT
   ===================================================================== */
function initCanvas() {
  canvas = new fabric.Canvas('c', {
    width: CANVAS_W, height: CANVAS_H,
    backgroundColor: '#ffffff',
    selection: true,
    preserveObjectStacking: true,
  });

  canvas.on('mouse:down', onMouseDown);
  canvas.on('mouse:move', onMouseMove);
  canvas.on('mouse:up',   onMouseUp);

  // Snapshot for undo whenever an object is committed
  canvas.on('object:added', pushHistory);
  canvas.on('object:modified', pushHistory);

  // Eraser: click-to-remove
  canvas.on('mouse:down', opt => {
    if (currentTool === 'erase' && opt.target) {
      canvas.remove(opt.target);
    }
  });
}

function pushHistory() {
  const json = JSON.stringify(canvas.toJSON(['selectable','evented']));
  if (undoStack[undoStack.length-1] === json) return;
  undoStack.push(json);
  if (undoStack.length > 60) undoStack.shift();
  redoStack = [];
  updateStreamlitPayload();
}

function undo() {
  if (undoStack.length < 2) { setStatus('Nothing to undo'); return; }
  redoStack.push(undoStack.pop());
  loadShapesFromJSON(undoStack[undoStack.length-1]);
  updateStreamlitPayload();
  setStatus('Undo');
}
function redo() {
  if (!redoStack.length) { setStatus('Nothing to redo'); return; }
  const j = redoStack.pop();
  undoStack.push(j);
  loadShapesFromJSON(j);
  updateStreamlitPayload();
  setStatus('Redo');
}
function clearAll() {
  if (!confirm('Clear all drawings?')) return;
  canvas.getObjects().forEach(o => canvas.remove(o));
  pushHistory();
  setStatus('Cleared drawings');
}

/* =====================================================================
   DRAWING LOGIC
   ===================================================================== */
const strokeColor = () => $('stroke-color').value;
const strokeWidth = () => parseInt($('stroke-width').value);
const fillColor   = () => $('fill-enabled').checked ? $('fill-color').value : 'transparent';
const fontSize    = () => parseInt($('font-size').value);

function onMouseDown(opt) {
  if (currentTool === 'select' || currentTool === 'erase') return;
  const p = canvas.getPointer(opt.e);
  drawing = true;
  startPt = p;

  if (currentTool === 'pen') {
    activeShape = new fabric.Path(`M ${p.x} ${p.y}`, {
      stroke: strokeColor(), strokeWidth: strokeWidth(),
      fill: '', strokeLineCap: 'round', strokeLineJoin: 'round',
      selectable: false, evented: false,
    });
    canvas.add(activeShape);
  } else if (currentTool === 'line') {
    activeShape = new fabric.Line([p.x, p.y, p.x, p.y], {
      stroke: strokeColor(), strokeWidth: strokeWidth(),
      selectable: false, evented: false,
    });
    canvas.add(activeShape);
  } else if (currentTool === 'rect') {
    activeShape = new fabric.Rect({
      left: p.x, top: p.y, width: 1, height: 1,
      fill: fillColor(), stroke: strokeColor(), strokeWidth: strokeWidth(),
      selectable: false, evented: false,
    });
    canvas.add(activeShape);
  } else if (currentTool === 'circle') {
    activeShape = new fabric.Circle({
      left: p.x, top: p.y, radius: 1,
      fill: fillColor(), stroke: strokeColor(), strokeWidth: strokeWidth(),
      selectable: false, evented: false, originX: 'left', originY: 'top',
    });
    canvas.add(activeShape);
  } else if (currentTool === 'text') {
    const t = new fabric.IText($('text-value').value || 'Label', {
      left: p.x, top: p.y,
      fill: strokeColor(), fontSize: fontSize(),
      fontFamily: 'system-ui, sans-serif', fontWeight: '600',
    });
    canvas.add(t);
    canvas.setActiveObject(t);
    drawing = false;
    activeShape = null;
    setStatus('Text added — double-click to edit');
  }
}

function onMouseMove(opt) {
  if (!drawing || !activeShape) return;
  const p = canvas.getPointer(opt.e);

  if (currentTool === 'pen') {
    const path = activeShape.path;
    // append line to path
    path.push(['L', p.x, p.y]);
    activeShape.set({ path });
    activeShape.dirty = true;
  } else if (currentTool === 'line') {
    activeShape.set({ x2: p.x, y2: p.y });
  } else if (currentTool === 'rect') {
    activeShape.set({
      left: Math.min(startPt.x, p.x),
      top: Math.min(startPt.y, p.y),
      width: Math.abs(p.x - startPt.x),
      height: Math.abs(p.y - startPt.y),
    });
  } else if (currentTool === 'circle') {
    const dx = p.x - startPt.x, dy = p.y - startPt.y;
    const r = Math.sqrt(dx*dx + dy*dy);
    activeShape.set({ left: startPt.x, top: startPt.y, radius: r });
  }
  canvas.requestRenderAll();
}

function onMouseUp() {
  if (!drawing) return;
  drawing = false;
  if (activeShape) {
    // Finalize: make selectable, push history
    activeShape.set({ selectable: true, evented: true });
    canvas.setActiveObject(activeShape);
    activeShape = null;
    canvas.requestRenderAll();
    pushHistory();
    setStatus('Shape added');
  }
}

/* =====================================================================
   TOOL SWITCHING
   ===================================================================== */
document.querySelectorAll('[data-tool]').forEach(btn => {
  btn.onclick = () => {
    document.querySelectorAll('[data-tool]').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentTool = btn.dataset.tool;
    canvas.isDrawingMode = false;
    canvas.selection = currentTool === 'select';
    canvas.forEachObject(o => {
      o.selectable = currentTool === 'select';
      o.evented = currentTool !== 'pen';   // pen shouldn't intercept
    });
    setStatus('Tool: ' + currentTool);
  };
});
$('stroke-width').oninput = e => $('sw-val').textContent = e.target.value;
$('font-size').oninput    = e => $('fs-val').textContent = e.target.value;

/* =====================================================================
   IMAGE LOADING (file / paste / drop) — all local, no server
   ===================================================================== */
function loadImageFromDataURL(dataUrl, name) {
  fabric.Image.fromURL(dataUrl, img => {
    // Scale to fit canvas while preserving aspect
    const scale = Math.min(CANVAS_W / img.width, CANVAS_H / img.height, 1);
    img.set({
      left: 0, top: 0,
      scaleX: scale, scaleY: scale,
      selectable: false, evented: false, excludeFromExport: false,
      isBackground: true,
    });
    // Resize canvas to match image
    canvas.setWidth(img.width * scale);
    canvas.setHeight(img.height * scale);
    canvas.setBackgroundImage(img, canvas.renderAll.bind(canvas));
    // Remove any previous background objects
    canvas.getObjects().filter(o => o.isBackground).forEach(o => canvas.remove(o));
    $('drop-hint').style.display = 'none';
    setStatus('Loaded: ' + (name || 'image') + ' — ' + Math.round(img.width) + '×' + Math.round(img.height));
  });
}

$('file-input').onchange = e => {
  const f = e.target.files[0];
  if (!f) return;
  const url = URL.createObjectURL(f);   // never sent to server
  const r = new FileReader();
  r.onload = ev => loadImageFromDataURL(ev.target.result, f.name);
  r.readAsDataURL(f);
};

// Paste (global)
document.addEventListener('paste', e => {
  const items = (e.clipboardData || {}).items || [];
  for (const it of items) {
    if (it.kind === 'file' && it.type.startsWith('image/')) {
      const f = it.getAsFile();
      const r = new FileReader();
      r.onload = ev => loadImageFromDataURL(ev.target.result, 'pasted');
      r.readAsDataURL(f);
      e.preventDefault();
      return;
    }
  }
});

// Drag & drop
document.addEventListener('dragover', e => { e.preventDefault(); });
document.addEventListener('drop', e => {
  e.preventDefault();
  const f = e.dataTransfer.files[0];
  if (!f || !f.type.startsWith('image/')) return;
  const r = new FileReader();
  r.onload = ev => loadImageFromDataURL(ev.target.result, f.name);
  r.readAsDataURL(f);
});

function clearImage() {
  canvas.setBackgroundImage(null, canvas.renderAll.bind(canvas));
  canvas.setWidth(CANVAS_W); canvas.setHeight(CANVAS_H);
  $('drop-hint').style.display = 'flex';
  setStatus('Image removed');
}
function focusPaste() {
  document.body.focus();
  setStatus('Press Ctrl+V / ⌘+V to paste your screenshot');
}

/* =====================================================================
   EXPORT (client-side downloads — no server round-trip)
   ===================================================================== */
function download(blob, filename) {
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 4000);
}

function exportPNG() {
  // Render at 2× for crisper output
  const dataUrl = canvas.toDataURL({ format: 'png', multiplier: 2 });
  fetch(dataUrl).then(r => r.blob()).then(b => {
    download(b, 'cable_routing_' + Date.now() + '.png');
    setStatus('PNG downloaded');
  });
}

function exportJSON() {
  const data = {
    version: 1,
    canvas: { width: canvas.getWidth(), height: canvas.getHeight() },
    fabric: canvas.toJSON(['selectable','evented','isBackground']),
  };
  download(new Blob([JSON.stringify(data, null, 2)], { type:'application/json' }),
           'annotations_' + Date.now() + '.json');
  setStatus('JSON downloaded');
}

function loadJSON() { $('json-input').click(); }
$('json-input').onchange = e => {
  const f = e.target.files[0];
  if (!f) return;
  const r = new FileReader();
  r.onload = ev => {
    try {
      const d = JSON.parse(ev.target.result);
      canvas.loadFromJSON(d.fabric || d, () => {
        canvas.renderAll();
        pushHistory();
        setStatus('Annotations loaded');
      });
    } catch (err) { setStatus('Invalid JSON: ' + err.message); }
  };
  r.readAsText(f);
};

/* =====================================================================
   SEND SMALL JSON BACK TO STREAMLIT (optional persistence)
   ===================================================================== */
function sendToStreamlit() {
  const payload = {
    shape_count: canvas.getObjects().filter(o => !o.isBackground).length,
    canvas: { width: canvas.getWidth(), height: canvas.getHeight() },
    fabric: canvas.toJSON(['selectable','evented','isBackground']),
  };
  const json = JSON.stringify(payload);

  if (window.Streamlit && window.Streamlit.setComponentValue) {
    window.Streamlit.setComponentValue({ action: 'save', payload });
    setStatus('Sent to Streamlit (' + (json.length/1024).toFixed(1) + ' KB)');
  } else {
    // Post to parent (Streamlit iframe)
    window.parent.postMessage({
      isStreamlitMessage: true,
      type: 'streamlit:setComponentValue',
      value: { action: 'save', payload },
    }, '*');
    setStatus('Sent to Streamlit (' + (json.length/1024).toFixed(1) + ' KB)');
  }
}

// Auto-sync shape count so Streamlit always has latest (tiny payload)
function updateStreamlitPayload() {
  const count = canvas.getObjects().filter(o => !o.isBackground).length;
  if (window.Streamlit && window.Streamlit.setComponentValue) {
    window.Streamlit.setComponentValue({ action: 'update', count });
  }
}

/* =====================================================================
   BOOT
   ===================================================================== */
initCanvas();

// Signal Streamlit we're a component (only if embedded)
if (window.Streamlit && window.Streamlit.setFrameHeight) {
  window.Streamlit.setFrameHeight(window.innerHeight);
}
</script>
</body>
</html>
"""

# =====================================================================
# Serve the HTML via a temporary custom component (no external folder)
# =====================================================================
@st.cache_resource(show_spinner=False)
def _build_app_component():
    d = tempfile.mkdtemp(prefix="cable_app_")
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(APP_HTML)
    return components.declare_component("cable_app", path=d)

_cable_app = _build_app_component()

result = _cable_app(key="cable_app_widget", default=None)

# Optional: react to JSON saves coming back from the browser
if isinstance(result, dict) and result.get("action") == "save":
    st.session_state.setdefault("last_saved", None)
    st.session_state["last_saved"] = result.get("payload")
    st.toast("💾 Annotations saved to Streamlit session", icon="✅")
