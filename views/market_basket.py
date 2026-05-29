"""Market Basket Analysis page — Premium "Dark Intelligence" design."""
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.charts import apply_premium_theme, BAR_COLOR


def render_market_basket(
    ar: pd.DataFrame,
) -> None:
    """Renders Market Basket Analysis page with premium design."""
    # ── CYBER HEADER ──
    st.markdown("""
    <div style="padding: 24px 0 16px; animation: fadeIn 0.8s ease;">
      <div style="display:flex; align-items:center; gap:14px; margin-bottom:12px;">
        <div style="
          width:44px; height:44px;
          background: linear-gradient(135deg, #10B981, #06B6D4);
          border-radius:12px;
          display:flex; align-items:center; justify-content:center;
          font-size:22px;
          box-shadow: 0 8px 24px rgba(6,182,212,0.3);
        ">🛒</div>
        <div>
          <div class="stat-badge" style="margin:0; background:rgba(6,182,212,0.15); border-color:rgba(6,182,212,0.35); color:#22D3EE; box-shadow:0 0 15px rgba(6,182,212,0.15);">PRODUCT AFFINITY</div>
          <div class="live-badge" style="margin-top:4px;">
            <span class="status-dot status-live"></span>
            Apriori Engine Connected
          </div>
        </div>
      </div>
      <h1 style="
        font-size:40px !important;
        font-weight:900 !important;
        letter-spacing:-0.03em !important;
        line-height:1.1 !important;
        margin:0 0 8px !important;
        background: linear-gradient(135deg, #FFFFFF 0%, #A7F3D0 50%, #06B6D4 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
      ">Market Basket Analysis</h1>
      <p style="
        font-size:14.5px; color:#64748B;
        font-weight:400; margin:0 0 20px;
        line-height:1.6;
      ">Association rules generated from 38,765 customer shopping transactions using the Apriori algorithm.</p>
    </div>
    """, unsafe_allow_html=True)
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
                color_continuous_scale=[[0, 'rgba(139,92,246,0.2)'], [0.5, '#8B5CF6'], [1, '#A78BFA']],
                hover_data=['rule', 'support_pct', 'confidence_pct', 'lift'],
                labels={'confidence_pct': 'Confidence % (If bought X, prob of Y)',
                        'lift': 'Lift (Multiplier vs Random purchase)',
                        'support_pct': 'Support % (Frequency in all baskets)'}
            )
            apply_premium_theme(fig_scatter, height=380)
            fig_scatter.update_layout(coloraxis_showscale=False)
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
                    <div style='background: linear-gradient(135deg,
                                  rgba(13,17,23,0.9) 0%, rgba(8,12,24,0.8) 100%);
                                border: 1px solid rgba(139,92,246,0.12);
                                border-radius: 12px; padding: 14px 18px; margin-bottom: 8px;
                                backdrop-filter: blur(20px);
                                transition: all 0.3s ease;'>
                        <div style='display:flex; justify-content:space-between; align-items:center;'>
                            <span style='color:#F8FAFC; font-weight:700; font-size:14px;'>👉 {row['consequents_str']}</span>
                            <span style='background: rgba(139,92,246,0.12);
                                         border: 1px solid rgba(139,92,246,0.25);
                                         color:#A78BFA; font-size:10px; font-weight:700;
                                         padding:2px 8px; border-radius:99px;'>
                                {row['lift']:.2f}x Lift
                            </span>
                        </div>
                        <div style='font-size:11px; color:#475569; margin-top: 4px;'>
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
