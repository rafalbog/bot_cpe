import datetime

x = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# wynik - [1, 2, 3, 4, 5, 6, 7, 8, 9]


y= [i for l in x for i in l]

print(y)
x = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

y= [i for wiersz in x for i in wiersz]
print(y)
def time_dawac():
    print (datetime.now())


def g_numerujacy(g):
    for i, linia in enumerate(g):
        yield f'{i} {linia}'
        time_dawac()
x = ['ala', 'ela', 'ola']
with open('towary.txt', encoding='utf-8') as f:
    for l in g_numerujacy(f):
        print(l)



