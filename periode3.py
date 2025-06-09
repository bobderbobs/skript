#source skript/bin/activate
#cd /home/bobderbobs/Schreibtisch/Manager\ Cup/skript
import pandas as pd
from pandas import concat
from itertools import chain
pd.options.mode.copy_on_write = True

# Excel-Datei laden
report = pd.ExcelFile("reports3.xlsx")

# Namen aller Tabellenblätter anzeigen
#print(report.sheet_names)

# Tabelle mit den Mitarbeitern laden
if True:
    fertigung = [pd.read_excel(report, sheet_name="3) Fertigungsbericht")]
    forschung = [pd.read_excel(report, sheet_name="4) Forschung & Entwicklung")]
    lager = [pd.read_excel(report, sheet_name="5) Lager")]
    personal = [pd.read_excel(report, sheet_name="6) Personal")]
    kostenstellen = [pd.read_excel(report, sheet_name="8) Kostenstellenrechnung")]
    kostenträger = [pd.read_excel(report, sheet_name="9) Kostenträgerrechnung")]
    gewinn = [pd.read_excel(report, sheet_name="11) Gewinn- und Verlustrechnung")]
    liquidität = [pd.read_excel(report, sheet_name="12) Liquiditätsrechnung")]
    bilanz = [pd.read_excel(report, sheet_name="14) Bilanz")]
    #cashflow = [pd.read_excel(report, sheet_name="13) Cashflow Statement")]
    #kostenarten = [pd.read_excel(report, sheet_name="7) Kostenartenrechnung")]
    #deckung = [pd.read_excel(report, sheet_name="10) Deckungsbeitragsrechnung")]
    #entscheidung = pd.read_excel(report, sheet_name="16) Entscheidungsprotokoll")



### Neue Daten

periode = 1

m_typ = ['A', 'B']
m_kaufpreis = [1250, 750]
m_dauer = [10, 10]
m_kapazität = [12000, 6000]
m_fixkosten = [40, 35]
m_resterlös = [25, 25]

p_kapazität = [1]
a_kapazität = [1900]

tech_step_cost = 100
tech_cost_increase = 2

#0 = einkauf
#1 = verwaltung
#2 = fertigung
#3 = kundenbetreuer

einstellung = 15
entlassung = 10
nebenkosten = 30
lohn = [37.6, 34.3, 42.4, 40.7]
überstunden_max = 0.20
überstunden_kosten = 0.25

einkauf_mengen = [35000, 45000, 60000, 80000, 1000000]
einkauf_preise = [41, 37, 35, 33, 31]
einkauf_jit = 50
lagerkosten = [3, 5]
transport = 5
betrieb = 3

#Einkauf, Verwaltung, F&E, Vertieb, Verwaltung
sonstige_fix = [50, 50, 0, 100, 100]

einzahlung = [80, 75]
auszahlung = 1

#überziehung, langzeit
zinsen = [5, 4]

steuern = 35



### Entscheidungen/Erwartungen

anzahl = 1

for i in range(anzahl):
    forschung.append(forschung[0].copy())
    personal.append(personal[0].copy())
    fertigung.append(fertigung[0].copy())
    lager.append(lager[0].copy())
    kostenstellen.append(kostenstellen[0].copy())
    kostenträger.append(kostenträger[0].copy())
    gewinn.append(gewinn[0].copy())
    liquidität.append(liquidität[0].copy())
    bilanz.append(bilanz[0].copy())


nachfrage = [0, 60000, 60000, 60000]
fluktuation = [0, 0, 0, 0]

plan_einkauf = [0, 60000, 60000, 60000]
plan_produktion = [0, 60000, 60000, 60000]
abschaffen = [0, 0, 0, 0]
m_anschaffen = [0, 0]
tech_increase = [0, 1, 1, 1]
arbeiter = [[2, 2, 20, 6], [4, 4.5, 32, 13], [4, 5, 31, 13], [4, 5, 32, 13]]
werbung = [0, 600, 600, 600]
corporate = [0, 150, 150, 150]
preis = [0, 160, 160, 160]


###

for i in range(1, anzahl+1):
    #Fertigungsbericht
    if(True):
        j = 12
        maschienen_anzahl = sum(m_anschaffen)
        liquidität[i].iloc[11, 1] = 0
        for k in abschaffen:
            if k == 0:
                maschienen_anzahl += 1
                j += 1
            else:
                liquidität[i].iloc[11, 1] += fertigung[i].iloc[j, 5] * fertigung[i].iloc[j, 7] / 100
                fertigung[i].drop(labels=j, axis=0, inplace=True)


        begin_fertigungsanlagen = 12

        while j <= fertigung[0].last_valid_index() and False:
            if fertigung[0].iloc[j, 0] == 'Summe':
                break
            j += 1

        #Fertigungsanlagen
        liquidität[i].iloc[24, 1] = 0
        for m in range(len(m_typ)):
            for k in range(m_anschaffen[m]):
                line = pd.DataFrame({'Fertigungsbericht' : m_typ[m], 'Unnamed: 1' : [periode], 'Unnamed: 2' : m_kaufpreis[m], 'Unnamed: 3' : m_dauer[m],
                    'Unnamed: 4' : m_kaufpreis[m]/m_dauer[m], 'Unnamed: 5' : m_kaufpreis[m], 'Unnamed: 6' : m_fixkosten[m], 'Unnamed: 7' : m_resterlös[m]})
                fertigung[i] = concat([fertigung[i].iloc[:j], line, fertigung[i].iloc[j:]]).reset_index(drop=True)
                liquidität[i].iloc[24, 1] += m_kaufpreis[m]
                j += 1



        ende_fertigungsanlagen = j

        for k in range(begin_fertigungsanlagen, ende_fertigungsanlagen):
            if fertigung[i].iloc[k, 3] > 0:
                fertigung[i].iloc[k, 4] = fertigung[i].iloc[k, 5] / fertigung[i].iloc[k, 3]
                fertigung[i].iloc[k, 5] = fertigung[i].iloc[k, 5] - fertigung[i].iloc[k, 4]
                fertigung[i].iloc[k, 3] -= 1
            else:
                fertigung[i].iloc[k, 4] = 0
        fertigung[i].iloc[ende_fertigungsanlagen, 2] = sum(fertigung[i].iloc[begin_fertigungsanlagen:ende_fertigungsanlagen, 2])
        fertigung[i].iloc[ende_fertigungsanlagen, 4] = sum(fertigung[i].iloc[begin_fertigungsanlagen:ende_fertigungsanlagen, 4])
        fertigung[i].iloc[ende_fertigungsanlagen, 5] = sum(fertigung[i].iloc[begin_fertigungsanlagen:ende_fertigungsanlagen, 5])
        fertigung[i].iloc[ende_fertigungsanlagen, 6] = sum(fertigung[i].iloc[begin_fertigungsanlagen:ende_fertigungsanlagen, 6])

        j = ende_fertigungsanlagen + 5

        for k in abschaffen:
            if k == 0:
                j += 1
            else:
                liquidität[i].iloc[11, 1] += fertigung[i].iloc[j, 5] * fertigung[i].iloc[j, 7] / 100
                fertigung[i].drop(labels=j+1, axis=0, inplace=True)

        while j <= fertigung[0].last_valid_index() and False:
            if fertigung[0].iloc[j, 0] == 'Summe':
                break
            j += 1

        #Kapazität
        for m in range(len(m_typ)):
            for k in range(m_anschaffen[m]):
                line = pd.DataFrame({'Fertigungsbericht' : m_typ[m], 'Unnamed: 1' : [m_kapazität[m]]})
                fertigung[i] = concat([fertigung[i].iloc[:j], line, fertigung[i].iloc[j:]]).reset_index(drop=True)
                j += 1

        ende_kapazität = j
        fertigung[i].iloc[ende_kapazität, 1] = sum(fertigung[i].iloc[ende_fertigungsanlagen + 5:ende_kapazität, 1])

        #Übersicht
        fertigung[i].iloc[3, 2] = plan_produktion[i]
        fertigung[i].iloc[4, 2] = min(max(plan_produktion[i], nachfrage[i] - lager[0].iloc[4, 2]), fertigung[i].iloc[ende_kapazität, 1] / p_kapazität[0], arbeiter[i][2] * a_kapazität[0] * (1+überstunden_max))
        fertigung[i].iloc[6, 2] = fertigung[i].iloc[4, 2]/fertigung[i].iloc[ende_kapazität, 1]
        fertigung[i].iloc[7, 2] = fertigung[i].iloc[4, 2]/(arbeiter[i][2]*a_kapazität[0])

        verkauf = min(fertigung[i].iloc[4, 2] + lager[0].iloc[4, 2], nachfrage[i])

        #Auslastung Fertigungsanlagen
        fertigung[i].iloc[ende_kapazität + 4, 2] = fertigung[i].iloc[3, 2]
        fertigung[i].iloc[ende_kapazität + 5, 2] = fertigung[i].iloc[ende_kapazität, 1]
        fertigung[i].iloc[ende_kapazität + 6, 2] = fertigung[i].iloc[4, 2]
        fertigung[i].iloc[ende_kapazität + 7, 2] = p_kapazität[0]
        fertigung[i].iloc[ende_kapazität + 8, 2] = fertigung[i].iloc[ende_kapazität + 6, 2] * p_kapazität[0]
        fertigung[i].iloc[ende_kapazität + 9, 2] = fertigung[i].iloc[6, 2]

        #Auslastung Mitarbeiter
        fertigung[i].iloc[ende_kapazität + 13, 2] = arbeiter[i][2]
        fertigung[i].iloc[ende_kapazität + 14, 2] = arbeiter[i][2] * (1+überstunden_max)
        fertigung[i].iloc[ende_kapazität + 15, 2] = a_kapazität[0]
        fertigung[i].iloc[ende_kapazität + 16, 2] = plan_produktion[i]
        fertigung[i].iloc[ende_kapazität + 17, 2] = fertigung[i].iloc[4, 2]
        fertigung[i].iloc[ende_kapazität + 18, 2] = fertigung[i].iloc[4, 2] / a_kapazität[0]
        fertigung[i].iloc[ende_kapazität + 19, 2] = fertigung[i].iloc[7, 2]
        #print(fertigung[i])

    #Forschungsbericht
    if True:
        forschung[i].iloc[3, 1] = forschung[0].iloc[3, 2]
        forschung[i].iloc[3, 2] = forschung[0].iloc[3, 2] + tech_increase[i]
        forschung[i].iloc[3, 3] = tech_increase[i] * tech_step_cost
        forschung[i].iloc[3, 4] = forschung[0].iloc[3, 4] + tech_increase[i] * tech_cost_increase
        forschung[i].iloc[3, 5] = forschung[i].iloc[3, 4] * verkauf/1000
        #print(forschung[i])

    #Personalbericht
    if True:
        for j in range(4):
            #Personalbestand
            personal[i].iloc[3, j+2] = personal[0].iloc[7, j+2]
            if personal[i].iloc[3, j+2] - fluktuation[j] <= arbeiter[i][j]:
                personal[i].iloc[4, j+2] = arbeiter[i][j] - personal[i].iloc[3, j+2] + fluktuation[j]
            else:
                personal[i].iloc[5, j+2] = personal[i].iloc[3, j+2] - arbeiter[i][j] - fluktuation[j]
            personal[i].iloc[6, j+2] = fluktuation[j]
            personal[i].iloc[7, j+2] = personal[i].iloc[3, j+2] + personal[i].iloc[4, j+2] - personal[i].iloc[5, j+2] - personal[i].iloc[6, j+2]

            #Personalkosten
            personal[i].iloc[11, j+2] = personal[i].iloc[7, j+2] * lohn[j]
            if j == 2 and fertigung[i].iloc[7, 2] >= 1.0:
                personal[i].iloc[11, j+2] *= (1 + überstunden_kosten * (fertigung[i].iloc[7, 2] - 1))
            personal[i].iloc[12, j+2] = personal[i].iloc[4, j+2] * einstellung + personal[i].iloc[5, j+2] * entlassung
            personal[i].iloc[13, j+2] = (personal[i].iloc[11, j+2] * nebenkosten)/100
            personal[i].iloc[14, j+2] = personal[i].iloc[11, j+2] + personal[i].iloc[12, j+2] + personal[i].iloc[13, j+2]


        for j in chain(range(3, 8), range(11, 15)):
            personal[i].iloc[j, 6] = personal[i].iloc[j, 2] + personal[i].iloc[j, 3] + personal[i].iloc[j, 4] + personal[i].iloc[j, 5]

        personal[i].iloc[18, 1] = nebenkosten
        #print(personal[i])

    #Lager > einsatzstoffe
    if True:
        lager[i].iloc[9, 1] = lager[0].iloc[13, 1]
        lager[i].iloc[9, 2] = lager[0].iloc[13, 2]
        lager[i].iloc[10, 1] = plan_einkauf[i]
        for j in range(len(einkauf_preise)):
            if einkauf_mengen[j] > plan_einkauf[i]:
                lager[i].iloc[10, 2] = einkauf_preise[j]
                break
        lager[i].iloc[11, 1] = max(0, fertigung[i].iloc[4, 2] - lager[i].iloc[10, 1] - lager[i].iloc[9, 1])
        lager[i].iloc[11, 2] = einkauf_jit
        lager[i].iloc[12, 1] = fertigung[i].iloc[4, 2]
        for j in range(9, 12):
            lager[i].iloc[j, 3] = lager[i].iloc[j, 1] * lager[i].iloc[j, 2] / 1000
        lager[i].iloc[13, 1] = lager[i].iloc[9, 1] + lager[i].iloc[10, 1] + lager[i].iloc[11, 1]
        lager[i].iloc[13, 3] = lager[i].iloc[9, 3] + lager[i].iloc[10, 3] + lager[i].iloc[11, 3]
        lager[i].iloc[13, 2] = lager[i].iloc[13, 3] / lager[i].iloc[13, 1] * 1000
        lager[i].iloc[12, 2] = lager[i].iloc[13, 2]
        lager[i].iloc[12, 3] = lager[i].iloc[12, 1] * lager[i].iloc[12, 2] / 1000
        lager[i].iloc[13, 1] = lager[i].iloc[13, 1] - lager[i].iloc[12, 1]
        lager[i].iloc[13, 3] = lager[i].iloc[13, 3] - lager[i].iloc[12, 3]
        
        #print(lager[i].iloc[7:14])

    #Kostenstellenrechnung\Lagerkosten
    if True:
        #Lohnkosten
        k = 7
        kostenstellen[i].iloc[k, 2] = personal[i].iloc[k+4, 2]
        if fertigung[i].iloc[ende_kapazität + 18, 2] < arbeiter[i][2]:
            kostenstellen[i].iloc[k, 3] = arbeiter[i][2] - fertigung[i].iloc[ende_kapazität + 18, 2]
        else:
            kostenstellen[i].iloc[k, 3] = 0
        kostenstellen[i].iloc[k, 5] = personal[i].iloc[k+4, 5]
        kostenstellen[i].iloc[k, 6] = personal[i].iloc[k+4, 3]
        k += 1
        kostenstellen[i].iloc[k, 2] = personal[i].iloc[k+4, 2]
        kostenstellen[i].iloc[k, 3] = personal[i].iloc[k+4, 4]
        kostenstellen[i].iloc[k, 5] = personal[i].iloc[k+4, 5]
        kostenstellen[i].iloc[k, 6] = personal[i].iloc[k+4, 3]
        k += 1
        kostenstellen[i].iloc[k, 2] = personal[i].iloc[k+4, 2]
        kostenstellen[i].iloc[k, 3] = kostenstellen[i].iloc[k-2, 3] * nebenkosten / 100
        kostenstellen[i].iloc[k, 5] = personal[i].iloc[k+4, 5]
        kostenstellen[i].iloc[k, 6] = personal[i].iloc[k+4, 3]

        #Abschreibungen
        #Gebäude bleiben gleich?
        kostenstellen[i].iloc[12, 3] = fertigung[i].iloc[ende_fertigungsanlagen, 4]

        kostenstellen[i].iloc[15, 2:7] = sonstige_fix
        kostenstellen[i].iloc[15, 3] += fertigung[i].iloc[ende_fertigungsanlagen, 6]
        kostenstellen[i].iloc[17, 5] = corporate[i]

        #Lagerkosten fehlen noch
        for k in [2, 3, 4, 6]:
            kostenstellen[i].iloc[20, k] = sum (kostenstellen[i].iloc[[4, 5, 7, 8, 9, 11, 12, 13, 15, 16, 17, 18, 19], k])
        
        #print(kostenstellen[i])

    #Kostenträgerrechnung > Herstellungskosten
    if True:
        k = 3
        kostenträger[i].iloc[k, 3] = lager[i].iloc[12, 3] + betrieb*fertigung[i].iloc[4, 2]/1000
        kostenträger[i].iloc[k + 17, 2] = kostenträger[i].iloc[k, 3]/fertigung[i].iloc[4, 2]*1000
        k += 1
        kostenträger[i].iloc[k, 3] = kostenstellen[i].iloc[20, 2]
        kostenträger[i].iloc[k + 17, 2] = kostenträger[i].iloc[k, 3]/fertigung[i].iloc[4, 2]*1000
        k += 1
        kostenträger[i].iloc[k, 3] = personal[i].iloc[14, 4] - sum(kostenstellen[i].iloc[[7, 9], 3])
        kostenträger[i].iloc[k + 17, 2] = kostenträger[i].iloc[k, 3]/fertigung[i].iloc[4, 2]*1000
        k += 1      #warum zählen genutzte kapazitäten der Maschienen nicht zu einzelkosten, sondern zu gemeinkosten?
        kostenträger[i].iloc[k, 3] = kostenstellen[i].iloc[20, 3]
        kostenträger[i].iloc[k + 17, 2] = kostenträger[i].iloc[k, 3]/fertigung[i].iloc[4, 2]*1000

        k = 7
        kostenträger[i].iloc[k, 3] = sum(kostenträger[i].iloc[range(3, k), 3])
        kostenträger[i].iloc[k + 17, 2] = sum(kostenträger[i].iloc[range(20, 24), 2])
        #print(kostenträger[i].iloc[chain(range(2, 8), range(18, 25))])

    #restlicher Lagerbericht
    if True:
        lager[i].iloc[18, 1] = lager[0].iloc[21, 1]
        lager[i].iloc[18, 3] = lager[0].iloc[21, 3]
        lager[i].iloc[18, 2] = lager[i].iloc[18, 3] / lager[i].iloc[18, 1]
        lager[i].iloc[19, 1] = fertigung[i].iloc[4, 2]
        lager[i].iloc[19, 2] = kostenträger[i].iloc[24, 2]
        lager[i].iloc[19, 3] = lager[i].iloc[19, 1] * lager[i].iloc[19, 2] / 1000
        lager[i].iloc[20, 1] = verkauf
        for j in [1, 3]:
            lager[i].iloc[21, j] = sum(lager[i].iloc[[18, 19], j])
        lager[i].iloc[21, 2] = lager[i].iloc[21, 3] / lager[i].iloc[21, 1] * 1000
        lager[i].iloc[20, 2] = lager[i].iloc[21, 2]
        lager[i].iloc[20, 3] = lager[i].iloc[20, 1] * lager[i].iloc[20, 2] / 1000
        for j in [1, 3]:
            lager[i].iloc[21, j] -= lager[i].iloc[20, j]

        #Lagerkosten
        lager[i].iloc[25, 2] = lagerkosten[0]*lager[i].iloc[13, 1]/1000
        lager[i].iloc[26, 2] = lagerkosten[1]*lager[i].iloc[21, 1]/1000
        lager[i].iloc[27, 2] = sum(lager[i].iloc[[25, 26], 2])

        #Übersicht
        lager[i].iloc[3, 2] = lager[i].iloc[13, 1]
        lager[i].iloc[4, 2] = lager[i].iloc[21, 1]

        #print (lager[i])

    #restliche Kostenstellenrechnung
    if True:
        kostenstellen[i].iloc[16, 5] = lager[i].iloc[27, 2]
        kostenstellen[i].iloc[20, 5] = sum (kostenstellen[i].iloc[[4, 5, 7, 8, 9, 11, 12, 13, 15, 16, 17, 18, 19], 5])
        for j in [4, 5, 7, 8, 9, 11, 12, 13, 15, 16, 17, 18, 19, 20]:
            kostenstellen[i].iloc[j, 1] = sum(kostenstellen[i].iloc[j, range(2, 7)])
        #print(kostenstellen[i])

    #restliche Kostenträgerrechnung
    if True:
        k =8
        kostenträger[i].iloc[k, 3] = lager[i].iloc[18, 3]-lager[i].iloc[21, 3]
        kostenträger[i].iloc[k + 17, 2] = lager[i].iloc[20, 2]
        k += 1
        kostenträger[i].iloc[k, 3] = kostenträger[i].iloc[k-2, 3] + kostenträger[i].iloc[k-1, 3]
        k += 1
        kostenträger[i].iloc[k, 3] = forschung[i].iloc[3, 5]
        kostenträger[i].iloc[k + 16, 2] = forschung[i].iloc[3, 4]
        k += 1
        kostenträger[i].iloc[k, 3] = forschung[i].iloc[3, 3]
        kostenträger[i].iloc[k + 16, 2] = kostenträger[i].iloc[k, 3]/verkauf*1000
        k += 1
        kostenträger[i].iloc[k, 3] = werbung[i] + transport*verkauf/1000
        kostenträger[i].iloc[k + 16, 2] = kostenträger[i].iloc[k, 3]/verkauf*1000
        k += 1
        kostenträger[i].iloc[k, 3] = kostenstellen[i].iloc[20, 5]
        kostenträger[i].iloc[k + 16, 2] = kostenträger[i].iloc[k, 3]/verkauf*1000
        #gibt es einzelkosten in der verwaltung?
        k += 2
        kostenträger[i].iloc[k, 3] = kostenstellen[i].iloc[20, 6]
        kostenträger[i].iloc[k + 16, 2] = kostenträger[i].iloc[k, 3]/verkauf*1000
        
        #Selbstkosten
        kostenträger[i].iloc[16, 3] = sum(kostenträger[i].iloc[range(9, 16), 3])
        kostenträger[i].iloc[32, 2] = sum(kostenträger[i].iloc[range(25, 32), 2])

        for j in range(3, 17):
            kostenträger[i].iloc[j, 2] = sum(kostenträger[i].iloc[j, 3:])

        #print(kostenträger[i].iloc[2:33])

    #Gewinn- und Verlustrechnung
    if True:
        gewinn[i].iloc[17, 1] = verkauf * preis[i]/1000
        gewinn[i].iloc[19, 1] = kostenträger[i].iloc[9, 2]
        gewinn[i].iloc[20, 1] = kostenträger[i].iloc[10, 2] + kostenträger[i].iloc[11, 2]
        gewinn[i].iloc[21, 1] = kostenträger[i].iloc[12, 2] + kostenträger[i].iloc[13, 2]
        gewinn[i].iloc[22, 1] = kostenträger[i].iloc[14, 2] + kostenträger[i].iloc[15, 2]

        #Betriebsergebnis
        gewinn[i].iloc[23, 1] = sum(gewinn[i].iloc[[17, 18], 1]) - sum(gewinn[i].iloc[range(19, 23), 1])


        #print(gewinn[i].iloc[16:])

    #Liquiditätsrechnung
    if True:
        liquidität[i].iloc[3, 1] = liquidität[0].iloc[32, 1]
        #Einzahlungen
        liquidität[i].iloc[7, 1] = gewinn[i].iloc[17, 1] * einzahlung[1] / 100
        liquidität[i].iloc[8, 1] = gewinn[0].iloc[17, 1] * (100-einzahlung[0]) / 100
        #desinvestitionen werden oben gemacht

 
        #Auszahlungen
        liquidität[i].iloc[18, 1] = kostenträger[i].iloc[3, 2] * auszahlung
        liquidität[i].iloc[19, 1] = kostenträger[0].iloc[3, 2] * (1-auszahlung)
        liquidität[i].iloc[20, 1] = personal[i].iloc[14, 6]
        liquidität[i].iloc[21, 1] = sum(kostenträger[i].iloc[range(10, 13), 2]) + sum(kostenstellen[i].iloc[[15, 17], 1])
        liquidität[i].iloc[22, 1] = liquidität[0].iloc[13, 1]
        liquidität[i].iloc[23, 1] = bilanz[0].iloc[11, 4] * zinsen[1] / 100

        gewinn[i].iloc[27, 1] = gewinn[i].iloc[23, 1]
        gewinn[i].iloc[30, 1] = liquidität[i].iloc[23, 1]

        summe = sum(liquidität[i].iloc[range(7, 13), 1]) - sum(liquidität[i].iloc[range(18, 26), 1])

        if summe >= (gewinn[i].iloc[23, 1] - liquidität[i].iloc[23, 1]) * steuern/100:
            gewinn[i].iloc[31, 1] = 0
            liquidität[i].iloc[13, 1] = 0
        else:
            end = (summe - (gewinn[i].iloc[27, 1] + gewinn[i].iloc[30, 1]) * steuern/100) / (1 + steuern * zinsen[0] / 10000)
            liquidität[i].iloc[13, 1] = -end
            gewinn[i].iloc[31, 1] = -end * zinsen[0]/100
            
        liquidität[i].iloc[14, 1] = sum(liquidität[i].iloc[7:14, 1])
        gewinn[i].iloc[28, 1] = gewinn[i].iloc[29, 1] - gewinn[i].iloc[30, 1] - gewinn[i].iloc[31, 1]
        gewinn[i].iloc[32, 1] = gewinn[i].iloc[27, 1] - sum(gewinn[i].iloc[[30, 31], 1])
        print(gewinn[i].iloc[32, 1], gewinn[i].iloc[27, 1], sum(gewinn[i].iloc[[30, 31], 1]))
        gewinn[i].iloc[33, 1] = max(gewinn[i].iloc[32, 1] * steuern / 100, 0)
        liquidität[i].iloc[27, 1] = gewinn[i].iloc[33, 1]
        gewinn[i].iloc[34, 1] = gewinn[i].iloc[32, 1] - gewinn[i].iloc[33, 1]
        liquidität[i].iloc[28, 1] = sum(liquidität[i].iloc[18:28, 1])

        
        #print(liquidität[i])
        #print(gewinn[i].iloc[16:])

    print(gewinn[i].iloc[17:35])
    print(liquidität[i])

    print()
    print()

    #Fertig:
    #Fertigungsbericht
    #Forschungsbericht
    #Personalbericht
    #Lagerbericht
    #Kostenstellenrechnung
    #Kostenträgerrechnung 

    #Noch machen:
    #Gewinn- und Verlustrechnung
    #Liquiditätsrechnung
    #Cashflow statement
    #Bilanz
    #Executive Summary
    #Deckungsbeitragrechnung
    #Kostenartenrechnung
