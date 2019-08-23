# HSBC CSV Statement processer

Parse HSBC business csv statement exports, and easily view
totall outgoings/income. Also ability to search through 
transactions.

- Easily & Quickly view total income/outgoing for each month
- Query by year, month

Steps to use:
  1. Download your csv statements and put in the 'statements' folder
  2. run the program `python main.py`
  3. Type `calculate()`

## Example output:

```
>>> calculate()
Year:2019
Month:04
#### Apr 2019 ####
Total payments: 1832.02
Total income: 5371.29
Profit/Loss: 3539.27
```

More advanced you can specify a year and selecton of months

```
>>> all("2019", "02,03,04,05")
#### Feb 2019 ####
Total payments: 747.02
Total income: 713.63
Profit/Loss: -33.39
#### Mar 2019 ####
Total payments: 1237.29
Total income: 1403.75
Profit/Loss: 166.46
#### Apr 2019 ####
Total payments: 1832.02
Total income: 5371.29
Profit/Loss: 3539.27
#### May 2019 ####
Total payments: 2542.00
Total income: 3603.81
Profit/Loss: 1061.81
```

### Search

Simple search:
```
> search("ASDA") 
```

OR based search
```
> search("ASDA OR Wallmart")
```
