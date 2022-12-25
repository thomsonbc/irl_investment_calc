# irl_investment_calc
An investment calculator that considers elements of Irish tax law for ETF investments

## Rationale for calculator

When ETF shares are bought in Ireland, the investor is liable to pay a tax of 41% on profits from the sale of the shares. If the investor has not disposed of the shares by the 8th anniversary of their purchase then the shares are deemed to be disposed. In other words, after 8 years of ownership of any ETF shares, you owe a tax on the profits of those shares even if you have not sold them. 

If a person chose to make regular investments into an ETF for an extended period of time, then trying to estimate returns and keeping track of each purchases's tax burden becomes complicated. 

This calculator tracks individual investments' growth over the specified number of years, and subtracts the tax owed at the appropriate time, to return a matrix containing each investment's growth and eventual final value. The matrix can then be summed to view the overall value of all investments made over time.

The calculator also returns a similar matrix describing the yearly tax burden that comes with regular ETF investments.

### Assumptions
 - Annual growth and investment amount remain constant (wishful thinking)
 - When an investment's deemed disposal occurs, the shares bough for that investment are entirely disposed and the post-tax value is immediately re-invested
 - No annual charges or management fees are taken into account
 - When disposing of an investment, the spread is not taken into account

## Features
- Calculates the growth of a constant period investment for a specified number of years
    - Takes Ireland's 'deemed disposal' rule into account, i.e. 41% tax on profits 8 years after investment. The 
    - Calculates yearly tax burden 
