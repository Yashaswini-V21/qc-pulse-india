"""Market Basket Analysis page — Product affinity dashboard design."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Design tokens ────────────────────────────────────────────
_BG       = "#060B14"
_CARD_BG  = "linear-gradient(135deg, #0F1C2E, #0D1823)"
_BORDER   = "linear-gradient(90deg, #DC2626, #7C3AED)"
_CYAN     = "#06B6D4"
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


def render_market_basket(
    ar: pd.DataFrame,
) -> None:
    """Renders Market Basket Analysis page with product affinity design."""

    # ── BADGE ──
    st.markdown(f"""
    <div style="padding:28px 0 6px;">
        <span style="
            display:inline-block;
            font-family:'Space Mono',monospace;
            font-size:11px; font-weight:700;
            text-transform:uppercase; letter-spacing:0.12em;
            color:{_CYAN};
            background:rgba(6,182,212,0.1);
            border:1px solid rgba(6,182,212,0.3);
            padding:5px 14px; border-radius:99px;
        ">● PRODUCT AFFINITY</span>
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
    ">Market Basket Analysis</h1>
    <p style="
        font-family:'DM Sans',sans-serif;
        font-size:14px; color:{_LABEL_C};
        margin:0 0 28px;
    ">Association rules from 38,765 transactions using the Apriori algorithm.</p>
    """, unsafe_allow_html=True)

    if len(ar) == 0:
        st.info("No association rules found. Please check your data pipeline.")
        return

    # ── KPI ROW ──
    best_lift_row = ar.sort_values('lift', ascending=False).iloc[0]
    best_conf_row = ar.sort_values('confidence_pct', ascending=False).iloc[0]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(_kpi_card("TOTAL RULES", f"{len(ar)}", "support ≥ 0.15%"), unsafe_allow_html=True)
    with c2:
        st.markdown(_kpi_card("HIGHEST LIFT", f"{best_lift_row['lift']:.2f}x",
            best_lift_row['rule'].replace('→', '→')), unsafe_allow_html=True)
    with c3:
        st.markdown(_kpi_card("HIGHEST CONFIDENCE", f"{best_conf_row['confidence_pct']:.1f}%",
            best_conf_row['rule'].replace('→', '→')), unsafe_allow_html=True)
    with c4:
        st.markdown(_kpi_card("AVG LIFT SCORE", f"{ar['lift'].mean():.2f}x", "vs random purchase"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CHARTS + RECOMMENDER ──
    col1, col2 = st.columns([1.4, 1])

    with col1:
        st.markdown(f"""
        <div style="font-family:'Space Mono',monospace;font-size:10px;
            text-transform:uppercase;color:{_LABEL_C};letter-spacing:0.12em;
            margin-bottom:12px;">Association Rules — Confidence vs Lift</div>
        """, unsafe_allow_html=True)

        fig_scatter = px.scatter(
            ar, x='confidence_pct', y='lift',
            size='support_pct', color='lift',
            color_continuous_scale=[[0, '#1E2D40'], [0.5, '#7C3AED'], [1, '#DC2626']],
            hover_data=['rule', 'support_pct', 'confidence_pct', 'lift'],
            labels={
                'confidence_pct': 'Confidence %',
                'lift': 'Lift (Multiplier)',
                'support_pct': 'Support %',
            }
        )
        fig_scatter.update_layout(
            plot_bgcolor=_PLOT_BG, paper_bgcolor=_PLOT_BG,
            font=dict(family='DM Sans', color='#94A3B8', size=11),
            margin=dict(l=10, r=10, t=10, b=10), height=380,
            xaxis=dict(color='#94A3B8', gridcolor='#1E2D40'),
            yaxis=dict(color='#94A3B8', gridcolor='#1E2D40'),
            coloraxis_showscale=False,
            hoverlabel=dict(bgcolor=_HOVER_BG, bordercolor=_HOVER_BD, font=dict(color='white', size=12)),
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col2:
        st.markdown(f"""
        <div style="font-family:'Space Mono',monospace;font-size:10px;
            text-transform:uppercase;color:{_LABEL_C};letter-spacing:0.12em;
            margin-bottom:12px;">🛒 Product Bundle Recommender</div>
        """, unsafe_allow_html=True)

        all_antecedents = sorted(list(ar['antecedents_str'].unique()))
        selected_item = st.selectbox("Select Product to Cross-Sell", all_antecedents, index=0)

        matching_rules = ar[ar['antecedents_str'] == selected_item].sort_values('lift', ascending=False)

        if len(matching_rules) == 0:
            st.markdown(f"<p style='color:#94A3B8;font-size:13px;'>No rules found starting with {selected_item}.</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='font-family:DM Sans;color:#94A3B8;font-size:13px;margin-bottom:12px;'>Customers buying <b>{selected_item}</b> are also highly likely to buy:</p>", unsafe_allow_html=True)
            for _, row in matching_rules.iterrows():
                st.markdown(f"""
                <div style="
                    background: {_CARD_BG};
                    border: 1px solid #1E2D40;
                    border-radius: 12px; padding: 14px 18px; margin-bottom: 8px;
                ">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="font-family:'DM Sans',sans-serif;color:#F1F5F9;font-weight:700;font-size:14px;">👉 {row['consequents_str']}</span>
                        <span style="
                            background:rgba(124,58,237,0.12);
                            border:1px solid rgba(124,58,237,0.25);
                            color:#A78BFA;font-size:10px;font-weight:700;
                            font-family:'Space Mono',monospace;
                            padding:2px 8px;border-radius:99px;
                        ">{row['lift']:.2f}x Lift</span>
                    </div>
                    <div style="font-family:'Space Mono',monospace;font-size:10px;color:#475569;margin-top:4px;">
                        Confidence: <span style="color:#94A3B8;">{row['confidence_pct']}%</span> |
                        Support: <span style="color:#94A3B8;">{row['support_pct']}%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── FULL RULES TABLE ──
    st.markdown(f"""
    <div style="font-family:'Space Mono',monospace;font-size:10px;
        text-transform:uppercase;color:{_LABEL_C};letter-spacing:0.12em;
        margin-bottom:12px;">Full Association Rules</div>
    """, unsafe_allow_html=True)

    tbl = ar[['rule', 'support_pct', 'confidence_pct', 'lift']].copy()
    tbl.columns = ['Association Rule', 'Support %', 'Confidence %', 'Lift']
    st.dataframe(tbl, use_container_width=True, hide_index=True)
