import requests # do API  #
from requests.auth import HTTPBasicAuth # do zalogowania się #
import json
# ==============================================================================#
# ===========================link do pobrania API===============================#
# ==============================================================================#

filtr="https://jira.nasksa.pl/rest/api/2/search?jql=project+in+(OSETT)+AND+issuetype+not+in+(%22Planned+Work%22,+%22Subcontractor+Issue%22)+AND+status+in+(%22Oczekiwanie+na+klienta%22,+Weryfikacja,+Zawieszone,+Nowe,+%22W+trakcie%22,+%22Odpowied%C5%BA+udzielona%22,+Obej%C5%9Bcie,+Reklamacja,+%22Przygotowanie+wyceny%22,+%22Oczekiwanie+na+odpowied%C5%BA%22,+%22Decyzja+koordynatora%22,+%22Weryfikacja+PIB%22,+%22Przygotowanie+oferty%22,+%22Oferta+przekazana%22,+%22Analiza+koordynatora%22,+%22Brak+warunk%C3%B3w+technicznych%22)+AND+%22Responsible+group%22+%3D+%22PT/DNOC+-+Dzia%C5%82+NOC%22+AND+labels+is+EMPTY+AND+(createdDate+%3E%3D+%222020/12/18+12:41%22+OR+createdDate+%3C+%222020/12/18+12:40%22)+OR+project+%3D+OSESD+AND+issuetype+%3D+Incident+AND+status+not+in+(Zako%C5%84czone,+%22Awaria+usuni%C4%99ta%22)+AND+issueFunction+not+in+linkedIssuesOf(%22type%3Dsupport%22)+AND+%22Responsible+group%22+%3D+%22PT/DNOC+-+Dzia%C5%82+NOC%22+AND+(createdDate+%3E%3D+%222020/12/18+12:41%22+OR+createdDate+%3C+%222020/12/18+12:40%22)&maxResults=-1"
response = requests.get (url=filtr, auth=HTTPBasicAuth('user', 'haslo')) #trzeba to zashashowac#

#informacja o statusie rest 200 >>OK, prawie sex #
print(response)
#nazywam sobie plik filtrem który wykorzystuje, "w" tworze nowy plik#
file= open("filtr_17708", "w")
#zapisuje obecne OSETT w osett_obecne#
file_osett= open("osettt_obecne", "w")
#tutaj calosc strony wrzucam jako json do data, nie potrzebne#
data= response.json()


list = [{'id': 123, 'data': 'qwerty', 'indices': [1,10]}, {'id': 345, 'data': 'mnbvc', 'indices': [2,11]}]

#wrzucanie wszystkich kluczy zgloszen do pliku #
try:
    i=0
    # dlugosc wyrazenia, chodzi o sprawdzneie ile jest kluczy osett#
    while(i<len(response.json()["issues"])):

        data2= response.json()["issues"][i]["key"]
        #dodaje do osett obecne klucze czyli umery osett#
        file_osett = open("osettt_obecne", "a")
        file_osett.write(data2)
        file_osett.write("\n")
        #print(data2)
        i+=1
except:
    #a chuj jakby się miało coś wysypać na wszelkie wu, może api kiedys zmienią jakos#
    print("AOB, albo zmienili api")

#sex za 2 linijki, zapisane wszystko w plikach  #
file.write(str(data))

file.close()
#sex zapisane, program zrealizowany, api zapisalo zgloszenia do pliku#
#nastpeny krok to zaladowanie danych z api typu numer servisu#
#zahashowanie hasla#
#kolejny temat to zaladowanie z solarwindsa adresacji#
#obliczenie adresacji z maskami z SW#

# pingowanie adresów #
#logowanie się na junipera  i pobierania service#

#pobranie adresacji z junipera #
#ping na vlany juniper na cpe #
#poprawienie stylistyki i czytelnosci kodu#
#pobranie cgnat z junipera#
#pobranie konfiguracji z cpe w szkole i #
#poprawienie stylistyki i czytelnosci kodu#
#spradzenie adresacji z konfigaami pobranymi#
#wyslanie ping z cpe na swiat, sprawdzenie ramki#
#poprawienie stylistyki i czytelnosci kodu#
#zapisanie wynikow pingow do csv,  test to 1000pingow#
#z testu zrobienie wykresu ladnego i zapisanie print screena#
#poprawienie stylistyki i czytelnosci kodu#
#dodanie komentarza do zgloszenia jira#
#pobranie informacji kto jest operatoarrem lacza#
#poprawienie stylistyki i czytelnosci kodu#
# pobranie danych lacza danych szkoly #
#pobranie godzin otwarcia szkoly, numetu kontaktowego, emaila#
#poprawienie stylistyki i czytelnosci kodu#
#wyslanie emaila do opearatora#
#wyslanie emaila do szkoly#
#poprawienie stylistyki i czytelnosci kodu#
#oznaczenie zgloszneia w celu weryfikacji zgloszenia i jego dalsze procesowanie#
#poprawienie konfigurajci na CPE jezeli jest bledna huawei#
#MT#
#FG#
#poprawienie stylistyki i czytelnosci kodu#
#poprawienie konfiguracji na szkielecie, rollback jezeli zbyt duzo lini jest poprawianych, badz brak ocmmita#
#poprawienie stylistyki i czytelnosci kodu#
#skonfigurowanie AWS EC2#
#skonfigurowanie na aws vpn do OSE, forticlient#
#zrobienie skalowania na aws#
#loadbalancer na aws#
#uruchomienie kontenerow na aws i sprawdzenie mozliwosci kodu#
#rozpoznawanie awarii w ose szkol pojedynczych, przed ich zgloszneiem#
#machine learning dotyczace awaii jeszcze nie utworzonych w osesd#
#komunikacja z szkolami#
#cdn#