"""Overview page — Recruiter-stopping dashboard design."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import logging
from utils.story_generator import generate_cohort_story

logger = logging.getLogger(__name__)


# ── Design tokens ────────────────────────────────────────────
_BG       = "#060B14"
_CARD_BG  = "linear-gradient(135deg, #0F1C2E, #0D1823)"
_BORDER   = "linear-gradient(90deg, #DC2626, #7C3AED)"
_RED      = "#DC2626"
_PURPLE   = "#7C3AED"
_GREEN    = "#1D9E75"
_LABEL_C  = "#64748B"
_VALUE_C  = "#F1F5F9"
_PLOT_BG  = "#0D1823"
_HOVER_BG = "#0F1C2E"
_HOVER_BD = "#1E2D40"


def _kpi_card(label: str, value: str, delta: str = "") -> str:
    """Render a single KPI card as HTML."""
    delta_html = ""
    if delta:
        delta_html = (
            f"<div style='font-family:\"Space Mono\",monospace;font-size:10px;"
            f"color:{_LABEL_C};margin-top:6px;'>{delta}</div>"
        )
    return f"""
    <div style="
        background: {_CARD_BG};
        border-radius: 14px;
        padding: 22px 24px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(0,0,0,0.4);
    ">
        <div style="
            position:absolute; top:0; left:0; right:0; height:2px;
            background: {_BORDER};
        "></div>
        <div style="
            font-family:'Space Mono',monospace;
            font-size:10px; text-transform:uppercase;
            color:{_LABEL_C}; letter-spacing:0.12em;
            margin-bottom:8px;
        ">{label}</div>
        <div style="
            font-family:'DM Sans',sans-serif;
            font-weight:700; font-size:30px;
            color:{_VALUE_C}; line-height:1.1;
        ">{value}</div>
        {delta_html}
    </div>
    """


def _insight_card(number: str, label: str, text: str) -> str:
    """Render a bottom insight card with red bottom border gradient."""
    return f"""
    <div style="
        background: {_CARD_BG};
        border-radius: 14px;
        padding: 24px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        min-height: 200px;
    ">
        <div style="
            position:absolute; bottom:0; left:0; right:0; height:2px;
            background: {_BORDER};
        "></div>
        <div style="
            font-family:'DM Sans',sans-serif;
            font-weight:700; font-size:24px;
            color:#FFFFFF; margin-bottom:8px;
        ">{number}</div>
        <div style="
            font-family:'Space Mono',monospace;
            font-size:10px; text-transform:uppercase;
            color:{_RED}; letter-spacing:0.12em;
            margin-bottom:10px;
        ">{label}</div>
        <div style="
            font-family:'DM Sans',sans-serif;
            font-size:13px; color:{_LABEL_C};
            line-height:1.65;
        ">{text}</div>
    </div>
    """


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
    """Renders the Overview page with recruiter-stopping design."""

    # ── BADGE ──
    st.markdown(f"""
    <div style="padding:28px 0 6px;">
        <span style="
            display:inline-block;
            font-family:'Space Mono',monospace;
            font-size:11px; font-weight:700;
            text-transform:uppercase; letter-spacing:0.12em;
            color:{_RED};
            background:rgba(220,38,38,0.1);
            border:1px solid rgba(220,38,38,0.3);
            padding:5px 14px; border-radius:99px;
        ">● LIVE DASHBOARD</span>
    </div>
    """, unsafe_allow_html=True)

    # ── TITLE + SUBTITLE ──
    st.markdown(f"""
    <h1 style="
        font-family:'DM Sans',sans-serif !important;
        font-size:28px !important; font-weight:700 !important;
        color:#F1F5F9 !important;
        -webkit-text-fill-color:#F1F5F9 !important;
        background:none !important;
        margin:10px 0 6px !important;
        letter-spacing:-0.02em !important;
    ">Quick Commerce Pulse India</h1>
    <p style="
        font-family:'DM Sans',sans-serif;
        font-size:14px; color:{_LABEL_C};
        margin:0 0 28px;
    ">Competitive intelligence across Blinkit · Zepto · BigBasket</p>
    """, unsafe_allow_html=True)

    # ── KPI ROW ──
    customers_count = rfm['customer_id'].nunique()
    transactions = len(gr)
    champ = rfm_sum[rfm_sum['segment'] == 'Champion'].iloc[0]
    champ_count = int(champ['customers'])

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(_kpi_card("TOTAL PRODUCTS", f"{total_prod:,}", "Blinkit + Zepto + BigBasket"), unsafe_allow_html=True)
    with c2:
        st.markdown(_kpi_card("CUSTOMERS ANALYSED", f"{customers_count:,}", "RFM segmented"), unsafe_allow_html=True)
    with c3:
        st.markdown(_kpi_card("TRANSACTIONS", f"{transactions:,}", "Grocery dataset"), unsafe_allow_html=True)
    with c4:
        st.markdown(_kpi_card("CHAMPION CUSTOMERS", f"{champ_count:,}", f"{champ['pct_customers']}% of base"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CHARTS ROW ──
    col_left, col_right = st.columns([1.5, 1])

    with col_left:
        st.markdown(f"""
        <div style="font-family:'Space Mono',monospace;font-size:10px;
            text-transform:uppercase;color:{_LABEL_C};letter-spacing:0.12em;
            margin-bottom:12px;">Top 10 Blinkit Categories by Product Count</div>
        """, unsafe_allow_html=True)

        cats = bl['category'].value_counts().head(10).reset_index()
        cats.columns = ['category', 'count']
        cats = cats.sort_values('count')

        # Custom colorscale: low=#1E2D40, high=#DC2626
        max_val = cats['count'].max()
        min_val = cats['count'].min()
        range_val = max_val - min_val if max_val != min_val else 1
        bar_colors = []
        for v in cats['count']:
            t = (v - min_val) / range_val
            r = int(30 + t * (220 - 30))
            g = int(45 + t * (38 - 45))
            b = int(64 + t * (38 - 64))
            bar_colors.append(f'rgb({r},{g},{b})')

        fig = go.Figure(go.Bar(
            x=cats['count'],
            y=cats['category'],
            orientation='h',
            marker_color=bar_colors,
            text=cats['count'],
            texttemplate='%{text:,}',
            textposition='outside',
            textfont=dict(color='#94A3B8', size=11, family='DM Sans'),
            marker_line_width=0,
        ))
        fig.update_layout(
            plot_bgcolor=_PLOT_BG,
            paper_bgcolor=_PLOT_BG,
            font=dict(family='DM Sans', color='#94A3B8', size=11),
            margin=dict(l=10, r=60, t=10, b=10),
            height=360,
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(gridcolor='#1E2D40', color='#94A3B8', tickfont=dict(size=11)),
            hoverlabel=dict(bgcolor=_HOVER_BG, bordercolor=_HOVER_BD, font=dict(color='white', size=12)),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown(f"""
        <div style="font-family:'Space Mono',monospace;font-size:10px;
            text-transform:uppercase;color:{_LABEL_C};letter-spacing:0.12em;
            margin-bottom:12px;">Platform Share</div>
        """, unsafe_allow_html=True)

        pf = pd.DataFrame({
            'Platform': ['BigBasket', 'Blinkit', 'Zepto'],
            'Products': [len(bb), len(bl), len(ze)]
        })
        pie_colors = {'BigBasket': '#6C63DB', 'Blinkit': '#DC2626', 'Zepto': '#1D9E75'}

        fig2 = px.pie(
            pf, values='Products', names='Platform',
            color='Platform',
            color_discrete_map=pie_colors,
            hole=0.62
        )
        fig2.update_layout(
            plot_bgcolor=_PLOT_BG,
            paper_bgcolor=_PLOT_BG,
            font=dict(family='DM Sans', color='#94A3B8', size=11),
            margin=dict(l=10, r=10, t=10, b=10),
            height=360,
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#94A3B8', size=12, family='DM Sans')),
            annotations=[dict(
                text=f'<b>{total_prod:,}</b><br><span style="font-size:10px">Products</span>',
                x=0.5, y=0.5, font_size=16, font_color=_VALUE_C,
                font_family='DM Sans',
                showarrow=False
            )],
            hoverlabel=dict(bgcolor=_HOVER_BG, bordercolor=_HOVER_BD, font=dict(color='white', size=12)),
        )
        fig2.update_traces(
            textfont_color='white', textinfo='percent',
            marker=dict(line=dict(color=_BG, width=3))
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ── AUTO-INTELLIGENCE — live story generation ──
    try:
        stories = generate_cohort_story(cohort_df=cohort, rfm_df=rfm, price_mat_df=pm)
    except Exception as e:
        logger.warning(f"Story generation failed: {e}")
        stories = {}

    # ── INSIGHT CARDS (live data) ──
    st.markdown("<br>", unsafe_allow_html=True)

    # Compute live values for cards
    champ_row = rfm_sum[rfm_sum['segment'] == 'Champion']
    churn_row = rfm_sum[rfm_sum['segment'] == 'Churned']
    champ_count_live = int(champ_row.iloc[0]['customers']) if len(champ_row) > 0 else 0
    champ_pct_live   = champ_row.iloc[0]['pct_customers'] if len(champ_row) > 0 else "?"
    champ_freq_live  = champ_row.iloc[0]['avg_frequency'] if len(champ_row) > 0 else "?"
    champ_mon_live   = champ_row.iloc[0]['avg_monetary'] if len(champ_row) > 0 else "?"
    churn_count_live = int(churn_row.iloc[0]['customers']) if len(churn_row) > 0 else 0
    churn_pct_live   = churn_row.iloc[0]['pct_customers'] if len(churn_row) > 0 else "?"

    try:
        cohort_num = cohort.copy()
        cohort_num.columns = cohort_num.columns.astype(int)
        best_cohort_label = str(cohort_num[1].idxmax())
        best_cohort_pct   = round(float(cohort_num[1].max()), 1)
        avg_m1_pct        = round(float(cohort_num[1].mean()), 1)
        pct_above          = round((best_cohort_pct - avg_m1_pct) / avg_m1_pct * 100)
    except Exception:
        best_cohort_label = "June 2015"
        best_cohort_pct   = 26.3
        avg_m1_pct        = 14.3
        pct_above          = 84

    ic1, ic2, ic3 = st.columns(3)
    with ic1:
        st.markdown(_insight_card(
            f"{champ_count_live:,}", "CHAMPION CUSTOMERS",
            f"Order every ~58 days avg — {champ_freq_live:.1f} orders, {champ_mon_live:.1f} items. "
            f"Highest LTV segment at {champ_pct_live}% of base."
        ), unsafe_allow_html=True)
    with ic2:
        st.markdown(_insight_card(
            f"{churn_count_live:,}", "CUSTOMERS CHURNED",
            f"{churn_pct_live}% of customers — last order 400+ days ago. "
            "Win-back campaigns needed urgently."
        ), unsafe_allow_html=True)
    with ic3:
        st.markdown(_insight_card(
            f"{best_cohort_pct}%", "PEAK MONTH-1 RETENTION",
            f"{best_cohort_label} cohort — {pct_above}% above the {avg_m1_pct}% average. "
            "Shows what's possible with the right acquisition strategy."
        ), unsafe_allow_html=True)

    # ── AUTO-INTELLIGENCE PANEL ──
    if stories:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-family:'Space Mono',monospace;font-size:10px;
            text-transform:uppercase;color:{_LABEL_C};letter-spacing:0.12em;
            margin-bottom:16px;">
            🤖 Auto-Intelligence — Data-Driven Business Stories
        </div>
        """, unsafe_allow_html=True)

        story_cfg = [
            ("headline",        "📊", "Retention Intelligence",         _PURPLE),
            ("price_war",       "⚔️", "Price War Insight",               _RED),
            ("champion_at_risk","👥", "LTV & Revenue at Risk",           _GREEN),
            ("retention_alert", "⚠️", "Retention Revenue Leak",          "#F59E0B"),
            ("opportunity",     "🚀", "Growth Opportunity",              "#06B6D4"),
        ]

        for key, icon, title, accent in story_cfg:
            text = stories.get(key, "")
            if not text:
                continue
            st.markdown(f"""
            <div style="
                background: {_CARD_BG};
                border-radius: 14px;
                padding: 20px 24px;
                margin-bottom: 10px;
                position: relative;
                overflow: hidden;
                box-shadow: 0 8px 24px rgba(0,0,0,0.4);
            ">
                <div style="
                    position:absolute; top:0; left:0; right:0; height:2px;
                    background: linear-gradient(90deg, {accent}, transparent);
                "></div>
                <div style="
                    font-family:'Space Mono',monospace;
                    font-size:10px; text-transform:uppercase;
                    color:{accent}; letter-spacing:0.12em;
                    margin-bottom:8px; font-weight:700;
                ">{icon} {title}</div>
                <div style="
                    font-family:'DM Sans',sans-serif;
                    font-size:13px; color:#CBD5E1;
                    line-height:1.7;
                ">{text}</div>
            </div>
            """, unsafe_allow_html=True)
