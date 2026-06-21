# Changelog

All notable changes to QC Pulse India are documented here.

Format: `[version] — date — type — description`

---

## [v1.3.0] — June 2026 — Feature + Integrity

### 🆕 Added
- **Page 9: Data Quality & Methodology** (`views/data_quality.py`)
  - Live IQR outlier detection (3×IQR extreme fence) on all 3 platform price CSVs
  - Price distribution box plots on log scale — reveals outlier spread visually
  - Per-platform PASS/WARN/FAIL quality badges
  - Category-level sanity check (flags medians > ₹5,000)
  - Full methodology transparency table — maps every dashboard section to its data source
- **Notebook 08** (`notebooks/08_data_quality.ipynb`)
  - Standalone IQR audit notebook; produces `data/clean/data_quality_report.csv`
  - Duplicate detection, missing value audit, worst-offender tables
- **`docs/LIMITATIONS.md`** — comprehensive data caveat disclosure (L1–L5)

### 🐛 Fixed (integrity)
- **`run_pipeline.py`**: Removed undisclosed parameter substitution that silently changed
  `min_support=0.005` → `min_support=0.0015` in basket analysis during every pipeline run.
  All notebook parameters now execute exactly as written.
- **`README.md`**: Fixed Beverages churn rate `31.4%` → `24.9%` (actual notebook output)
- **`README.md`**: Removed fabricated `"Zepto 6% median discount"` claim
- **`README.md`**: Corrected `"inactive 400+ days"` → `"avg 400 days since last order"`
- **`views/market_basket.py`**: Fixed KPI card support threshold `0.15%` → `0.5%`
- **`views/overview.py`**: Fixed `"400+ days ago"` → `"avg 400 days (proxy dataset)"`
- **`app.py`**: Removed fabricated `"Zepto Value Gap: -12.4%"` from global ticker bar
- **`utils/story_generator.py`**: Fixed At-Risk fallback `761` → `206` (notebook Cell 4)

### 📚 Improved
- **`views/market_basket.py`**: Added amber analyst note explaining why 1 rule is an honest finding
- **`views/business_simulator.py`**: Added assumptions expander with data-derived vs. assumed table
- **`utils/story_generator.py`**: Fixed docstring — now honestly documents that fallbacks exist
- **`requirements.txt`**: Added `scipy>=1.11.0` (IQR stats); added inline package descriptions
- **`README.md`**: Full rewrite — dataset transparency block, notebook citations for all numbers

---

## [v1.2.0] — May 2026 — Initial Release

### 🆕 Added
- 8-page Streamlit dark dashboard
- Platform price intelligence heatmap
- RFM segmentation (5 classes, quintile scoring)
- 24-month cohort retention matrix
- Customer journey Sankey diagram
- Business Decision Simulator (win-back ROI, price elasticity, retention LTV)
- Auto-intelligence story generator
- Modular views/utils architecture

---

*Maintained by Yashaswini V*
