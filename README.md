<!-- ═══════════════════════════════════════════════════════════════════
     QC PULSE INDIA — README
     ═══════════════════════════════════════════════════════════════════ -->

<!-- ── HERO HEADER ───────────────────────────────────────────────────── -->

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,20,24&height=220&section=header&text=QC%20Pulse%20India&fontSize=62&fontColor=ffffff&fontAlignY=38&desc=Quick%20Commerce%20Intelligence%20Dashboard&descAlignY=58&descSize=19&descColor=a78bfa&animation=fadeIn" width="100%"/>

<br/>

<!-- ── STATUS BADGES ─────────────────────────────────────────────────── -->

<a href="https://qc-pulse-india.streamlit.app" target="_blank">
  <img src="https://img.shields.io/badge/🚀%20Live%20Demo-Open%20App-7C3AED?style=for-the-badge&logoColor=white" alt="Live Demo"/>
</a>
&nbsp;
<a href="https://github.com/Yashaswini-V21/qc-pulse-india" target="_blank">
  <img src="https://img.shields.io/badge/⭐%20Star%20on-GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/>
</a>
&nbsp;
<img src="https://img.shields.io/badge/Status-Portfolio%20Ready-10B981?style=for-the-badge" alt="Portfolio Ready"/>

<br/><br/>

<!-- ── TECH PILLS ────────────────────────────────────────────────────── -->

<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white"/>
&nbsp;
<img src="https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat-square&logo=streamlit&logoColor=white"/>
&nbsp;
<img src="https://img.shields.io/badge/Plotly-5.x-3F4F75?style=flat-square&logo=plotly&logoColor=white"/>
&nbsp;
<img src="https://img.shields.io/badge/Pandas-2.x-150458?style=flat-square&logo=pandas&logoColor=white"/>
&nbsp;
<img src="https://img.shields.io/badge/SciPy-Stats-4C78A8?style=flat-square"/>
&nbsp;
<img src="https://img.shields.io/badge/mlxtend-Apriori-8B5CF6?style=flat-square"/>
&nbsp;
<img src="https://img.shields.io/badge/License-MIT-10B981?style=flat-square"/>

<br/><br/>

<!-- ── HERO SCREENSHOT ────────────────────────────────────────────────── -->

<a href="https://qc-pulse-india.streamlit.app" target="_blank">
  <img src="public/1.png" alt="QC Pulse India — Overview Dashboard" width="92%" style="border-radius:18px; box-shadow:0 24px 64px rgba(0,0,0,0.55);"/>
</a>

<br/><br/>

<!-- ── STATS ROW ──────────────────────────────────────────────────────── -->

| &nbsp;&nbsp;🛒 **39,357**&nbsp;&nbsp; | &nbsp;&nbsp;📦 **38,765**&nbsp;&nbsp; | &nbsp;&nbsp;👥 **3,898**&nbsp;&nbsp; | &nbsp;&nbsp;🏪 **3**&nbsp;&nbsp; | &nbsp;&nbsp;📊 **9**&nbsp;&nbsp; | &nbsp;&nbsp;🔬 **IQR**&nbsp;&nbsp; |
|:---:|:---:|:---:|:---:|:---:|:---:|
| Products catalogued | Transactions analysed | Customers segmented | Platforms compared | Dashboard modules | Price quality audit |

<br/>

</div>

---

## 📌 Business Questions Answered

- Which platform wins the price war by category?
- Why do 22.8% of customers churn — and what is the revenue risk?
- Which customer acquisition cohort has the highest lifetime value?
- What product category drives the most loyal customers?
- How much revenue can a targeted retention campaign recover?

---

## 🔍 Key Findings (from real data)

- **Champions (20.8%, 809 customers)** order every 58 days with 6.3× avg frequency
- **Churned segment (22.8%, 899 customers)** represents ₹310K+ annual revenue at risk
- **Jun 2015 cohort** achieved 26.3% Month-1 retention — 84% above the 24-cohort average
- **Beverages-first customers** show 24.9% churn rate — highest of any first-category
- **Business simulator** projects ROI of retention campaigns across all 5 RFM segments

> Every number is traceable to a notebook cell. Assumptions are labelled. See [`docs/LIMITATIONS.md`](docs/LIMITATIONS.md).

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Dashboard | Streamlit |
| Data Processing | Python · Pandas · NumPy |
| Visualizations | Plotly |
| Statistical Analysis | SciPy (chi-squared, IQR) · mlxtend (Apriori) |
| Data Pipeline | Jupyter Notebooks (7-step) |
| Deployment | Streamlit Cloud |

> Pipeline outputs feed a dbt-compatible star schema (`fct_orders`, `dim_products`, `dim_platforms`) for downstream analytics engineering workflows.

---

## 📊 Dashboard Pages

<div align="center">

<table>
  <tr>
    <td align="center" width="50%">
      <img src="public/1.png" width="100%" alt="Overview" style="border-radius:12px;"/>
      <br/><sub><b>📊 Overview</b> — Platform KPIs &amp; Intelligence Report</sub>
    </td>
    <td align="center" width="50%">
      <img src="public/2.png" width="100%" alt="Price Intelligence" style="border-radius:12px;"/>
      <br/><sub><b>⚔️ Price Intelligence</b> — Category Price Gap Heatmap</sub>
    </td>
  </tr>
  <tr>
    <td align="center" width="50%">
      <img src="public/4.png" width="100%" alt="Market Basket" style="border-radius:12px;"/>
      <br/><sub><b>🛒 Market Basket</b> — Apriori Association Rules</sub>
    </td>
    <td align="center" width="50%">
      <img src="public/5.png" width="100%" alt="Customer Journey" style="border-radius:12px;"/>
      <br/><sub><b>🌊 Customer Journey</b> — Sankey Flow Diagram</sub>
    </td>
  </tr>
</table>

</div>

<br/>

| Page | What It Shows |
|---|---|
| 📊 Overview + Intelligence Report | Key metrics, auto-generated insights, platform comparison |
| ⚔️ Price Intelligence | Price gap matrix across 15+ categories |
| ⭐ Review & Rating | Rating distributions by platform and category |
| 🛒 Market Basket | Apriori association rules with honest sparse-result disclosure |
| 👥 Customer Segments | RFM treemap, recency vs frequency scatter, chi-squared test |
| 📈 Cohort Retention | 24-cohort heatmap, Month-1 retention trends |
| 🌊 Customer Journey | Sankey: first category → segment → outcome |
| 🎯 Business Simulator | Revenue impact projections for retention campaigns |
| 🔬 Data Quality | IQR outlier detection · missing value audit · methodology map |

---

## 🔢 Key Numbers — Notebook-Verified

```
39,357   products — Blinkit + Zepto + BigBasket catalog CSVs
38,765   grocery transactions (proxy dataset)              [nb 05, Cell 1]
 3,898   unique customers                                  [nb 05, Cell 1]
   809   Champion customers — 20.8% of base               [nb 05, Cell 4]
   899   Churned customers — avg 400 days since last order [nb 05, Cell 5]
   206   At-Risk customers — 5.3% of base                 [nb 05, Cell 4]

Jun-2015 cohort → 26.3% Month-1 retention (avg: 14.3%)   [nb 06, Cell 6]
Beverages first-buyers → 24.9% Churned segment rate       [nb 07, Cell 5]
Champion avg items 16.9 vs Churned 4.7  (3.6× ratio)     [nb 05, Cell 5]

₹350     avg order value                    [assumed — DPIIT/Redseer estimate]
 -2.0    price elasticity (Simulator)       [assumed — standard retail textbook]
```

---

## 🚀 Run Locally

```bash
git clone https://github.com/Yashaswini-V21/qc-pulse-india
cd qc-pulse-india
pip install -r requirements.txt
streamlit run app.py
```

To regenerate all pipeline outputs from raw CSVs:

```bash
python run_pipeline.py   # runs notebooks 01 → 07 in sequence
```

---

## 📁 Project Structure

```
QC_Pulse_India/
│
├── 📄 app.py                      ← Streamlit entrypoint — routing + CSS injection
├── 📄 run_pipeline.py             ← Notebook orchestrator (01 → 07, no silent substitutions)
├── 📄 requirements.txt            ← Pinned Python dependencies
├── 📄 CHANGELOG.md                ← Version history and integrity fix log
│
├── 📁 views/                      ← One module per dashboard page
│   ├── overview.py                  KPI cards + AI story cards
│   ├── price_intelligence.py        Price gap heatmap + platform scorecard
│   ├── review_rating.py             Rating distributions
│   ├── market_basket.py             Apriori rules + honest sparse-result disclosure
│   ├── customer_segments.py         RFM bubble chart + segment table + chi-squared
│   ├── cohort_retention.py          24-month retention heatmap
│   ├── customer_journey.py          Sankey diagram
│   ├── business_simulator.py        4-tab simulator + assumptions expander
│   └── data_quality.py              Live IQR outlier detection
│
├── 📁 utils/                      ← Shared backend utilities
│   ├── data_loader.py               @st.cache_data CSV loader + column validator
│   ├── simulator.py                 Business projection functions (typed params)
│   ├── story_generator.py           Auto-intelligence text — live from DataFrames
│   ├── styles.py                    Dark theme CSS tokens
│   ├── charts.py                    Plotly dark theme config
│   └── config.py                    File paths + constants
│
├── 📁 notebooks/                  ← Data pipeline (run in order)
│   ├── 01_data_load.ipynb
│   ├── 02_cleaning.ipynb
│   ├── 03_price_intelligence.ipynb
│   ├── 04_basket_analysis.ipynb     min_support=0.005 — as written, no substitution
│   ├── 05_rfm_segmentation.ipynb
│   ├── 06_cohort_retention.ipynb
│   ├── 07_sankey.ipynb
│   └── 08_data_quality.ipynb        IQR price audit
│
├── 📁 data/
│   ├── raw/                         Source CSVs (Blinkit, Zepto, BigBasket, Groceries)
│   └── clean/                       Processed outputs consumed by dashboard
│
├── 📁 docs/
│   ├── LIMITATIONS.md              ← ⭐ L1–L5 data caveat disclosure
│   ├── data_schema.md
│   └── DEVELOPER_GUIDE.md
│
└── 📁 tests/
    └── test_data_loader.py
```

---

## 👤 Author

**Yashaswini V** · [LinkedIn](https://linkedin.com/in/yashaswini21) · [GitHub](https://github.com/Yashaswini-V21)

---

<!-- ── FOOTER ──────────────────────────────────────────────────────────── -->

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,20,24&height=140&section=footer&text=Built%20with%20honest%20data%20%26%20clean%20code&fontSize=16&fontColor=a78bfa&fontAlignY=65&animation=fadeIn" width="100%"/>

<div align="center">

<br/>

<a href="https://github.com/Yashaswini-V21" target="_blank">
  <img src="https://img.shields.io/badge/GitHub-Yashaswini--V21-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub Profile"/>
</a>
&nbsp;
<a href="https://qc-pulse-india.streamlit.app" target="_blank">
  <img src="https://img.shields.io/badge/🚀%20Live-Dashboard-7C3AED?style=for-the-badge&logo=streamlit&logoColor=white" alt="Live Dashboard"/>
</a>
&nbsp;
<a href="docs/LIMITATIONS.md">
  <img src="https://img.shields.io/badge/📋%20Read-Limitations-F59E0B?style=for-the-badge" alt="Limitations"/>
</a>

<br/><br/>

<sub><i>QC Pulse India &nbsp;·&nbsp; MIT Licensed &nbsp;·&nbsp; Made with Python, Streamlit &amp; honest data work &nbsp;·&nbsp; 2026</i></sub>

<br/>

</div>
