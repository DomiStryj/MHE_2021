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
        1   2   4   6   4   2   6   5   3   1   3   5   1
["a","b","c","d","e","f"]
["ac","ca", "ae","ea", "ce","ec", "ab","ba", "ef","fa", "bf","fb", "bd","db", "df","fd"]
[1,1,5,5,2,2,3,3,4,4,6,6,1,1,1,1]


"""

import ast
import random
import itertools


def funkcjaCelu(rozwiazanie, punkt, odcinki, dlugosci):
    suma = 0
    tmp = []
    try:
        for i in range(0, len(rozwiazanie), 1):
            odc = punkt[rozwiazanie[i] - 1] + punkt[rozwiazanie[i + 1] - 1]
            tmp.append(odc)

    except IndexError:
        pass
    for x in range(0, len(tmp), 1):
        for y in range(0, len(odcinki), 1):
            if tmp[x] == odcinki[y]:
                suma += dlugosci[y]
    return suma


def generowanieLosowejKolejnoci(ilosc_punktow, wielkosc_rozw):
    losowa_kolejnosc = [1]
    kolekcja = [i for i in range(2, ilosc_punktow + 1, 1)]
    # print(kolekcja)
    for i in range(0, wielkosc_rozw - 2):
        p = int(random.uniform(0, len(kolekcja)))
        losowa_kolejnosc.append(kolekcja[p])
    losowa_kolejnosc.append(1)
    return losowa_kolejnosc  # 1,2,4,6,4,2,6,5,3,1,3,5,1
    # 1,3,5,6,4,2,1


def losoweProbkowanie(cel, gen_roz, iteracje):
    najlepszy_wynik = [2, 6, 2, 6, 2, 6, 2, 6, 2, 6, 2, 6]
    for i in range(0, iteracje, 1):
        nowe_roz = gen_roz()
        print(nowe_roz)
        temp = []
        for j in range(0, len(nowe_roz), 1):
            if j < len(nowe_roz) - 1:
                temp.append(punkty[nowe_roz[j] - 1] + punkty[nowe_roz[j + 1] - 1])
            else:
                continue
        koniec = temp[len(temp) - 1]
        koniec = koniec[1:]
        licznik = 0
        for k in range(0, len(temp), 1):
            for j in range(0, len(odcinki), 1):
                x, y = temp[k]
                if k < len(nowe_roz) - 2:
                    z, v = temp[k + 1]
                else:
                    continue
                if k == 0:
                    punkt_startu = x
                if temp[k] == odcinki[j]:
                    if y == z and koniec == punkt_startu:
                        licznik += 1
                        if cel(nowe_roz) < cel(najlepszy_wynik) and licznik == n - 2:
                            najlepszy_wynik = nowe_roz
    print(najlepszy_wynik)
    return najlepszy_wynik


with open("graf.txt", 'r') as f:
    punkty, odcinki, dlugosci = map(ast.literal_eval, f.readlines())

# print(funkcjaCelu([1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 1], punkty, odcinki, dlugosci))
# print(generowanieLosowejKolejnoci(len(punkty), 13))

n = 7
roz = losoweProbkowanie(lambda s: funkcjaCelu(s, punkty, odcinki, dlugosci),
                        lambda: generowanieLosowejKolejnoci(len(punkty), n, ), 100000)

print(funkcjaCelu(roz, punkty, odcinki, dlugosci))
