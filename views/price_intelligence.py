"""Price Intelligence page — Premium "Dark Intelligence" design."""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import logging
from config import PLATFORM_COLORS
from utils.charts import (
    apply_premium_theme, apply_premium_theme_no_axes,
    PRICE_GAP_COLORSCALE, BAR_COLOR, hex_to_rgba
)

logger = logging.getLogger(__name__)


def _format_scorecard_cell(platform: str, val: float, winner_platform: str) -> str:
    """Format scorecard cells with winner highlight."""
    if platform == winner_platform:
        return f"<span style='color:#A78BFA;font-weight:700'>{val:.0f} 🥇</span>"
    return f"<span style='color:#64748B'>{val:.0f}</span>"


def render_price_intelligence(
    bl: pd.DataFrame,
    ze: pd.DataFrame,
    bb: pd.DataFrame,
    pm: pd.DataFrame,
) -> None:
    """Renders Price Intelligence page with premium design."""
    # ── CYBER HEADER ──
    st.markdown("""
    <div style="padding: 24px 0 16px; animation: fadeIn 0.8s ease;">
      <div style="display:flex; align-items:center; gap:14px; margin-bottom:12px;">
        <div style="
          width:44px; height:44px;
          background: linear-gradient(135deg, #8B5CF6, #F43F5E);
          border-radius:12px;
          display:flex; align-items:center; justify-content:center;
          font-size:22px;
          box-shadow: 0 8px 24px rgba(139,92,246,0.3);
        ">⚔️</div>
        <div>
          <div class="stat-badge" style="margin:0;">COMPETITIVE INTEL</div>
          <div class="live-badge" style="margin-top:4px;">
            <span class="status-dot status-live"></span>
            Price War Matrix Active
          </div>
        </div>
      </div>
      <h1 style="
        font-size:40px !important;
        font-weight:900 !important;
        letter-spacing:-0.03em !important;
        line-height:1.1 !important;
        margin:0 0 8px !important;
        background: linear-gradient(135deg, #FFFFFF 0%, #C4B5FD 50%, #93C5FD 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
      ">Price Intelligence Matrix</h1>
      <p style="
        font-size:14.5px; color:#64748B;
        font-weight:400; margin:0 0 20px;
        line-height:1.6;
      ">Who wins the price war? Blinkit vs Zepto vs BigBasket — category by category.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # ── 🏆 COMPETITIVE SCORECARD ──
    st.markdown("<p class='section-label'>🏆 Platform Competitive Scorecard 2026</p>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#475569;font-size:13px;margin-bottom:20px'>"
        "Scoring all 3 platforms across 4 dimensions: Price Competitiveness, "
        "Catalog Depth, Discount Aggressiveness, and Category Coverage.</p>",
        unsafe_allow_html=True
    )

    try:
        from utils.simulator import calculate_platform_scores
        scores = calculate_platform_scores(bl, ze, bb, pm)

        categories_radar = ['Price<br>Competitiveness', 'Catalog<br>Depth',
                            'Discount<br>Aggressiveness', 'Category<br>Coverage']
        fill_colors = {p: hex_to_rgba(c, 0.12) for p, c in PLATFORM_COLORS.items()}

        fig_radar = go.Figure()
        for pname in ['Blinkit', 'Zepto', 'BigBasket']:
            s = scores[pname]
            vals = [s['price_score'], s['depth_score'], s['discount_score'], s['coverage_score']]
            vals_c = vals + [vals[0]]
            cats_c = categories_radar + [categories_radar[0]]
            fig_radar.add_trace(go.Scatterpolar(
                r=vals_c, theta=cats_c, fill='toself',
                fillcolor=fill_colors[pname],
                line=dict(color=PLATFORM_COLORS[pname], width=2.5),
                name=pname,
                hovertemplate=f'<b>{pname}</b><br>%{{theta}}: %{{r:.1f}}/100<extra></extra>'
            ))

        fig_radar.update_layout(
            polar=dict(
                bgcolor='rgba(13,17,23,0.4)',
                radialaxis=dict(visible=True, range=[0, 100], color='#475569',
                                gridcolor='rgba(139,92,246,0.06)',
                                tickfont=dict(size=9, color='#475569')),
                angularaxis=dict(color='#94A3B8',
                                 gridcolor='rgba(139,92,246,0.06)',
                                 linecolor='rgba(139,92,246,0.1)',
                                 tickfont=dict(size=11, color='#94A3B8'))
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#94A3B8', family='Inter'),
            legend=dict(bgcolor='rgba(13,17,23,0.8)', font=dict(color='#94A3B8', size=12),
                        bordercolor='rgba(139,92,246,0.2)', borderwidth=1,
                        orientation='h', x=0.5, xanchor='center', y=-0.12),
            margin=dict(l=50, r=50, t=30, b=60), height=380,
            hoverlabel=dict(
                bgcolor='rgba(13,17,23,0.95)',
                bordercolor='rgba(139,92,246,0.3)',
                font=dict(color='#F8FAFC', size=12, family='Inter'),
            ),
        )

        col_radar, col_table = st.columns([1, 1.2])

        with col_radar:
            st.plotly_chart(fig_radar, use_container_width=True)

        with col_table:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div style='grid-template-columns:1.6fr 1fr 1fr 1fr;
                        display:grid; gap:8px;padding:4px 12px;font-size:10px;color:#475569;
                        font-weight:700; letter-spacing:0.1em; text-transform:uppercase;
                        margin-bottom:4px'>
                <div>METRIC</div>
                <div style='color:#FF3366'>BLINKIT</div>
                <div style='color:#00F5A0'>ZEPTO</div>
                <div style='color:#B923FF'>BIGBASKET</div>
            </div>""", unsafe_allow_html=True)

            metrics_rows = [
                ("Price Competitiveness", "price_score"),
                ("Catalog Depth",         "depth_score"),
                ("Discount Aggression",   "discount_score"),
                ("Category Coverage",     "coverage_score"),
                ("Overall Score",         "overall_score"),
            ]
            for mlabel, mkey in metrics_rows:
                bl_v = scores['Blinkit'][mkey]
                ze_v = scores['Zepto'][mkey]
                bb_v = scores['BigBasket'][mkey]
                winner = max(['Blinkit', 'Zepto', 'BigBasket'], key=lambda p: scores[p][mkey])
                is_total = mlabel == "Overall Score"
                st.markdown(f"""
                <div style='display:grid;grid-template-columns:1.6fr 1fr 1fr 1fr;
                            gap:8px;padding:8px 12px;margin-bottom:4px;
                            background:{"rgba(139,92,246,0.08)" if is_total else "rgba(13,17,23,0.6)"};
                            border:1px solid {"rgba(139,92,246,0.25)" if is_total else "rgba(139,92,246,0.08)"};
                            border-radius:10px;font-size:12px;'>
                    <div style='color:#94A3B8;font-weight:{"700" if is_total else "400"}'>{mlabel}</div>
                    {_format_scorecard_cell("Blinkit", bl_v, winner)}
                    {_format_scorecard_cell("Zepto", ze_v, winner)}
                    {_format_scorecard_cell("BigBasket", bb_v, winner)}
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        price_leader = max(['Blinkit', 'Zepto', 'BigBasket'], key=lambda p: scores[p]['price_score'])
        depth_leader = max(['Blinkit', 'Zepto', 'BigBasket'], key=lambda p: scores[p]['depth_score'])
        disc_leader  = max(['Blinkit', 'Zepto', 'BigBasket'], key=lambda p: scores[p]['discount_score'])
        depth_cnt = scores[depth_leader]['product_count']
        disc_avg  = scores[disc_leader]['avg_discount']
        n_cats_pm = len(pm)

        st.markdown(f"""
        <div class='glass-card' style='border-left: 3px solid #8B5CF6;
                    border-radius: 0 20px 20px 0; margin-bottom: 24px;'>
            <div style='font-size: 10px; color: #8B5CF6;
                        font-weight: 700; text-transform: uppercase; letter-spacing:.12em;
                        margin-bottom: 10px;'>📊 Intelligence Summary</div>
            <ul style='color: #CBD5E1; font-size: 13px; line-height: 1.8; margin: 0; padding-left: 20px;'>
                <li><b>{price_leader}</b> leads price competitiveness in
                    <b>{scores[price_leader]["price_wins"]} of {n_cats_pm}</b> categories —
                    the clearest value signal for price-sensitive consumers.</li>
                <li><b>{depth_leader}</b> dominates catalog depth with
                    <b>{depth_cnt:,} products</b> ({round(scores[depth_leader]["depth_score"])}% of max catalogue size).</li>
                <li><b>{disc_leader}</b> shows the strongest discount strategy at
                    <b>{disc_avg:.1f}% average discount</b> — the most aggressive value proposition of the three.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

    except Exception as _sc_err:
        logger.warning(f"Scorecard failed: {_sc_err}")
        st.warning(f"⚠️ Scorecard requires all platform data. ({_sc_err})")
        st.markdown("---")

    # Dynamic price gap alert
    _gap_cols = {col: col.replace('_gap%', '') for col in pm.columns if '_gap%' in col}
    _max_gap_val = 0.0
    _max_gap_platform = "Zepto"
    _max_gap_category = "Beverages"
    for _, _row in pm.iterrows():
        for _gcol, _gplat in _gap_cols.items():
            _v = _row.get(_gcol)
            if not pd.isna(_v) and abs(float(_v)) > abs(_max_gap_val):
                _max_gap_val = float(_v)
                _max_gap_platform = _gplat
                _max_gap_category = str(_row['category'])

    _gap_dir = "overprices" if _max_gap_val > 0 else "underprices"
    _alert_icon = "📈" if _max_gap_val > 0 else "📉"
    st.markdown(f"""
    <div style='background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.3);
                border-radius: 16px; padding: 18px 24px; margin-bottom: 24px;
                backdrop-filter: blur(20px);'>
        <div style='display:flex; align-items:center; gap:12px;'>
            <span style='font-size:24px;'>{_alert_icon}</span>
            <div>
                <div style='font-size:10px; color:#EF4444; font-weight:700;
                            text-transform:uppercase; letter-spacing:0.1em;'>Pricing Disparity Alert</div>
                <div style='font-size:15px; font-weight:600; color:#F8FAFC; margin-top:2px;'>
                    {_max_gap_platform} {_gap_dir} <b>{_max_gap_category}</b> by
                    <span style='color:#EF4444; font-weight:700;'>{abs(_max_gap_val):.1f}%</span>
                    vs market average — the largest price gap in the dataset.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Platforms Compared", "3", "Blinkit · Zepto · BigBasket")
    with c2:
        st.metric("Categories", str(len(pm)), "master categories")
    with c3:
        zd = ze['discount_pct'].median() if 'discount_pct' in ze.columns else 0
        st.metric("Zepto Median Discount", f"{zd:.0f}%", "most aggressive")
    with c4:
        bd = bb['discount_pct'].median() if 'discount_pct' in bb.columns else 0
        st.metric("BigBasket Median Discount", f"{bd:.0f}%", "vs market avg")

    st.markdown("<br>", unsafe_allow_html=True)

    # Heatmap
    st.markdown("<p class='section-label'>Price Gap Matrix — % vs Market Average</p>", unsafe_allow_html=True)
    gap_cols = [c for c in pm.columns if '_gap%' in c]
    if gap_cols:
        gd = pm[['category'] + gap_cols].dropna().copy()
        gd.columns = ['Category'] + [c.replace('_gap%', '') for c in gap_cols]

        text_matrix = [[f"<b>{v:+.1f}%</b>" for v in row] for row in gd.iloc[:, 1:].values]

        fig = go.Figure(data=go.Heatmap(
            z=gd.iloc[:, 1:].values,
            x=gd.columns[1:].tolist(),
            y=gd['Category'].tolist(),
            colorscale=PRICE_GAP_COLORSCALE,
            zmid=0,
            text=text_matrix,
            texttemplate='%{text}',
            textfont=dict(size=14, color='white', family='Inter'),
            colorbar=dict(
                title=dict(text='Gap %', font=dict(color='#94A3B8', size=11)),
                ticksuffix='%', tickfont=dict(color='#94A3B8'),
                bgcolor='rgba(0,0,0,0)', bordercolor='rgba(139,92,246,0.2)', borderwidth=1
            )
        ))
        apply_premium_theme_no_axes(fig, height=460)
        fig.update_layout(
            xaxis=dict(side='top', color='#94A3B8', tickfont=dict(size=13)),
            yaxis=dict(color='#94A3B8', autorange='reversed'),
            margin=dict(l=10, r=10, t=50, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

    # Winner by Category
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p class='section-label'>Platform Pricing Position by Category</p>", unsafe_allow_html=True)
    cols_win = st.columns(len(pm))
    for idx, (_, row) in enumerate(pm.iterrows()):
        cat = row['category']
        gaps = {}
        for p in ['Blinkit', 'Zepto', 'BigBasket']:
            col_name = f"{p}_gap%"
            if col_name in pm.columns and not pd.isna(row[col_name]):
                gaps[p] = row[col_name]

        cheapest = min(gaps, key=gaps.get) if gaps else None
        expensive = max(gaps, key=gaps.get) if gaps else None

        with cols_win[idx]:
            st.markdown(f"<div style='font-size:11px; font-weight:700; color:#F8FAFC; margin-bottom:8px; height:32px; line-height:1.2;'>{cat}</div>", unsafe_allow_html=True)
            for p in ['Blinkit', 'Zepto', 'BigBasket']:
                if p not in gaps:
                    st.markdown(f"""
                    <div style='background:rgba(139,92,246,0.05); border:1px solid rgba(139,92,246,0.1);
                                border-radius:99px; padding:2px 6px; font-size:10px; text-align:center;
                                color:#475569; margin-bottom:4px; font-weight:500;'>
                        {p[:2]}: N/A
                    </div>
                    """, unsafe_allow_html=True)
                elif p == cheapest:
                    st.markdown(f"""
                    <div style='background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.3);
                                border-radius:99px; padding:2px 6px; font-size:10px; text-align:center;
                                color:#6EE7B7; font-weight:700; margin-bottom:4px;'>
                        {p[:2]}: {gaps[p]:+.0f}%
                    </div>
                    """, unsafe_allow_html=True)
                elif p == expensive:
                    st.markdown(f"""
                    <div style='background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.3);
                                border-radius:99px; padding:2px 6px; font-size:10px; text-align:center;
                                color:#FCA5A5; font-weight:700; margin-bottom:4px;'>
                        {p[:2]}: {gaps[p]:+.0f}%
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='background:rgba(13,17,23,0.6); border:1px solid rgba(139,92,246,0.1);
                                border-radius:99px; padding:2px 6px; font-size:10px; text-align:center;
                                color:#94A3B8; margin-bottom:4px;'>
                        {p[:2]}: {gaps[p]:+.0f}%
                    </div>
                    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Discount charts side by side
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<p class='section-label'>Zepto — Discount % by Category</p>", unsafe_allow_html=True)
        if 'master_category' in ze.columns and 'discount_pct' in ze.columns:
            disc = ze.groupby('master_category')['discount_pct'].median().reset_index()
            disc = disc[disc['master_category'] != 'Others'].sort_values('discount_pct', ascending=True)

            fig = px.bar(
                disc, x='discount_pct', y='master_category', orientation='h',
                color_discrete_sequence=['#00F5A0'],
                text='discount_pct',
                labels={'discount_pct': 'Median Discount (%)', 'master_category': ''}
            )
            fig.update_traces(
                texttemplate='%{text:.1f}%', textposition='outside',
                textfont=dict(color='#94A3B8', size=10),
                marker_line_width=0
            )
            apply_premium_theme(fig, height=330)
            fig.update_xaxes(showgrid=False)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("<p class='section-label'>BigBasket — Discount % by Category</p>", unsafe_allow_html=True)
        if 'category' in bb.columns and 'discount_pct' in bb.columns:
            disc_bb = bb.groupby('category')['discount_pct'].median().reset_index()
            disc_bb = disc_bb.sort_values('discount_pct', ascending=True).head(7)

            fig_bb = px.bar(
                disc_bb, x='discount_pct', y='category', orientation='h',
                color_discrete_sequence=['#B923FF'],
                text='discount_pct',
                labels={'discount_pct': 'Median Discount (%)', 'category': ''}
            )
            fig_bb.update_traces(
                texttemplate='%{text:.1f}%', textposition='outside',
                textfont=dict(color='#94A3B8', size=10),
                marker_line_width=0
            )
            apply_premium_theme(fig_bb, height=330)
            fig_bb.update_xaxes(showgrid=False)
            st.plotly_chart(fig_bb, use_container_width=True)
