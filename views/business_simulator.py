"""Business Decision Simulator page — Premium "Dark Intelligence" design."""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from utils.simulator import (
    simulate_winback_campaign,
    simulate_price_change,
    simulate_retention_improvement,
)
from utils.charts import apply_premium_theme


def render_business_simulator(
    rfm: pd.DataFrame,
    cohort: pd.DataFrame,
    pm: pd.DataFrame,
) -> None:
    """Renders Business Simulator page with premium design."""
    # ── CYBER HEADER ──
    st.markdown("""
    <div style="padding: 24px 0 16px; animation: fadeIn 0.8s ease;">
      <div style="display:flex; align-items:center; gap:14px; margin-bottom:12px;">
        <div style="
          width:44px; height:44px;
          background: linear-gradient(135deg, #EF4444, #B923FF);
          border-radius:12px;
          display:flex; align-items:center; justify-content:center;
          font-size:22px;
          box-shadow: 0 8px 24px rgba(239,68,68,0.3);
        ">🎯</div>
        <div>
          <div class="stat-badge" style="margin:0; background:rgba(239,68,68,0.15); border-color:rgba(239,68,68,0.35); color:#FCA5A5; box-shadow:0 0 15px rgba(239,68,68,0.15);">DECISION ENGINE</div>
          <div class="live-badge" style="margin-top:4px;">
            <span class="status-dot status-live"></span>
            Simulation Sandbox Active
          </div>
        </div>
      </div>
      <h1 style="
        font-size:40px !important;
        font-weight:900 !important;
        letter-spacing:-0.03em !important;
        line-height:1.1 !important;
        margin:0 0 8px !important;
        background: linear-gradient(135deg, #FFFFFF 0%, #FCA5A5 50%, #B923FF 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
      ">Business Decision Simulator</h1>
      <p style="
        font-size:14.5px; color:#64748B;
        font-weight:400; margin:0 0 20px;
        line-height:1.6;
      ">Model real business decisions — what-if scenarios backed by your actual data. Every number here is computed from the 38,765 real transactions in this dataset.</p>
    </div>
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
            "<p style='color:#64748B;font-size:13px;margin-bottom:20px'>"
            "Model the ROI of an email/SMS re-engagement campaign targeting inactive segments. "
            "Recovery rate is derived from your actual cohort Month-1 retention data.</p>",
            unsafe_allow_html=True
        )

        col_ctrl, col_res = st.columns([1, 1.6])

        with col_ctrl:
            st.markdown(
                "<div class='glass-card'>",
                unsafe_allow_html=True
            )
            wb_segment = st.selectbox("Target Segment", ["Churned", "At-Risk"], key="wb_seg")
            seg_size = len(rfm[rfm['segment'] == wb_segment])
            st.markdown(
                f"<p style='color:#475569;font-size:11px;"
                f"margin-top:-8px;margin-bottom:12px'>"
                f"Segment: {seg_size:,} customers available</p>",
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
            r_color = "#10B981" if wb_res['roi_pct'] > 0 else "#EF4444"

            st.markdown(f"""
            <div style='display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px;'>
                <div style='background:linear-gradient(135deg,rgba(13,17,23,0.9),rgba(8,12,24,0.8));
                            border:1px solid rgba(139,92,246,0.12);border-radius:16px;padding:18px;
                            backdrop-filter:blur(20px);'>
                    <div style='font-size:9px;color:#475569;text-transform:uppercase;letter-spacing:.1em;
                                margin-bottom:6px;font-weight:700;'>Customers Recovered</div>
                    <div style='font-size:28px;font-weight:800;
                                background:linear-gradient(135deg,#F8FAFC,#A78BFA);
                                -webkit-background-clip:text;-webkit-text-fill-color:transparent;'>
                        {wb_res["customers_recovered"]:,}</div>
                    <div style='font-size:11px;color:#475569;margin-top:4px;'>
                        {wb_res["recovery_rate_pct"]}% rate (+{wb_res["discount_boost_pp"]}pp from discount)</div>
                </div>
                <div style='background:linear-gradient(135deg,rgba(13,17,23,0.9),rgba(8,12,24,0.8));
                            border:1px solid rgba(139,92,246,0.12);border-radius:16px;padding:18px;
                            backdrop-filter:blur(20px);'>
                    <div style='font-size:9px;color:#475569;text-transform:uppercase;letter-spacing:.1em;
                                margin-bottom:6px;font-weight:700;'>Revenue Gained (3 months)</div>
                    <div style='font-size:28px;font-weight:800;
                                background:linear-gradient(135deg,#F8FAFC,#A78BFA);
                                -webkit-background-clip:text;-webkit-text-fill-color:transparent;'>
                        &#8377;{wb_res["revenue_gained"]:,.0f}</div>
                    <div style='font-size:11px;color:#475569;margin-top:4px;'>
                        2 orders/month (estimated win-back) * &#8377;350 basket</div>
                </div>
                <div style='background:linear-gradient(135deg,rgba(13,17,23,0.9),rgba(8,12,24,0.8));
                            border:1px solid {"rgba(16,185,129,0.3)" if wb_res["roi_pct"] > 0 else "rgba(239,68,68,0.3)"};
                            border-radius:16px;padding:18px;backdrop-filter:blur(20px);'>
                    <div style='font-size:9px;color:#475569;text-transform:uppercase;letter-spacing:.1em;
                                margin-bottom:6px;font-weight:700;'>Campaign ROI</div>
                    <div style='font-size:28px;font-weight:800;color:{r_color};'>
                        {wb_res["roi_pct"]:+.1f}%</div>
                    <div style='font-size:11px;color:#475569;margin-top:4px;'>
                        vs &#8377;{wb_budget:,} budget spent</div>
                </div>
                <div style='background:linear-gradient(135deg,rgba(13,17,23,0.9),rgba(8,12,24,0.8));
                            border:1px solid rgba(139,92,246,0.12);border-radius:16px;padding:18px;
                            backdrop-filter:blur(20px);'>
                    <div style='font-size:9px;color:#475569;text-transform:uppercase;letter-spacing:.1em;
                                margin-bottom:6px;font-weight:700;'>Cost Per Recovery</div>
                    <div style='font-size:28px;font-weight:800;
                                background:linear-gradient(135deg,#F8FAFC,#A78BFA);
                                -webkit-background-clip:text;-webkit-text-fill-color:transparent;'>
                        &#8377;{wb_res["cost_per_recovered"]:,.0f}</div>
                    <div style='font-size:11px;color:#475569;margin-top:4px;'>per recovered customer</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            payback = wb_res['payback_months']
            payback_txt = f"{payback:.1f} months" if payback < 90 else "Not profitable at this budget"
            st.markdown(f"""
            <div style='background:linear-gradient(135deg,rgba(13,17,23,0.9),rgba(8,12,24,0.8));
                        border:1px solid rgba(139,92,246,0.25);border-radius:16px;padding:18px;
                        backdrop-filter:blur(20px);'>
                <div style='font-size:9px;color:#8B5CF6;
                            font-weight:700;text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px;'>
                    Simulation Recommendation</div>
                <div style='color:#CBD5E1;font-size:13px;line-height:1.7;'>
                    Targeting <b>{wb_customers:,} {wb_segment}</b> customers with a
                    <b>&#8377;{wb_budget:,}</b> campaign and <b>{wb_discount}% discount</b> coupon
                    yields <b>{wb_res["customers_recovered"]:,} recovered customers</b> and
                    <b>&#8377;{wb_res["revenue_gained"]:,.0f}</b> in 3-month revenue.
                    Payback period: <b>{payback_txt}</b>.
                    Benchmark against <b>{wb_res["recommended_cohort"]}</b> cohort
                    ({wb_res["base_retention_rate"]}% baseline retention).
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── TAB 2: PRICE CHANGE IMPACT ──
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p class='section-label'>Price Change Impact Simulator</p>", unsafe_allow_html=True)
        st.markdown(
            "<p style='color:#64748B;font-size:13px;margin-bottom:20px'>"
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
                direction_color = "#10B981" if pc_discount_change > 0 else "#EF4444"
                rev_color = "#10B981" if pc_res['revenue_impact'] > 0 else "#EF4444"
                rev_sign = "+" if pc_res['revenue_impact'] >= 0 else ""

                st.markdown(f"""
                <div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:14px;'>
                    <div style='background:linear-gradient(135deg,rgba(13,17,23,0.9),rgba(8,12,24,0.8));
                                border:1px solid rgba(139,92,246,0.12);border-radius:14px;padding:16px;
                                backdrop-filter:blur(20px);'>
                        <div style='font-size:9px;color:#475569;text-transform:uppercase;margin-bottom:4px;
                                    font-weight:700;'>Current Price</div>
                        <div style='font-size:22px;font-weight:800;
                                    background:linear-gradient(135deg,#F8FAFC,#A78BFA);
                                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;'>
                            &#8377;{pc_res["current_price"]:.2f}</div>
                        <div style='font-size:10px;color:#475569;margin-top:3px;'>
                            Market avg: &#8377;{pc_res["market_avg"]:.2f}</div>
                    </div>
                    <div style='background:linear-gradient(135deg,rgba(13,17,23,0.9),rgba(8,12,24,0.8));
                                border:1px solid {direction_color}40;border-radius:14px;padding:16px;
                                backdrop-filter:blur(20px);'>
                        <div style='font-size:9px;color:#475569;text-transform:uppercase;margin-bottom:4px;
                                    font-weight:700;'>New Price</div>
                        <div style='font-size:22px;font-weight:800;color:{direction_color};'>
                            &#8377;{pc_res["new_price"]:.2f}</div>
                        <div style='font-size:10px;color:#475569;margin-top:3px;'>
                            {pc_discount_change:+.0f}% {"cut" if pc_discount_change > 0 else "increase"}</div>
                    </div>
                    <div style='background:linear-gradient(135deg,rgba(13,17,23,0.9),rgba(8,12,24,0.8));
                                border:1px solid {rev_color}40;border-radius:14px;padding:16px;
                                backdrop-filter:blur(20px);'>
                        <div style='font-size:9px;color:#475569;text-transform:uppercase;margin-bottom:4px;
                                    font-weight:700;'>Revenue Impact</div>
                        <div style='font-size:22px;font-weight:800;color:{rev_color};'>
                            {rev_sign}&#8377;{abs(pc_res["revenue_impact"]):,.0f}</div>
                        <div style='font-size:10px;color:#475569;margin-top:3px;'>
                            {pc_customers:,} customers affected</div>
                    </div>
                </div>
                <div style='display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px;'>
                    <div style='background:linear-gradient(135deg,rgba(13,17,23,0.9),rgba(8,12,24,0.8));
                                border:1px solid rgba(139,92,246,0.12);border-radius:14px;padding:16px;
                                backdrop-filter:blur(20px);'>
                        <div style='font-size:9px;color:#475569;text-transform:uppercase;margin-bottom:4px;
                                    font-weight:700;'>Gap Before</div>
                        <div style='font-size:20px;font-weight:800;
                                    color:{"#EF4444" if pc_res["gap_before"] > 0 else "#10B981"};'>
                            {pc_res["gap_before"]:+.1f}%</div>
                        <div style='font-size:10px;color:#475569;margin-top:3px;'>
                            vs market average — {pc_res["position_before"]}</div>
                    </div>
                    <div style='background:linear-gradient(135deg,rgba(13,17,23,0.9),rgba(8,12,24,0.8));
                                border:1px solid {direction_color}40;border-radius:14px;padding:16px;
                                backdrop-filter:blur(20px);'>
                        <div style='font-size:9px;color:#475569;text-transform:uppercase;margin-bottom:4px;
                                    font-weight:700;'>Gap After {pc_res["position_arrow"]}</div>
                        <div style='font-size:20px;font-weight:800;
                                    color:{"#EF4444" if pc_res["gap_after"] > 0 else "#10B981"};'>
                            {pc_res["gap_after"]:+.1f}%</div>
                        <div style='font-size:10px;color:#475569;margin-top:3px;'>
                            vs market average — {pc_res["position_after"]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                fig_gap = go.Figure()
                fig_gap.add_trace(go.Bar(
                    x=['Before', 'After'],
                    y=[pc_res['gap_before'], pc_res['gap_after']],
                    marker_color=['#EF4444' if pc_res['gap_before'] > 0 else '#10B981',
                                  '#EF4444' if pc_res['gap_after'] > 0 else '#10B981'],
                    text=[f"{pc_res['gap_before']:+.1f}%", f"{pc_res['gap_after']:+.1f}%"],
                    textposition='outside',
                    textfont=dict(color='#94A3B8', size=13, family='Inter'),
                    marker_line_width=0,
                ))
                fig_gap.add_hline(y=0, line_color='#475569', line_dash='dash', line_width=1)
                apply_premium_theme(fig_gap, height=220)
                fig_gap.update_layout(
                    title=dict(text='Price Gap vs Market Average (%)', font=dict(color='#94A3B8', size=12)),
                    yaxis=dict(title='Gap %', color='#94A3B8',
                               gridcolor='rgba(139,92,246,0.06)', ticksuffix='%'),
                    xaxis=dict(color='#94A3B8'),
                    margin=dict(l=10, r=10, t=44, b=10),
                )
                st.plotly_chart(fig_gap, use_container_width=True)

    # ── TAB 3: RETENTION IMPROVEMENT ──
    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p class='section-label'>Retention Improvement Simulator</p>", unsafe_allow_html=True)
        st.markdown(
            "<p style='color:#64748B;font-size:13px;margin-bottom:20px'>"
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
            roi_color = "#10B981" if ri_res['roi_pct'] > 0 else "#EF4444"

            st.markdown(f"""
            <div style='display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:14px;'>
                <div style='background:linear-gradient(135deg,rgba(13,17,23,0.9),rgba(8,12,24,0.8));
                            border:1px solid rgba(139,92,246,0.12);border-radius:16px;padding:18px;
                            backdrop-filter:blur(20px);'>
                    <div style='font-size:9px;color:#475569;text-transform:uppercase;letter-spacing:.1em;
                                margin-bottom:6px;font-weight:700;'>Current M{ri_month} Rate</div>
                    <div style='font-size:26px;font-weight:800;
                                background:linear-gradient(135deg,#F8FAFC,#A78BFA);
                                -webkit-background-clip:text;-webkit-text-fill-color:transparent;'>
                        {ri_res["current_rate"]}%</div>
                    <div style='font-size:11px;color:#475569;margin-top:4px;'>avg across all 24 cohorts</div>
                </div>
                <div style='background:linear-gradient(135deg,rgba(13,17,23,0.9),rgba(8,12,24,0.8));
                            border:1px solid rgba(16,185,129,0.3);border-radius:16px;padding:18px;
                            backdrop-filter:blur(20px);'>
                    <div style='font-size:9px;color:#475569;text-transform:uppercase;letter-spacing:.1em;
                                margin-bottom:6px;font-weight:700;'>Target M{ri_month} Rate</div>
                    <div style='font-size:26px;font-weight:800;color:#10B981;'>{ri_res["new_rate"]}%</div>
                    <div style='font-size:11px;color:#475569;margin-top:4px;'>
                        best cohort {ri_res["best_cohort"]}: {ri_res["best_cohort_rate"]}%</div>
                </div>
                <div style='background:linear-gradient(135deg,rgba(13,17,23,0.9),rgba(8,12,24,0.8));
                            border:1px solid rgba(139,92,246,0.12);border-radius:16px;padding:18px;
                            backdrop-filter:blur(20px);'>
                    <div style='font-size:9px;color:#475569;text-transform:uppercase;letter-spacing:.1em;
                                margin-bottom:6px;font-weight:700;'>Additional Retained</div>
                    <div style='font-size:26px;font-weight:800;
                                background:linear-gradient(135deg,#F8FAFC,#A78BFA);
                                -webkit-background-clip:text;-webkit-text-fill-color:transparent;'>
                        {ri_res["additional_retained"]:,}</div>
                    <div style='font-size:11px;color:#475569;margin-top:4px;'>customers saved per cohort cycle</div>
                </div>
                <div style='background:linear-gradient(135deg,rgba(13,17,23,0.9),rgba(8,12,24,0.8));
                            border:1px solid {roi_color}40;border-radius:16px;padding:18px;
                            backdrop-filter:blur(20px);'>
                    <div style='font-size:9px;color:#475569;text-transform:uppercase;letter-spacing:.1em;
                                margin-bottom:6px;font-weight:700;'>LTV Gained (Annual)</div>
                    <div style='font-size:26px;font-weight:800;color:{roi_color};'>
                        &#8377;{ri_res["ltv_gained"]:,.0f}</div>
                    <div style='font-size:11px;color:#475569;margin-top:4px;'>
                        ROI: {ri_res["roi_pct"]:+.1f}% vs &#8377;{ri_cost:,} cost</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=ri_res['roi_pct'],
                delta={'reference': 0, 'suffix': '%',
                       'increasing': {'color': '#10B981'}, 'decreasing': {'color': '#EF4444'}},
                number={'suffix': '%', 'font': {'size': 28, 'color': '#F8FAFC', 'family': 'Inter'}},
                gauge={
                    'axis': {'range': [-100, 500], 'tickcolor': '#475569',
                             'tickfont': {'color': '#475569', 'size': 9}},
                    'bar': {'color': roi_color, 'thickness': 0.25},
                    'bgcolor': 'rgba(13,17,23,0.4)',
                    'bordercolor': 'rgba(139,92,246,0.15)',
                    'steps': [
                        {'range': [-100, 0], 'color': 'rgba(239,68,68,0.08)'},
                        {'range': [0, 500], 'color': 'rgba(16,185,129,0.05)'},
                    ],
                    'threshold': {'line': {'color': '#8B5CF6', 'width': 2}, 'thickness': 0.75, 'value': 100}
                },
                title={'text': f"ROI vs Intervention Cost",
                       'font': {'size': 12, 'color': '#94A3B8', 'family': 'Inter'}},
            ))
            fig_gauge.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#94A3B8', family='Inter'),
                height=260,
                margin=dict(l=20, r=20, t=40, b=10),
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

            st.markdown(f"""
            <div style='background:linear-gradient(135deg,rgba(13,17,23,0.9),rgba(8,12,24,0.8));
                        border:1px solid rgba(139,92,246,0.25);border-radius:16px;padding:18px;
                        backdrop-filter:blur(20px);'>
                <div style='font-size:9px;color:#8B5CF6;
                            font-weight:700;text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px;'>
                    Simulation Insight</div>
                <div style='color:#CBD5E1;font-size:13px;line-height:1.7;'>
                    Improving M{ri_month} retention by <b>{ri_improvement:.1f}pp</b>
                    saves <b>{ri_res["additional_retained"]:,} extra customers</b>,
                    generating <b>&#8377;{ri_res["ltv_gained"]:,.0f}</b> in annual LTV uplift.
                    Your benchmark: <b>{ri_res["best_cohort"]}</b> cohort at <b>{ri_res["best_cohort_rate"]}%</b>.
                    Champion LTV benchmark = &#8377;{ri_res["champion_ltv"]:,.0f}/year.
                </div>
            </div>
            """, unsafe_allow_html=True)
