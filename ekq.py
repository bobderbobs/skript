import pandas as pd
from pandas import concat
from itertools import chain


report0 = pd.ExcelFile("reports2.xlsx")
report1 = pd.ExcelFile("reports3.xlsx")

#print(report.sheet_names)

geschäftsbericht = [pd.read_excel(report0, sheet_name='15) Geschäftsbericht'), pd.read_excel(report1, sheet_name='15) Geschäftsbericht')]

print(geschäftsbericht[1])
print()
print("Fremdkapitalquote")
for i in [6, 5, 8, 4]:
    print(i, geschäftsbericht[1].iloc[38, i]/geschäftsbericht[1].iloc[42, i])
print()
print("Eigenkapitalrendite")
for i in [6, 5, 8, 4]:
    print(i, geschäftsbericht[1].iloc[13, i]/geschäftsbericht[0].iloc[32, i])
print()
print("Umsatzrendite")
for i in [6, 5, 8, 4]:
    print(i, geschäftsbericht[1].iloc[13, i]/geschäftsbericht[1].iloc[3, i])