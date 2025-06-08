import pandas as pd
from pandas import concat
from itertools import chain
import math

report3 = pd.ExcelFile("reports0.xlsx")
report2 = pd.ExcelFile("reports1.xlsx")
report1 = pd.ExcelFile("reports2.xlsx")
report0 = pd.ExcelFile("reports3.xlsx")

#print(report1.sheet_names)

markt = [pd.read_excel(report0, sheet_name='2) Marktforschungsbericht'), pd.read_excel(report1, sheet_name='2) Marktforschungsbericht'), pd.read_excel(report2, sheet_name='2) Marktforschungsbericht'), pd.read_excel(report3, sheet_name='2) Marktforschungsbericht')]
geschäftsbericht = [pd.read_excel(report0, sheet_name='15) Geschäftsbericht'), pd.read_excel(report1, sheet_name='15) Geschäftsbericht'), pd.read_excel(report2, sheet_name='15) Geschäftsbericht'), pd.read_excel(report3, sheet_name='15) Geschäftsbericht')]
#print(markt)
#print(geschäftsbericht[1])
if(False):
    print()
    print("Fremdkapitalquote")
    for i in [1, 3, 4, 5, 6, 7, 8]: #fremdkapital/bilanz
        print(i, geschäftsbericht[1].iloc[38, i]/geschäftsbericht[1].iloc[42, i])
    print()
    print("Eigenkapitalrendite")
    for i in [1, 3, 4, 5, 6, 7, 8]: #gewinn/eigenkapital(p-1)
        print(i, geschäftsbericht[1].iloc[13, i]/geschäftsbericht[0].iloc[32, i])
    print()
    print("Umsatzrendite")
    for i in [1, 3, 4, 5, 6, 7, 8]: #gewinn/umsatz
        print(i, geschäftsbericht[1].iloc[13, i]/geschäftsbericht[1].iloc[3, i])
    print()
#print("Kurs tatsächlich")
kurs = [319, 468, 477, 479, 391, 470]
eigenkapital = geschäftsbericht[0].iloc[32, [3, 4, 5, 6, 7, 8]].to_list() + geschäftsbericht[1].iloc[32, [1, 3, 4, 5, 6, 7, 8]].to_list() + geschäftsbericht[2].iloc[32, range(1, 9)].to_list()
eigenkapital_vorperiode = geschäftsbericht[1].iloc[32, [3, 4, 5, 6, 7, 8]].to_list() + geschäftsbericht[2].iloc[32, [1, 3, 4, 5, 6, 7, 8]].to_list() + geschäftsbericht[3].iloc[32, range(1, 9)].to_list()
gewinn = geschäftsbericht[0].iloc[13, [3, 4, 5, 6, 7, 8]].to_list() + geschäftsbericht[1].iloc[13, [1, 3, 4, 5, 6, 7, 8]].to_list() + geschäftsbericht[2].iloc[13, range(1, 9)].to_list()
tech = markt[0].iloc[5, [4, 5, 6, 7, 8, 9]].to_list() + markt[1].iloc[5, [2, 4, 5, 6, 7, 8, 9]].to_list() + markt[2].iloc[5, range(2, 10)].to_list()
bekanntheit = markt[0].iloc[9, [4, 5, 6, 7, 8, 9]].to_list() + markt[1].iloc[9, [2, 4, 5, 6, 7, 8, 9]].to_list() + markt[2].iloc[9, range(2, 10)].to_list()
fremdkapital = geschäftsbericht[0].iloc[38, [3, 4, 5, 6, 7, 8]].to_list() + geschäftsbericht[1].iloc[38, [1, 3, 4, 5, 6, 7, 8]].to_list() + geschäftsbericht[2].iloc[38, range(1, 9)].to_list()
umsatz = geschäftsbericht[0].iloc[3, [3, 4, 5, 6, 7, 8]].to_list() + geschäftsbericht[1].iloc[3, [1, 3, 4, 5, 6, 7, 8]].to_list() + geschäftsbericht[2].iloc[3, range(1, 9)].to_list()
bilanz = geschäftsbericht[0].iloc[42, [3, 4, 5, 6, 7, 8]].to_list() + geschäftsbericht[1].iloc[42, [1, 3, 4, 5, 6, 7, 8]].to_list() + geschäftsbericht[2].iloc[42, range(1, 9)].to_list()
berechnet = kurs.copy()
abweichung = kurs.copy()
Faktoren = [[43, 43, 43],
            [0.0993, 0.0993, 0.0993],
            [0.14, 0.14, 0.14],
            [12, 12, 12], 
            [-0.045, -0.045, -0.045],
            [0.0023, 0.0023, 0.0023],
            [220, 220, 220],
            [95, 95, 95],
            [-9, -9, -9],
            [7, 7, 7],
            [-0.0001, -0.0001, -0.0001],
            [-0.04, -0.04, -0.04]]
for j in range(3):
    for i in range(len(kurs)):
        berechnet[i] = Faktoren[0][j]                                           #konstant
        berechnet[i] += eigenkapital[i] * Faktoren[1][j]                        #eigenkapital
        berechnet[i] += gewinn[i] * Faktoren[2][j]                              #gewinn
        berechnet[i] += tech[i] * Faktoren[3][j]                                #tech
        berechnet[i] += fremdkapital[i] * Faktoren[4][j]                        #fremdkapital
        berechnet[i] += umsatz[i] * Faktoren[5][j]                              #umsatz
        berechnet[i] += gewinn[i]/umsatz[i] * Faktoren[6][j]                    #umsatzrendite
        berechnet[i] += gewinn[i]/eigenkapital_vorperiode[i] * Faktoren[7][j]   #eigenkapitalrendite
        berechnet[i] += eigenkapital[i]/bilanz[i] * Faktoren[8][j]              #eigenkapitalquote
        berechnet[i] += fremdkapital[i]/bilanz[i] * Faktoren[9][j]              #fremdkapitalqute
        berechnet[i] += bilanz[i] * Faktoren[10][j]                             #bilanz
        berechnet[i] += bekanntheit[i] * Faktoren[11][j]                        #bekanntheit
        abweichung[i] = kurs[i] - berechnet[i]
    print("berechneter Aktienkurs = " + str(Faktoren[0][j]) + " + Eigenkapital * " + str(Faktoren[1][j]) + " + Jahresüberschuss * " + str(Faktoren[2][j]) +
          " + Produktqualität * " + str(Faktoren[3][j]) + " + Fremdkapital * " + str(Faktoren[4][j]) + " + Umsatz * " + str(Faktoren[5][j]) +
          " + Umsatzrendite * " + str(Faktoren[6][j]) + " + Eigenkapitalrendite * " + str(Faktoren[7][j]) + " + Eigenkapital * " + str(Faktoren[1][j]) + " + Eigenkapital * " + str(Faktoren[1][j]) + " + Eigenkapital * " + str(Faktoren[1][j]) + " + Eigenkapital * " + str(Faktoren[1][j]))
    print("Standardabweichung", math.sqrt(sum(i*i for i in abweichung)/len(kurs)))