import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Cable Routing Studio",
    page_icon="🔌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Kill Streamlit chrome so the app takes the full viewport
st.markdown(
    """
    <style>
      #MainMenu, header, footer {visibility: hidden; height: 0;}
      .block-container {padding: 0 !important; max-width: 100% !important;}
      iframe {border: none; display: block;}
      [data-testid="stAppViewContainer"] > .main { padding: 0; }
    </style>
    """,
    unsafe_allow_html=True,
)

APP_HTML = r"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Cable Routing Studio</title>
<script src="https://cdn.jsdelivr.net/npm/fabric@5.3.0/dist/fabric.min.js"></script>
<style>
  *{box-sizing:border-box}
  html,body{margin:0;height:100%;font-family:system-ui,-apple-system,sans-serif;
    background:#0f172a;color:#e2e8f0;overflow:hidden}
  #app{display:flex;height:100vh}

  #sidebar{width:260px;background:#1e293b;padding:14px;overflow-y:auto;flex-shrink:0}
  #sidebar h3{margin:12px 0 6px;font-size:.78rem;text-transform:uppercase;
    letter-spacing:.06em;color:#94a3b8}
  .btn{display:block;width:100%;padding:8px 10px;margin:4px 0;background:#334155;
    color:#e2e8f0;border:1px solid #475569;border-radius:8px;font-size:.85rem;
    cursor:pointer;text-align:left;transition:.15s}
  .btn:hover{background:#475569}
  .btn.active{background:linear-gradient(90deg,#2563eb,#7c3aed);border-color:transparent;
    color:#fff;font-weight:600}
  .row{display:flex;gap:6px}
  .row .btn{flex:1;text-align:center}
  input[type="color"]{width:100%;height:32px;border:none;background:transparent;cursor:pointer}
  input[type="range"]{width:100%}
  input[type="text"]{width:100%;padding:6px 8px;border-radius:6px;
    border:1px solid #475569;background:#0f172a;color:#e2e8f0;font-size:.85rem}
  label{font-size:.75rem;color:#94a3b8;display:block;margin:8px 0 3px}

  #stage{flex:1;position:relative;overflow:auto;background:
    repeating-conic-gradient(#1e293b 0 25%,#0f172a 0 50%) 50%/24px 24px}
  #canvas-wrap{position:relative;margin:20px auto;width:max-content}
  #drop-hint{position:absolute;inset:40px;display:flex;flex-direction:column;
    align-items:center;justify-content:center;border:3px dashed #475569;
    border-radius:16px;color:#94a3b8;font-size:1.05rem;text-align:center;
    pointer-events:none;padding:20px}
  #drop-hint b{color:#a5b4fc}
  #status{position:fixed;bottom:12px;right:16px;background:#1e293b;padding:6px 12px;
    border-radius:8px;font-size:.75rem;color:#94a3b8;border:1px solid #334155;z-index:99}
</style>
</head>
<body>
<div id="app">
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
    <button class="btn" data-tool="erase">🧹 Eraser</button>

    <h3>🎨 Style</h3>
    <label>Stroke color</label>
    <input type="color" id="stroke-color" value="#ef4444">
    <label>Stroke width: <span id="sw-val">4</span>px</label>
    <input type="range" id="stroke-width" min="1" max="25" value="4">
    <label>Fill color</label>
    <input type="color" id="fill-color" value="#ef4444">
    <label><input type="checkbox" id="fill-enabled"> Enable fill</label>

    <h3>🔤 Text</h3>
    <input type="text" id="text-value" value="Outlet A">
    <label>Font size: <span id="fs-val">22</span>px</label>
    <input type="range" id="font-size" min="10" max="72" value="22">

    <h3>🔧 Actions</h3>
    <div class="row">
      <button class="btn" onclick="undo()">↩️ Undo</button>
      <button class="btn" onclick="redo()">↪️ Redo</button>
    </div>
    <button class="btn" onclick="clearAll()">🗑️ Clear drawings</button>

    <h3>💾 Export</h3>
    <button class="btn" onclick="exportPNG()">⬇️ Download PNG</button>
    <button class="btn" onclick="exportJSON()">⬇️ Download JSON</button>
    <button class="btn" onclick="loadJSON()">📂 Load JSON…</button>
    <input type="file" id="json-input" accept=".json" style="display:none">
  </aside>

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

  <div id="status">Ready</div>
</div>

<script>
const $ = id => document.getElementById(id);
const setStatus = m => { $('status').textContent = m; };
let canvas, currentTool='pen', drawing=false, startPt=null, activeShape=null;
let undoStack=[], redoStack=[];
const CW=1400, CH=900;

function initCanvas(){
  canvas = new fabric.Canvas('c', {
    width:CW, height:CH, backgroundColor:'#ffffff',
    selection:true, preserveObjectStacking:true,
  });
  canvas.on('mouse:down', onDown);
  canvas.on('mouse:move', onMove);
  canvas.on('mouse:up',   onUp);
  canvas.on('object:added',    pushHistory);
  canvas.on('object:modified', pushHistory);
  canvas.on('mouse:down', opt => {
    if (currentTool==='erase' && opt.target) canvas.remove(opt.target);
  });
}

function pushHistory(){
  const j = JSON.stringify(canvas.toJSON(['selectable','evented','isBackground']));
  if (undoStack[undoStack.length-1]===j) return;
  undoStack.push(j); if (undoStack.length>60) undoStack.shift();
  redoStack = [];
}
function undo(){
  if (undoStack.length<2){ setStatus('Nothing to undo'); return; }
  redoStack.push(undoStack.pop());
  loadShapes(undoStack[undoStack.length-1]); setStatus('Undo');
}
function redo(){
  if (!redoStack.length){ setStatus('Nothing to redo'); return; }
  const j = redoStack.pop(); undoStack.push(j); loadShapes(j); setStatus('Redo');
}
function loadShapes(j){
  const bg = canvas.backgroundImage;
  canvas.loadFromJSON(j, () => {
    if (bg) canvas.setBackgroundImage(bg, canvas.renderAll.bind(canvas));
    canvas.renderAll();
  });
}
function clearAll(){
  if (!confirm('Clear all drawings?')) return;
  canvas.getObjects().forEach(o => canvas.remove(o));
  pushHistory(); setStatus('Cleared');
}

const strokeColor = () => $('stroke-color').value;
const strokeWidth = () => parseInt($('stroke-width').value);
const fillColor   = () => $('fill-enabled').checked ? $('fill-color').value : 'transparent';
const fontSize    = () => parseInt($('font-size').value);

function onDown(opt){
  if (currentTool==='select' || currentTool==='erase') return;
  const p = canvas.getPointer(opt.e);
  drawing = true; startPt = p;

  if (currentTool==='pen'){
    activeShape = new fabric.Path(`M ${p.x} ${p.y}`, {
      stroke:strokeColor(), strokeWidth:strokeWidth(), fill:'',
      strokeLineCap:'round', strokeLineJoin:'round',
      selectable:false, evented:false,
    });
    canvas.add(activeShape);
  } else if (currentTool==='line'){
    activeShape = new fabric.Line([p.x,p.y,p.x,p.y], {
      stroke:strokeColor(), strokeWidth:strokeWidth(),
      selectable:false, evented:false,
    });
    canvas.add(activeShape);
  } else if (currentTool==='rect'){
    activeShape = new fabric.Rect({
      left:p.x, top:p.y, width:1, height:1,
      fill:fillColor(), stroke:strokeColor(), strokeWidth:strokeWidth(),
      selectable:false, evented:false,
    });
    canvas.add(activeShape);
  } else if (currentTool==='circle'){
    activeShape = new fabric.Circle({
      left:p.x, top:p.y, radius:1,
      fill:fillColor(), stroke:strokeColor(), strokeWidth:strokeWidth(),
      selectable:false, evented:false, originX:'left', originY:'top',
    });
    canvas.add(activeShape);
  } else if (currentTool==='text'){
    const t = new fabric.IText($('text-value').value || 'Label', {
      left:p.x, top:p.y, fill:strokeColor(), fontSize:fontSize(),
      fontFamily:'system-ui, sans-serif', fontWeight:'600',
    });
    canvas.add(t); canvas.setActiveObject(t);
    drawing=false; activeShape=null; setStatus('Text added — double-click to edit');
  }
}
function onMove(opt){
  if (!drawing || !activeShape) return;
  const p = canvas.getPointer(opt.e);
  if (currentTool==='pen'){
    activeShape.path.push(['L', p.x, p.y]);
    activeShape.dirty = true;
  } else if (currentTool==='line'){
    activeShape.set({ x2:p.x, y2:p.y });
  } else if (currentTool==='rect'){
    activeShape.set({
      left:Math.min(startPt.x,p.x), top:Math.min(startPt.y,p.y),
      width:Math.abs(p.x-startPt.x), height:Math.abs(p.y-startPt.y),
    });
  } else if (currentTool==='circle'){
    const dx=p.x-startPt.x, dy=p.y-startPt.y;
    activeShape.set({ left:startPt.x, top:startPt.y, radius:Math.sqrt(dx*dx+dy*dy) });
  }
  canvas.requestRenderAll();
}
function onUp(){
  if (!drawing) return;
  drawing = false;
  if (activeShape){
    activeShape.set({ selectable:true, evented:true });
    canvas.setActiveObject(activeShape);
    activeShape = null; canvas.requestRenderAll();
    pushHistory(); setStatus('Shape added');
  }
}

document.querySelectorAll('[data-tool]').forEach(btn => {
  btn.onclick = () => {
    document.querySelectorAll('[data-tool]').forEach(b => b.classList.remove('active'));
    btn.classList.add('active'); currentTool = btn.dataset.tool;
    canvas.selection = currentTool==='select';
    canvas.forEachObject(o => {
      o.selectable = currentTool==='select';
      o.evented = currentTool!=='pen';
    });
    setStatus('Tool: ' + currentTool);
  };
});
$('stroke-width').oninput = e => $('sw-val').textContent = e.target.value;
$('font-size').oninput    = e => $('fs-val').textContent = e.target.value;

/* ---------------- IMAGE ---------------- */
function loadImage(dataUrl, name){
  fabric.Image.fromURL(dataUrl, img => {
    const s = Math.min(CW/img.width, CH/img.height, 1);
    img.set({ left:0, top:0, scaleX:s, scaleY:s,
      selectable:false, evented:false, isBackground:true });
    canvas.setWidth(img.width*s);
    canvas.setHeight(img.height*s);
    canvas.setBackgroundImage(img, canvas.renderAll.bind(canvas));
    $('drop-hint').style.display = 'none';
    setStatus('Loaded: ' + (name||'image') + ' — ' + Math.round(img.width) + '×' + Math.round(img.height));
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
    if (it.kind==='file' && it.type.startsWith('image/')){
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
  setStatus('Image removed');
}
function focusPaste(){ document.body.focus(); setStatus('Press Ctrl+V / ⌘+V to paste'); }

/* ---------------- EXPORT ---------------- */
function download(blob, name){
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = name; document.body.appendChild(a);
  a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 4000);
}
function exportPNG(){
  const url = canvas.toDataURL({ format:'png', multiplier:2 });
  fetch(url).then(r=>r.blob()).then(b=>{
    download(b, 'cable_routing_' + Date.now() + '.png');
    setStatus('PNG downloaded');
  });
}
function exportJSON(){
  const data = { version:1,
    canvas:{ width:canvas.getWidth(), height:canvas.getHeight() },
    fabric:canvas.toJSON(['selectable','evented','isBackground']) };
  download(new Blob([JSON.stringify(data,null,2)], {type:'application/json'}),
           'annotations_' + Date.now() + '.json');
  setStatus('JSON downloaded');
}
function loadJSON(){ $('json-input').click(); }
$('json-input').onchange = e => {
  const f = e.target.files[0]; if (!f) return;
  const r = new FileReader();
  r.onload = ev => {
    try{
      const d = JSON.parse(ev.target.result);
      canvas.loadFromJSON(d.fabric || d, () => {
        canvas.renderAll(); pushHistory(); setStatus('Annotations loaded');
      });
    }catch(err){ setStatus('Invalid JSON: ' + err.message); }
  };
  r.readAsText(f);
};

initCanvas();
</script>
</body>
</html>
"""

# Full-height iframe; no key kwarg (that was the bug)
components.html(APP_HTML, height=1000, scrolling=False)
