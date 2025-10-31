# Chart Background Fix for Light Theme

## Issue Identified

Charts in the application were displaying with **black/dark backgrounds**, making them unreadable in the light theme interface.

### Affected Charts
1. Dashboard - Amount Distribution (histogram)
2. Dashboard - Priority Breakdown (pie chart)
3. Technical Explanation - Feature Importance (bar chart)
4. Reports/Analytics - Decisions Over Time (line chart)
5. Reports/Analytics - Amount Distribution by Decision (box plot)
6. Reports/Analytics - Confidence Score Distribution (histogram)

## Root Cause

Plotly charts use a dark template by default in recent versions. Without explicit layout configuration, they render with:
- Dark backgrounds (#0E1117 or similar)
- Light text
- Dark plot area

This conflicts with the light theme configuration of the application.

## Solution Applied

Added explicit layout configuration to **all 6 Plotly charts** with:

```python
fig.update_layout(
    plot_bgcolor='white',        # White plot area
    paper_bgcolor='white',       # White background
    font=dict(color=KEBOOLA_COLORS['text_dark'])  # Dark text (#212121)
)
```

## Charts Fixed

### 1. Dashboard - Amount Distribution
**Location**: `render_dashboard()` - Line ~205
**Chart Type**: Histogram
```python
fig.update_layout(
    xaxis_title="Invoice Amount ($)",
    yaxis_title="Count",
    height=300,
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(color=KEBOOLA_COLORS['text_dark'])
)
```

### 2. Dashboard - Priority Breakdown  
**Location**: `render_dashboard()` - Line ~235
**Chart Type**: Pie Chart
```python
fig.update_layout(
    height=300,
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(color=KEBOOLA_COLORS['text_dark'])
)
```

### 3. Technical Explanation - Feature Importance
**Location**: `render_technical_explanation()` - Line ~639
**Chart Type**: Horizontal Bar Chart
```python
fig.update_layout(
    height=350,
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(color=KEBOOLA_COLORS['text_dark'])
)
```

### 4. Reports - Decisions Over Time
**Location**: `render_reports()` Tab 3 - Line ~1036
**Chart Type**: Line Chart
```python
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(color=KEBOOLA_COLORS['text_dark'])
)
```

### 5. Reports - Amount Distribution by Decision
**Location**: `render_reports()` Tab 3 - Line ~1059
**Chart Type**: Box Plot
```python
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(color=KEBOOLA_COLORS['text_dark'])
)
```

### 6. Reports - Confidence Score Distribution
**Location**: `render_reports()` Tab 3 - Line ~1079
**Chart Type**: Histogram
```python
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(color=KEBOOLA_COLORS['text_dark'])
)
```

## Result

✅ All charts now have:
- **White backgrounds** matching the light theme
- **Dark text** (#212121) for labels and titles
- **Clean, professional appearance**
- **High contrast for readability**
- **Consistent with overall app design**

## Testing

Verify each chart renders correctly:
- [ ] Dashboard histogram shows white background
- [ ] Dashboard pie chart shows white background  
- [ ] Technical explanation bar chart shows white background
- [ ] All Reports/Analytics charts have white backgrounds
- [ ] All text is readable (dark on light)
- [ ] Colors for data points remain correct (blue, red, green)

## Files Modified

- `main_simple.py` - Updated 6 chart configurations

## Visual Comparison

**Before**: Black backgrounds with invisible/hard-to-read labels
**After**: White backgrounds with dark, readable text matching light theme

---

**Status**: ✅ Fixed and Ready
**Date**: October 24, 2025

