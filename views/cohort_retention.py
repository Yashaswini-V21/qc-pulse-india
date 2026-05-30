"""Cohort Retention page — Retention analytics dashboard design."""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import logging

logger = logging.getLogger(__name__)


# ── Design tokens ────────────────────────────────────────────
_BG       = "#060B14"
_CARD_BG  = "linear-gradient(135deg, #0F1C2E, #0D1823)"
_BORDER   = "linear-gradient(90deg, #DC2626, #7C3AED)"
_BLUE     = "#0EA5E9"
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


def _finding_card(title: str, main_text: str, body: str) -> str:
    return f"""
    <div style="
        background: {_CARD_BG};
        border-radius: 14px;
        padding: 22px 24px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        min-height: 170px;
    ">
        <div style="
            position:absolute; top:0; left:0; right:0; height:2px;
            background: {_BORDER};
        "></div>
        <div style="
            font-family:'Space Mono',monospace;
            font-size:10px; text-transform:uppercase;
            color:{_BLUE}; letter-spacing:0.12em;
            margin-bottom:8px;
        ">{title}</div>
        <div style="
            font-family:'DM Sans',sans-serif;
            font-weight:700; font-size:18px;
            color:#F1F5F9; margin-bottom:8px;
        ">{main_text}</div>
        <div style="
            font-family:'DM Sans',sans-serif;
            font-size:12.5px; color:{_LABEL_C};
            line-height:1.6;
        ">{body}</div>
    </div>
    """


def render_cohort_retention(
    cohort: pd.DataFrame,
) -> None:
    """Renders Cohort Retention page with retention analytics design."""

    # ── BADGE ──
    st.markdown(f"""
    <div style="padding:28px 0 6px;">
        <span style="
            display:inline-block;
            font-family:'Space Mono',monospace;
            font-size:11px; font-weight:700;
            text-transform:uppercase; letter-spacing:0.12em;
            color:{_BLUE};
            background:rgba(14,165,233,0.1);
            border:1px solid rgba(14,165,233,0.3);
            padding:5px 14px; border-radius:99px;
        ">● RETENTION ANALYSIS</span>
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
    ">Cohort Retention Analysis</h1>
    <p style="
        font-family:'DM Sans',sans-serif;
        font-size:14px; color:{_LABEL_C};
        margin:0 0 28px;
    ">24 monthly cohorts tracked across 2 years — who came back and when?</p>
    """, unsafe_allow_html=True)

    # ── Data prep ──
    cohort_num = cohort.copy()
    cohort_num.columns = cohort_num.columns.astype(int)

    avg_m1  = cohort_num[1].mean()
    avg_m3  = cohort_num[3].mean()
    best_c  = cohort_num[1].idxmax()
    best_v  = cohort_num[1].max()
    worst_c = cohort_num[1].idxmin()
    worst_v = cohort_num[1].min()

    # ── KPI ROW ──
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(_kpi_card("COHORTS", "24", "Jan 2014 – Dec 2015"), unsafe_allow_html=True)
    with c2:
        st.markdown(_kpi_card("AVG MONTH-1 RETENTION", f"{avg_m1:.1f}%", "of new customers return"), unsafe_allow_html=True)
    with c3:
        st.markdown(_kpi_card("AVG MONTH-3 RETENTION", f"{avg_m3:.1f}%", f"{avg_m3 - avg_m1:+.1f}pp vs Month-1"), unsafe_allow_html=True)
    with c4:
        st.markdown(_kpi_card("BEST COHORT M1", f"{best_v:.1f}%", str(best_c)), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── RETENTION HEATMAP ──
    st.markdown(f"""
    <div style="font-family:'Space Mono',monospace;font-size:10px;
        text-transform:uppercase;color:{_LABEL_C};letter-spacing:0.12em;
        margin-bottom:12px;">Retention Heatmap</div>
    """, unsafe_allow_html=True)

    ret_plot = cohort_num.iloc[:, :13].copy()
    ret_plot.index = ret_plot.index.astype(str)

    text_heatmap = [
        [f'<b>{v:.0f}%</b>' if not np.isnan(v) else '' for v in row]
        for row in ret_plot.values
    ]

    retention_colorscale = [
        [0.0, '#450A0A'], [0.15, '#991B1B'], [0.3, '#DC2626'],
        [0.45, '#F59E0B'], [0.6, '#FBBF24'], [0.8, '#86EFAC'], [1.0, '#16A34A']
    ]

    fig = go.Figure(data=go.Heatmap(
        z=ret_plot.values,
        x=[f'M{i}' for i in ret_plot.columns],
        y=ret_plot.index.tolist(),
        colorscale=retention_colorscale,
        zmin=0, zmax=35,
        text=text_heatmap,
        texttemplate='%{text}',
        textfont=dict(size=10, color='white', family='DM Sans'),
        colorbar=dict(
            title=dict(text='Retention %', font=dict(color='#94A3B8', size=11, family='DM Sans')),
            ticksuffix='%', tickfont=dict(color='white'),
            bgcolor=_PLOT_BG, bordercolor=_HOVER_BD, borderwidth=1,
        )
    ))
    fig.update_layout(
        plot_bgcolor=_PLOT_BG,
        paper_bgcolor=_PLOT_BG,
        font=dict(family='DM Sans', color='#94A3B8', size=11),
        height=580,
        xaxis=dict(color='#94A3B8', tickfont=dict(size=11)),
        yaxis=dict(color='#94A3B8', autorange='reversed', tickfont=dict(size=11)),
        margin=dict(l=10, r=10, t=10, b=10),
        hoverlabel=dict(bgcolor=_HOVER_BG, bordercolor=_HOVER_BD, font=dict(color='white', size=12)),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── MONTH-1 RETENTION LINE CHART ──
    st.markdown(f"""
    <div style="font-family:'Space Mono',monospace;font-size:10px;
        text-transform:uppercase;color:{_LABEL_C};letter-spacing:0.12em;
        margin-bottom:12px;">Month-1 Retention Trend</div>
    """, unsafe_allow_html=True)

    m1 = cohort_num[1].dropna().reset_index()
    m1.columns = ['cohort', 'retention']
    m1['cohort'] = m1['cohort'].astype(str)

    best_m1_idx = m1['retention'].idxmax()
    best_m1_row = m1.loc[best_m1_idx]
    worst_m1_idx = m1['retention'].idxmin()
    worst_m1_row = m1.loc[worst_m1_idx]

    fig2 = go.Figure()

    # Main line
    fig2.add_trace(go.Scatter(
        x=m1['cohort'], y=m1['retention'],
        mode='lines+markers',
        line=dict(color='#DC2626', width=2.5),
        marker=dict(color='#F97316', size=8, line=dict(color=_BG, width=2)),
        fill='tozeroy', fillcolor='rgba(220,38,38,0.07)',
        name='Month-1 Retention',
    ))

    # Best dot (green)
    fig2.add_trace(go.Scatter(
        x=[best_m1_row['cohort']], y=[best_m1_row['retention']],
        mode='markers',
        marker=dict(color='#16A34A', size=12, line=dict(color=_BG, width=2)),
        hoverinfo='text',
        text=f"Best: {best_m1_row['cohort']} ({best_m1_row['retention']:.1f}%)",
        name=f"Best: {best_m1_row['cohort']}",
    ))

    # Worst dot (red)
    fig2.add_trace(go.Scatter(
        x=[worst_m1_row['cohort']], y=[worst_m1_row['retention']],
        mode='markers',
        marker=dict(color='#DC2626', size=12, line=dict(color=_BG, width=2)),
        hoverinfo='text',
        text=f"Worst: {worst_m1_row['cohort']} ({worst_m1_row['retention']:.1f}%)",
        name=f"Worst: {worst_m1_row['cohort']}",
    ))

    # Average dashed line
    fig2.add_hline(
        y=avg_m1, line_dash='dash', line_color='#6C63DB', line_width=1.5,
        annotation_text=f'Avg {avg_m1:.1f}%',
        annotation_font_color='#94A3B8', annotation_font_size=11,
    )

    fig2.update_layout(
        plot_bgcolor=_PLOT_BG,
        paper_bgcolor=_PLOT_BG,
        font=dict(family='DM Sans', color='#94A3B8', size=11),
        margin=dict(l=10, r=10, t=10, b=10),
        height=280,
        xaxis=dict(color='#94A3B8', tickangle=45, tickfont=dict(size=10), gridcolor='#1E2D40'),
        yaxis=dict(color='#94A3B8', ticksuffix='%', gridcolor='#1E2D40'),
        showlegend=True,
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#94A3B8', size=10, family='DM Sans')),
        hoverlabel=dict(bgcolor=_HOVER_BG, bordercolor=_HOVER_BD, font=dict(color='white', size=12)),
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── THREE FINDING CARDS ──
    diff_best = ((best_v - avg_m1) / avg_m1 * 100) if avg_m1 > 0 else 0

    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        st.markdown(_finding_card(
            "BEST COHORT",
            f"{best_c} — {best_v:.1f}%",
            f"Achieved {best_v:.1f}% Month-1 retention — {diff_best:.0f}% above average"
        ), unsafe_allow_html=True)

    with fc2:
        st.markdown(_finding_card(
            "WORST COHORT",
            f"{worst_c} — {worst_v:.1f}%",
            f"{worst_v:.1f}% Month-1 — investigate acquisition quality this month"
        ), unsafe_allow_html=True)

    with fc3:
        loyalty_direction = "HIGHER" if avg_m3 > avg_m1 else "LOWER"
        st.markdown(_finding_card(
            "LOYALTY SIGNAL",
            f"Month-3: {avg_m3:.1f}%",
            f"Month-3 retention ({avg_m3:.1f}%) is {loyalty_direction} than Month-1 ({avg_m1:.1f}%) — customers who survive the first month become long-term loyalists"
        ), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── BUSINESS INSIGHT BOX ──
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #020B18, #041520);
        border: 1px solid {_BLUE};
        border-radius: 12px;
        padding: 26px 30px;
    ">
        <div style="
            font-family:'DM Sans',sans-serif;
            font-size:16px; font-weight:700;
            color:{_BLUE}; margin-bottom:14px;
        ">💡 Retention Insight</div>
        <div style="
            font-family:'DM Sans',sans-serif;
            font-size:13.5px; color:#CBD5E1;
            line-height:1.75;
        ">
            Average Month-1 retention of 14.3% means most first-time customers don't return.<br>
            A targeted "second purchase" incentive in Month-1 window could move this toward<br>
            the 26.3% peak seen in June 2015 — representing a potential 84% improvement<br>
            in early retention with the right intervention.
        </div>
    </div>
    """, unsafe_allow_html=True)
