import streamlit as st
import numpy as np
import joblib

st.set_page_config(page_title="House Price Predictor", page_icon="🏙️", layout="centered")

st.markdown("""
<style>
    /* ── Glass-blue theme ── */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(160deg, #071428 0%, #0c1f3f 50%, #071020 100%);
        min-height: 100vh;
    }
    [data-testid="stAppViewBlockContainer"] {
        background: transparent;
    }
    /* City skyline hero banner */
    .hero-banner {
        background: url("https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=900&q=80")
                    center/cover no-repeat;
        border-radius: 16px;
        padding: 40px 32px 24px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    .hero-banner::after {
        content: '';
        position: absolute; inset: 0;
        background: linear-gradient(180deg, rgba(7,20,40,0.55) 0%, rgba(7,20,40,0.82) 100%);
        border-radius: 16px;
    }
    .hero-content { position: relative; z-index: 1; }
    .hero-title {
        font-size: 2rem; font-weight: 700;
        color: #e0f2fe; letter-spacing: -0.5px;
        text-shadow: 0 2px 12px rgba(0,0,0,0.5);
    }
    .hero-sub { font-size: 1rem; color: #7dd3fc; margin-top: 6px; }
    /* Glass cards */
    .glass {
        background: rgba(14, 42, 80, 0.55);
        border: 1px solid rgba(147, 197, 253, 0.22);
        border-radius: 14px;
        padding: 20px 24px;
        backdrop-filter: blur(12px);
        margin-bottom: 16px;
    }
    .sec-label {
        font-size: 10px; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.1em;
        color: #60a5fa; margin-bottom: 12px;
    }
    /* Override Streamlit inputs */
    [data-testid="stNumberInput"] input,
    [data-testid="stTextInput"] input {
        background: rgba(7, 25, 55, 0.8) !important;
        border: 1px solid rgba(147,197,253,0.25) !important;
        border-radius: 8px !important;
        color: #e0f2fe !important;
    }
    [data-testid="stNumberInput"] input:focus,
    [data-testid="stTextInput"] input:focus {
        border-color: #60a5fa !important;
        box-shadow: 0 0 0 2px rgba(96,165,250,0.2) !important;
    }
    /* Labels */
    label { color: #93c5fd !important; font-size: 13px !important; }
    /* Slider */
    [data-testid="stSlider"] .stSlider { color: #60a5fa; }
    /* Primary button */
    [data-testid="stButton"] button[kind="primary"] {
        background: rgba(59,130,246,0.85) !important;
        border: 1px solid rgba(147,197,253,0.4) !important;
        border-radius: 12px !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 14px !important;
        font-size: 15px !important;
        transition: background 0.15s !important;
    }
    [data-testid="stButton"] button[kind="primary"]:hover {
        background: #3b82f6 !important;
    }
    /* Result box */
    .result-box {
        background: rgba(14, 60, 100, 0.65);
        border: 1px solid rgba(147, 197, 253, 0.3);
        border-radius: 14px;
        padding: 28px 24px;
        text-align: center;
        backdrop-filter: blur(8px);
    }
    .result-label {
        font-size: 11px; letter-spacing: 0.1em;
        text-transform: uppercase; color: #7dd3fc;
    }
    .result-price {
        font-size: 3rem; font-weight: 700;
        color: #bfdbfe; letter-spacing: -1px; margin: 8px 0;
    }
    .result-meta { font-size: 13px; color: #60a5fa; }
    /* Info box */
    [data-testid="stInfo"] {
        background: rgba(14,42,80,0.5) !important;
        border: 1px solid rgba(147,197,253,0.2) !important;
        color: #93c5fd !important;
    }
    /* Hide default header */
    header { visibility: hidden; }
    /* Dividers */
    hr { border-color: rgba(147,197,253,0.15) !important; }
    /* Markdown text color */
    p, .stMarkdown { color: #93c5fd !important; }
</style>

<!-- Hero banner with city skyline -->
<div class="hero-banner">
  <div class="hero-content">
    <div class="hero-title">🏙️ House Price Predictor</div>
    <div class="hero-sub">ML-powered instant valuation · Enter property details below</div>
  </div>
</div>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

model = load_model()

st.markdown('<div class="glass">', unsafe_allow_html=True)
st.markdown('<p class="sec-label">Property details</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    bedrooms   = st.number_input("🛏  Bedrooms",        min_value=0, max_value=20, value=3,    step=1)
    living_area= st.number_input("📐  Living area (sq ft)", min_value=0, max_value=20000, value=2000, step=50)
with col2:
    bathrooms  = st.number_input("🚿  Bathrooms",       min_value=0, max_value=20, value=2,    step=1)
    schools    = st.number_input("🏫  Schools nearby",  min_value=0, max_value=20, value=2,    step=1)

st.markdown('<p class="sec-label" style="margin-top:16px">House condition</p>', unsafe_allow_html=True)
cond_map = {1:"1 — Poor", 2:"2 — Fair", 3:"3 — Good", 4:"4 — Very good", 5:"5 — Excellent"}
condition = st.select_slider(
    "condition_slider",
    options=[1,2,3,4,5],
    value=3,
    format_func=lambda x: cond_map[x],
    label_visibility="collapsed",
)
st.markdown('</div>', unsafe_allow_html=True)

predict_clicked = st.button("✨  Predict price", use_container_width=True, type="primary")

if predict_clicked:
    X = np.array([[bedrooms, bathrooms, living_area, condition, schools]])
    pred = model.predict(X)[0]
    st.markdown(f"""
    <div class="result-box">
        <div class="result-label">Estimated market value</div>
        <div class="result-price">${pred:,.0f}</div>
        <div class="result-meta">
            {bedrooms} bed &nbsp;·&nbsp; {bathrooms} bath &nbsp;·&nbsp;
            {living_area:,} sq ft &nbsp;·&nbsp; condition {condition}
            &nbsp;·&nbsp; {schools} school{'s' if schools != 1 else ''} nearby
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.balloons()
else:
    st.info("💡 Fill in the details above and click **Predict price**")