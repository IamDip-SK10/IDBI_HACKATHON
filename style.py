def load_css(st):
    st.markdown("""
    <style>

    /* =========================
       GLOBAL BACKGROUND
    ========================= */
    .stApp {
        background-color: #f8fafc;
        color: #1f2937;
    }

    /* =========================
       GLASS CARD (LIGHT)
    ========================= */
    .glass {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 20px;
        backdrop-filter: blur(6px);
        -webkit-backdrop-filter: blur(6px);
        border: 1px solid rgba(0,0,0,0.08);
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* =========================
       HEADER STYLE
    ========================= */
    .header-glass {
        text-align: center;
        padding: 25px;
    }

    /* =========================
       BUTTON STYLE
    ========================= */
    .stButton>button {
        background: linear-gradient(135deg, #2563eb, #3b82f6);
        color: white;
        border-radius: 10px;
        height: 45px;
        font-weight: 600;
        border: none;
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #1d4ed8, #2563eb);
        color: white;
    }

    /* =========================
       METRIC CARDS
    ========================= */
    [data-testid="metric-container"] {
        background: white;
        border-radius: 10px;
        padding: 12px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    /* =========================
       SIDEBAR
    ========================= */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e5e7eb;
    }

    /* =========================
       TEXT IMPROVEMENTS
    ========================= */
    h1, h2, h3, h4 {
        color: #111827;
    }

    p, span, label {
        color: #374151;
    }

    /* =========================
       INPUT BOXES
    ========================= */
    input, textarea {
        border-radius: 8px !important;
    }

    </style>
    """, unsafe_allow_html=True)
