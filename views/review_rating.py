"""Review & Rating page — Customer sentiment dashboard design."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.config import BLINKIT_REVIEW_CAT_MAP, BIGBASKET_REVIEW_CAT_MAP

# ── Design tokens ────────────────────────────────────────────
_BG       = "#060B14"
_CARD_BG  = "linear-gradient(135deg, #0F1C2E, #0D1823)"
_BORDER   = "linear-gradient(90deg, #DC2626, #7C3AED)"
_AMBER    = "#F59E0B"
_LABEL_C  = "#64748B"
_VALUE_C  = "#F1F5F9"
_PLOT_BG  = "#0D1823"
_HOVER_BG = "#0F1C2E"
_HOVER_BD = "#1E2D40"


def _kpi_card(label: str, value: str, delta: str = "") -> str:
    delta_html = ""
    if delta:
        delta_html = (
            f"<div style='font-family:\"Space Mono\",monospace;font-size:10px;"
            f"color:{_LABEL_C};margin-top:6px;'>{delta}</div>"
        )
    return f"""
    <div style="
        background: {_CARD_BG};
        border-radius: 14px;
        padding: 22px 24px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(0,0,0,0.4);
    ">
        <div style="
            position:absolute; top:0; left:0; right:0; height:2px;
            background: {_BORDER};
        "></div>
        <div style="
            font-family:'Space Mono',monospace;
            font-size:10px; text-transform:uppercase;
            color:{_LABEL_C}; letter-spacing:0.12em;
            margin-bottom:8px;
        ">{label}</div>
        <div style="
            font-family:'DM Sans',sans-serif;
            font-weight:700; font-size:30px;
            color:{_VALUE_C}; line-height:1.1;
        ">{value}</div>
        {delta_html}
    </div>
    """


def render_review_rating(
    bl: pd.DataFrame,
    bb: pd.DataFrame,
) -> None:
    """Renders Review & Rating page with customer sentiment design."""

    # ── BADGE ──
    st.markdown(f"""
    <div style="padding:28px 0 6px;">
        <span style="
            display:inline-block;
            font-family:'Space Mono',monospace;
            font-size:11px; font-weight:700;
            text-transform:uppercase; letter-spacing:0.12em;
            color:{_AMBER};
            background:rgba(245,158,11,0.1);
            border:1px solid rgba(245,158,11,0.3);
            padding:5px 14px; border-radius:99px;
        ">● CUSTOMER SENTIMENT</span>
    </div>
    """, unsafe_allow_html=True)

    # ── TITLE + SUBTITLE ──
    st.markdown(f"""
    <h1 style="
        font-family:'DM Sans',sans-serif !important;
        font-size:28px !important; font-weight:700 !important;
        color:#F1F5F9 !important;
        -webkit-text-fill-color:#F1F5F9 !important;
        background:none !important;
        margin:10px 0 6px !important;
        letter-spacing:-0.02em !important;
    ">Review & Rating Analysis</h1>
    <p style="
        font-family:'DM Sans',sans-serif;
        font-size:14px; color:{_LABEL_C};
        margin:0 0 28px;
    ">Customer product ratings and feedback comparison across Blinkit and BigBasket.</p>
    """, unsafe_allow_html=True)

    # Filter out null/invalid ratings
    bb_rated = bb[bb['rating'].notna() & (bb['rating'] > 0)].copy()
    bl_rated = bl[bl['rating'].notna() & (bl['rating'] > 0)].copy()

    # ── KPI ROW ──
    bb_avg = bb_rated['rating'].mean()
    bl_avg = bl_rated['rating'].mean()
    bb_disc_rated = bb_rated['discount_pct'].mean() if 'discount_pct' in bb_rated.columns else 0
    bb_five = len(bb_rated[bb_rated['rating'] == 5.0])
    bl_five = len(bl_rated[bl_rated['rating'] == 5.0])

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(_kpi_card("BIGBASKET AVG RATING", f"{bb_avg:.2f} ★", f"Out of {len(bb_rated):,} products"), unsafe_allow_html=True)
    with c2:
        st.markdown(_kpi_card("BLINKIT AVG RATING", f"{bl_avg:.2f} ★", f"Out of {len(bl_rated):,} products"), unsafe_allow_html=True)
    with c3:
        st.markdown(_kpi_card("BB RATED DISC AVG", f"{bb_disc_rated:.1f}%", "discount on rated items"), unsafe_allow_html=True)
    with c4:
        st.markdown(_kpi_card("5-STAR PRODUCTS", f"{bb_five + bl_five:,}", f"{bb_five:,} BB · {bl_five:,} Blinkit"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CHARTS ROW ──
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div style="font-family:'Space Mono',monospace;font-size:10px;
            text-transform:uppercase;color:{_LABEL_C};letter-spacing:0.12em;
            margin-bottom:12px;">Rating Distributions — BigBasket vs Blinkit</div>
        """, unsafe_allow_html=True)

        fig_dist = go.Figure()
        fig_dist.add_trace(go.Histogram(
            x=bb_rated['rating'], name='BigBasket',
            marker_color='#6C63DB', opacity=0.75,
            histnorm='percent', xbins=dict(start=1.0, end=5.0, size=0.2)
        ))
        fig_dist.add_trace(go.Histogram(
            x=bl_rated['rating'], name='Blinkit',
            marker_color='#DC2626', opacity=0.75,
            histnorm='percent', xbins=dict(start=1.0, end=5.0, size=0.2)
        ))
        fig_dist.update_layout(
            barmode='overlay',
            plot_bgcolor=_PLOT_BG, paper_bgcolor=_PLOT_BG,
            font=dict(family='DM Sans', color='#94A3B8', size=11),
            margin=dict(l=10, r=10, t=10, b=10), height=360,
            xaxis=dict(title='Rating Score', color='#94A3B8', gridcolor='#1E2D40'),
            yaxis=dict(title='% of Products', color='#94A3B8', gridcolor='#1E2D40'),
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#94A3B8', size=11, family='DM Sans')),
            hoverlabel=dict(bgcolor=_HOVER_BG, bordercolor=_HOVER_BD, font=dict(color='white', size=12)),
        )
        st.plotly_chart(fig_dist, use_container_width=True)

    with col2:
        st.markdown(f"""
        <div style="font-family:'Space Mono',monospace;font-size:10px;
            text-transform:uppercase;color:{_LABEL_C};letter-spacing:0.12em;
            margin-bottom:12px;">Avg Rating by Category Comparison</div>
        """, unsafe_allow_html=True)

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
            barmode='group',
            plot_bgcolor=_PLOT_BG, paper_bgcolor=_PLOT_BG,
            font=dict(family='DM Sans', color='#94A3B8', size=11),
            margin=dict(l=10, r=10, t=10, b=10), height=360,
            yaxis=dict(title='Avg Rating ★', range=[1.0, 5.0], color='#94A3B8', gridcolor='#1E2D40'),
            xaxis=dict(color='#94A3B8', gridcolor='#1E2D40'),
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#94A3B8', size=11, family='DM Sans')),
            hoverlabel=dict(bgcolor=_HOVER_BG, bordercolor=_HOVER_BD, font=dict(color='white', size=12)),
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── DISCOUNT vs RATING + BRAND EXPLORER ──
    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        st.markdown(f"""
        <div style="font-family:'Space Mono',monospace;font-size:10px;
            text-transform:uppercase;color:{_LABEL_C};letter-spacing:0.12em;
            margin-bottom:12px;">BigBasket — Discount vs Customer Rating</div>
        """, unsafe_allow_html=True)

        bb_rated['discount_bin'] = pd.cut(
            bb_rated['discount_pct'], bins=[-1, 0, 10, 20, 30, 40, 50, 100],
            labels=['No Discount', '1-10%', '11-20%', '21-30%', '31-40%', '41-50%', '50%+']
        )
        disc_rel = bb_rated.groupby('discount_bin', observed=False)['rating'].agg(['mean', 'count']).reset_index()
        disc_rel = disc_rel[disc_rel['count'] > 5]

        fig_disc = go.Figure(go.Scatter(
            x=disc_rel['discount_bin'], y=disc_rel['mean'],
            mode='lines+markers',
            line=dict(color=_AMBER, width=3),
            marker=dict(size=10, color=_AMBER, line=dict(color=_BG, width=2)),
        ))
        fig_disc.update_layout(
            plot_bgcolor=_PLOT_BG, paper_bgcolor=_PLOT_BG,
            font=dict(family='DM Sans', color='#94A3B8', size=11),
            margin=dict(l=10, r=10, t=10, b=10), height=320,
            xaxis=dict(title='Discount Bracket', color='#94A3B8', gridcolor='#1E2D40'),
            yaxis=dict(title='Avg Rating ★', range=[3.5, 4.8], color='#94A3B8', gridcolor='#1E2D40'),
            hoverlabel=dict(bgcolor=_HOVER_BG, bordercolor=_HOVER_BD, font=dict(color='white', size=12)),
        )
        st.plotly_chart(fig_disc, use_container_width=True)

    with col_right:
        st.markdown(f"""
        <div style="font-family:'Space Mono',monospace;font-size:10px;
            text-transform:uppercase;color:{_LABEL_C};letter-spacing:0.12em;
            margin-bottom:12px;">Interactive Brand Rating Explorer</div>
        """, unsafe_allow_html=True)

        top_brands = bb_rated['brand'].value_counts().head(50).index.tolist()
        selected_brand = st.selectbox("Select Brand to Explore", sorted(top_brands), index=0)

        brand_df = bb_rated[bb_rated['brand'] == selected_brand]
        brand_avg_rating = brand_df['rating'].mean()
        brand_avg_disc = brand_df['discount_pct'].mean()

        st.markdown(f"""
        <div style="
            background: {_CARD_BG};
            border: 1px solid rgba(245,158,11,0.2);
            border-radius: 14px;
            padding: 24px;
            margin-top: 10px;
        ">
            <div style="font-family:'Space Mono',monospace;font-size:10px;color:{_AMBER};
                font-weight:700;text-transform:uppercase;letter-spacing:0.08em;">Brand Insights</div>
            <div style="font-family:'DM Sans',sans-serif;font-size:20px;font-weight:700;
                color:#F1F5F9;margin:8px 0 18px;">{selected_brand}</div>
            <div style="display:flex;justify-content:space-between;margin-bottom:12px;
                border-bottom:1px solid #1E2D40;padding-bottom:10px;">
                <span style="font-family:'Space Mono',monospace;color:#94A3B8;font-size:11px;">Average Rating</span>
                <span style="font-family:'DM Sans',sans-serif;color:#F1F5F9;font-weight:700;font-size:14px;">{brand_avg_rating:.2f} ★</span>
            </div>
            <div style="display:flex;justify-content:space-between;margin-bottom:12px;
                border-bottom:1px solid #1E2D40;padding-bottom:10px;">
                <span style="font-family:'Space Mono',monospace;color:#94A3B8;font-size:11px;">Average Discount</span>
                <span style="font-family:'DM Sans',sans-serif;color:#F1F5F9;font-weight:700;font-size:14px;">{brand_avg_disc:.1f}%</span>
            </div>
            <div style="display:flex;justify-content:space-between;">
                <span style="font-family:'Space Mono',monospace;color:#94A3B8;font-size:11px;">Total Rated Products</span>
                <span style="font-family:'DM Sans',sans-serif;color:#F1F5F9;font-weight:700;font-size:14px;">{len(brand_df)}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
