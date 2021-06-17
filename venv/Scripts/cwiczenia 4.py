"""
Napisać generator, który będzie zwracał wszystkie dostępne notowania waluty o podanym kodzie z API NBP:
http://api.nbp.pl
Generator będzie wczytywał dane latami (wolno wysłać zapytanie tylko o rok danych na raz) i będzie zwracał (yield)notowania w kolejności odwrotnej chronologicznie (w tył).
Format pojedynczego notowania będzie słownikiem o postaci:
{
    'code': 'USD',
   'bid': 3.3,
   'ask': 3.4,
   'effectiveDate': <tutaj obiekt date z datą notowania>
}
Proponuję skorzystać z usługi:
https://api.nbp.pl/api/exchangerates/rates/c/gbp/2012-01-01/2012-01-31/?format=json
Zwróćcie uwagę, że w URLu są zawarte: kod waluty, i obie daty.
Jak wysłać zapytanie i przeczytać odpowiedź:
r = requests.get("https://api.nbp.pl/api/exchangerates/rates/c/gbp/2012-01-01/2012-01-31/?format=json")
# Sprawdzanie statusu zapytania:
# if r.status_code != 200:
#     print('coś nie tak', r.status_code)
#     exit()
# lub:
# r.raise_for_status()
# Format JSON to po prostu zagnieżdżona struktura słowników i list, a więc np cena bid # pierwszego notowania:
j = r.json()
print(j["rates"][0]["bid"])
Możemy oczywiście po listach iterować za pomocą pętli for.
Korzystamy z pakietu requests, który trzeba ściągnąć i zainstalować.
Aby to zrobić wpisujemy w oknie Terminal w Pycharm polecenie:
pip install requests
Dodadkowo dla ambitnych napisać 3 generatory przetwarzające notowania strumieniowo:
# 1. Wyliczał spread i dodawał do notowania jako wartość dla klucza 'spread'
# 2. Wyliczał zmianę względem dnia poprzedniego (dla ceny ask) - i dodawał do notowania jako wartość dla klucza 'delta'
# 3. Generator filtrujący, który będzie puszczał dalej tylko notowania spełniające warunek:
#    wartosc bezwzględna pola o nazwie nazwa_pola >= min wartosc
Ostatecznie chciałbym mieć możliwość np znaleźć notowania USD w których spread >= 0.08 i zmiana względem dnia poprzedniego była >=0.07:
g_nbp = generatorNBP("usd")
g1 = generuj_spread(g_nbp)
g2 = generuj_delta(g1)
g3 = filtruj(g2, "spread", 0.08)
g4 = filtruj(g3, "delta", 0.07)
"""
import datetime
import requests

# r = requests.get('https://api.nbp.pl/api/exchangerates/rates/c/gbp/2012-01-01/2012-01-31/?format=json')
# print(r.status_code)
# r.raise_for_status()
# j = r.json()
# print(j['rates'][0]['effectiveDate'])
#
# datetime.date.today() - 365
#
def generatorNBP(code):
    td1 = datetime.timedelta(days=1)
    to_date = datetime.date.today()
    while True:
        from_date = to_date - 365 * td1
        url = f'https://api.nbp.pl/api/exchangerates/rates/c/{code}/{from_date.strftime("%Y-%m-%d")}/{to_date.strftime("%Y-%m-%d")}/?format=json'
        r = requests.get(url)
        if r.status_code == 404:
            return
        r.raise_for_status()
        for d in reversed(r.json()['rates']):
            yield {**d, 'code': code}
        to_date = to_date - 366 * td1

def dodaj_spread(g):
    for n in g:
        yield {**n, 'spread': n['ask'] - n['bid']}

def dodaj_delta(g):
    poprzedni = None
    for n in g:
        if poprzedni:
            yield {**n,
                   'delta_ask': n['ask'] - poprzedni['ask'],
                   'delta_bid': n['bid'] - poprzedni['bid']}
        poprzedni = n

def filtruj(g, nazwa_pola, min_w):
    for n in g:
        if abs(n[nazwa_pola] >= min_w):
            yield n
if __name__ == '__main__':
    g1 = generatorNBP('usd')
    g2 = dodaj_delta(g1)
    g3 = dodaj_spread(g2)
    g4 = filtruj(g3, 'spread', 0.085)
    for d in g4:
        print(d)


class PierwszyGenerator:
    def __iter__(self):
        return self
    def __next__(self):
        return 22
g1 = PierwszyGenerator()
for i in g1:
    print(i)