import csv
from pathlib import Path
from datetime import datetime
import hashlib # for file checking
path = Path('./statements')
from decimal import Decimal
from collections import namedtuple

HSBCStatementRecord = namedtuple('HSBCStatementRecord', ['date', 'type', 
                                'description', 'debit', 'credit', 'balance',
                                'timestamp'])

def normalize(record):
  """ Remove formating inconsistences"""
  for index, attribute in enumerate(record):
    record[index] = str(record[index]).strip()
  return record
       

def get_records():
  seen = [] # Prevent processing the same file twice, by storing list of hashes
  records = [] #empty list of records, which we build from the statements
  for statement in path.iterdir():
    with open(statement, newline='') as csvfile:
      # check we've not already seen this file by hashing it
      hasher = hashlib.md5()
      buf = csvfile.read()
      hasher.update(buf.encode('utf-8'))
      fileHash = hasher.hexdigest()
      if fileHash in seen:
        print("Skipping file {filename}".format(filename=statement))
        continue
      seen.append(fileHash)
      csvfile.seek(0) # Go back to begining of file after hashing
      reader = csv.reader(csvfile, delimiter=',')
      next(reader, None)
      for row in reader:
        # Convert date to timestamp, append to end of record for easy sorting
        row.append(datetime.strptime(row[0], "%d %b %Y").timestamp())
        row = normalize(row)
        if len(row) == 8: # NOTE Why are HSBC statement lines on rare occasions 8 elements rather than 7?
          """ Concatenate element 3 into element 2 (description) then delete (pop) the third element"""
          row[2] = row[2] + ' ' + row[3]
          row.pop(3)
        records.append(HSBCStatementRecord._make(row))
      
  records.sort(key=lambda record: record[-1]) # Sort on last element (a timestamp)
  return records

#  Index key:
#  0 - Date
#  1 - Type
#  2 - Description
#  3 - Paid Out, amount, float
#  4 - Pain In, amount, float
#  7 - Balance (not used, because does not show opening balance)
#  8 - Timestamp (we created and added)

def isDebit(record):
  try:
    Decimal(record.debit)
    return True
  except:
    return False

def isCredit(record):
  try:
    Decimal(record.credit)
    return True
  except:
    return False

def total_income(records):
  income = Decimal(0.0)
  for record in records:
    if isCredit(record):
      income += Decimal(record.credit)
  return income

def total_payments(records):
  payments = Decimal(0.0)
  for record in records:
    if isDebit(record) and "BEDS" not in record[3]: #TODO ask HSBC about BEDS
      payments += Decimal(record.debit)
  return payments

def filter_by_month_year(record, check_month, check_year):
  # The last element (-1) of records is assumed to be timestamp
  # %m Month as a zero-padded decimal number 01, 02, …, 12
  # %Y Year with century as a decimal number 0001, 0002, …, 2013, 2014...
  # * If "*" is passed for either year or month, then all are included respectivly
  if check_month is "*" and check_year is "*":
    return True # No filter needed, both month and year is globbed

  date = datetime.fromtimestamp(int(float(record[-1])))
  year = date.strftime("%Y")
  month = date.strftime("%m")
  # Filter on both month and year
  if (month == check_month and year == check_year):
    return True
  # Just filter on year
  if (check_month is "*" and check_year is not "*"):
    if year == check_year:
      return True
  # Just filter on month. Why would anyone do this?
  if (check_year is "*" and check_month is not "*"):
    if month == check_month:
      return True
  return False #Always return false if we get here, no match

def filter_by_needle(record, needle):
    # Lower sting 
    # find sting in description index 2
    needle = needle.lower()
    if needle in record[2].lower():
        return True
    return False

def search(needle):
  # split on or string if used (e.g. a search for "this OR that")
  found = []
  for needle in needle.split("OR"):
    records = get_records()
    # Filter by needle
    records = list(filter(lambda record: filter_by_needle(record, needle.strip()), records))
    for record in records:
      record = normalize(record)
      found.append(record)
  #Make unique (an OR query may result in the same record(s) being found twice)
  seen = []
  for record in found:
    if record not in seen:
      seen.append(record)
  
  return seen

def calculate(year=None, month=None):
  if year is None or month is None:
    year = input("Year:")
    month = input("Month:")
  records = get_records()
  records = list(filter(lambda record: filter_by_month_year(record, month, year), records))
  if month != "*":
    month = datetime.strptime(month, "%m").strftime("%b")
  msg = "#### {month} {year} ####\n".format(month=month, year=year)
  total_paid = total_payments(records)
  total_recieved = total_income(records)
  msg += "Total payments: {}\n".format(str(total_paid))
  msg += "Total income: {}\n".format(str(total_recieved))
  profitLoss = total_income(records) - total_payments(records)
  msg += "Profit/Loss: {}\n".format(str(total_income(records) - total_payments(records)))
  print(msg)
  return msg

def g():
  calculate()

def all(year, months):
  # e.g. all("2019", "01,02,03,04,05")
  monthsList = months.split(',')
  for month in monthsList:
    calculate(year=year, month=month)

def usage():
  print("Usage:")
  print("- calculate() # For single quick usage")
  print('- all("2019", "01,02,03")')

if __name__ == "__main__":
  usage()
