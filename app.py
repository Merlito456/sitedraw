import streamlit as st
import streamlit.components.v1 as components
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageDraw, ImageFont
import io
import json
import base64
from datetime import datetime

# ---------- Page ----------
st.set_page_config(
    page_title="Floor Plan Cable Routing",
    page_icon="🔌",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Session state ----------
_defaults = {
    "canvas_key": 0,
    "undo_stack": [],
    "redo_stack": [],
    "uploaded_image": None,
    "image_size": (900, 650),
    "saved_shapes": None,
    "pasted_image": None,
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------- CSS ----------
st.markdown(
    """
    <style>
    .main-header{font-size:2rem;font-weight:700;
        background:linear-gradient(90deg,#2563eb,#7c3aed);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:0}
    .sub-header{color:#6b7280;margin-top:0;font-size:.95rem}
    .paste-hint{background:#eef2ff;border-left:4px solid #6366f1;padding:8px 12px;
        border-radius:6px;font-size:.85rem;color:#3730a3;margin-bottom:8px}
    .stButton button{border-radius:8px}
    .block-container{padding-top:1.2rem}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<p class="main-header">🔌 Floor Plan Cable Routing Studio</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Upload or paste a floor plan, draw cable routes, add labels, and export.</p>', unsafe_allow_html=True)

# ============================================================
# PASTE CAPTURE — reads ?paste=<b64> from URL query params.
# The iframe writes the pasted image into the parent URL via
# window.parent.history.replaceState, then triggers a rerun.
# ============================================================
PASTE_HTML = r"""
<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
  html,body{margin:0;padding:0;font-family:system-ui,sans-serif;background:transparent}
  #zone{border:2px dashed #6366f1;border-radius:10px;padding:12px;text-align:center;
    color:#4338ca;background:#eef2ff;font-size:.85rem;cursor:pointer;outline:none;transition:.15s}
  #zone:hover{background:#e0e7ff}
  #zone.drag{background:#c7d2fe;border-color:#4338ca}
  #status{color:#059669;font-size:.75rem;margin-top:4px;min-height:1em}
</style></head><body>
<div id="zone" tabindex="0">
  📋 <b>Click here, then press Ctrl+V</b> (⌘+V on Mac)<br>
  <span style="font-size:.72rem;color:#6366f1">…or drag &amp; drop an image</span>
  <div id="status"></div>
</div>
<script>
(function(){
  const zone=document.getElementById('zone'), status=document.getElementById('status');
  const TOP = window.parent;

  function push(dataUrl){
    try {
      const u = new URL(TOP.location.href);
      // strip previous paste to keep URL small
      u.searchParams.delete('paste');
      u.searchParams.set('paste', dataUrl);
      TOP.history.replaceState({}, '', u.toString());
      status.textContent = '✓ Sent to app…';
      // trigger Streamlit rerun by dispatching a popstate on the parent
      TOP.dispatchEvent(new PopStateEvent('popstate', {state:{}}));
      // Fallback: reload the parent after a short delay
      setTimeout(()=>{ try{ TOP.location.reload(); }catch(e){} }, 250);
    } catch(e) {
      status.textContent = '✗ Could not send: ' + e.message;
    }
  }

  function handleFile(file){
    if(!file || !file.type || file.type.indexOf('image')!==0) return false;
    const r = new FileReader();
    r.onload = e => {
      status.textContent = '✓ Loaded (' + Math.round(file.size/1024) + ' KB)';
      push(e.target.result);
    };
    r.readAsDataURL(file);
    return true;
  }

  function onPaste(e){
    const items = (e.clipboardData || window.clipboardData || {}).items || [];
    for(const it of items){
      if(it.kind==='file' && it.type.indexOf('image')===0){
        if(handleFile(it.getAsFile())){ e.preventDefault(); return; }
      }
    }
    status.textContent = 'No image found in clipboard.';
  }

  zone.addEventListener('paste', onPaste);
  document.addEventListener('paste', onPaste);
  zone.addEventListener('click', ()=>{ zone.focus(); status.textContent='Ready — press Ctrl+V'; });
  ['dragenter','dragover'].forEach(ev=>zone.addEventListener(ev,e=>{
    e.preventDefault(); e.stopPropagation(); zone.classList.add('drag');
  }));
  ['dragleave','drop'].forEach(ev=>zone.addEventListener(ev,e=>{
    e.preventDefault(); e.stopPropagation(); zone.classList.remove('drag');
  }));
  zone.addEventListener('drop', e=>{
    const f = e.dataTransfer.files;
    if(f && f.length) handleFile(f[0]);
  });

  if(window.Streamlit && window.Streamlit.setFrameHeight) window.Streamlit.setFrameHeight(85);
})();
</script></body></html>
"""

# ---------- Sidebar ----------
with st.sidebar:
    st.header("⚙️ Configuration")

    tab_upload, tab_paste = st.tabs(["📤 Upload file", "📋 Paste screenshot"])

    uploaded_file = None
    with tab_upload:
        uploaded_file = st.file_uploader(
            "Choose floor plan image",
            type=["png", "jpg", "jpeg", "bmp", "webp"],
            label_visibility="collapsed",
        )

    with tab_paste:
        st.markdown(
            '<div class="paste-hint">Screenshot first (Win+Shift+S / ⌘+Shift+4), '
            'then paste below with <b>Ctrl+V</b>.</div>',
            unsafe_allow_html=True,
        )
        components.html(PASTE_HTML, height=85)

    st.divider()
    st.subheader("🖌️ Drawing Tool")

    drawing_mode_label = st.selectbox(
        "Tool",
        [
            "freedraw (Pen / Cable Route)",
            "line (Straight Segment)",
            "rect (Rectangle / Equipment)",
            "circle (Circle / Node)",
            "polygon (Zone)",
            "transform (Move / Resize)",
            "text (Add Label)",
            "eraser (Erase)",
        ],
        index=0,
    )
    drawing_mode = drawing_mode_label.split(" ")[0]

    stroke_width = st.slider("Stroke width", 1, 25, 4)
    stroke_color = st.color_picker("Stroke color", "#ef4444")

    if drawing_mode == "text":
        text_value = st.text_input("Text to add", "Outlet A")
        font_size = st.slider("Font size", 10, 72, 24)
    else:
        text_value = ""
        font_size = 24

    if drawing_mode in ("rect", "circle", "polygon"):
        fill_color = st.color_picker("Fill color", "#ef444422")
    else:
        fill_color = "rgba(255,255,255,0)"

    st.divider()
    st.subheader("🔧 Actions")
    ca, cb = st.columns(2)
    with ca: undo_clicked = st.button("↩️ Undo", use_container_width=True)
    with cb: redo_clicked = st.button("↪️ Redo", use_container_width=True)
    clear_clicked  = st.button("🗑️ Clear drawings", use_container_width=True)
    reset_img      = st.button("🔄 Reload image", use_container_width=True)

    st.divider()
    st.subheader("💾 Export")
    export_png_btn  = st.button("⬇️ Download annotated PNG", use_container_width=True)
    export_json_btn = st.button("⬇️ Download annotations (JSON)", use_container_width=True)

    st.caption("Built with Streamlit + drawable-canvas")

# ---------- Pull pasted image from query params ----------
def _load_pasted_from_query():
    try:
        qp = st.query_params
        raw = qp.get("paste")
        if not raw:
            return None
        if isinstance(raw, list):
            raw = raw[0]
        if not isinstance(raw, str) or not raw.startswith("data:image"):
            return None
        header, b64 = raw.split(",", 1)
        img_bytes = base64.b64decode(b64)
        return Image.open(io.BytesIO(img_bytes)).convert("RGBA")
    except Exception as e:
        st.warning(f"Could not decode pasted image: {e}")
        return None

pasted_img = _load_pasted_from_query()
if pasted_img is not None:
    st.session_state.pasted_image = pasted_img
    # Clear the param so it doesn't re-trigger forever
    try:
        del st.query_params["paste"]
    except Exception:
        pass
    st.toast("📋 Pasted image loaded!", icon="✅")

# ---------- Resolve image ----------
img = None
if uploaded_file is not None:
    try:
        img = Image.open(uploaded_file).convert("RGBA")
    except Exception as e:
        st.error(f"Could not open image: {e}")
        st.stop()
elif st.session_state.pasted_image is not None:
    img = st.session_state.pasted_image

if img is not None:
    MAX_W, MAX_H = 1000, 700
    w, h = img.size
    ratio = min(MAX_W / w, MAX_H / h, 1.0)
    nw, nh = int(w * ratio), int(h * ratio)
    img = img.resize((nw, nh), Image.LANCZOS)
    st.session_state.uploaded_image = img
    st.session_state.image_size = (nw, nh)
else:
    img = st.session_state.uploaded_image

# ---------- Empty state ----------
if img is None:
    st.info("👆 Upload a file **or paste a screenshot** from the sidebar to get started.")
    st.markdown("""
    ### How to use
    1. **Upload** or **paste** (Ctrl+V) a floor plan.
    2. Pick a **tool**: Pen, Line, Rectangle, Circle, Text, Eraser.
    3. Customize **color, width, fill**.
    4. **Undo/Redo**, then **Export** PNG or JSON.
    """)
    st.stop()

# ---------- Reset / clear ----------
if reset_img:
    st.session_state.canvas_key += 1
    st.session_state.undo_stack = []
    st.session_state.redo_stack = []
    st.session_state.saved_shapes = None

if clear_clicked:
    if st.session_state.saved_shapes:
        st.session_state.undo_stack.append(st.session_state.saved_shapes)
    st.session_state.saved_shapes = None
    st.session_state.canvas_key += 1

cw, ch = st.session_state.image_size

# ---------- Canvas ----------
canvas_result = st_canvas(
    fill_color=fill_color,
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_image=img,
    update_streamlit=True,
    height=ch,
    width=cw,
    drawing_mode=drawing_mode,
    point_display_radius=3,
    key=f"canvas_{st.session_state.canvas_key}",
    initial_drawing=st.session_state.saved_shapes,
    display_toolbar=True,
)

if canvas_result.json_data is not None:
    cur = canvas_result.json_data
    prev = st.session_state.saved_shapes
    if prev is None or json.dumps(prev, sort_keys=True) != json.dumps(cur, sort_keys=True):
        pc = len(prev["objects"]) if prev and "objects" in prev else 0
        cc = len(cur.get("objects", []))
        if prev and cc >= pc:
            st.session_state.undo_stack.append(prev)
            if len(st.session_state.undo_stack) > 50:
                st.session_state.undo_stack.pop(0)
        st.session_state.saved_shapes = cur
        st.session_state.redo_stack = []

# ---------- Undo / Redo ----------
if undo_clicked:
    if st.session_state.undo_stack:
        last = st.session_state.undo_stack.pop()
        if st.session_state.saved_shapes is not None:
            st.session_state.redo_stack.append(st.session_state.saved_shapes)
        st.session_state.saved_shapes = last
        st.session_state.canvas_key += 1
        st.rerun()
    else:
        st.toast("Nothing to undo")

if redo_clicked:
    if st.session_state.redo_stack:
        nxt = st.session_state.redo_stack.pop()
        if st.session_state.saved_shapes is not None:
            st.session_state.undo_stack.append(st.session_state.saved_shapes)
        st.session_state.saved_shapes = nxt
        st.session_state.canvas_key += 1
        st.rerun()
    else:
        st.toast("Nothing to redo")

# ---------- Composite render ----------
def render_composite():
    base = st.session_state.uploaded_image.copy()
    if base.mode != "RGBA":
        base = base.convert("RGBA")
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    shapes = st.session_state.saved_shapes
    if not shapes or "objects" not in shapes:
        return base

    def parse_color(c):
        if not c: return (0, 0, 0, 255)
        if c.startswith("rgba"):
            p = c.strip("rgba() ").split(",")
            r, g, b = [int(float(x)) for x in p[:3]]
            a = int(float(p[3]) * 255) if len(p) > 3 else 255
            return (r, g, b, a)
        if c.startswith("rgb"):
            p = c.strip("rgb() ").split(",")
            return tuple(int(float(x)) for x in p[:3]) + (255,)
        if c.startswith("#"):
            h = c.lstrip("#")
            if len(h) == 6: return tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) + (255,)
            if len(h) == 8: return tuple(int(h[i:i+2], 16) for i in (0, 2, 4, 6))
        return (0, 0, 0, 255)

    for obj in shapes["objects"]:
        t = obj.get("type")
        stroke = parse_color(obj.get("stroke"))
        sw = int(obj.get("strokeWidth", 3) or 3)
        fill = parse_color(obj.get("fill")) if obj.get("fill") not in (None, "", "transparent") else None
        if fill == (0, 0, 0, 255): fill = None

        if t == "path":
            pts = []
            for cmd in obj.get("path", []):
                if cmd[0] in ("M", "L"): pts.append((cmd[1], cmd[2]))
                elif cmd[0] == "Q":       pts.append((cmd[3], cmd[4]))
            if len(pts) > 1:
                draw.line(pts, fill=stroke, width=sw, joint="curve")
        elif t == "line":
            draw.line([(obj.get("x1", 0), obj.get("y1", 0)),
                       (obj.get("x2", 0), obj.get("y2", 0))], fill=stroke, width=sw)
        elif t == "rect":
            x, y = obj.get("left", 0), obj.get("top", 0)
            w = obj.get("width", 0) * obj.get("scaleX", 1)
            h = obj.get("height", 0) * obj.get("scaleY", 1)
            draw.rectangle([x-w/2, y-h/2, x+w/2, y+h/2], outline=stroke, width=sw, fill=fill)
        elif t == "circle":
            cx, cy = obj.get("left", 0), obj.get("top", 0)
            r = obj.get("radius", 10) * max(obj.get("scaleX", 1), obj.get("scaleY", 1))
            draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=stroke, width=sw, fill=fill)
        elif t in ("i-text", "text", "textbox"):
            tx, ty = obj.get("left", 0), obj.get("top", 0)
            txt = obj.get("text", "")
            fs = int(obj.get("fontSize", 20))
            try: f = ImageFont.truetype("DejaVuSans-Bold.ttf", fs)
            except Exception: f = ImageFont.load_default()
            draw.text((tx, ty - fs), txt, fill=stroke, font=f)

    return Image.alpha_composite(base, overlay)

# ---------- Export ----------
if export_png_btn:
    buf = io.BytesIO()
    render_composite().convert("RGB").save(buf, format="PNG")
    buf.seek(0)
    st.sidebar.success("PNG ready!")
    st.sidebar.download_button(
        "📥 Save PNG now", data=buf,
        file_name=f"cable_routing_{datetime.now():%Y%m%d_%H%M%S}.png",
        mime="image/png", use_container_width=True,
    )

if export_json_btn:
    if st.session_state.saved_shapes:
        buf = io.BytesIO(json.dumps(st.session_state.saved_shapes, indent=2).encode())
        st.sidebar.download_button(
            "📥 Save JSON now", data=buf,
            file_name=f"annotations_{datetime.now():%Y%m%d_%H%M%S}.json",
            mime="application/json", use_container_width=True,
        )
    else:
        st.sidebar.warning("No annotations to export yet.")

# ---------- Stats ----------
st.divider()
c1, c2, c3 = st.columns(3)
c1.metric("Canvas", f"{cw} × {ch}px")
n_obj = len(st.session_state.saved_shapes.get("objects", [])) if st.session_state.saved_shapes else 0
c2.metric("Annotations", n_obj)
c3.metric("Undo steps", len(st.session_state.undo_stack))

with st.expander("👁️ Preview exported composite (PNG)"):
    st.image(render_composite(), use_container_width=True)
