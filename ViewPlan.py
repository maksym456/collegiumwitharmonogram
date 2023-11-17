# -*- coding: UTF-8 -*-
from datetime import date
import json
import termtables as tt
import SaveToJson
import os.path
if not os.path.exists("plan.json"):
    print("Nie wykryto pliku! Automatyczna synchronizacja...")
    SaveToJson.savetojson()
def ktorydzientygodnia(danydzientygodnia):
    if danydzientygodnia==0:
        danydzientygodnia="Poniedziałek"
    elif danydzientygodnia==1:
        danydzientygodnia="Wtorek"
    elif danydzientygodnia==2:
        danydzientygodnia="Środa"
    elif danydzientygodnia==3:
        danydzientygodnia="Czwartek"
    elif danydzientygodnia==4:
        danydzientygodnia="Piątek"
    elif danydzientygodnia==5:
        danydzientygodnia="Sobota"
    elif danydzientygodnia==6:
        danydzientygodnia="Niedziela"
    return str(danydzientygodnia)
def ktorymiesiac(ktorytomiesiac):
    ktorytomiesiac=int(ktorytomiesiac)
    if ktorytomiesiac==1:
        ktorytomiesiac="Styczeń"
    elif ktorytomiesiac==2:
        ktorytomiesiac="Luty"
    elif ktorytomiesiac==3:
        ktorytomiesiac="Marzec"
    elif ktorytomiesiac==4:
        ktorytomiesiac="Kwiecień"
    elif ktorytomiesiac==5:
        ktorytomiesiac="Maj"
    elif ktorytomiesiac==6:
        ktorytomiesiac="Czerwiec"
    elif ktorytomiesiac==7:
        ktorytomiesiac="Lipiec"
    elif ktorytomiesiac==8:
        ktorytomiesiac="Sierpień"
    elif ktorytomiesiac==9:
        ktorytomiesiac="Wrzesień"
    elif ktorytomiesiac==10:
        ktorytomiesiac="Październik"
    elif ktorytomiesiac==11:
        ktorytomiesiac="Listopad"
    elif ktorytomiesiac==12:
        ktorytomiesiac="Grudzień"
    else:
        ktorytomiesiac="miesiac"
    return str(ktorytomiesiac)
def ladniewyswietldzien(calyjson,wybranagrupa,rok,miesiac,dzien):
    print("\n")
    maxdlugosc=47
    dzientygodnia=ktorydzientygodnia(date(int(rok),int(miesiac),int(dzien)).weekday())
    nazwamiesiaca=ktorymiesiac(date(int(rok),int(miesiac),int(dzien)).month)
    tabelka=[]
    datajakas=str(dzientygodnia+", "+dzien+" "+nazwamiesiaca+" "+rok)
    header=[wybranagrupa,datajakas]
    previousday=calyjson[rok][miesiac][dzien]["08:15-09:45"][wybranagrupa]
    przedmiot=previousday["Przedmiot"]
    if maxdlugosc > len(przedmiot):
        for i in range(maxdlugosc-len(przedmiot)):
            przedmiot+=" "
    previoushour="09:45"
    row=["08:15",przedmiot]
    tabelka.append(row)
    tt.print(
        tabelka,
        header=header,
        padding=(0,1),
        style=tt.styles.markdown
    )
    skipfirst=True
    for godzina,dane in calyjson[rok][miesiac][dzien].items():
        if skipfirst:
            skipfirst=False
            continue
        salawykladowca=previousday["Sala"]+" "+previousday["Wykladowca"]
        previousday=dane[wybranagrupa]
        if maxdlugosc > len(salawykladowca):
            for i in range(maxdlugosc-len(salawykladowca)):
                salawykladowca+=" "
        header=[previoushour,salawykladowca]
        previoushour=godzina[-5:]
        tabelka=[]
        przedmiot=dane[wybranagrupa]["Przedmiot"]
        if maxdlugosc > len(przedmiot):
            for i in range(maxdlugosc-len(przedmiot)):
                przedmiot+=" "
        row=[godzina[:5],przedmiot]
        tabelka.append(row)
        tt.print(
            tabelka,
            header=header,
            padding=(0,1),
            style=tt.styles.markdown
        )
    salawykladowca=previousday["Sala"]+" "+previousday["Wykladowca"]
    if maxdlugosc > len(salawykladowca):
        for i in range(maxdlugosc-len(salawykladowca)):
            salawykladowca+=" "
    header=[previoushour,salawykladowca]
    tabelka=[]
    row=[wybranagrupa,"Koniec zajęć"]
    tabelka.append(row)
    tt.print(
        tabelka,
        header=header,
        padding=(0,1),
        style=tt.styles.markdown
    )
    return "\n"
def brzydkowyswietldzien(daneztegodnia,rok,miesiac,dzien):
    tabelka=[]
    dzientygodnia=ktorydzientygodnia(date(int(rok),int(miesiac),int(dzien)).weekday())
    nazwamiesiaca=ktorymiesiac(miesiac)
    header=[dzientygodnia+", "+dzien+" "+nazwamiesiaca+" "+rok,"Przedmiot","Wykladowca","Sala","Przedmiot",
        "Wykladowca","Sala","Przedmiot",
        "Wykladowca",
        "Sala","Przedmiot","Wykladowca","Sala","Przedmiot","Wykladowca","Sala","Przedmiot",
        "Wykladowca",
        "Sala",
        "Przedmiot","Wykladowca","Sala","Przedmiot","Wykladowca","Sala"]
    row=["Grupa","1(1)","1(1)","1(1)",
        "1(2)","1(2)","1(2)",
        "2(1)","2(1)",
        "2(1)","2(2)","2(2)","2(2)",
        "3(1)","3(1)","3(1)","3(2)",
        "3(2)","3(2)","4(1)","4(1)",
        "4(1)","4(2)","4(2)","4(2)"]
    tabelka.append(row)
    for godziny,wartosci in daneztegodnia.items():
        row=[godziny,wartosci["1(1)"]["Przedmiot"],wartosci["1(1)"]["Wykladowca"],
            wartosci["1(1)"]["Sala"],
            wartosci["1(2)"]["Przedmiot"],wartosci["1(2)"]["Wykladowca"],wartosci["1(2)"]["Sala"],
            wartosci["2(1)"]["Przedmiot"],wartosci["2(1)"]["Wykladowca"],
            wartosci["2(1)"]["Sala"],wartosci["2(2)"]["Przedmiot"],wartosci["2(2)"]["Wykladowca"],
            wartosci["2(2)"]["Sala"],
            wartosci["3(1)"]["Przedmiot"],wartosci["3(1)"]["Wykladowca"],wartosci["3(1)"]["Sala"],
            wartosci["3(2)"]["Przedmiot"],
            wartosci["3(2)"]["Wykladowca"],wartosci["3(2)"]["Sala"],wartosci["4(1)"]["Przedmiot"],
            wartosci["4(1)"]["Wykladowca"],
            wartosci["4(1)"]["Sala"],wartosci["4(2)"]["Przedmiot"],wartosci["4(2)"]["Wykladowca"],
            wartosci["4(2)"]["Sala"]]
        tabelka.append(row)
    tt.print(
        tabelka,
        header=header,
        padding=(0,1)
    )
    return "\n"
f=open('plan.json',"r")
data=json.loads(f.read())
f.close()
grupa=" "
while True:
    print('PLAN LEKCJI 1 SEMESTR'+grupa+'KIERUNEK INFORMATYKA COLLEGIUM WITELONA')
    print("1: Wybierz grupe")
    print("2: Plan lekcji na dziś")
    print("3: Plan lekcji na konkretny dzień")
    print("4: Plan lekcji na cały semestr")
    print("5: Zsynchronizuj plan lekcji ze strony")
    print("6: Wyjście")
    ans=input()
    if ans=="1":
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
            ans=input()
            if ans=="1(1)":
                grupa=" GRUPA 1(1) "
                break
            elif ans=="1(2)":
                grupa=" GRUPA 1(2) "
                break
            elif ans=="2(1)":
                grupa=" GRUPA 2(1) "
                break
            elif ans=="2(2)":
                grupa=" GRUPA 2(2) "
                break
            elif ans=="3(1)":
                grupa=" GRUPA 3(1) "
                break
            elif ans=="3(2)":
                grupa=" GRUPA 3(2) "
                break
            elif ans=="4(1)":
                grupa=" GRUPA 4(1) "
                break
            elif ans=="4(2)":
                grupa=" GRUPA 4(2) "
                break
            elif ans=="r":
                print("Grupa zresetowana!")
                grupa=" "
                break
            else:
                print("Nie ma takiej grupy!")
    elif ans=="2"or ans=="3":
        if ans == "2":
            danyrok=str(date.today().year)
        else:
            danyrok=input("Proszę podać rok:")
        if danyrok not in data:
            print("Brak danych o planie z tego roku! Wykracza on poza semestr!")
        if ans == "2":
            danymiesiac=str(date.today().month)
        else:
            danymiesiac=input("Proszę podać miesiac:")
        if danymiesiac not in data[danyrok]:
            print("Brak danych o planie z tego miesiaca! W tym miesiącu nie ma zajęć, bądź wykracza on poza ten semestr")
        if ans == "2":
            danydzien=str(date.today().day)
        else:
            danydzien=input("Proszę podać dzien:")
        if danydzien not in data[danyrok][danymiesiac]:
            print("W tym dniu nie ma zajęć!")
        if grupa!=" ":
            print(ladniewyswietldzien(data,grupa[-5:-1],danyrok,danymiesiac,danydzien))
        else:
            print(brzydkowyswietldzien(data[danyrok][danymiesiac][danydzien],danyrok,danymiesiac,danydzien))
    elif ans=="4":
        for lata,wartoscilat in data.items():
            for miesiace,wartoscimiesiecy in wartoscilat.items():
                for dni,wartoscidni in wartoscimiesiecy.items():
                    if grupa!=" ":
                        print(ladniewyswietldzien(data,grupa[-5:-1],lata,miesiace,dni))
                    else:
                        print(brzydkowyswietldzien(wartoscidni,lata,miesiace,dni))
        print("TO BYŁA TABELKA DLA"+grupa)
    elif ans=="5":
        print("to może chwilę potrwać...")
        SaveToJson.savetojson()
        print('Zakończono! Plik "plan.json" został zaktualizowany!')
    elif ans=="6":
        print("Miłego dnia!")
        break
    else:
      print("Nie ma takiej opcji!")