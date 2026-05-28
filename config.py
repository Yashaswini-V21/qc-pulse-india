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
