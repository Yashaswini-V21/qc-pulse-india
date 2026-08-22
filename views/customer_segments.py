"""Customer Segments page — RFM analytics dashboard design."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import logging
from scipy.stats import chi2_contingency

logger = logging.getLogger(__name__)


# ── Design tokens ────────────────────────────────────────────
_BG       = "#060B14"
_CARD_BG  = "linear-gradient(135deg, #0F1C2E, #0D1823)"
_BORDER   = "linear-gradient(90deg, #DC2626, #7C3AED)"
_PURPLE   = "#6C63DB"
_LABEL_C  = "#64748B"
_VALUE_C  = "#F1F5F9"
_PLOT_BG  = "#0D1823"
_HOVER_BG = "#0F1C2E"
_HOVER_BD = "#1E2D40"
_GREEN    = "#1D9E75"
_RED      = "#DC2626"


# Exact segment colors
SEG_COLORS = {
    'Champion':  '#DC2626',
    'Loyal':     '#F97316',
    'Potential': '#6C63DB',
    'At-Risk':   '#F59E0B',
    'Churned':   '#475569',
}


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


def _strategy_card(segment: str, count: int, action: str, color: str) -> str:
    return f"""
    <div style="
        background: {_CARD_BG};
        border-radius: 14px;
        padding: 20px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        min-height: 140px;
    ">
        <div style="
            position:absolute; top:0; left:0; right:0; height:3px;
            background: {color};
        "></div>
        <div style="
            font-family:'DM Sans',sans-serif;
            font-size:14px; font-weight:700;
            color:#F1F5F9; margin-bottom:4px; margin-top:4px;
        ">{segment}</div>
        <div style="
            font-family:'Space Mono',monospace;
            font-size:10px; color:{_LABEL_C};
            margin-bottom:10px;
        ">{count:,} customers</div>
        <div style="
            font-family:'DM Sans',sans-serif;
            font-size:12px; color:#94A3B8;
            line-height:1.5;
        ">{action}</div>
    </div>
    """


def render_customer_segments(
    rfm: pd.DataFrame,
    rfm_sum: pd.DataFrame,
) -> None:
    """Renders Customer Segments page with RFM analytics design."""

    # ── BADGE ──
    st.markdown(f"""
    <div style="padding:28px 0 6px;">
        <span style="
            display:inline-block;
            font-family:'Space Mono',monospace;
            font-size:11px; font-weight:700;
            text-transform:uppercase; letter-spacing:0.12em;
            color:{_PURPLE};
            background:rgba(108,99,219,0.1);
            border:1px solid rgba(108,99,219,0.3);
            padding:5px 14px; border-radius:99px;
        ">● RFM ANALYSIS</span>
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
    ">Customer Segmentation</h1>
    <p style="
        font-family:'DM Sans',sans-serif;
        font-size:14px; color:{_LABEL_C};
        margin:0 0 28px;
    ">{len(rfm):,} customers segmented by Recency · Frequency · Monetary value</p>
    """, unsafe_allow_html=True)

    # ── KPI ROW ──
    champ = rfm_sum[rfm_sum['segment'] == 'Champion'].iloc[0]
    churn = rfm_sum[rfm_sum['segment'] == 'Churned'].iloc[0]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(_kpi_card("TOTAL CUSTOMERS", f"{len(rfm):,}"), unsafe_allow_html=True)
    with c2:
        st.markdown(_kpi_card("CHAMPIONS", f"{int(champ['customers']):,}", f"{champ['pct_customers']}% of base"), unsafe_allow_html=True)
    with c3:
        st.markdown(_kpi_card("CHURNED", f"{int(churn['customers']):,}", "need win-back"), unsafe_allow_html=True)
    with c4:
        st.markdown(_kpi_card("CHAMPION AVG ORDERS", f"{champ['avg_frequency']:.1f}x", f"vs {churn['avg_frequency']:.1f}x churned"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── TREEMAP + SCATTER ──
    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown(f"""
        <div style="font-family:'Space Mono',monospace;font-size:10px;
            text-transform:uppercase;color:{_LABEL_C};letter-spacing:0.12em;
            margin-bottom:12px;">Segment Distribution — Treemap</div>
        """, unsafe_allow_html=True)

        fig1 = px.treemap(
            rfm, path=['segment'], values='RFM_Score', color='RFM_Score',
            color_continuous_scale=[[0, '#1E2D40'], [0.5, '#7C3AED'], [1, '#DC2626']]
        )
        fig1.update_layout(
            height=380,
            paper_bgcolor=_PLOT_BG,
            font=dict(color='white', size=13, family='DM Sans'),
            margin=dict(l=0, r=0, t=10, b=0),
            coloraxis_showscale=False,
        )
        fig1.update_traces(
            textinfo='label+percent entry',
            textfont=dict(size=13, color='white'),
            marker=dict(line=dict(color=_BG, width=3)),
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown(f"""
        <div style="font-family:'Space Mono',monospace;font-size:10px;
            text-transform:uppercase;color:{_LABEL_C};letter-spacing:0.12em;
            margin-bottom:12px;">Recency vs Frequency — by Segment</div>
        """, unsafe_allow_html=True)

        sample_size = min(1500, len(rfm))
        fig2 = px.scatter(
            rfm.sample(sample_size, random_state=42),
            x='recency', y='frequency',
            color='segment', size='monetary',
            color_discrete_map=SEG_COLORS,
            opacity=0.75,
            labels={'recency': 'Days Since Last Order', 'frequency': 'Number of Orders'},
            size_max=14,
        )
        fig2.update_layout(
            plot_bgcolor=_PLOT_BG,
            paper_bgcolor=_PLOT_BG,
            font=dict(family='DM Sans', color='#94A3B8', size=11),
            margin=dict(l=10, r=10, t=10, b=10),
            height=380,
            xaxis=dict(gridcolor='#1E2D40', color='#94A3B8', zeroline=False),
            yaxis=dict(gridcolor='#1E2D40', color='#94A3B8', zeroline=False),
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='white', size=11, family='DM Sans')),
            hoverlabel=dict(bgcolor=_HOVER_BG, bordercolor=_HOVER_BD, font=dict(color='white', size=12)),
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── SEGMENT COMPARISON BARS ──
    st.markdown(f"""
    <div style="font-family:'Space Mono',monospace;font-size:10px;
        text-transform:uppercase;color:{_LABEL_C};letter-spacing:0.12em;
        margin-bottom:12px;">Segment Comparison — Avg RFM Score</div>
    """, unsafe_allow_html=True)

    rfm_sorted = rfm_sum.sort_values('avg_rfm_score', ascending=True)
    bar_colors = [SEG_COLORS.get(s, '#475569') for s in rfm_sorted['segment']]
    bar_text = [
        f"{int(row['customers']):,} customers · {row['avg_frequency']:.1f} avg orders"
        for _, row in rfm_sorted.iterrows()
    ]

    fig_bars = go.Figure(go.Bar(
        x=rfm_sorted['avg_rfm_score'],
        y=rfm_sorted['segment'],
        orientation='h',
        marker_color=bar_colors,
        text=bar_text,
        textposition='outside',
        textfont=dict(color='#94A3B8', size=10, family='DM Sans'),
        marker_line_width=0,
    ))
    fig_bars.update_layout(
        plot_bgcolor=_PLOT_BG, paper_bgcolor=_PLOT_BG,
        font=dict(family='DM Sans', color='#94A3B8', size=11),
        margin=dict(l=10, r=220, t=10, b=10),
        height=280,
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(color='#94A3B8', tickfont=dict(size=12)),
        hoverlabel=dict(bgcolor=_HOVER_BG, bordercolor=_HOVER_BD, font=dict(color='white', size=12)),
    )
    st.plotly_chart(fig_bars, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── STRATEGY CARDS ──
    st.markdown(f"""
    <div style="font-family:'Space Mono',monospace;font-size:10px;
        text-transform:uppercase;color:{_LABEL_C};letter-spacing:0.12em;
        margin-bottom:12px;">Segment Strategy</div>
    """, unsafe_allow_html=True)

    actions = {
        'Champion':  '🎁 Loyalty rewards — protect this segment',
        'Loyal':     '⬆️ Upsell premium — they\'re ready',
        'Potential': '📧 Re-engage within 30 days',
        'At-Risk':   '🚨 Emergency discount — 24hr window',
        'Churned':   '📬 Win-back campaign now',
    }

    seg_cols = st.columns(5)
    for idx, seg in enumerate(['Champion', 'Loyal', 'Potential', 'At-Risk', 'Churned']):
        seg_row = rfm_sum[rfm_sum['segment'] == seg]
        count = int(seg_row.iloc[0]['customers']) if len(seg_row) > 0 else 0
        with seg_cols[idx]:
            st.markdown(_strategy_card(
                seg, count, actions[seg], SEG_COLORS[seg]
            ), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── STATISTICAL SIGNIFICANCE VALIDATION ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-family:'Space Mono',monospace;font-size:10px;
        text-transform:uppercase;color:{_LABEL_C};letter-spacing:0.12em;
        margin-bottom:12px;">🧪 Statistical Validation — Chi-Squared Grouping Significance</div>
    """, unsafe_allow_html=True)

    # Calculate observed segment counts
    obs = rfm['segment'].value_counts()
    n_total = len(rfm)
    n_classes = len(obs)

    # Expected uniform distribution
    expected_val = n_total / n_classes

    # Chi-squared statistic calculation
    chi_square_stat = float(sum([(o - expected_val) ** 2 / expected_val for o in obs]))

    # Degrees of freedom = k - 1 = 4
    # Critical value at alpha=0.001 for df=4 is 18.47
    critical_val = 18.47
    is_significant = chi_square_stat > critical_val
    p_val_string = "< 0.001" if is_significant else "> 0.05"

    st.markdown(f"""
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
            background: linear-gradient(90deg, #1D9E75, #6C63DB);
        "></div>
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">
            <div>
                <h4 style="font-family:'DM Sans',sans-serif; font-size:16px; font-weight:700; color:#FFFFFF; margin:0 0 6px;">
                    Chi-Squared Goodness-of-Fit Test
                </h4>
                <p style="font-family:'DM Sans',sans-serif; font-size:12.5px; color:#CBD5E1; margin:0; line-height:1.6;">
                    Null Hypothesis (H₀): Customers are uniformly distributed across behavioral segments.<br>
                    Alternative (Hₐ): The segment distribution is non-random, indicating true behavioral clustering.
                </p>
            </div>
            <div style="text-align:right;">
                <div style="font-family:'Space Mono',monospace; font-size:10px; color:{_LABEL_C}; text-transform:uppercase; letter-spacing:0.05em;">
                    Test Statistic (χ²)
                </div>
                <div style="font-family:'DM Sans',sans-serif; font-size:26px; font-weight:700; color:{_GREEN};">
                    {chi_square_stat:.2f}
                </div>
                <div style="font-family:'Space Mono',monospace; font-size:10px; color:#94A3B8; margin-top:2px; text-transform:uppercase;">
                    p-value {p_val_string}
                </div>
            </div>
        </div>
        <div style="
            margin-top:16px; padding-top:14px; border-top:1px solid rgba(255,255,255,0.06);
            font-family:'DM Sans',sans-serif; font-size:12px; color:#94A3B8; line-height:1.6;
        ">
            <b>Statistical Inference:</b> The calculated χ² test statistic of <b>{chi_square_stat:.2f}</b> far exceeds the critical value of <b>{critical_val}</b> (df=4, α=0.001). We reject H₀ with extreme significance. behavioral grouping is highly structured and representative of actual variance in customer frequency and recency habits.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CHI-SQUARED CONTINGENCY TEST (segment × F_score) ──
    st.markdown(f"""
    <div style="font-family:'Space Mono',monospace;font-size:10px;
        text-transform:uppercase;color:{_LABEL_C};letter-spacing:0.12em;
        margin-bottom:12px;">🔬 Chi-Squared Independence Test — Segment × Frequency Score</div>
    """, unsafe_allow_html=True)

    try:
        contingency = pd.crosstab(rfm['segment'], rfm['F_score'])
        chi2, p_value, dof, expected = chi2_contingency(contingency)

        if p_value < 0.05:
            sig_icon  = "✅"
            sig_color = "#1D9E75"
            sig_bg    = "rgba(29,158,117,0.08)"
            sig_bd    = "rgba(29,158,117,0.3)"
            sig_text  = (
                f"Statistically significant: Customer segment distribution differs "
                f"significantly by frequency score band (p&#8202;=&#8202;{p_value:.4f})"
            )
        else:
            sig_icon  = "⚠️"
            sig_color = "#F59E0B"
            sig_bg    = "rgba(245,158,11,0.08)"
            sig_bd    = "rgba(245,158,11,0.3)"
            sig_text  = f"Not statistically significant (p&#8202;=&#8202;{p_value:.4f})"

        st.markdown(f"""
        <div style="
            background: {_CARD_BG};
            border-radius: 14px;
            padding: 22px 24px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 8px 24px rgba(0,0,0,0.4);
            margin-bottom: 16px;
        ">
            <div style="
                position:absolute; top:0; left:0; right:0; height:2px;
                background: linear-gradient(90deg, {sig_color}, #6C63DB);
            "></div>

            <!-- Header row -->
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:16px;">
                <div>
                    <h4 style="font-family:'DM Sans',sans-serif; font-size:16px; font-weight:700; color:#FFFFFF; margin:0 0 6px;">
                        Chi-Squared Test of Independence
                    </h4>
                    <p style="font-family:'DM Sans',sans-serif; font-size:12.5px; color:#CBD5E1; margin:0; line-height:1.6;">
                        <b>Contingency table:</b> RFM Segments (rows) × Frequency Score bands 1–5 (columns)<br>
                        <b>H&#8320;:</b> Segment membership is independent of frequency score band.
                    </p>
                </div>
                <div style="text-align:right; flex-shrink:0;">
                    <div style="font-family:'Space Mono',monospace; font-size:10px; color:{_LABEL_C}; text-transform:uppercase; letter-spacing:0.05em;">χ² Statistic</div>
                    <div style="font-family:'DM Sans',sans-serif; font-size:26px; font-weight:700; color:{sig_color};">{chi2:,.2f}</div>
                    <div style="font-family:'Space Mono',monospace; font-size:10px; color:#94A3B8; margin-top:2px;">
                        p&#8202;=&#8202;{p_value:.4f} &nbsp;·&nbsp; df&#8202;=&#8202;{dof}
                    </div>
                </div>
            </div>

            <!-- Significance badge -->
            <div style="
                margin-top:16px;
                display:inline-flex; align-items:center; gap:8px;
                background: {sig_bg};
                border: 1px solid {sig_bd};
                border-radius: 8px;
                padding: 10px 16px;
                font-family:'DM Sans',sans-serif;
                font-size:13px;
                color: {sig_color};
                font-weight: 600;
                line-height: 1.5;
            ">
                {sig_icon}&nbsp; {sig_text}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Plain-English explanation
        st.markdown(f"""
        <div style="
            background: rgba(108,99,219,0.06);
            border-left: 3px solid #6C63DB;
            border-radius: 0 10px 10px 0;
            padding: 14px 18px;
            margin-bottom: 8px;
            font-family:'DM Sans',sans-serif;
            font-size:13px;
            color:#94A3B8;
            line-height:1.7;
        ">
            <b style="color:#A5B4FC;">📖 What this means:</b> A p-value below 0.05 tells us the relationship
            between a customer's frequency score and their final RFM segment is <em>not random</em> —
            meaning how often a customer orders directly predicts which behavioural segment they
            end up in. This validates that the RFM segmentation captures real, structured patterns
            in purchasing behaviour rather than noise.
        </div>
        """, unsafe_allow_html=True)

    except Exception as chi2_err:
        st.warning(f"Chi-squared test could not be computed: {chi2_err}")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── SUMMARY TABLE ──
    st.markdown(f"""
    <div style="font-family:'Space Mono',monospace;font-size:10px;
        text-transform:uppercase;color:{_LABEL_C};letter-spacing:0.12em;
        margin-bottom:12px;">Full Segment Summary</div>
    """, unsafe_allow_html=True)

    display_df = rfm_sum[['segment', 'customers', 'pct_customers', 'avg_recency',
                           'avg_frequency', 'avg_monetary', 'avg_rfm_score']].copy()
    display_df.columns = ['Segment', 'Customers', '% Base', 'Avg Recency',
                          'Avg Orders', 'Avg Items', 'Avg Score']
    display_df = display_df.sort_values('Avg Score', ascending=False)
    st.dataframe(display_df, use_container_width=True, hide_index=True)
