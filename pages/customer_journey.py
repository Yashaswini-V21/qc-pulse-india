"""
Customer Journey page - Sankey diagram of customer flow.

Purpose:
  Visualize customer journey from first product category through RFM segment
  to final outcome (Retained/Churned/Retained High-Value).

Data Used:
  - sankey_df (customer journey data with first category, segment, outcome)
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go


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
    """Render customer journey page."""
    st.title("🌊 Customer Journey Analysis")
    st.markdown("<p style='color:#64748B;font-size:14px'>First product category → RFM Segment → Final outcome. Width = number of customers.</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # KPIs
    retained_hv = len(sankey_df[sankey_df['outcome']=='Retained High-Value'])
    churned_n   = len(sankey_df[sankey_df['outcome']=='Churned'])
    retained_n  = len(sankey_df[sankey_df['outcome']=='Retained'])
    
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("Retained High-Value", f"{retained_hv:,}", f"{retained_hv/len(sankey_df)*100:.1f}% of customers")
    with c2: st.metric("Retained", f"{retained_n:,}", f"{retained_n/len(sankey_df)*100:.1f}% of customers")
    with c3: st.metric("Churned", f"{churned_n:,}", f"{churned_n/len(sankey_df)*100:.1f}% of customers")
    with c4:
        bev = sankey_df[sankey_df['first_category']=='Beverages']
        bev_churn = len(bev[bev['segment']=='Churned'])/len(bev)*100 if len(bev)>0 else 0
        st.metric("Beverages Churn Rate", f"{bev_churn:.1f}%", "highest churn category")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Sankey
    st.markdown("<p class='section-label'>Customer Flow: First Category → Segment → Outcome</p>", unsafe_allow_html=True)
    
    categories = sankey_df['first_category'].unique().tolist()
    segments   = sankey_df['segment'].unique().tolist()
    outcomes   = sankey_df['outcome'].unique().tolist()
    all_nodes  = categories + segments + outcomes
    node_idx   = {name: i for i, name in enumerate(all_nodes)}
    
    cat_colors = {
        'Dairy':'rgba(220,38,38,0.6)','Fresh Produce':'rgba(29,158,117,0.6)',
        'Bakery & Grains':'rgba(108,99,219,0.6)','Beverages':'rgba(14,165,233,0.6)',
        'Meat & Snacks':'rgba(245,158,11,0.6)','Other':'rgba(100,116,139,0.6)'
    }
    seg_colors = {
        'Champion':'rgba(220,38,38,0.6)','Loyal':'rgba(249,115,22,0.6)',
        'Potential':'rgba(108,99,219,0.6)','At-Risk':'rgba(245,158,11,0.6)',
        'Churned':'rgba(100,116,139,0.6)'
    }
    
    ls, lt, lv, lc = [], [], [], []
    for cat in categories:
        for seg in segments:
            count = len(sankey_df[(sankey_df['first_category']==cat)&(sankey_df['segment']==seg)])
            if count > 0:
                ls.append(node_idx[cat]); lt.append(node_idx[seg])
                lv.append(count); lc.append(cat_colors.get(cat,'rgba(150,150,150,0.4)'))
    for seg in segments:
        for out in outcomes:
            count = len(sankey_df[(sankey_df['segment']==seg)&(sankey_df['outcome']==out)])
            if count > 0:
                ls.append(node_idx[seg]); lt.append(node_idx[out])
                lv.append(count); lc.append(seg_colors.get(seg,'rgba(150,150,150,0.4)'))
    
    node_colors = (
        [cat_colors.get(c,'rgba(150,150,150,0.9)') for c in categories] +
        [seg_colors.get(s,'rgba(150,150,150,0.9)') for s in segments] +
        ['rgba(29,158,117,0.9)','rgba(249,115,22,0.9)','rgba(100,116,139,0.9)']
    )
    
    fig = go.Figure(data=[go.Sankey(
        arrangement='snap',
        node=dict(
            pad=20, thickness=25,
            line=dict(color='#0F172A',width=1),
            label=all_nodes, color=node_colors,
            hovertemplate='<b>%{label}</b><br>%{value} customers<extra></extra>'
        ),
        link=dict(
            source=ls, target=lt, value=lv, color=lc,
            hovertemplate='%{source.label} → %{target.label}<br>%{value} customers<extra></extra>'
        )
    )])
    fig.update_layout(
        height=600, paper_bgcolor='#1E293B',
        font=dict(color='white',size=12),
        margin=dict(l=0,r=0,t=10,b=0)
    )
    st.plotly_chart(fig, width='stretch')
    
    # Category insights table
    st.markdown("---")
    st.markdown("<p class='section-label'>Champion vs Churn Rate by First Category</p>", unsafe_allow_html=True)
    rows = []
    for cat in sankey_df['first_category'].value_counts().index:
        sub = sankey_df[sankey_df['first_category']==cat]
        rows.append({
            'First Category': cat,
            'Customers': len(sub),
            'Champion %': f"{len(sub[sub['segment']=='Champion'])/len(sub)*100:.1f}%",
            'Churned %':  f"{len(sub[sub['segment']=='Churned'])/len(sub)*100:.1f}%",
            'Best Outcome': 'Beverages avoid' if cat=='Beverages' else '✅ Good'
        })
    st.dataframe(pd.DataFrame(rows), width='stretch', hide_index=True)
