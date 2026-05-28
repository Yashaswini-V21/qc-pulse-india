import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import logging
from typing import Dict, Any
from config import PLATFORM_COLORS

# Ensure proper logger configuration
logger = logging.getLogger(__name__)

def _format_scorecard_cell(platform: str, val: float, winner_platform: str) -> str:
    """
    Helper to format scorecard cells and show a medal icon for the winning platform.
    Declared at module scope to fix Python inner-loop function declaration anti-pattern.
    """
    if platform == winner_platform:
        return f"<span style='color:#1D9E75;font-weight:700'>{val:.0f} 🥇</span>"
    return f"<span style='color:#64748B'>{val:.0f}</span>"

def render_price_intelligence(
    bl: pd.DataFrame,
    ze: pd.DataFrame,
    bb: pd.DataFrame,
    pm: pd.DataFrame,
    DARK_LAYOUT: Dict[str, Any]
) -> None:
    """
    Renders modular Price Intelligence page for QC Pulse India.
    """
    st.markdown("<span class='stat-badge'>COMPETITIVE INTEL</span>", unsafe_allow_html=True)
    st.title("Price Intelligence Matrix")
    st.markdown("<p style='color:#475569;font-size:14px;margin-top:-8px'>Who wins the price war? Blinkit vs Zepto vs BigBasket — category by category.</p>", unsafe_allow_html=True)
    st.markdown("---")

    # ── 🏆 COMPETITIVE SCORECARD ─────────────────────────────────────────
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
        def hex_to_rgba(hex_str, opacity=0.12):
            hex_str = hex_str.lstrip('#')
            r = int(hex_str[0:2], 16)
            g = int(hex_str[2:4], 16)
            b = int(hex_str[4:6], 16)
            return f"rgba({r},{g},{b},{opacity})"

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
                bgcolor='#0D1823',
                radialaxis=dict(visible=True, range=[0, 100], color='#475569',
                                gridcolor='#1E2D40', tickfont=dict(size=9, color='#475569')),
                angularaxis=dict(color='#94A3B8', gridcolor='#1E2D40',
                                 linecolor='#1E2D40', tickfont=dict(size=11, color='#94A3B8'))
            ),
            paper_bgcolor='#0D1823', plot_bgcolor='#0D1823',
            font=dict(color='#94A3B8', family='DM Sans'),
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#94A3B8', size=12),
                        bordercolor='#1E2D40', borderwidth=1,
                        orientation='h', x=0.5, xanchor='center', y=-0.12),
            margin=dict(l=50, r=50, t=30, b=60), height=380,
        )

        col_radar, col_table = st.columns([1, 1.2])

        with col_radar:
            st.plotly_chart(fig_radar, use_container_width=True)

        with col_table:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div style='grid-template-columns:1.6fr 1fr 1fr 1fr;
                        display:grid; gap:8px;padding:4px 12px;font-size:10px;color:#334155;
                        font-family:Space Mono,monospace;margin-bottom:4px'>
                <div>METRIC</div>
                <div style='color:#DC2626'>BLINKIT</div>
                <div style='color:#1D9E75'>ZEPTO</div>
                <div style='color:#6C63DB'>BIGBASKET</div>
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
                            background:{"rgba(15,28,46,0.9)" if is_total else "#0D1823"};
                            border:1px solid {"#7C3AED" if is_total else "#1E2D40"};
                            border-radius:8px;font-size:12px;'>
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
        <div style='background: linear-gradient(135deg, #0F1C2E 0%, #0D1823 100%);
                    border: 1px solid #1E2D40; border-left: 3px solid #7C3AED;
                    border-radius: 0 12px 12px 0; padding: 18px 24px; margin-bottom: 24px;'>
            <div style='font-family: Space Mono, monospace; font-size: 9px; color: #7C3AED;
                        font-weight: 700; text-transform: uppercase; letter-spacing:.12em;
                        margin-bottom: 10px;'>📊 Intelligence Summary</div>
            <ul style='color: #E2E8F0; font-size: 13px; line-height: 1.8; margin: 0; padding-left: 20px;'>
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

    # Dynamic: find the biggest price gap across all platforms
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
    <div style='background: rgba(220,38,38,0.1); border: 1px solid #DC2626; border-radius: 12px; padding: 16px; margin-bottom: 24px;'>
        <div style='display:flex; align-items:center; gap:12px;'>
            <span style='font-size:24px;'>{_alert_icon}</span>
            <div>
                <div style='font-family: Space Mono, monospace; font-size:10px; color:#DC2626; font-weight:700; text-transform:uppercase;'>Pricing Disparity Alert</div>
                <div style='font-size:15px; font-weight:600; color:#F1F5F9; margin-top:2px;'>
                    {_max_gap_platform} {_gap_dir} <b>{_max_gap_category}</b> by <span style='color:#DC2626; font-weight:700;'>{abs(_max_gap_val):.1f}%</span> vs market average — the largest price gap in the dataset.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Platforms Compared", "3", "Blinkit · Zepto · BigBasket")
    with c2: st.metric("Categories", str(len(pm)), "master categories")
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

        # Cells text in 14px bold white
        text_matrix = [[f"<b>{v:+.1f}%</b>" for v in row] for row in gd.iloc[:, 1:].values]

        fig = go.Figure(data=go.Heatmap(
            z=gd.iloc[:, 1:].values,
            x=gd.columns[1:].tolist(),
            y=gd['Category'].tolist(),
            colorscale=[[0.0, '#14532D'], [0.5, '#F8FAFC'], [1.0, '#7F1D1D']],
            zmid=0,
            text=text_matrix,
            texttemplate='%{text}',
            textfont=dict(size=14, color='white', family='DM Sans'),
            colorbar=dict(
                title=dict(text='Gap %', font=dict(color='#94A3B8', size=11)),
                ticksuffix='%', tickfont=dict(color='#94A3B8'),
                bgcolor='#0D1823', bordercolor='#1E2D40', borderwidth=1
            )
        ))
        fig.update_layout(
            **{k: v for k, v in DARK_LAYOUT.items() if k not in ['xaxis', 'yaxis']},
            height=460,
            xaxis=dict(side='top', color='#94A3B8', tickfont=dict(size=13)),
            yaxis=dict(color='#94A3B8', autorange='reversed'),
            margin=dict(l=10, r=10, t=50, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

    # Winner by Category section below heatmap
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
            st.markdown(f"<div style='font-size:11px; font-weight:700; color:#E2E8F0; margin-bottom:8px; height: 32px; line-height: 1.2;'>{cat}</div>", unsafe_allow_html=True)
            for p in ['Blinkit', 'Zepto', 'BigBasket']:
                if p not in gaps:
                    st.markdown(f"""
                    <div style='background:#1E2D40; border: 1px solid #334155; border-radius: 99px;
                                padding:2px 6px; font-size:10px; text-align:center; color:#475569; margin-bottom:4px; font-family: Space Mono, monospace;'>
                        {p[:2]}: N/A
                    </div>
                    """, unsafe_allow_html=True)
                elif p == cheapest:
                    st.markdown(f"""
                    <div style='background:#14532D; border: 1px solid #16A34A; border-radius: 99px;
                                padding:2px 6px; font-size:10px; text-align:center; color:#86EFAC; font-weight:700; margin-bottom:4px; font-family: Space Mono, monospace;'>
                        {p[:2]}: {gaps[p]:+.0f}%
                    </div>
                    """, unsafe_allow_html=True)
                elif p == expensive:
                    st.markdown(f"""
                    <div style='background:#7F1D1D; border: 1px solid #DC2626; border-radius: 99px;
                                padding:2px 6px; font-size:10px; text-align:center; color:#FCA5A5; font-weight:700; margin-bottom:4px; font-family: Space Mono, monospace;'>
                        {p[:2]}: {gaps[p]:+.0f}%
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='background:#0F1C2E; border: 1px solid #1E2D40; border-radius: 99px;
                                padding:2px 6px; font-size:10px; text-align:center; color:#94A3B8; margin-bottom:4px; font-family: Space Mono, monospace;'>
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
                color='discount_pct', color_continuous_scale=[[0, '#1E2D40'], [1, '#1D9E75']],
                text='discount_pct',
                labels={'discount_pct': 'Median Discount (%)', 'master_category': ''}
            )
            fig.update_traces(
                texttemplate='%{text:.1f}%', textposition='outside',
                textfont=dict(color='#94A3B8', size=10),
                marker_line_width=0
            )
            fig.update_layout(**DARK_LAYOUT, height=330, coloraxis_showscale=False,
                              yaxis=dict(color='#94A3B8', gridcolor='#1E2D40'))
            fig.update_xaxes(showgrid=False)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("<p class='section-label'>BigBasket — Discount % by Category</p>", unsafe_allow_html=True)
        if 'category' in bb.columns and 'discount_pct' in bb.columns:
            disc_bb = bb.groupby('category')['discount_pct'].median().reset_index()
            disc_bb = disc_bb.sort_values('discount_pct', ascending=True).head(7)

            fig_bb = px.bar(
                disc_bb, x='discount_pct', y='category', orientation='h',
                color='discount_pct', color_continuous_scale=[[0, '#1E2D40'], [1, '#6C63DB']],
                text='discount_pct',
                labels={'discount_pct': 'Median Discount (%)', 'category': ''}
            )
            fig_bb.update_traces(
                texttemplate='%{text:.1f}%', textposition='outside',
                textfont=dict(color='#94A3B8', size=10),
                marker_line_width=0
            )
            fig_bb.update_layout(**DARK_LAYOUT, height=330, coloraxis_showscale=False,
                                 yaxis=dict(color='#94A3B8', gridcolor='#1E2D40'))
            fig_bb.update_xaxes(showgrid=False)
            st.plotly_chart(fig_bb, use_container_width=True)
