class Finance():
    def __init__(self, investment = None):
        if investment != None:
            self.investment = investment
        self.set_frequency()
        self.calculate()

    def set_frequency(self):
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
        r = self.investment["rate"]/100
        n = self.compound
        m = self.contribution
        t = self.investment["years"]
        P = self.investment["initial_deposit"]
        PMT = self.investment["contribution_amount"]
        invested = PMT * self.contribution + P

        if r == 0:
            initial_capital_results = P
            contribution_results = PMT * m * t
        else:
            initial_capital_results = P * ((1 + r/n) ** (n * t))
            contribution_results = PMT * (((1 + r/n) ** (n * t) - 1) / (r/n)) * (n/m)

        final_capital = initial_capital_results + contribution_results
        self.investment.update({
            "final_capital" : final_capital,
            "profit" : final_capital - invested,
            "invested" : invested
        })
    
    def get_results(self):
        return self.investment