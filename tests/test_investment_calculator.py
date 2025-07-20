import pytest
from typing import Dict, Any, List
from core.investment_calculator import InvestmentData, InvestmentCalculator

class TestInvestmentData:
    """Test cases for InvestmentData dataclass"""
    
    def test_valid_investment_data(self):
        """Test creating valid investment data"""
        investment = InvestmentData(
            initial_deposit=1000.0,
            contribution_amount=100.0,
            rate=0.07,
            ticker="SPY"
        )
        assert investment.initial_deposit == 1000.0
        assert investment.contribution_amount == 100.0
        assert investment.rate == 0.07
        assert investment.ticker == "SPY"
    
    def test_default_ticker(self):
        """Test default ticker value"""
        investment = InvestmentData(
            initial_deposit=1000.0,
            contribution_amount=100.0,
            rate=0.07
        )
        assert investment.ticker == ""
    
    def test_negative_initial_deposit(self):
        """Test validation for negative initial deposit"""
        with pytest.raises(ValueError, match="Initial deposit cannot be negative"):
            InvestmentData(
                initial_deposit=-1000.0,
                contribution_amount=100.0,
                rate=0.07
            )
    
    def test_negative_contribution_amount(self):
        """Test validation for negative contribution amount"""
        with pytest.raises(ValueError, match="Contribution amount cannot be negative"):
            InvestmentData(
                initial_deposit=1000.0,
                contribution_amount=-100.0,
                rate=0.07
            )
    
    def test_negative_rate(self):
        """Test validation for negative rate"""
        with pytest.raises(ValueError, match="Rate cannot be negative"):
            InvestmentData(
                initial_deposit=1000.0,
                contribution_amount=100.0,
                rate=-0.05
            )
    
    def test_zero_values_allowed(self):
        """Test that zero values are allowed"""
        investment = InvestmentData(
            initial_deposit=0.0,
            contribution_amount=0.0,
            rate=0.0
        )
        assert investment.initial_deposit == 0.0
        assert investment.contribution_amount == 0.0
        assert investment.rate == 0.0


class TestInvestmentCalculator:
    """Test cases for InvestmentCalculator class"""
    
    def setup_method(self):
        """Setup method run before each test"""
        self.calculator = InvestmentCalculator()
    
    def test_get_frequency_multiplier_valid(self):
        """Test frequency multiplier for valid frequencies"""
        assert self.calculator.get_frequency_multiplier("Monthly") == 12
        assert self.calculator.get_frequency_multiplier("Quarterly") == 4
        assert self.calculator.get_frequency_multiplier("Semiannually") == 2
        assert self.calculator.get_frequency_multiplier("Annually") == 1
    
    def test_get_frequency_multiplier_invalid(self):
        """Test frequency multiplier for invalid frequency"""
        with pytest.raises(ValueError, match="Invalid frequency: Weekly"):
            self.calculator.get_frequency_multiplier("Weekly")
    
    def test_validate_years_valid(self):
        """Test years validation with valid inputs"""
        assert self.calculator.validate_years("5") == 5.0
        assert self.calculator.validate_years("10.5") == 10.5
        assert self.calculator.validate_years("  1  ") == 1.0  # Test trimming
    
    def test_validate_years_zero_or_negative(self):
        """Test years validation with zero or negative values"""
        with pytest.raises(ValueError, match="Years must be a positive number"):
            self.calculator.validate_years("0")
        
        with pytest.raises(ValueError, match="Years must be a positive number"):
            self.calculator.validate_years("-5")
    
    def test_validate_years_invalid_string(self):
        """Test years validation with invalid string"""
        with pytest.raises(ValueError, match="Please enter a valid number for years"):
            self.calculator.validate_years("not_a_number")
    
    def test_parse_investment_data_valid(self):
        """Test parsing valid investment data"""
        raw_data = {
            "initial_deposit": "1000",
            "contribution_amount": "100",
            "rate": "0.07",
            "ticker": "SPY"
        }
        investment = self.calculator.parse_investment_data(raw_data)
        
        assert investment.initial_deposit == 1000.0
        assert investment.contribution_amount == 100.0
        assert investment.rate == 0.07
        assert investment.ticker == "SPY"
    
    def test_parse_investment_data_missing_ticker(self):
        """Test parsing investment data without ticker"""
        raw_data = {
            "initial_deposit": "1000",
            "contribution_amount": "100",
            "rate": "0.07"
        }
        investment = self.calculator.parse_investment_data(raw_data)
        assert investment.ticker == ""
    
    def test_parse_investment_data_invalid_values(self):
        """Test parsing investment data with invalid values"""
        raw_data = {
            "initial_deposit": "not_a_number",
            "contribution_amount": "100",
            "rate": "0.07"
        }
        with pytest.raises(ValueError, match="Invalid investment data"):
            self.calculator.parse_investment_data(raw_data)
    
    def test_parse_investment_data_missing_required_field(self):
        """Test parsing investment data with missing required field"""
        raw_data = {
            "initial_deposit": "1000",
            "contribution_amount": "100"
            # missing rate
        }
        with pytest.raises(ValueError, match="Invalid investment data"):
            self.calculator.parse_investment_data(raw_data)
    
    def test_calculate_investment_weight(self):
        """Test investment weight calculation"""
        investment = InvestmentData(
            initial_deposit=1000.0,
            contribution_amount=100.0,
            rate=0.07
        )
        
        # Monthly contributions for 5 years: 1000 + (100 * 12 * 5) = 1000 + 6000 = 7000
        weight = self.calculator.calculate_investment_weight(investment, "Monthly", 5.0)
        assert weight == 7000.0
        
        # Annually for 10 years: 1000 + (100 * 1 * 10) = 1000 + 1000 = 2000
        weight = self.calculator.calculate_investment_weight(investment, "Annually", 10.0)
        assert weight == 2000.0
    
    def test_calculate_weighted_average_rate_single_investment(self):
        """Test weighted average rate with single investment"""
        investments = [
            InvestmentData(initial_deposit=1000.0, contribution_amount=100.0, rate=0.07)
        ]
        
        avg_rate = self.calculator.calculate_weighted_average_rate(investments, "Monthly", 5.0)
        assert avg_rate == 0.07
    
    def test_calculate_weighted_average_rate_multiple_investments(self):
        """Test weighted average rate with multiple investments"""
        investments = [
            InvestmentData(initial_deposit=1000.0, contribution_amount=100.0, rate=0.07),  # Weight: 7000
            InvestmentData(initial_deposit=500.0, contribution_amount=50.0, rate=0.05)     # Weight: 3500
        ]
        
        # Expected weighted average: (0.07 * 7000 + 0.05 * 3500) / (7000 + 3500)
        # = (490 + 175) / 10500 = 665 / 10500 ≈ 0.063333
        avg_rate = self.calculator.calculate_weighted_average_rate(investments, "Monthly", 5.0)
        expected_rate = (0.07 * 7000 + 0.05 * 3500) / 10500
        assert abs(avg_rate - expected_rate) < 1e-10
    
    def test_calculate_weighted_average_rate_empty_list(self):
        """Test weighted average rate with empty investments list"""
        avg_rate = self.calculator.calculate_weighted_average_rate([], "Monthly", 5.0)
        assert avg_rate == 0.0
    
    def test_calculate_totals(self):
        """Test calculation of total initial deposits and contributions"""
        investments = [
            InvestmentData(initial_deposit=1000.0, contribution_amount=100.0, rate=0.07),
            InvestmentData(initial_deposit=500.0, contribution_amount=50.0, rate=0.05),
            InvestmentData(initial_deposit=2000.0, contribution_amount=200.0, rate=0.08)
        ]
        
        total_initial, total_contribution = self.calculator.calculate_totals(investments)
        assert total_initial == 3500.0  # 1000 + 500 + 2000
        assert total_contribution == 350.0  # 100 + 50 + 200
    
    def test_calculate_totals_empty_list(self):
        """Test totals calculation with empty list"""
        total_initial, total_contribution = self.calculator.calculate_totals([])
        assert total_initial == 0.0
        assert total_contribution == 0.0
    
    def test_process_investments_valid_single(self):
        """Test processing single valid investment"""
        raw_investments = [
            {
                "initial_deposit": "1000",
                "contribution_amount": "100",
                "rate": "0.07",
                "ticker": "SPY"
            }
        ]
        
        result = self.calculator.process_investments(
            raw_investments, "Monthly", "Monthly", 5.0
        )
        
        assert result["rate"] == 0.07
        assert result["initial_deposit"] == 1000.0
        assert result["contribution_amount"] == 100.0
        assert result["compound_frequency"] == "Monthly"
        assert result["contribution_frequency"] == "Monthly"
        assert result["years"] == 5.0
        assert result["is_empty"] is False
        assert result["investment_count"] == 1
    
    def test_process_investments_valid_multiple(self):
        """Test processing multiple valid investments"""
        raw_investments = [
            {
                "initial_deposit": "1000",
                "contribution_amount": "100",
                "rate": "0.07"
            },
            {
                "initial_deposit": "500",
                "contribution_amount": "50",
                "rate": "0.05"
            }
        ]
        
        result = self.calculator.process_investments(
            raw_investments, "Quarterly", "Monthly", 10.0
        )
        
        # Check aggregated values
        assert result["initial_deposit"] == 1500.0  # 1000 + 500
        assert result["contribution_amount"] == 150.0  # 100 + 50
        assert result["compound_frequency"] == "Quarterly"
        assert result["contribution_frequency"] == "Monthly"
        assert result["years"] == 10.0
        assert result["is_empty"] is False
        assert result["investment_count"] == 2
        
        # Check weighted average rate calculation
        # Investment 1 weight: 1000 + (100 * 12 * 10) = 13000
        # Investment 2 weight: 500 + (50 * 12 * 10) = 6500
        # Weighted average: (0.07 * 13000 + 0.05 * 6500) / 19500
        expected_rate = (0.07 * 13000 + 0.05 * 6500) / 19500
        assert abs(result["rate"] - expected_rate) < 1e-10
    
    def test_process_investments_empty_list(self):
        """Test processing empty investments list"""
        with pytest.raises(ValueError, match="At least one investment is required"):
            self.calculator.process_investments([], "Monthly", "Monthly", 5.0)
    
    def test_process_investments_invalid_data(self):
        """Test processing investments with invalid data"""
        raw_investments = [
            {
                "initial_deposit": "invalid",
                "contribution_amount": "100",
                "rate": "0.07"
            }
        ]
        
        with pytest.raises(ValueError, match="Invalid investment data"):
            self.calculator.process_investments(
                raw_investments, "Monthly", "Monthly", 5.0
            )
    
    def test_get_available_frequencies(self):
        """Test getting available frequency options"""
        frequencies = self.calculator.get_available_frequencies()
        expected = ["Monthly", "Quarterly", "Semiannually", "Annually"]
        
        assert len(frequencies) == 4
        for freq in expected:
            assert freq in frequencies


class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def setup_method(self):
        self.calculator = InvestmentCalculator()
    
    def test_zero_initial_deposit_with_contributions(self):
        """Test investment with zero initial deposit but positive contributions"""
        investment = InvestmentData(
            initial_deposit=0.0,
            contribution_amount=100.0,
            rate=0.07
        )
        
        weight = self.calculator.calculate_investment_weight(investment, "Monthly", 5.0)
        assert weight == 6000.0  # 0 + (100 * 12 * 5)
    
    def test_zero_contributions_with_initial_deposit(self):
        """Test investment with positive initial deposit but zero contributions"""
        investment = InvestmentData(
            initial_deposit=1000.0,
            contribution_amount=0.0,
            rate=0.07
        )
        
        weight = self.calculator.calculate_investment_weight(investment, "Monthly", 5.0)
        assert weight == 1000.0  # 1000 + (0 * 12 * 5)
    
    def test_zero_rate_investment(self):
        """Test investment with zero interest rate"""
        investments = [
            InvestmentData(initial_deposit=1000.0, contribution_amount=100.0, rate=0.0)
        ]
        
        avg_rate = self.calculator.calculate_weighted_average_rate(investments, "Monthly", 5.0)
        assert avg_rate == 0.0
    
    def test_very_small_numbers(self):
        """Test with very small numbers"""
        investment = InvestmentData(
            initial_deposit=0.01,
            contribution_amount=0.01,
            rate=0.001
        )
        
        weight = self.calculator.calculate_investment_weight(investment, "Monthly", 1.0)
        expected_weight = 0.01 + (0.01 * 12 * 1.0)
        assert abs(weight - expected_weight) < 1e-10
    
    def test_large_numbers(self):
        """Test with large numbers"""
        investment = InvestmentData(
            initial_deposit=1000000.0,
            contribution_amount=10000.0,
            rate=0.15
        )
        
        weight = self.calculator.calculate_investment_weight(investment, "Monthly", 30.0)
        expected_weight = 1000000.0 + (10000.0 * 12 * 30.0)
        assert weight == expected_weight


class TestIntegration:
    """Integration tests combining multiple components"""
    
    def setup_method(self):
        self.calculator = InvestmentCalculator()
    
    def test_full_workflow_realistic_scenario(self):
        """Test complete workflow with realistic investment scenario"""
        # Portfolio with stocks, bonds, and REITs
        raw_investments = [
            {
                "initial_deposit": "10000",
                "contribution_amount": "500",
                "rate": "0.10",
                "ticker": "VTI"  # Total Stock Market
            },
            {
                "initial_deposit": "5000",
                "contribution_amount": "200",
                "rate": "0.04",
                "ticker": "BND"  # Total Bond Market
            },
            {
                "initial_deposit": "2000",
                "contribution_amount": "100",
                "rate": "0.08",
                "ticker": "VNQ"  # REITs
            }
        ]
        
        result = self.calculator.process_investments(
            raw_investments, "Monthly", "Monthly", 20.0
        )
        
        # Verify all components
        assert result["initial_deposit"] == 17000.0  # 10000 + 5000 + 2000
        assert result["contribution_amount"] == 800.0  # 500 + 200 + 100
        assert result["investment_count"] == 3
        assert result["years"] == 20.0
        assert result["is_empty"] is False
        
        # Calculate expected weighted average manually
        # VTI weight: 10000 + (500 * 12 * 20) = 10000 + 120000 = 130000
        # BND weight: 5000 + (200 * 12 * 20) = 5000 + 48000 = 53000
        # VNQ weight: 2000 + (100 * 12 * 20) = 2000 + 24000 = 26000
        # Total weight: 209000
        # Weighted rate: (0.10 * 130000 + 0.04 * 53000 + 0.08 * 26000) / 209000
        expected_rate = (0.10 * 130000 + 0.04 * 53000 + 0.08 * 26000) / 209000
        assert abs(result["rate"] - expected_rate) < 1e-10


# Parametrized tests for comprehensive frequency testing
class TestParametrized:
    """Parametrized tests for comprehensive coverage"""
    
    @pytest.mark.parametrize("frequency,expected_multiplier", [
        ("Monthly", 12),
        ("Quarterly", 4),
        ("Semiannually", 2),
        ("Annually", 1)
    ])
    def test_all_frequency_multipliers(self, frequency, expected_multiplier):
        """Test all frequency multipliers"""
        calculator = InvestmentCalculator()
        assert calculator.get_frequency_multiplier(frequency) == expected_multiplier
    
    @pytest.mark.parametrize("years_input,expected_result", [
        ("1", 1.0),
        ("5.5", 5.5),
        ("10", 10.0),
        ("0.5", 0.5),
        ("  2.5  ", 2.5)  # Test with whitespace
    ])
    def test_valid_years_inputs(self, years_input, expected_result):
        """Test various valid years inputs"""
        calculator = InvestmentCalculator()
        assert calculator.validate_years(years_input) == expected_result
    
    @pytest.mark.parametrize("invalid_years", [
        "0",
        "-1",
        "-5.5",
        "not_a_number",
        "",
        "1.2.3"
    ])
    def test_invalid_years_inputs(self, invalid_years):
        """Test various invalid years inputs"""
        calculator = InvestmentCalculator()
        with pytest.raises(ValueError):
            calculator.validate_years(invalid_years)