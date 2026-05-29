"""Customer Journey page — Premium "Dark Intelligence" design."""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

from config import SEGMENT_COLORS
from utils.charts import (
    apply_premium_theme, apply_premium_theme_no_axes,
    CATEGORY_COLORS_NEW, OUTCOME_COLORS, SEGMENT_SCATTER_COLORS,
    hex_to_rgba,
)


def render_customer_journey(
    sk: pd.DataFrame,
) -> None:
    """Renders Customer Journey page with premium Sankey diagram."""
    # ── CYBER HEADER ──
    st.markdown("""
    <div style="padding: 24px 0 16px; animation: fadeIn 0.8s ease;">
      <div style="display:flex; align-items:center; gap:14px; margin-bottom:12px;">
        <div style="
          width:44px; height:44px;
          background: linear-gradient(135deg, #00F5A0, #06B6D4);
          border-radius:12px;
          display:flex; align-items:center; justify-content:center;
          font-size:22px;
          box-shadow: 0 8px 24px rgba(6,182,212,0.3);
        ">🌊</div>
        <div>
          <div class="stat-badge" style="margin:0; background:rgba(6,182,212,0.15); border-color:rgba(6,182,212,0.35); color:#22D3EE; box-shadow:0 0 15px rgba(6,182,212,0.15);">JOURNEY ANALYSIS</div>
          <div class="live-badge" style="margin-top:4px;">
            <span class="status-dot status-live"></span>
            Path Optimization Active
          </div>
        </div>
      </div>
      <h1 style="
        font-size:40px !important;
        font-weight:900 !important;
        letter-spacing:-0.03em !important;
        line-height:1.1 !important;
        margin:0 0 8px !important;
        background: linear-gradient(135deg, #FFFFFF 0%, #A7F3D0 50%, #60A5FA 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
      ">Customer Journey Mapping</h1>
      <p style="
        font-size:14.5px; color:#64748B;
        font-weight:400; margin:0 0 20px;
        line-height:1.6;
      ">From first purchase category → RFM segment → final outcome. Width = number of customers.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # Highlight finding cards
    c_f1, c_f2, c_f3, c_f4 = st.columns(4)
    card_data = [
        ("Highest Churn Acquisition", "Beverages-first", "24.9% Churn Rate", "#EF4444"),
        ("High Performance Acquisition", "Bakery-first", "20.1% Champion Rate", "#8B5CF6"),
        ("Overall Churn", "22.8% Churned", "Of total customer base", "#F59E0B"),
        ("High Value Base", "809 Champions", "20.8% of base", "#10B981"),
    ]
    for col, (title, value, subtitle, color) in zip([c_f1, c_f2, c_f3, c_f4], card_data):
        with col:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg,
                          rgba(13,17,23,0.9) 0%, rgba(8,12,24,0.8) 100%);
                        border: 1px solid {color}30;
                        border-radius: 16px; padding: 18px; height: 110px;
                        backdrop-filter: blur(20px);
                        position: relative; overflow: hidden;
                        transition: all 0.3s ease;'>
                <div style='position:absolute; top:0; left:0; right:0; height:2px;
                            background: {color}; opacity:0.5;'></div>
                <div style='font-size: 9px; color: {color}; font-weight: 700;
                            text-transform: uppercase; letter-spacing:0.1em;'>{title}</div>
                <div style='font-size:16px; font-weight:700; color:#F8FAFC; margin-top:6px;'>{value}</div>
                <div style='font-size:12px; color:#94A3B8; margin-top:2px;'>{subtitle}</div>
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

    CAT_C = CATEGORY_COLORS_NEW
    SEG_C = SEGMENT_SCATTER_COLORS
    OUT_C = OUTCOME_COLORS

    CAT_RGBA = {k: hex_to_rgba(v, 0.55) for k, v in CAT_C.items()}
    SEG_RGBA = {k: hex_to_rgba(v, 0.55) for k, v in SEG_C.items()}

    ls, lt, lv, lc = [], [], [], []
    for cat in categories:
        for seg in segments:
            n = len(sk[(sk['first_category'] == cat) & (sk['segment'] == seg)])
            if n > 0:
                ls.append(node_idx[cat])
                lt.append(node_idx[seg])
                lv.append(n)
                lc.append(CAT_RGBA.get(cat, 'rgba(100,100,100,0.3)'))
    for seg in segments:
        for out in outcomes:
            n = len(sk[(sk['segment'] == seg) & (sk['outcome'] == out)])
            if n > 0:
                ls.append(node_idx[seg])
                lt.append(node_idx[out])
                lv.append(n)
                lc.append(SEG_RGBA.get(seg, 'rgba(100,100,100,0.3)'))

    # Node colors
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
            line=dict(color='#050810', width=1.5),
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
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F8FAFC', size=12, family='Inter'),
        margin=dict(l=10, r=10, t=10, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Comparison Bar Chart
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
        color_discrete_map={'Champion %': '#EC4899', 'Churned %': '#EF4444'},
        labels={'Value': 'Percentage (%)', 'First Category': ''}
    )
    apply_premium_theme(fig_comp, height=350)
    fig_comp.update_layout(
        yaxis=dict(title='Percentage (%)', color='#94A3B8',
                   gridcolor='rgba(139,92,246,0.06)', ticksuffix='%'),
        xaxis=dict(color='#94A3B8', gridcolor='rgba(139,92,246,0.06)'),
        legend=dict(bgcolor='rgba(13,17,23,0.8)', font=dict(color='#94A3B8', size=11))
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
    st.markdown("<br>")
    st.markdown("---")
    st.markdown("<p class='section-label'>Key Business Insight</p>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.25);
                border-radius: 16px; padding: 22px 26px; backdrop-filter: blur(20px);'>
        <div style='font-size: 10px; color: #EF4444; font-weight: 700;
                    text-transform: uppercase; letter-spacing:0.1em;'>Strategic Recommendation</div>
        <div style='font-size:14px; font-weight:500; color:#F8FAFC; margin-top:8px; line-height:1.6;'>
            Customers who first purchase Beverages churn at 24.9% — the highest of any category.
            This suggests promotional pricing on beverages attracts low-LTV customers.
            Recommendation: shift acquisition spend toward Fresh Produce and Bakery categories
            which produce proportionally more Champions.
        </div>
    </div>
    """, unsafe_allow_html=True)
