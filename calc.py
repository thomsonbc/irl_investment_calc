import numpy as np
import math

class InvestmentCalc:

    '''WORK IN PROGRESS'''

    def __init__(self, principal: int, years: int, growth_pc: int, frequency: str = 'monthly') -> None:
        self.dd_division_constants = {'monthly': 96, 'yearly': 8}
        self.principal = self._is_valid_principal(principal)
        self.years = self._is_valid_years(years)
        self.growth =  self._is_valid_growth(growth_pc)
        self.frequency = self._is_valid_frequency(frequency)
        self.periods = self._years_to_periods()
        self.dd_chunks = self._calculate_dd_chunks(self.periods)
        self.tax_rate = 0.41
        self.inv_calc_matrix = self.build_matrix(dd = True)
        self.inv_calc_summary = self.matrix_sum(matrix = self.inv_calc_matrix)
        self.untaxed_inv_calc_matrix = self.build_matrix(dd = False)
        self.untaxed_inv_calc_summary = self.matrix_sum(matrix = self.untaxed_inv_calc_matrix)
        self.tax_owed_matrix = self.build_tax_matrix()
        self.tax_owed_summary = self.matrix_sum(matrix = self.tax_owed_matrix)
        
    
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
    
    def _calculate_dd_chunks(self, periods: int) -> dict:
        dd_chunks = periods // self.dd_division_constants[self.frequency]
        remainder = periods % self.dd_division_constants[self.frequency]
        return {'dd_chunks':dd_chunks, 'remainder':remainder}
        
    def growth_formula(self) -> float:
        return 1+(self.growth/12)

    def dd_tax_deduct(self, value: float, principal: float) -> float:
        profit = value - principal
        net_profit = profit * (1 - self.tax_rate)
        return principal + net_profit
    
    def dd_tax_owed(self, value: float, principal:float) -> float:
        profit = value - principal
        return profit * self.tax_rate
    
    def get_growth_array(self, array: np.ndarray, new_principal: float) -> np.ndarray:
        return (self.growth_formula() ** array) * new_principal

    def calculate_untaxed_growth(self, periods: int) -> np.ndarray:
        '''Calculates investment growth without taxation as a comparison to deemed disposal growth 
        for a single investment'''
        
        master_array=self.get_growth_array(np.array(range(periods)), self.principal)
        final_value = self.dd_tax_deduct(master_array[-1], self.principal)
        return np.append(master_array, final_value)

    def calculate_growth(self, periods: int) -> np.ndarray:
        '''Returns an array recording an investment's growth and taxation for a given
        period of time.
        
        Runs in chunks of up to 8 years, then does the deemed disposal.
        
        Taxes final value and appends to end of array.'''

        new_principal = self.principal
        master_array = np.zeros(0, dtype=float)
        dd_chunks = self._calculate_dd_chunks(periods)
        
        for chunk in range(dd_chunks['dd_chunks']):
            growth_array = self.get_growth_array(np.array(range(96)), new_principal)

            master_array = np.append(master_array, growth_array)

            new_principal = self.dd_tax_deduct(growth_array[-1], new_principal)

        if dd_chunks['remainder'] > 0:
            growth_array = self.get_growth_array(np.array(range(dd_chunks['remainder'])), new_principal)

            master_array = np.append(master_array, growth_array)

            new_principal = self.dd_tax_deduct(growth_array[-1], new_principal)

        try:
            final_principal = growth_array[0]
            final_value = self.dd_tax_deduct(master_array[-1], final_principal)
            #print(f"Last new principal: {final_principal}. Final value of investment:{master_array[-1]} after {periods} months. Tax: {master_array[-1]-final_value}")
            master_array = np.append(master_array,final_value)
        except:
            print(f"periods at error: {periods}")

        return master_array
    
    def calculate_tax_owed(self, periods: int) -> np.ndarray:
        '''Returns an array recording investment tax burden per year
        Could likely be worked into self.calculate_growth()'''
        new_principal = self.principal
        master_tax_array = np.zeros(1, dtype=float)
        dd_chunks = self._calculate_dd_chunks(periods)

        for chunk in range(dd_chunks['dd_chunks']):
            growth_array = self.get_growth_array(np.array(range(96)), new_principal)
            
            tax_array = np.append(np.zeros(7, dtype=float), self.dd_tax_owed(growth_array[-1], new_principal))

            new_principal = self.dd_tax_deduct(growth_array[-1], new_principal)
            
            master_tax_array = np.append(master_tax_array, tax_array)
        
        if dd_chunks['remainder'] > 0:
            growth_array = self.get_growth_array(np.array(range(dd_chunks['remainder'])), new_principal)

            tax_array = np.append(np.zeros(self.round_up(periods)-1, dtype=float), self.dd_tax_owed(growth_array[-1], new_principal))

            new_principal = self.dd_tax_deduct(growth_array[-1], new_principal)
            
            master_tax_array = np.append(master_tax_array, tax_array)

    
        return master_tax_array


    def build_matrix(self, dd = True) -> np.ndarray:
        '''
        -Build a 2d array that tracks each month's investment growth and taxation
        for a given period of time.
        -use calculate_growth for each month's / year's investment, adjusting period var.
        -Add zeros as prefix for each month. month 1 = 1 zero, month 2 = 2 zeros, etc
        -Append to master_array
        -Reshape at end into 2D array. Each period's array must be same shape before appending!!
        '''
        master_array = np.zeros(0,dtype=float)

        for i in range(self.periods):
            zeros_array = np.zeros(i, dtype = float)
            if dd:
                growth_array = self.calculate_growth(periods = self.periods - i)
            else:
                growth_array = self.calculate_untaxed_growth(periods = self.periods - i)
            result_array = np.append(zeros_array, growth_array)
            master_array = np.append(master_array, result_array)

        
        return master_array.reshape(self.periods, self.periods+1)

    def build_tax_matrix(self) -> np.ndarray:
        '''
        Same as above but purpose is to calculate tax owed for each year
        '''
        init_array_length = self.calculate_tax_owed(periods = self.periods).shape[0]
        master_array = np.zeros(0,dtype=float)

        for i in range(self.periods+1):
            growth_array = self.calculate_tax_owed(periods = self.periods - i)
            zeros_to_add = init_array_length - growth_array.shape[0]
            zeros_array = np.zeros(zeros_to_add, dtype = float)
            result_array = np.append(zeros_array, growth_array)
            master_array = np.append(master_array,result_array)

        
        return master_array.reshape(self.periods+1, init_array_length)
    
    def matrix_sum(self, matrix: np.ndarray) -> np.ndarray:
        '''Returns col sum'''
        return np.around(np.sum(matrix, axis = 0), decimals = 2)
    
    def round_up(self, periods: int, decimals=0)  -> float:
        '''Function to round up remainder periods to next year when calculating tax burden'''
        multiplier = 10 ** decimals
        dd_chunks = self._calculate_dd_chunks(periods)
        x = math.ceil(dd_chunks['remainder']/12 * multiplier) / multiplier
        return int(x)


#Need to add functionality for yearly option etc
    

x=InvestmentCalc(years=24, growth_pc=10, principal=1000, frequency='monthly')




print(x.tax_owed_summary)



