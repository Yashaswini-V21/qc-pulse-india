# ═══════════════════════════════════════════════════════════
# CONFIG — QC Pulse India  ·  "Dark Intelligence" Design System
# ═══════════════════════════════════════════════════════════

# ─── COLORS — Premium Palette ───────────────────────────────
COLORS = {
    'space_black':    '#050810',
    'deep_navy':      '#0A0F1E',
    'card_bg':        '#0D1117',
    'card_border':    'rgba(139, 92, 246, 0.15)',
    'card_hover':     'rgba(139, 92, 246, 0.25)',
    'purple_primary': '#8B5CF6',
    'purple_light':   '#A78BFA',
    'blue_accent':    '#3B82F6',
    'teal_accent':    '#06B6D4',
    'green_success':  '#10B981',
    'red_alert':      '#EF4444',
    'amber_warn':     '#F59E0B',
    'text_primary':   '#F8FAFC',
    'text_secondary': '#94A3B8',
    'text_muted':     '#475569',
    'glow_purple':    'rgba(139, 92, 246, 0.4)',
    'glow_blue':      'rgba(59, 130, 246, 0.3)',
}

PLATFORM_COLORS = {
    'BigBasket': '#B923FF',   # Neon Cyber Purple
    'Blinkit':   '#FF3366',   # Hot Pink-Red
    'Zepto':     '#00F5A0',   # Vivid Neon Mint Green
}

SEGMENT_COLORS = {
    'Champion':  '#EC4899',   # Hot Pink
    'Loyal':     '#3B82F6',   # Electric Blue
    'Potential': '#10B981',   # Emerald Green
    'At-Risk':   '#F59E0B',   # Amber Glow
    'Churned':   '#EF4444',   # Cyber Red
}

CATEGORY_COLORS = {
    'Dairy':           'rgba(239,68,68,0.6)',
    'Fresh Produce':   'rgba(16,185,129,0.6)',
    'Bakery & Grains': 'rgba(139,92,246,0.6)',
    'Beverages':       'rgba(6,182,212,0.6)',
    'Meat & Snacks':   'rgba(245,158,11,0.6)',
    'Other':           'rgba(71,85,105,0.6)',
}

# ─── LAYOUT ─────────────────────────────────────────────────
CHART_HEIGHT = 380
HEATMAP_HEIGHT = 460
RETENTION_HEATMAP_HEIGHT = 580
SANKEY_HEIGHT = 620

CHART_FONT_SIZE = 11
CHART_FONT_SIZE_LARGE = 13

METRIC_PADDING = 16

# ─── FONTS ──────────────────────────────────────────────────
FONT_REGULAR = dict(color='#94A3B8', size=CHART_FONT_SIZE, family='Inter')
FONT_LARGE = dict(color='#F8FAFC', size=CHART_FONT_SIZE_LARGE, family='Inter')

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
