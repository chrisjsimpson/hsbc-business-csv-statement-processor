import csv
from pathlib import Path
from datetime import datetime
import hashlib # for file checking
path = Path('./statements')
from decimal import Decimal

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
        records.append(row)
      
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
  if record[3] is not '':
    return True
  return False

def isCredit(record):
  if record[4] is not '':
    return True
  return False


def total_income(records):
  income = Decimal(0.0)
  for record in records:
    if isCredit(record):
      income += Decimal(record[4])
  return income

def total_payments(records):
  payments = Decimal(0.0)
  for record in records:
    if isDebit(record):
      payments += Decimal(record[3])
  return payments

def filter_by_month_year(record, check_month, check_year):
  # The last element (-1) of records is assumed to be timestamp
  # %m Month as a zero-padded decimal number 01, 02, …, 12
  # %Y Year with century as a decimal number 0001, 0002, …, 2013, 2014...
  date = datetime.fromtimestamp(record[-1])
  year = date.strftime("%Y")
  month = date.strftime("%m")
  if (year == check_year and month == check_month):
    return True
  return False

def calculate():
  year = input("Year:")
  month = input("Month:")
  records = get_records()
  records = list(filter(lambda record: filter_by_month_year(record, month, year), records))
  print("Total payments: {}".format(str(total_payments(records))))
  print("Total income: {}".format(str(total_income(records))))
  print("Profit/Loss: {}".format(str(total_income(records) - total_payments(records))))
 
calculate() 
