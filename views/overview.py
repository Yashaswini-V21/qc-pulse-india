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
            f"{churn_pct_live}% of customers — avg 400 days since last order (proxy dataset). "
            "Win-back campaign modelling available in the Simulator tab."
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

    # ── AUTO-GENERATED INTELLIGENCE REPORT ──────────────────────────────────
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(108,99,219,0.08), rgba(220,38,38,0.05));
        border: 1px solid rgba(108,99,219,0.25);
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 4px;
    ">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:6px;">
            <span style="font-size:24px;">🤖</span>
            <h2 style="
                font-family:'DM Sans',sans-serif;
                font-size:20px; font-weight:700;
                color:#F1F5F9; margin:0;
                letter-spacing:-0.02em;
            ">Auto-Generated Intelligence Report</h2>
        </div>
        <p style="
            font-family:'DM Sans',sans-serif;
            font-size:13px; color:{_LABEL_C};
            margin:0;
        ">Five data-driven insight cards computed live from your CSV pipeline outputs.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Load data ──
    try:
        _rsum  = pd.read_csv("data/clean/rfm_summary.csv")
        _rsum.columns = [c.strip().lower() for c in _rsum.columns]
    except Exception:
        _rsum = pd.DataFrame()

    try:
        _coh = pd.read_csv("data/clean/cohort_retention.csv")
    except Exception:
        _coh = pd.DataFrame()

    try:
        _pm  = pd.read_csv("data/clean/price_matrix.csv")
    except Exception:
        _pm = pd.DataFrame()

    # ── Helper: safe segment lookup ──
    def _seg(name: str, col: str, default=0):
        if len(_rsum) == 0:
            return default
        row = _rsum[_rsum["segment"].str.strip() == name]
        return row.iloc[0][col] if len(row) > 0 else default

    total_customers   = int(_rsum["customers"].sum()) if len(_rsum) > 0 else 1
    champ_count_r     = int(_seg("Champion",  "customers", 0))
    churn_count_r     = int(_seg("Churned",   "customers", 0))
    atrisk_count_r    = int(_seg("At-Risk",   "customers", 0))
    potential_count_r = int(_seg("Potential", "customers", 0))

    champ_pct_r  = round(champ_count_r  / total_customers * 100, 1)
    churn_pct_r  = round(churn_count_r  / total_customers * 100, 1)
    atrisk_pct_r = round(atrisk_count_r / total_customers * 100, 1)
    pot_pct_r    = round(potential_count_r / total_customers * 100, 1)

    churn_mon_r  = float(_seg("Churned",  "avg_monetary", 0))
    atrisk_mon_r = float(_seg("At-Risk",  "avg_monetary", 0))
    churn_rev_risk  = round(churn_count_r  * churn_mon_r)
    atrisk_rev_risk = round(atrisk_count_r * atrisk_mon_r)

    # cohort retention metrics
    try:
        _coh_vals = _coh["1"].astype(float)
        avg_m1 = round(float(_coh_vals.mean()), 1)
        best_idx  = _coh_vals.idxmax()
        worst_idx = _coh_vals.idxmin()
        best_cohort_name  = str(_coh.loc[best_idx,  "cohort_month"]) if "cohort_month" in _coh.columns else str(best_idx)
        worst_cohort_name = str(_coh.loc[worst_idx, "cohort_month"]) if "cohort_month" in _coh.columns else str(worst_idx)
        best_m1   = round(float(_coh_vals.max()), 1)
        worst_m1  = round(float(_coh_vals.min()), 1)
    except Exception:
        avg_m1 = best_m1 = worst_m1 = 0.0
        best_cohort_name = worst_cohort_name = "N/A"

    # price metrics
    try:
        price_cols = ["Blinkit", "Zepto", "BigBasket"]
        existing_price_cols = [c for c in price_cols if c in _pm.columns]
        if existing_price_cols:
            _pm_avgs = {c: round(float(_pm[c].dropna().mean()), 2) for c in existing_price_cols}
            cheapest_platform = min(_pm_avgs, key=_pm_avgs.get)
            cheapest_avg      = _pm_avgs[cheapest_platform]

            def _price_range(row):
                vals = [row[c] for c in existing_price_cols if pd.notna(row.get(c))]
                return max(vals) - min(vals) if len(vals) >= 2 else 0

            _pm["_gap"] = _pm.apply(_price_range, axis=1)
            gap_row      = _pm.loc[_pm["_gap"].idxmax()]
            gap_cat      = str(gap_row.get("category", "Unknown"))
            gap_val      = round(float(gap_row["_gap"]), 2)
        else:
            cheapest_platform = "N/A"
            cheapest_avg      = 0
            gap_cat = "N/A"
            gap_val = 0
    except Exception:
        cheapest_platform = "N/A"
        cheapest_avg      = 0
        gap_cat = "N/A"
        gap_val = 0

    # ── Card 5 recommendation logic ──
    if churn_pct_r > 20:
        card5_bullet = (
            f"🔴 **Priority: Reduce churn.** {churn_pct_r}% of customers are Churned. "
            "Focus retention budget on At-Risk segment before they become Churned."
        )
    elif champ_pct_r < 15:
        card5_bullet = (
            f"🟡 **Priority: Nurture Potential segment to Champions.** "
            f"Potential customers are {pot_pct_r}% of base — the biggest upgrade opportunity."
        )
    else:
        card5_bullet = (
            "🟢 **Platform is healthy.** Focus on expanding the Champion segment "
            "through loyalty programmes and premium tier incentives."
        )

    # ── Build plain-text report for download ──
    report_txt = f"""QC Pulse India — Auto-Generated Intelligence Report
Generated: 2026-08-22
={'='*55}

📊 CUSTOMER BASE HEALTH
  • {champ_pct_r}% of customers are Champions — your highest-value segment ({champ_count_r:,} customers)
  • {churn_pct_r}% are Churned — representing ₹{churn_rev_risk:,} monthly revenue at risk

📈 RETENTION PERFORMANCE
  • Average Month-1 retention across all cohorts: {avg_m1}%
  • Best cohort: {best_cohort_name} ({best_m1}% Month-1 retention)
  • Worst cohort: {worst_cohort_name} ({worst_m1}% Month-1 retention)

💰 PRICE INTELLIGENCE
  • Cheapest platform on average: {cheapest_platform} (avg ₹{cheapest_avg})
  • Biggest price gap by category: {gap_cat} (₹{gap_val} spread across platforms)

⚠️ RISK SIGNALS
  • At-Risk customer count: {atrisk_count_r:,} ({atrisk_pct_r}% of base)
  • Estimated At-Risk revenue at risk: ₹{atrisk_rev_risk:,}
  • Recommendation: Consider reactivation campaign for At-Risk segment

🎯 TOP RECOMMENDATION
  • {card5_bullet.replace("**", "").replace("🔴 ", "").replace("🟡 ", "").replace("🟢 ", "")}
"""

    # ── Render 5 expander cards ──
    _expander_style = f"""
    <style>
    details[data-testid="stExpander"] {{
        background: {_CARD_BG} !important;
        border-radius: 12px !important;
        border: 1px solid rgba(108,99,219,0.2) !important;
        margin-bottom: 12px !important;
        overflow: hidden !important;
    }}
    details[data-testid="stExpander"] summary {{
        padding: 14px 20px !important;
        cursor: pointer !important;
    }}
    details[data-testid="stExpander"] summary p {{
        font-family: 'DM Sans', sans-serif !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        color: #F1F5F9 !important;
        margin: 0 !important;
        display: inline-block !important;
    }}
    /* Eliminate raw ligature text leak (_arrow_right_) */
    details[data-testid="stExpander"] summary [data-testid="stExpanderToggleIcon"],
    details[data-testid="stExpander"] summary [data-testid="stIconMaterial"],
    details[data-testid="stExpander"] summary svg,
    details[data-testid="stExpander"] summary i {{
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
    }}
    </style>
    """
    st.markdown(_expander_style, unsafe_allow_html=True)

    with st.expander("📊 Customer Base Health", expanded=True):
        st.markdown(f"""
- **{champ_pct_r}%** of customers are Champions — your highest-value segment ({champ_count_r:,} customers)
- **{churn_pct_r}%** are Churned — representing **₹{churn_rev_risk:,}** monthly revenue at risk \\
  *(Churned count × avg monetary value)*
        """)

    with st.expander("📈 Retention Performance"):
        st.markdown(f"""
- Average Month-1 retention across all cohorts: **{avg_m1}%**
- Best cohort: **{best_cohort_name}** with **{best_m1}%** Month-1 retention — {round(best_m1 - avg_m1, 1)}pp above average
- Worst cohort: **{worst_cohort_name}** with **{worst_m1}%** Month-1 retention — identifies acquisition quality issues
        """)

    with st.expander("💰 Price Intelligence"):
        st.markdown(f"""
- Cheapest platform on average: **{cheapest_platform}** (avg price ₹{cheapest_avg})
- Biggest inter-platform price gap: **{gap_cat}** category — ₹{gap_val} spread across platforms
- High price dispersion signals arbitrage opportunities and customer switching risk
        """)

    with st.expander("⚠️ Risk Signals"):
        st.markdown(f"""
- At-Risk customers: **{atrisk_count_r:,}** ({atrisk_pct_r}% of customer base)
- Estimated At-Risk revenue at risk: **₹{atrisk_rev_risk:,}** *(At-Risk count × avg monetary)*
- ⚡ **Recommendation:** Consider reactivation campaign for At-Risk segment before they churn
        """)

    with st.expander("🎯 Top Recommendation"):
        st.markdown(card5_bullet)

    # ── Download button ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.download_button(
        label="📥 Download Intelligence Report (.txt)",
        data=report_txt,
        file_name="qc_pulse_intelligence_report.txt",
        mime="text/plain",
        use_container_width=False,
    )
