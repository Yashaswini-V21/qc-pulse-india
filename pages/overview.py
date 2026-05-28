"""
Overview page - Dashboard home with key metrics and findings.

Purpose:
  Provide high-level snapshot of all three platforms with key customer and product metrics.
  
Data Used:
  - blinkit, zepto, bigbasket (product catalogs)
  - rfm, rfm_sum (customer segmentation)
  - groceries (transactions)
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from typing import Tuple


def render(
    blinkit: pd.DataFrame,
    zepto: pd.DataFrame,
    bigbasket: pd.DataFrame,
    groceries: pd.DataFrame,
    rfm: pd.DataFrame,
    rfm_sum: pd.DataFrame,
    price_mat: pd.DataFrame,
    cohort: pd.DataFrame,
    sankey_df: pd.DataFrame,
) -> None:
    """Render overview page."""
    # Hero section
    st.markdown("""
    <style>
        .hero-title {
            font-size: 42px;
            font-weight: 800;
            letter-spacing: -0.02em;
            background: linear-gradient(135deg, #60A5FA 0%, #A78BFA 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 8px;
        }
        .hero-subtitle {
            font-size: 16px;
            color: #94A3B8;
            font-weight: 500;
            letter-spacing: 0.02em;
            margin-bottom: 24px;
        }
    </style>
    <h1 class="hero-title">📊 QC Pulse India</h1>
    <p class="hero-subtitle">Premium Analytics for Quick Commerce Giants · Blinkit · Zepto · BigBasket</p>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Enhanced KPI Row
    st.markdown("<p class='section-label'>Key Metrics Overview</p>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    
    with col1:
        st.metric(
            "📦 Total Products",
            f"{len(blinkit)+len(zepto)+len(bigbasket):,}",
            "Across platforms"
        )
    with col2:
        st.metric(
            "👥 Active Customers",
            f"{rfm['customer_id'].nunique():,}",
            "RFM Analyzed"
        )
    with col3:
        st.metric(
            "🛒 Transactions",
            f"{len(groceries):,}",
            "2 Years Data"
        )
    with col4:
        avg_disc = zepto['discount_pct'].median() if 'discount_pct' in zepto.columns else 0
        st.metric(
            "💰 Zepto Discounts",
            f"{avg_disc:.0f}%",
            "Median"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Charts section
    st.markdown("<p class='section-label'>Catalog Composition Analysis</p>", unsafe_allow_html=True)
    col_left, col_right = st.columns([1.6, 1])
    
    with col_left:
        st.markdown("<p class='section-label'>Top Categories — Blinkit</p>", unsafe_allow_html=True)
        cat_counts = blinkit['category'].value_counts().head(10).reset_index()
        cat_counts.columns = ['category', 'count']
        fig = px.bar(
            cat_counts.sort_values('count'),
            x='count', y='category', orientation='h',
            color='count', color_continuous_scale='Blues',
            labels={'count': 'Products', 'category': ''},
            title=None
        )
        fig.update_layout(
            height=380,
            plot_bgcolor='rgba(30, 41, 59, 0.5)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E2E8F0', size=11),
            showlegend=False,
            coloraxis_showscale=False,
            margin=dict(l=0,r=0,t=10,b=0),
            hovermode='closest'
        )
        fig.update_xaxes(color='#94A3B8', gridcolor='rgba(51, 65, 85, 0.2)')
        fig.update_yaxes(color='#94A3B8')
        st.plotly_chart(fig, width='stretch')
    
    with col_right:
        st.markdown("<p class='section-label'>Market Share</p>", unsafe_allow_html=True)
        platform_counts = pd.DataFrame({
            'Platform': ['BigBasket', 'Blinkit', 'Zepto'],
            'Products': [len(bigbasket), len(blinkit), len(zepto)]
        })
        fig2 = px.pie(
            platform_counts, values='Products', names='Platform',
            color_discrete_map={'BigBasket':'#6C63DB','Blinkit':'#DC2626','Zepto':'#1D9E75'},
            hole=0.55
        )
        fig2.update_layout(
            height=380,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E2E8F0', size=12),
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#E2E8F0')),
            margin=dict(l=0,r=0,t=10,b=0),
            hovermode='closest'
        )
        fig2.update_traces(textfont_color='white', textinfo='percent+label')
        st.plotly_chart(fig2, width='stretch')
    
    # Insights row
    st.markdown("---")
    st.markdown("<p class='section-label'>Key Findings</p>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""<div class='insight-card'>
            <h4>🏆 Champions</h4>
            <p>809 customers (20.8%) are Champions — ordering every 58 days with avg 6.3 orders and 16.9 items per customer.</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class='insight-card'>
            <h4>⚠️ Churn Risk</h4>
            <p>889 customers (22.8%) have churned — last order was 400+ days ago. Immediate win-back campaigns needed.</p>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class='insight-card'>
            <h4>📈 Retention</h4>
            <p>Avg Month-1 retention is 14.3%. Best cohort (Jun 2015) achieved 26.3% — 84% above average.</p>
        </div>""", unsafe_allow_html=True)
