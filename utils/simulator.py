"""
utils/simulator.py
──────────────────
Business Decision Simulator for QC Pulse India.
Contains 4 simulation functions that power the Business Simulator dashboard page
and the Competitive Intelligence Scorecard.

All monetary projections use avg_order_value = ₹350 (standard Indian QC basket).
"""

import pandas as pd
import numpy as np
from utils.config import (
    AVG_ORDER_VALUE,
    ORDERS_PER_MONTH_WINBACK as ORDERS_PER_MONTH,
    CHAMPION_LTV_ITEMS,
    PRICE_ELASTICITY,
    MAX_EXPECTED_DISCOUNT,
    BLINKIT_CAT_MAP,
    ZEPTO_CAT_MAP,
    BIGBASKET_CAT_MAP
)



# ════════════════════════════════════════════════════════════════════════════
# FUNCTION 1 — Win-Back Campaign Simulator
# ════════════════════════════════════════════════════════════════════════════

def simulate_winback_campaign(
    rfm_df: pd.DataFrame,
    cohort_df: pd.DataFrame,
    segment_targeted: str,
    customers_targeted: int,
    campaign_budget_inr: float,
    discount_offered_pct: float
) -> dict:
    """
    Simulate an email/SMS win-back campaign targeting At-Risk or Churned customers.

    Parameters
    ----------
    rfm_df : RFM segmentation dataframe (rfm_segments.csv)
    cohort_df : Cohort retention dataframe (cohort_retention.csv)
    segment_targeted : "At-Risk" or "Churned"
    customers_targeted : how many customers to contact
    campaign_budget_inr : total campaign spend in ₹
    discount_offered_pct : 0–100 — discount coupon included in campaign

    Returns
    -------
    dict with keys:
        customers_recovered, revenue_gained, roi_pct, payback_months,
        recovery_rate_pct, recommended_cohort, cost_per_recovered,
        segment_size, base_retention_rate, adjusted_retention_rate
    """
    # --- Derive base month-1 retention from cohort data ---
    cohort_num = cohort_df.copy()
    try:
        cohort_num.columns = cohort_num.columns.astype(int)
        base_m1_retention = float(cohort_num[1].mean()) / 100.0   # convert % to ratio
    except Exception:
        base_m1_retention = 0.143  # fallback: dataset average 14.3%

    # --- Adjust retention rate based on discount incentive ---
    # Each % of discount adds 0.3% to recovery probability (diminishing return baked in cap)
    discount_boost = min(discount_offered_pct / 100.0 * 0.3, 0.25)
    adjusted_retention = min(base_m1_retention + discount_boost, 0.60)

    # --- Segment size cap ---
    segment_df = rfm_df[rfm_df['segment'] == segment_targeted]
    segment_size = len(segment_df)
    customers_targeted = min(customers_targeted, segment_size)

    # --- Core calculations ---
    customers_recovered = int(round(customers_targeted * adjusted_retention))
    revenue_gained = customers_recovered * AVG_ORDER_VALUE * ORDERS_PER_MONTH
    roi_pct = ((revenue_gained - campaign_budget_inr) / campaign_budget_inr * 100
               if campaign_budget_inr > 0 else 0.0)
    monthly_revenue = revenue_gained / 3.0   # spread over 3 months
    payback_months = (campaign_budget_inr / monthly_revenue
                      if monthly_revenue > 0 else float('inf'))
    cost_per_recovered = (campaign_budget_inr / customers_recovered
                          if customers_recovered > 0 else float('inf'))

    # --- Best cohort recommendation ---
    try:
        best_cohort_idx = cohort_num[1].idxmax()
        recommended_cohort = str(best_cohort_idx)
    except Exception:
        recommended_cohort = "Jun-2015"

    return {
        "customers_recovered": customers_recovered,
        "revenue_gained": revenue_gained,
        "roi_pct": round(roi_pct, 1),
        "payback_months": round(payback_months, 1) if payback_months != float('inf') else 99.9,
        "recovery_rate_pct": round(adjusted_retention * 100, 1),
        "base_retention_rate": round(base_m1_retention * 100, 1),
        "recommended_cohort": recommended_cohort,
        "cost_per_recovered": round(cost_per_recovered, 0) if cost_per_recovered != float('inf') else 0,
        "segment_size": segment_size,
        "discount_boost_pp": round(discount_boost * 100, 1),
    }


# ════════════════════════════════════════════════════════════════════════════
# FUNCTION 2 — Price Change Simulator
# ════════════════════════════════════════════════════════════════════════════

def simulate_price_change(
    price_matrix_df: pd.DataFrame,
    platform: str,
    category: str,
    discount_change_pct: float,
    estimated_customers: int
) -> dict:
    """
    Simulate the revenue and competitive impact of a price change on a platform.

    Parameters
    ----------
    price_matrix_df : price_matrix.csv dataframe
    platform : "Blinkit", "Zepto", or "BigBasket"
    category : one of the master category names in price_matrix
    discount_change_pct : -30 to +30 (negative = price increase, positive = discount)
    estimated_customers : customers affected by the change

    Returns
    -------
    dict with keys:
        current_price, new_price, market_avg, gap_before, gap_after,
        position_before, position_after, volume_change_pct,
        revenue_impact, position_arrow
    """
    row = price_matrix_df[price_matrix_df['category'] == category]
    if row.empty or platform not in price_matrix_df.columns:
        return {
            "error": f"No data for {platform} / {category}",
            "current_price": 0, "new_price": 0, "market_avg": 0,
            "gap_before": 0, "gap_after": 0,
            "position_before": "Unknown", "position_after": "Unknown",
            "volume_change_pct": 0, "revenue_impact": 0, "position_arrow": "→"
        }

    current_price = float(row[platform].values[0])
    market_avg = float(row['market_avg'].values[0])

    if pd.isna(current_price) or pd.isna(market_avg) or market_avg == 0:
        return {
            "error": f"Insufficient price data for {platform} / {category}",
            "current_price": 0, "new_price": 0, "market_avg": 0,
            "gap_before": 0, "gap_after": 0,
            "position_before": "N/A", "position_after": "N/A",
            "volume_change_pct": 0, "revenue_impact": 0, "position_arrow": "→"
        }

    # Positive discount_change_pct means price drops (discount increases)
    new_price = current_price * (1 - discount_change_pct / 100.0)
    new_price = max(new_price, 0.01)

    gap_before = (current_price - market_avg) / market_avg * 100
    gap_after = (new_price - market_avg) / market_avg * 100

    def classify_position(gap_pct):
        if gap_pct > 5:
            return "Premium"
        elif gap_pct > -5:
            return "Mid-Market"
        else:
            return "Value"

    position_before = classify_position(gap_before)
    position_after = classify_position(gap_after)

    # Volume change from price elasticity (positive discount → more volume)
    volume_change_pct = PRICE_ELASTICITY * (-discount_change_pct)  # elasticity works on price change

    # Revenue impact: positive discount reduces price but increases volume
    baseline_revenue = estimated_customers * AVG_ORDER_VALUE
    volume_adjustment = 1 + volume_change_pct / 100.0
    price_adjustment = 1 - discount_change_pct / 100.0
    revenue_impact = baseline_revenue * (volume_adjustment * price_adjustment - 1)

    POSITION_ICONS = {
        ("Premium", "Mid-Market"): "↓", ("Premium", "Value"): "↓↓",
        ("Mid-Market", "Value"): "↓", ("Mid-Market", "Premium"): "↑",
        ("Value", "Mid-Market"): "↑", ("Value", "Premium"): "↑↑",
    }
    position_arrow = POSITION_ICONS.get((position_before, position_after), "→")

    return {
        "current_price": round(current_price, 2),
        "new_price": round(new_price, 2),
        "market_avg": round(market_avg, 2),
        "gap_before": round(gap_before, 1),
        "gap_after": round(gap_after, 1),
        "position_before": position_before,
        "position_after": position_after,
        "volume_change_pct": round(volume_change_pct, 1),
        "revenue_impact": round(revenue_impact, 0),
        "position_arrow": position_arrow,
        "error": None,
    }


# ════════════════════════════════════════════════════════════════════════════
# FUNCTION 3 — Retention Improvement Simulator
# ════════════════════════════════════════════════════════════════════════════

def simulate_retention_improvement(
    cohort_df: pd.DataFrame,
    rfm_df: pd.DataFrame,
    target_month: int,
    improvement_pct: float,
    intervention_cost_inr: float
) -> dict:
    """
    Simulate the LTV and ROI impact of improving cohort retention at a target month.

    Parameters
    ----------
    cohort_df : cohort_retention.csv dataframe
    rfm_df : rfm_segments.csv dataframe
    target_month : 1, 3, or 6 (month number to target)
    improvement_pct : percentage point improvement (1–10)
    intervention_cost_inr : total cost of intervention in ₹

    Returns
    -------
    dict with keys:
        current_rate, new_rate, additional_retained, ltv_gained,
        roi_pct, best_cohort, total_customers
    """
    cohort_num = cohort_df.copy()
    try:
        cohort_num.columns = cohort_num.columns.astype(int)
    except Exception:
        pass

    # Get current retention rate for target month
    if target_month in cohort_num.columns:
        current_rate = float(cohort_num[target_month].mean())
    else:
        current_rate = 14.3  # fallback

    new_rate = current_rate + improvement_pct
    total_customers = len(rfm_df)

    additional_retained = int(round(total_customers * (improvement_pct / 100.0)))

    # Champion LTV: avg_monetary × avg_order_value × 12 months
    # avg_monetary from rfm_summary = 16.9 items → 16.9 × ₹350 × 12
    champion_ltv = CHAMPION_LTV_ITEMS * AVG_ORDER_VALUE * 12

    # Assume recovered customers achieve 30% of champion LTV
    ltv_gained = additional_retained * champion_ltv * 0.30

    roi_pct = ((ltv_gained - intervention_cost_inr) / intervention_cost_inr * 100
               if intervention_cost_inr > 0 else 0.0)

    # Best cohort at target month
    try:
        best_cohort_col = cohort_num[target_month].dropna()
        best_cohort = str(best_cohort_col.idxmax()) if not best_cohort_col.empty else "Jun-2015"
        best_cohort_rate = float(best_cohort_col.max()) if not best_cohort_col.empty else current_rate
    except Exception:
        best_cohort = "Jun-2015"
        best_cohort_rate = current_rate

    return {
        "current_rate": round(current_rate, 1),
        "new_rate": round(new_rate, 1),
        "additional_retained": additional_retained,
        "ltv_gained": round(ltv_gained, 0),
        "roi_pct": round(roi_pct, 1),
        "best_cohort": best_cohort,
        "best_cohort_rate": round(best_cohort_rate, 1),
        "total_customers": total_customers,
        "champion_ltv": round(champion_ltv, 0),
    }


# ════════════════════════════════════════════════════════════════════════════
# SHARED COMPETITIVE UTILITY
# ════════════════════════════════════════════════════════════════════════════

def calculate_platform_price_wins(price_mat_df: pd.DataFrame) -> dict:
    """
    Computes price wins per platform and tracks cheapest categories and gaps.
    Centralized helper function to eliminate code duplication across simulator and story generator.
    """
    gap_cols = {
        'Blinkit': 'Blinkit_gap%',
        'Zepto': 'Zepto_gap%',
        'BigBasket': 'BigBasket_gap%',
    }
    price_wins = {'Blinkit': 0, 'Zepto': 0, 'BigBasket': 0}
    cheapest_platform_by_cat = {}
    zepto_cheapest_cat = None
    zepto_cheapest_gap = float('inf')
    total_cats_compared = 0

    for _, row in price_mat_df.iterrows():
        gaps = {}
        for p, col in gap_cols.items():
            if col in price_mat_df.columns and not pd.isna(row.get(col)):
                gaps[p] = float(row[col])
        if len(gaps) >= 2:
            winner = min(gaps, key=gaps.get)
            price_wins[winner] += 1
            total_cats_compared += 1
            cheapest_platform_by_cat[str(row['category'])] = winner
            if 'Zepto' in gaps and gaps['Zepto'] < zepto_cheapest_gap:
                zepto_cheapest_gap = gaps['Zepto']
                zepto_cheapest_cat = str(row['category'])

    return {
        "price_wins": price_wins,
        "cheapest_platform_by_cat": cheapest_platform_by_cat,
        "zepto_cheapest_cat": zepto_cheapest_cat,
        "zepto_cheapest_gap": zepto_cheapest_gap,
        "total_cats_compared": total_cats_compared
    }


# ════════════════════════════════════════════════════════════════════════════
# FUNCTION 4 — Platform Competitive Scorecard
# ════════════════════════════════════════════════════════════════════════════

def calculate_platform_scores(
    blinkit_df: pd.DataFrame,
    zepto_df: pd.DataFrame,
    bigbasket_df: pd.DataFrame,
    price_mat_df: pd.DataFrame
) -> dict:
    """
    Score each platform 0–100 on 4 competitive dimensions.

    Dimensions
    ----------
    1. Price Competitiveness: % of categories where platform has lowest gap (most discounted)
    2. Catalog Depth: platform product count / max product count × 100
    3. Discount Aggressiveness: platform avg discount / MAX_EXPECTED_DISCOUNT × 100
    4. Category Coverage: unique master categories covered / 6 × 100

    Returns
    -------
    dict with keys: 'Blinkit', 'Zepto', 'BigBasket'
    Each value is a dict with: price_score, depth_score, discount_score,
    coverage_score, overall_score, product_count, avg_discount
    """
    platforms = {
        'Blinkit': blinkit_df,
        'Zepto': zepto_df,
        'BigBasket': bigbasket_df,
    }

    # --- Product counts for depth score ---
    counts = {p: len(df) for p, df in platforms.items()}
    max_count = max(counts.values()) if counts else 1

    # --- Average discounts ---
    avg_discounts = {}
    for p, df in platforms.items():
        if 'discount_pct' in df.columns:
            avg_discounts[p] = float(df['discount_pct'].mean())
        else:
            avg_discounts[p] = 0.0

    # --- Price competitiveness helper ---
    price_analysis = calculate_platform_price_wins(price_mat_df)
    price_wins = price_analysis["price_wins"]
    n_categories = max(price_analysis["total_cats_compared"], 1)

    # --- Category coverage ---
    MASTER_CATS = ['Beverages', 'Dairy & Eggs', 'Fresh Produce',
                   'Bakery & Grains', 'Meat & Snacks', 'Personal Care']
    N_MASTER = len(MASTER_CATS)

    def coverage_score(df, cat_map):
        if 'category' not in df.columns:
            return 0.0
        mapped = df['category'].map(cat_map).dropna().unique()
        covered = len([c for c in mapped if c in MASTER_CATS])
        return covered / N_MASTER * 100

    # Mapping platforms to their specific maps
    bl_coverage = coverage_score(blinkit_df, BLINKIT_CAT_MAP)
    ze_coverage = coverage_score(zepto_df, ZEPTO_CAT_MAP)
    bb_coverage = coverage_score(bigbasket_df, BIGBASKET_CAT_MAP)

    # --- Compile all scores ---
    results = {}
    for platform, cnt, avg_disc, cat_cov, wins in [
        ('Blinkit',   counts['Blinkit'],   avg_discounts['Blinkit'],   bl_coverage, price_wins['Blinkit']),
        ('Zepto',     counts['Zepto'],     avg_discounts['Zepto'],     ze_coverage, price_wins['Zepto']),
        ('BigBasket', counts['BigBasket'], avg_discounts['BigBasket'], bb_coverage, price_wins['BigBasket']),
    ]:
        depth_s    = round(cnt / max_count * 100, 1)
        disc_s     = round(min(avg_disc / MAX_EXPECTED_DISCOUNT * 100, 100), 1)
        coverage_s = round(cat_cov, 1)
        price_s    = round(wins / n_categories * 100, 1)
        overall    = round((price_s + depth_s + disc_s + coverage_s) / 4, 1)

        results[platform] = {
            "price_score": price_s,
            "depth_score": depth_s,
            "discount_score": disc_s,
            "coverage_score": coverage_s,
            "overall_score": overall,
            "product_count": cnt,
            "avg_discount": round(avg_disc, 1),
            "price_wins": wins,
        }
    return results
