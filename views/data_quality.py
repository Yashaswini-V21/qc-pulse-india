"""
views/data_quality.py
─────────────────────
Data Quality & Methodology Transparency page for QC Pulse India.
Shows IQR outlier detection results, missing value audit, and
platform-level data quality scores — computed from notebook 08 output.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ── Design tokens ─────────────────────────────────────────────
_BG       = "#060B14"
_CARD_BG  = "linear-gradient(135deg, #0F1C2E, #0D1823)"
_BORDER   = "linear-gradient(90deg, #06B6D4, #7C3AED)"
_CYAN     = "#06B6D4"
_AMBER    = "#F59E0B"
_GREEN    = "#10B981"
_RED      = "#EF4444"
_PURPLE   = "#7C3AED"
_LABEL_C  = "#64748B"
_VALUE_C  = "#F1F5F9"
_PLOT_BG  = "#0D1823"
_HOVER_BG = "#0F1C2E"
_HOVER_BD = "#1E2D40"

PLATFORM_COLORS = {
    "Blinkit":   "#FF3366",
    "Zepto":     "#00F5A0",
    "BigBasket": "#B923FF",
}


def _kpi_card(label: str, value: str, delta: str = "", color: str = _VALUE_C) -> str:
    delta_html = (
        f"<div style='font-family:\"Space Mono\",monospace;font-size:10px;"
        f"color:{_LABEL_C};margin-top:6px;'>{delta}</div>"
    ) if delta else ""
    return f"""
    <div style="
        background: {_CARD_BG};
        border-radius: 14px; padding: 20px 22px;
        position: relative; overflow: hidden;
        box-shadow: 0 8px 24px rgba(0,0,0,0.4);
    ">
        <div style="position:absolute;top:0;left:0;right:0;height:2px;
            background:{_BORDER};"></div>
        <div style="font-family:'Space Mono',monospace;font-size:10px;
            text-transform:uppercase;color:{_LABEL_C};letter-spacing:0.12em;
            margin-bottom:8px;">{label}</div>
        <div style="font-family:'DM Sans',sans-serif;font-weight:700;
            font-size:28px;color:{color};line-height:1.1;">{value}</div>
        {delta_html}
    </div>
    """


def _status_badge(status: str) -> str:
    if status == "PASS":
        return f"<span style='background:rgba(16,185,129,0.15);border:1px solid rgba(16,185,129,0.4);color:{_GREEN};font-family:Space Mono,monospace;font-size:9px;font-weight:700;padding:2px 8px;border-radius:99px;'>✓ PASS</span>"
    elif status == "WARN":
        return f"<span style='background:rgba(245,158,11,0.15);border:1px solid rgba(245,158,11,0.4);color:{_AMBER};font-family:Space Mono,monospace;font-size:9px;font-weight:700;padding:2px 8px;border-radius:99px;'>⚠ WARN</span>"
    else:
        return f"<span style='background:rgba(239,68,68,0.15);border:1px solid rgba(239,68,68,0.4);color:{_RED};font-family:Space Mono,monospace;font-size:9px;font-weight:700;padding:2px 8px;border-radius:99px;'>✗ FAIL</span>"


def _run_iqr_analysis(df: pd.DataFrame, price_col: str, platform: str) -> dict:
    """Run IQR outlier detection on a platform's price column. Returns stats dict."""
    if price_col not in df.columns:
        return {}
    prices = df[price_col].dropna()
    Q1 = prices.quantile(0.25)
    Q3 = prices.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 3 * IQR
    upper = Q3 + 3 * IQR
    outliers = df[(df[price_col] < lower) | (df[price_col] > upper)]
    return {
        "platform": platform,
        "total": len(df),
        "Q1": round(Q1, 0),
        "Q3": round(Q3, 0),
        "IQR": round(IQR, 0),
        "lower_fence": round(lower, 0),
        "upper_fence": round(upper, 0),
        "n_outliers": len(outliers),
        "pct_outliers": round(len(outliers) / len(df) * 100, 1),
        "median": round(prices.median(), 0),
        "max_price": round(prices.max(), 0),
        "outlier_df": outliers,
        "price_col": price_col,
    }


def render_data_quality(
    bl: pd.DataFrame,
    ze: pd.DataFrame,
    bb: pd.DataFrame,
) -> None:
    """Renders the Data Quality & Methodology Transparency dashboard page."""

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
        ">● DATA QUALITY AUDIT</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <h1 style="
        font-family:'DM Sans',sans-serif !important;
        font-size:28px !important; font-weight:700 !important;
        color:#F1F5F9 !important;
        -webkit-text-fill-color:#F1F5F9 !important;
        background:none !important;
        margin:10px 0 6px !important;
        letter-spacing:-0.02em !important;
    ">Data Quality & Methodology</h1>
    <p style="
        font-family:'DM Sans',sans-serif;
        font-size:14px; color:{_LABEL_C};
        margin:0 0 8px;
    ">IQR outlier detection · Missing value audit · Platform data reliability scores</p>
    <p style="
        font-family:'Space Mono',monospace;
        font-size:10px; color:#334155;
        margin:0 0 24px;
    ">Computed live from raw CSVs — every number on this page is derived in this session, not pre-calculated.</p>
    """, unsafe_allow_html=True)

    # ── METHODOLOGY CALLOUT ──
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(6,182,212,0.07), rgba(124,58,237,0.05));
        border: 1px solid rgba(6,182,212,0.2);
        border-radius: 12px; padding: 16px 20px; margin-bottom: 24px;
    ">
        <div style="font-family:'Space Mono',monospace;font-size:10px;text-transform:uppercase;
            color:{_CYAN};letter-spacing:0.1em;margin-bottom:8px;font-weight:700;">
            Why This Page Exists
        </div>
        <div style="font-family:'DM Sans',sans-serif;font-size:13px;color:#94A3B8;line-height:1.7;">
            During analysis, notebook 03 revealed that Zepto's <b>Beverages median price = ₹9,500</b>
            and <b>Personal Care median = ₹16,200</b> — implausible for a grocery quick-commerce platform.
            Real analyst work requires <b>detecting and disclosing data quality issues before drawing conclusions.</b>
            This page runs IQR outlier detection programmatically and flags categories that should be
            excluded from cross-platform price comparisons until the source CSV is verified.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── LIVE IQR ANALYSIS ──
    price_col_map = {
        "Blinkit":   ("sale_price", bl),
        "Zepto":     ("sale_price", ze),
        "BigBasket": ("sale_price", bb),
    }

    iqr_stats = {}
    for platform, (col, df) in price_col_map.items():
        stats = _run_iqr_analysis(df, col, platform)
        if stats:
            iqr_stats[platform] = stats

    # ── KPI ROW ──
    total_products = sum(len(df) for _, (_, df) in price_col_map.items())
    total_outliers = sum(s["n_outliers"] for s in iqr_stats.values())
    overall_pct = round(total_outliers / total_products * 100, 1)
    platforms_with_issues = sum(1 for s in iqr_stats.values() if s["pct_outliers"] > 5)

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(_kpi_card("PRODUCTS AUDITED", f"{total_products:,}", "across 3 platform CSVs"), unsafe_allow_html=True)
    with k2:
        col = _RED if total_outliers > 0 else _GREEN
        st.markdown(_kpi_card("PRICE OUTLIERS", f"{total_outliers:,}", f"{overall_pct}% of all products", color=col), unsafe_allow_html=True)
    with k3:
        col = _RED if platforms_with_issues > 1 else (_AMBER if platforms_with_issues == 1 else _GREEN)
        st.markdown(_kpi_card("PLATFORMS FLAGGED", str(platforms_with_issues), "with >5% outlier rate", color=col), unsafe_allow_html=True)
    with k4:
        method_txt = "IQR × 3 (extreme)"
        st.markdown(_kpi_card("DETECTION METHOD", "IQR ×3", "Q1−3×IQR, Q3+3×IQR fences", color=_CYAN), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── PER-PLATFORM IQR CARDS ──
    st.markdown(f"""
    <div style="font-family:'Space Mono',monospace;font-size:10px;
        text-transform:uppercase;color:{_LABEL_C};letter-spacing:0.12em;
        margin-bottom:16px;">Platform Price Distribution — IQR Analysis</div>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    for i, (platform, stats) in enumerate(iqr_stats.items()):
        pct = stats["pct_outliers"]
        status = "PASS" if pct < 2 else ("WARN" if pct < 10 else "FAIL")
        badge = _status_badge(status)
        color = PLATFORM_COLORS.get(platform, _VALUE_C)

        with cols[i]:
            st.markdown(f"""
            <div style="
                background: {_CARD_BG};
                border-radius: 14px; padding: 20px 22px;
                position: relative; overflow: hidden;
                box-shadow: 0 8px 24px rgba(0,0,0,0.4);
                border-left: 3px solid {color};
            ">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                    <div style="font-family:'DM Sans',sans-serif;font-weight:700;
                        font-size:16px;color:{color};">{platform}</div>
                    {badge}
                </div>
                <div style="font-family:'Space Mono',monospace;font-size:10px;
                    color:{_LABEL_C};line-height:2;">
                    Total rows: <span style="color:{_VALUE_C}">{stats['total']:,}</span><br>
                    Median price: <span style="color:{_VALUE_C}">₹{stats['median']:,.0f}</span><br>
                    IQR fence: <span style="color:{_VALUE_C}">₹{stats['lower_fence']:,.0f} → ₹{stats['upper_fence']:,.0f}</span><br>
                    Outliers: <span style="color:{'#EF4444' if pct > 5 else _VALUE_C}">{stats['n_outliers']:,} ({pct}%)</span><br>
                    Max price seen: <span style="color:{'#EF4444' if stats['max_price'] > 5000 else _VALUE_C}">₹{stats['max_price']:,.0f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── PRICE DISTRIBUTION CHART ──
    st.markdown(f"""
    <div style="font-family:'Space Mono',monospace;font-size:10px;
        text-transform:uppercase;color:{_LABEL_C};letter-spacing:0.12em;
        margin-bottom:12px;">Price Distribution — Log Scale (reveals outlier spread)</div>
    """, unsafe_allow_html=True)

    fig = go.Figure()
    for platform, (col, df) in price_col_map.items():
        if col not in df.columns:
            continue
        prices = df[col].dropna()
        prices_clipped = prices[prices > 0]  # log scale needs positive values
        fig.add_trace(go.Box(
            y=prices_clipped,
            name=platform,
            marker_color=PLATFORM_COLORS.get(platform, "#94A3B8"),
            boxpoints="outliers",
            jitter=0.3,
            pointpos=-1.8,
            marker=dict(size=3, opacity=0.5),
            line=dict(width=1.5),
        ))

    fig.update_layout(
        plot_bgcolor=_PLOT_BG,
        paper_bgcolor=_PLOT_BG,
        font=dict(family="DM Sans", color="#94A3B8", size=11),
        margin=dict(l=10, r=10, t=10, b=10),
        height=380,
        yaxis=dict(
            type="log",
            title="Sale Price ₹ (log scale)",
            gridcolor="#1E2D40",
            color="#94A3B8",
        ),
        xaxis=dict(color="#94A3B8"),
        hoverlabel=dict(bgcolor=_HOVER_BG, bordercolor=_HOVER_BD, font=dict(color="white", size=12)),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── CATEGORY-LEVEL ISSUE FINDER ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-family:'Space Mono',monospace;font-size:10px;
        text-transform:uppercase;color:{_LABEL_C};letter-spacing:0.12em;
        margin-bottom:12px;">Category Median Price Sanity Check (threshold: ₹5,000)</div>
    """, unsafe_allow_html=True)

    THRESHOLD = 5000
    issue_rows = []
    for platform, (price_col, df) in price_col_map.items():
        if price_col not in df.columns or "category" not in df.columns:
            continue
        cat_med = df.groupby("category")[price_col].median().reset_index()
        cat_med.columns = ["category", "median_price"]
        flagged = cat_med[cat_med["median_price"] > THRESHOLD]
        for _, row in flagged.iterrows():
            issue_rows.append({
                "Platform": platform,
                "Category": row["category"],
                "Median Price (₹)": f"₹{row['median_price']:,.0f}",
                "Verdict": "Likely data error — exclude from comparison",
            })

    if issue_rows:
        issues_df = pd.DataFrame(issue_rows)
        # Render as styled HTML table
        rows_html = ""
        for _, row in issues_df.iterrows():
            rows_html += f"""
            <tr style="border-bottom:1px solid #1E2D40;">
                <td style="padding:10px 14px;color:{PLATFORM_COLORS.get(row['Platform'], _VALUE_C)};
                    font-weight:700;font-family:'DM Sans',sans-serif;">{row['Platform']}</td>
                <td style="padding:10px 14px;color:{_VALUE_C};font-family:'DM Sans',sans-serif;">{row['Category']}</td>
                <td style="padding:10px 14px;color:#EF4444;font-family:'Space Mono',monospace;
                    font-weight:700;">{row['Median Price (₹)']}</td>
                <td style="padding:10px 14px;font-family:'Space Mono',sans-serif;font-size:11px;color:{_AMBER};">{row['Verdict']}</td>
            </tr>
            """
        st.markdown(f"""
        <div style="background:{_CARD_BG};border-radius:12px;overflow:hidden;
            box-shadow:0 8px 24px rgba(0,0,0,0.4);">
            <table style="width:100%;border-collapse:collapse;">
                <thead>
                    <tr style="background:rgba(239,68,68,0.08);border-bottom:1px solid rgba(239,68,68,0.2);">
                        <th style="padding:10px 14px;text-align:left;font-family:'Space Mono',monospace;
                            font-size:9px;text-transform:uppercase;letter-spacing:0.1em;color:{_RED};">Platform</th>
                        <th style="padding:10px 14px;text-align:left;font-family:'Space Mono',monospace;
                            font-size:9px;text-transform:uppercase;letter-spacing:0.1em;color:{_RED};">Category</th>
                        <th style="padding:10px 14px;text-align:left;font-family:'Space Mono',monospace;
                            font-size:9px;text-transform:uppercase;letter-spacing:0.1em;color:{_RED};">Median Price</th>
                        <th style="padding:10px 14px;text-align:left;font-family:'Space Mono',monospace;
                            font-size:9px;text-transform:uppercase;letter-spacing:0.1em;color:{_RED};">Verdict</th>
                    </tr>
                </thead>
                <tbody>{rows_html}</tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.success("✅ No category-level price anomalies detected above ₹5,000 threshold.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── METHODOLOGY TRANSPARENCY SECTION ──
    st.markdown(f"""
    <div style="font-family:'Space Mono',monospace;font-size:10px;
        text-transform:uppercase;color:{_LABEL_C};letter-spacing:0.12em;
        margin-bottom:16px;">Project Methodology & Data Source Map</div>
    """, unsafe_allow_html=True)

    method_rows = [
        ("Pages 1–3 (Overview, Price, Reviews)", "Blinkit, Zepto, BigBasket Kaggle CSVs", "Real platform product listings", "PASS"),
        ("Pages 4 (Market Basket)", "groceries_clean.csv (2014–2015)", "Western grocery benchmark — methodology demo", "WARN"),
        ("Pages 5–7 (RFM, Cohort, Sankey)", "groceries_clean.csv (2014–2015)", "Western grocery benchmark — methodology demo", "WARN"),
        ("Page 8 (Business Simulator)", "Mixed — cohort/RFM from proxy; ₹350 is assumed", "Projections are illustrative, not data-derived", "WARN"),
        ("Page 9 (This page)", "Raw platform CSVs — computed live this session", "IQR detection runs on real CSVs every load", "PASS"),
    ]

    rows_html = ""
    for page, source, note, status in method_rows:
        badge = _status_badge(status)
        rows_html += f"""
        <tr style="border-bottom:1px solid #1E2D40;">
            <td style="padding:10px 14px;color:{_VALUE_C};font-family:'DM Sans',sans-serif;font-size:13px;">{page}</td>
            <td style="padding:10px 14px;color:{_CYAN};font-family:'Space Mono',monospace;font-size:10px;">{source}</td>
            <td style="padding:10px 14px;color:{_LABEL_C};font-family:'DM Sans',sans-serif;font-size:12px;">{note}</td>
            <td style="padding:10px 14px;">{badge}</td>
        </tr>
        """

    st.markdown(f"""
    <div style="background:{_CARD_BG};border-radius:12px;overflow:hidden;
        box-shadow:0 8px 24px rgba(0,0,0,0.4);">
        <table style="width:100%;border-collapse:collapse;">
            <thead>
                <tr style="background:rgba(6,182,212,0.06);border-bottom:1px solid rgba(6,182,212,0.15);">
                    <th style="padding:10px 14px;text-align:left;font-family:'Space Mono',monospace;
                        font-size:9px;text-transform:uppercase;letter-spacing:0.1em;color:{_CYAN};">Dashboard Section</th>
                    <th style="padding:10px 14px;text-align:left;font-family:'Space Mono',monospace;
                        font-size:9px;text-transform:uppercase;letter-spacing:0.1em;color:{_CYAN};">Data Source</th>
                    <th style="padding:10px 14px;text-align:left;font-family:'Space Mono',monospace;
                        font-size:9px;text-transform:uppercase;letter-spacing:0.1em;color:{_CYAN};">Notes</th>
                    <th style="padding:10px 14px;text-align:left;font-family:'Space Mono',monospace;
                        font-size:9px;text-transform:uppercase;letter-spacing:0.1em;color:{_CYAN};">Status</th>
                </tr>
            </thead>
            <tbody>{rows_html}</tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)
