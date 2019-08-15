import csv
from pathlib import Path
from datetime import datetime
import hashlib # for file checking
path = Path('./statements')

###
### TODO IMPORTANT: Remove / Check for duplicate files to avoid double counting
### Cannot remove duplicated, because sometimes trasactions have the same
### date, amount & description even for seperate payments (HSBC does NOT show
# the exact time the trasaction happened, so it's imposible to know if they are
# duplicates or not).  To sovle this, just check if we've already processed that
# file.
###

# entry
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
      # Convert date to timestamp, append to start of record for easy sorting
      row.insert(0, datetime.strptime(row[0], "%d %b %Y").timestamp())
      records.append(row)
      
records.sort(key=lambda record: record[0]) # Sort on element on (a timestamp)
for record in records:
  print(record)
import pdb;pdb.set_trace()
