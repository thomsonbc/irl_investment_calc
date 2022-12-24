import numpy as np

class InvestmentCalc:

    def __init__(self, principal: int, years: int, growth_pc: int, frequency: str = 'monthly') -> None:
        
        self.dd_division_constants = {'monthly': 96, 'yearly': 8}
        self.principal = self._is_valid_principal(principal)
        self.years = self._is_valid_years(years)
        self.growth =  self._is_valid_growth(growth_pc)
        self.frequency = self._is_valid_frequency(frequency)
        self.periods = self._years_to_periods()
        self.dd_chunks = self._calculate_dd_chunks()
        self.tax_rate = 0.41
        
    
    def _is_valid_principal(self, principal) -> int:
        if principal < 0:
            raise ValueError("principal needs to be greater than zero")
        return principal
    
    def _is_valid_years(self, years) -> int:
        if years < 0:
            raise ValueError("years needs to be greater than zero")
        return years

    def _is_valid_growth(self, growth_pc) -> float:
        if growth_pc < 0:
            raise ValueError('growth needs to be type int greater than zero')
        return growth_pc/100

    def _is_valid_frequency(self, frequency) -> str:
        if frequency.lower() not in self.dd_division_constants.keys():
            raise ValueError(f"frequency not recognised. Choose from {self.dd_division_constants.keys()}. Not case sensitive.")
        return frequency.lower()
    
    def _years_to_periods(self) -> int:
        freq_dict = {'monthly':12, 'yearly':1}
        return self.years * freq_dict[self.frequency]
    
    def _calculate_dd_chunks(self):
        dd_chunks = self.periods // self.dd_division_constants[self.frequency]
        remainder = self.periods % self.dd_division_constants[self.frequency]
        return {'dd_chunks':dd_chunks, 'remainder':remainder}
        
    def growth_formula(self) -> float:

        return 1+(self.growth/12)

    def dd_tax(self, value, principal):
        profit = value - principal
        net_profit = profit * (1 - self.tax_rate)
        return principal + net_profit
    
    def calculate_growth(self):
        '''Returns an array recording an investment's growth and taxation for a given
        period of time.
        
        Runs in chunks of up to 8 years, then does the deemed disposal.
        
        Taxes final value.'''

        
        growth_array = np.array(range(1, self.periods + 1), dtype = float)  

        new_principal = self.principal

        master_array = np.array(self.principal, dtype=float)

        for chunk in range(self.dd_chunks['dd_chunks']):
            growth_array = (self.growth_formula() ** np.array(range(1,97))) * new_principal
            
            new_principal = self.dd_tax(growth_array[-1], new_principal)
            
            master_array = np.append(master_array, growth_array)

        if self.dd_chunks['remainder'] > 0:
            growth_array = (self.growth_formula() ** np.array(range(1, self.dd_chunks['remainder']+1))) * new_principal
            
            new_principal = self.dd_tax(growth_array[-1], new_principal)
            
            master_array = np.append(master_array, growth_array)
            
            final_value = self.dd_tax(growth_array[-1], new_principal)
            
            master_array[-1] = final_value

        return master_array

    def build_matrix(self):
        '''Build a matrix that tracks each month's investment growth and taxation
        for a given period of time'''
    
    

x=InvestmentCalc(years=33, growth_pc=10, principal=1000, frequency='monthly')


print(f"Interest compounds {x.frequency}")
print(x.periods)
print(x.dd_chunks)
print(x.calculate_growth())
