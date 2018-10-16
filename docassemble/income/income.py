from docassemble.base.core import DAObject, DAList, DADict
from docassemble.base.util import Value, PeriodicValue, FinancialList, PeriodicFinancialList
from decimal import Decimal

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
    return [
        ['wages','Wages'],
        ['ssr','Social Security Benefits'],
        ['ssi','Supplemental Security Income (SSI)'],
        ['pension','Pension'],
        ['tafdc','TAFDC'],
        ['eaedc','EAEDC'],
        ['public assistance','Other public assistance'],
        ['tanf','Food Stamps (TANF)'],
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


class HourlyOrPeriodicValue(PeriodicValue):
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
    # kind
    @property
    def value(self):
        return self.amount()
    
    @value.setter
    def value(self, value):
        self._value = value

    def amount(self, period_to_use=1):
        """Returns the amount earned over the specified period """
        if hasattr(self, 'is_hourly') and self.is_hourly:
            return Decimal(self.hourly_rate * self.hours_per_period * self.period) / Decimal(period_to_use)        
        return (Decimal(self._value) * Decimal(self.period)) / Decimal(period_to_use)

    def net(self, period_to_use=1):
        """Returns the net amount. Only applies if value is non-hourly."""
        return (Decimal(self.net) * Decimal(self.period)) / Decimal(period_to_use)
    def gross(self, period_to_use=1):
        """Returns the gross amount. Only applies if value is non-hourly."""
        return (Decimal(self.gross) * Decimal(self.period)) / Decimal(period_to_use)
    def income(self, period_to_use):
        """Returns the income, which may be different from value for an asset like a Savings account."""
        return (Decimal(self.income) * Decimal(self.period)) / Decimal(period_to_use)
    def __str__(self):
        return self.kind

class SimpleValue(DAObject):
    """Like a Value object, but no fiddling around with .exists attribute because it's designed to store in a list, not a dictionary"""
    def amount(self):
        return self.value
    def __str__(self):
        return self.value

class ValueList(DAList):
    """Represents a filterable DAList of Values"""
    def init(self, *pargs, **kwargs):
        self.elements = list()
        self.object_type = SimpleValue
        return super(ValueList, self).init(*pargs, **kwargs)        
    def kinds(self):
        """Returns a set of the unique kinds of values stored in the list. Will fail if any items in the list leave the kind field unspecified"""
        kinds = set()
        for item in self.elements:
            kinds.add(item.kind)
        return kinds
    def total(self, kind=None):
        """Returns the total value in the list, gathering the list items if necessary.
        You can specify kind, which may be a list, to coalesce multiple entries of the same kind."""
        self._trigger_gather()
        result = 0
        if kind is None:
            for item in self.elements:
                #if self.elements[item].exists:
                result += Decimal(item.amount())
        elif isinstance(kind, list):
            for item in self.elements:
                if item.kind in kind:
                    result += Decimal(item.amount())
        else:
            for item in self.elements:
                if item.kind == kind:
                    result += Decimal(item.amount())
        return result


class HourlyOrPeriodicFinancialList(DAList):
    """Represents a filterable DAList of income items, each of which has an associated period or hourly wages."""
    
    def init(self, *pargs, **kwargs):
        self.elements = list()
        self.object_type = HourlyOrPeriodicValue
        return super(HourlyOrPeriodicFinancialList, self).init(*pargs, **kwargs)        
    def kinds(self):
        """Returns a set of the unique kinds of values stored in the list. Will fail if any items in the list leave the kind field unspecified"""
        kinds = set()
        for item in self.elements:
            kinds.add(item.kind)
        return kinds

    def total(self, period_to_use=1, kind=None):
        """Returns the total periodic value in the list, gathering the list items if necessary.
        You can specify kind, which may be a list, to coalesce multiple entries of the same kind."""
        self._trigger_gather()
        result = 0
        if period_to_use == 0:
            return(result)
        if kind is None:
            for item in self.elements:
                #if self.elements[item].exists:
                result += Decimal(item.amount(period_to_use=period_to_use))
        elif isinstance(kind, list):
            for item in self.elements:
                if item.kind in kind:
                    result += Decimal(item.amount(period_to_use=period_to_use))
        else:
            for item in self.elements:
                if item.kind == kind:
                    result += Decimal(item.amount(period_to_use=period_to_use))
        return result

    def gross_total(self, period_to_use=1, kind=None):
        self._trigger_gather()
        result = 0
        if period_to_use == 0:
            return(result)
        if kind is None:
            for item in self.elements:
                #if self.elements[item].exists:
                result += Decimal(item.gross(period_to_use=period_to_use))
        elif isinstance(kind, list):
            for item in self.elements:
                if item.kind in kind:
                    result += Decimal(item.gross(period_to_use=period_to_use))
        else:
            for item in self.elements:
                if item.kind == kind:
                    result += Decimal(item.gross(period_to_use=period_to_use))
        return result
    def net_total(self, period_to_use=1, kind=None):
        self._trigger_gather()
        result = 0
        if period_to_use == 0:
            return(result)
        if kind is None:
            for item in self.elements:
                #if self.elements[item].exists:
                result += Decimal(item.net(period_to_use=period_to_use))
        elif isinstance(kind, list):
            for item in self.elements:
                if item.kind in kind:
                    result += Decimal(item.net(period_to_use=period_to_use))
        else:
            for item in self.elements:
                if item.kind == kind:
                    result += Decimal(item.net(period_to_use=period_to_use))
        return result
    
    def income_total(self, period_to_use=1, kind=None):
        self._trigger_gather()
        result = 0
        if period_to_use == 0:
            return(result)
        if kind is None:
            for item in self.elements:
                #if self.elements[item].exists:
                result += Decimal(item.income(period_to_use=period_to_use))
        elif isinstance(kind, list):
            for item in self.elements:
                if item.kind in kind:
                    result += Decimal(item.income(period_to_use=period_to_use))
        else:
            for item in self.elements:
                if item.kind == kind:
                    result += Decimal(item.income(period_to_use=period_to_use))
        return result