# Income Module for Docassemble

Includes examples at docassemble.income:interview_test.yml, docassemble.income:financial_statement.yml

## Classes

### Income(PeriodicValue)
```
    def amount(self, period_to_use=1):
        """Returns the amount earned over the specified period """
```
### IncomeList(DAList)
```
    def types(self):
        """Returns a set of the unique types of values stored in the list. Will fail if any items in the list leave the type field unspecified"""

    def owners(self, type=None):
        """Returns a set of the unique owners for the specified type of value stored in the list. If type is None, returns all unique owners in the IncomeList"""

    def total(self, period_to_use=1, type=None):
        """Returns the total periodic value in the list, gathering the list items if necessary.
    
    def market_value_total(self, type=None):
        """Returns the total market value of values in the list."""

    def balance_total(self, type=None):
    
    def matches(self, type):
        """Returns an IncomeList consisting only of elements matching the specified Income type, assisting in filling PDFs with predefined spaces"""
```

### Job(Income)
```
    def net_amount(self, period_to_use=1):
        """Returns the net amount (e.g., minus deductions). Only applies if value is non-hourly."""

    def gross_amount(self, period_to_use=1):
        """Gross amount is identical to value"""
```
### JobList
```
    def gross_total(self, period_to_use=1, type=None):

    def net_total(self, period_to_use=1, type=None):
 
```

### SimpleValue

```
    def amount(self):

```

### Vehicle
Like SimpleValue, but adds year_make_model method

### ValueList
```
    def types(self):
        """Returns a set of the unique types of values stored in the list. Will fail if any items in the list leave the type field unspecified"""

    def total(self, type=None):
```

### VehicleList

### Asset

Like Income, but the value field is optional

### AssetList
list of Assets

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

def non_wage_income_list():
    """Returns a list of income types for a multiple choice dropdown, excluding wages"""

expense_type_list() :
    """Returns a list of expense types for a multiple choice dropdown"""
    
def flatten(listname,index=1):
    """Return just the nth item in an 2D list. Intended to use for multiple choice option lists in Docassemble.
        e.g., flatten(asset_type_list()) will return ['Savings','Certificate of Deposit'...] """

def income_period(frequency):
  """Returns the plain language translation of the income period, which is a number"""

```