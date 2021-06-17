import pprint
import  re
import collections

file= open('mt_config', "r")


table=file.read().split('\n')
dictio= collections.defaultdict(list)
temp2 = re.compile('.')
print(temp2.findall(file.read()))
print(file.readlines())
temp=""
#temp4=re.re.findall(r'\b25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?\.25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?\.25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?\.25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?\b',s)

# for i, x in enumerate(table):
 #   if table[i][:1] == "/":
  #       temp=table[i][1:]
   # print( re.findall(r'\b25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?\.25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?\.25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?\.25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?\b', table[i]))
arr=[]


for i in table:
    regex_ipv4=re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', i)
    if(regex_ipv4 !=arr ):
         print(regex_ipv4)


    #dictio[temp].append(table[i])


         ## drukowanie pierwszego elementu tabeli ale tylko do pierwszego znaku z stringa





### chce zrobic tak zeby wyszukiwalo pierwszy eelement i pozniej jak spotka drugi taki sam to przerwie
###  sie  petla i bedzie fin drugiej petli i wroci dalej szukac takiego elementu w pierwszej petli
### jak skonczy sie petla to waidomo ze  koioifnvc



pprint.pprint(dictio)