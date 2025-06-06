import pandas as pd
from pandas import concat
from itertools import chain


report0 = pd.ExcelFile("reports1.xlsx")
report1 = pd.ExcelFile("reports2.xlsx")
report2 = pd.ExcelFile("reports3.xlsx")

#print(report1.sheet_names)

markt = [pd.read_excel(report0, sheet_name='2) Marktforschungsbericht'), pd.read_excel(report1, sheet_name='2) Marktforschungsbericht'), pd.read_excel(report2, sheet_name='2) Marktforschungsbericht')]
geschäftsbericht = [pd.read_excel(report0, sheet_name='15) Geschäftsbericht'), pd.read_excel(report1, sheet_name='15) Geschäftsbericht'), pd.read_excel(report2, sheet_name='15) Geschäftsbericht')]
#print(markt)
#print(geschäftsbericht[1])
if(False):
    print()
    print("Fremdkapitalquote")
    for i in [1, 3, 4, 5, 6, 7, 8]:
        print(i, geschäftsbericht[1].iloc[38, i]/geschäftsbericht[1].iloc[42, i])
    print()
    print("Eigenkapitalrendite")
    for i in [1, 3, 4, 5, 6, 7, 8]:
        print(i, geschäftsbericht[1].iloc[13, i]/geschäftsbericht[0].iloc[32, i])
    print()
    print("Umsatzrendite")
    for i in [1, 3, 4, 5, 6, 7, 8]:
        print(i, geschäftsbericht[1].iloc[13, i]/geschäftsbericht[1].iloc[3, i])
    print()
#print("Kurs tatsächlich")
kurs = [218, 319, 468, 477, 479, 391, 470, 220, 262, 206, 202, 291, 295, 285, 365, 74, 334, 305, 284, 374, 300, 349]
eigenkapital = geschäftsbericht[2].iloc[32, [1, 3, 4, 5, 6, 7, 8]].to_list() + geschäftsbericht[1].iloc[32, [1, 3, 4, 5, 6, 7, 8]].to_list() + geschäftsbericht[0].iloc[32, range(1, 9)].to_list()
gewinn = geschäftsbericht[2].iloc[13, [1, 3, 4, 5, 6, 7, 8]].to_list() + geschäftsbericht[1].iloc[13, [1, 3, 4, 5, 6, 7, 8]].to_list() + geschäftsbericht[0].iloc[13, range(1, 9)].to_list()
tech = markt[2].iloc[5, [2, 4, 5, 6, 7, 8, 9]].to_list() + markt[1].iloc[5, [2, 4, 5, 6, 7, 8, 9]].to_list() + markt[0].iloc[5, range(2, 10)].to_list()
fremdkapital = geschäftsbericht[2].iloc[38, [1, 3, 4, 5, 6, 7, 8]].to_list() + geschäftsbericht[1].iloc[38, [1, 3, 4, 5, 6, 7, 8]].to_list() + geschäftsbericht[0].iloc[38, range(1, 9)].to_list()
berechnet = kurs.copy()
abweichung = kurs.copy()
for i in range(len(kurs)):
    berechnet[i] = 22.4 + eigenkapital[i] * 0.101 + gewinn[i] * 0.087 + tech[i] * 14 - fremdkapital[i] * 0.03
for i in range(len(kurs)):
    #print(i, kurs[i])
    abweichung[i] = kurs[i] - berechnet[i]
#print()
#print("Kurs?")
for i in range(len(kurs)):
    1
    #print(i+1, berechnet[i])
print()
print("Abweichung", sum(abweichung)/len(kurs), sum(i*i for i in abweichung)/len(kurs))
for i in range(len(kurs)):
    1
    #print(i+1, abweichung[i])