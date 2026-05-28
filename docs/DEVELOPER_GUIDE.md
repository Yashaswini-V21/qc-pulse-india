# 🛠️ QC Pulse India — Developer & Guide Manual

Welcome to the **QC Pulse India** Quick Commerce Analytics platform. This guide provides developers and analysts with step-by-step instructions on setting up the workspace, running the interactive dashboard, executing the data pipeline, running automated tests, and resolving common environment issues.

---

## 📋 Table of Contents

1. [Local Workspace Setup](#1-local-workspace-setup)
2. [Running the Streamlit Dashboard](#2-running-the-streamlit-dashboard)
3. [Running the Automated Data Pipeline](#3-running-the-automated-data-pipeline)
4. [Running the Automated Tests](#4-running-the-automated-tests)
5. [Troubleshooting Guide](#5-troubleshooting-guide)

---

## 1. Local Workspace Setup

Follow these steps to configure your Python environment and verify dataset presence.

### Prerequisites
- Python 3.8+ (Recommended: Python 3.9 or 3.10)
- `pip` package manager

### Environment Configuration
1. Open your terminal in the root of the workspace (`QC_Pulse_India`).
2. Create a clean virtual environment:
   ```bash
   python -m venv .venv
   ```
3. Activate the virtual environment:
   - **Windows PowerShell**:
     ```powershell
     .venv\Scripts\activate
     ```
   - **Windows Command Prompt (cmd)**:
     ```cmd
     .venv\Scripts\activate.bat
     ```
   - **macOS/Linux**:
     ```bash
     source .venv/bin/activate
     ```
4. Install all required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 2. Running the Streamlit Dashboard

To launch the interactive multi-page dashboard, run:

```bash
streamlit run app.py
```

Once running, the application will automatically launch in your default web browser at `http://localhost:8501`.

### Core Features & Visual Layout
- **Overview Dashboard**: High-level platform comparisons, active statistics counters, and custom red-gradient bar charts.
- **Price Intelligence**: Competitive matrix comparing item prices across Zepto, Blinkit, and BigBasket.
- **Customer Segments**: RFM analysis showing Champion vs Churned customer groupings.
- **Cohort Retention**: Month-by-month retention matrices.
- **Customer Journey**: Sankey diagram visualizing flows from acquisition to long-term segments.
- **Market Basket Analysis**: Apriori association rules and interactive bundle recommendations.
- **Review & Rating**: Ratings distribution, category trends, and discount-to-rating correlations.

---

## 3. Running the Automated Data Pipeline

The data analysis and model training reside in the `notebooks/` directory. Rather than executing Jupyter notebooks manually, the platform includes a unified orchestrator script that executes all steps end-to-end.

To run the pipeline and regenerate all processed datasets in `data/clean/`:

```bash
python run_pipeline.py
```

### Pipeline Progression Sequence:
1. `01_data_load.ipynb`: Ingests raw platform datasets from `data/raw/`.
2. `02_cleaning.ipynb`: Preprocesses, filters nulls, and standardizes category names.
3. `03_price_intelligence.ipynb`: Calculates the competitive pricing and discount matrices.
4. `04_basket_analysis.ipynb`: Discovers frequent itemsets and prints association rules.
5. `05_rfm_segmentation.ipynb`: Groups customers into actionable personas (e.g. Champions, Churned).
6. `06_cohort_retention.ipynb`: Builds monthly retention tables.
7. `07_sankey.ipynb`: Maps user journey pathways.

---

## 4. Running the Automated Tests

To verify code changes, data integrity, and pipeline consistency, execute the unit test suite:

```bash
python -m unittest tests.test_data_loader -v
```

This tests standard loading operations, ensures consistent row/column schemas, and validates customer RFM boundaries.

---

## 5. Troubleshooting Guide

### Issue: "No such file or directory: 'data/clean/...'"
- **Cause**: Clean datasets have not been generated yet.
- **Solution**: Execute the automated pipeline using `python run_pipeline.py` to process the raw datasets.

### Issue: "ModuleNotFoundError: No module named 'streamlit'" or other import error
- **Cause**: Script was executed outside the virtual environment.
- **Solution**: Activate your virtual environment first (`.venv\Scripts\activate` on Windows), then run the command. If issues persist, reinstall dependencies:
  ```bash
  pip install --force-reinstall -r requirements.txt
  ```

### Issue: "Address already in use / Port 8501 busy"
- **Cause**: Another instance of Streamlit (or another app) is running on port 8501.
- **Solution**: Stop the current process or launch the dashboard on an alternative port:
  ```bash
  streamlit run app.py --server.port 8502
  ```

### Issue: "UnicodeEncodeError: 'charmap' codec can't encode..."
- **Cause**: Terminal is running with an encoding that does not support Unicode character output (common in Windows cmd).
- **Solution**: Force the terminal session to use UTF-8 encoding or set environment variables before running:
  - **PowerShell**:
    ```powershell
    $env:PYTHONIOENCODING="utf-8"
    ```
  - **CMD**:
    ```cmd
    set PYTHONIOENCODING=utf-8
    ```
