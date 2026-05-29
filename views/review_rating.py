"""Review & Rating page — Premium "Dark Intelligence" design."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import BLINKIT_REVIEW_CAT_MAP, BIGBASKET_REVIEW_CAT_MAP
from utils.charts import apply_premium_theme, BAR_COLOR


def render_review_rating(
    bl: pd.DataFrame,
    bb: pd.DataFrame,
) -> None:
    """Renders Review & Rating page with premium design."""
    # ── CYBER HEADER ──
    st.markdown("""
    <div style="padding: 24px 0 16px; animation: fadeIn 0.8s ease;">
      <div style="display:flex; align-items:center; gap:14px; margin-bottom:12px;">
        <div style="
          width:44px; height:44px;
          background: linear-gradient(135deg, #F59E0B, #EF4444);
          border-radius:12px;
          display:flex; align-items:center; justify-content:center;
          font-size:22px;
          box-shadow: 0 8px 24px rgba(245,158,11,0.3);
        ">⭐</div>
        <div>
          <div class="stat-badge" style="margin:0; background:rgba(245,158,11,0.15); border-color:rgba(245,158,11,0.35); color:#F59E0B; box-shadow:0 0 15px rgba(245,158,11,0.15);">CUSTOMER SENTIMENT</div>
          <div class="live-badge" style="margin-top:4px;">
            <span class="status-dot status-live"></span>
            Sentiment Analysis Engine Active
          </div>
        </div>
      </div>
      <h1 style="
        font-size:40px !important;
        font-weight:900 !important;
        letter-spacing:-0.03em !important;
        line-height:1.1 !important;
        margin:0 0 8px !important;
        background: linear-gradient(135deg, #FFFFFF 0%, #FDE68A 50%, #F59E0B 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
      ">Review & Rating Analysis</h1>
      <p style="
        font-size:14.5px; color:#64748B;
        font-weight:400; margin:0 0 20px;
        line-height:1.6;
      ">Customer product ratings and feedback comparison across Blinkit and BigBasket.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # Filter out null/invalid ratings
    bb_rated = bb[bb['rating'].notna() & (bb['rating'] > 0)].copy()
    bl_rated = bl[bl['rating'].notna() & (bl['rating'] > 0)].copy()

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
            marker_color='#B923FF',
            opacity=0.75,
            histnorm='percent',
            xbins=dict(start=1.0, end=5.0, size=0.2)
        ))
        fig_dist.add_trace(go.Histogram(
            x=bl_rated['rating'],
            name='Blinkit',
            marker_color='#FF3366',
            opacity=0.75,
            histnorm='percent',
            xbins=dict(start=1.0, end=5.0, size=0.2)
        ))
        fig_dist.update_layout(barmode='overlay')
        apply_premium_theme(fig_dist, height=360)
        fig_dist.update_layout(
            xaxis=dict(title='Rating Score', color='#94A3B8',
                       gridcolor='rgba(139,92,246,0.06)'),
            yaxis=dict(title='Percentage of Products (%)', color='#94A3B8',
                       gridcolor='rgba(139,92,246,0.06)'),
            legend=dict(bgcolor='rgba(13,17,23,0.8)', font=dict(color='#94A3B8', size=11))
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
            name='BigBasket', marker_color='#B923FF', marker_line_width=0
        ))
        fig_cat.add_trace(go.Bar(
            x=cat_comp['Category'], y=cat_comp['Blinkit'],
            name='Blinkit', marker_color='#FF3366', marker_line_width=0
        ))
        fig_cat.update_layout(barmode='group')
        apply_premium_theme(fig_cat, height=360)
        fig_cat.update_layout(
            yaxis=dict(title='Avg Rating ★', range=[1.0, 5.0], color='#94A3B8',
                       gridcolor='rgba(139,92,246,0.06)'),
            xaxis=dict(color='#94A3B8', gridcolor='rgba(139,92,246,0.06)'),
            legend=dict(bgcolor='rgba(13,17,23,0.8)', font=dict(color='#94A3B8', size=11))
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
            marker=dict(size=10, line=dict(color='#050810', width=2))
        )
        apply_premium_theme(fig_disc, height=320)
        fig_disc.update_layout(
            xaxis=dict(color='#94A3B8', gridcolor='rgba(139,92,246,0.06)'),
            yaxis=dict(title='Avg Rating ★', range=[3.5, 4.8], color='#94A3B8',
                       gridcolor='rgba(139,92,246,0.06)')
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
        <div class='glass-card' style='margin-top: 10px;'>
            <div style='font-size:11px; color:#F59E0B; font-weight:700;
                        text-transform:uppercase; letter-spacing:0.08em;'>Brand Insights</div>
            <div style='font-size:20px; font-weight:800; color:#F8FAFC; margin: 4px 0 16px 0;
                        background: linear-gradient(135deg, #F8FAFC, #A78BFA);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;'>{selected_brand}</div>
            <div style='display:flex; justify-content:space-between; margin-bottom:12px;
                        border-bottom:1px solid rgba(139,92,246,0.1); padding-bottom:10px;'>
                <span style='color:#94A3B8; font-size:13px;'>Average Rating</span>
                <span style='color:#F8FAFC; font-weight:700; font-size:14px;'>{brand_avg_rating:.2f} ★</span>
            </div>
            <div style='display:flex; justify-content:space-between; margin-bottom:12px;
                        border-bottom:1px solid rgba(139,92,246,0.1); padding-bottom:10px;'>
                <span style='color:#94A3B8; font-size:13px;'>Average Discount</span>
                <span style='color:#F8FAFC; font-weight:700; font-size:14px;'>{brand_avg_disc:.1f}%</span>
            </div>
            <div style='display:flex; justify-content:space-between; margin-bottom:4px;'>
                <span style='color:#94A3B8; font-size:13px;'>Total Rated Products</span>
                <span style='color:#F8FAFC; font-weight:700; font-size:14px;'>{len(brand_df)}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
