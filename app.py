import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import io
import json
from datetime import datetime

# ---------- Page Config ----------
st.set_page_config(
    page_title="Floor Plan Cable Routing",
    page_icon="🔌",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Session State Init ----------
if "canvas_key" not in st.session_state:
    st.session_state.canvas_key = 0
if "undo_stack" not in st.session_state:
    st.session_state.undo_stack = []
if "redo_stack" not in st.session_state:
    st.session_state.redo_stack = []
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None
if "image_size" not in st.session_state:
    st.session_state.image_size = (900, 650)
if "saved_shapes" not in st.session_state:
    st.session_state.saved_shapes = None  # persists shapes across reruns

# ---------- Custom CSS ----------
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #2563eb, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .sub-header {
        color: #6b7280;
        margin-top: 0;
        font-size: 0.95rem;
    }
    .tool-badge {
        display: inline-block;
        padding: 2px 8px;
        background: #eef2ff;
        color: #4338ca;
        border-radius: 6px;
        font-size: 0.75rem;
        margin-right: 4px;
    }
    .stButton button { border-radius: 8px; }
    .block-container { padding-top: 1.2rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Header ----------
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown('<p class="main-header">🔌 Floor Plan Cable Routing Studio</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Upload a floor plan, draw cable routes, add labels, and export your annotated layout.</p>',
        unsafe_allow_html=True,
    )

# ---------- Sidebar ----------
with st.sidebar:
    st.header("⚙️ Configuration")

    uploaded_file = st.file_uploader(
        "📤 Upload floor plan image",
        type=["png", "jpg", "jpeg", "bmp", "webp"],
    )

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

    if drawing_mode == "freedraw":
        st.caption("💡 Tip: hold and drag to draw cable runs.")

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

    st.divider()
    st.caption("Built with Streamlit + drawable-canvas")

# ---------- Process uploaded image ----------
if uploaded_file is not None:
    try:
        img = Image.open(uploaded_file).convert("RGBA")
    except Exception as e:
        st.error(f"Could not open image: {e}")
        st.stop()

    # Fit within working canvas while preserving aspect ratio
    MAX_W, MAX_H = 1000, 700
    w, h = img.size
    ratio = min(MAX_W / w, MAX_H / h, 1.0)
    new_w, new_h = int(w * ratio), int(h * ratio)
    img = img.resize((new_w, new_h), Image.LANCZOS)

    st.session_state.uploaded_image = img
    st.session_state.image_size = (new_w, new_h)
else:
    img = st.session_state.uploaded_image

# ---------- Main Area ----------
if img is None:
    st.info("👆 Upload a floor plan image from the sidebar to get started.")
    st.markdown(
        """
        ### How to use
        1. **Upload** your floor plan (PNG/JPG).
        2. Pick a **tool** from the sidebar:
           - 🖊️ **Pen** — freehand cable routes
           - 📏 **Line** — straight segments
           - ⬛ **Rectangle / Circle** — equipment, nodes, cabinets
           - 🔤 **Text** — labels like *"AP-01"* or *"Switch A"*
           - 🧹 **Eraser** — remove strokes
        3. Customize **color, stroke width, fill**.
        4. **Undo/Redo** mistakes, then **Export** PNG or JSON.
        """
    )
    st.stop()

# Canvas state reset handler
if reset_img:
    st.session_state.canvas_key += 1
    st.session_state.undo_stack = []
    st.session_state.redo_stack = []
    st.session_state.saved_shapes = None

if clear_clicked:
    # push current to undo, clear
    if st.session_state.saved_shapes:
        st.session_state.undo_stack.append(st.session_state.saved_shapes)
    st.session_state.saved_shapes = None
    st.session_state.canvas_key += 1

canvas_w, canvas_h = st.session_state.image_size

# Prepare initial drawing
initial_drawing = st.session_state.saved_shapes

# Draw the canvas
canvas_result = st_canvas(
    fill_color=fill_color,
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_image=img,
    update_streamlit=True,
    height=canvas_h,
    width=canvas_w,
    drawing_mode=drawing_mode if drawing_mode != "transform" else "transform",
    point_display_radius=3,
    key=f"canvas_{st.session_state.canvas_key}",
    initial_drawing=initial_drawing,
    display_toolbar=True,
)

# Save current state
if canvas_result.json_data is not None:
    current_shapes = canvas_result.json_data
    # Only treat as new state if it differs (avoids push on every rerun)
    prev = st.session_state.saved_shapes
    if prev is None or json.dumps(prev, sort_keys=True) != json.dumps(current_shapes, sort_keys=True):
        # Detect a new "action" (object count grew) to push undo
        prev_count = len(prev["objects"]) if prev and "objects" in prev else 0
        cur_count = len(current_shapes.get("objects", []))
        if cur_count > prev_count or (prev and cur_count >= prev_count):
            st.session_state.undo_stack.append(prev) if prev else None
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

# ---------- Render composite PNG ----------
def render_composite():
    base = st.session_state.uploaded_image.copy()
    if base.mode != "RGBA":
        base = base.convert("RGBA")

    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    shapes = st.session_state.saved_shapes
    if not shapes or "objects" not in shapes:
        return base

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 24)
    except Exception:
        font = ImageFont.load_default()

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
            x1, y1 = obj.get("x1", 0), obj.get("y1", 0)
            x2, y2 = obj.get("x2", 0), obj.get("y2", 0)
            draw.line([(x1, y1), (x2, y2)], fill=stroke, width=sw)

        elif otype == "rect":
            x, y = obj.get("left", 0), obj.get("top", 0)
            w = obj.get("width", 0) * obj.get("scaleX", 1)
            h = obj.get("height", 0) * obj.get("scaleY", 1)
            box = [x - w/2, y - h/2, x + w/2, y + h/2]
            draw.rectangle(box, outline=stroke, width=sw, fill=fill)

        elif otype == "circle":
            cx, cy = obj.get("left", 0), obj.get("top", 0)
            r = obj.get("radius", 10) * max(obj.get("scaleX", 1), obj.get("scaleY", 1))
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=stroke, width=sw, fill=fill)

        elif otype in ("i-text", "text", "textbox"):
            tx = obj.get("left", 0)
            ty = obj.get("top", 0)
            text = obj.get("text", "")
            fs = int(obj.get("fontSize", 20))
            try:
                f = ImageFont.truetype("DejaVuSans-Bold.ttf", fs)
            except Exception:
                f = font
            # i-text coords are baseline-ish; nudge up
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

# ---------- Preview + Stats ----------
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
