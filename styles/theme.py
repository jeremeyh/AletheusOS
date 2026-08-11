import streamlit as st


def inject_cardhawk_styles():
    st.markdown(
        """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    :root{--bg:#05070B;--gold:#D4AF37;--gold2:#F4C542;--muted:#A8AFBC;--white:#F8FAFC;--green:#35D66B;--red:#FF5C5C;}
    html, body, [class*="css"]{font-family:'Inter', sans-serif;}
    .stApp{background:radial-gradient(circle at 50% 2%, rgba(212,175,55,.12), transparent 31%),radial-gradient(circle at 5% 20%, rgba(212,175,55,.07), transparent 24%),linear-gradient(135deg, #05070B 0%, #080B10 48%, #030407 100%);color:var(--white);}
    .block-container{max-width:1400px;padding-top:1.2rem;padding-bottom:2rem;}
    header[data-testid="stHeader"]{background:rgba(0,0,0,0);}
    section[data-testid="stSidebar"]{width:300px !important;background:radial-gradient(circle at 50% 5%, rgba(212,175,55,.17), transparent 30%),linear-gradient(180deg,#05070A 0%,#070A0F 100%) !important;border-right:1px solid rgba(212,175,55,.50);}
    section[data-testid="stSidebar"] *{color:var(--white);}
    .sidebar-logo-wrap{text-align:center;margin-top:-.25rem;margin-bottom:.35rem;}
    .sidebar-logo{width:258px;max-width:96%;display:block;margin:0 auto;filter:drop-shadow(0 0 22px rgba(212,175,55,.22));}
    .sidebar-title{text-align:center;font-size:1.82rem;font-weight:900;letter-spacing:-.04em;margin-top:3px;}
    .sidebar-title span{color:var(--gold2);}
    .sidebar-caption{text-align:center;color:#F1D56A;font-size:.92rem;margin-top:6px;margin-bottom:30px;}
    .sidebar-section{color:var(--gold2);font-size:.72rem;font-weight:900;letter-spacing:.16em;text-transform:uppercase;margin:22px 0 12px 10px;}
    .stRadio label{border-radius:10px;padding:7px 10px !important;}
    .stRadio label:has(input:checked){background:linear-gradient(90deg,rgba(212,175,55,.30),rgba(212,175,55,.055));border-left:4px solid var(--gold2);}
    .sidebar-footer{border:1px solid rgba(212,175,55,.55);border-radius:14px;padding:18px;margin:38px 8px 28px;background:linear-gradient(180deg,rgba(212,175,55,.08),rgba(255,255,255,.02));}
    .sidebar-footer-title{color:var(--gold2);font-size:.82rem;font-weight:900;letter-spacing:.08em;text-transform:uppercase;}
    .sidebar-footer-caption{color:#E5E7EB;margin-top:12px;font-size:.86rem;}
    .footer{text-align:center;color:#7E8593;font-size:.80rem;margin:28px 0 8px;}
    .hero{text-align:center;padding-top:8px;}
    .hero-mark{width:216px;max-width:28vw;display:block;margin:0 auto;filter:drop-shadow(0 0 42px rgba(212,175,55,.48));opacity:.99;}
    .hero-title{color:var(--gold2);font-size:1.10rem;font-weight:800;letter-spacing:.48em;text-transform:uppercase;margin-top:18px;text-shadow:0 0 18px rgba(212,175,55,.28);}
    .hero-divider{display:flex;align-items:center;justify-content:center;gap:14px;margin:25px 0 26px;}
    .hero-divider:before,.hero-divider:after{content:"";height:1px;flex:1;background:linear-gradient(90deg,transparent,rgba(212,175,55,.62));}
    .hero-divider:after{background:linear-gradient(90deg,rgba(212,175,55,.62),transparent);}
    .diamond{color:var(--gold2);}
    .metric-card{position:relative;overflow:hidden;background:radial-gradient(circle at 50% 0%,rgba(212,175,55,.10),transparent 36%),linear-gradient(180deg,rgba(255,255,255,.045),rgba(255,255,255,.012));border:1px solid rgba(255,255,255,.18);border-radius:12px;min-height:194px;padding:24px 18px 20px;text-align:center;box-shadow:0 12px 34px rgba(0,0,0,.30);transition:.22s ease;}
    .metric-card:hover{transform:translateY(-4px);border-color:rgba(212,175,55,.82);box-shadow:0 16px 42px rgba(0,0,0,.35),0 0 32px rgba(212,175,55,.18);}
    .metric-top-gradient{position:absolute;top:0;left:0;width:100%;height:3px;background:linear-gradient(90deg,transparent,rgba(244,197,66,.90),transparent);}
    .metric-icon{width:72px;height:72px;border:1px solid var(--gold2);border-radius:50%;display:flex;align-items:center;justify-content:center;color:var(--gold2);margin:0 auto 18px;font-size:1.84rem;background:rgba(212,175,55,.07);}
    .metric-label{color:var(--gold2);text-transform:uppercase;font-weight:900;font-size:.74rem;letter-spacing:.12em;margin-bottom:10px;}
    .metric-value{color:#FFF;font-size:2.24rem;font-weight:900;letter-spacing:-.045em;line-height:1.02;}
    .metric-sub{color:#D5D9E2;font-size:.86rem;margin-top:14px;}
    .metric-sub .up,.trend{color:var(--green);font-weight:700;}
    .panel{position:relative;overflow:hidden;background:radial-gradient(circle at 40% 0%,rgba(212,175,55,.060),transparent 31%),linear-gradient(180deg,rgba(255,255,255,.034),rgba(255,255,255,.01));border:1px solid rgba(255,255,255,.13);border-radius:11px;padding:20px 22px;min-height:245px;box-shadow:0 10px 30px rgba(0,0,0,.25);}
    .panel-reflection{position:absolute;top:0;left:0;width:100%;height:1px;background:linear-gradient(90deg,transparent,rgba(244,197,66,.45),transparent);}
    .panel-title{color:var(--gold2);font-size:.86rem;font-weight:900;text-transform:uppercase;letter-spacing:.17em;margin-bottom:18px;}
    .panel-link{color:var(--gold2);font-size:.82rem;float:right;margin-top:-36px;}
    .row-item{display:grid;grid-template-columns:56px 1fr auto;gap:14px;align-items:center;padding:10px 0;border-bottom:1px solid rgba(255,255,255,.08);}
    .thumb{width:48px;height:48px;border-radius:6px;background:linear-gradient(135deg,rgba(212,175,55,.50),rgba(90,63,19,.30));border:1px solid rgba(212,175,55,.25);display:flex;align-items:center;justify-content:center;font-size:1.3rem;object-fit:cover;}
    .asset-img{width:48px;height:48px;border-radius:6px;object-fit:cover;border:1px solid rgba(212,175,55,.28);}
    .item-title{color:#FFF;font-size:.94rem;font-weight:600;margin-bottom:4px;}
    .item-sub{color:var(--muted);font-size:.79rem;}
    .item-price{color:#FFF;font-size:.92rem;text-align:right;white-space:nowrap;}
    .gold-chart{width:100%;height:245px;display:block;overflow:visible;}
    .chart-grid{stroke:rgba(255,255,255,.085);stroke-width:1;}
    .chart-line{fill:none;stroke:#F4C542;stroke-width:3.35;}
    .chart-area{fill:url(#goldGradient);opacity:.78;}
    .chart-label{fill:#A8AFBC;font-size:11px;font-family:Inter,sans-serif;}
    .interactive-donut-wrap{width:245px;max-width:100%;margin:0 auto;}
    .interactive-donut{width:245px;height:245px;max-width:100%;transform:rotate(-90deg);overflow:visible;}
    .donut-segment{transition:.18s ease;cursor:pointer;opacity:.95;}
    .donut-segment:hover{stroke-width:22;opacity:1;filter:drop-shadow(0 0 14px rgba(244,197,66,.46));}
    .donut-center-label,.donut-center-value{transform:rotate(90deg);transform-origin:60px 60px;fill:#F4C542;font-family:Inter,sans-serif;pointer-events:none;}
    .donut-center-label{font-size:7px;letter-spacing:.22em;font-weight:900;}
    .donut-center-value{font-size:13px;font-weight:900;fill:#FFF;}
    .breakdown-row{display:grid;grid-template-columns:18px 1fr auto;align-items:center;gap:12px;margin:17px 0;padding:4px 6px;border-radius:8px;}
    .legend-box{width:16px;height:16px;border-radius:4px;background:var(--gold2);}
    .legend-blue{background:#4BA3E3}.legend-purple{background:#7357D6}.legend-violet{background:#8D4CC2}
    .legend-label,.legend-value{color:#F2F4F8;font-size:.90rem;}
    .stButton > button{background:linear-gradient(135deg,#F4C542,#9B6A15);color:#090A0D;border:none;border-radius:10px;font-weight:900;}
    div[data-testid="stDataFrame"]{border:1px solid rgba(212,175,55,.20);border-radius:10px;overflow:hidden;}
    div[data-baseweb="select"] > div,div[data-testid="stTextInput"] input,div[data-testid="stNumberInput"] input,textarea{background:#0B0F16 !important;color:#FFF !important;border-color:rgba(212,175,55,.22) !important;}
    </style>
    """,
        unsafe_allow_html=True,
    )
