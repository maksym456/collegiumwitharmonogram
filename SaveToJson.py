def savetojson():
    import requests
    from lxml import etree
    import json

    print('Łączenie ze stroną "http://www.plan.pwsz.legnica.edu.pl/checkSpecjalnoscStac.php?specjalnosc=s1INF"...')
    api_url = "http://www.plan.pwsz.legnica.edu.pl/checkSpecjalnoscStac.php?specjalnosc=s1INF"
    response = requests.get(api_url)
    print('Połączono!')
    print('Pobieranie danych do zmiennej...')
    fullhtml = response.text
    tree = etree.HTML(fullhtml)
    path = '/html/body/table[1]/div[2]/'
    grouped_dates = {}
    print('Dane pobrane')
    print('Parsowanie danych...')
    for tygodnie in range(15):
        for dni in range(8):
            dane = tree.xpath(path + 'tr[1]/td/text()')
            if len(dane) == 0:
                path = path[:-10]
                path += '2]/'
                break
            else:
                godzina = {}
                for row in range(7):
                    table = tree.xpath(path + 'tr[' + str(row + 4) + ']/td/text()')
                    lekcja = [
                        {"Przedmiot": table[1], "Wykladowca": table[2], "Sala": table[3]},
                        {"Przedmiot": table[4], "Wykladowca": table[5], "Sala": table[6]},
                        {"Przedmiot": table[7], "Wykladowca": table[8], "Sala": table[9]},
                        {"Przedmiot": table[10], "Wykladowca": table[11], "Sala": table[12]},
                        {"Przedmiot": table[13], "Wykladowca": table[14], "Sala": table[15]},
                        {"Przedmiot": table[16], "Wykladowca": table[17], "Sala": table[18]},
                        {"Przedmiot": table[19], "Wykladowca": table[20], "Sala": table[21]},
                        {"Przedmiot": table[22], "Wykladowca": table[23], "Sala": table[24]}]
                    grupa = {
                        "1(1)": lekcja[0], "1(2)": lekcja[1], "2(1)": lekcja[2], "2(2)": lekcja[3], "3(1)": lekcja[4],
                        "3(2)": lekcja[5], "4(1)": lekcja[6], "4(2)": lekcja[7]}
                    godzina[table[0]] = grupa
                path += 'div[1]/'
                rok = dane[0][-10:-6]
                miesiac = dane[0][-5:-3]
                dzien = dane[0][-2::]
                if rok not in grouped_dates:
                    grouped_dates[rok] = {}
                if miesiac not in grouped_dates[rok]:
                    grouped_dates[rok][miesiac] = {}
                grouped_dates[rok][miesiac][dzien] = godzina
    print('Dane zparsowane')
    print('Zapisywanie do pliku...')
    with open("plan.json", "w") as outfile:
        json.dump(grouped_dates, outfile)
    print('Zapisano')
    print('Zamykanie pliku...')
    outfile.close()
    print('Plik zamknięty, koniec funkcji')
