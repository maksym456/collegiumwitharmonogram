import requests
from lxml import etree
import json


def saveToJson():
    print('Łączenie ze stroną "http://www.plan.pwsz.legnica.edu.pl/checkSpecjalnoscStac.php?specjalnosc=s1INF"...')
    apiUrl = "http://www.plan.pwsz.legnica.edu.pl/checkSpecjalnoscStac.php?specjalnosc=s1INF"
    response = requests.get(apiUrl)
    if response.ok:
        print("Błąd połączenia! koniec funkcji")
        return
    print('Połączono!')
    print('Pobieranie danych do zmiennej...')
    fullHtml = response.text
    htmlTree = etree.HTML(fullHtml)
    xpathBase = '/html/body/table[1]/div[2]/'
    groupedDates = {}
    print('Dane pobrane')
    print('Parsowanie danych...')
    for week in range(15):
        for day in range(8):
            data = htmlTree.xpath(xpathBase + 'tr[1]/td/text()')
            if len(data) == 0:
                xpathBase = xpathBase[:-10]
                xpathBase += '2]/'
                break
            else:
                hourData = {}
                for row in range(7):
                    tableData = htmlTree.xpath(xpathBase + 'tr[' + str(row + 4) + ']/td/text()')
                    lesson = [
                        {"Przedmiot": tableData[1], "Wykladowca": tableData[2], "Sala": tableData[3]},
                        {"Przedmiot": tableData[4], "Wykladowca": tableData[5], "Sala": tableData[6]},
                        {"Przedmiot": tableData[7], "Wykladowca": tableData[8], "Sala": tableData[9]},
                        {"Przedmiot": tableData[10], "Wykladowca": tableData[11], "Sala": tableData[12]},
                        {"Przedmiot": tableData[13], "Wykladowca": tableData[14], "Sala": tableData[15]},
                        {"Przedmiot": tableData[16], "Wykladowca": tableData[17], "Sala": tableData[18]},
                        {"Przedmiot": tableData[19], "Wykladowca": tableData[20], "Sala": tableData[21]},
                        {"Przedmiot": tableData[22], "Wykladowca": tableData[23], "Sala": tableData[24]}]
                    group = {
                        "1(1)": lesson[0], "1(2)": lesson[1], "2(1)": lesson[2], "2(2)": lesson[3], "3(1)": lesson[4],
                        "3(2)": lesson[5], "4(1)": lesson[6], "4(2)": lesson[7]}
                    hourData[tableData[0]] = group
                xpathBase += 'div[1]/'
                year = data[0][-10:-6]
                month = data[0][-5:-3]
                day = data[0][-2::]
                if year not in groupedDates:
                    groupedDates[year] = {}
                if month not in groupedDates[year]:
                    groupedDates[year][month] = {}
                groupedDates[year][month][day] = hourData
    print('Dane zparsowane')
    print('Zapisywanie do pliku...')
    with open("plan.json", "w") as file:
        json.dump(groupedDates, file)
    print('Zapisano')
    print('Zamykanie pliku...')
    file.close()
    print('Plik zamknięty, koniec funkcji')
