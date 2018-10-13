from docassemble.base.core import DAObject, DAList, DADict
from docassemble.base.util import Value, PeriodicValue, FinancialList, PeriodicFinancialList
from decimal import Decimal

def asset_type_list() :
    """Returns a list of assset types for a multiple choice dropdown"""
    return [
        'Savings',
        'Certificate of Deposit',
        'Individual Retirement Account',
        'Money or Mutual Fund',
        'Stocks or Bonds',
        'Trust Fund',
        'Checking Account',
        'Vehicle',
        'Real Estate',
        'Other Asset'
    ]

def income_type_list() :
    """Returns a list of income types for a multiple choice dropdown"""
    return [
        'Wages',
        'Social Security Benefits',
        'Supplemental Security Income (SSI)',
        'Pension',
        'TAFDC',
        'EAEDC',
        'Food Stamps (TANF)',
        'Income from real estate (rent, etc)',
        'Room and/or Board Payments',
        'Child Support',
        'Alimony',
        'Other Support'
    ]

def expenses_type_list() :
    """Returns a list of expense types for a multiple choice dropdown"""
    return [
        'Rent',
        'Mortgage',
        'Food',
        'Utilities',
        'Other Heating/Cooking Fuel',
        'Clothing',
        'Credit Card Payments',
        'Property Tax (State and Local)',
        'Other taxes and fees related to your home',
        'Insurance',
        'Medical-Dental (after amount paid by insurance)',
        'Car operation and maintenance',
        'Other transportation',
        'Church or charitable donations',
        'Loan, credit, or lay-away payments',
        'Support to someone not in household',
        'Other'
    ]

class HourlyOrPeriodicValue(PeriodicValue):
    """Represents a job which may have an hourly rate or a salary.
        Hourly rate jobs must include hours and period. 
        Period is some demoninator of a year for compatibility with
        PeriodicFinancialList class. E.g, to express hours/week, use 52"""
    is_hourly = True
    # hourly_rate = 0
    # hours_per_period = 0
    # period=52
    # value = 0
    @property
    def value(self):
        return self.amount()
    
    @value.setter
    def value(self, value):
        self._value = value

    def amount(self, period_to_use=1):
        """Returns the amount earned over the specified period"""
        #if not self.exists:
        #    return 0
        if self.is_hourly:
            return Decimal(self.hourly_rate * self.hours_per_period * self.period) / Decimal(period_to_use)        
        return (Decimal(self._value) * Decimal(self.period)) / Decimal(period_to_use)

class HourlyOrPeriodicFinancialList(DAList):
    """Represents a set of income items, each of which has an associated period or hourly wages."""
    def init(self, *pargs, **kwargs):
        self.elements = list()
        self.object_type = HourlyOrPeriodicValue
        return super(HourlyOrPeriodicFinancialList, self).init(*pargs, **kwargs)
    def total(self, period_to_use=1):
        """Returns the total periodic value in the list, gathering the list items if necessary."""
        self._trigger_gather()
        result = 0
        if period_to_use == 0:
            return(result)
        for item in self.elements:
            #if self.elements[item].exists:
            result += Decimal(item.amount(period_to_use=period_to_use))
        return result 