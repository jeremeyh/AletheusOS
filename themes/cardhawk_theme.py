import streamlit as st


def apply_cardhawk_theme():
    st.markdown(
        """
    <style>
        :root {
            --ch-bg: #06080D;
            --ch-panel: #10131B;
            --ch-panel2: #171B25;
            --ch-gold: #D4AF37;
            --ch-gold2: #8E6F1E;
            --ch-text: #F7F0DF;
            --ch-muted: #AFA895;
            --ch-green: #31D17C;
        }

        .stApp {
            background:
                radial-gradient(circle at top center, rgba(212,175,55,0.08), transparent 26%),
                linear-gradient(180deg, #05070C 0%, #090B12 100%);
            color: var(--ch-text);
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0D1018 0%, #07090F 100%);
            border-right: 1px solid rgba(212,175,55,0.28);
        }

        [data-testid="stSidebar"] section { padding-top: 0 !important; }

        .ch-sidebar-top { margin-top: -1.55rem; padding-top: 0; }

        .ch-sidebar-subtitle {
            text-align: center;
            color: var(--ch-muted);
            font-size: 0.70rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-top: 0.05rem;
        }

        .ch-nav-group {
            color: var(--ch-gold);
            font-size: 0.70rem;
            text-transform: uppercase;
            letter-spacing: 0.18em;
            font-weight: 950;
            margin-top: 1rem;
            margin-bottom: 0.25rem;
        }

        h1, h2, h3 { color: var(--ch-text); letter-spacing: -0.04em; }

        .ch-hero {
            display:flex;
            flex-direction:column;
            align-items:center;
            justify-content:center;
            padding: 6px 24px 4px 24px;
            margin-bottom: 12px;
        }

        .ch-hero-title {
            color: var(--ch-gold);
            font-size: 1.02rem;
            letter-spacing: 0.34em;
            text-transform: uppercase;
            font-weight: 950;
            margin-top: 0.6rem;
            text-align:center;
        }

        .ch-hero-rule {
            width: 88%;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(212,175,55,0.76), transparent);
            margin: 18px auto 8px auto;
        }

        .ch-card {
            border: 1px solid rgba(212,175,55,0.28);
            border-radius: 18px;
            background:
                radial-gradient(circle at top left, rgba(212,175,55,0.16), transparent 36%),
                linear-gradient(180deg, rgba(255,255,255,0.052), rgba(255,255,255,0.018));
            box-shadow: 0 18px 46px rgba(0,0,0,0.28);
            padding: 18px;
            min-height: 116px;
            margin-bottom: 14px;
        }

        .ch-card:hover {
            border-color: rgba(212,175,55,0.58);
            transform: translateY(-1px);
            transition: 160ms ease;
        }

        .ch-card-label {
            color: var(--ch-muted);
            font-size: 0.70rem;
            text-transform: uppercase;
            letter-spacing: 0.13em;
            font-weight: 950;
        }

        .ch-card-value {
            font-size: 1.95rem;
            font-weight: 950;
            color: #FFFFFF;
            margin-top: 8px;
        }

        .ch-card-delta {
            color: var(--ch-green);
            font-size: 0.78rem;
            margin-top: 8px;
        }

        .ch-panel {
            border: 1px solid rgba(212,175,55,0.23);
            border-radius: 18px;
            background:
                radial-gradient(circle at top right, rgba(212,175,55,0.08), transparent 34%),
                linear-gradient(180deg, rgba(16,19,27,0.96), rgba(7,9,15,0.96));
            padding: 18px;
            box-shadow: 0 22px 52px rgba(0,0,0,0.26);
            min-height: 165px;
            margin-bottom: 16px;
        }

        .ch-panel-title {
            color: var(--ch-gold);
            font-size: 0.84rem;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            font-weight: 950;
            margin-bottom: 12px;
        }

        .ch-row {
            display:flex;
            align-items:center;
            justify-content:space-between;
            padding: 9px 0;
            border-bottom: 1px solid rgba(255,255,255,0.065);
            gap: 12px;
        }

        .ch-row:last-child { border-bottom:none; }

        .ch-muted { color: var(--ch-muted); }

        .ch-pill {
            display:inline-block;
            border: 1px solid rgba(212,175,55,0.42);
            color: var(--ch-gold);
            border-radius: 999px;
            padding: 3px 9px;
            font-size: 0.68rem;
            font-weight: 950;
            white-space: nowrap;
        }

        .stButton > button {
            background: linear-gradient(135deg, #D4AF37, #8E6F1E);
            color: #0B0D12;
            border: none;
            border-radius: 12px;
            font-weight: 950;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )
