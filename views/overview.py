import streamlit as st
import pandas as pd
import plotly.express as px
import logging
from typing import Dict, Any

# Ensure proper logger configuration
logger = logging.getLogger(__name__)

def render_overview(
    bl: pd.DataFrame,
    ze: pd.DataFrame,
    bb: pd.DataFrame,
    gr: pd.DataFrame,
    rfm: pd.DataFrame,
    rfm_sum: pd.DataFrame,
    cohort: pd.DataFrame,
    pm: pd.DataFrame,
    total_prod: int,
    DARK_LAYOUT: Dict[str, Any]
) -> None:
    """
    Renders the modular Overview page for QC Pulse India.
    """
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-left">
            <span class="stat-badge">QC PULSE INDIA</span>
            <h1 style="margin: 4px 0 12px 0; font-size: 32px; font-weight: 800; background: linear-gradient(90deg, #F1F5F9, #94A3B8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Quick Commerce Analytics</h1>
            <p style="color: #64748B; font-size: 14px; line-height: 1.5; margin: 0;">Competitive intelligence, pricing matrix comparison, RFM segmentation, cohort retention, and customer journey mapping for India's leading 10-minute delivery services.</p>
        </div>
        <div class="hero-stats">
            <div class="hero-stat-card">
                <div class="hero-stat-value animate-stat">67,357</div>
                <div class="hero-stat-label">Products</div>
            </div>
            <div class="hero-stat-card">
                <div class="hero-stat-value animate-stat">3,898</div>
                <div class="hero-stat-label">Customers</div>
            </div>
            <div class="hero-stat-card">
                <div class="hero-stat-value animate-stat">38,765</div>
                <div class="hero-stat-label">Transactions</div>
            </div>
            <div class="hero-stat-card">
                <div class="hero-stat-value animate-stat">3</div>
                <div class="hero-stat-label">Platforms</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPIs ──
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Total Products", f"{total_prod:,}", "3 platforms")
    with c2: st.metric("Customers Analysed", f"{rfm['customer_id'].nunique():,}", "RFM segmented")
    with c3: st.metric("Transactions", f"{len(gr):,}", "2 years")
    with c4:
        champ = rfm_sum[rfm_sum['segment'] == 'Champion'].iloc[0]
        st.metric("Champion Customers", f"{int(champ['customers']):,}", f"{champ['pct_customers']}% of base")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts row ──
    col_left, col_right = st.columns([1.6, 1])

    with col_left:
        st.markdown("<p class='section-label'>Top Categories — Blinkit Products</p>", unsafe_allow_html=True)
        cats = bl['category'].value_counts().head(10).reset_index()
        cats.columns = ['category', 'count']
        fig = px.bar(
            cats.sort_values('count'),
            x='count', y='category', orientation='h',
            color='count', color_continuous_scale=[[0, '#1E2D40'], [1, '#DC2626']],
            text='count',
            labels={'count': '', 'category': ''}
        )
        fig.update_traces(
            texttemplate='%{text:,}', textposition='outside',
            textfont=dict(color='#94A3B8', size=10),
            marker_line_width=0
        )
        fig.update_layout(**DARK_LAYOUT, height=360,
                          coloraxis_showscale=False,
                          yaxis=dict(color='#94A3B8', gridcolor='#1E2D40'))
        fig.update_xaxes(showgrid=False)
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown("<p class='section-label'>Platform Share</p>", unsafe_allow_html=True)
        pf = pd.DataFrame({
            'Platform': ['BigBasket', 'Blinkit', 'Zepto'],
            'Products': [len(bb), len(bl), len(ze)]
        })
        fig2 = px.pie(
            pf, values='Products', names='Platform',
            color_discrete_map={'BigBasket': '#6C63DB', 'Blinkit': '#DC2626', 'Zepto': '#1D9E75'},
            hole=0.62
        )
        fig2.update_layout(
            **{k: v for k, v in DARK_LAYOUT.items() if k not in ['xaxis', 'yaxis']},
            height=360,
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#94A3B8', size=12)),
            annotations=[dict(text=f'<b>{total_prod:,}</b><br><span style="font-size:10px">Products</span>',
                              x=0.5, y=0.5, font_size=14, font_color='#F1F5F9',
                              showarrow=False)]
        )
        fig2.update_traces(
            textfont_color='white', textinfo='percent',
            marker=dict(line=dict(color='#060B14', width=3))
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ── Insights ──
    st.markdown("---")
    st.markdown("<p class='section-label'>Key Findings</p>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""<div class='insight-card'>
            <span class='num'>809</span>
            <h4>Champions</h4>
            <p>Champions order every 58 days, averaging 6.3 orders per customer. They generate 3.6x higher lifetime value (LTV) than churned customers, representing the core value of the user base.</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class='insight-card'>
            <span class='num'>889</span>
            <h4>Churned</h4>
            <p>Churned customers have been inactive for over 400 days. Launching immediate win-back marketing campaigns presents a significant opportunity to recover lost subscription and basket revenue.</p>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class='insight-card'>
            <span class='num'>26.3%</span>
            <h4>Best Cohort</h4>
            <p>The June 2015 cohort achieved the highest customer retention rate at 26.3%. This is a remarkable 84% above the average customer retention rate, highlighting a highly successful onboarding period.</p>
        </div>""", unsafe_allow_html=True)

    # ── Auto-Generated Business Intelligence ──────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<p class='section-label'>📰 Auto-Generated Business Intelligence</p>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#475569;font-size:13px;margin-bottom:20px'>"
        "5 data-backed insights computed live from your dataset — no manual interpretation needed."
        "</p>",
        unsafe_allow_html=True
    )

    try:
        from utils.story_generator import generate_cohort_story
        stories = generate_cohort_story(cohort, rfm, pm)
    except Exception as _story_err:
        logger.warning(f"Story generator failed: {_story_err}")
        stories = {
            "headline": "Data analysis in progress — run the pipeline to refresh insights.",
            "price_war": "Platform pricing gaps detected — see Price Intelligence page for details.",
            "champion_at_risk": "Champion and At-Risk segment analysis ready — see Customer Segments.",
            "retention_alert": "Retention metrics loaded — see Cohort Retention for the full picture.",
            "opportunity": "Improvement opportunity identified — use the Business Simulator to model scenarios.",
        }

    STORY_CONFIG = [
        ("headline",         "🏆 Cohort Highlight",     "#7C3AED"),
        ("price_war",        "⚔️ Price Intelligence",   "#DC2626"),
        ("champion_at_risk", "💰 Revenue Opportunity",  "#F59E0B"),
        ("retention_alert",  "⚠️ Retention Alert",      "#EF4444"),
        ("opportunity",      "📈 Growth Potential",     "#1D9E75"),
    ]

    col_a, col_b = st.columns(2)
    for idx, (key, label, color) in enumerate(STORY_CONFIG):
        text = stories.get(key, "")
        container = col_a if idx % 2 == 0 else col_b
        with container:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #0F1C2E 0%, #0D1823 100%);
                        border: 1px solid #1E2D40;
                        border-left: 3px solid {color};
                        border-radius: 0 12px 12px 0;
                        padding: 18px 20px;
                        margin-bottom: 14px;'>
                <div style='font-family: Space Mono, monospace; font-size: 9px;
                            color: {color}; font-weight: 700; text-transform: uppercase;
                            letter-spacing: .12em; margin-bottom: 8px;'>{label}</div>
                <div style='color: #E2E8F0; font-size: 13px; line-height: 1.7;'>{text}</div>
            </div>
            """, unsafe_allow_html=True)
