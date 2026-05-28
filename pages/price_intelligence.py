"""
Price Intelligence page - Competitive pricing analysis across platforms.

Purpose:
  Compare prices and discounts across Blinkit, Zepto, BigBasket by category.
  Identify pricing gaps and competitive positioning.

Data Used:
  - blinkit, zepto, bigbasket (product catalogs with prices)
  - price_mat (pre-calculated price matrix)
"""
import streamlit as st
import pandas as pd
import plotly.express as px
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
    """Render price intelligence page."""
    st.title("⚔️ Price Intelligence Matrix")
    st.markdown("<p style='color:#64748B;font-size:14px'>Who wins the price war by category? Blinkit vs Zepto vs BigBasket</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Platforms", "3", "Blinkit · Zepto · BigBasket")
    with c2:
        st.metric("Categories", str(len(price_mat)), "master categories")
    with c3:
        zepto_disc = zepto['discount_pct'].median() if 'discount_pct' in zepto.columns else 0
        st.metric("Zepto Median Discount", f"{zepto_disc:.0f}%", "highest discounter")
    with c4:
        bb_disc = bigbasket['discount_pct'].median() if 'discount_pct' in bigbasket.columns else 0
        st.metric("BigBasket Median Discount", f"{bb_disc:.0f}%", "vs market avg")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Price gap heatmap
    st.markdown("<p class='section-label'>Price Gap Matrix (% vs Market Average)</p>", unsafe_allow_html=True)
    
    gap_cols = [c for c in price_mat.columns if '_gap%' in c]
    if gap_cols:
        gap_data = price_mat[['category'] + gap_cols].copy()
        gap_data.columns = ['Category'] + [c.replace('_gap%','') for c in gap_cols]
        gap_data = gap_data.dropna()
        
        fig = go.Figure(data=go.Heatmap(
            z=gap_data.iloc[:,1:].values,
            x=gap_data.columns[1:].tolist(),
            y=gap_data['Category'].tolist(),
            colorscale='RdYlGn_r', zmid=0,
            text=[[f'{v:+.1f}%' for v in row] for row in gap_data.iloc[:,1:].values],
            texttemplate='%{text}', textfont={"size":13},
            colorbar=dict(title='Gap %', ticksuffix='%', tickfont=dict(color='white'))
        ))
        fig.update_layout(
            height=450, plot_bgcolor='#1E293B', paper_bgcolor='#1E293B',
            font=dict(color='white',size=13),
            xaxis=dict(side='top', color='white'),
            yaxis=dict(color='white'),
            margin=dict(l=0,r=0,t=40,b=0)
        )
        st.plotly_chart(fig, width='stretch')
    
    # Discount chart
    st.markdown("<p class='section-label'>Zepto Discount % by Category</p>", unsafe_allow_html=True)
    if 'master_category' in zepto.columns and 'discount_pct' in zepto.columns:
        disc = zepto.groupby('master_category')['discount_pct'].median().reset_index()
        disc = disc[disc['master_category'] != 'Others'].sort_values('discount_pct', ascending=True)
        fig2 = px.bar(
            disc, x='discount_pct', y='master_category', orientation='h',
            color='discount_pct', color_continuous_scale='Reds',
            labels={'discount_pct':'Discount %','master_category':'Category'}
        )
        fig2.update_layout(
            height=350, plot_bgcolor='#1E293B', paper_bgcolor='#1E293B',
            font=dict(color='white',size=12), coloraxis_showscale=False,
            margin=dict(l=0,r=0,t=10,b=0)
        )
        fig2.update_xaxes(color='white', gridcolor='#334155')
        fig2.update_yaxes(color='white')
        st.plotly_chart(fig2, width='stretch')
