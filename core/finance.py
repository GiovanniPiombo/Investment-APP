class Finance():
    """Class to handle financial calculations for investments"""
    def __init__(self, investment = None):
        if investment != None:
            self.investment = investment
        self.set_frequency()
        self.calculate()

    def set_frequency(self):
        """Set the compound and contribution frequencies based on the investment data"""
        match self.investment["compound_frequency"]:
            case "Monthly":
                self.compound = 12
            case "Quarterly":
                self.compound = 4
            case "Semiannually":
                self.compound = 2
            case "Annually":
                self.compound = 1
        
        match self.investment["contribution_frequency"]:
            case "Monthly":
                self.contribution = 12
            case "Quarterly":
                self.contribution = 4
            case "Semiannually":
                self.contribution = 2
            case "Annually":
                self.contribution = 1
    
    def calculate(self):
        """
        Calculates the future value of an investment based on compound interest and regular contributions.

        This method computes:
        - The total amount invested over time.
        - The final capital at the end of the investment period.
        - The profit earned from the investment (final capital minus total invested).

        The calculation considers:
        - Initial deposit ("P")
        - Annual interest rate ("r")
        - Compounding frequency ("n")
        - Contribution frequency ("m")
        - Contribution amount ("PMT")
        - Investment duration in years ("t")

        If the interest rate is zero, the final capital is simply the sum of the initial deposit and total contributions.
        Otherwise, it uses compound interest formulas to compute both the growth of the initial deposit and the value
        of regular contributions over time.

        Updates the `self.investment` dictionary with:
        - "final_capital": the calculated value at the end of the investment
        - "profit": the earnings over the total invested amount
        - "invested": the total amount contributed including the initial deposit
        """
        r = self.investment["rate"]/100
        n = self.compound
        m = self.contribution
        t = self.investment["years"]
        P = self.investment["initial_deposit"]
        PMT = self.investment["contribution_amount"]
        
        invested = P + PMT * m * t

        if r == 0:
            final_capital = P + PMT * m * t
        else:
            initial_capital_results = P * (1 + r/n)**(n*t)
            effective_rate_per_contribution = (1 + r/n)**(n/m) - 1
            contribution_results = PMT * ((1 + effective_rate_per_contribution)**(m*t) - 1) / effective_rate_per_contribution
            
            final_capital = initial_capital_results + contribution_results

        self.investment.update({
            "final_capital" : final_capital,
            "profit" : final_capital - invested,
            "invested" : invested
        })
    
    def get_results(self):
        """Return the investment results"""
        return self.investment
    
    def get_annual_breakdown(self):
        """
        Generates a year-by-year breakdown of the investment's growth over time.

        This method calculates the total capital at the end of each year throughout the investment duration,
        taking into account compound interest and periodic contributions.

        Calculation details:
        - If the interest rate is zero, growth is linear based on contributions.
        - Otherwise, the method computes:
        - Growth of the initial deposit using compound interest.
        - Growth from periodic contributions using an effective rate per contribution period.

        Returns:
            tuple:
                - years (list of int): A list of years from 0 up to the investment duration.
                - capital (list of float): A list of corresponding capital values at the end of each year.
        """
        r = self.investment["rate"] / 100
        n = self.compound
        m = self.contribution
        t = self.investment["years"]
        P = self.investment["initial_deposit"]
        PMT = self.investment["contribution_amount"]

        years = list(range(int(t) + 1))
        capital = []

        for year in years:
            if r == 0:
                total = P + PMT * m * year
            else:
                initial = P * (1 + r/n)**(n*year)
                
                effective_rate_per_contribution = (1 + r/n)**(n/m) - 1
                contribution = PMT * ((1 + effective_rate_per_contribution)**(m*year) - 1) / effective_rate_per_contribution
                
                total = initial + contribution

            capital.append(total)

        return years, capital
