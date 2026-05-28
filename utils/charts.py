"""Chart utilities and styling functions with type hints."""
import logging
import plotly.graph_objects as go
from config import COLORS, MARGIN_COMPACT, FONT_REGULAR, FONT_LARGE
from typing import Optional, Union, Dict, Any

logger = logging.getLogger(__name__)


def apply_chart_theme(
    fig: go.Figure,
    height: int = 400,
    margin: Optional[Dict[str, int]] = None,
    font_size: str = 'regular'
) -> go.Figure:
    """
    Apply consistent dark theme styling to Plotly figures.
    
    Args:
        fig (go.Figure): Plotly figure object
        height (int): Chart height in pixels (default: 400)
        margin (dict): Margin settings (default: MARGIN_COMPACT)
        font_size (str): 'regular' or 'large' (default: 'regular')
    
    Returns:
        go.Figure: Styled figure
        
    Raises:
        TypeError: If fig is not a Plotly Figure
    """
    if margin is None:
        margin = MARGIN_COMPACT
    
    font = FONT_LARGE if font_size == 'large' else FONT_REGULAR
    
    try:
        fig.update_layout(
            height=height,
            plot_bgcolor=COLORS['sidebar'],
            paper_bgcolor=COLORS['sidebar'],
            font=font,
            margin=margin,
            showlegend=True,
        )
        
        fig.update_xaxes(color=COLORS['text_light'], gridcolor=COLORS['border'])
        fig.update_yaxes(color=COLORS['text_light'], gridcolor=COLORS['border'])
        
        logger.debug(f"Applied theme to chart (height={height}, font={font_size})")
        return fig
    except Exception as e:
        logger.error(f"Error applying chart theme: {str(e)}")
        raise


def style_heatmap(
    fig: go.Figure,
    height: int = 400,
    zmid: Optional[Union[int, float]] = None
) -> go.Figure:
    """
    Apply heatmap styling with dark theme.
    
    Args:
        fig (go.Figure): Plotly heatmap figure
        height (int): Chart height in pixels (default: 400)
        zmid (float): Midpoint for color scale (optional)
    
    Returns:
        go.Figure: Styled heatmap
    """
    try:
        fig.update_layout(
            height=height,
            plot_bgcolor=COLORS['sidebar'],
            paper_bgcolor=COLORS['sidebar'],
            font=FONT_LARGE,
            xaxis=dict(side='top', color=COLORS['text_light']),
            yaxis=dict(color=COLORS['text_light']),
            margin=dict(l=0, r=0, t=40, b=0),
            coloraxis_colorbar=dict(
                tickfont=dict(color=COLORS['text_light'])
            )
        )
        
        if zmid is not None:
            fig.update_traces(zmid=zmid)
        
        logger.debug(f"Applied heatmap styling (height={height})")
        return fig
    except Exception as e:
        logger.error(f"Error applying heatmap styling: {str(e)}")
        raise


def style_sankey(fig: go.Figure) -> go.Figure:
    """
    Apply Sankey diagram styling with dark theme.
    
    Args:
        fig (go.Figure): Plotly Sankey figure
    
    Returns:
        go.Figure: Styled Sankey diagram
    """
    try:
        fig.update_layout(
            height=600,
            paper_bgcolor=COLORS['sidebar'],
            font=dict(color=COLORS['text_light'], size=12),
            margin=MARGIN_COMPACT,
        )
        
        logger.debug("Applied Sankey styling")
        return fig
    except Exception as e:
        logger.error(f"Error applying Sankey styling: {str(e)}")
        raise


def get_safe_metric_value(
    df: Any,
    column_name: str,
    operation: str = 'median',
    default: Union[int, float] = 0
) -> Union[int, float]:
    """
    Safely get a metric value from a dataframe with fallback.
    
    Args:
        df (pd.DataFrame): Source dataframe
        column_name (str): Column to aggregate
        operation (str): 'median', 'mean', 'sum', 'max', 'min' (default: 'median')
        default (float): Value to return if column doesn't exist (default: 0)
    
    Returns:
        float: Calculated value or default
        
    Examples:
        >>> get_safe_metric_value(df, 'price', 'mean', default=0)
        1234.56
    """
    if column_name not in df.columns:
        logger.debug(f"Column '{column_name}' not found in dataframe, returning default")
        return default
    
    try:
        if operation == 'median':
            return df[column_name].median()
        elif operation == 'mean':
            return df[column_name].mean()
        elif operation == 'sum':
            return df[column_name].sum()
        elif operation == 'max':
            return df[column_name].max()
        elif operation == 'min':
            return df[column_name].min()
        else:
            logger.warning(f"Unknown operation '{operation}', returning default")
            return default
    except Exception as e:
        logger.warning(f"Error computing {operation} for '{column_name}': {str(e)}")
        return default

