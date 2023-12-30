# -*- coding: UTF-8 -*-
from datetime import date
import json
import termtables as tt
import SaveToJson
import os.path
if not os.path.exists("plan.json"):
    print("Nie wykryto pliku! Automatyczna synchronizacja...")
    SaveToJson.saveToJson()
if not os.path.exists("plan.json"):
    print("Błąd synchronizacji, brak pliku, koniec programu")
def whichDayOfWeek(givenDayOfWeek):
    if givenDayOfWeek == 0:
        givenDayOfWeek = "Poniedziałek"
    elif givenDayOfWeek == 1:
        givenDayOfWeek = "Wtorek"
    elif givenDayOfWeek == 2:
        givenDayOfWeek = "Środa"
    elif givenDayOfWeek == 3:
        givenDayOfWeek = "Czwartek"
    elif givenDayOfWeek == 4:
        givenDayOfWeek = "Piątek"
    elif givenDayOfWeek == 5:
        givenDayOfWeek = "Sobota"
    elif givenDayOfWeek == 6:
        givenDayOfWeek = "Niedziela"
    return str(givenDayOfWeek)


def whichMonth(whichMonth):
    whichMonth = int(whichMonth)
    if whichMonth == 1:
        whichMonth = "Styczeń"
    elif whichMonth == 2:
        whichMonth = "Luty"
    elif whichMonth == 3:
        whichMonth = "Marzec"
    elif whichMonth == 4:
        whichMonth = "Kwiecień"
    elif whichMonth == 5:
        whichMonth = "Maj"
    elif whichMonth == 6:
        whichMonth = "Czerwiec"
    elif whichMonth == 7:
        whichMonth = "Lipiec"
    elif whichMonth == 8:
        whichMonth = "Sierpień"
    elif whichMonth == 9:
        whichMonth = "Wrzesień"
    elif whichMonth == 10:
        whichMonth = "Październik"
    elif whichMonth == 11:
        whichMonth = "Listopad"
    elif whichMonth == 12:
        whichMonth = "Grudzień"
    else:
        whichMonth = "miesiac"
    return str(whichMonth)


def nicelyDisplayDay(jsonData, selectedGroup, year, month, day):
    print("\n")
    maxLength = 47
    dayOfWeek = whichDayOfWeek(date(int(year), int(month), int(day)).weekday())
    monthName = whichMonth(date(int(year), int(month), int(day)).month)
    table = []
    dateAsString = str(dayOfWeek + ", " + day + " " + monthName + " " + year)
    header = [selectedGroup, dateAsString]
    previousDay = jsonData[year][month][day]["08:15-09:45"][selectedGroup]
    subject = previousDay["Przedmiot"]
    if maxLength > len(subject):
        for i in range(maxLength - len(subject)):
            subject += " "
    previousHour = "09:45"
    row = ["08:15", subject]
    table.append(row)
    tt.print(
        table,
        header=header,
        padding=(0, 1),
        style=tt.styles.markdown
    )
    skipFirst = True
    for hour, data in jsonData[year][month][day].items():
        if skipFirst:
            skipFirst = False
            continue
        roomLecturer = previousDay["Sala"] + " " + previousDay["Wykladowca"]
        previousDay = data[selectedGroup]
        if maxLength > len(roomLecturer):
            for i in range(maxLength - len(roomLecturer)):
                roomLecturer += " "
        header = [previousHour, roomLecturer]
        previousHour = hour[-5:]
        table = []
        subject = data[selectedGroup]["Przedmiot"]
        if maxLength > len(subject):
            for i in range(maxLength - len(subject)):
                subject += " "
        row = [hour[:5], subject]
        table.append(row)
        tt.print(
            table,
            header=header,
            padding=(0, 1),
            style=tt.styles.markdown
        )
    roomLecturer = previousDay["Sala"] + " " + previousDay["Wykladowca"]
    if maxLength > len(roomLecturer):
        for i in range(maxLength - len(roomLecturer)):
            roomLecturer += " "
    header = [previousHour, roomLecturer]
    table = []
    row = [selectedGroup, "Koniec zajęć"]
    table.append(row)
    tt.print(
        table,
        header=header,
        padding=(0, 1),
        style=tt.styles.markdown
    )
    return "\n"


def poorlyDisplayDay(dataOfTheDay, year, month, day):
    table = []
    dayOfWeek = whichDayOfWeek(date(int(year), int(month), int(day)).weekday())
    monthName = whichMonth(month)
    header = [dayOfWeek + ", " + day + " " + monthName + " " + year, "Przedmiot", "Wykladowca", "Sala",
              "Przedmiot", "Wykladowca", "Sala", "Przedmiot", "Wykladowca", "Sala", "Przedmiot", "Wykladowca", "Sala", "Przedmiot", "Wykladowca", "Sala", "Przedmiot", "Wykladowca", "Sala", "Przedmiot", "Wykladowca", "Sala", "Przedmiot", "Wykladowca", "Sala"]
    row = ["Grupa", "1(1)", "1(1)", "1(1)", "1(2)", "1(2)", "1(2)", "2(1)", "2(1)", "2(1)", "2(2)", "2(2)", "2(2)", "3(1)", "3(1)", "3(1)", "3(2)", "3(2)", "3(2)", "4(1)", "4(1)", "4(1)", "4(2)", "4(2)", "4(2)"]
    table.append(row)
    for hours, values in dataOfTheDay.items():
        row = [hours, values["1(1)"]["Przedmiot"], values["1(1)"]["Wykladowca"],
               values["1(1)"]["Sala"],
               values["1(2)"]["Przedmiot"], values["1(2)"]["Wykladowca"], values["1(2)"]["Sala"],
               values["2(1)"]["Przedmiot"], values["2(1)"]["Wykladowca"],
               values["2(1)"]["Sala"], values["2(2)"]["Przedmiot"], values["2(2)"]["Wykladowca"],
               values["2(2)"]["Sala"],
               values["3(1)"]["Przedmiot"], values["3(1)"]["Wykladowca"], values["3(1)"]["Sala"],
               values["3(2)"]["Przedmiot"],
               values["3(2)"]["Wykladowca"], values["3(2)"]["Sala"], values["4(1)"]["Przedmiot"],
               values["4(1)"]["Wykladowca"],
               values["4(1)"]["Sala"], values["4(2)"]["Przedmiot"], values["4(2)"]["Wykladowca"],
               values["4(2)"]["Sala"]]
        table.append(row)
    tt.print(
        table,
        header=header,
        padding=(0, 1)
    )
    return "\n"


f = open('plan.json', "r")
jsonData = json.loads(f.read())
f.close()
group = " "
while True:
    print('PLAN LEKCJI 1 SEMESTR' + group + 'KIERUNEK INFORMATYKA COLLEGIUM WITELONA')
    print("1: Wybierz grupe")
    print("2: Plan lekcji na dziś")
    print("3: Plan lekcji na konkretny dzień")
    print("4: Plan lekcji na cały semestr")
    print("5: Zsynchronizuj plan lekcji ze strony")
    print("6: Wyjście")
    answer = input()
    if answer == "1":
        while True:
            print("Dostępne opcje:")
            print("1(1)")
            print("1(2)")
            print("2(1)")
            print("2(2)")
            print("3(1)")
            print("3(2)")
            print("4(1)")
            print("4(2)")
            print("r: Reset grupy")
            answer = input()
            if answer == "1(1)":
                group = " GRUPA 1(1) "
                break
            elif answer == "1(2)":
                group = " GRUPA 1(2) "
                break
            elif answer == "2(1)":
                group = " GRUPA 2(1) "
                break
            elif answer == "2(2)":
                group = " GRUPA 2(2) "
                break
            elif answer == "3(1)":
                group = " GRUPA 3(1) "
                break
            elif answer == "3(2)":
                group = " GRUPA 3(2) "
                break
            elif answer == "4(1)":
                group = " GRUPA 4(1) "
                break
            elif answer == "4(2)":
                group = " GRUPA 4(2) "
                break
            elif answer == "r":
                print("Grupa zresetowana!")
                group = " "
                break
            else:
                print("Nie ma takiej grupy!")
    elif answer == "2" or answer == "3":
        if answer == "2":
            currentYear = str(date.today().year)
        else:
            currentYear = input("Proszę podać rok:")
        if len(currentYear) < 4:
            currentYear = "20"+currentYear
        if currentYear not in jsonData:
            print("Brak danych o planie z tego roku! Wykracza on poza semestr!")
            continue
        if answer == "2":
            currentMonth = str(date.today().month)
        else:
            currentMonth = input("Proszę podać miesiac:")
        if len(currentMonth) < 2:
            currentMonth = "0"+currentMonth
        if currentMonth not in jsonData[currentYear]:
            print("Brak danych o planie z tego miesiaca! W tym miesiącu nie ma zajęć, bądź wykracza on poza ten semestr")
            continue
        if answer == "2":
            currentDay = str(date.today().day)
        else:
            currentDay = input("Proszę podać dzien:")
        if len(currentDay) < 2:
            currentDay = "0"+currentDay
        if currentDay not in jsonData[currentYear][currentMonth]:
            print("W tym dniu nie ma zajęć!")
            continue
        if group != " ":
            print(nicelyDisplayDay(jsonData, group[-5:-1], currentYear, currentMonth, currentDay))
        else:
            print(poorlyDisplayDay(jsonData[currentYear][currentMonth][currentDay], currentYear, currentMonth, currentDay))
    elif answer == "4":
        for years, yearValues in jsonData.items():
            for months, monthValues in yearValues.items():
                for days, dayValues in monthValues.items():
                    if group != " ":
                        print(nicelyDisplayDay(jsonData, group[-5:-1], years, months, days))
                    else:
                        print(poorlyDisplayDay(dayValues, years, months, days))
        print("TO BYŁA TABELKA DLA" + group)
    elif answer == "5":
        print("to może chwilę potrwać...")
        SaveToJson.saveToJson()
    elif answer == "6":
        print("Miłego dnia!")
        break
    else:
        print("Nie ma takiej opcji!")
