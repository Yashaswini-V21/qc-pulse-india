import streamlit as st
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings('ignore')

# ─── PAGE CONFIG ────────────────────────────────────────────
st.set_page_config(
    page_title="QC Pulse India",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── PREMIUM CSS ────────────────────────────────────────────
from utils.styles import load_custom_css
st.markdown(load_custom_css(), unsafe_allow_html=True)


# ─── DATA LOADING ────────────────────────────────────────────
from utils.data_loader import load_data

try:
    bl, ze, bb, gr, rfm, rfm_sum, pm, cohort, sk, ar = load_data()
except Exception as e:
    st.error(f"❌ Data load failed: {e}")
    st.info("Make sure you've run all notebooks (01→07) first.")
    st.stop()


# ─── SIDEBAR ─────────────────────────────────────────────────
with st.sidebar:
    # Brand Logo
    st.markdown("""
    <div style='padding: 24px 20px 16px;
                border-bottom: 1px solid rgba(139,92,246,0.1);
                margin-bottom: 20px;'>
        <h2 style='font-size: 20px !important;
                    font-weight: 800 !important;
                    background: linear-gradient(135deg, #8B5CF6, #3B82F6, #06B6D4);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    letter-spacing: -0.03em;
                    margin: 0 !important;'>QC Pulse India</h2>
        <p style='font-size: 11px;
                   color: #475569;
                   margin: 4px 0 0;
                   text-transform: uppercase;
                   letter-spacing: 0.1em;'>Quick Commerce Intelligence</p>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "",
        ["📊  Overview",
         "⚔️  Price Intelligence",
         "⭐  Review & Rating",
         "🛒  Market Basket",
         "👥  Customer Segments",
         "📈  Cohort Retention",
         "🌊  Customer Journey",
         "🎯  Business Simulator",
         "🔬  Data Quality"],
        label_visibility="collapsed"
    )

    st.markdown("""
    <hr style='border:none; height:1px;
               background: linear-gradient(90deg, transparent,
               rgba(139,92,246,0.2), transparent);
               margin:16px 0'>
    """, unsafe_allow_html=True)
    st.markdown("<p class='section-label'>Live Stats</p>", unsafe_allow_html=True)

    total_prod = len(bl) + len(ze) + len(bb)
    for icon, val, label in [
        ("🛒", f"{total_prod:,}", "products"),
        ("👥", f"{rfm['customer_id'].nunique():,}", "customers"),
        ("📦", f"{len(gr):,}", "transactions"),
        ("🏪", "3", "platforms analysed"),
        ("🔮", "3", "simulation models"),
        ("🤖", "ON", "auto-intelligence"),
    ]:
        st.markdown(f"""
        <div style='display:flex; align-items:center; gap:10px;
                    padding:8px 0;
                    border-bottom:1px solid rgba(139,92,246,0.08)'>
            <span style='font-size:14px'>{icon}</span>
            <div>
                <div style='font-size:14px; font-weight:700;
                            background: linear-gradient(135deg, #F8FAFC, #A78BFA);
                            -webkit-background-clip: text;
                            -webkit-text-fill-color: transparent;'>{val}</div>
                <div style='font-size:10px; color:#475569;
                            text-transform:uppercase;
                            letter-spacing:.07em;
                            font-weight:600'>{label}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:10px; color:#334155;
                text-align:center; padding:8px 0'>
        Built by Yashaswini V<br>
        <span style='color:#8B5CF6'>●</span> May 2026
    </div>
    """, unsafe_allow_html=True)


# ─── GLOBAL LIVE SYSTEM STATS TICKER ──────────────────────────
st.markdown("""
<div style='display: flex; align-items: center; justify-content: space-between;
            padding: 10px 18px; margin-bottom: 24px;
            background: linear-gradient(135deg, rgba(13,20,35,0.7) 0%, rgba(7,10,22,0.6) 100%);
            border: 1px solid rgba(139,92,246,0.18); border-radius: 12px;
            backdrop-filter: blur(15px); box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            animation: fadeIn 1s ease;
            flex-wrap: wrap; gap: 8px;'>
    <div style='display: flex; align-items: center; gap: 8px; font-size: 11.5px; font-weight: 600; color: #94A3B8;'>
        <span class="status-dot status-live" style="margin: 0; width: 8px; height: 8px;"></span>
        <span style="color: #22D3EE; text-transform: uppercase; letter-spacing: 0.05em;">Live Pipeline:</span>
        <span>38,765 transactions · 39,357 products · 3 platforms</span>
    </div>
    <div style='display: flex; align-items: center; gap: 14px; font-size: 11px; font-weight: 500; color: #64748B; flex-wrap: wrap;'>
        <span>⚡ RFM: <span style='color: #FF3366; font-weight: 700;'>5 Segments</span></span>
        <span style='color: rgba(139,92,246,0.2);'>|</span>
        <span>📊 Cohort: <span style='color: #00F5A0; font-weight: 700;'>24 Months</span></span>
        <span style='color: rgba(139,92,246,0.2);'>|</span>
        <span>🔬 Data Quality: <span style='color: #B923FF; font-weight: 700;'>IQR Checked</span></span>
    </div>
</div>
""", unsafe_allow_html=True)


# ─── VIEW ROUTING ─────────────────────────────────────────────
if "Overview" in page:
    from views.overview import render_overview
    render_overview(bl, ze, bb, gr, rfm, rfm_sum, cohort, pm, total_prod)

elif "Price" in page:
    from views.price_intelligence import render_price_intelligence
    render_price_intelligence(bl, ze, bb, pm)

elif "Review" in page or "Rating" in page:
    from views.review_rating import render_review_rating
    render_review_rating(bl, bb)

elif "Basket" in page or "Market" in page:
    from views.market_basket import render_market_basket
    render_market_basket(ar)

elif "Customer Seg" in page or "Segments" in page:
    from views.customer_segments import render_customer_segments
    render_customer_segments(rfm, rfm_sum)

elif "Cohort" in page:
    from views.cohort_retention import render_cohort_retention
    render_cohort_retention(cohort)

elif "Journey" in page:
    from views.customer_journey import render_customer_journey
    render_customer_journey(sk)

elif "Simulator" in page:
    from views.business_simulator import render_business_simulator
    render_business_simulator(rfm, cohort, pm)

elif "Quality" in page or "Data Quality" in page:
    from views.data_quality import render_data_quality
    render_data_quality(bl, ze, bb)


# ─── FOOTER ───────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style='display:flex; justify-content:space-between; align-items:center;
            padding:16px 28px;
            background: linear-gradient(135deg,
              rgba(13,17,23,0.9) 0%, rgba(10,15,30,0.8) 100%);
            border:1px solid rgba(139,92,246,0.15);
            border-radius:16px; margin-top:20px;
            backdrop-filter: blur(20px);
            flex-wrap: wrap; gap: 12px;'>
    <div style='font-size:11px; color:#475569; font-weight:500;'>
        © 2026 QC Pulse India &nbsp;·&nbsp;
        <a href="https://github.com/Yashaswini-V21/qc-pulse-india"
           target="_blank"
           style="text-decoration:none; color:#8B5CF6; font-weight:700;">
           📂 GitHub
        </a>
    </div>
    <div style='font-size:10px; color:#475569;'>
        Made by <span style='color:#A78BFA; font-weight:600;'>Yashaswini V</span>
        &nbsp;·&nbsp; May 2026
    </div>
</div>
""", unsafe_allow_html=True)
