"""
test_main.py
Placeholder test - confirms the scaffold's health check runs without error.
Replace/expand this in Month 6 with real tests for your actual capstone logic.

Run: python -m pytest tests/ (from the capstone_scaffold/ directory)
     or just: python tests/test_main.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from main import health_check


def test_health_check_runs():
    result = health_check()
    assert result["python_version_ok"] is True
    assert result["data_dir_exists"] is True
    print("test_health_check_runs: PASS")


if __name__ == "__main__":
    test_health_check_runs()
