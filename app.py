"""
QC Pulse India - Quick Commerce Analytics Platform
Main app file that coordinates page navigation and data loading.

Run with: streamlit run app.py
"""
import streamlit as st
import pandas as pd
import warnings
from utils.data_loader import load_data
from utils.styles import load_custom_css
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

warnings.filterwarnings('ignore')

# ─── PAGE CONFIG ────────────────────────────────────────────
st.set_page_config(
    page_title="QC Pulse India",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ─────────────────────────────────────────────
load_custom_css()

# ─── DATA LOADING ────────────────────────────────────────────
try:
    logger.info("Loading data from CSV files...")
    blinkit, zepto, bigbasket, groceries, rfm, rfm_sum, price_mat, cohort, sankey_df = load_data()
    logger.info(f"Successfully loaded {len(rfm)} customers across {len(blinkit)+len(zepto)+len(bigbasket)} products")
except Exception as e:
    st.error(f"❌ Failed to load data: {str(e)}")
    logger.error(f"Data loading error: {str(e)}", exc_info=True)
    st.stop()

# ─── SIDEBAR & NAVIGATION ────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛒 QC Pulse India")
    st.markdown("<p style='color:#64748B;font-size:12px'>Quick Commerce Analytics Platform</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    page = st.radio(
        "📍 Navigate",
        ["📊 Overview",
         "⚔️ Price Intelligence",
         "👥 Customer Segments",
         "📈 Cohort Retention",
         "🌊 Customer Journey"],
        label_visibility="visible"
    )
    
    st.markdown("---")
    st.markdown("<p class='section-label'>Data Summary</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#94A3B8;font-size:12px'>🛒 {len(blinkit)+len(zepto)+len(bigbasket):,} products</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#94A3B8;font-size:12px'>👥 {rfm['customer_id'].nunique():,} customers</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#94A3B8;font-size:12px'>📦 {len(groceries):,} transactions</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#94A3B8;font-size:12px'>🏪 3 platforms analysed</p>", unsafe_allow_html=True)
# ─── IMPORT PAGES ────────────────────────────────────────────
# Dynamic page routing
pages = {
    "📊 Overview": "pages.overview",
    "⚔️ Price Intelligence": "pages.price_intelligence",
    "👥 Customer Segments": "pages.customer_segments",
    "📈 Cohort Retention": "pages.cohort_retention",
    "🌊 Customer Journey": "pages.customer_journey",
}

# ─── PAGE ROUTING ────────────────────────────────────────────
try:
    module_name = pages[page]
    module = __import__(module_name, fromlist=[module_name.split('.')[-1]])
    
    logger.info(f"Loading page: {page}")
    module.render(
        blinkit=blinkit, 
        zepto=zepto, 
        bigbasket=bigbasket,
        groceries=groceries, 
        rfm=rfm, 
        rfm_sum=rfm_sum,
        price_mat=price_mat,
        cohort=cohort,
        sankey_df=sankey_df
    )
except Exception as e:
    st.error(f"❌ Error rendering page: {str(e)}")
    logger.error(f"Page rendering error for '{page}': {str(e)}", exc_info=True)
