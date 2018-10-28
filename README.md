# Income Module for Docassemble

Includes examples at docassemble.income:interview_test.yml

## Classes

### Income

### IncomeList

### Job

### JobList

### SimpleValue

### ValueList

## Utility functions

```
recent_years(years=15, order='descending',future=1):
    """Returns a list of the most recent years, continuing into the future. Defaults to most recent 15 years+1. Useful to populate
        a combobox of years where the most recent ones are most likely. E.g. automobile years or birthdate.
        Keyword paramaters: years, order (descending or ascending), future (defaults to 1)"""
        
asset_type_list() :
    """Returns a list of assset types for a multiple choice dropdown"""
    
income_type_list() :
    """Returns a list of income types for a multiple choice dropdown"""

expense_type_list() :
    """Returns a list of expense types for a multiple choice dropdown"""
    
def flatten(listname,index=1):
    """Return just the nth item in an 2D list. Intended to use for multiple choice option lists in Docassemble.
        e.g., flatten(asset_type_list()) will return ['Savings','Certificate of Deposit'...] """

def non_wage_income_list():
```