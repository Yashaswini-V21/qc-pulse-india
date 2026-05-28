# ═══════════════════════════════════════════════════════════
# CONFIG — QC Pulse India
# ═══════════════════════════════════════════════════════════

# ─── COLORS ─────────────────────────────────────────────────
COLORS = {
    'background': '#0F172A',
    'sidebar': '#1E293B',
    'border': '#334155',
    'text_light': '#F8FAFC',
    'text_muted': '#94A3B8',
    'text_dim': '#64748B',
    'red': '#DC2626',
    'orange': '#F97316',
    'purple': '#6C63DB',
    'amber': '#F59E0B',
    'gray': '#64748B',
    'green': '#1D9E75',
}

PLATFORM_COLORS = {
    'BigBasket': '#6C63DB',
    'Blinkit': '#DC2626',
    'Zepto': '#1D9E75',
}

SEGMENT_COLORS = {
    'Champion': '#DC2626',
    'Loyal': '#F97316',
    'Potential': '#6C63DB',
    'At-Risk': '#F59E0B',
    'Churned': '#64748B',
}

CATEGORY_COLORS = {
    'Dairy': 'rgba(220,38,38,0.6)',
    'Fresh Produce': 'rgba(29,158,117,0.6)',
    'Bakery & Grains': 'rgba(108,99,219,0.6)',
    'Beverages': 'rgba(14,165,233,0.6)',
    'Meat & Snacks': 'rgba(245,158,11,0.6)',
    'Other': 'rgba(100,116,139,0.6)',
}

# ─── LAYOUT ─────────────────────────────────────────────────
CHART_HEIGHT = 380
HEATMAP_HEIGHT = 450
RETENTION_HEATMAP_HEIGHT = 560
SANKEY_HEIGHT = 600

CHART_FONT_SIZE = 11
CHART_FONT_SIZE_LARGE = 13

METRIC_PADDING = 16

# ─── FONTS ──────────────────────────────────────────────────
FONT_REGULAR = dict(color='white', size=CHART_FONT_SIZE)
FONT_LARGE = dict(color='white', size=CHART_FONT_SIZE_LARGE)

# ─── MARGINS ────────────────────────────────────────────────
MARGIN_COMPACT = dict(l=0, r=0, t=10, b=0)
MARGIN_WITH_TOP = dict(l=0, r=0, t=40, b=0)

# ─── DATA FILES ─────────────────────────────────────────────
DATA_FILES = {
    'blinkit': 'data/clean/blinkit_clean.csv',
    'zepto': 'data/clean/zepto_clean.csv',
    'bigbasket': 'data/clean/bigbasket_clean.csv',
    'groceries': 'data/clean/groceries_clean.csv',
    'rfm': 'data/clean/rfm_segments.csv',
    'rfm_summary': 'data/clean/rfm_summary.csv',
    'price_matrix': 'data/clean/price_matrix.csv',
    'cohort': 'data/clean/cohort_retention.csv',
    'sankey': 'data/clean/sankey_data.csv',
}

# ─── MESSAGES ────────────────────────────────────────────────
ERROR_MESSAGES = {
    'data_not_found': '📁 Data file not found: {}. Please ensure all CSV files are in the data/clean/ directory.',
    'data_invalid': '⚠️ Data validation failed: {}',
    'missing_column': '❌ Required column "{}" not found in {}',
}

# ─── SIMULATION & INTELLIGENCE PARAMETERS ────────────────────
AVG_ORDER_VALUE = 350          # ₹ — standard Indian quick-commerce basket
ORDERS_PER_MONTH_WINBACK = 2   # realistic order frequency for recovered churned customers (1-2 recommended)
CHAMPION_LTV_ITEMS = 16.9      # from rfm_summary: avg_monetary for Champions
PRICE_ELASTICITY = -2.0        # standard retail price elasticity assumption
MAX_EXPECTED_DISCOUNT = 40.0   # 40% = upper bound for discount aggressiveness scoring


# ─── CATEGORY MAPPINGS ────────────────────────────────────────
BLINKIT_CAT_MAP = {
    'Fruits and Vegetables': 'Fresh Produce', 'Dairy': 'Dairy & Eggs',
    'Soft Drinks': 'Beverages', 'Baking Goods': 'Bakery & Grains',
    'Snack Foods': 'Meat & Snacks', 'Breads': 'Bakery & Grains',
    'Meat': 'Meat & Snacks', 'Seafood': 'Meat & Snacks',
    'Breakfast': 'Bakery & Grains', 'Health and Hygiene': 'Personal Care',
    'Starchy Foods': 'Bakery & Grains', 'Household': 'Personal Care',
}

BIGBASKET_CAT_MAP = {
    'Beverages': 'Beverages', 'Bakery, Cakes & Dairy': 'Dairy & Eggs',
    'Fruits & Vegetables': 'Fresh Produce', 'Foodgrains, Oil & Masala': 'Bakery & Grains',
    'Snacks & Branded Foods': 'Meat & Snacks', 'Eggs, Meat & Fish': 'Meat & Snacks',
    'Beauty & Hygiene': 'Personal Care', 'Cleaning & Household': 'Personal Care',
}

ZEPTO_CAT_MAP = {
    'Fruits & Vegetables': 'Fresh Produce', 'Dairy, Bread & Batter': 'Dairy & Eggs',
    'Beverages': 'Beverages', 'Munchies': 'Meat & Snacks',
    'Meats, Fish & Eggs': 'Meat & Snacks', 'Biscuits': 'Bakery & Grains',
    'Packaged Food': 'Bakery & Grains', 'Personal Care': 'Personal Care',
}

# Standard mapping for the Review & Rating page
BLINKIT_REVIEW_CAT_MAP = {
    'Fruits and Vegetables': 'Fresh Produce', 'Health and Hygiene': 'Other',
    'Frozen Foods': 'Meat & Snacks', 'Canned': 'Other', 'Soft Drinks': 'Beverages',
    'Dairy': 'Dairy', 'Baking Goods': 'Bakery & Grains', 'Snack Foods': 'Meat & Snacks',
    'Household': 'Other', 'Breads': 'Bakery & Grains', 'Meat': 'Meat & Snacks',
    'Seafood': 'Meat & Snacks', 'Breakfast': 'Bakery & Grains', 'Starchy Foods': 'Bakery & Grains'
}

BIGBASKET_REVIEW_CAT_MAP = {
    'Beauty & Hygiene': 'Other', 'Kitchen, Garden & Pets': 'Other',
    'Cleaning & Household': 'Other', 'Gourmet & World Food': 'Other',
    'Foodgrains, Oil & Masala': 'Bakery & Grains', 'Snacks & Branded Foods': 'Meat & Snacks',
    'Beverages': 'Beverages', 'Bakery, Cakes & Dairy': 'Dairy',
    'Fruits & Vegetables': 'Fresh Produce', 'Eggs, Meat & Fish': 'Meat & Snacks',
    'Baby Care': 'Other'
}


