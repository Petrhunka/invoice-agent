# Light Theme Configuration

## Overview

The Invoice Payment Manager is now configured to use **Streamlit's light theme** by default for optimal readability and professional appearance.

---

## Configuration File

**Location**: `.streamlit/config.toml`

```toml
[theme]
# Light theme with Keboola branding
primaryColor = "#1F8FFF"              # Keboola blue for buttons and links
backgroundColor = "#FFFFFF"            # White background for main content
secondaryBackgroundColor = "#F5F5F5"  # Light gray for sidebar and cards
textColor = "#212121"                 # Dark text for readability
font = "sans serif"
base = "light"                        # Force light theme mode
```

---

## Visual Elements Optimized

### 1. **Main Content Area**
- ✅ Pure white background (#FFFFFF)
- ✅ Dark text (#212121) for maximum contrast
- ✅ Light blue accents (#E3F2FD) for cards

### 2. **Sidebar**
- ✅ Light gray background (#F5F5F5)
- ✅ Dark text for all labels and content
- ✅ Keboola blue for navigation highlights

### 3. **Tables**
- ✅ White backgrounds forced via CSS
- ✅ Dark text (#212121) for all cells
- ✅ Light gray borders (#E0E0E0)
- ✅ Light blue hover states (#E3F2FD)

### 4. **Charts (Plotly)**
- ✅ Transparent backgrounds
- ✅ Keboola blue primary color
- ✅ Color-coded by decision type (green/red)
- ✅ Clean gridlines

### 5. **Buttons**
- ✅ Primary: Keboola blue (#1F8FFF)
- ✅ Secondary: Darker blue (#0D47A1)
- ✅ White text on colored backgrounds
- ✅ Hover effects for interactivity

### 6. **Metric Cards**
- ✅ Light blue gradient backgrounds
- ✅ Blue left borders (4px)
- ✅ Dark text for values
- ✅ Light gray text for labels

### 7. **Status Indicators**
- ✅ Color-coded factors (🟢🟡🔴)
- ✅ High contrast badges
- ✅ Clear visual hierarchy

---

## CSS Enhancements for Light Theme

The following CSS rules ensure optimal light theme appearance:

### Force Light Background
```css
.stApp {
    background-color: #FFFFFF;
}
```

### Ensure Text Visibility
```css
.stMarkdown, .stText {
    color: #212121;
}
```

### Radio Buttons and Selects
```css
.stRadio label, .stSelectbox label, .stMultiSelect label {
    color: #212121 !important;
}
```

### Tabs Styling
```css
.stTabs [aria-selected="true"] {
    background-color: #E3F2FD;
    color: #1F8FFF;
}
```

### Table Forcing
```css
.dataframe, .dataframe td, .dataframe th {
    background-color: #FFFFFF !important;
    color: #212121 !important;
}
```

---

## Benefits of Light Theme

### 1. **Readability**
- High contrast between text and background
- Reduced eye strain during extended use
- Professional appearance

### 2. **Accessibility**
- WCAG AAA contrast ratios
- Clear visual hierarchy
- Color-blind friendly indicators

### 3. **Professional Look**
- Clean, modern interface
- Keboola branding integrated
- Business-appropriate styling

### 4. **Print-Friendly**
- Reports export well to PDF
- Screenshots look professional
- No dark backgrounds wasting ink

---

## User Experience

### What Users See

1. **Clean White Interface**
   - No dark or gray backgrounds
   - Bright, professional appearance
   - Easy to focus on content

2. **Keboola Blue Accents**
   - Buttons and links in brand color
   - Hover effects consistent
   - Visual feedback clear

3. **Color-Coded Information**
   - Green = Good/Approved
   - Yellow = Warning/Moderate
   - Red = Danger/Rejected
   - Blue = Information

4. **Readable Tables**
   - White cells with dark text
   - Light gray borders
   - Alternating row colors
   - Hover highlights

---

## Customization

### To Change Theme Colors

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#YOUR_COLOR"      # Change primary color
backgroundColor = "#FFFFFF"        # Keep white for light theme
textColor = "#212121"             # Keep dark for readability
```

### To Switch to Dark Theme (Not Recommended)

If you really want dark theme:

```toml
[theme]
base = "dark"
backgroundColor = "#0E1117"
textColor = "#FAFAFA"
```

**Note**: The app is optimized for light theme. Dark theme may require CSS adjustments.

---

## Testing

### Verified Elements

- ✅ Dashboard loads with light theme
- ✅ All text is readable
- ✅ Charts display correctly
- ✅ Tables have white backgrounds
- ✅ Buttons show proper colors
- ✅ Sidebar is light gray
- ✅ No dark elements
- ✅ Color indicators visible
- ✅ Progress bars styled correctly
- ✅ Email previews readable

### Browser Compatibility

Tested and works in:
- ✅ Chrome/Chromium
- ✅ Firefox
- ✅ Safari
- ✅ Edge

---

## Troubleshooting

### Issue: Dark theme still showing
**Solution**: 
1. Clear browser cache
2. Delete `.streamlit/cache` folder
3. Restart Streamlit server

### Issue: Text not visible
**Solution**: 
1. Verify `.streamlit/config.toml` exists
2. Check `base = "light"` is set
3. Restart application

### Issue: Tables have dark backgrounds
**Solution**: 
1. CSS may not be loading
2. Check `styles.py` is imported
3. Verify `load_custom_css()` is called

---

## Files Modified for Light Theme

### New Files
- `.streamlit/config.toml` - Theme configuration

### Modified Files
- `main_simple.py` - Added menu items, theme awareness
- `styles.py` - Enhanced CSS for light theme
- `README.md` - Documented theme configuration
- `QUICKSTART.md` - Added theme note
- `INDEX.md` - Updated file listing

---

## Implementation Details

### Why Light Theme?

1. **Business Context**: Invoice management is a professional business application
2. **User Preference**: Most business users prefer light interfaces
3. **Readability**: Better for extended document review sessions
4. **Printing**: Reports and emails look better on white backgrounds
5. **Accessibility**: Higher contrast for users with visual impairments

### Design Principles

- **Consistency**: All elements follow light theme
- **Contrast**: Minimum 4.5:1 ratio (WCAG AA)
- **Hierarchy**: Color used to show importance
- **Whitespace**: Generous spacing for clarity
- **Branding**: Keboola blue integrated naturally

---

## Future Enhancements

Potential improvements:
- [ ] Theme toggle in settings (optional)
- [ ] Custom color schemes per user
- [ ] High contrast mode
- [ ] Print stylesheet optimization

---

## Conclusion

The light theme configuration provides a **professional, readable, and accessible** interface for the Invoice Payment Manager. All elements are optimized for the light color scheme, ensuring a consistent user experience.

**Theme Status**: ✅ Fully Implemented and Tested

---

**Made with ❤️ by Keboola**

*For questions about theme configuration, see README.md Configuration section*

