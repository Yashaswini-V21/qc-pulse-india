# Known Limitations & Data Caveats

> **For interviewers and reviewers:** This document exists because honest data work requires
> disclosing what the data cannot tell you. Every limitation here was discovered during analysis
> and is documented here rather than hidden.

---

## L1 — Customer Behaviour Dataset is not Blinkit/Zepto Data

**Affected pages:** Market Basket, Customer Segments (RFM), Cohort Retention, Customer Journey

The grocery transactions dataset (`groceries_clean.csv`) is a public benchmark dataset of
Western grocery store transactions from **2014–2015**. Zepto was founded in 2021.

**Impact:**
- RFM segments, cohort retention rates, and basket rules describe a generic grocery
  store customer base, not Indian quick-commerce users
- Customer counts (3,898), transaction counts (38,765), and retention rates (14.3% avg M1)
  apply to this proxy dataset, not any real platform

**Why it's still valid:**
- All methodology (quintile scoring, cohort period arithmetic, Apriori pipeline) is
  textbook-correct and transferable to any transactional dataset
- The technical implementation is what the project demonstrates — not real business intelligence about Zepto

---

## L2 — Market Basket Analysis Produced 1 Rule

**Affected page:** Market Basket

At `min_support=0.005` (0.5%), the Apriori algorithm on this dataset found:
- **1 statistically significant rule**: `frankfurter → vegetables`, lift=1.12x, confidence=13.6%

**Root cause:**
The dataset is in single-item-per-row format with ~2.6 average items per shopping trip.
This is a data density limitation — not a pipeline error. Association rules require dense
co-occurrence patterns that this dataset structure does not support at standard thresholds.

**What was NOT done (integrity note):**
The `run_pipeline.py` originally silently lowered `min_support` from 0.005 to 0.0015 during
execution to produce "more rules." This undisclosed parameter change has been removed.
The pipeline now uses the threshold as written in the notebook.

---

## L3 — Zepto Price Data Has Corrupted Categories

**Affected page:** Price Intelligence

Notebook 03 revealed:
- **Zepto Beverages median price: ₹9,500** (real Zepto Beverages = ₹50–500 range)
- **Zepto Personal Care median price: ₹16,200** (implausible for a grocery platform)

These appear to be data entry errors or currency mismatches in the source Kaggle CSV.

**Impact:**
- The "6% Zepto median discount" claim that previously appeared in the README was
  removed because it cannot be verified from this corrupted data
- The Data Quality dashboard page (Page 9) flags these categories automatically using IQR detection

---

## L4 — Business Simulator Uses Assumed Parameters

**Affected page:** Business Simulator

All financial projections (ROI, LTV, payback period) are based on:

| Parameter | Value | Type |
|---|---|---|
| Avg order value | ₹350 | Industry estimate (not from this dataset) |
| Orders/month per recovered customer | 2 | Conservative assumption |
| Price elasticity | -2.0 | Standard retail textbook value |
| Discount-to-retention boost | +0.3pp per 1% discount | Heuristic |
| Recovered LTV fraction | 30% of Champion LTV | Conservative heuristic |

The Simulator is a **modelling framework demonstrating how to structure these calculations** —
not a forecast derived from the datasets in this project.

---

## L5 — Blinkit Discount Percentages Are Imputed

**Affected pages:** Overview, Price Intelligence (radar chart)

The Blinkit raw CSV does not contain a `discount_pct` column. `data_loader.py`
generates synthetic discount percentages using a Beta distribution:

```python
blinkit['discount_pct'] = np.random.beta(a=2.5, b=12.0, size=len(blinkit)) * 100
```

This produces a center-weighted distribution around ~14.5% to prevent a flat radar chart.
The values are **not from real Blinkit discount data**. `np.random.seed(42)` is used for
reproducibility, so the same values are generated every run.

---

## Summary Table

| ID | Limitation | Severity | Mitigated? |
|---|---|---|---|
| L1 | Proxy grocery dataset, not real QC data | 🔴 High | ✅ Disclosed in README, dashboard, notebook headers |
| L2 | Basket analysis: 1 rule at standard threshold | 🟡 Medium | ✅ Honest analyst note on dashboard page |
| L3 | Zepto price data corrupted in 2+ categories | 🟡 Medium | ✅ IQR detection flags these automatically |
| L4 | Simulator uses assumed ₹ parameters | 🟡 Medium | ✅ Assumptions expander in dashboard |
| L5 | Blinkit discount_pct is imputed, not real | 🟡 Medium | ✅ Documented in data_loader.py comments |

---

*Last updated: June 2026*
