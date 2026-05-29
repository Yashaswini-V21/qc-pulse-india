"""Customer Segments page — Premium "Dark Intelligence" design."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config import SEGMENT_COLORS
from utils.charts import (
    apply_premium_theme, apply_premium_theme_no_axes,
    SEGMENT_SCATTER_COLORS,
)


def render_customer_segments(
    rfm: pd.DataFrame,
    rfm_sum: pd.DataFrame,
) -> None:
    """Renders Customer Segments page with premium design."""
    # ── CYBER HEADER ──
    st.markdown("""
    <div style="padding: 24px 0 16px; animation: fadeIn 0.8s ease;">
      <div style="display:flex; align-items:center; gap:14px; margin-bottom:12px;">
        <div style="
          width:44px; height:44px;
          background: linear-gradient(135deg, #B923FF, #3B82F6);
          border-radius:12px;
          display:flex; align-items:center; justify-content:center;
          font-size:22px;
          box-shadow: 0 8px 24px rgba(185,35,255,0.3);
        ">👥</div>
        <div>
          <div class="stat-badge" style="margin:0; background:rgba(185,35,255,0.15); border-color:rgba(185,35,255,0.35); color:#D8B4FE; box-shadow:0 0 15px rgba(185,35,255,0.15);">RFM ANALYSIS</div>
          <div class="live-badge" style="margin-top:4px;">
            <span class="status-dot status-live"></span>
            Customer Clustering Engine Active
          </div>
        </div>
      </div>
      <h1 style="
        font-size:40px !important;
        font-weight:900 !important;
        letter-spacing:-0.03em !important;
        line-height:1.1 !important;
        margin:0 0 8px !important;
        background: linear-gradient(135deg, #FFFFFF 0%, #D8B4FE 50%, #60A5FA 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
      ">Customer Segmentation</h1>
      <p style="
        font-size:14.5px; color:#64748B;
        font-weight:400; margin:0 0 20px;
        line-height:1.6;
      ">3,898 customers segmented by Recency · Frequency · Monetary value</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # Segment selector in sidebar
    with st.sidebar:
        st.markdown("""<hr style='border:none; height:1px;
                       background: linear-gradient(90deg, transparent,
                       rgba(139,92,246,0.2), transparent); margin:16px 0'>""", unsafe_allow_html=True)
        st.markdown("<p class='section-label'>Segment Filtering</p>", unsafe_allow_html=True)
        selected_segment = st.selectbox(
            "Highlight Segment",
            ["All Segments", "Champion", "Loyal", "Potential", "At-Risk", "Churned"]
        )

    # Setup colors based on selection
    if selected_segment == "All Segments":
        seg_colors = SEGMENT_SCATTER_COLORS.copy()
    else:
        seg_colors = {
            s: (color if s == selected_segment else '#1E293B')
            for s, color in SEGMENT_SCATTER_COLORS.items()
        }

    champ = rfm_sum[rfm_sum['segment'] == 'Champion'].iloc[0]
    churn = rfm_sum[rfm_sum['segment'] == 'Churned'].iloc[0]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Customers", f"{len(rfm):,}")
    with c2:
        st.metric("Champions", f"{int(champ['customers']):,}", f"{champ['pct_customers']}% of base")
    with c3:
        st.metric("Churned", f"{int(churn['customers']):,}", f"{churn['pct_customers']}% need win-back")
    with c4:
        st.metric("Champion Avg Frequency", f"{champ['avg_frequency']:.1f}x", f"vs {churn['avg_frequency']:.1f}x churned")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<p class='section-label'>Segment Distribution — Treemap</p>", unsafe_allow_html=True)
        fig1 = px.treemap(
            rfm, path=['segment'], values='RFM_Score', color='segment',
            color_discrete_map=seg_colors
        )
        fig1.update_layout(
            height=380, paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=13, family='Inter'),
            margin=dict(l=0, r=0, t=10, b=0),
            coloraxis_showscale=False
        )
        fig1.update_traces(
            textinfo='label+percent entry',
            textfont=dict(size=14, color='white'),
            marker=dict(line=dict(color='#050810', width=3))
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("<p class='section-label'>Recency vs Frequency — by Segment</p>", unsafe_allow_html=True)
        fig2 = px.scatter(
            rfm.sample(min(1500, len(rfm))),
            x='recency', y='frequency',
            color='segment', size='monetary',
            color_discrete_map=seg_colors,
            opacity=0.75,
            labels={'recency': 'Days Since Last Order', 'frequency': 'Number of Orders'},
            size_max=14
        )
        fig2.add_annotation(
            x=80, y=9.5,
            text="High frequency, recent",
            showarrow=False,
            font=dict(color='#475569', size=10),
            align='left'
        )
        apply_premium_theme(fig2, height=380)
        fig2.update_layout(
            legend=dict(bgcolor='rgba(13,17,23,0.8)', font=dict(color='#94A3B8', size=11),
                        bordercolor='rgba(139,92,246,0.2)', borderwidth=1)
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Segment Deep Dive
    st.markdown("---")
    st.markdown("<p class='section-label'>Segment Deep Dive — Metrics Comparison</p>", unsafe_allow_html=True)

    fig_deep = go.Figure()
    metric_labels = ['Avg Recency (Days)', 'Avg Orders', 'Avg Items Bought']

    for seg in rfm_sum['segment'].unique():
        sub = rfm_sum[rfm_sum['segment'] == seg].iloc[0]
        fig_deep.add_trace(go.Bar(
            name=seg,
            y=metric_labels,
            x=[sub['avg_recency'], sub['avg_frequency'], sub['avg_monetary']],
            orientation='h',
            marker_color=seg_colors.get(seg, '#475569'),
            text=[f"{sub['avg_recency']:.0f}d", f"{sub['avg_frequency']:.1f}x", f"{sub['avg_monetary']:.0f}"],
            textposition='outside',
            textfont=dict(color='#94A3B8', size=10)
        ))

    fig_deep.update_layout(barmode='group')
    apply_premium_theme(fig_deep, height=350,
                        margin=dict(l=10, r=40, t=10, b=10))
    fig_deep.update_layout(
        legend=dict(bgcolor='rgba(13,17,23,0.8)', font=dict(color='#94A3B8', size=11))
    )
    st.plotly_chart(fig_deep, use_container_width=True)

    # Summary table
    st.markdown("<p class='section-label'>Full Segment Summary</p>", unsafe_allow_html=True)
    display_df = rfm_sum[['segment', 'customers', 'pct_customers', 'avg_recency',
                           'avg_frequency', 'avg_monetary', 'avg_rfm_score']].copy()
    display_df.columns = ['Segment', 'Customers', '% of Base', 'Avg Recency (days)',
                          'Avg Orders', 'Avg Items', 'Avg RFM Score']
    display_df = display_df.sort_values('Avg RFM Score', ascending=False)
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    # Business Recommendations
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p class='section-label'>Business Recommendations by Segment</p>", unsafe_allow_html=True)

    rec_cols = st.columns(5)
    recs = {
        'Champion': ("Offer Loyalty Rewards", "Offer loyalty rewards — don't let them churn. Focus on exclusive early access and retention programs.", "#A78BFA"),
        'Loyal': ("Upsell Premium", "Upsell premium categories — they're ready. Cross-sell high-margin items and organic premium brands.", "#60A5FA"),
        'Potential': ("Targeted Re-engagement", "Send targeted re-engagement within 30 days. Nurture them with personalized deals and repeat-purchase perks.", "#34D399"),
        'At-Risk': ("Emergency Discount", "Emergency discount campaign — 24hr offer. Trigger time-limited win-back push notifications.", "#FBBF24"),
        'Churned': ("Win-back Activation", "Win-back email with highest-performing product from their history. Run cold-customer reactivation campaigns.", "#F87171")
    }

    for idx, seg in enumerate(['Champion', 'Loyal', 'Potential', 'At-Risk', 'Churned']):
        title, desc, color = recs[seg]
        border_color = color if (selected_segment == "All Segments" or selected_segment == seg) else "rgba(139,92,246,0.08)"
        opacity = 1.0 if (selected_segment == "All Segments" or selected_segment == seg) else 0.4

        with rec_cols[idx]:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg,
                          rgba(13,17,23,0.9) 0%, rgba(8,12,24,0.8) 100%);
                        border: 1px solid {border_color}; border-radius: 16px; padding: 18px; height: 170px;
                        opacity: {opacity}; transition: all 0.3s ease;
                        backdrop-filter: blur(20px);'>
                <div style='font-size: 10px; color: {color}; font-weight: 700;
                            text-transform: uppercase; letter-spacing:0.1em;'>
                    {seg}
                </div>
                <div style='font-size:13px; font-weight:700; color:#F8FAFC; margin: 4px 0 8px 0;'>{title}</div>
                <div style='font-size:11px; color:#94A3B8; line-height: 1.5;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)
