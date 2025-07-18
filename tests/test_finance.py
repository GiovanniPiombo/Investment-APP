import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from math import isclose
from core.finance import Finance

@pytest.fixture
def sample_investment():
    return {
        "initial_deposit": 1000,
        "rate": 5,
        "compound_frequency": "Monthly",
        "contribution_frequency": "Monthly",
        "contribution_amount": 100,
        "years": 3
    }

def test_calculate_with_interest(sample_investment):
    f = Finance(sample_investment.copy())
    results = f.get_results()
    
    # Checks
    assert "final_capital" in results
    assert "profit" in results
    assert "invested" in results
    
    expected_invested = 1000 + 100 * 12 * 3
    assert results["invested"] == expected_invested
    assert results["final_capital"] > expected_invested
    assert isclose(results["profit"], results["final_capital"] - results["invested"], rel_tol=1e-2)

def test_calculate_without_interest(sample_investment):
    investment = sample_investment.copy()
    investment["rate"] = 0
    f = Finance(investment)
    results = f.get_results()

    expected_final = 1000 + 100 * 12 * 3
    assert results["final_capital"] == expected_final
    assert results["profit"] == 0
    assert results["invested"] == expected_final

def test_get_annual_breakdown(sample_investment):
    f = Finance(sample_investment.copy())
    years, capital = f.get_annual_breakdown()

    assert len(years) == sample_investment["years"] + 1
    assert len(capital) == len(years)

    # Check that capital is strictly increasing
    for i in range(1, len(capital)):
        assert capital[i] > capital[i-1]

def test_frequency_settings():
    frequencies = {
        "Monthly": 12,
        "Quarterly": 4,
        "Semiannually": 2,
        "Annually": 1
    }

    for compound, expected_n in frequencies.items():
        for contribution, expected_m in frequencies.items():
            inv = {
                "initial_deposit": 1000,
                "rate": 5,
                "compound_frequency": compound,
                "contribution_frequency": contribution,
                "contribution_amount": 100,
                "years": 1
            }
            f = Finance(inv)
            assert f.compound == expected_n
            assert f.contribution == expected_m

def test_zero_contribution():
    inv = {
        "initial_deposit": 1000,
        "rate": 5,
        "compound_frequency": "Annually",
        "contribution_frequency": "Annually",
        "contribution_amount": 0,
        "years": 2
    }
    f = Finance(inv)
    results = f.get_results()

    # Final capital should be just compound interest on initial deposit
    expected = 1000 * (1 + 0.05)**2
    assert isclose(results["final_capital"], expected, rel_tol=1e-4)
    assert isclose(results["invested"], 1000)
    assert isclose(results["profit"], expected - 1000, rel_tol=1e-4)
