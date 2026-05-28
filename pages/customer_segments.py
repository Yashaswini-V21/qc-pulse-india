"""
Customer Segments page - RFM segmentation analysis.

Purpose:
  Display RFM (Recency, Frequency, Monetary) customer segments.
  Show segment distribution and characteristics.

Data Used:
  - rfm (customer RFM scores and segments)
  - rfm_sum (aggregate segment statistics)
"""
import streamlit as st
import pandas as pd
import plotly.express as px


def render(
    blinkit: pd.DataFrame,
    zepto: pd.DataFrame,
    bigbasket: pd.DataFrame,
    groceries: pd.DataFrame,
    rfm: pd.DataFrame,
    rfm_sum: pd.DataFrame,
    price_mat: pd.DataFrame,
    cohort: pd.DataFrame,
    sankey_df: pd.DataFrame,
) -> None:
    """Render customer segments page."""
    st.markdown("""
    <style>
        .segment-title {
            font-size: 36px;
            font-weight: 800;
            letter-spacing: -0.02em;
            background: linear-gradient(135deg, #60A5FA 0%, #A78BFA 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 8px;
        }
        .segment-subtitle {
            font-size: 16px;
            color: #94A3B8;
            font-weight: 500;
        }
    </style>
    <h1 class="segment-title">🎯 Customer Segments</h1>
    <p class="segment-subtitle">RFM Analysis across 3,898 Customers · Recency · Frequency · Monetary Value</p>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    # KPIs from rfm_summary
    champions = rfm_sum[rfm_sum['segment']=='Champion'].iloc[0]
    churned   = rfm_sum[rfm_sum['segment']=='Churned'].iloc[0]
    
    st.markdown("<p class='section-label'>Quick Metrics</p>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4, gap="medium")
    with c1:
        st.metric("👥 Total Customers", f"{len(rfm):,}")
    with c2:
        st.metric("👑 Champions", f"{int(champions['customers']):,}", f"{champions['pct_customers']}%")
    with c3:
        st.metric("❌ Churned", f"{int(churned['customers']):,}", f"{churned['pct_customers']}%")
    with c4:
        st.metric("📊 Avg Frequency", f"{champions['avg_frequency']:.1f}", "(Champions)")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("<p class='section-label'>Segment Analysis</p>", unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        st.markdown("<p class='section-label'>Distribution by Segment</p>", unsafe_allow_html=True)
        fig1 = px.treemap(
            rfm, path=['segment'], values='RFM_Score', color='RFM_Score',
            color_continuous_scale='Purples'
        )
        fig1.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E2E8F0', size=13),
            margin=dict(l=0,r=0,t=10,b=0),
            hovermode='closest'
        )
        fig1.update_traces(textinfo='label+percent entry', textfont_color='white')
        st.plotly_chart(fig1, width='stretch')
    
    with col2:
        st.markdown("<p class='section-label'>Recency vs Frequency</p>", unsafe_allow_html=True)
        fig2 = px.scatter(
            rfm, x='recency', y='frequency', color='segment', size='monetary',
            color_discrete_map={
                'Champion':'#10B981','Loyal':'#06B6D4',
                'Potential':'#8B5CF6','At-Risk':'#F59E0B','Churned':'#EF4444'
            },
            labels={'recency':'Days Since Order','frequency':'Order Count'},
            hover_data={'monetary': ':.0f'}
        )
        fig2.update_layout(
            height=400,
            plot_bgcolor='rgba(30, 41, 59, 0.3)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E2E8F0', size=11),
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#E2E8F0')),
            margin=dict(l=0,r=0,t=10,b=0),
            hovermode='closest'
        )
        fig2.update_xaxes(color='#94A3B8', gridcolor='rgba(51, 65, 85, 0.2)')
        fig2.update_yaxes(color='#94A3B8', gridcolor='rgba(51, 65, 85, 0.2)')
        st.plotly_chart(fig2, width='stretch')
    
    # Segment table
    st.markdown("---")
    st.markdown("<p class='section-label'>Segment Summary</p>", unsafe_allow_html=True)
        )
        fig1.update_layout(
            height=380, paper_bgcolor='#1E293B',
            font=dict(color='white',size=13), margin=dict(l=0,r=0,t=10,b=0)
        )
        fig1.update_traces(textinfo='label+percent entry')
        st.plotly_chart(fig1, width='stretch')
    
    with col2:
        st.markdown("<p class='section-label'>Recency vs Frequency by Segment</p>", unsafe_allow_html=True)
        fig2 = px.scatter(
            rfm, x='recency', y='frequency', color='segment', size='monetary',
            color_discrete_map={
                'Champion':'#DC2626','Loyal':'#F97316',
                'Potential':'#6C63DB','At-Risk':'#F59E0B','Churned':'#64748B'
            },
            labels={'recency':'Days Since Last Order','frequency':'Number of Orders'}
        )
        fig2.update_layout(
            height=380, plot_bgcolor='#1E293B', paper_bgcolor='#1E293B',
            font=dict(color='white',size=11),
            legend=dict(bgcolor='rgba(0,0,0,0)',font=dict(color='white')),
            margin=dict(l=0,r=0,t=10,b=0)
        )
        fig2.update_xaxes(color='white', gridcolor='#334155')
        fig2.update_yaxes(color='white', gridcolor='#334155')
        st.plotly_chart(fig2, width='stretch')
    
    # Segment table
    st.markdown("---")
    st.markdown("<p class='section-label'>Segment Summary Table</p>", unsafe_allow_html=True)
    display_cols = ['segment','customers','pct_customers','avg_recency','avg_frequency','avg_monetary','avg_rfm_score']
    st.dataframe(
        rfm_sum[display_cols].sort_values('avg_rfm_score', ascending=False),
        width='stretch', hide_index=True
    )
