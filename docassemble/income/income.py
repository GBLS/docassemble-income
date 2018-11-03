from docassemble.base.core import DAObject, DAList, DADict
from docassemble.base.util import Value, PeriodicValue, FinancialList, PeriodicFinancialList
from decimal import Decimal
import datetime
import docassemble.base.functions

def flatten(listname,index=1):
    """Return just the nth item in an 2D list. Intended to use for multiple choice option lists in Docassemble.
        e.g., flatten(asset_type_list()) will return ['Savings','Certificate of Deposit'...] """
    return [item[index] for item in listname]

def income_period_list():
    return [
        [12,"Monthly"],
        [1,"Yearly"],
        [52,"Weekly"],
        [24,"Twice per month"],
        [26,"Once every two weeks"],
        [4,"Once every 3 months"]
    ]

docassemble.base.functions.update_language_function('*', 'period_list', income_period_list)

def recent_years(years=15, order='descending',future=1):
    """Returns a list of the most recent years, continuing into the future. Defaults to most recent 15 years+1. Useful to populate
        a combobox of years where the most recent ones are most likely. E.g. automobile years or birthdate.
        Keyword paramaters: years, order (descending or ascending), future (defaults to 1)"""
    now = datetime.datetime.now()
    if order=='ascending':
        return list(range(now.year-years,now.year+future,1))
    else:
        return list(range(now.year+future,now.year-years,-1))

def asset_type_list() :
    """Returns a list of assset types for a multiple choice dropdown"""
    return [
        ['savings', 'Savings'],
        ['cd','Certificate of Deposit'],
        ['ira','Individual Retirement Account'],
        ['mutual fund','Money or Mutual Fund'],
        ['stocks','Stocks or Bonds'],
        ['trust','Trust Fund'],
        ['checking','Checking Account'],
        ['vehicle','Vehicle'],
        ['real estate','Real Estate'],
        ['other','Other Asset']
    ]

def income_type_list() :
    """Returns a list of income types for a multiple choice dropdown"""
    type_list = non_wage_income_list()
    type_list.insert(0,['wages','Wages'])
    return type_list

def non_wage_income_list():
    return [
        ['SSR','Social Security Retirement Benefits'],
        ['SSDI','Social Security Disability Benefits'],
        ['SSI','Supplemental Security Income (SSI)'],
        ['pension','Pension'],
        ['TAFDC','TAFDC'],
        ['EAEDC','EAEDC'],
        ['public assistance','Other public assistance'],
        ['SNAP','Food Stamps (SNAP)'],
        ['rent','Income from real estate (rent, etc)'],
        ['room and board','Room and/or Board Payments'],
        ['child support','Child Support'],
        ['alimony','Alimony'],
        ['other','Other Support']
    ]

def expense_type_list() :
    """Returns a list of expense types for a multiple choice dropdown"""
    return [
        ['rent','Rent'],
        ['mortgage','Mortgage'],
        ['food','Food'],
        ['utilities','Utilities'],
        ['fuel','Other Heating/Cooking Fuel'],
        ['clothing','Clothing'],
        ['credit cards','Credit Card Payments'],
        ['property tax','Property Tax (State and Local)'],
        ['other taxes','Other taxes and fees related to your home'],
        ['insurance','Insurance'],
        ['medical','Medical-Dental (after amount paid by insurance)'],
        ['auto','Car operation and maintenance'],
        ['transportation','Other transportation'],
        ['charity','Church or charitable donations'],
        ['loan payments','Loan, credit, or lay-away payments'],
        ['support','Support to someone not in household'],
        ['other','Other']
    ]


class Income(PeriodicValue):
    """Represents a job which may have an hourly rate or a salary.
        Hourly rate jobs must include hours and period. 
        Period is some demoninator of a year for compatibility with
        PeriodicFinancialList class. E.g, to express hours/week, use 52 """
    # is_hourly
    # hourly_rate
    # hours_per_period
    # period (1=year, 12=month, 52=week)
    # value
    # net
    # gross
    # type

    def amount(self, period_to_use=1):
        """Returns the amount earned over the specified period """
        if hasattr(self, 'is_hourly') and self.is_hourly:
            return Decimal(self.hourly_rate * self.hours_per_period * self.period) / Decimal(period_to_use)        
        return (Decimal(self.value) * Decimal(self.period)) / Decimal(period_to_use)

class Job(Income):
    """Represents a job that may be hourly or pay-period based. If non-hourly, may specify gross and net income amounts"""
    def net_amount(self, period_to_use=1):
        """Returns the net amount (e.g., minus deductions). Only applies if value is non-hourly."""
        return (Decimal(self.net) * Decimal(self.period)) / Decimal(period_to_use)

    def gross_amount(self, period_to_use=1):
        """Gross amount is identical to value"""
        return (Decimal(self.value) * Decimal(self.period)) / Decimal(period_to_use)

class SimpleValue(DAObject):
    """Like a Value object, but no fiddling around with .exists attribute because it's designed to store in a list, not a dictionary"""
    def amount(self):
        return self.value    
    def __str__(self):
        return self.value

class ValueList(DAList):
    """Represents a filterable DAList of SimpleValues"""
    def init(self, *pargs, **kwargs):
        self.elements = list()
        self.object_type = SimpleValue
        return super(ValueList, self).init(*pargs, **kwargs)        
    def types(self):
        """Returns a set of the unique types of values stored in the list. Will fail if any items in the list leave the type field unspecified"""
        types = set()
        for item in self.elements:
            if hasattr(item,'type'):
                types.add(item.type)
        return types
    def total(self, type=None):
        """Returns the total value in the list, gathering the list items if necessary.
        You can specify type, which may be a list, to coalesce multiple entries of the same type."""
        self._trigger_gather()
        result = 0
        if type is None:
            for item in self.elements:
                #if self.elements[item].exists:
                result += Decimal(item.amount())
        elif isinstance(type, list):
            for item in self.elements:
                if item.type in type:
                    result += Decimal(item.amount())
        else:
            for item in self.elements:
                if item.type == type:
                    result += Decimal(item.amount())
        return result

class IncomeList(DAList):
    """Represents a filterable DAList of income items, each of which has an associated period or hourly wages."""
    
    def init(self, *pargs, **kwargs):
        self.elements = list()
        if not hasattr(self, 'object_type'):
            self.object_type = Income
        return super(IncomeList, self).init(*pargs, **kwargs)        
    def types(self):
        """Returns a set of the unique types of values stored in the list."""
        types = set()
        for item in self.elements:
            if hasattr(item,'type'):
                types.add(item.type)
        return types

    def owners(self, type=None):
        """Returns a set of the unique owners for the specified type of value stored in the list. If type is None, returns all 
        unique owners in the IncomeList"""
        owners=set()
        if type is None:
            for item in self.elements:
                if hasattr(item, 'owner'):
                    owners.add(item.owner)
        elif isinstance(type, list):
            for item in self.elements:
                if hasattr(item,'owner') and hasattr(item,'type') and item.type in type:
                    owners.add(item.owner)
        else:
            for item in self.elements:
                if hasattr(item,'owner') and item.type == type:
                    owners.add(item.owner)
        return owners

    def total(self, period_to_use=1, type=None):
        """Returns the total periodic value in the list, gathering the list items if necessary.
        You can specify type, which may be a list, to coalesce multiple entries of the same type."""
        self._trigger_gather()
        result = 0
        if period_to_use == 0:
            return(result)
        if type is None:
            for item in self.elements:
                #if self.elements[item].exists:
                result += Decimal(item.amount(period_to_use=period_to_use))
        elif isinstance(type, list):
            for item in self.elements:
                if item.type in type:
                    result += Decimal(item.amount(period_to_use=period_to_use))
        else:
            for item in self.elements:
                if item.type == type:
                    result += Decimal(item.amount(period_to_use=period_to_use))
        return result
    
    def market_value_total(self, type=None):
        """Returns the total market value of values in the list."""
        result = 0
        for item in self.elements:
            if type is None:
                result += Decimal(item.market_value)
            elif isinstance(type, list): 
                if item.type in type:
                    result += Decimal(item.market_value)
            else:
                if item.type == type:
                    result += Decimal(item.market_value)
        return result


    def balance_total(self, type=None):
        self._trigger_gather()
        result = 0
        for item in self.elements:
            if type is None:
                result += Decimal(item.balance)
            elif isinstance(type, list): 
                if item.type in type:
                    result += Decimal(item.balance)
            else:
                if item.type == type:
                    result += Decimal(item.balance)
        return result

class JobList(IncomeList):
    """Represents a list of jobs. Adds the net_total and gross_total methods to the IncomeList class"""
    def init(self, *pargs, **kwargs):
        # self.elements = list()
        self.object_type = Job
        return super(JobList, self).init(*pargs, **kwargs)        
    
    def gross_total(self, period_to_use=1, type=None):
        self._trigger_gather()
        result = 0
        if period_to_use == 0:
            return(result)
        if type is None:
            for item in self.elements:
                #if self.elements[item].exists:
                result += Decimal(item.gross_amount(period_to_use=period_to_use))
        elif isinstance(type, list):
            for item in self.elements:
                if item.type in type:
                    result += Decimal(item.gross_amount(period_to_use=period_to_use))
        else:
            for item in self.elements:
                if item.type == type:
                    result += Decimal(item.gross_amount(period_to_use=period_to_use))
        return result
    def net_total(self, period_to_use=1, type=None):
        self._trigger_gather()
        result = 0
        if period_to_use == 0:
            return(result)
        if type is None:
            for item in self.elements:
                #if self.elements[item].exists:
                result += Decimal(item.net_amount(period_to_use=period_to_use))
        elif isinstance(type, list):
            for item in self.elements:
                if item.type in type:
                    result += Decimal(item.net_amount(period_to_use=period_to_use))
        else:
            for item in self.elements:
                if item.type == type:
                    result += Decimal(item.net_amount(period_to_use=period_to_use))
        return result
