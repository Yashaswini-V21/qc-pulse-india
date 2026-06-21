<!--
███████████████████████████████████████████████████████████████████████████████
                           QC PULSE INDIA
            Quick Commerce Analytics · Blinkit · Zepto · BigBasket
███████████████████████████████████████████████████████████████████████████████
-->

<div align="center">

<br/>

<!-- ─── HERO TITLE ─────────────────────────────────────────────────────────── -->

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,20,24&height=200&section=header&text=QC%20Pulse%20India&fontSize=56&fontColor=ffffff&fontAlignY=38&desc=Quick%20Commerce%20Intelligence%20Dashboard&descAlignY=58&descSize=18&descColor=a78bfa&animation=fadeIn" width="100%"/>

<br/>

<!-- ─── STATUS BADGES ──────────────────────────────────────────────────────── -->

<a href="https://qc-pulse-india.streamlit.app" target="_blank">
  <img src="https://img.shields.io/badge/🚀%20Live%20Demo-Open%20App-7C3AED?style=for-the-badge&logoColor=white" alt="Live Demo"/>
</a>
&nbsp;
<a href="https://github.com/Yashaswini-V21/qc-pulse-india" target="_blank">
  <img src="https://img.shields.io/badge/⭐%20Star%20on-GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/>
</a>
&nbsp;
<img src="https://img.shields.io/badge/Status-Portfolio%20Ready-10B981?style=for-the-badge" alt="Status"/>

<br/><br/>

<!-- ─── TECH STACK PILLS ───────────────────────────────────────────────────── -->

<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white"/>
&nbsp;
<img src="https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat-square&logo=streamlit&logoColor=white"/>
&nbsp;
<img src="https://img.shields.io/badge/Plotly-5.x-3F4F75?style=flat-square&logo=plotly&logoColor=white"/>
&nbsp;
<img src="https://img.shields.io/badge/Pandas-2.x-150458?style=flat-square&logo=pandas&logoColor=white"/>
&nbsp;
<img src="https://img.shields.io/badge/mlxtend-Apriori-8B5CF6?style=flat-square"/>
&nbsp;
<img src="https://img.shields.io/badge/scipy-IQR%20Stats-4C78A8?style=flat-square"/>
&nbsp;
<img src="https://img.shields.io/badge/License-MIT-10B981?style=flat-square"/>

<br/><br/>

<!-- ─── HERO DASHBOARD SCREENSHOT ─────────────────────────────────────────── -->

<a href="https://qc-pulse-india.streamlit.app" target="_blank">
  <img src="public/1.png" alt="QC Pulse India — Overview Dashboard" width="90%" style="border-radius:16px; box-shadow:0 20px 60px rgba(0,0,0,0.5);"/>
</a>

<br/><br/>

<!-- ─── STATS ROW ──────────────────────────────────────────────────────────── -->

| &nbsp;&nbsp;🛒 **39,357**&nbsp;&nbsp; | &nbsp;&nbsp;📦 **38,765**&nbsp;&nbsp; | &nbsp;&nbsp;👥 **3,898**&nbsp;&nbsp; | &nbsp;&nbsp;🏪 **3**&nbsp;&nbsp; | &nbsp;&nbsp;📊 **9**&nbsp;&nbsp; | &nbsp;&nbsp;🔬 **IQR**&nbsp;&nbsp; |
|:---:|:---:|:---:|:---:|:---:|:---:|
| Products catalogued | Transactions analysed | Customers segmented | Platforms compared | Dashboard modules | Price quality audit |

<br/>

</div>

---

<!-- ════════════════════════════════════════════════════════════════════════════
     SECTION 1 — ABOUT
     ════════════════════════════════════════════════════════════════════════════ -->

## 🧠 About This Project

**QC Pulse India** is a portfolio-grade data analytics dashboard that benchmarks India's three largest quick commerce platforms — **Blinkit**, **Zepto**, and **BigBasket** — across price competitiveness, customer behaviour, and platform rating quality.

Built entirely in Python with Streamlit and Plotly, it demonstrates **end-to-end analytical thinking**: from raw CSV ingestion and exploratory analysis through RFM segmentation, cohort retention modelling, market basket rules, and a what-if business simulator — all in a **9-module dark-theme dashboard**.

> **Interview-ready by design.** Every claim is traced to a notebook cell. Every assumption is labelled. Every limitation is documented. See [`docs/LIMITATIONS.md`](docs/LIMITATIONS.md).

---

<!-- ════════════════════════════════════════════════════════════════════════════
     SECTION 2 — DATA TRANSPARENCY
     ════════════════════════════════════════════════════════════════════════════ -->

## ⚠️ Data Sources — Full Transparency

> Two distinct datasets are used. Read this before citing any numbers.

| Pages | Data Source | Type |
|---|---|:---:|
| 1–3 · Overview, Price, Reviews | Real Kaggle CSVs — Blinkit, Zepto, BigBasket product listings | ✅ Real |
| 4–7 · Basket, RFM, Cohort, Journey | Public grocery benchmark (2014–2015 Western supermarket transactions) | ⚠️ Proxy |
| 8 · Business Simulator | Mixed — RFM/cohort from proxy; `₹350` avg order = industry estimate | ⚠️ Modelled |
| 9 · Data Quality | Raw platform CSVs — IQR computed live each session | ✅ Live |

→ Full caveats in [`docs/LIMITATIONS.md`](docs/LIMITATIONS.md) · covers L1 (dataset mismatch) through L5 (imputed Blinkit discounts)

---

<!-- ════════════════════════════════════════════════════════════════════════════
     SECTION 3 — DASHBOARD SCREENSHOTS
     ════════════════════════════════════════════════════════════════════════════ -->

## 📸 Dashboard Previews

<div align="center">

<table>
  <tr>
    <td align="center" width="50%">
      <img src="public/1.png" width="100%" alt="Overview"/>
      <br/><sub><b>📊 Overview</b> — Platform KPIs & Category Breakdown</sub>
    </td>
    <td align="center" width="50%">
      <img src="public/2.png" width="100%" alt="Price Intelligence"/>
      <br/><sub><b>⚔️ Price Intelligence</b> — Category Price Gap Heatmap</sub>
    </td>
  </tr>
  <tr>
    <td align="center" width="50%">
      <img src="public/4.png" width="100%" alt="Market Basket"/>
      <br/><sub><b>🛒 Market Basket</b> — Apriori Association Rules</sub>
    </td>
    <td align="center" width="50%">
      <img src="public/5.png" width="100%" alt="Customer Journey"/>
      <br/><sub><b>🌊 Customer Journey</b> — Sankey Flow Diagram</sub>
    </td>
  </tr>
</table>

</div>

---

<!-- ════════════════════════════════════════════════════════════════════════════
     SECTION 4 — 9 MODULES
     ════════════════════════════════════════════════════════════════════════════ -->

## 📋 9 Dashboard Modules

| # | Module | Source | What it Analyses |
|:---:|---|:---:|---|
| 1 | 📊 **Overview** | Platform CSVs | Product counts, KPI cards, platform share, AI-generated insights |
| 2 | ⚔️ **Price Intelligence** | Platform CSVs | Price gap heatmap — who is cheapest per category |
| 3 | ⭐ **Review & Rating** | Blinkit + BigBasket | Rating distributions and averages by platform and category |
| 4 | 🛒 **Market Basket** | Grocery proxy | Apriori rules · sparse result disclosed with analyst note |
| 5 | 👥 **Customer Segments** | Grocery proxy | RFM quintile scoring — Champions · Loyal · Potential · At-Risk · Churned |
| 6 | 📈 **Cohort Retention** | Grocery proxy | 24-month retention heatmap with Month-1 trend line |
| 7 | 🌊 **Customer Journey** | Grocery proxy | Sankey: first purchase category → RFM segment → outcome |
| 8 | 🎯 **Business Simulator** | Proxy + assumptions | Win-back ROI · price elasticity curve · retention LTV uplift |
| 9 | 🔬 **Data Quality** `NEW` | Platform CSVs (live) | IQR outlier detection · missing value audit · methodology map |

---

<!-- ════════════════════════════════════════════════════════════════════════════
     SECTION 5 — KEY NUMBERS
     ════════════════════════════════════════════════════════════════════════════ -->

## 🔢 Key Numbers — All Notebook-Verified

> Every number below is traceable to a specific notebook cell output.
> Numbers marked `[assumed]` are estimates, **not** derived from data.

```
39,357   products — Blinkit + Zepto + BigBasket catalog CSVs
38,765   grocery transactions (proxy dataset)              [nb 05, Cell 1]
 3,898   unique customers in proxy dataset                 [nb 05, Cell 1]
   809   Champion customers — 20.8% of base               [nb 05, Cell 4]
   889   Churned customers — avg 400 days since last order [nb 05, Cell 5]
   206   At-Risk customers — 5.3% of base                 [nb 05, Cell 4]

Jun-2015 cohort → 26.3% Month-1 retention (avg: 14.3%)   [nb 06, Cell 6]
Beverages first-buyers → 24.9% Churned segment rate       [nb 07, Cell 5]
Champion avg items 16.9 vs Churned 4.7  (3.6× ratio)     [nb 05, Cell 5]

₹350     avg order value                    [assumed — DPIIT/Redseer estimate]
 -2.0    price elasticity (Simulator)       [assumed — standard retail textbook]
```

---

<!-- ════════════════════════════════════════════════════════════════════════════
     SECTION 6 — ARCHITECTURE
     ════════════════════════════════════════════════════════════════════════════ -->

## 🏗️ Architecture

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
│   ├── customer_segments.py         RFM bubble chart + segment table
│   ├── cohort_retention.py          24-month retention heatmap
│   ├── customer_journey.py          Sankey diagram
│   ├── business_simulator.py        3-tab simulator + assumptions expander
│   └── data_quality.py             ← NEW — live IQR outlier detection
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
│   └── 08_data_quality.ipynb      ← NEW — IQR price audit
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

<!-- ════════════════════════════════════════════════════════════════════════════
     SECTION 7 — QUICK START
     ════════════════════════════════════════════════════════════════════════════ -->

## 🚀 Quick Start

```bash
# 1 — Clone the repo
git clone https://github.com/Yashaswini-V21/qc-pulse-india.git
cd QC_Pulse_India

# 2 — Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux

# 3 — Install all dependencies
pip install -r requirements.txt

# 4 — Run the data pipeline  (generates all clean/ CSVs)
python run_pipeline.py

# 5 — Launch the dashboard
streamlit run app.py
```

> **Note on step 4:** Runs notebooks 01 → 07. The Data Quality page (module 9) computes
> its IQR statistics live from raw CSVs — notebook 08 is optional standalone audit.

---

<!-- ════════════════════════════════════════════════════════════════════════════
     SECTION 8 — INTERVIEW DEFENCE TABLE
     ════════════════════════════════════════════════════════════════════════════ -->

## 🎯 Interview Defence — "Walk me through that number"

> Use this table when a recruiter asks you to justify a claim.

| Claim | Evidence | File |
|---|---|---|
| 3,898 customers, 38,765 transactions | Notebook 05, Cell 1 output | `notebooks/05_rfm_segmentation.ipynb` |
| 24.9% Beverages churn rate | Notebook 07, Cell 5 output | `notebooks/07_sankey.ipynb` |
| Jun-2015 → 26.3% Month-1 retention | Notebook 06, Cell 6 output | `notebooks/06_cohort_retention.ipynb` |
| Basket analysis: 1 rule (honest) | Analyst note + `min_support=0.005` not touched | `views/market_basket.py` |
| Zepto price anomaly flagged | IQR fence: Beverages median ₹9,500 detected | `views/data_quality.py` |
| ₹350 avg order is an assumption | Assumptions expander in Simulator | `views/business_simulator.py` |
| RFM threshold ≥13 = Champion | Quintile scoring, documented in notebook | `notebooks/05_rfm_segmentation.ipynb` |

---

<!-- ════════════════════════════════════════════════════════════════════════════
     SECTION 9 — LICENSE
     ════════════════════════════════════════════════════════════════════════════ -->

## 📄 License

Distributed under the **MIT License** — see [`LICENSE`](LICENSE) for details.

---

<!-- ════════════════════════════════════════════════════════════════════════════
     FOOTER
     ════════════════════════════════════════════════════════════════════════════ -->

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,20,24&height=130&section=footer&text=Built%20for%20defensibility%2C%20not%20just%20impressiveness&fontSize=16&fontColor=a78bfa&fontAlignY=65&animation=fadeIn" width="100%"/>

<div align="center">

<br/>

**Yashaswini V** &nbsp;·&nbsp; Data Analytics Portfolio &nbsp;·&nbsp; June 2026

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

<sub>
  <i>QC Pulse India · MIT Licensed · Made with Python, Streamlit &amp; honest data work</i>
</sub>

<br/>

</div>
