import streamlit as st
import streamlit.components.v1 as components
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import io
import json
import base64
from datetime import datetime

# ---------- Page Config ----------
st.set_page_config(
    page_title="Floor Plan Cable Routing",
    page_icon="🔌",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Session State Init ----------
defaults = {
    "canvas_key": 0,
    "undo_stack": [],
    "redo_stack": [],
    "uploaded_image": None,
    "image_size": (900, 650),
    "saved_shapes": None,
    "paste_counter": 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------- Custom CSS ----------
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2rem; font-weight: 700;
        background: linear-gradient(90deg, #2563eb, #7c3aed);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .sub-header { color: #6b7280; margin-top: 0; font-size: 0.95rem; }
    .stButton button { border-radius: 8px; }
    .block-container { padding-top: 1.2rem; }
    .paste-hint {
        background: #eef2ff; border-left: 4px solid #6366f1;
        padding: 8px 12px; border-radius: 6px; font-size: 0.85rem;
        color: #3730a3; margin-bottom: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Header ----------
st.markdown('<p class="main-header">🔌 Floor Plan Cable Routing Studio</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-header">Upload or paste a floor plan, draw cable routes, add labels, and export.</p>',
    unsafe_allow_html=True,
)

# ============================================================
# CLIPBOARD PASTE CAPTURE (JS → Streamlit bridge)
# ============================================================
# Hidden component listens for paste events globally and pushes
# the base64 PNG back into a hidden text_area via query params.
PASTE_BRIDGE_HTML = """
<div id="paste-zone" style="
    border: 2px dashed #6366f1; border-radius: 10px;
    padding: 14px; text-align: center; color: #4338ca;
    background: #eef2ff; font-family: system-ui; font-size: 0.9rem;
    cursor: text;" tabindex="0">
  📋 <b>Click here, then press Ctrl+V</b> (⌘+V on Mac) to paste a screenshot
  <div id="status" style="color:#059669; font-size:0.8rem; margin-top:4px;"></div>
</div>
<script>
(function() {
  const zone = document.getElementById('paste-zone');
  const status = document.getElementById('status');

  async function handlePaste(e) {
    const items = (e.clipboardData || window.clipboardData || {}).items || [];
    for (const item of items) {
      if (item.type && item.type.indexOf('image') === 0) {
        const blob = item.getAsFile();
        const reader = new FileReader();
        reader.onload = function(ev) {
          const dataUrl = ev.target.result;
          status.textContent = "✓ Image pasted — sending to app…";
          // Send to Streamlit via query-param-free channel:
          // use window.parent.postMessage + Streamlit.setComponentValue pattern
          window.parent.postMessage({
            isStreamlitMessage: true,
            type: "streamlit:setComponentValue",
            value: dataUrl,
            dataType: "string"
          }, "*");
        };
        reader.readAsDataURL(blob);
        e.preventDefault();
        return;
      }
    }
    status.textContent = "No image found in clipboard.";
  }

  zone.addEventListener('paste', handlePaste);
  document.addEventListener('paste', handlePaste);
  zone.focus();
})();
</script>
"""

def clipboard_paste_component(key):
    """Returns a base64 data URL string if the user pasted an image, else None."""
    return components.html(
        PASTE_BRIDGE_HTML,
        height=90,
        key=key,
    )

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

    pasted_data = None
    with tab_paste:
        st.markdown(
            '<div class="paste-hint">Take a screenshot (Win+Shift+S / ⌘+Shift+4), '
            'then paste below with <b>Ctrl+V</b>.</div>',
            unsafe_allow_html=True,
        )
        pasted_data = clipboard_paste_component(key=f"paste_{st.session_state.paste_counter}")

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
    col_a, col_b = st.columns(2)
    with col_a:
        undo_clicked = st.button("↩️ Undo", use_container_width=True)
    with col_b:
        redo_clicked = st.button("↪️ Redo", use_container_width=True)
    clear_clicked = st.button("🗑️ Clear all drawings", use_container_width=True)
    reset_img = st.button("🔄 Reload image", use_container_width=True)

    st.divider()
    st.subheader("💾 Export")
    export_png_btn = st.button("⬇️ Download annotated PNG", use_container_width=True)
    export_json_btn = st.button("⬇️ Download annotations (JSON)", use_container_width=True)

    st.caption("Built with Streamlit + drawable-canvas")

# ---------- Resolve image source (upload OR paste) ----------
def load_pasted_image(data_url: str) -> Image.Image | None:
    """Convert data:image/...;base64,... → PIL Image."""
    try:
        if not isinstance(data_url, str) or not data_url.startswith("data:image"):
            return None
        header, b64 = data_url.split(",", 1)
        raw = base64.b64decode(b64)
        return Image.open(io.BytesIO(raw)).convert("RGBA")
    except Exception as e:
        st.warning(f"Could not decode pasted image: {e}")
        return None

img = None

if uploaded_file is not None:
    try:
        img = Image.open(uploaded_file).convert("RGBA")
    except Exception as e:
        st.error(f"Could not open image: {e}")
        st.stop()

elif pasted_data:
    pasted_img = load_pasted_image(pasted_data)
    if pasted_img is not None:
        img = pasted_img
        st.toast("📋 Pasted image loaded!", icon="✅")

if img is not None:
    # Fit within working canvas while preserving aspect ratio
    MAX_W, MAX_H = 1000, 700
    w, h = img.size
    ratio = min(MAX_W / w, MAX_H / h, 1.0)
    new_w, new_h = int(w * ratio), int(h * ratio)
    img = img.resize((new_w, new_h), Image.LANCZOS)

    # If image changed (new upload/paste), reset drawing state
    prev_size = st.session_state.image_size
    st.session_state.uploaded_image = img
    st.session_state.image_size = (new_w, new_h)
    if prev_size != (new_w, new_h) and st.session_state.saved_shapes is not None:
        # keep drawings if same size; otherwise clear
        pass
else:
    img = st.session_state.uploaded_image

# ---------- Empty state ----------
if img is None:
    st.info("👆 Upload a file **or paste a screenshot** from the sidebar to get started.")
    st.markdown(
        """
        ### How to use
        1. **Upload** or **paste** (Ctrl+V) a floor plan.
        2. Pick a **tool**:
           - 🖊️ **Pen** — freehand cable routes
           - 📏 **Line** — straight segments
           - ⬛ **Rectangle / Circle** — equipment, nodes
           - 🔤 **Text** — labels (*AP-01*, *Switch A*)
           - 🧹 **Eraser** — remove strokes
        3. Customize **color, width, fill**.
        4. **Undo/Redo**, then **Export** PNG or JSON.
        """
    )
    st.stop()

# ---------- Reset handlers ----------
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

canvas_w, canvas_h = st.session_state.image_size

# ---------- Canvas ----------
canvas_result = st_canvas(
    fill_color=fill_color,
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_image=img,
    update_streamlit=True,
    height=canvas_h,
    width=canvas_w,
    drawing_mode=drawing_mode,
    point_display_radius=3,
    key=f"canvas_{st.session_state.canvas_key}",
    initial_drawing=st.session_state.saved_shapes,
    display_toolbar=True,
)

if canvas_result.json_data is not None:
    current_shapes = canvas_result.json_data
    prev = st.session_state.saved_shapes
    if prev is None or json.dumps(prev, sort_keys=True) != json.dumps(current_shapes, sort_keys=True):
        prev_count = len(prev["objects"]) if prev and "objects" in prev else 0
        cur_count = len(current_shapes.get("objects", []))
        if prev and cur_count >= prev_count:
            st.session_state.undo_stack.append(prev)
            if len(st.session_state.undo_stack) > 50:
                st.session_state.undo_stack.pop(0)
        st.session_state.saved_shapes = current_shapes
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
        if not c:
            return (0, 0, 0, 255)
        if c.startswith("rgba"):
            parts = c.strip("rgba() ").split(",")
            r, g, b = [int(float(x)) for x in parts[:3]]
            a = int(float(parts[3]) * 255) if len(parts) > 3 else 255
            return (r, g, b, a)
        if c.startswith("rgb"):
            parts = c.strip("rgb() ").split(",")
            r, g, b = [int(float(x)) for x in parts[:3]]
            return (r, g, b, 255)
        if c.startswith("#"):
            h = c.lstrip("#")
            if len(h) == 6:
                return tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) + (255,)
            if len(h) == 8:
                return tuple(int(h[i:i+2], 16) for i in (0, 2, 4, 6))
        return (0, 0, 0, 255)

    for obj in shapes["objects"]:
        otype = obj.get("type")
        stroke = parse_color(obj.get("stroke"))
        sw = int(obj.get("strokeWidth", 3) or 3)
        fill = parse_color(obj.get("fill")) if obj.get("fill") not in (None, "", "transparent") else None
        if fill == (0, 0, 0, 255):
            fill = None

        if otype == "path":
            pts = []
            for cmd in obj.get("path", []):
                if cmd[0] in ("M", "L"):
                    pts.append((cmd[1], cmd[2]))
                elif cmd[0] == "Q":
                    pts.append((cmd[3], cmd[4]))
            if len(pts) > 1:
                draw.line(pts, fill=stroke, width=sw, joint="curve")

        elif otype == "line":
            draw.line(
                [(obj.get("x1", 0), obj.get("y1", 0)), (obj.get("x2", 0), obj.get("y2", 0))],
                fill=stroke, width=sw,
            )

        elif otype == "rect":
            x, y = obj.get("left", 0), obj.get("top", 0)
            w = obj.get("width", 0) * obj.get("scaleX", 1)
            h = obj.get("height", 0) * obj.get("scaleY", 1)
            draw.rectangle([x - w/2, y - h/2, x + w/2, y + h/2], outline=stroke, width=sw, fill=fill)

        elif otype == "circle":
            cx, cy = obj.get("left", 0), obj.get("top", 0)
            r = obj.get("radius", 10) * max(obj.get("scaleX", 1), obj.get("scaleY", 1))
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=stroke, width=sw, fill=fill)

        elif otype in ("i-text", "text", "textbox"):
            tx, ty = obj.get("left", 0), obj.get("top", 0)
            text = obj.get("text", "")
            fs = int(obj.get("fontSize", 20))
            try:
                f = ImageFont.truetype("DejaVuSans-Bold.ttf", fs)
            except Exception:
                f = ImageFont.load_default()
            draw.text((tx, ty - fs), text, fill=stroke, font=f)

    return Image.alpha_composite(base, overlay)

# ---------- Export ----------
if export_png_btn:
    composite = render_composite()
    buf = io.BytesIO()
    composite.convert("RGB").save(buf, format="PNG")
    buf.seek(0)
    st.sidebar.success("PNG ready!")
    st.sidebar.download_button(
        "📥 Save PNG now",
        data=buf,
        file_name=f"cable_routing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
        mime="image/png",
        use_container_width=True,
    )

if export_json_btn:
    if st.session_state.saved_shapes:
        buf = io.BytesIO()
        buf.write(json.dumps(st.session_state.saved_shapes, indent=2).encode())
        buf.seek(0)
        st.sidebar.download_button(
            "📥 Save JSON now",
            data=buf,
            file_name=f"annotations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True,
        )
    else:
        st.sidebar.warning("No annotations to export yet.")

# ---------- Stats ----------
st.divider()
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Canvas", f"{canvas_w} × {canvas_h}px")
with c2:
    n_obj = len(st.session_state.saved_shapes.get("objects", [])) if st.session_state.saved_shapes else 0
    st.metric("Annotations", n_obj)
with c3:
    st.metric("Undo steps", len(st.session_state.undo_stack))

with st.expander("👁️ Preview exported composite (PNG)"):
    st.image(render_composite(), use_container_width=True, caption="Final annotated floor plan")
