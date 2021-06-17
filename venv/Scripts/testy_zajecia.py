

file= open('towary.txt', "r")

k={}
for lines in file:
    key, value1, value2, v3 = lines.split()
    v4= [ value1, value2, v3]
    k[key] = v4
print(k)

def dodaj_do_zak(abc):
    for key in abc:
        if abc ("key", key, "value:", abc[key]):
            print(abc[key])



nowa_lista={
'Banany': ['2.4', 'kg', '3.5']
}
dodaj_do_zak(nowa_lista)

