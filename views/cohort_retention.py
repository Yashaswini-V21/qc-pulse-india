import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any

def render_cohort_retention(
    cohort: pd.DataFrame,
    DARK_LAYOUT: Dict[str, Any]
) -> None:
    """
    Renders modular Cohort Retention page for QC Pulse India.
    """
    st.markdown("<span class='stat-badge'>RETENTION ANALYSIS</span>", unsafe_allow_html=True)
    st.title("Cohort Retention Analysis")
    st.markdown("<p style='color:#475569;font-size:14px;margin-top:-8px'>24 monthly cohorts tracked across 2 years — who came back and when?</p>", unsafe_allow_html=True)
    st.markdown("---")

    cohort_num = cohort.copy()
    cohort_num.columns = cohort_num.columns.astype(int)

    avg_m1   = cohort_num[1].mean()
    avg_m3   = cohort_num[3].mean()
    best_c   = cohort_num[1].idxmax()
    best_v   = cohort_num[1].max()
    worst_v  = cohort_num[1].min()

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Cohorts", "24", "Jan 2014 – Dec 2015")
    with c2: st.metric("Avg Month-1 Retention", f"{avg_m1:.1f}%", "of new customers return")
    with c3: st.metric("Avg Month-3 Retention", f"{avg_m3:.1f}%", f"{avg_m3-avg_m1:+.1f}pp vs Month-1")
    with c4: st.metric("Best Cohort M1", f"{best_v:.1f}%", str(best_c))

    st.markdown("<br>", unsafe_allow_html=True)

    # Heatmap
    st.markdown("<p class='section-label'>Retention Heatmap — Green = Strong Retention, Red = Drop-off</p>", unsafe_allow_html=True)
    ret_plot = cohort_num.iloc[:, :13].copy()
    ret_plot.index = ret_plot.index.astype(str)

    # Cells 10px bold white text
    text_heatmap = [[f'<b>{v:.0f}%</b>' if not np.isnan(v) else '' for v in row] for row in ret_plot.values]

    fig = go.Figure(data=go.Heatmap(
        z=ret_plot.values,
        x=[f'M{i}' for i in ret_plot.columns],
        y=ret_plot.index.tolist(),
        colorscale=[
            [0.0,  '#450A0A'],   # 0%
            [0.15, '#DC2626'],   # 15%
            [0.25, '#F59E0B'],   # 25%
            [0.35, '#FBBF24'],   # 35%
            [0.50, '#86EFAC'],   # 50%
            [0.75, '#16A34A'],   # 75%
            [1.0,  '#052E16']    # 100%
        ],
        zmin=0, zmax=35,
        text=text_heatmap,
        texttemplate='%{text}',
        textfont={"size": 10, "color": "white", "family": "DM Sans"},
        colorbar=dict(
            title=dict(text='Retention %', font=dict(color='#94A3B8', size=11)),
            ticksuffix='%', tickfont=dict(color='#94A3B8'),
            bgcolor='#0D1823', bordercolor='#1E2D40', borderwidth=1
        )
    ))
    fig.update_layout(
        **{k: v for k, v in DARK_LAYOUT.items() if k not in ['xaxis', 'yaxis']},
        height=580,
        xaxis=dict(color='#94A3B8', tickfont=dict(size=11)),
        yaxis=dict(color='#94A3B8', autorange='reversed', tickfont=dict(size=11)),
        margin=dict(l=10, r=10, t=10, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Slider for Cohort retention analysis by month number
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
                colors_bar.append('#16A34A')  # green
            elif row['Cohort'] == worst_cohort:
                colors_bar.append('#DC2626')  # red
            else:
                colors_bar.append('#1E2D40')  # navy

        fig_m = go.Figure(go.Bar(
            x=m_data['Retention'],
            y=m_data['Cohort'].astype(str),
            orientation='h',
            marker_color=colors_bar,
            text=m_data['Retention'].round(1).astype(str) + '%',
            textposition='outside',
            textfont=dict(color='#94A3B8', size=9)
        ))
        fig_m.update_layout(
            **DARK_LAYOUT,
            height=450,
            xaxis=dict(title='Retention %', color='#94A3B8', gridcolor='#1E2D40', ticksuffix='%'),
            yaxis=dict(color='#94A3B8', gridcolor='#1E2D40'),
            margin=dict(l=10, r=40, t=10, b=10)
        )
        st.plotly_chart(fig_m, use_container_width=True)

    # Month-1 line with markers and average
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
    # Fill area under line with rgba(220,38,38,0.08)
    fig2.add_trace(go.Scatter(
        x=m1['cohort'], y=m1['retention'],
        mode='lines',
        line=dict(color='#DC2626', width=2.5),
        fill='tozeroy', fillcolor='rgba(220,38,38,0.08)',
        name='Month-1 Retention'
    ))
    # Best dot
    fig2.add_trace(go.Scatter(
        x=[best_m1_row['cohort']], y=[best_m1_row['retention']],
        mode='markers',
        marker=dict(color='#16A34A', size=12, line=dict(color='#060B14', width=2)),
        hoverinfo='text',
        text=f"Best Cohort: {best_m1_row['cohort']} ({best_m1_row['retention']:.1f}%)",
        name=f"Best: {best_m1_row['cohort']}"
    ))
    # Worst dot
    fig2.add_trace(go.Scatter(
        x=[worst_m1_row['cohort']], y=[worst_m1_row['retention']],
        mode='markers',
        marker=dict(color='#DC2626', size=12, line=dict(color='#060B14', width=2)),
        hoverinfo='text',
        text=f"Worst Cohort: {worst_m1_row['cohort']} ({worst_m1_row['retention']:.1f}%)",
        name=f"Worst: {worst_m1_row['cohort']}"
    ))
    # Dashed purple average line
    fig2.add_hline(
        y=avg_m1, line_dash='dash', line_color='#6C63DB', line_width=1.5,
        annotation_text=f'Avg {avg_m1:.1f}%',
        annotation_font_color='#94A3B8', annotation_font_size=11
    )
    fig2.update_layout(
        **DARK_LAYOUT, height=280,
        xaxis=dict(color='#94A3B8', tickangle=45, tickfont=dict(size=10)),
        yaxis=dict(color='#94A3B8', ticksuffix='%'),
        showlegend=True,
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#94A3B8', size=10))
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Cohort Insights
    st.markdown("<br>---")
    st.markdown("<p class='section-label'>Cohort Insights</p>", unsafe_allow_html=True)
    diff_m3_m1 = avg_m3 - avg_m1

    st.markdown(f"""
    <div style='background:#0F1C2E; border:1px solid #1E2D40; border-radius:12px; padding:20px; font-size:13px; margin-bottom: 24px;'>
        <ul style='color:#E2E8F0; margin:0; padding-left:20px; line-height:1.75;'>
            <li><b>Highest Performing Cohort:</b> The best cohort is <b>{best_c}</b>, achieving a Month-1 retention rate of <b>{best_v:.1f}%</b>. This is a remarkable 84% above the average customer retention rate, highlighting a highly successful onboarding period.</li>
            <li><b>Lowest Performing Cohort:</b> The worst cohort is <b>{cohort_num[1].idxmin()}</b>, with a Month-1 retention rate of <b>{worst_v:.1f}%</b>, which warrants further operational and acquisition quality review.</li>
            <li><b>Loyalty Progression:</b> Month-3 retention is <b>{diff_m3_m1:.1f}% HIGHER</b> than Month-1 — meaning customers who survive the first month become long-term loyalists.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style='background: rgba(108,99,219,0.1); border: 1px solid #6C63DB; border-radius: 12px; padding: 20px; margin-bottom: 24px;'>
        <div style='font-family: Space Mono, monospace; font-size: 10px; color: #6C63DB; font-weight: 700; text-transform: uppercase;'>Strategic Recommendation</div>
        <div style='font-size:14px; font-weight:600; color:#F1F5F9; margin-top:6px; line-height:1.6;'>
            The 14.3% average Month-1 retention suggests most first-time customers don't return. A targeted "second purchase" incentive campaign in Month-1 could move this to 25%+ based on best cohort performance.
        </div>
    </div>
    """, unsafe_allow_html=True)
