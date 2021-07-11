# ["a","b","c","d","e","f"]
# ["ac","ca", "ae","ea", "ce","ec", "ab","ba", "ef","fe", "bf","fb", "bd","db", "df","fd"]
# [1,1,5,5,2,2,3,3,4,4,6,6,1,1,1,1]

"""
                     3
        (a)-----------------(b)
     1 /  |                  |  \1
      /   |                  |   \
     (c)  | 5               6|   (d)
      \   |                  |   /
     2 \  |         4        |  /1
        (e)------------------(f)

        a - b - d - f - d - b - f - e - c - a - c - e - a
"""
import ast
import copy
import math
import random


def funkcjaCelu(rozwiazanie, punkt, odcinki, dlugosci):
    suma = 0
    tmp = []
    try:
        for i in range(0, len(rozwiazanie), 1): # na podstawie kolejności odwiedzanych punktów przydzieliłam pasujące do nich odcinki
            odc = punkt[rozwiazanie[i] - 1] + punkt[rozwiazanie[i + 1] - 1]
            # print(odc)
            tmp.append(odc)      # wszystkie odcinki znajdują się w tablicy tmp
    except IndexError:
        pass
    # print(tmp)
    for x in range(0, len(tmp), 1):     # dodajemy długości odcinków na podstawie tablicy tmp
        for y in range(0, len(odcinki), 1):
            if tmp[x] == odcinki[y]:
                suma += dlugosci[y]
    return suma


def generowanieLosowejKolejnoci(wielkosc_rozw, punkty, odcinki):
    losowa_kolejnosc = [1]    #tablica zaczyna się domyślnie od punktu startu a=1
    for k in range(0, wielkosc_rozw - 1, 1):
        punkt = punkty[losowa_kolejnosc[-1] - 1] #zmienna posiada informacje punktu w którym się znajdujemy
        kolejne_wierzch = []
        #print(punkt)
        for i in range(0, len(odcinki), 1):   #petla wyznacza kolejne wierzchołki
            if odcinki[i][:1] == punkt:
                kolejne_wierzch.append(odcinki[i][1:])
        #print(kolejne_wierzch)
        p = int(random.uniform(0, len(kolejne_wierzch))) #losujemy liczbę o wielkości tablicy w której znajdują się dostępne wierzchołki
        # print(kolejne_wierzch[p])
        # print(punkty)
        for j in range(0, len(punkty), 1):
            if punkty[j] == kolejne_wierzch[p]:  # dodajemy wylosowany wierzchołek do kolejki
                losowa_kolejnosc.append(j + 1)
        #print(losowa_kolejnosc)
    return losowa_kolejnosc


def losoweProbkowanie(cel):
    max_dl_roz = len(odcinki)  # maksymalny rozmiar rozwiązania
    min_dl_roz = int((len(odcinki) / 2) - 1)  # najmniejszy rozmiar rozwiązania
    iteracje = 1000  # ilość literacji
    tablica = []  # lista punktów odwiedzanych w proponowanym rozwiązaniu
    najlepszy_wynik = [1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1] #jeśli nie znjdzie rozwiązania wyświetli ten wynik
    while max_dl_roz >= min_dl_roz:  # pętla while zmieniająca rozmiar rozwiązania
        for j in range(0, iteracje, 1):
            nowe_roz = generowanieLosowejKolejnoci(max_dl_roz, punkty, odcinki) # tworzymy potecjalne rozwiązanie
            # print(nowe_roz)
            for k in range(1, len(punkty) + 1): #sprawdzam czy wszystkie punkty podanego rozwiązania zostały odwiedzone
                odw_ptk = k in nowe_roz
                #print(k, odw_ptk)
                if odw_ptk:
                    tablica.append(k)   #zwracam do tablicy True jeśli punkt został odwiedzony
            if (len(tablica) >= len(punkty)) and \
                    (nowe_roz[0] == nowe_roz[len(nowe_roz) - 1]) and \
                    cel(nowe_roz) <= cel(najlepszy_wynik):  # warunek czy wszystkie punkty zostały odwiedzone, start = koniec, wynik lepszy od bieżącego
                # print("rozwiązanie wynosi :", cel(nowe_roz))
                najlepszy_wynik = nowe_roz   #wartość zgodna z warunkami nadpisuje bierzący
                # print("nowy rozwiązaniem jest sekwencja :", najlepszy_wynik)
            # print("odwiedzone punkty", tablica)
            tablica = []

        max_dl_roz -= 1
    return najlepszy_wynik


def losowySasiad(roz, punkty, odcinki):
    dl_max_roz = len(roz)   # maks. dł. rozwiązania
    # print("długść tablicy ", dl_max_roz)
    # print("rozwiązanie", roz)
    ptk = int(random.randint(0, len(roz) - 1)) #losuje ptk z zakresu rozwiązania
    # print("wylosowana liczba", ptk)
    # print("miejsce tablicy z indeksem wylo. liczby", roz[ptk])
    del roz[ptk + 1:]   # kasuję tablice od wybranego ptk
    # print("po usunięciu", roz)
    for k in range(len(roz), dl_max_roz, 1):
        punkt = punkty[roz[-1] - 1] #sprawdzam ptk z konca skasowanej tablicy
        # print(punkt)
        kolejne_wierzch = []
        # print(punkt)
        for i in range(0, len(odcinki), 1):  # wyznaczam dostępne wierzchołki na podst. ptk z końca tablicy
            if odcinki[i][:1] == punkt:
                kolejne_wierzch.append(odcinki[i][1:])
        # print(kolejne_wierzch)
        p = int(random.uniform(0, len(kolejne_wierzch))) #losujemy nowy wierzchołek dostępny z listy
        for j in range(0, len(punkty), 1):          #dopisuje nowy wierzchołek
            if punkty[j] == kolejne_wierzch[p]:
                roz.append(j + 1)
    # print("nowa tablica", roz)
    return roz


def losowyWspinaczkowy(cel):
    max_dl_roz = len(odcinki)  # maksymalny rozmiar rozwiązania
    min_dl_roz = int((len(odcinki) / 2) - 1)  # najmniejszy rozmiar rozwiązania
    iteracje = 100  # ilość literacji
    tablica = []  # lista punktów odwiedzanych w proponowanym rozwiązaniu
    najlepszy_wynik = [1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1]
    while max_dl_roz >= min_dl_roz:
        for j in range(0, iteracje, 1):
            roz = generowanieLosowejKolejnoci(max_dl_roz, punkty, odcinki)
            nowe_roz = losowySasiad(roz, punkty, odcinki)  #metoda losowy sąsiad
            # print(nowe_roz)
            for k in range(1, len(punkty) + 1):#sprawdzam czy wszystkie punkty podanego rozwiązania zostały odwiedzone
                odw_ptk = k in nowe_roz
                # print(k, odw_ptk)
                if odw_ptk:
                    tablica.append(k)
            if (len(tablica) >= len(punkty)) and \
                    (nowe_roz[0] == nowe_roz[len(nowe_roz) - 1]) and \
                    cel(nowe_roz) <= cel(najlepszy_wynik):  #sprawdzamy czy są sprawdzone warunki
                # print("rozwiązanie wynosi :", cel(nowe_roz))
                najlepszy_wynik = nowe_roz
                # print("nowy rozwiązaniem jest sekwencja :", najlepszy_wynik)
            # print("odwiedzone punkty", tablica)
            tablica = []
        max_dl_roz -= 1
    return najlepszy_wynik


def najlepszySasiad(cel, roz):  # cel, roz, punkty, odcinki
    najlepszy_wynik = roz
    dl_max_roz = len(roz)

    # print(roz)
    tym = roz
    for ptk in range(1, len(roz) - 1):
        # print(ptk)
        del tym[ptk:]
        # print("rozwiązanie w pętli ", tym)
        for k in range(len(roz), dl_max_roz, 1):
            punkt = punkty[roz[-1] - 1]
            kolejne_wierzch = []
            for i in range(0, len(odcinki), 1):
                if odcinki[i][:1] == punkt:
                    kolejne_wierzch.append(odcinki[i][1:])
            p = int(random.uniform(0, len(kolejne_wierzch)))
            for j in range(0, len(punkty), 1):
                if punkty[j] == kolejne_wierzch[p]:
                    tym.append(j + 1)

            if (tym[0] == tym[len(tym) - 1]) and \
                    cel(tym) <= cel(najlepszy_wynik):
                najlepszy_wynik = tym
                # print("naj", najlepszy_wynik)
    return najlepszy_wynik


def determistycznyWspinaczkowy(cel):
    max_dl_roz = len(odcinki)  # maksymalny rozmiar rozwiązania
    min_dl_roz = int((len(odcinki) / 2) - 1)  # najmniejszy rozmiar rozwiązania
    iteracje = 100  # ilość literacji
    tablica = []  # lista punktów odwiedzanych w proponowanym rozwiązaniu
    najlepszy_wynik = [1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1]
    while max_dl_roz >= min_dl_roz:
        for j in range(0, iteracje, 1):
            roz = generowanieLosowejKolejnoci(max_dl_roz, punkty, odcinki)
            nowe_roz = najlepszySasiad(cel, roz)
            # print(nowe_roz)
            for k in range(1, len(punkty) + 1):
                odw_ptk = k in nowe_roz
                # print(k, odw_ptk)
                if odw_ptk:
                    tablica.append(k)
            if (len(tablica) >= len(punkty)) and \
                    (nowe_roz[0] == nowe_roz[len(nowe_roz) - 1]) and \
                    cel(nowe_roz) <= cel(najlepszy_wynik):
                # print("rozwiązanie wynosi :", cel(nowe_roz))
                najlepszy_wynik = nowe_roz
                # print("nowy rozwiązaniem jest sekwencja :", najlepszy_wynik)
            # print("odwiedzone punkty", tablica)
            tablica = []
        max_dl_roz -= 1
    return najlepszy_wynik


def symulowaneWyzarzanie(cel, Temperatura):
    max_dl_roz = len(odcinki)  # maksymalny rozmiar rozwiązania
    min_dl_roz = int((len(odcinki) / 2) - 1)  # najmniejszy rozmiar rozwiązania
    iteracje = 1000  # ilość literacji
    tablica = []  # lista punktów odwiedzanych w proponowanym rozwiązaniu
    najlepszy_wynik = generowanieLosowejKolejnoci(max_dl_roz, punkty, odcinki)
    while max_dl_roz >= min_dl_roz:

        V = [najlepszy_wynik]
        for j in range(1, iteracje + 1, 1):
            roz = generowanieLosowejKolejnoci(max_dl_roz, punkty, odcinki)
            nowe_roz = losowySasiad(roz, punkty, odcinki)
            # print(nowe_roz)
            for k in range(1, len(punkty) + 1):
                odw_ptk = k in nowe_roz
                # print(k, odw_ptk)
                if odw_ptk:
                    tablica.append(k)
            if (len(tablica) == len(punkty)) and \
                    (nowe_roz[0] == nowe_roz[len(nowe_roz) - 1]) and \
                    cel(nowe_roz) <= cel(najlepszy_wynik):
                # print("rozwiązanie wynosi :", cel(nowe_roz))
                najlepszy_wynik = nowe_roz
                V.append(najlepszy_wynik)
                # print("nowy rozwiązaniem jest sekwencja :", najlepszy_wynik)
            # print("odwiedzone punkty", tablica)

            else:
                e = math.exp(- abs(cel(nowe_roz) - cel(najlepszy_wynik)) / Temperatura(j))
                u = random.uniform(0.0, 1.0)
                if (u < e) and \
                        (len(tablica) == len(punkty)) and \
                        (nowe_roz[0] == nowe_roz[len(nowe_roz) - 1]):
                    najlepszy_wynik = nowe_roz
                    V.append(najlepszy_wynik)
                    # print("jest ")
            tablica = []
            # print(V)
        max_dl_roz -= 1
    return min(V, key=cel)


def oneMax(chromosome):
    result = 0.0
    for c in chromosome:
        result = result + c
    return result


def krzyzowanieJednoPunktowe(chromosom1, chromosom2):
    podział = random.randint(0, len(chromosom1) - 1)
    dziecko1, dziecko2 = copy.copy(chromosom1), copy.copy(chromosom2)
    dziecko1 = chromosom1[:podział] + chromosom2[podział:]
    dziecko2 = chromosom2[:podział] + chromosom1[podział:]
    return [dziecko1, dziecko2]




with open("graf.txt", 'r') as f:
    punkty, odcinki, dlugosci = map(ast.literal_eval, f.readlines())

wybor = input("1. Losowe probkowanie \n"
              "2. Symulowane wyzarzanie \n"
              "3. Losowy wspinaczkowy\n"
              "4. Determistyczny wspinaczkowy \n"
              "5. Gentyczny \n")

if wybor == "1":
    roz = losoweProbkowanie(lambda s: funkcjaCelu(s, punkty, odcinki, dlugosci))
    print(roz)
    print(funkcjaCelu(roz, punkty, odcinki, dlugosci))
if wybor == "2":
    roz = symulowaneWyzarzanie(lambda s: funkcjaCelu(s, punkty, odcinki, dlugosci),
                               lambda k: 1000 / k)
    print(roz)
    print(funkcjaCelu(roz, punkty, odcinki, dlugosci))
if wybor == "3":
    roz = losowyWspinaczkowy(lambda s: funkcjaCelu(s, punkty, odcinki, dlugosci))
    print(roz)
    print(funkcjaCelu(roz, punkty, odcinki, dlugosci))
if wybor == "4":
    roz = determistycznyWspinaczkowy(lambda s: funkcjaCelu(s, punkty, odcinki, dlugosci))
    print(roz)
    print(funkcjaCelu(roz, punkty, odcinki, dlugosci))
if wybor == "5":
    print(krzyzowanieJednoPunktowe([1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1]))

