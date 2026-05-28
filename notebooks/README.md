# 📚 QC Pulse India - Jupyter Notebooks Guide

This directory contains all data analysis notebooks used to generate the processed datasets for the Streamlit dashboard.

## 📖 Overview

The notebooks are numbered sequentially and should be run in order:

```
01_data_load.ipynb
    ↓ (loads raw data)
02_cleaning.ipynb
    ↓ (creates clean datasets)
03_price_intelligence.ipynb  → price_matrix.csv
04_basket_analysis.ipynb     → association_rules.csv
05_rfm_segmentation.ipynb    → rfm_segments.csv, rfm_summary.csv
06_cohort_retention.ipynb    → cohort_retention.csv
07_sankey.ipynb              → sankey_data.csv
    ↓ (all feeds into)
app.py (Streamlit Dashboard)
```

---

## 🔍 Detailed Notebook Descriptions

### **01_data_load.ipynb**
**Load raw CSV files and initial exploration**

**Questions Answered:**
- What raw data files do we have?
- How many rows and columns in each file?
- What are the data types?

**Data Sources:**
- `data/raw/BigBasket Products.csv`
- `data/raw/BlinkIT Grocery Data.csv`
- `data/raw/Groceries_dataset.csv`
- `data/raw/zepto_v1.csv`

**Outputs:**
- Data shape summaries
- Column names and types
- Initial data exploration (head, info, describe)
- Missing values analysis

**Key Learnings:**
- Understand structure of each platform's data
- Identify data quality issues early
- Note naming inconsistencies across sources

**Run Time:** ~1-2 minutes

---

### **02_cleaning.ipynb**
**Data preprocessing and validation**

**Questions Answered:**
- Which rows/columns have data quality issues?
- How do we standardize category names?
- What transformations are needed?

**Input Datasets:**
- Raw CSV files from `data/raw/`

**Output Datasets:**
- `blinkit_clean.csv`
- `zepto_clean.csv`
- `bigbasket_clean.csv`
- `groceries_clean.csv`

**Cleaning Steps:**
1. **Duplicate Removal** — Remove exact row duplicates
2. **Missing Value Handling** — Drop/fill nulls based on column importance
3. **Category Standardization** — Map vendor categories to 6 master categories
   - Dairy
   - Fresh Produce
   - Bakery & Grains
   - Beverages
   - Meat & Snacks
   - Other
4. **Price Validation** — Remove negative/zero prices
5. **Discount Calculation** — Calculate discount % from MRP and price
6. **Date Parsing** — Convert date columns to datetime
7. **Type Optimization** — Convert columns to appropriate dtypes

**Data Quality Rules Applied:**
- ✓ No negative prices
- ✓ Discount between 0-100%
- ✓ Valid date ranges (2014-2015 for transactions)
- ✓ Customer IDs not null
- ✓ Product names not empty

**Run Time:** ~3-5 minutes

---

### **03_price_intelligence.ipynb**
**Competitive pricing analysis**

**Questions Answered:**
- Which platform is cheapest by category?
- What are the average discounts?
- How do platforms position themselves price-wise?
- What is the price gap vs market average?

**Input Datasets:**
- `blinkit_clean.csv`
- `zepto_clean.csv`
- `bigbasket_clean.csv`

**Output Dataset:**
- `price_matrix.csv`

**Analysis Performed:**
1. **Category Grouping** — Group products into master categories
2. **Price Metrics** — Calculate median prices, discounts by platform
3. **Market Average** — Compute average price per category across platforms
4. **Gap Analysis** — Calculate price gap %:
   ```
   Gap% = ((Platform_Median - Market_Average) / Market_Average) * 100
   ```
5. **Competitive Positioning** — Identify cheapest/most expensive platforms

**Key Insights Generated:**
- Zepto: Most aggressive discounting (high gap %)
- BigBasket: Stable mid-range pricing
- Blinkit: Premium positioning in select categories

**Run Time:** ~2-3 minutes

---

### **04_basket_analysis.ipynb**
**Market basket and association rules analysis**

**Questions Answered:**
- Which products are frequently bought together?
- What are the association rules (if X bought, likely to buy Y)?
- Which product combinations have high confidence?

**Input Dataset:**
- `groceries_clean.csv` (transaction data)

**Output Dataset:**
- `association_rules.csv`

**Methodology:**
1. **Transaction Grouping** — Group items by order
2. **Frequent Itemsets** — Use Apriori algorithm to find itemsets
3. **Association Rules** — Generate rules with metrics:
   - **Support**: Probability of itemset occurring
   - **Confidence**: P(B | A) — If A bought, probability of B
   - **Lift**: How much more likely B given A (vs random)
4. **Rule Filtering** — Keep rules with confidence > 0.3, lift > 1.2

**Example Rules:**
```
If: Dairy bought → Then: Fresh Produce (confidence: 45%, lift: 1.8)
If: Beverages → Snacks (confidence: 52%, lift: 2.1)
```

**Business Applications:**
- Product recommendations
- Cross-sell strategies
- Bundle pricing
- Store layout optimization

**Run Time:** ~5-10 minutes (Apriori can be slow for large datasets)

---

### **05_rfm_segmentation.ipynb**
**RFM (Recency-Frequency-Monetary) customer segmentation**

**Questions Answered:**
- Who are our best customers (Champions)?
- Who are at-risk of churning?
- What is the value of each customer segment?
- How do we segment based on behavior?

**Input Dataset:**
- `groceries_clean.csv`

**Output Datasets:**
- `rfm_segments.csv` (customer-level scores and segments)
- `rfm_summary.csv` (aggregate segment statistics)

**RFM Metrics Calculated:**
1. **Recency (R)** — Days since last purchase
   - Score 5: ≤30 days
   - Score 1: >400 days
2. **Frequency (F)** — Number of orders
   - Score 5: ≥10 orders
   - Score 1: 1-2 orders
3. **Monetary (M)** — Total customer spending
   - Score 5: Top 20% spenders
   - Score 1: Bottom 20% spenders

**Segmentation Logic:**
```
RFM_Score = R_Score + F_Score + M_Score (0-15 scale)

13-15 → Champion (Best customers, retain at all costs)
10-12 → Loyal (Good customers, nurture relationship)
7-9   → Potential (Can be converted to Champions)
4-6   → At-Risk (Declining engagement, win-back campaigns)
3     → Churned (Inactive, last order 400+ days ago)
```

**Segment Characteristics:**
| Segment | Count | Pct | Recency | Frequency | Monetary | Action |
|---------|-------|-----|---------|-----------|----------|--------|
| Champion | 809 | 20.8% | 58 days | 6.3 orders | High | Loyalty programs |
| Loyal | 615 | 15.8% | 121 days | 4.8 orders | Medium | Upsell |
| Potential | 814 | 20.9% | 245 days | 2.1 orders | Low-Med | Engagement |
| At-Risk | 761 | 19.5% | 341 days | 1.5 orders | Low | Win-back |
| Churned | 899 | 22.8% | 400+ days | 1.0 order | Very Low | Re-activation |

**Run Time:** ~3-5 minutes

---

### **06_cohort_retention.ipynb**
**Cohort analysis and customer retention tracking**

**Questions Answered:**
- How many customers return after their first purchase?
- Which acquisition cohorts are most valuable?
- What is the retention curve over time?
- How does retention vary by month?

**Input Dataset:**
- `groceries_clean.csv`

**Output Dataset:**
- `cohort_retention.csv` (24 cohorts × 13 months matrix)

**Cohort Approach:**
1. **Cohort Definition** — Group customers by their first purchase month
2. **Cohort Size** — Count new customers per month
3. **Month-by-Month Tracking** — For each cohort, track:
   - Month 0: 100% (all new customers)
   - Month 1: % who returned
   - Month 2: % still active
   - Month 12: % still active after 1 year

**Key Metrics:**
```
Month-1 Retention = Customers_Returning / Initial_Cohort_Size

Example:
Jun-2015 cohort: 100 new customers
Month 1: 26 returned = 26% retention (excellent!)
Month 3: 14 active = 14% retention
Month 12: 4 active = 4% retention
```

**Findings:**
- Average Month-1 retention: 14.3% (challenging!)
- Best cohort: Jun 2015 with 26.3% Month-1
- Steep decline Month 1→Month 3
- **Implication:** Focus on Month 1 retention critical for LTV

**Business Insights:**
- High customer acquisition cost given low retention
- Need to improve onboarding experience
- Target improvements in Month 0-1 period

**Run Time:** ~5-8 minutes

---

### **07_sankey.ipynb**
**Customer journey flow analysis**

**Questions Answered:**
- What is the typical customer journey?
- Do customers in certain categories churn more?
- Which RFM segments have best outcomes?
- How do first category purchases relate to retention?

**Input Datasets:**
- `groceries_clean.csv`
- `rfm_segments.csv`

**Output Dataset:**
- `sankey_data.csv` (customer journey with first category → segment → outcome)

**Sankey Diagram Elements:**
1. **First Category** (Left) — Customer's first product category
   - Dairy, Fresh Produce, Beverages, etc.
2. **RFM Segment** (Middle) — Where customer ended up
   - Champion, Loyal, Potential, At-Risk, Churned
3. **Outcome** (Right) — Final customer state
   - Retained High-Value (high spenders, active)
   - Retained (active, lower spend)
   - Churned (inactive)

**Flow Width Represents** — Number of customers

**Example Flows:**
```
Dairy → Champion → Retained High-Value (500 customers)
        ↓
     Loyal → Retained (350 customers)
        ↓
     At-Risk → Churned (200 customers)

Beverages → Champion (20 customers)
         → Churned (400 customers) ← PROBLEM! High churn
```

**Key Insights:**
- Beverages category has highest churn rate
- Dairy category produces most Champions
- Path dependency: first category affects long-term outcome
- Need targeted interventions by category

**Run Time:** ~3-4 minutes

---

## 🚀 Running All Notebooks

### Option 1: Command Line (Using nbconvert)
```bash
cd notebooks/

# Run all notebooks in sequence
for i in {01..07}; do
    jupyter nbconvert --to notebook --execute --inplace ${i}_*.ipynb
done
```

### Option 2: Jupyter UI
```bash
jupyter notebook
# Open each notebook in order and click "Run All Cells"
```

### Option 3: Python Script
```python
import subprocess
import sys

notebooks = [
    '01_data_load.ipynb',
    '02_cleaning.ipynb',
    '03_price_intelligence.ipynb',
    '04_basket_analysis.ipynb',
    '05_rfm_segmentation.ipynb',
    '06_cohort_retention.ipynb',
    '07_sankey.ipynb'
]

for nb in notebooks:
    print(f"\n▶️  Running {nb}...")
    subprocess.run([
        sys.executable, '-m', 'jupyter', 'nbconvert',
        '--to', 'notebook', '--execute', '--inplace', nb
    ], check=True)
    print(f"✓ {nb} completed")
```

---

## 📊 Dependencies in Notebooks

**Data Manipulation:**
- `pandas` — DataFrames and data wrangling
- `numpy` — Numerical operations

**Analysis:**
- `scikit-learn` — For Apriori algorithm (basket analysis)
- `mlxtend` — Market basket analysis utilities

**Visualization:**
- `plotly` — Interactive charts
- `matplotlib`/`seaborn` — Static plots (if used)

**Other:**
- `datetime` — Date/time operations

---

## 🔧 Customization & Modification

### To Add New Analysis:
1. Create new notebook `08_custom_analysis.ipynb`
2. Load cleaned data from `data/clean/`
3. Add your analysis
4. Save outputs to `data/clean/` or `outputs/`
5. If creating new dashboard page, add render function to `pages/`

### To Change Parameters:
- **RFM Thresholds:** Edit scoring ranges in `05_rfm_segmentation.ipynb`
- **Retention Cohort Length:** Edit month range in `06_cohort_retention.ipynb`
- **Category Mappings:** Edit category standardization in `02_cleaning.ipynb`

### To Update Data:
1. Replace raw files in `data/raw/`
2. Run all notebooks in sequence
3. Restart Streamlit app

---

## ⚠️ Common Issues & Solutions

### "FileNotFoundError: No such file or directory"
- **Cause:** Working directory is not `notebooks/`
- **Fix:** Run `%cd notebooks` or start from project root

### "ModuleNotFoundError: No module named 'mlxtend'"
- **Cause:** Apriori library not installed
- **Fix:** `pip install mlxtend`

### "MemoryError" (in basket analysis)
- **Cause:** Dataset too large for Apriori
- **Fix:** Reduce min_support parameter or filter transactions

### "No such column 'category'"
- **Cause:** Column name differs in raw data
- **Fix:** Check raw file headers and update notebook accordingly

---

## 📈 Expected Outputs

After running all notebooks, you should have:

```
data/clean/
├── blinkit_clean.csv           (~15K rows, 10 cols)
├── zepto_clean.csv             (~8K rows, 10 cols)
├── bigbasket_clean.csv         (~12K rows, 10 cols)
├── groceries_clean.csv         (~5K rows, 10 cols)
├── rfm_segments.csv            (3,898 rows, 8 cols)
├── rfm_summary.csv             (5 rows, 8 cols)
├── price_matrix.csv            (15 rows, 11 cols)
├── cohort_retention.csv        (24 rows, 13 cols)
└── sankey_data.csv             (3,898 rows, 7 cols)
```

---

## 📝 Best Practices

1. **Always run notebooks in order** — Later notebooks depend on earlier outputs
2. **Don't edit cleaned data manually** — Modify source notebooks instead
3. **Keep raw data unchanged** — Never modify `data/raw/`
4. **Document your changes** — Add markdown cells explaining modifications
5. **Test on small samples first** — Use `.head(100)` before full processing
6. **Save intermediate results** — Saves time if re-running specific analyses

---

## 🔗 Related Files

- [README.md](../README.md) — Project overview
- [docs/data_schema.md](../docs/data_schema.md) — Column definitions
- [config.py](../config.py) — Dashboard configuration
- [app.py](../app.py) — Main Streamlit application

---

**Last Updated:** May 2026  
**Python Version:** 3.8+  
**Status:** Production Ready
