import sys
import os

# Ensure core directory is in Python path
# This file is automatically loaded by pytest and ensures imports work
# regardless of how pytest is invoked

def pytest_configure(config):
    """Configure pytest to add core directory to Python path"""
    core_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if core_dir not in sys.path:
        sys.path.insert(0, core_dir)