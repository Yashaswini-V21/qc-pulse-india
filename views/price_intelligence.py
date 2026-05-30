"""Price Intelligence page — Competitive analytics dashboard design."""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import logging

logger = logging.getLogger(__name__)


# ── Design tokens ────────────────────────────────────────────
_BG       = "#060B14"
_CARD_BG  = "linear-gradient(135deg, #0F1C2E, #0D1823)"
_BORDER   = "linear-gradient(90deg, #DC2626, #7C3AED)"
_ORANGE   = "#F97316"
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


def render_price_intelligence(
    bl: pd.DataFrame,
    ze: pd.DataFrame,
    bb: pd.DataFrame,
    pm: pd.DataFrame,
) -> None:
    """Renders Price Intelligence page with competitive analytics design."""

    # ── BADGE ──
    st.markdown(f"""
    <div style="padding:28px 0 6px;">
        <span style="
            display:inline-block;
            font-family:'Space Mono',monospace;
            font-size:11px; font-weight:700;
            text-transform:uppercase; letter-spacing:0.12em;
            color:{_ORANGE};
            background:rgba(249,115,22,0.1);
            border:1px solid rgba(249,115,22,0.3);
            padding:5px 14px; border-radius:99px;
        ">● COMPETITIVE INTEL</span>
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
    ">Price Intelligence Matrix</h1>
    <p style="
        font-family:'DM Sans',sans-serif;
        font-size:14px; color:{_LABEL_C};
        margin:0 0 28px;
    ">Who wins the price war? Blinkit vs Zepto vs BigBasket — category by category.</p>
    """, unsafe_allow_html=True)

    # ── KPI ROW ──
    zd = ze['discount_pct'].median() if 'discount_pct' in ze.columns else 0
    bd = bb['discount_pct'].median() if 'discount_pct' in bb.columns else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(_kpi_card("PLATFORMS COMPARED", "3", "Blinkit · Zepto · BigBasket"), unsafe_allow_html=True)
    with c2:
        st.markdown(_kpi_card("CATEGORIES", str(len(pm)), "master categories"), unsafe_allow_html=True)
    with c3:
        st.markdown(_kpi_card("ZEPTO MEDIAN DISCOUNT", f"{zd:.0f}%", "most aggressive"), unsafe_allow_html=True)
    with c4:
        st.markdown(_kpi_card("BIGBASKET MEDIAN DISCOUNT", f"{bd:.0f}%", "vs market avg"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── SIGNATURE HEATMAP — Price Gap Matrix ──
    st.markdown(f"""
    <div style="font-family:'Space Mono',monospace;font-size:10px;
        text-transform:uppercase;color:{_LABEL_C};letter-spacing:0.12em;
        margin-bottom:12px;">Price Gap Matrix — % vs Market Average</div>
    """, unsafe_allow_html=True)

    gap_cols = [c for c in pm.columns if '_gap%' in c]
    if gap_cols:
        gd = pm[['category'] + gap_cols].dropna().copy()
        gd.columns = ['Category'] + [c.replace('_gap%', '') for c in gap_cols]

        text_matrix = [[f"<b>{v:+.1f}%</b>" for v in row] for row in gd.iloc[:, 1:].values]

        custom_colorscale = [
            [0, '#7F1D1D'], [0.35, '#DC2626'], [0.45, '#FEF3C7'],
            [0.5, '#F8FAFC'], [0.55, '#DCFCE7'], [0.65, '#16A34A'], [1, '#14532D']
        ]

        fig = go.Figure(data=go.Heatmap(
            z=gd.iloc[:, 1:].values,
            x=gd.columns[1:].tolist(),
            y=gd['Category'].tolist(),
            colorscale=custom_colorscale,
            zmid=0,
            text=text_matrix,
            texttemplate='%{text}',
            textfont=dict(size=14, color='white', family='DM Sans'),
            colorbar=dict(
                title=dict(text='Gap %', font=dict(color='#94A3B8', size=11, family='DM Sans')),
                ticksuffix='%', tickfont=dict(color='#94A3B8'),
                bgcolor=_PLOT_BG, bordercolor=_HOVER_BD, borderwidth=1
            )
        ))
        fig.update_layout(
            plot_bgcolor=_PLOT_BG,
            paper_bgcolor=_PLOT_BG,
            font=dict(family='DM Sans', color='#94A3B8', size=11),
            height=480,
            xaxis=dict(side='top', color='white', tickfont=dict(size=13, color='white')),
            yaxis=dict(color='white', autorange='reversed', tickfont=dict(size=12, color='white')),
            margin=dict(l=10, r=10, t=50, b=10),
            hoverlabel=dict(bgcolor=_HOVER_BG, bordercolor=_HOVER_BD, font=dict(color='white', size=12)),
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── TWO DISCOUNT CHARTS ──
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div style="font-family:'Space Mono',monospace;font-size:10px;
            text-transform:uppercase;color:{_LABEL_C};letter-spacing:0.12em;
            margin-bottom:12px;">Zepto — Discount % by Category</div>
        """, unsafe_allow_html=True)

        if 'master_category' in ze.columns and 'discount_pct' in ze.columns:
            disc = ze.groupby('master_category')['discount_pct'].median().reset_index()
            disc = disc[disc['master_category'] != 'Others'].sort_values('discount_pct', ascending=True)

            # Colorscale: low=#1E2D40, mid=#F59E0B, high=#DC2626
            max_v = disc['discount_pct'].max()
            min_v = disc['discount_pct'].min()
            range_v = max_v - min_v if max_v != min_v else 1
            bar_colors = []
            for v in disc['discount_pct']:
                t = (v - min_v) / range_v
                if t < 0.5:
                    t2 = t * 2
                    r = int(30 + t2 * (245 - 30))
                    g = int(45 + t2 * (158 - 45))
                    b = int(64 + t2 * (11 - 64))
                else:
                    t2 = (t - 0.5) * 2
                    r = int(245 + t2 * (220 - 245))
                    g = int(158 + t2 * (38 - 158))
                    b = int(11 + t2 * (38 - 11))
                bar_colors.append(f'rgb({r},{g},{b})')

            fig_z = go.Figure(go.Bar(
                x=disc['discount_pct'],
                y=disc['master_category'],
                orientation='h',
                marker_color=bar_colors,
                text=disc['discount_pct'].round(1).astype(str) + '%',
                textposition='outside',
                textfont=dict(color='#94A3B8', size=10, family='DM Sans'),
                marker_line_width=0,
            ))
            fig_z.update_layout(
                plot_bgcolor=_PLOT_BG, paper_bgcolor=_PLOT_BG,
                font=dict(family='DM Sans', color='#94A3B8', size=11),
                margin=dict(l=10, r=60, t=10, b=10), height=330,
                xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
                yaxis=dict(color='#94A3B8', tickfont=dict(size=11)),
                hoverlabel=dict(bgcolor=_HOVER_BG, bordercolor=_HOVER_BD, font=dict(color='white', size=12)),
            )
            st.plotly_chart(fig_z, use_container_width=True)

    with col2:
        st.markdown(f"""
        <div style="font-family:'Space Mono',monospace;font-size:10px;
            text-transform:uppercase;color:{_LABEL_C};letter-spacing:0.12em;
            margin-bottom:12px;">BigBasket — Discount % by Category (Top 8)</div>
        """, unsafe_allow_html=True)

        if 'category' in bb.columns and 'discount_pct' in bb.columns:
            disc_bb = bb.groupby('category')['discount_pct'].median().reset_index()
            disc_bb = disc_bb.sort_values('discount_pct', ascending=True).tail(8)

            # Colorscale: low=#1E2D40, mid=#6C63DB, high=#DC2626
            max_v = disc_bb['discount_pct'].max()
            min_v = disc_bb['discount_pct'].min()
            range_v = max_v - min_v if max_v != min_v else 1
            bar_colors_bb = []
            for v in disc_bb['discount_pct']:
                t = (v - min_v) / range_v
                if t < 0.5:
                    t2 = t * 2
                    r = int(30 + t2 * (108 - 30))
                    g = int(45 + t2 * (99 - 45))
                    b = int(64 + t2 * (219 - 64))
                else:
                    t2 = (t - 0.5) * 2
                    r = int(108 + t2 * (220 - 108))
                    g = int(99 + t2 * (38 - 99))
                    b = int(219 + t2 * (38 - 219))
                bar_colors_bb.append(f'rgb({r},{g},{b})')

            fig_bb = go.Figure(go.Bar(
                x=disc_bb['discount_pct'],
                y=disc_bb['category'],
                orientation='h',
                marker_color=bar_colors_bb,
                text=disc_bb['discount_pct'].round(1).astype(str) + '%',
                textposition='outside',
                textfont=dict(color='#94A3B8', size=10, family='DM Sans'),
                marker_line_width=0,
            ))
            fig_bb.update_layout(
                plot_bgcolor=_PLOT_BG, paper_bgcolor=_PLOT_BG,
                font=dict(family='DM Sans', color='#94A3B8', size=11),
                margin=dict(l=10, r=60, t=10, b=10), height=330,
                xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
                yaxis=dict(color='#94A3B8', tickfont=dict(size=11)),
                hoverlabel=dict(bgcolor=_HOVER_BG, bordercolor=_HOVER_BD, font=dict(color='white', size=12)),
            )
            st.plotly_chart(fig_bb, use_container_width=True)

    # ── INSIGHT BOX ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1C0A00, #1A0F00);
        border: 1px solid {_ORANGE};
        border-radius: 12px;
        padding: 26px 30px;
    ">
        <div style="
            font-family:'DM Sans',sans-serif;
            font-size:16px; font-weight:700;
            color:{_ORANGE}; margin-bottom:14px;
        ">💡 Key Competitive Finding</div>
        <div style="
            font-family:'DM Sans',sans-serif;
            font-size:13.5px; color:#CBD5E1;
            line-height:1.75;
        ">
            Zepto leads aggressive discounting across Snacks and Beverages.<br>
            BigBasket maintains premium positioning in Fresh Produce and Dairy.<br>
            For a budget-conscious shopper: Zepto wins Snacks, BigBasket wins Staples.<br>
            Strategic recommendation: a new QC entrant should undercut on Fresh Produce
            where current platform variance is highest.
        </div>
    </div>
    """, unsafe_allow_html=True)
