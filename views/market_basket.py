import streamlit as st
import pandas as pd
import plotly.express as px
from typing import Dict, Any

def render_market_basket(
    ar: pd.DataFrame,
    DARK_LAYOUT: Dict[str, Any]
) -> None:
    """
    Renders modular Market Basket Analysis page for QC Pulse India.
    """
    st.markdown("<span class='stat-badge'>PRODUCT AFFINITY</span>", unsafe_allow_html=True)
    st.title("Market Basket Analysis")
    st.markdown("<p style='color:#475569;font-size:14px;margin-top:-8px'>Association rules generated from 38,765 customer shopping transactions using the Apriori algorithm.</p>", unsafe_allow_html=True)
    st.markdown("---")

    if len(ar) == 0:
        st.info("No association rules found. Please check your data pipeline.")
    else:
        # KPIs
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Total Association Rules", f"{len(ar)}", "support >= 0.15%")
        with c2:
            best_lift_row = ar.sort_values('lift', ascending=False).iloc[0]
            st.metric("Highest Lift Score", f"{best_lift_row['lift']:.2f}x", f"{best_lift_row['rule'].replace('→', '->')}")
        with c3:
            best_conf_row = ar.sort_values('confidence_pct', ascending=False).iloc[0]
            st.metric("Highest Confidence", f"{best_conf_row['confidence_pct']:.1f}%", f"{best_conf_row['rule'].replace('→', '->')}")
        with c4:
            st.metric("Avg Lift Score", f"{ar['lift'].mean():.2f}x", "vs random purchase")

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns([1.4, 1])

        with col1:
            st.markdown("<p class='section-label'>Association Rules — Confidence vs. Lift</p>", unsafe_allow_html=True)
            fig_scatter = px.scatter(
                ar,
                x='confidence_pct', y='lift',
                size='support_pct', color='lift',
                color_continuous_scale=[[0, '#1E2D40'], [0.5, '#7C3AED'], [1, '#DC2626']],
                hover_data=['rule', 'support_pct', 'confidence_pct', 'lift'],
                labels={'confidence_pct': 'Confidence % (If bought X, prob of Y)',
                        'lift': 'Lift (Multiplier vs Random purchase)',
                        'support_pct': 'Support % (Frequency in all baskets)'}
            )
            fig_scatter.update_layout(
                **DARK_LAYOUT, height=380,
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

        with col2:
            st.markdown("<p class='section-label'>🛒 Product Bundle Recommender</p>", unsafe_allow_html=True)

            all_antecedents = sorted(list(ar['antecedents_str'].unique()))
            selected_item = st.selectbox("Select Product to Cross-Sell", all_antecedents, index=0)

            matching_rules = ar[ar['antecedents_str'] == selected_item].sort_values('lift', ascending=False)

            if len(matching_rules) == 0:
                st.markdown(f"<p style='color:#94A3B8;font-size:13px;'>No rules found starting with {selected_item}.</p>", unsafe_allow_html=True)
            else:
                st.markdown(f"<p style='color:#94A3B8;font-size:13px;margin-bottom:12px;'>Customers buying <b>{selected_item}</b> are also highly likely to buy:</p>", unsafe_allow_html=True)
                for _, row in matching_rules.iterrows():
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #0F1C2E 0%, #0D1823 100%);
                                border: 1px solid #1E2D40; border-radius: 10px; padding: 12px 16px; margin-bottom: 8px;'>
                        <div style='display:flex; justify-content:space-between; align-items:center;'>
                            <span style='color:#F1F5F9; font-weight:700; font-size:14px;'>👉 {row['consequents_str']}</span>
                            <span style='background: rgba(220,38,38,.12); border: 1px solid rgba(220,38,38,.25);
                                         color:#FCA5A5; font-size:10px; font-weight:700; padding:2px 8px;
                                         border-radius:99px; font-family:Space Mono,monospace;'>
                                {row['lift']:.2f}x Lift
                            </span>
                        </div>
                        <div style='font-size:11px; color:#475569; font-family:Space Mono,monospace; margin-top: 4px;'>
                            Confidence: <span style='color:#94A3B8;'>{row['confidence_pct']}%</span> |
                            Support: <span style='color:#94A3B8;'>{row['support_pct']}%</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("<p class='section-label'>Full Association Rules Data Table</p>", unsafe_allow_html=True)
        tbl = ar[['rule', 'support_pct', 'confidence_pct', 'lift']].copy()
        tbl.columns = ['Association Rule', 'Support % (Frequency)', 'Confidence % (Strength)', 'Lift (Multiplier)']
        st.dataframe(tbl, use_container_width=True, hide_index=True)
