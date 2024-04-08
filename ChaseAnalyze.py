"""
Author: David Hill
Email: DavidLeeHill77@yahoo.com
Date: April 7, 2024
Purpose: To aid in reviewing monthly budget for customers of Chase Bank.
Chase Bank was chosen because it is the author's bank.
Skills Demonstrated: Python, Pandas, Pandas Pivot Tables, Data Manipulation,
Regular Expressions,
Package dependencies: openpyxl, Jinja2, csv, re, pandas, datetime, locale, IPython.display
"""

import csv
import re
import pandas as pd
import datetime as dt
import locale

from IPython.display import display

"""
Capitalized because it is a constant, this dictionary is where the user 
can setup which transactions they want to summarize.  The pattern field 
is a text that the user wants to search, and assign to a replacement 
category.  The pattern is case insensitive.  The number of patterns is
not limited.  It can be as many as are needed.
"""
REPLACEMENTS = [
    {"pattern": "fanny mae.+","replacement": "House Pmt"},
    {"pattern": "ford motor.+?","replacement": "Jeep Pmt"},
    {"pattern": "city of springfield.+?","replacement": "Garbage"},
    {"pattern": "energy company.+?","replacement": "Electricity"},
    {"pattern": "abc lender.+?","replacement": "A/C"},
    {"pattern": "salvation army.+?","replacement": "World Vision"},
    {"pattern": "play store.+?","replacement": "Apple"},
    {"pattern": "verizon.+?payment","replacement": "Phone"},
    {"pattern": "satellite.+?","replacement": "Internet"},
    {"pattern": "geico.+?","replacement": "Car Insurance"},
    {"pattern": "allstate.+?","replacement": "Life Insurance"},
    {"pattern": "orkin.+?","replacement": "Pest Control"},
    {"pattern": "nord.+?","replacement": "VPN"},
    {"pattern": "(walmart|kroger|tom thumb|albertsons|target|exxon).+?","replacement": "Groceries & Gas"},
    {"pattern": "(netflix|hulu|max|paramount|peacock).+?","replacement": "TV Streaming"},
]

"""
Months are irregular, and banks have holidays.  As such, payments can be
posted within a different month than they are budgeted.  Therefor, the 
DAY_TO_ALIGN_MONTH variable is used as a cutoff.  Any transactions before 
the day of month of the DAY_TO_ALIGN_MONTH value will be assigned to the 
month in which it was posted.  All others will be assigned to the following
month.
"""
DAY_TO_ALIGN_MONTH = 15

# Change this FILENAME to match your path and filename.
FILENAME = "C:/Users/profile/Downloads/Chase1234_Activity_YYYYMMDD.CSV"

#  This is banking data, so it will be good to format the numbers like currency.
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def format_value(table_value):  # table_value is a variant data type
    """
    This function formats a value as currency, if the passed value is a float.

    :param table_value: a value from the pivot table.  It could be anything, hence
    it is a variant data type.
    :return: Only float data types get modified, all others get returned with no
    changes at all.  Variant data type.
    """
    if isinstance(table_value, float):
        return locale.currency(table_value, grouping=True)
    return table_value


def align_month(date_value: str, align_to_day: int = 15) -> dt.datetime:
    """
    This function manipulates the date a transaction posted, and assigns the transaction
    to a month.  The month is represented by the fist day of that month (Ex: 2024-02-01)
    The transaction is assigned to a month based on whether it falls before or after the
    align_to_date, which defaults to the 15th of each month.  That date is adjustable by
    passing a different value to the align_to_day parameter in the signature  of the fun-
    ction.  Without this adjustment, transactions might appear twice in one month, and z-
    ero times in other months.

    :param date_value: String that represents a date
    :param align_to_day: Default is 15. This is the day to compare the date_vlaue to.
    :return: date value to align the expense to, based on whether is is greater or
    less than the align_to day.  If greater, it will return the first date of the
    next month, else it will return the first date of the current month.
    """
    dt_val = dt.datetime.strptime(date_value, "%m/%d/%Y")  # Date from string
    if dt_val.day > align_to_day:
        month = 30 if dt_val.month != 1 else 28  # Days added to get next month
        dt_val = dt_val + dt.timedelta(days=month)
    return dt_val.strftime(f"%Y-%m-01")


def patternize(search_string: str) -> str:
    """
    This function modifies a search string.  I changes it into a regular expression
    that searches for both capitalized and lower-case letters, for every letter in
    the search string.  This is necessary because the regular expression engine used
    below does not allow the -i option.

    :param search_string: String that will be turned into a regular expression
    :return: regular expresssion returned as a string
    """
    p = re.compile('[A-Za-z]')
    pattern = ""
    for char in search_string:
        if p.match(char):
            pattern += f"[{char.upper()}{char.lower()}]"
        else:
            pattern += char
    return pattern


def summarize_expenses():  # This is the main method
    """
    The file comes from Chase bank with an extra comma at the end of every line.
    To repair the problem, an extra field must be added to the first line of the
    file.  Without this step, the columns will be mis-aligned.  Pandas will assume
    that this first column in every record is a row-header.
    """
    with open(FILENAME, 'r') as f:
        content = f.readlines()
    if "field" not in content[0]:  # If the field is already added, don't add it again
        content[0] = content[0][:-2] + ",field" + content[0][-1:]  # Add "field" right before the carriage return
        with open(FILENAME, 'w') as f:
            f.writelines(content)

    #  Read the data from the hard drive.
    df = pd.read_csv(FILENAME, sep=',', quoting=csv.QUOTE_MINIMAL)

    #  Data manipulation phase.
    """  
    Create a new field called Month, that will allow all Posting Dates to be aggregated to a single date
    that represents all the dates for that month.
    """
    df["Month"] = df["Posting Date"].apply(lambda x: align_month(x))
    #  Create a new field called Payee, that is empty.
    df["Payee"] = None

    """
    Some payees in the data appear the same all the time, other contain unique transaction IDs in the Description
    field.  It is necessary to create a homogenized field for each payee, so that records can be shown on a single
    line of a pivot table.  Payee will be the group-by field.
    """
    for rep in REPLACEMENTS:
        print(f"Processing {rep["replacement"]}")
        df.loc[df["Description"].str.contains(patternize(rep["pattern"]), regex=True
                                              , na=False), "Payee"] = rep["replacement"]

    # Create a pivot table
    table = pd.pivot_table(df, values='Amount', index=['Payee'], columns=['Month'], aggfunc="sum", margins=True
                           , margins_name="Total", fill_value=0)
    # Format value fields as currency (Non-Jupyter)
    formatted_table = table.map(lambda x: locale.currency(x, grouping=True) if isinstance(x, float) else x)

    # Format value fields as currency (Jupyter)
    styler = table.style.format({"Amount": "${0:,.0f}"})
    styler

    # Export modified DataFrame as CSV
    df.to_csv("c:/Users/ColdB/Downloads/Chase_Activity.CSV")

    # Export formatted pivot table as Excel
    styler.to_excel('styled_table.xlsx')

    print('Finished!')


if __name__ == "__main__":
    summarize_expenses()
