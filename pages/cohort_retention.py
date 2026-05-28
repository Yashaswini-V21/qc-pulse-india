"""
Cohort Retention page - Customer retention analysis by cohort.

Purpose:
  Show month-by-month retention rates for each customer acquisition cohort.
  Identify high-performing cohorts and retention patterns.

Data Used:
  - cohort (cohort × month retention matrix)
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np


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
    """Render cohort retention page."""
    st.title("📈 Cohort Retention Analysis")
    st.markdown("<p style='color:#64748B;font-size:14px'>How many customers came back? Month-by-month retention across 24 cohorts.</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # KPIs
    cohort_num = cohort.copy()
    cohort_num.columns = cohort_num.columns.astype(int)
    
    avg_m1 = cohort_num[1].mean()
    avg_m3 = cohort_num[3].mean()
    best_cohort = cohort_num[1].idxmax()
    best_val    = cohort_num[1].max()
    
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("Cohorts Analysed", "24", "Jan 2014 — Dec 2015")
    with c2: st.metric("Avg Month-1 Retention", f"{avg_m1:.1f}%", "of new customers return")
    with c3: st.metric("Avg Month-3 Retention", f"{avg_m3:.1f}%", "3 months later")
    with c4: st.metric("Best Cohort", str(best_cohort), f"{best_val:.1f}% Month-1")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Heatmap
    st.markdown("<p class='section-label'>Retention Heatmap — Green = High Retention, Red = Low</p>", unsafe_allow_html=True)
    retention_plot = cohort_num.iloc[:, :13].copy()
    retention_plot.index = retention_plot.index.astype(str)
    
    fig = go.Figure(data=go.Heatmap(
        z=retention_plot.values,
        x=[f'Month {i}' for i in retention_plot.columns],
        y=retention_plot.index.tolist(),
        colorscale='RdYlGn', zmin=0, zmax=100,
        text=[[f'{v:.0f}%' if not np.isnan(v) else '' for v in row] for row in retention_plot.values],
        texttemplate='%{text}', textfont={"size":10},
        colorbar=dict(title='Retention %', ticksuffix='%', tickfont=dict(color='white'))
    ))
    fig.update_layout(
        height=560, plot_bgcolor='#1E293B', paper_bgcolor='#1E293B',
        font=dict(color='white',size=11),
        xaxis=dict(color='white'),
        yaxis=dict(color='white', autorange='reversed'),
        margin=dict(l=0,r=0,t=10,b=0)
    )
    st.plotly_chart(fig, width='stretch')
