"""Business Decision Simulator page — Premium dark dashboard design."""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from utils.simulator import (
    simulate_winback_campaign,
    simulate_price_change,
    simulate_retention_improvement,
)


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


def _kpi_card(label: str, value: str, subtext: str = "", border: str = _BORDER, value_color: str = _VALUE_C) -> str:
    """Render a single simulator KPI card as HTML."""
    subtext_html = ""
    if subtext:
        subtext_html = (
            f"<div style='font-family:\"Space Mono\",monospace;font-size:10px;"
            f"color:{_LABEL_C};margin-top:6px;'>{subtext}</div>"
        )
    return f"""
    <div style="
        background: {_CARD_BG};
        border-radius: 14px;
        padding: 20px 22px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(0,0,0,0.4);
    ">
        <div style="
            position:absolute; top:0; left:0; right:0; height:2px;
            background: {border};
        "></div>
        <div style="
            font-family:'Space Mono',monospace;
            font-size:10px; text-transform:uppercase;
            color:{_LABEL_C}; letter-spacing:0.12em;
            margin-bottom:8px;
        ">{label}</div>
        <div style="
            font-family:'DM Sans',sans-serif;
            font-weight:700; font-size:28px;
            color:{value_color}; line-height:1.1;
        ">{value}</div>
        {subtext_html}
    </div>
    """


def _recommendation_card(title: str, text: str, border: str = _BORDER, accent: str = _PURPLE) -> str:
    """Render a premium bottom recommendation/insight card."""
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
            background: {border};
        "></div>
        <div style="
            font-family:'Space Mono',monospace;
            font-size:10px; text-transform:uppercase;
            color:{accent}; letter-spacing:0.12em;
            margin-bottom:10px;
            font-weight:700;
        ">{title}</div>
        <div style="
            font-family:'DM Sans',sans-serif;
            font-size:13px; color:#CBD5E1;
            line-height:1.7;
        ">{text}</div>
    </div>
    """


def _apply_custom_theme(fig, height=220, title=""):
    """Applies premium dark mode styles to a Plotly figure."""
    fig.update_layout(
        plot_bgcolor=_PLOT_BG,
        paper_bgcolor=_PLOT_BG,
        font=dict(family='DM Sans', color='#94A3B8', size=11),
        margin=dict(l=10, r=10, t=44 if title else 10, b=10),
        height=height,
        xaxis=dict(color='#94A3B8', gridcolor='#1E2D40', linecolor='#1E2D40'),
        yaxis=dict(color='#94A3B8', gridcolor='#1E2D40', linecolor='#1E2D40'),
        hoverlabel=dict(bgcolor=_HOVER_BG, bordercolor=_HOVER_BD, font=dict(color='white', size=12)),
    )
    if title:
        fig.update_layout(title=dict(text=title, font=dict(color='#94A3B8', size=12)))


def render_business_simulator(
    rfm: pd.DataFrame,
    cohort: pd.DataFrame,
    pm: pd.DataFrame,
) -> None:
    """Renders Business Simulator page with premium recruiter-stopping design."""

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
        ">● DECISION ENGINE</span>
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
    ">Business Decision Simulator</h1>
    <p style="
        font-family:'DM Sans',sans-serif;
        font-size:14px; color:{_LABEL_C};
        margin:0 0 28px;
    ">Model real business decisions — what-if scenarios backed by your actual data</p>
    """, unsafe_allow_html=True)

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs([
        "📧  Win-Back Campaign",
        "💲  Price Change Impact",
        "📈  Retention Improvement",
    ])

    # ── TAB 1: WIN-BACK CAMPAIGN ──
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p class='section-label'>Win-Back Campaign Simulator</p>", unsafe_allow_html=True)
        st.markdown(
            f"<p style='color:{_LABEL_C};font-family:\"DM Sans\",sans-serif;font-size:13px;margin-bottom:20px'>"
            "Model the ROI of an email/SMS re-engagement campaign targeting inactive segments. "
            "Recovery rate is derived from your actual cohort Month-1 retention data.</p>",
            unsafe_allow_html=True
        )

        col_ctrl, col_res = st.columns([1, 1.6])

        with col_ctrl:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            wb_segment = st.selectbox("Target Segment", ["Churned", "At-Risk"], key="wb_seg")
            seg_size = len(rfm[rfm['segment'] == wb_segment])
            st.markdown(
                f"<p style='color:{_LABEL_C};font-family:\"Space Mono\",monospace;font-size:10px;"
                f"margin-top:-8px;margin-bottom:12px;text-transform:uppercase;'>"
                f"Segment size: {seg_size:,} customers</p>",
                unsafe_allow_html=True
            )
            wb_customers = st.slider("Customers to Contact", 50, max(50, seg_size), min(300, seg_size), key="wb_cust")
            wb_budget = st.number_input("Campaign Budget (₹)", min_value=1000, max_value=500000, value=50000, step=5000, key="wb_budget")
            wb_discount = st.slider("Discount Offered (%)", 0, 50, 15, key="wb_disc",
                                    help="Discount coupon included in win-back email/SMS")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_res:
            wb_res = simulate_winback_campaign(
                rfm_df=rfm, cohort_df=cohort,
                segment_targeted=wb_segment, customers_targeted=wb_customers,
                campaign_budget_inr=wb_budget, discount_offered_pct=wb_discount,
            )
            r_color = _GREEN if wb_res['roi_pct'] > 0 else _RED

            col_grid1, col_grid2 = st.columns(2)
            with col_grid1:
                st.markdown(_kpi_card(
                    "Customers Recovered",
                    f"{wb_res['customers_recovered']:,}",
                    f"{wb_res['recovery_rate_pct']}% rate (+{wb_res['discount_boost_pp']}pp discount)"
                ), unsafe_allow_html=True)
            with col_grid2:
                st.markdown(_kpi_card(
                    "Revenue Gained (3m)",
                    f"₹{wb_res['revenue_gained']:,.0f}",
                    "2 orders/month @ ₹350 basket estimate"
                ), unsafe_allow_html=True)

            st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)

            col_grid3, col_grid4 = st.columns(2)
            with col_grid3:
                st.markdown(_kpi_card(
                    "Campaign ROI",
                    f"{wb_res['roi_pct']:+.1f}%",
                    f"vs ₹{wb_budget:,} budget spent",
                    value_color=r_color
                ), unsafe_allow_html=True)
            with col_grid4:
                st.markdown(_kpi_card(
                    "Cost Per Recovery",
                    f"₹{wb_res['cost_per_recovered']:,.0f}",
                    "per recovered customer"
                ), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            payback = wb_res['payback_months']
            payback_txt = f"{payback:.1f} months" if payback < 90 else "Not profitable at this budget"

            rec_text = f"""
            Targeting <b>{wb_customers:,} {wb_segment}</b> customers with a
            <b>₹{wb_budget:,}</b> campaign and <b>{wb_discount}% discount</b> coupon
            yields <b>{wb_res["customers_recovered"]:,} recovered customers</b> and
            <b>₹{wb_res["revenue_gained"]:,.0f}</b> in 3-month revenue.<br>
            Payback period: <b>{payback_txt}</b>.<br>
            Benchmark against <b>{wb_res["recommended_cohort"]}</b> cohort
            ({wb_res["base_retention_rate"]}% baseline retention).
            """
            st.markdown(_recommendation_card("Simulation Recommendation", rec_text, border=_BORDER, accent=_PURPLE), unsafe_allow_html=True)

    # ── TAB 2: PRICE CHANGE IMPACT ──
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p class='section-label'>Price Change Impact Simulator</p>", unsafe_allow_html=True)
        st.markdown(
            f"<p style='color:{_LABEL_C};font-family:\"DM Sans\",sans-serif;font-size:13px;margin-bottom:20px'>"
            "Model how a pricing decision shifts competitive position and impacts revenue. "
            "Uses standard retail price elasticity = -2.0 (20% volume gain per 10% price drop).</p>",
            unsafe_allow_html=True
        )

        col_ctrl2, col_res2 = st.columns([1, 1.6])
        available_cats_pc = pm['category'].dropna().unique().tolist()

        with col_ctrl2:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            pc_platform = st.selectbox("Platform", ['Blinkit', 'Zepto', 'BigBasket'], key="pc_plat")
            pc_category = st.selectbox("Category", available_cats_pc, key="pc_cat")
            pc_discount_change = st.slider(
                "Price Change (%)", -30, 30, 5, key="pc_disc",
                help="Positive = price cut (discount), Negative = price increase"
            )
            pc_customers = st.number_input(
                "Customers Affected", min_value=100, max_value=100000,
                value=5000, step=500, key="pc_cust"
            )
            st.markdown("</div>", unsafe_allow_html=True)

        with col_res2:
            pc_res = simulate_price_change(
                price_matrix_df=pm, platform=pc_platform, category=pc_category,
                discount_change_pct=pc_discount_change, estimated_customers=pc_customers,
            )
            if pc_res.get('error'):
                st.warning(f"Data unavailable: {pc_res['error']}")
            else:
                direction_color = _GREEN if pc_discount_change > 0 else _RED
                rev_color = _GREEN if pc_res['revenue_impact'] > 0 else _RED
                rev_sign = "+" if pc_res['revenue_impact'] >= 0 else ""

                col_grid1, col_grid2, col_grid3 = st.columns(3)
                with col_grid1:
                    st.markdown(_kpi_card(
                        "Current Price",
                        f"₹{pc_res['current_price']:.2f}",
                        f"Market avg: ₹{pc_res['market_avg']:.2f}"
                    ), unsafe_allow_html=True)
                with col_grid2:
                    st.markdown(_kpi_card(
                        "New Price",
                        f"₹{pc_res['new_price']:.2f}",
                        f"{pc_discount_change:+.0f}% {'cut' if pc_discount_change > 0 else 'increase'}",
                        value_color=direction_color
                    ), unsafe_allow_html=True)
                with col_grid3:
                    st.markdown(_kpi_card(
                        "Revenue Impact",
                        f"{rev_sign}₹{abs(pc_res['revenue_impact']):,.0f}",
                        f"{pc_customers:,} customers",
                        value_color=rev_color
                    ), unsafe_allow_html=True)

                st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)

                col_grid4, col_grid5 = st.columns(2)
                with col_grid4:
                    st.markdown(_kpi_card(
                        "Gap Before",
                        f"{pc_res['gap_before']:+.1f}%",
                        f"vs market avg — {pc_res['position_before']}",
                        value_color=_RED if pc_res["gap_before"] > 0 else _GREEN
                    ), unsafe_allow_html=True)
                with col_grid5:
                    st.markdown(_kpi_card(
                        f"Gap After {pc_res['position_arrow']}",
                        f"{pc_res['gap_after']:+.1f}%",
                        f"vs market avg — {pc_res['position_after']}",
                        value_color=_RED if pc_res["gap_after"] > 0 else _GREEN
                    ), unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                fig_gap = go.Figure()
                fig_gap.add_trace(go.Bar(
                    x=['Before', 'After'],
                    y=[pc_res['gap_before'], pc_res['gap_after']],
                    marker_color=[_RED if pc_res['gap_before'] > 0 else _GREEN,
                                  _RED if pc_res['gap_after'] > 0 else _GREEN],
                    text=[f"{pc_res['gap_before']:+.1f}%", f"{pc_res['gap_after']:+.1f}%"],
                    textposition='outside',
                    textfont=dict(color='#94A3B8', size=13, family='DM Sans'),
                    marker_line_width=0,
                ))
                fig_gap.add_hline(y=0, line_color='#475569', line_dash='dash', line_width=1)
                _apply_custom_theme(fig_gap, height=220, title='Price Gap vs Market Average (%)')
                fig_gap.update_layout(
                    yaxis=dict(ticksuffix='%'),
                    margin=dict(l=10, r=10, t=44, b=10),
                )
                st.plotly_chart(fig_gap, use_container_width=True)

                # ── PRICE ELASTICITY OPTIMIZATION CURVE ──
                st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
                st.markdown(f"""
                <div style="font-family:'Space Mono',monospace;font-size:10px;
                    text-transform:uppercase;color:{_LABEL_C};letter-spacing:0.12em;
                    margin-bottom:12px;">📈 Dynamic Price Elasticity Curve (Revenue Optimization)</div>
                """, unsafe_allow_html=True)

                # Generate data points from -30% to +30% price change
                price_changes = list(range(-30, 31, 2))
                base_rev = pc_res['current_price'] * pc_customers

                rev_curves = []
                for dp in price_changes:
                    f_p = 1 - dp / 100.0
                    f_q = 1 + 2.0 * dp / 100.0
                    r_val = base_rev * f_p * f_q
                    rev_curves.append(r_val)

                fig_curve = go.Figure()

                # Plot dynamic revenue path
                fig_curve.add_trace(go.Scatter(
                    x=price_changes, y=rev_curves,
                    mode='lines',
                    line=dict(color='#F97316', width=3),
                    fill='tozeroy',
                    fillcolor='rgba(249,115,22,0.06)',
                    name='Projected Revenue',
                    hoverinfo='x+y',
                ))

                # Plot active slider position
                active_fp = 1 - pc_discount_change / 100.0
                active_fq = 1 + 2.0 * pc_discount_change / 100.0
                active_rev = base_rev * active_fp * active_fq
                fig_curve.add_trace(go.Scatter(
                    x=[pc_discount_change], y=[active_rev],
                    mode='markers',
                    marker=dict(color='#FF3366', size=12, line=dict(color='#060B14', width=2)),
                    name='Current Position',
                    hoverinfo='text',
                    text=f"Selected: {pc_discount_change:+.0f}% (₹{active_rev:,.0f})",
                ))

                # Plot theoretical optimal position at +25%
                optimal_fp = 1 - 25 / 100.0
                optimal_fq = 1 + 2.0 * 25 / 100.0
                optimal_rev = base_rev * optimal_fp * optimal_fq
                fig_curve.add_trace(go.Scatter(
                    x=[25], y=[optimal_rev],
                    mode='markers',
                    marker=dict(color='#00F5A0', size=12, symbol='star', line=dict(color='#060B14', width=2)),
                    name='Optimal Point (25% Discount)',
                    hoverinfo='text',
                    text=f"Optimal: +25% Cut (₹{optimal_rev:,.0f})",
                ))

                _apply_custom_theme(fig_curve, height=240)
                fig_curve.update_layout(
                    xaxis=dict(title='Price Cut / Discount (%)', ticksuffix='%', gridcolor='#1E2D40'),
                    yaxis=dict(title='Projected Revenue (₹)', gridcolor='#1E2D40'),
                    showlegend=True,
                    legend=dict(x=0.02, y=0.98, bgcolor='rgba(0,0,0,0)'),
                    margin=dict(l=10, r=10, t=10, b=10),
                )
                st.plotly_chart(fig_curve, use_container_width=True)


    # ── TAB 3: RETENTION IMPROVEMENT ──
    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p class='section-label'>Retention Improvement Simulator</p>", unsafe_allow_html=True)
        st.markdown(
            f"<p style='color:{_LABEL_C};font-family:\"DM Sans\",sans-serif;font-size:13px;margin-bottom:20px'>"
            "Quantify the LTV and ROI impact of improving cohort retention at a target month. "
            "Recovered customers are assumed to achieve 30% of Champion annual LTV.</p>",
            unsafe_allow_html=True
        )

        col_ctrl3, col_res3 = st.columns([1, 1.6])

        with col_ctrl3:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            ri_month = st.selectbox("Target Retention Month", [1, 2, 3, 6, 12], key="ri_month",
                                    help="Month number in the cohort retention sequence")
            ri_improvement = st.slider("Improvement (pp)", 1.0, 15.0, 5.0, 0.5, key="ri_imp",
                                       help="Percentage point improvement in retention rate")
            ri_cost = st.number_input("Intervention Cost (₹)", min_value=0,
                                      max_value=5000000, value=100000, step=10000, key="ri_cost",
                                      help="Total cost of the retention program")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_res3:
            ri_res = simulate_retention_improvement(
                cohort_df=cohort, rfm_df=rfm,
                target_month=ri_month, improvement_pct=ri_improvement,
                intervention_cost_inr=ri_cost,
            )
            roi_color = _GREEN if ri_res['roi_pct'] > 0 else _RED

            col_grid1, col_grid2 = st.columns(2)
            with col_grid1:
                st.markdown(_kpi_card(
                    f"Current M{ri_month} Rate",
                    f"{ri_res['current_rate']}%",
                    "avg across all 24 cohorts"
                ), unsafe_allow_html=True)
            with col_grid2:
                st.markdown(_kpi_card(
                    f"Target M{ri_month} Rate",
                    f"{ri_res['new_rate']}%",
                    f"best cohort {ri_res['best_cohort']}: {ri_res['best_cohort_rate']}%",
                    value_color=_GREEN
                ), unsafe_allow_html=True)

            st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)

            col_grid3, col_grid4 = st.columns(2)
            with col_grid3:
                st.markdown(_kpi_card(
                    "Additional Retained",
                    f"{ri_res['additional_retained']:,}",
                    "customers saved per cohort cycle"
                ), unsafe_allow_html=True)
            with col_grid4:
                st.markdown(_kpi_card(
                    "LTV Gained (Annual)",
                    f"₹{ri_res['ltv_gained']:,.0f}",
                    f"ROI: {ri_res['roi_pct']:+.1f}% vs ₹{ri_cost:,} cost",
                    value_color=roi_color
                ), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=ri_res['roi_pct'],
                delta={'reference': 0, 'suffix': '%',
                       'increasing': {'color': '#1D9E75'}, 'decreasing': {'color': '#DC2626'}},
                number={'suffix': '%', 'font': {'size': 28, 'color': '#F8FAFC', 'family': 'DM Sans'}},
                gauge={
                    'axis': {'range': [-100, 500], 'tickcolor': '#475569',
                             'tickfont': {'color': '#475569', 'size': 9}},
                    'bar': {'color': roi_color, 'thickness': 0.25},
                    'bgcolor': 'rgba(13,17,23,0.4)',
                    'bordercolor': 'rgba(139,92,246,0.15)',
                    'steps': [
                        {'range': [-100, 0], 'color': 'rgba(220,38,38,0.08)'},
                        {'range': [0, 500], 'color': 'rgba(29,158,117,0.05)'},
                    ],
                    'threshold': {'line': {'color': '#7C3AED', 'width': 2}, 'thickness': 0.75, 'value': 100}
                },
                title={'text': f"ROI vs Intervention Cost",
                       'font': {'size': 12, 'color': '#94A3B8', 'family': 'Space Mono'}},
            ))
            _apply_custom_theme(fig_gauge, height=260)
            st.plotly_chart(fig_gauge, use_container_width=True)

            st.markdown("<br>", unsafe_allow_html=True)

            ri_rec_text = f"""
            Improving M{ri_month} retention by <b>{ri_improvement:.1f}pp</b>
            saves <b>{ri_res["additional_retained"]:,} extra customers</b>,
            generating <b>₹{ri_res["ltv_gained"]:,.0f}</b> in annual LTV uplift.<br>
            Your benchmark: <b>{ri_res["best_cohort"]}</b> cohort at <b>{ri_res["best_cohort_rate"]}%</b>.<br>
            Champion LTV benchmark = ₹{ri_res["champion_ltv"]:,.0f}/year.
            """
            st.markdown(_recommendation_card("Simulation Insight", ri_rec_text, border=_BORDER, accent=_PURPLE), unsafe_allow_html=True)
