import os
import sys
from setuptools import setup, find_packages
from fnmatch import fnmatchcase
from distutils.util import convert_path

standard_exclude = ('*.pyc', '*~', '.*', '*.bak', '*.swp*')
standard_exclude_directories = ('.*', 'CVS', '_darcs', './build', './dist', 'EGG-INFO', '*.egg-info')
def find_package_data(where='.', package='', exclude=standard_exclude, exclude_directories=standard_exclude_directories):
    out = {}
    stack = [(convert_path(where), '', package)]
    while stack:
        where, prefix, package = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            if os.path.isdir(fn):
                bad_name = False
                for pattern in exclude_directories:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        break
                if bad_name:
                    continue
                if os.path.isfile(os.path.join(fn, '__init__.py')):
                    if not package:
                        new_package = name
                    else:
                        new_package = package + '.' + name
                        stack.append((fn, '', new_package))
                else:
                    stack.append((fn, prefix + name + '/', package))
            else:
                bad_name = False
                for pattern in exclude:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        break
                if bad_name:
                    continue
                out.setdefault(package, []).append(prefix+name)
    return out

setup(name='docassemble.income',
      version='0.0.36',
      description=('A module to help with gathering a financial statement, including hourly wages'),
      long_description='# Income Module for Docassemble\r\n\r\nIncludes examples at docassemble.income:interview_test.yml, docassemble.income:financial_statement.yml\r\n\r\n## Classes\r\n\r\n### Income(PeriodicValue)\r\n```\r\n    def amount(self, period_to_use=1):\r\n        """Returns the amount earned over the specified period """\r\n```\r\n### IncomeList(DAList)\r\n```\r\n    def types(self):\r\n        """Returns a set of the unique types of values stored in the list. Will fail if any items in the list leave the type field unspecified"""\r\n\r\n    def owners(self, type=None):\r\n        """Returns a set of the unique owners for the specified type of value stored in the list. If type is None, returns all unique owners in the IncomeList"""\r\n\r\n    def total(self, period_to_use=1, type=None):\r\n        """Returns the total periodic value in the list, gathering the list items if necessary.\r\n    \r\n    def market_value_total(self, type=None):\r\n        """Returns the total market value of values in the list."""\r\n\r\n    def balance_total(self, type=None):\r\n    \r\n    def matches(self, type):\r\n        """Returns an IncomeList consisting only of elements matching the specified Income type, assisting in filling PDFs with predefined spaces"""\r\n```\r\n\r\n### Job(Income)\r\n```\r\n    def net_amount(self, period_to_use=1):\r\n        """Returns the net amount (e.g., minus deductions). Only applies if value is non-hourly."""\r\n\r\n    def gross_amount(self, period_to_use=1):\r\n        """Gross amount is identical to value"""\r\n```\r\n### JobList\r\n```\r\n    def gross_total(self, period_to_use=1, type=None):\r\n\r\n    def net_total(self, period_to_use=1, type=None):\r\n \r\n```\r\n\r\n### SimpleValue\r\n\r\n```\r\n    def amount(self):\r\n\r\n```\r\n\r\n### Vehicle\r\nLike SimpleValue, but adds year_make_model method\r\n\r\n### ValueList\r\n```\r\n    def types(self):\r\n        """Returns a set of the unique types of values stored in the list. Will fail if any items in the list leave the type field unspecified"""\r\n\r\n    def total(self, type=None):\r\n```\r\n\r\n### VehicleList\r\n\r\n### Asset\r\n\r\nLike Income, but the value field is optional\r\n\r\n### AssetList\r\nlist of Assets\r\n\r\n## Utility functions\r\n\r\n```\r\nrecent_years(years=15, order=\'descending\',future=1):\r\n    """Returns a list of the most recent years, continuing into the future. Defaults to most recent 15 years+1. Useful to populate\r\n        a combobox of years where the most recent ones are most likely. E.g. automobile years or birthdate.\r\n        Keyword paramaters: years, order (descending or ascending), future (defaults to 1)"""\r\n        \r\nasset_type_list() :\r\n    """Returns a list of assset types for a multiple choice dropdown"""\r\n    \r\nincome_type_list() :\r\n    """Returns a list of income types for a multiple choice dropdown"""\r\n\r\ndef non_wage_income_list():\r\n    """Returns a list of income types for a multiple choice dropdown, excluding wages"""\r\n\r\nexpense_type_list() :\r\n    """Returns a list of expense types for a multiple choice dropdown"""\r\n    \r\ndef flatten(listname,index=1):\r\n    """Return just the nth item in an 2D list. Intended to use for multiple choice option lists in Docassemble.\r\n        e.g., flatten(asset_type_list()) will return [\'Savings\',\'Certificate of Deposit\'...] """\r\n\r\ndef income_period(frequency):\r\n  """Returns the plain language translation of the income period, which is a number"""\r\n\r\n```',
      long_description_content_type='text/markdown',
      author='Quinten Steenhuis',
      author_email='admin@admin.com',
      license='The MIT License (MIT)',
      url='https://docassemble.org',
      packages=find_packages(),
      namespace_packages=['docassemble'],
      install_requires=[],
      zip_safe=False,
      package_data=find_package_data(where='docassemble/income/', package='docassemble.income'),
     )

