# 🛒 QC Pulse India — Quick Commerce Analytics Platform

A comprehensive data analytics dashboard analyzing pricing strategies, customer behavior, and retention patterns across India's top quick commerce platforms: **Blinkit**, **Zepto**, and **BigBasket**.

---

## 📋 Project Overview

**QC Pulse India** provides competitive intelligence and customer insights for the fast-growing quick commerce (10-minute delivery) market in India. The project combines price intelligence, RFM customer segmentation, basket analysis, and cohort retention analysis to answer critical business questions:

- **Which platform wins the price war by category?**
- **How valuable are our customer segments?**
- **What drives customer churn and retention?**
- **What is the typical customer journey?**

### Key Metrics
- **3 Platforms** analyzed: Blinkit, Zepto, BigBasket
- **3,898 Customers** segmented via RFM analysis
- **24 Cohorts** tracked across 2 years (2014-2015)
- **9 Datasets** processed through data pipeline
- **5 Interactive Pages** in Streamlit dashboard

---

## 🎯 Features

### 📊 Dashboard Pages

1. **Overview** — Platform comparison, category breakdown, key findings
2. **⚔️ Price Intelligence** — Price gap matrix, discount analysis by platform
3. **👥 Customer Segments** — RFM segmentation treemap, recency vs frequency scatter
4. **📈 Cohort Retention** — Month-by-month retention heatmap across 24 cohorts
5. **🌊 Customer Journey** — Sankey diagram showing first category → segment → outcome flow

### 📈 Analytics Included

- **Price Competitive Analysis** — Market positioning across 15+ product categories
- **RFM Segmentation** — 5 segments: Champion, Loyal, Potential, At-Risk, Churned
- **Market Basket Analysis** — Association rules and product affinity patterns
- **Cohort Retention Analysis** — Customer lifecycle tracking
- **Customer Journey Mapping** — Flow analysis from acquisition to outcome

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ (Recommended: 3.9 or 3.10)
- pip or conda for package management
- ~500MB disk space for data files

### Installation

1. **Clone or download the project:**
   ```bash
   cd QC_Pulse_India
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   # Using venv
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   **Required packages:**
   - `streamlit==1.28.1` — Dashboard framework
   - `pandas==2.1.3` — Data manipulation
   - `numpy==1.24.3` — Numerical computing
   - `plotly==5.17.0` — Interactive visualizations
   - `python-dateutil==2.8.2` — Date utilities
   - `pytz==2023.3` — Timezone handling

4. **Verify data files are present:**
   ```
   data/clean/
   ├── blinkit_clean.csv
   ├── zepto_clean.csv
   ├── bigbasket_clean.csv
   ├── groceries_clean.csv
   ├── rfm_segments.csv
   ├── rfm_summary.csv
   ├── price_matrix.csv
   ├── cohort_retention.csv
   └── sankey_data.csv
   ```

### Running the Dashboard

```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

---

## 📁 Project Structure

```
QC_Pulse_India/
├── app.py                           # Main Streamlit application
├── config.py                        # Configuration (colors, layouts, data paths)
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
│
├── notebooks/                       # Jupyter notebooks for analysis
│   ├── 01_data_load.ipynb          # Load raw CSV files
│   ├── 02_cleaning.ipynb           # Data cleaning & preprocessing
│   ├── 03_price_intelligence.ipynb # Competitive pricing analysis
│   ├── 04_basket_analysis.ipynb    # Market basket & association rules
│   ├── 05_rfm_segmentation.ipynb   # RFM customer clustering
│   ├── 06_cohort_retention.ipynb   # Cohort analysis & retention curves
│   └── 07_sankey.ipynb             # Customer journey flows
│
├── data/
│   ├── raw/                         # Original unprocessed data
│   │   ├── BigBasket Products.csv
│   │   ├── BlinkIT Grocery Data.csv
│   │   ├── Groceries_dataset.csv
│   │   └── zepto_v1.csv
│   │
│   └── clean/                       # Processed & analyzed data
│       ├── blinkit_clean.csv
│       ├── zepto_clean.csv
│       ├── bigbasket_clean.csv
│       ├── groceries_clean.csv
│       ├── rfm_segments.csv
│       ├── rfm_summary.csv
│       ├── price_matrix.csv
│       ├── cohort_retention.csv
│       └── sankey_data.csv
│
├── outputs/                         # Generated visualizations (HTML)
│   ├── basket_rules_bar.html
│   ├── price_intelligence_heatmap.html
│   ├── rfm_scatter.html
│   ├── cohort_retention_heatmap.html
│   └── sankey_customer_journey.html
│
├── utils/                           # Utility modules
│   ├── __init__.py
│   ├── data_loader.py              # CSV loading & caching with error handling
│   └── charts.py                   # Plotly chart styling & utilities
│
└── pages/                           # Streamlit page modules (modular dashboard)
    ├── __init__.py
    ├── 00_overview.py              # Overview & key metrics
    ├── 01_price_intelligence.py    # Competitive pricing
    ├── 02_customer_segments.py     # RFM segmentation
    ├── 03_cohort_retention.py      # Retention analysis
    └── 04_customer_journey.py      # Sankey flow diagram
```

---

## 📊 Data Dictionary

See [data/data_schema.md](data/data_schema.md) for detailed column definitions and data sources.

### Core Datasets

| Dataset | Records | Purpose |
|---------|---------|---------|
| **blinkit_clean.csv** | 15K+ products | Blinkit platform inventory |
| **zepto_clean.csv** | 8K+ products | Zepto platform inventory |
| **bigbasket_clean.csv** | 12K+ products | BigBasket platform inventory |
| **groceries_clean.csv** | 5K transactions | Customer purchase history |
| **rfm_segments.csv** | 3,898 rows | RFM scores & segments per customer |
| **rfm_summary.csv** | 5 rows | Aggregate segment statistics |
| **price_matrix.csv** | 20 rows | Price comparison by category |
| **cohort_retention.csv** | 24 rows × 13 cols | Month-by-month retention % |
| **sankey_data.csv** | 3,898 rows | Customer journey with outcomes |

---

## 🔍 How to Use

### Dashboard Navigation

1. **Overview Page** — Start here for high-level metrics and key findings
2. **Price Intelligence** — Identify pricing gaps by category
3. **Customer Segments** — Understand who your customers are (Champions vs Churned)
4. **Cohort Retention** — See which customer cohorts have best lifetime value
5. **Customer Journey** — Visualize the flow from first purchase to outcome

### Analysis Notebooks

Run notebooks sequentially to regenerate analysis:

```bash
jupyter notebook notebooks/
```

**Notebook order matters:**
1. `01_data_load.ipynb` — Loads raw CSVs
2. `02_cleaning.ipynb` — Data preprocessing & validation
3. `03_price_intelligence.ipynb` → `price_matrix.csv`
4. `04_basket_analysis.ipynb` → `association_rules.csv`
5. `05_rfm_segmentation.ipynb` → `rfm_segments.csv`, `rfm_summary.csv`
6. `06_cohort_retention.ipynb` → `cohort_retention.csv`
7. `07_sankey.ipynb` → `sankey_data.csv`

---

## 🎨 Design & Styling

- **Dark Theme** — Professional slate/blue color scheme optimized for long viewing
- **Responsive Layout** — Adapts to desktop/tablet/mobile screens
- **Consistent Branding** — Custom CSS + Plotly theming across all charts
- **Color System**:
  - Platforms: Purple (BigBasket), Red (Blinkit), Green (Zepto)
  - Segments: Red (Champion), Orange (Loyal), Purple (Potential), Amber (At-Risk), Gray (Churned)

---

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Colors
COLORS = { ... }
PLATFORM_COLORS = { 'BigBasket': '#6C63DB', ... }
SEGMENT_COLORS = { 'Champion': '#DC2626', ... }

# Chart dimensions
CHART_HEIGHT = 380
HEATMAP_HEIGHT = 450
SANKEY_HEIGHT = 600

# Data file paths
DATA_FILES = {
    'blinkit': 'data/clean/blinkit_clean.csv',
    ...
}
```

---

## 🐛 Troubleshooting

### Issue: "Data file not found"
- **Cause:** CSV files missing from `data/clean/`
- **Fix:** Run notebooks in order to regenerate processed data

### Issue: "Column 'X' not found"
- **Cause:** Data schema mismatch between notebooks and app
- **Fix:** Ensure all notebooks have been run recently

### Issue: Streamlit page won't load
- **Cause:** Memory issue with large datasets
- **Fix:** Streamlit uses `@st.cache_data` to optimize. Try: `streamlit run app.py --logger.level=debug`

### Issue: Charts not rendering
- **Cause:** Missing Plotly dependency
- **Fix:** Run `pip install plotly==5.17.0`

---

## 📈 Key Findings

### RFM Segmentation
- **Champions** (809 customers, 20.8%): Order every 58 days, avg 6.3 orders, high LTV
- **Loyal** (615 customers, 15.8%): Regular customers with decent frequency
- **Potential** (814 customers, 20.9%): Could be converted to Champions
- **At-Risk** (761 customers, 19.5%): Declining engagement, need interventions
- **Churned** (899 customers, 22.8%): Last order 400+ days ago

### Price Positioning
- **Zepto** leads with aggressive discounting (median discount varies by category)
- **BigBasket** maintains competitive positioning across categories
- **Blinkit** premium positioning with selective discounts

### Retention Trends
- Average Month-1 retention: 14.3%
- Best performing cohort (Jun 2015): 26.3% (84% above average)
- Month-3 retention significantly drops → customer acquisition vs retention challenge

---

## 🔐 Data Privacy & Disclaimer

- All customer data is anonymized with customer_id identifiers
- This is for demonstration/educational purposes
- Actual implementation should follow GDPR/local data protection regulations

---

## 📝 Notebooks Documentation

Each notebook includes:
- **Overview**: What question it answers
- **Data Source**: Which raw files are used
- **Methodology**: Statistical/analytical approach
- **Outputs**: Which cleaned datasets are created
- **Key Insights**: Main findings from the analysis

See individual notebooks for detailed explanations.

---

## 🤝 Contributing

To improve this project:

1. Add new analysis notebooks in `notebooks/`
2. Update data files in `data/clean/`
3. Add new dashboard pages in `pages/` (following existing structure)
4. Update this README with new features
5. Run all notebooks end-to-end to verify reproducibility

---

## 📞 Support

For issues or questions:
1. Check [Troubleshooting](#-troubleshooting) section
2. Review relevant notebook for data validation
3. Check `config.py` for data paths
4. Enable debug logging: `streamlit run app.py --logger.level=debug`

---

## 📄 License

This project is provided as-is for educational and analytical purposes.

---

## 🎓 Learning Outcomes

By studying this project, you'll learn:
- ✅ Building data pipelines with Pandas
- ✅ RFM (Recency-Frequency-Monetary) customer segmentation
- ✅ Cohort analysis and retention modeling
- ✅ Interactive dashboards with Streamlit + Plotly
- ✅ Data-driven business insights
- ✅ Project organization best practices
- ✅ Dark theme UI/UX design

---

**Last Updated:** May 2026  
**Status:** ✅ Production Ready with Documentation
