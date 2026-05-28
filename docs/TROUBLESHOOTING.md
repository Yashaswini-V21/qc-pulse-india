# Troubleshooting Guide

## Common Issues & Solutions

### 1. Data Loading Issues

#### Problem: "No such file or directory: 'data/clean/groceries_clean.csv'"

**Cause:** Data files are missing from the expected directory

**Solution:**
```bash
# Verify data folder structure
dir data/clean/

# Expected files:
# ✓ blinkit_clean.csv
# ✓ zepto_clean.csv
# ✓ bigbasket_clean.csv
# ✓ groceries_clean.csv
# ✓ rfm_segments.csv
# ✓ rfm_summary.csv
# ✓ price_matrix.csv
# ✓ cohort_retention.csv
# ✓ sankey_data.csv

# Regenerate data by running notebooks
jupyter notebook notebooks/
# Run in order: 01 → 02 → 03 → ... → 07
```

---

### 2. Streamlit Won't Start

#### Problem: "ModuleNotFoundError: No module named 'streamlit'"

**Solution:**
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Verify streamlit installed
streamlit --version

# Try running again
streamlit run app.py
```

---

### 3. Port Already in Use

#### Problem: "Error: Address already in use"

**Solution:**
```bash
# Use different port
streamlit run app.py --server.port 8502

# Or kill existing process
# Windows
taskkill /PID [process_id] /F

# macOS/Linux
lsof -ti:8501 | xargs kill -9
```

---

### 4. Chart Not Rendering

#### Problem: "Plotly charts show as blank"

**Cause:** Missing Plotly or data mismatch

**Solution:**
```bash
# Reinstall Plotly
pip install --upgrade plotly==6.5.2

# Check browser console (F12) for errors
# Restart streamlit
```

---

### 5. Memory Issues

#### Problem: "Streamlit app runs slowly or crashes"

**Solutions:**
- Streamlit auto-caches data (should be fast after 1st run)
- Restart app: `streamlit run app.py`
- Check available RAM: 2GB minimum recommended
- Disable browser extensions that may conflict

---

### 6. Notebook Execution Errors

#### Problem: Jupyter notebook fails to run

**Solution:**
```bash
# Verify dependencies
pip install jupyter pandas numpy plotly python-dateutil pytz

# Start jupyter
jupyter notebook

# Run notebooks in correct order
# 01_data_load → 02_cleaning → 03_price... → etc
```

---

### 7. Column Not Found Errors

#### Problem: "KeyError: 'customer_id'"

**Cause:** Data schema mismatch between notebooks and app

**Solution:**
```bash
# Re-run notebooks to regenerate data
# Verify column names match between:
#   - data/data_schema.md (documentation)
#   - Generated CSV files
#   - Page Python files

# Check data/data_schema.md for exact column names
```

---

### 8. Git Issues

#### Problem: "fatal: not a git repository"

**Solution:**
```bash
# Initialize git repository
git init

# Configure user
git config user.name "Your Name"
git config user.email "your@email.com"

# Add files & commit
git add .
git commit -m "[INIT] Initial commit"
```

---

### 9. GitHub Connection Issues

#### Problem: "fatal: unable to access repository"

**Solutions:**

**If using HTTPS:**
```bash
# Configure credential helper
git config --global credential.helper store

# Try push again (will prompt for credentials)
git push origin main
```

**If using SSH:**
```bash
# Generate SSH key
ssh-keygen -t rsa -b 4096

# Add to GitHub Settings → SSH Keys
# Copy public key from ~/.ssh/id_rsa.pub

# Test connection
ssh -T git@github.com

# Update remote to SSH
git remote set-url origin git@github.com:Yashaswini-V21/qc-pulse-india.git
```

---

### 10. Browser Compatibility

#### Problem: Dashboard looks broken in some browsers

**Supported browsers:**
- ✅ Chrome/Chromium (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge

**Solution:**
- Use Chrome for best experience
- Check browser console for JavaScript errors (F12)
- Clear browser cache (Ctrl+Shift+Delete)

---

## Performance Optimization

### Streamlit Caching
Streamlit caches data automatically:
- **First run**: 2-3 seconds (all data loads)
- **Subsequent runs**: <200ms (from cache)

### Clear Cache
```bash
# Option 1: Restart app
# Ctrl+C in terminal, then run again

# Option 2: Clear Streamlit cache
# Remove .streamlit/cache folder

# Option 3: Use Streamlit cache button
# In UI: Settings → Clear Cache
```

---

## Debug Mode

Enable detailed logging:
```bash
streamlit run app.py --logger.level=debug
```

---

## Getting Help

1. **Check existing issues**: github.com/Yashaswini-V21/qc-pulse-india/issues
2. **Search Stack Overflow**: tag `streamlit`, `pandas`, `plotly`
3. **Email**: yashasyashu0987@gmail.com
4. **Streamlit Docs**: docs.streamlit.io

---

## Still Stuck?

Provide these details when asking for help:
- Python version: `python --version`
- Streamlit version: `streamlit --version`
- Operating system: Windows/Mac/Linux
- Full error message & traceback
- Steps to reproduce
- Screenshot if UI issue
