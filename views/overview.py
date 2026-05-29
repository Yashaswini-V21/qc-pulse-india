"""Overview page — Premium "Dark Intelligence" design."""
import streamlit as st
import pandas as pd
import plotly.express as px
import logging

from utils.charts import (
    apply_premium_theme, apply_premium_theme_no_axes,
    BAR_COLOR, PLATFORM_PIE_COLORS
)

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
) -> None:
    """Renders the Overview page with premium hero header."""

    # ── HERO SECTION ──
    st.markdown("""
    <div style="padding: 32px 0 24px; animation: fadeIn 0.8s ease;">

      <div style="display:flex; align-items:center;
                  gap:12px; margin-bottom:16px;">
        <div style="
          width:40px; height:40px;
          background: linear-gradient(135deg, #8B5CF6, #3B82F6);
          border-radius:10px;
          display:flex; align-items:center;
          justify-content:center;
          font-size:20px;
          box-shadow: 0 8px 24px rgba(139,92,246,0.3);
        ">🛒</div>
        <div>
          <div style="
            font-size:11px; font-weight:700;
            text-transform:uppercase; letter-spacing:0.15em;
            color:#475569;
          ">India Quick Commerce Intelligence</div>
          <div class="live-badge" style="margin-top:4px;">
            <span class="status-dot status-live"></span>
            Live Dashboard
          </div>
        </div>
      </div>

      <h1 style="
        font-size:48px !important;
        font-weight:900 !important;
        letter-spacing:-0.04em !important;
        line-height:1.05 !important;
        margin:0 0 12px !important;
        background: linear-gradient(135deg,
          #F8FAFC 0%, #C4B5FD 40%, #93C5FD 80%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
      ">QC Pulse India</h1>

      <p style="
        font-size:16px; color:#64748B;
        font-weight:400; margin:0 0 28px;
        max-width:600px; line-height:1.6;
      ">Competitive intelligence across Blinkit, Zepto & BigBasket —
         RFM segmentation, cohort retention, price intelligence,
         and business decision simulation.</p>

      <div style="display:flex; gap:8px; flex-wrap:wrap;">
        <span class="platform-badge badge-blinkit">⚡ Blinkit</span>
        <span class="platform-badge badge-zepto">🟢 Zepto</span>
        <span class="platform-badge badge-bigbasket">🛍️ BigBasket</span>
        <span style="
          display:inline-flex; align-items:center; gap:6px;
          padding:4px 12px; border-radius:99px;
          font-size:12px; font-weight:600;
          background:rgba(6,182,212,0.1);
          border:1px solid rgba(6,182,212,0.3);
          color:#67E8F9;
        ">📊 3,898 Customers Analysed</span>
        <span style="
          display:inline-flex; align-items:center; gap:6px;
          padding:4px 12px; border-radius:99px;
          font-size:12px; font-weight:600;
          background:rgba(16,185,129,0.1);
          border:1px solid rgba(16,185,129,0.3);
          color:#6EE7B7;
        ">🔮 Business Simulator</span>
      </div>

    </div>
    """, unsafe_allow_html=True)

    # ── KPIs ──
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Products", f"{total_prod:,}", "3 platforms")
    with c2:
        st.metric("Customers Analysed", f"{rfm['customer_id'].nunique():,}", "RFM segmented")
    with c3:
        st.metric("Transactions", f"{len(gr):,}", "2 years")
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
            color_discrete_sequence=[BAR_COLOR],
            text='count',
            labels={'count': '', 'category': ''}
        )
        fig.update_traces(
            texttemplate='%{text:,}', textposition='outside',
            textfont=dict(color='#94A3B8', size=10),
            marker_line_width=0
        )
        apply_premium_theme(fig, height=360)
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
            color='Platform',
            color_discrete_map=PLATFORM_PIE_COLORS,
            hole=0.62
        )
        apply_premium_theme_no_axes(fig2, height=360)
        fig2.update_layout(
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#94A3B8', size=12)),
            annotations=[dict(
                text=f'<b>{total_prod:,}</b><br><span style="font-size:10px">Products</span>',
                x=0.5, y=0.5, font_size=14, font_color='#F8FAFC',
                showarrow=False
            )]
        )
        fig2.update_traces(
            textfont_color='white', textinfo='percent',
            marker=dict(line=dict(color='#050810', width=3))
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

    # ── Auto-Generated Business Intelligence ──
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
        ("headline",         "🏆 Cohort Highlight",     "#8B5CF6"),
        ("price_war",        "⚔️ Price Intelligence",   "#EF4444"),
        ("champion_at_risk", "💰 Revenue Opportunity",  "#F59E0B"),
        ("retention_alert",  "⚠️ Retention Alert",      "#EF4444"),
        ("opportunity",      "📈 Growth Potential",     "#10B981"),
    ]

    col_a, col_b = st.columns(2)
    for idx, (key, label, color) in enumerate(STORY_CONFIG):
        text = stories.get(key, "")
        container = col_a if idx % 2 == 0 else col_b
        with container:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg,
                          rgba(13,17,23,0.9) 0%, rgba(8,12,24,0.8) 100%);
                        border: 1px solid rgba(139,92,246,0.1);
                        border-left: 3px solid {color};
                        border-radius: 0 16px 16px 0;
                        padding: 18px 24px;
                        margin-bottom: 14px;
                        transition: all 0.3s ease;
                        animation: slideUp 0.6s ease forwards;
                        animation-delay: {idx * 0.1}s;'>
                <div style='font-size: 10px;
                            color: {color}; font-weight: 700; text-transform: uppercase;
                            letter-spacing: .12em; margin-bottom: 8px;'>{label}</div>
                <div style='color: #CBD5E1; font-size: 13px; line-height: 1.7;'>{text}</div>
            </div>
            """, unsafe_allow_html=True)
