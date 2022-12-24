import numpy as np

class InvestmentCalc:

    def __init__(self, principal: int, years: int, growth: int, frequency: str = 'monthly') -> None:
        
        self.dd_division_constants = {'monthly': 96, 'yearly': 8}
        self.principal = self._is_valid_principal(principal)
        self.years = self._is_valid_years(years)
        self.growth =  self._is_valid_growth(growth)
        self.frequency = self._is_valid_frequency(frequency)
        self.periods = self._years_to_periods()
        self.dd_chunks = self._calculate_dd_chunks()
        
    
    def _is_valid_principal(self, principal) -> int:
        if principal < 0:
            raise ValueError("principal needs to be greater than zero")
        return principal
    
    def _is_valid_years(self, years) -> int:
        if years < 0:
            raise ValueError("years needs to be greater than zero")
        return years

    def _is_valid_growth(self, growth) -> float:
        if growth < 0:
            raise ValueError('growth needs to be type int greater than zero')
        return growth/100

    def _is_valid_frequency(self, frequency) -> str:
        if frequency.lower() not in self.dd_division_constants.keys():
            raise ValueError("frequency not recognised")
        return frequency
    
    def _years_to_periods(self) -> int:
        freq_dict = {'monthly':12, 'yearly':1}
        return self.years * freq_dict[self.frequency]
    
    def _calculate_dd_chunks(self):
        dd_chunks = self.periods // self.dd_division_constants[self.frequency]
        remainder = self.periods % self.dd_division_constants[self.frequency]
        return {'dd_chunks':dd_chunks, 'remainder':remainder}
        
    def growth_formula(self) -> float:

        return 1+(self.growth/12)
    
    def calculate_growth(self):
        '''Returns an array recording an investment's growth and taxation for a given
        period of time.
        
        Run this in chunks of up to 8 years, then do the deemed disposal'''

        inv_array = np.full(self.periods, self.principal, dtype=float)
        growth_array = np.array(range(1, self.periods + 1), dtype = float) 

        x = self.growth_formula() ** growth_array 
        return x * self.principal

    def build_matrix(self):
        '''Build a matrix that tracks each month's investment growth and taxation
        for a given period of time'''
    
    


        


x=InvestmentCalc(years=9, growth=10, principal=1000, frequency='monthly')


print(x.frequency)
print(x.periods)
print(x.calculate_growth())
print(x.periods_after_dd())
print(x.dd_chunks)