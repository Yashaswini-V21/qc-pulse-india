import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any
from config import BLINKIT_REVIEW_CAT_MAP, BIGBASKET_REVIEW_CAT_MAP


def render_review_rating(
    bl: pd.DataFrame,
    bb: pd.DataFrame,
    DARK_LAYOUT: Dict[str, Any]
) -> None:
    """
    Renders modular Review & Rating page for QC Pulse India.
    """
    st.markdown("<span class='stat-badge'>CUSTOMER SENTIMENT</span>", unsafe_allow_html=True)
    st.title("Review & Rating Analysis")
    st.markdown("<p style='color:#475569;font-size:14px;margin-top:-8px'>Customer product ratings and feedback comparison across Blinkit and BigBasket.</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Filter out null/invalid ratings
    bb_rated = bb[bb['rating'].notna() & (bb['rating'] > 0)]
    bl_rated = bl[bl['rating'].notna() & (bl['rating'] > 0)]

    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("BigBasket Avg Rating", f"{bb_rated['rating'].mean():.2f} ★", f"Out of {len(bb_rated):,} products")
    with c2:
        st.metric("Blinkit Avg Rating", f"{bl_rated['rating'].mean():.2f} ★", f"Out of {len(bl_rated):,} products")
    with c3:
        bb_disc_rated = bb_rated['discount_pct'].mean()
        st.metric("BigBasket Rated Disc Avg", f"{bb_disc_rated:.1f}%", "discount on rated items")
    with c4:
        bb_five = len(bb_rated[bb_rated['rating'] == 5.0])
        bl_five = len(bl_rated[bl_rated['rating'] == 5.0])
        st.metric("5-Star Products Count", f"{bb_five + bl_five:,}", f"{bb_five:,} BB · {bl_five:,} Blinkit")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<p class='section-label'>Rating Distributions — BigBasket vs. Blinkit</p>", unsafe_allow_html=True)
        fig_dist = go.Figure()
        fig_dist.add_trace(go.Histogram(
            x=bb_rated['rating'],
            name='BigBasket',
            marker_color='#6C63DB',
            opacity=0.75,
            histnorm='percent',
            xbins=dict(start=1.0, end=5.0, size=0.2)
        ))
        fig_dist.add_trace(go.Histogram(
            x=bl_rated['rating'],
            name='Blinkit',
            marker_color='#DC2626',
            opacity=0.75,
            histnorm='percent',
            xbins=dict(start=1.0, end=5.0, size=0.2)
        ))
        fig_dist.update_layout(
            barmode='overlay',
            **DARK_LAYOUT,
            height=360,
            xaxis=dict(title='Rating Score', color='#94A3B8', gridcolor='#1E2D40'),
            yaxis=dict(title='Percentage of Products (%)', color='#94A3B8', gridcolor='#1E2D40'),
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#94A3B8', size=11))
        )
        st.plotly_chart(fig_dist, use_container_width=True)

    with col2:
        st.markdown("<p class='section-label'>Avg Rating by Category Comparison</p>", unsafe_allow_html=True)

        bl_rated_m = bl_rated.copy()
        bl_rated_m['Master Category'] = bl_rated_m['category'].map(BLINKIT_REVIEW_CAT_MAP).fillna('Other')

        bb_rated_m = bb_rated.copy()
        bb_rated_m['Master Category'] = bb_rated_m['category'].map(BIGBASKET_REVIEW_CAT_MAP).fillna('Other')

        bl_cat_m = bl_rated_m.groupby('Master Category')['rating'].mean().reset_index()
        bl_cat_m.columns = ['Category', 'Blinkit']

        bb_cat_m = bb_rated_m.groupby('Master Category')['rating'].mean().reset_index()
        bb_cat_m.columns = ['Category', 'BigBasket']

        cat_comp = pd.merge(bb_cat_m, bl_cat_m, on='Category', how='outer').fillna(0)

        fig_cat = go.Figure()
        fig_cat.add_trace(go.Bar(
            x=cat_comp['Category'], y=cat_comp['BigBasket'],
            name='BigBasket', marker_color='#6C63DB', marker_line_width=0
        ))
        fig_cat.add_trace(go.Bar(
            x=cat_comp['Category'], y=cat_comp['Blinkit'],
            name='Blinkit', marker_color='#DC2626', marker_line_width=0
        ))
        fig_cat.update_layout(
            barmode='group', **DARK_LAYOUT, height=360,
            yaxis=dict(title='Avg Rating ★', range=[1.0, 5.0], color='#94A3B8', gridcolor='#1E2D40'),
            xaxis=dict(color='#94A3B8', gridcolor='#1E2D40'),
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#94A3B8', size=11))
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        st.markdown("<p class='section-label'>BigBasket — Discount vs. Customer Rating Relationship</p>", unsafe_allow_html=True)
        bb_rated['discount_bin'] = pd.cut(bb_rated['discount_pct'], bins=[-1, 0, 10, 20, 30, 40, 50, 100],
                                         labels=['No Discount', '1-10%', '11-20%', '21-30%', '31-40%', '41-50%', '50%+'])
        disc_rel = bb_rated.groupby('discount_bin', observed=False)['rating'].agg(['mean', 'count']).reset_index()
        disc_rel = disc_rel[disc_rel['count'] > 5]

        fig_disc = px.line(
            disc_rel, x='discount_bin', y='mean',
            markers=True,
            labels={'discount_bin': 'Discount Bracket', 'mean': 'Average Rating ★'},
            color_discrete_sequence=['#F59E0B']
        )
        fig_disc.update_traces(
            line=dict(width=3),
            marker=dict(size=10, line=dict(color='#060B14', width=2))
        )
        fig_disc.update_layout(
            **DARK_LAYOUT, height=320,
            xaxis=dict(color='#94A3B8', gridcolor='#1E2D40'),
            yaxis=dict(title='Avg Rating ★', range=[3.5, 4.8], color='#94A3B8', gridcolor='#1E2D40')
        )
        st.plotly_chart(fig_disc, use_container_width=True)

    with col_right:
        st.markdown("<p class='section-label'>Interactive Brand Rating Explorer</p>", unsafe_allow_html=True)
        top_brands = bb_rated['brand'].value_counts().head(50).index.tolist()
        selected_brand = st.selectbox("Select Brand to Explore", sorted(top_brands), index=0)

        brand_df = bb_rated[bb_rated['brand'] == selected_brand]
        brand_avg_rating = brand_df['rating'].mean()
        brand_avg_disc = brand_df['discount_pct'].mean()

        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #0F1C2E 0%, #0D1823 100%);
                    border: 1px solid #1E2D40; border-radius: 12px; padding: 24px; margin-top: 10px;'>
            <div style='font-family:Space Mono,monospace; font-size:11px; color:#F59E0B; font-weight:700; text-transform:uppercase;'>Brand Insights</div>
            <div style='font-size:20px; font-weight:700; color:#F1F5F9; margin: 4px 0 16px 0;'>{selected_brand}</div>
            <div style='display:flex; justify-content:space-between; margin-bottom:12px; border-bottom:1px solid #1E2D40; padding-bottom:10px;'>
                <span style='color:#94A3B8; font-size:13px;'>Average Rating</span>
                <span style='color:#F1F5F9; font-weight:700; font-size:14px;'>{brand_avg_rating:.2f} ★</span>
            </div>
            <div style='display:flex; justify-content:space-between; margin-bottom:12px; border-bottom:1px solid #1E2D40; padding-bottom:10px;'>
                <span style='color:#94A3B8; font-size:13px;'>Average Discount</span>
                <span style='color:#F1F5F9; font-weight:700; font-size:14px;'>{brand_avg_disc:.1f}%</span>
            </div>
            <div style='display:flex; justify-content:space-between; margin-bottom:4px;'>
                <span style='color:#94A3B8; font-size:13px;'>Total Rated Products</span>
                <span style='color:#F1F5F9; font-weight:700; font-size:14px;'>{len(brand_df)}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
