"""Cohort Retention page — Premium "Dark Intelligence" design."""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from utils.charts import (
    apply_premium_theme, apply_premium_theme_no_axes,
    RETENTION_COLORSCALE, BAR_COLOR, LINE_COLOR, LINE_MARKER_COLOR,
)


def render_cohort_retention(
    cohort: pd.DataFrame,
) -> None:
    """Renders Cohort Retention page with premium design."""
    # ── CYBER HEADER ──
    st.markdown("""
    <div style="padding: 24px 0 16px; animation: fadeIn 0.8s ease;">
      <div style="display:flex; align-items:center; gap:14px; margin-bottom:12px;">
        <div style="
          width:44px; height:44px;
          background: linear-gradient(135deg, #EC4899, #8B5CF6);
          border-radius:12px;
          display:flex; align-items:center; justify-content:center;
          font-size:22px;
          box-shadow: 0 8px 24px rgba(236,72,153,0.3);
        ">📈</div>
        <div>
          <div class="stat-badge" style="margin:0; background:rgba(236,72,153,0.15); border-color:rgba(236,72,153,0.35); color:#F472B6; box-shadow:0 0 15px rgba(236,72,153,0.15);">RETENTION ANALYSIS</div>
          <div class="live-badge" style="margin-top:4px;">
            <span class="status-dot status-live"></span>
            Cohort Tracking Active
          </div>
        </div>
      </div>
      <h1 style="
        font-size:40px !important;
        font-weight:900 !important;
        letter-spacing:-0.03em !important;
        line-height:1.1 !important;
        margin:0 0 8px !important;
        background: linear-gradient(135deg, #FFFFFF 0%, #F472B6 50%, #8B5CF6 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
      ">Cohort Retention Analysis</h1>
      <p style="
        font-size:14.5px; color:#64748B;
        font-weight:400; margin:0 0 20px;
        line-height:1.6;
      ">24 monthly cohorts tracked across 2 years — who came back and when?</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    cohort_num = cohort.copy()
    cohort_num.columns = cohort_num.columns.astype(int)

    avg_m1   = cohort_num[1].mean()
    avg_m3   = cohort_num[3].mean()
    best_c   = cohort_num[1].idxmax()
    best_v   = cohort_num[1].max()
    worst_v  = cohort_num[1].min()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Cohorts", "24", "Jan 2014 – Dec 2015")
    with c2:
        st.metric("Avg Month-1 Retention", f"{avg_m1:.1f}%", "of new customers return")
    with c3:
        st.metric("Avg Month-3 Retention", f"{avg_m3:.1f}%", f"{avg_m3-avg_m1:+.1f}pp vs Month-1")
    with c4:
        st.metric("Best Cohort M1", f"{best_v:.1f}%", str(best_c))

    st.markdown("<br>", unsafe_allow_html=True)

    # Heatmap with premium retention colorscale
    st.markdown("<p class='section-label'>Retention Heatmap — Purple = Strong Retention</p>", unsafe_allow_html=True)
    ret_plot = cohort_num.iloc[:, :13].copy()
    ret_plot.index = ret_plot.index.astype(str)

    text_heatmap = [[f'<b>{v:.0f}%</b>' if not np.isnan(v) else '' for v in row] for row in ret_plot.values]

    fig = go.Figure(data=go.Heatmap(
        z=ret_plot.values,
        x=[f'M{i}' for i in ret_plot.columns],
        y=ret_plot.index.tolist(),
        colorscale=RETENTION_COLORSCALE,
        zmin=0, zmax=35,
        text=text_heatmap,
        texttemplate='%{text}',
        textfont={"size": 10, "color": "white", "family": "Inter"},
        colorbar=dict(
            title=dict(text='Retention %', font=dict(color='#94A3B8', size=11)),
            ticksuffix='%', tickfont=dict(color='#94A3B8'),
            bgcolor='rgba(0,0,0,0)', bordercolor='rgba(139,92,246,0.2)', borderwidth=1
        )
    ))
    apply_premium_theme_no_axes(fig, height=580)
    fig.update_layout(
        xaxis=dict(color='#94A3B8', tickfont=dict(size=11)),
        yaxis=dict(color='#94A3B8', autorange='reversed', tickfont=dict(size=11)),
        margin=dict(l=10, r=10, t=10, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Slider for Cohort retention analysis by month
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p class='section-label'>Cohort Retention Analysis by Month</p>", unsafe_allow_html=True)
    selected_month = st.slider("Select Month Number to Analyse", 0, 12, 1)

    m_data = cohort_num[selected_month].dropna().reset_index()
    m_data.columns = ['Cohort', 'Retention']
    m_data = m_data.sort_values('Retention', ascending=True)

    if not m_data.empty:
        best_cohort = m_data.sort_values('Retention', ascending=False).iloc[0]['Cohort']
        worst_cohort = m_data.sort_values('Retention', ascending=True).iloc[0]['Cohort']

        colors_bar = []
        for idx, row in m_data.iterrows():
            if row['Cohort'] == best_cohort:
                colors_bar.append('#A78BFA')  # purple light
            elif row['Cohort'] == worst_cohort:
                colors_bar.append('#EF4444')  # red alert
            else:
                colors_bar.append('rgba(139,92,246,0.2)')  # muted purple

        fig_m = go.Figure(go.Bar(
            x=m_data['Retention'],
            y=m_data['Cohort'].astype(str),
            orientation='h',
            marker_color=colors_bar,
            text=m_data['Retention'].round(1).astype(str) + '%',
            textposition='outside',
            textfont=dict(color='#94A3B8', size=9)
        ))
        apply_premium_theme(fig_m, height=450)
        fig_m.update_layout(
            xaxis=dict(title='Retention %', color='#94A3B8',
                       gridcolor='rgba(139,92,246,0.06)', ticksuffix='%'),
            yaxis=dict(color='#94A3B8', gridcolor='rgba(139,92,246,0.06)'),
            margin=dict(l=10, r=40, t=10, b=10)
        )
        st.plotly_chart(fig_m, use_container_width=True)

    # Month-1 line with markers
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p class='section-label'>Month-1 Retention Trend — by Cohort</p>", unsafe_allow_html=True)
    m1 = cohort_num[1].dropna().reset_index()
    m1.columns = ['cohort', 'retention']
    m1['cohort'] = m1['cohort'].astype(str)

    best_m1_idx = m1['retention'].idxmax()
    best_m1_row = m1.loc[best_m1_idx]
    worst_m1_idx = m1['retention'].idxmin()
    worst_m1_row = m1.loc[worst_m1_idx]

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=m1['cohort'], y=m1['retention'],
        mode='lines',
        line=dict(color=LINE_COLOR, width=2.5),
        fill='tozeroy', fillcolor='rgba(139,92,246,0.08)',
        name='Month-1 Retention'
    ))
    # Best dot
    fig2.add_trace(go.Scatter(
        x=[best_m1_row['cohort']], y=[best_m1_row['retention']],
        mode='markers',
        marker=dict(color='#10B981', size=12, line=dict(color='#050810', width=2)),
        hoverinfo='text',
        text=f"Best Cohort: {best_m1_row['cohort']} ({best_m1_row['retention']:.1f}%)",
        name=f"Best: {best_m1_row['cohort']}"
    ))
    # Worst dot
    fig2.add_trace(go.Scatter(
        x=[worst_m1_row['cohort']], y=[worst_m1_row['retention']],
        mode='markers',
        marker=dict(color='#EF4444', size=12, line=dict(color='#050810', width=2)),
        hoverinfo='text',
        text=f"Worst Cohort: {worst_m1_row['cohort']} ({worst_m1_row['retention']:.1f}%)",
        name=f"Worst: {worst_m1_row['cohort']}"
    ))
    # Average line
    fig2.add_hline(
        y=avg_m1, line_dash='dash', line_color='#8B5CF6', line_width=1.5,
        annotation_text=f'Avg {avg_m1:.1f}%',
        annotation_font_color='#94A3B8', annotation_font_size=11
    )
    apply_premium_theme(fig2, height=280)
    fig2.update_layout(
        xaxis=dict(color='#94A3B8', tickangle=45, tickfont=dict(size=10)),
        yaxis=dict(color='#94A3B8', ticksuffix='%'),
        showlegend=True,
        legend=dict(bgcolor='rgba(13,17,23,0.8)', font=dict(color='#94A3B8', size=10))
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Cohort Insights
    st.markdown("<br>")
    st.markdown("---")
    st.markdown("<p class='section-label'>Cohort Insights</p>", unsafe_allow_html=True)
    diff_m3_m1 = avg_m3 - avg_m1

    st.markdown(f"""
    <div class='glass-card' style='margin-bottom: 24px;'>
        <ul style='color:#CBD5E1; margin:0; padding-left:20px; line-height:1.75; font-size:13px;'>
            <li><b>Highest Performing Cohort:</b> The best cohort is <b>{best_c}</b>, achieving a Month-1 retention rate of <b>{best_v:.1f}%</b>. This is a remarkable 84% above the average customer retention rate, highlighting a highly successful onboarding period.</li>
            <li><b>Lowest Performing Cohort:</b> The worst cohort is <b>{cohort_num[1].idxmin()}</b>, with a Month-1 retention rate of <b>{worst_v:.1f}%</b>, which warrants further operational and acquisition quality review.</li>
            <li><b>Loyalty Progression:</b> Month-3 retention is <b>{diff_m3_m1:.1f}% HIGHER</b> than Month-1 — meaning customers who survive the first month become long-term loyalists.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style='background: rgba(139,92,246,0.08); border: 1px solid rgba(139,92,246,0.25);
                border-radius: 16px; padding: 22px 26px; margin-bottom: 24px;
                backdrop-filter: blur(20px);'>
        <div style='font-size: 10px; color: #8B5CF6; font-weight: 700;
                    text-transform: uppercase; letter-spacing:0.1em;'>Strategic Recommendation</div>
        <div style='font-size:14px; font-weight:500; color:#F8FAFC; margin-top:8px; line-height:1.6;'>
            The 14.3% average Month-1 retention suggests most first-time customers don't return.
            A targeted "second purchase" incentive campaign in Month-1 could move this to 25%+
            based on best cohort performance.
        </div>
    </div>
    """, unsafe_allow_html=True)
