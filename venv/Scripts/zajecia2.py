import functools


# Napisać za pomocą reduce agregację listy stringów do postaci słownika:
# z danych: ['ala', 'alamo', 'alfred', 'boisko', 'alfred', 'boisko', 'alfred', 'boisko', 'bot', ]
# ma powstać słownik: {'a': {'ala', 'alamo', 'alfred'}, 'b': {'boisko', 'bot'}}


dane =['ala', 'alamo', 'alfred', 'boisko', 'alfred', 'boisko', 'alfred', 'boisko', 'bot', ]



def f3(agg, v):
    agg.setdefault(v[0], set()).add(v)
    return  agg


y= functools.reduce (f3, x, {}).reduce
y = functools.reduce(lambda agg if agg.setdefault)