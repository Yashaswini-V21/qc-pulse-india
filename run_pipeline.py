import os
import sys
import json
import subprocess
import time

INJECTED_UTILS = """
import pandas as pd

def display(*args, **kwargs):
    for arg in args:
        if isinstance(arg, pd.DataFrame):
            print(f"DataFrame: {arg.shape[0]} rows x {arg.shape[1]} cols")
            print(arg.head(5).to_string())
        else:
            print(arg)

class DummyIPython:
    def run_line_magic(self, *args, **kwargs):
        pass
    def run_cell_magic(self, *args, **kwargs):
        pass

def get_ipython():
    return DummyIPython()
"""

def run_notebook(notebook_path):
    print(f"\n==================================================")
    print(f"[RUN] Running {os.path.basename(notebook_path)}...")
    print(f"==================================================")
    
    start_time = time.time()
    
    # Read notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    # Extract code cells
    code_lines = [INJECTED_UTILS]
    for cell in nb.get('cells', []):
        if cell.get('cell_type') == 'code':
            source = cell.get('source', [])
            if isinstance(source, list):
                source_code = "".join(source)
            else:
                source_code = source
            
            # Skip magic commands (lines starting with % or !)
            filtered_lines = []
            for line in source_code.splitlines():
                stripped = line.strip()
                if stripped.startswith('%') or stripped.startswith('!'):
                    filtered_lines.append(f"# {line}")
                else:
                    filtered_lines.append(line)
            
            code_lines.append("\n".join(filtered_lines))
    
    full_code = "\n\n# --- CELL ---\n\n".join(code_lines)
    
    # NOTE: No parameter substitutions are applied.
    # The basket analysis (04) uses min_support=0.005 as written in the notebook.
    # If this produces few rules, that is a real finding — do not silently
    # lower the threshold to produce "better-looking" results.
    # See notebooks/04_basket_analysis.ipynb Cell 3 for full parameter rationale.

    # Write to a temporary python file in notebooks/ directory
    notebooks_dir = os.path.dirname(os.path.abspath(notebook_path))
    temp_filename = f"temp_{os.path.splitext(os.path.basename(notebook_path))[0]}.py"
    temp_path = os.path.join(notebooks_dir, temp_filename)

    with open(temp_path, 'w', encoding='utf-8') as f:
        f.write(full_code)

    try:
        # Set PYTHONIOENCODING in environment to prevent UnicodeEncodeError in subprocess
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'

        # Run python script in subprocess with working directory set to notebooks/
        result = subprocess.run(
            [sys.executable, temp_filename],
            cwd=notebooks_dir,
            env=env,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )

        # Display output
        if result.stdout:
            print("--- Standard Output ---")
            # Replace non-ascii chars in stdout if any when printing to terminal
            clean_stdout = result.stdout.encode('ascii', errors='replace').decode('ascii')
            print(clean_stdout.strip())

        if result.stderr:
            print("--- Error/Warning Output ---")
            clean_stderr = result.stderr.encode('ascii', errors='replace').decode('ascii')
            print(clean_stderr.strip())

        if result.returncode == 0:
            elapsed = time.time() - start_time
            print(f"[OK] {os.path.basename(notebook_path)} completed successfully in {elapsed:.2f}s")
            return True
        else:
            print(f"[ERROR] {os.path.basename(notebook_path)} failed with exit code {result.returncode}")
            return False

    except Exception as e:
        print(f"[ERROR] Exception occurred running {notebook_path}: {e}")
        return False
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    notebooks_dir = os.path.join(base_dir, 'notebooks')

    notebooks = [
        '01_data_load.ipynb',
        '02_cleaning.ipynb',
        '03_price_intelligence.ipynb',
        '04_basket_analysis.ipynb',   # min_support=0.005 — may yield sparse rules (expected)
        '05_rfm_segmentation.ipynb',
        '06_cohort_retention.ipynb',
        '07_sankey.ipynb',
        # '08_data_quality.ipynb',    # Optional — Data Quality page computes IQR live
    ]

    
    success_count = 0
    total_start_time = time.time()
    
    print("[START] Starting QC Pulse India Data Pipeline Orchestrator")
    print(f"Notebooks directory: {notebooks_dir}")
    
    for nb in notebooks:
        nb_path = os.path.join(notebooks_dir, nb)
        if not os.path.exists(nb_path):
            print(f"[ERROR] Notebook {nb} not found at {nb_path}!")
            sys.exit(1)
            
        success = run_notebook(nb_path)
        if not success:
            print("\n[ERROR] Pipeline stopped due to execution failure.")
            sys.exit(1)
        success_count += 1
        
    total_elapsed = time.time() - total_start_time
    print(f"\n[SUCCESS] Pipeline executed successfully! {success_count}/{len(notebooks)} notebooks run in {total_elapsed:.2f}s.")

if __name__ == '__main__':
    main()
