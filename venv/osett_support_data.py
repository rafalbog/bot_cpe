import requests
from requests.auth import HTTPBasicAuth
import pandas


#wczytujemy zgloszenia do obrobienia#
file = open("osettt_obecne", "r")
#tworzymy pustą zmienną panda#
csvpanda = pandas.DataFrame( )

#print(csvpanda) << przy wydrukowania plik pokazuje tylko
#Empty DataFrame
#Columns: []
#Index: []


#zgloszenie wrzucamy w tablice#
Issue_osett= file.read().split()
#bazowy link do zgloszeń #

link="https://jira.nasksa.pl/rest/api/2/issue/"
#csv_dane= []
i=0
for n in Issue_osett:
    #tworzymy link ktorym bedizemy wchodzic na api jiry#
    link_final=str (link+n)

    #print(link_final)
    #probujemy pobrac dane z APi#


    try:
        #csv_dane.append(n +";")
        odpowiedz= requests.get(url=link_final, auth=HTTPBasicAuth('rafalbo', '13!#Rafael'))
        #jeżeli mamy kof 503 to serwer jest nie dostepny#
        #przy tym IF trzeba dodac kolejne kody ktore sa#
        if (odpowiedz.status_code == 503):
            print("JIRA IS DED, 503;")
          #  csv_dane[i] = csv_dane[i]+"JIRA IS DED, 503"
            result="JIRA IS DED, 503"
        else:
            data= odpowiedz.json()["fields"]["customfield_12901"][0]
         #   print(data)
        #    csv_dane[i] = csv_dane[i] + data
            result= data

    except:
        #wszelkie inne problemy jak nie dziala#
        print("JIRA IS DED")
       # csv_dane[i] = csv_dane[i] + "JIRA IS DED"
        result="JIRA IS DED"
    #do obslugi petli#
    i += 1
    # tworzymy pande 1 wiersz do dodania do naszego pliku#
    pandas_temp = pandas.DataFrame({'issue':[n],  'service':[result] })
    #dodajemy wszystkie wiersze do naszej pandy i pomijamy index#
    csvpanda=csvpanda.append(pandas_temp, ignore_index=True)
    #print(pandas_temp)
print(csvpanda)

### dopisac zapisywanie
csvpanda.to_csv(path_or_buf="CSV_dane")
#print(csv_dane)
#do przemyslenia czy maja sie pobierac wszystkie serwisy i maja sie zapisywac gdzies#
#wydaje mi sie ze trzeba bedzie zrobic slownik z slownikiem w srodku aby przechowywac#
#w jsonie dane zgloszneia, co wiecej bedize mozna pomyslec nad rozbudowa jsona, w sumie w owolny spowb#
#bede mogl przeez to sobie dodawac nowe dane, z racji ze location id jest ostateczne to #
#moze jednak pobierac szkoly po loczation id 2017?#
#koniecnzie zrobic hasha na haslo i wrzucac wszystko na gita bo ne wygodnie jest tak#
#dodac pande i aby zapisywalo sie w csv#
#ogarnac gita#
#zoptymalizowac kod i opisac"