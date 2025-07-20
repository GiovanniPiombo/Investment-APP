from typing import List, Dict, Any, Tuple
from dataclasses import dataclass

@dataclass
class InvestmentData:
    """Data class to represent a single investment"""
    initial_deposit: float
    contribution_amount: float
    rate: float
    ticker: str = ""
    
    def __post_init__(self):
        """Validate investment data after initialization"""
        if self.initial_deposit < 0:
            raise ValueError("Initial deposit cannot be negative")
        if self.contribution_amount < 0:
            raise ValueError("Contribution amount cannot be negative")
        if self.rate < 0:
            raise ValueError("Rate cannot be negative")

class InvestmentCalculator:
    """Handles all investment-related calculations"""
    
    # Frequency mappings
    FREQUENCY_MAP = {
        "Monthly": 12,
        "Quarterly": 4,
        "Semiannually": 2,
        "Annually": 1
    }
    
    def __init__(self):
        pass
    
    @staticmethod
    def get_frequency_multiplier(frequency: str) -> int:
        """Convert frequency string to multiplier"""
        if frequency not in InvestmentCalculator.FREQUENCY_MAP:
            raise ValueError(f"Invalid frequency: {frequency}")
        return InvestmentCalculator.FREQUENCY_MAP[frequency]
    
    @staticmethod
    def validate_years(years_str: str) -> float:
        """Validate and convert years input"""
        try:
            years = float(years_str.strip())
            if years <= 0:
                raise ValueError("Years must be a positive number")
            return years
        except ValueError as e:
            if "could not convert" in str(e):
                raise ValueError("Please enter a valid number for years")
            raise
    
    @staticmethod
    def parse_investment_data(raw_data: Dict[str, Any]) -> InvestmentData:
        """Parse and validate raw investment data"""
        try:
            return InvestmentData(
                initial_deposit=float(raw_data["initial_deposit"]),
                contribution_amount=float(raw_data["contribution_amount"]),
                rate=float(raw_data["rate"]),
                ticker=raw_data.get("ticker", "")
            )
        except (ValueError, KeyError) as e:
            raise ValueError(f"Invalid investment data: {str(e)}")
    
    def calculate_investment_weight(self, investment: InvestmentData, 
                                 contribution_frequency: str, years: float) -> float:
        """Calculate the weight of an investment for weighted average calculations"""
        freq_multiplier = self.get_frequency_multiplier(contribution_frequency)
        return investment.initial_deposit + (investment.contribution_amount * freq_multiplier * years)
    
    def calculate_weighted_average_rate(self, investments: List[InvestmentData],
                                      contribution_frequency: str, years: float) -> float:
        """Calculate the weighted average rate across all investments"""
        if not investments:
            return 0.0
            
        weighted_rate_sum = 0.0
        total_weight = 0.0
        
        for investment in investments:
            weight = self.calculate_investment_weight(investment, contribution_frequency, years)
            weighted_rate_sum += investment.rate * weight
            total_weight += weight
        
        return weighted_rate_sum / total_weight if total_weight > 0 else 0.0
    
    def calculate_totals(self, investments: List[InvestmentData]) -> Tuple[float, float]:
        """Calculate total initial deposits and total contributions"""
        total_initial = sum(inv.initial_deposit for inv in investments)
        total_contribution = sum(inv.contribution_amount for inv in investments)
        return total_initial, total_contribution
    
    def process_investments(self, raw_investments: List[Dict[str, Any]], 
                          compound_frequency: str, contribution_frequency: str, 
                          years: float) -> Dict[str, Any]:
        """
        Process a list of raw investment data and return aggregated results
        
        Args:
            raw_investments: List of raw investment dictionaries
            compound_frequency: How often interest compounds
            contribution_frequency: How often contributions are made
            years: Investment time horizon
            
        Returns:
            Dictionary with aggregated investment data
            
        Raises:
            ValueError: If any validation fails
        """
        if not raw_investments:
            raise ValueError("At least one investment is required")
        
        # Parse and validate all investments
        investments = []
        for raw_inv in raw_investments:
            investments.append(self.parse_investment_data(raw_inv))
        
        # Calculate totals
        total_initial, total_contribution = self.calculate_totals(investments)
        
        # Calculate weighted average rate
        weighted_avg_rate = self.calculate_weighted_average_rate(
            investments, contribution_frequency, years
        )

        return {
            "rate": weighted_avg_rate,
            "initial_deposit": total_initial,
            "contribution_amount": total_contribution,
            "compound_frequency": compound_frequency,
            "contribution_frequency": contribution_frequency,
            "years": years,
            "is_empty": False,
            "investment_count": len(investments)
        }
    
    @staticmethod
    def get_available_frequencies() -> List[str]:
        """Get list of available frequency options"""
        return list(InvestmentCalculator.FREQUENCY_MAP.keys())