"""
Premium Plotly Chart Theme — "Vibrant Dark Intelligence" Design System
Applies consistent cyber-neon styling to all Plotly figures across the dashboard.
"""
import plotly.graph_objects as go
from utils.config import PLATFORM_COLORS, SEGMENT_COLORS


# ─── BASE LAYOUT ─────────────────────────────────────────────
PREMIUM_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(7,10,22,0.5)',
    font=dict(
        family='Outfit',
        color='#94A3B8',
        size=12
    ),
    margin=dict(l=0, r=0, t=10, b=0),
    xaxis=dict(
        gridcolor='rgba(139,92,246,0.08)',
        linecolor='rgba(139,92,246,0.15)',
        tickcolor='rgba(139,92,246,0.3)',
        color='#94A3B8',
        zeroline=False,
    ),
    yaxis=dict(
        gridcolor='rgba(139,92,246,0.08)',
        linecolor='rgba(139,92,246,0.15)',
        tickcolor='rgba(139,92,246,0.3)',
        color='#94A3B8',
        zeroline=False,
    ),
    legend=dict(
        bgcolor='rgba(5,8,16,0.85)',
        bordercolor='rgba(139,92,246,0.3)',
        borderwidth=1,
        font=dict(color='#E2E8F0', size=11),
    ),
    hoverlabel=dict(
        bgcolor='rgba(5,8,16,0.95)',
        bordercolor='rgba(6,182,212,0.4)',
        font=dict(color='#FFFFFF', size=12, family='Outfit'),
    ),
)


# ─── COLOR SCHEMES ───────────────────────────────────────────

# Retention heatmap: Deep Dark Violet -> Neon Purple -> Electric Blue -> Hot Pink
RETENTION_COLORSCALE = [
    [0.0, '#12072B'],
    [0.3, '#4C1D95'],
    [0.6, '#7C3AED'],
    [0.8, '#A78BFA'],
    [1.0, '#EC4899'],
]

# Price gap heatmap: Emerald Green (cheap) -> Space Slate -> Hot Crimson Red (expensive)
PRICE_GAP_COLORSCALE = [
    [0.0, '#065F46'],  # deep green
    [0.3, '#059669'],  # emerald green
    [0.5, '#0F172A'],  # slate slate
    [0.7, '#DC2626'],  # red
    [1.0, '#991B1B'],  # dark crimson
]

# Platform colors mapped from core config
PLATFORM_COLORS_NEW = PLATFORM_COLORS

# Segment scatter colors mapped from core config
SEGMENT_SCATTER_COLORS = SEGMENT_COLORS

# Platform pie/donut map matching platform neon definitions
PLATFORM_PIE_COLORS = PLATFORM_COLORS_NEW

# Bar chart defaults
BAR_COLOR = '#8B5CF6'
BAR_COLOR_SEQUENCE = ['#8B5CF6', '#06B6D4', '#FF3366', '#00F5A0', '#F59E0B']

# Line chart defaults
LINE_COLOR = '#06B6D4'
LINE_MARKER_COLOR = '#22D3EE'

# Category colors for Sankey (Translucent cyberpunk glow)
CATEGORY_COLORS_NEW = {
    'Dairy':           '#FF3366',  # Magenta
    'Fresh Produce':   '#00F5A0',  # Neon Mint
    'Bakery & Grains': '#B923FF',  # Cyber Purple
    'Beverages':       '#06B6D4',  # Bright Cyan
    'Meat & Snacks':   '#F59E0B',  # Amber Glow
    'Other':           '#64748B',  # Cool Slate
}

# Outcome colors for Sankey
OUTCOME_COLORS = {
    'Retained High-Value': '#00F5A0',
    'Retained':            '#FBBF24',
    'Churned':             '#EF4444',
}


def apply_premium_theme(fig: go.Figure, height: int = 400, **overrides) -> go.Figure:
    """
    Apply the premium 'Vibrant Dark Intelligence' theme to any Plotly figure.

    Args:
        fig: Plotly Figure object.
        height: Chart height in pixels.
        **overrides: Any additional layout overrides (e.g., title, margin).

    Returns:
        The same figure with premium styling applied.
    """
    layout_kwargs = {**PREMIUM_LAYOUT, 'height': height}
    layout_kwargs.update(overrides)
    fig.update_layout(**layout_kwargs)
    return fig


def apply_premium_theme_no_axes(fig: go.Figure, height: int = 400, **overrides) -> go.Figure:
    """
    Apply premium theme WITHOUT xaxis/yaxis overrides — for pie/polar/sankey charts.
    """
    layout_kwargs = {
        k: v for k, v in PREMIUM_LAYOUT.items()
        if k not in ('xaxis', 'yaxis')
    }
    layout_kwargs['height'] = height
    layout_kwargs.update(overrides)
    fig.update_layout(**layout_kwargs)
    return fig


def hex_to_rgba(hex_str: str, opacity: float = 0.65) -> str:
    """Convert hex color to rgba string."""
    hex_str = hex_str.lstrip('#')
    r = int(hex_str[0:2], 16)
    g = int(hex_str[2:4], 16)
    b = int(hex_str[4:6], 16)
    return f"rgba({r},{g},{b},{opacity})"
