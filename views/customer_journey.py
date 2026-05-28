import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any
from config import SEGMENT_COLORS

def render_customer_journey(
    sk: pd.DataFrame,
    DARK_LAYOUT: Dict[str, Any]
) -> None:
    """
    Renders modular Customer Journey page for QC Pulse India.
    """
    st.markdown("<span class='stat-badge'>JOURNEY ANALYSIS</span>", unsafe_allow_html=True)
    st.title("Customer Journey Mapping")
    st.markdown("<p style='color:#475569;font-size:14px;margin-top:-8px'>From first purchase category → RFM segment → final outcome. Width = number of customers.</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Highlight finding cards above the Sankey
    c_f1, c_f2, c_f3, c_f4 = st.columns(4)
    with c_f1:
        st.markdown("""
        <div style='background: rgba(220,38,38,0.1); border: 1px solid #DC2626; border-radius: 12px; padding: 16px; height: 100px;'>
            <div style='font-family: Space Mono, monospace; font-size: 9px; color: #DC2626; font-weight: 700; text-transform: uppercase;'>Highest Churn Acquisition</div>
            <div style='font-size:16px; font-weight:700; color:#F1F5F9; margin-top:4px;'>Beverages-first</div>
            <div style='font-size:12px; color:#94A3B8; margin-top:2px;'>24.9% Churn Rate</div>
        </div>
        """, unsafe_allow_html=True)
    with c_f2:
        st.markdown("""
        <div style='background: rgba(108,99,219,0.1); border: 1px solid #6C63DB; border-radius: 12px; padding: 16px; height: 100px;'>
            <div style='font-family: Space Mono, monospace; font-size: 9px; color: #6C63DB; font-weight: 700; text-transform: uppercase;'>High Performance Acquisition</div>
            <div style='font-size:16px; font-weight:700; color:#F1F5F9; margin-top:4px;'>Bakery-first</div>
            <div style='font-size:12px; color:#94A3B8; margin-top:2px;'>20.1% Champion Rate</div>
        </div>
        """, unsafe_allow_html=True)
    with c_f3:
        st.markdown("""
        <div style='background: rgba(245,158,11,0.1); border: 1px solid #F59E0B; border-radius: 12px; padding: 16px; height: 100px;'>
            <div style='font-family: Space Mono, monospace; font-size: 9px; color: #F59E0B; font-weight: 700; text-transform: uppercase;'>Overall Churn</div>
            <div style='font-size:16px; font-weight:700; color:#F1F5F9; margin-top:4px;'>22.8% Churned</div>
            <div style='font-size:12px; color:#94A3B8; margin-top:2px;'>Of total customer base</div>
        </div>
        """, unsafe_allow_html=True)
    with c_f4:
        st.markdown("""
        <div style='background: rgba(29,158,117,0.1); border: 1px solid #1D9E75; border-radius: 12px; padding: 16px; height: 100px;'>
            <div style='font-family: Space Mono, monospace; font-size: 9px; color: #1D9E75; font-weight: 700; text-transform: uppercase;'>High Value Base</div>
            <div style='font-size:16px; font-weight:700; color:#F1F5F9; margin-top:4px;'>809 Champions</div>
            <div style='font-size:12px; color:#94A3B8; margin-top:2px;'>20.8% of base</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Build Sankey
    st.markdown("<p class='section-label'>Flow: First Category → Segment → Outcome</p>", unsafe_allow_html=True)

    categories = sk['first_category'].unique().tolist()
    segments   = sk['segment'].unique().tolist()
    outcomes   = sk['outcome'].unique().tolist()
    all_nodes  = categories + segments + outcomes
    node_idx   = {n: i for i, n in enumerate(all_nodes)}

    # Custom colors
    CAT_C = {
        'Dairy': '#DC2626',
        'Fresh Produce': '#1D9E75',
        'Bakery & Grains': '#6C63DB',
        'Beverages': '#0EA5E9',
        'Meat & Snacks': '#F59E0B',
        'Other': '#475569'
    }
    SEG_C = SEGMENT_COLORS
    OUT_C = {
        'Retained High-Value': '#1D9E75',
        'Retained': '#F97316',
        'Churned': '#475569'
    }

    # Helper to convert hex to rgba
    def hex_to_rgba(hex_str, opacity=0.65):
        hex_str = hex_str.lstrip('#')
        r = int(hex_str[0:2], 16)
        g = int(hex_str[2:4], 16)
        b = int(hex_str[4:6], 16)
        return f"rgba({r},{g},{b},{opacity})"

    CAT_RGBA = {k: hex_to_rgba(v, 0.65) for k, v in CAT_C.items()}
    SEG_RGBA = {k: hex_to_rgba(v, 0.65) for k, v in SEG_C.items()}

    ls, lt, lv, lc = [], [], [], []
    for cat in categories:
        for seg in segments:
            n = len(sk[(sk['first_category'] == cat) & (sk['segment'] == seg)])
            if n > 0:
                ls.append(node_idx[cat])
                lt.append(node_idx[seg])
                lv.append(n)
                lc.append(CAT_RGBA.get(cat, 'rgba(100,100,100,0.4)'))
    for seg in segments:
        for out in outcomes:
            n = len(sk[(sk['segment'] == seg) & (sk['outcome'] == out)])
            if n > 0:
                ls.append(node_idx[seg])
                lt.append(node_idx[out])
                lv.append(n)
                lc.append(SEG_RGBA.get(seg, 'rgba(100,100,100,0.4)'))

    # Node colors compilation:
    node_colors = []
    for n in all_nodes:
        if n in CAT_C:
            node_colors.append(CAT_C[n])
        elif n in SEG_C:
            node_colors.append(SEG_C[n])
        elif n in OUT_C:
            node_colors.append(OUT_C[n])
        else:
            node_colors.append('#94A3B8')

    fig = go.Figure(data=[go.Sankey(
        arrangement='snap',
        node=dict(
            pad=22, thickness=28,
            line=dict(color='#060B14', width=1.5),
            label=all_nodes, color=node_colors,
            hovertemplate='<b>%{label}</b><br>%{value:,} customers<extra></extra>'
        ),
        link=dict(
            source=ls, target=lt, value=lv, color=lc,
            hovertemplate='%{source.label} → %{target.label}<br><b>%{value:,}</b> customers<extra></extra>'
        )
    )])
    fig.update_layout(
        height=620,
        paper_bgcolor='#0D1823',
        font=dict(color='#E2E8F0', size=12, family='DM Sans'),
        margin=dict(l=10, r=10, t=10, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Comparison Bar Chart Champion % vs Churned %
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p class='section-label'>Champion vs. Churn Rate by First Category</p>", unsafe_allow_html=True)
    bar_rows = []
    for cat in sk['first_category'].value_counts().index:
        sub = sk[sk['first_category'] == cat]
        champ_p = len(sub[sub['segment'] == 'Champion']) / len(sub) * 100
        churn_p = len(sub[sub['segment'] == 'Churned'])  / len(sub) * 100
        bar_rows.append({'First Category': cat, 'Metric': 'Champion %', 'Value': champ_p})
        bar_rows.append({'First Category': cat, 'Metric': 'Churned %', 'Value': churn_p})

    fig_comp = px.bar(
        pd.DataFrame(bar_rows),
        x='First Category', y='Value', color='Metric',
        barmode='group',
        color_discrete_map={'Champion %': '#1D9E75', 'Churned %': '#DC2626'},
        labels={'Value': 'Percentage (%)', 'First Category': ''}
    )
    fig_comp.update_layout(
        **DARK_LAYOUT, height=350,
        yaxis=dict(title='Percentage (%)', color='#94A3B8', gridcolor='#1E2D40', ticksuffix='%'),
        xaxis=dict(color='#94A3B8', gridcolor='#1E2D40'),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#94A3B8', size=11))
    )
    st.plotly_chart(fig_comp, use_container_width=True)

    # Category table
    st.markdown("---")
    st.markdown("<p class='section-label'>Champion vs Churn Rate — by First Purchase Category Details</p>", unsafe_allow_html=True)
    rows = []
    for cat in sk['first_category'].value_counts().index:
        sub = sk[sk['first_category'] == cat]
        champ_p = len(sub[sub['segment'] == 'Champion']) / len(sub) * 100
        churn_p = len(sub[sub['segment'] == 'Churned'])  / len(sub) * 100
        rows.append({
            'First Category': cat,
            'Customers': f"{len(sub):,}",
            'Champion %': f"{champ_p:.1f}%",
            'Churned %':  f"{churn_p:.1f}%",
            'Signal': '🔴 Avoid for acquisition' if cat == 'Beverages' else '✅ Good acquisition'
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # Key Business Insight
    st.markdown("<br>---")
    st.markdown("<p class='section-label'>Key Business Insight</p>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background: rgba(127, 29, 29, 0.2); border: 1px solid #7F1D1D; border-radius: 12px; padding: 20px;'>
        <div style='font-family: Space Mono, monospace; font-size: 10px; color: #DC2626; font-weight: 700; text-transform: uppercase;'>Strategic Recommendation</div>
        <div style='font-size:14px; font-weight:600; color:#F1F5F9; margin-top:6px; line-height:1.6;'>
            Customers who first purchase Beverages churn at 24.9% — the highest of any category. This suggests promotional pricing on beverages attracts low-LTV customers. Recommendation: shift acquisition spend toward Fresh Produce and Bakery categories which produce proportionally more Champions.
        </div>
    </div>
    """, unsafe_allow_html=True)
