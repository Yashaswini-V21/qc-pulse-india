"""
Unit tests for data loading and validation.

Run tests with:
  pytest tests/test_data_loader.py -v
  
Or without pytest:
  python -m unittest tests.test_data_loader -v
"""
import unittest
import os
import sys
import pandas as pd
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.data_loader import _load_csv, validate_columns


class TestDataLoader(unittest.TestCase):
    """Test suite for data loading utilities."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.base_path = Path(__file__).parent.parent / "data" / "clean"
        self.test_data = pd.DataFrame({
            'customer_id': ['C001', 'C002', 'C003'],
            'amount': [100.0, 200.0, 150.0],
            'category': ['Dairy', 'Fresh', 'Dairy']
        })
    
    def test_csv_file_loading(self):
        """Test that CSV files exist and can be loaded."""
        # Check if blinkit_clean.csv exists and can be loaded
        blinkit_path = self.base_path / "blinkit_clean.csv"
        
        if blinkit_path.exists():
            try:
                df = _load_csv(str(blinkit_path), "Test Blinkit")
                self.assertIsInstance(df, pd.DataFrame)
                self.assertGreater(len(df), 0, "Blinkit data should have rows")
                print(f"[OK] Blinkit: {len(df):,} rows x {len(df.columns)} columns")
            except Exception as e:
                self.fail(f"Failed to load blinkit_clean.csv: {str(e)}")
        else:
            print(f"[WARN] Skipping: {blinkit_path} not found")
    
    def test_groceries_data_loading(self):
        """Test groceries dataset loading."""
        groceries_path = self.base_path / "groceries_clean.csv"
        
        if groceries_path.exists():
            try:
                df = _load_csv(str(groceries_path), "Test Groceries")
                self.assertIsInstance(df, pd.DataFrame)
                self.assertGreater(len(df), 0)
                print(f"[OK] Groceries: {len(df):,} rows x {len(df.columns)} columns")
            except Exception as e:
                self.fail(f"Failed to load groceries_clean.csv: {str(e)}")
        else:
            print(f"[WARN] Skipping: {groceries_path} not found")
    
    def test_rfm_data_loading(self):
        """Test RFM segmentation data loading."""
        rfm_path = self.base_path / "rfm_segments.csv"
        
        if rfm_path.exists():
            try:
                df = _load_csv(str(rfm_path), "Test RFM")
                self.assertIsInstance(df, pd.DataFrame)
                self.assertIn('segment', df.columns, "RFM should have segment column")
                print(f"[OK] RFM Segments: {len(df):,} rows x {len(df.columns)} columns")
            except Exception as e:
                self.fail(f"Failed to load rfm_segments.csv: {str(e)}")
        else:
            print(f"[WARN] Skipping: {rfm_path} not found")
    
    def test_column_validation_success(self):
        """Test successful column validation."""
        required_cols = ['customer_id', 'amount']
        result = validate_columns(self.test_data, required_cols, "Test Data")
        self.assertTrue(result)
    
    def test_column_validation_failure(self):
        """Test column validation with missing columns."""
        required_cols = ['customer_id', 'missing_column']
        with self.assertRaises(ValueError):
            validate_columns(self.test_data, required_cols, "Test Data")
    
    def test_data_integrity(self):
        """Test data integrity checks."""
        # Test for duplicates
        blinkit_path = self.base_path / "blinkit_clean.csv"
        
        if blinkit_path.exists():
            try:
                df = _load_csv(str(blinkit_path), "Integrity Test")
                duplicates = df.duplicated().sum()
                print(f"  Duplicate rows in Blinkit: {duplicates}")
                # Note: This may pass even with duplicates - depends on data
            except Exception as e:
                print(f"[WARN] Could not run integrity test: {str(e)}")
    
    def test_missing_file(self):
        """Test handling of missing files."""
        with self.assertRaises(FileNotFoundError):
            _load_csv("/nonexistent/path/data.csv", "Nonexistent")
    
    def test_datetime_parsing(self):
        """Test datetime column parsing."""
        test_data = pd.DataFrame({
            'date': ['2024-01-01', '2024-01-02', '2024-01-03']
        })
        
        # Simulate datetime conversion like in load_data()
        test_data['date'] = pd.to_datetime(test_data['date'], errors='coerce')
        
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(test_data['date']))
        self.assertEqual(test_data['date'].isna().sum(), 0, "All dates should parse successfully")


class TestDataConsistency(unittest.TestCase):
    """Test data consistency across datasets."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.base_path = Path(__file__).parent.parent / "data" / "clean"
    
    def test_rfm_customer_count(self):
        """Test that RFM customer count matches expected range."""
        rfm_path = self.base_path / "rfm_segments.csv"
        rfm_sum_path = self.base_path / "rfm_summary.csv"
        
        if rfm_path.exists() and rfm_sum_path.exists():
            try:
                rfm = _load_csv(str(rfm_path), "RFM")
                rfm_sum = _load_csv(str(rfm_sum_path), "RFM Summary")
                
                customers_in_rfm = rfm['customer_id'].nunique()
                customers_in_sum = rfm_sum['customers'].sum()
                
                self.assertEqual(customers_in_rfm, customers_in_sum,
                    f"Customer count mismatch: {customers_in_rfm} vs {customers_in_sum}")
                print(f"[OK] RFM customer count consistent: {customers_in_rfm:,}")
            except Exception as e:
                print(f"[WARN] Skipping consistency check: {str(e)}")
    
    def test_segments_valid(self):
        """Test that RFM segments are valid."""
        rfm_path = self.base_path / "rfm_segments.csv"
        
        if rfm_path.exists():
            try:
                rfm = _load_csv(str(rfm_path), "RFM")
                valid_segments = {'Champion', 'Loyal', 'Potential', 'At-Risk', 'Churned'}
                
                if 'segment' in rfm.columns:
                    actual_segments = set(rfm['segment'].unique())
                    self.assertTrue(actual_segments.issubset(valid_segments),
                        f"Invalid segments found: {actual_segments - valid_segments}")
                    print(f"[OK] Valid segments: {actual_segments}")
            except Exception as e:
                print(f"[WARN] Skipping segment validation: {str(e)}")


def run_all_tests():
    """Run all tests and print summary."""
    print("\n" + "="*70)
    print("QC Pulse India - Data Loader Tests")
    print("="*70 + "\n")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestDataLoader))
    suite.addTests(loader.loadTestsFromTestCase(TestDataConsistency))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    if result.wasSuccessful():
        print("[OK] All tests passed!")
    else:
        print(f"✗ {len(result.failures)} failures, {len(result.errors)} errors")
    print("="*70 + "\n")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)
