import time
import  collections

class TimeMenager:
    __slots__ = ['start', 'end', 'nazwa']

    def __init__(self, nazwa):
        self.nazwa = nazwa

    def __enter__(self):
        self.start = time.perf_counter()
        print('enter')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.perf_counter()
        print('exit', exc_type, exc_val, exc_tb)

    def __str__(self):
        return f'{self.nazwa} {self.end - self.start}'


with TimeMenager('Pomiar') as tm:
    x = collections.deque() # tutaj jest taka kwestia ze jak zrobimy x=[] to za kazdym razem bedzie
    # zaalakowana pamiec w tej tablicy
    # zlozonos kwadratowa jest niestety w tablicach gdy dodajemy element
    #na poczatku listy, gdyz leementy wszsystkie trzeba przesunac,
    # deque jest tylko stosowane do dodawania elementow
    # kiedy chcemy wyszukac konretnety index to musimy stracic tyle czasu jaki ma index element
    # wiec czas uzyskania indexu n jest rowny n
    # dequee tylko poczatek i koniec
    for i in range(200000):
        x.insert(0, i)

print(tm)