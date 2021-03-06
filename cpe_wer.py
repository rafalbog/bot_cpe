# wew
from typing import List, Any, Dict, Union
import paramiko
import subprocess
import re
import pprint

diagnostyka_dict = {}


## sprawdzenie czy urzadzenie jest dostepne
def czy_dostepne_urzadzenie(hosta):
    proc = subprocess.Popen(
        ['ping', '-c', '1', hosta],
        stdout=subprocess.DEVNULL
    )
    proc.wait()
    if proc.returncode == 0:
        return True
        # host dostepny
    else:
        return False


## polaceznie do USG
def polaczCPE_USG(hosta, command, un, pwd):
    ssh2 = paramiko.SSHClient()
    ### !!!dla bezpieczenstwa usunac auto dodawanie!!!
    ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh2.connect(hostname=hosta, username=un, password=pwd)
    stdin, stdout, stderr = ssh2.exec_command(command)
    ## przy dluzszym wydruku na ekranie, huawei oczekuje na potwierdzenie wydruku
    stdin.write(
        "                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         ")
    print(stderr)
    wydruk_komendy = ""
    stdout = stdout.readlines()  ## czytanie linii z terminala
    for line in stdout:
        wydruk_komendy = wydruk_komendy + line
    # print(stdout)
    ssh2.close()
    # print(command, wydruk_komendy)
    return wydruk_komendy


#### do weryfikacji polacz cpe usg i polaczcpe
def polaczCPE(hosta, command, un, pwd):
    ssh2 = paramiko.SSHClient()
    ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh2.connect(hostname=hosta, username=un, password=pwd)
    stdin, stdout, stderr = ssh2.exec_command(command)
    ## przy dluzszej komendzie, huawei oczekuje na potwierdzenie wydruku
    stdin.write(
        "                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         ")
    print(stderr)
    wydruk_komendy = ""
    stdout = stdout.readlines()  ## czytanie linii z terminala
    for line in stdout:
        wydruk_komendy = wydruk_komendy + line
    # print(stdout)
    ssh2.close()
    # print(command, wydruk_komendy)
    return wydruk_komendy


## sprawdzamy model CPE
def sprawdz_model_CPE(stdout_ssh):
    # print("model")
    # print(stdout_ssh)
    ### splitlines() do czytnia linia po liniii w stringu
    for line in stdout_ssh.splitlines():
        wersja = re.match("^USG?.{1}[0-9]{1,3}", line)
        if re.match("^USG?.{1}[0-9]{1,3}", line):
            return wersja.group()
    return False


## komendy do testowania Huawei
## funkcja>>> pelna komenda
# "C_display_arp": "display arp",
# "C_display_ip_interface_b": "display  ip interface  brief",
# "C_display_in_b": "display interface brief",
# "C_display_nat_add": "display  nat address-group all-systems",
# "C_display_curr_conf": "display  current-configuration",
# "C_ping": "ping 192.168.100.21",
# "C_display_route_static": " display  current-configuration | include  route-static",
# ## trudne do okre??lenia dzia??anie prawid??owe pingu powy??ej c100
# "C_ping_c10_f_s1472": "ping -c 10 -f -s 1472 192.168.100.21",
# "C_display_firewall_session_table": "display  firewall  session table"
def wykonaj_diagnostyke_Huawei(hosta, un, pwd):
    diagnostyka_dict = {}

    def C_display_ip_vpn_instance():
        stdout = polaczCPE_USG(hosta, "display  ip vpn-instance", un, pwd)
        ### regex kt??ry wyszukuje linie z VRF i default
        ### zapisuje nast??pnie linie wyszukane jako listy z instancjami i vlan distinguisher
        ### przyk??ad  [['VRF_1_DATA', '11:1', 'IPv4'], ['VRF_1_DATA', '11:1', 'IPv6'], ['VRF_1_NOSEC', '101:1', 'IPv4'], ['VRF_1_NOSEC', '101:1', 'IPv6'], ['VRF_1_WLAN', '51:1', 'IPv4'], ['VRF_1_WLAN', '51:1', 'IPv6'], ['default', 'IPv4']]
        regex_VRF = re.compile(r"(VRF)|(default)")
        VRF_dic: List[any] = []
        for line in stdout.splitlines():
            if regex_VRF.search(line):
                VRF_dic.append(line.split())

        return VRF_dic

    def C_display_arp():
        ## regex do ipv4 \b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b
        ## regex do MAC adresu \b([0-9a-f-]){14}(?=.*-)\b  >> ulepszony \b([0-9a-f-]){14}\b >> ulepszony \b([0-9a-f]|[-]){14}\b
        ## regex do VRF \b(VRF)[_0-9A-Z]{1,}|(default)
        stdout = polaczCPE_USG(hosta, "display arp", un, pwd)
        ARP_dic: List[any] = []
        tempARP = []
        for line in stdout.splitlines():
            ###regex na ipv4
            if re.search(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", line):
                tempARP.append(re.search(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", line).group())
                ###regex do MAC
            if re.search(r"\b([0-9a-f]|[-]){14}\b", line):
                tempARP.append(re.search(r"\b([0-9a-f]|[-]){14}\b", line).group())
                ###regex do VRF
            if re.search(r"\b(VRF)[_0-9A-Z]{1,}|(default)", line):
                tempARP.append(re.search(r"\b(VRF)[_0-9A-Z]{1,}|(default)", line).group())
                ### regex by?? OK, problemem by??o samo re.match rozwiazaniem bylo re.search
            # ARP_dic.append(tempARP)nie appenduje sie lista prawidlowo
            # ARP_dic.append(tempARP) >>> przez referencje dziala, stad po wyczyszczeniu jest czysto
            if tempARP != []:
                ARP_dic.append(tempARP[:])
            tempARP.clear()
        return ARP_dic

    def C_display_in_b():
        display_inb = {}
        tempWAN = []
        tempinnyport = []
        uszkodzneporty = {}
        stdout = polaczCPE_USG(hosta, "display interface brief", un, pwd)
        for line in stdout.splitlines():
            if "up" in line:
                if re.search(r"(GigabitEthernet)", line):
                    if re.search(r"[0-9][\/][0-9][\/][0-9][\.]\S{1,9}", line):
                        tempWAN.append(re.search(r"[0-9][\/][0-9][\/][0-9][\.]\S{1,9}", line).group())
                    else:
                        ### wyszukamy kazdy  interfejs up czy wan czy nie wan
                        tempinnyport.append(re.search(r"(GigabitEthernet)[0-9][\/][0-9][\/][0-9]", line).group())
                        temp = tempinnyport[0]
                        ### wyszukamy porty z bledami regex do wyszukiwania \s[1-9]{1}[0-9]{0,10}\s
                        ### regex na wszystkie wartosci czy sa bledy na int czy nie \s[0-9]{1,8}\s
                        if re.search((r"\s[0-9]{1,8}\s"), line):
                            ### do zweryfikowania dlaczego nie drukuje sie prawidlowa ilosc int z bledami/bez
                            tempar = re.findall(r"\s[0-9]{1,8}\b", line)
                            ## findall zwraca wynik w postaci tabeli, tutaj przekazany wynik do slownika
                            # budowa slownika nazwa interface: "INuti/OUTuti/INerror/OUTerror" 0,0,0,0
                            if int(tempar[2]) != 0 or int(tempar[3]) != 0:
                                uszkodzneporty.update({temp: ["INuti/OUTuti/INerror/OUTerror", tempar]})

        if uszkodzneporty != {}:
            display_inb["uszkodzone porty"] = uszkodzneporty
        else:
            display_inb["uszkodzone porty"] = "brak"

        display_inb["WAN"] = tempWAN
        display_inb["portyUP"] = tempinnyport
        ## regex do wy??apana tylko nazw interfacow \b(GigabitEthernet){1}\S{1,9}
        ## regex tylko na WAN (GigabitEthernet)[0-9][\/][0-9][\/][0-9][\.]\S{1,9}
        ###
        ## regex do up/down ale tez wylapuje inne interface \b(up)\b|\b(down)\b
        ### pomys?? wyszuka?? linie zawieraj??ce interface, vlany i je podzielic do listy>> z polecenia dis ip in b
        ### r"\s[0-9]{1,8}\b"

        return display_inb

    def C_display_ip_interface_b():
        stdout = polaczCPE_USG(hosta, "display  ip interface  brief", un, pwd)
        vlanlist = {}  ### vlan z adresacja jaka ma brame
        WAN_IG_iplist = {}  ### zmienna z interfejsami gigabite ethernet WAN z adres ip przypisany
        IG_iplist = {}  ###zmienna z interfejsami gigabite  nieWAN z ip
        Loopback_int = {}
        display_ip_in_b = {}
        ###pobranie adresacji z interfejsow i z vlanow, tyylko linie zawierajace ip4 brane pod uwage
        for line in stdout.splitlines():
            ### wyszukujemy port wan
            if re.search(r"(GigabitEthernet)[0-9][\/][0-9][\/][0-9][\.]\S{1,9}", line):
                ### czy znaleziony port WAN ma adres IP przypisany
                if re.search(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", line):
                    WAN_IG_iplist.update({re.search(r"(GigabitEthernet)[0-9][\/][0-9][\/][0-9][\.]\S{1,9}",
                                                    line).group(): [
                        re.search(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", line).group(),
                        re.search(r"[\/]([0-9]{2})", line).group(1)]})
                # wyszukiwanie maski [\/]([0-9]{2}) >>> wpis group(1) zwraca maske bez slash
                ### wyszukiwanie interface GE nieWAN
            if re.search(r"(GigabitEthernet)[0-9][\/][0-9][\/][0-9]\s", line):
                ### czy znaleziony port nieWAN ma adres IP przypisany
                if re.search(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", line):
                    IG_iplist.update({re.search(r"(GigabitEthernet)[0-9][\/][0-9][\/][0-9]\s", line).group(): [
                        re.search(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", line).group(),
                        re.search(r"[\/]([0-9]{2})", line).group(1)]})
            ### wyszukiwanie interface loopback
            if re.search(r"(LoopBack)[0-9]{1,8}", line):
                ### sprawdzenie czy loopback ma adres ip
                if re.search(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", line):
                    Loopback_int.update({re.search(r"(LoopBack)[0-9]{1,8}", line).group(): [
                        re.search(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", line).group(),
                        re.search(r"[\/]([0-9]{2})", line).group(1)]})
                else:  ### w przypadku jezeli nie jest skonfigurowany adres ip na loopback
                    Loopback_int.update(
                        {re.search(r"(LoopBack)[0-9]{1,8}", line).group(): ["brak adresu", "brak adresu"]})

            ### wyszukiwanie vlanow
            if re.search(r"(Vlanif)[0-9]{1,8}", line):
                ## wyszukiwanie skonfigureowanego adresu do vlanu
                if re.search(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", line):
                    vlanlist.update({re.search(r"(Vlanif)[0-9]{1,8}", line).group(): [
                        re.search(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", line).group(),
                        re.search(r"[\/]([0-9]{2})", line).group(1)]
                                     })

        display_ip_in_b["VLAN"] = vlanlist
        display_ip_in_b["WAN IP"] = WAN_IG_iplist
        if Loopback_int == {}:
            display_ip_in_b["Loopback_int"] = "brak skonfigurowanego loopbacka"
        if IG_iplist == {}:
            display_ip_in_b["Interface z ip"] = "brak interface nieWAN  z adresem IP"

        return display_ip_in_b

    def C_display_nat_add():
        stdout = polaczCPE_USG(hosta, "display  nat address-group all-systems  ", un, pwd)
        VRF_nat = {}

        for line in stdout.splitlines():
            ### wyszukujemy linie z VRF, i przypisujemy/aktualizujemy wartosc temp
            if re.search(r"(VRF_1_)((WLAN)|(NOSEC)|(DATA))", line):
                temp = re.search(r"(VRF_1_)((WLAN)|(NOSEC)|(DATA))", line).group()
                ### wyszukujemy adres ip w linii i przypisujemy do temp
            if (re.search(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", line) and temp is not None):
                VRF_nat.update({temp: [re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", line)]})

        return VRF_nat

    def C_display_curr_conf():
        ## na chwile obecna nic z tego nie potrzebuje
        ## przyszlosciowo pobranie dnsow?
        ## sprawdzenie czy sa w konfiguracji informacje o rulce diagnostyka
        return polaczCPE_USG(hosta, "display  current-configuration", un, pwd)

    def C_ping():
        ## tylko statystyki pingow zebrac, w przypadku wystepowania packet loss wywalic error
        ## w przypadku 100% start dodac tez pingowanie pozostalych adresow, jezeli brak pinga to nie podlaczony sw/ap
        ## dodac pingi na ap i sw
        ### trzeba zrobic ping na adresy z mgmt, czyli z danych ktore juz uzyskalismy z poprzednich funkcji
        # 'display ip interface': {'VLAN': {'Vlanif1000': ['192.168.100.1', '24'],
        # w sumie ping na adresy 11 12 13 14 15 16  21 22 23 24 25  26  niestety brak moze byc widocznych arp urzadzen i dopiero po ping beda widoczne
        ## ale tez pingi po koleii beda dlugo sie robic bardzo..
        stdout = {"sw1 192.168.100.21": polaczCPE_USG(hosta, "ping 192.168.100.21", un, pwd),
                  "sw2 192.168.100.22": polaczCPE_USG(hosta, "ping 192.168.100.22", un, pwd),
                  "sw3 192.168.100.23": polaczCPE_USG(hosta, "ping 192.168.100.23", un, pwd),
                  "ap1 192.168.100.11": polaczCPE_USG(hosta, "ping 192.168.100.11", un, pwd),
                  "ap2 192.168.100.12": polaczCPE_USG(hosta, "ping 192.168.100.12", un, pwd),
                  "ap3 192.168.100.13": polaczCPE_USG(hosta, "ping 192.168.100.13", un, pwd)
                  }
        dostepnosc_sw_ap = {}
        for line in stdout:
            if re.search(r"([0-9]){1,3}[.][0-9]{1,2}[%]", stdout[line]):
                if re.search(r"(100.00%)", stdout[line]):
                    dostepnosc_sw_ap.update({line: ["nie pod??aczone/brak"]})
                elif re.search(r"(\s(0.00%)%)", stdout[line]):
                    dostepnosc_sw_ap.update({line: ["brak strat do sw/ap, packet loss",
                                                    re.search(r"([0-9]){1,3}[.][0-9]{1,2}[%]", stdout[line]).group()]})
                else:
                    dostepnosc_sw_ap.update(
                        {line: ["packet loss", re.search(r"([0-9]){1,3}[.][0-9]{1,2}[%]", stdout[line]).group()]})

        return dostepnosc_sw_ap

    def C_display_route_static():
        stdout = polaczCPE_USG(hosta, "display  current-configuration | include  route-static", un, pwd)
        VRF_route = {}
        temp = None

        for line in stdout.splitlines():

            ### regex tylko na mgmt (10)(?:[0-9]{0,3}\.){3}[0-9]{1,3}\b, doda tylko mgmt
            if re.search(r"(10)(?:[0-9]{0,3}\.){3}[0-9]{1,3}\b", line):
                #### (?:[1-9][0-9]{1,3}\.){3}[0-9]{1,3}\b regex gdzie adres nie zaczyna sie od 0
                VRF_route.update({"MGMT": re.search(r"(10)(?:[0-9]{0,3}\.){3}[0-9]{1,3}\b", line).group(0)})

            if re.search(r"(VRF_1_)((WLAN)|(NOSEC)|(DATA))", line):
                temp = re.search(r"(VRF_1_)((WLAN)|(NOSEC)|(DATA))", line).group()

            if (re.search(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", line) and temp is not None):
                #### (?:[1-9][0-9]{1,3}\.){3}[0-9]{1,3}\b regex gdzie adres nie zaczyna sie od 0
                VRF_route.update({temp: re.search(r"(?:[1-9][0-9]{1,3}\.){3}[0-9]{1,3}\b", line).group(0)})

        return VRF_route

    def C_ping_c10_f_s1472():

        pingi_polaczeniowka = {}
        for adres in diagnostyka_dict["route static"]:
            if adres == "MGMT":
                stdout = polaczCPE_USG(hosta, f"ping -s 1472 -f  {diagnostyka_dict['route static'][adres]}", un, pwd)
            else:
                stdout = polaczCPE_USG(hosta,
                                       f"ping -s 1472 -f -vpn-instance {adres}  {diagnostyka_dict['route static'][adres]}",
                                       un, pwd)
            for line in stdout.splitlines():
                if re.search(r"([0-9]){1,3}[.][0-9]{1,2}[%]\s", line):
                    if re.search(r"(100.00%)", line):
                        print(re.search(r"(100.00%)", line))
                        pingi_polaczeniowka.update({adres: ["nie pod??aczone/brak"]})
                    elif re.search(r"\s(0.00%)", adres):
                        print(re.search(r"(\s(0.00%))", adres))
                        pingi_polaczeniowka.update({adres: ["brak strat do sw/ap, packet loss",
                                                            re.search(r"([0-9]){1,3}[.][0-9]{1,2}[%]\s",
                                                                      line).group()]})
                    else:
                        pingi_polaczeniowka.update(
                            {adres: ["packet loss", re.search(r"([0-9]){1,3}[.][0-9]{1,2}[%]\s", line).group()]})

        print(pingi_polaczeniowka)

    def C_display_firewall_session_table():
        ## regex do protokolow ^\s*([^ \t]+).* , ale tylko wtedy jezeli w linii jest adres ip
        # > nie krytyczna funkcjonalnosc
        # podusmowa?? ilo???? sesji w ka??dym protokole, podsumowac ile adres??w jest przychodz??cych i wychodz??cych
        # \b[a-zC]{2,8} >> REGEX DI \\o protokolow i do current >>> do wypisania sumy sesji i do wypisania poszczegolnch sesji
        # chce zrobic tak ze jezeli sesja sie powtarza to bedzie ddodawana do  juz powstalego prokotolu
        # jezeli w danym protokole jest adres jakis konretny to ten adres zostane dodany a nastepnie kolejny adres docelowy
        # i jest potrzebna kolejna wartosc slownikowa z statystykami na danym adresie ip i na ilu portach jest komunikacja

        Nprotocols = {}

        stdout = polaczCPE_USG(hosta, "display  firewall  session table", un, pwd)
        for line in stdout.splitlines():

            if re.search(r"(Current Total Sessions :)", line):
                Nprotocols.update({"Current Total Sessions ": re.search(r"[0-9]{1,999}", line).group(0)})

            ## \b[a-zC-]{2,8}[a-z]{0,8}
            if (re.search(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", line)):
                temp = False
                #### (?:[1-9][0-9]{1,3}\.){3}[0-9]{1,3}\b regex gdzie adres nie zaczyna sie od 0
                for key in Nprotocols:
                    if key == re.search(r"\b[a-zC-]{2,8}[a-z]{0,8}", line).group(0):
                        Nprotocols[key][0] += 1
                        temp = True

                if temp == False:
                    Nprotocols.update({re.search(r"\b[a-zC-]{2,8}[a-z]{0,8}", line).group(0): [1]})

        print(Nprotocols)
        return Nprotocols

    if czy_dostepne_urzadzenie(hosta):
        # dziala OK
        diagnostyka_dict["VRF_instance"] = C_display_ip_vpn_instance()
        diagnostyka_dict["ARP"] = C_display_arp()
        ### interface regex musi zostac zmieniony, regex powinien pobierac rowniez dane jezeli nazwa portu jest 2 cyfrowa typu 1/0/11 1/0/10
        diagnostyka_dict["display_int_brief"] = C_display_in_b()
        diagnostyka_dict["display ip interface"] = C_display_ip_interface_b()
        diagnostyka_dict["VRF_nat"] = C_display_nat_add()

        diagnostyka_dict["dostepne sw ap"] = C_ping()
        diagnostyka_dict["firewall_session_table"] = C_display_firewall_session_table()
        diagnostyka_dict["route static"] = C_display_route_static()
        diagnostyka_dict["ping polaczeniowka"] = C_ping_c10_f_s1472()
        ### dodanie odczytow optyki
        # poni??sze w trakcie

        # C_display_curr_conf()

        return diagnostyka_dict
    else:
        return False


### komendy do diagnostyki
###### nale??y doda?? najpierw sprwadzenie modelu cpe, jezeli jest to model huawei, to mozna wykonac komendy huawei,
###### je??eli jest to inny model CPE to nale??y przekaza?? inn?? list?? z komendami
###### przygotowa?? pare list z komendami
###### zapisa?? w s??owniku dane do diagnostyki
######
###### display version sprawdzenie modelu cpe
#####display  ip vpn-instance i  display  current-configuration | include  route-static pingowanie szkieletu
#####
##### display  ip interface  brief << sprawdzenie adresacji przypisanych do vlanow i portow
##### display interface brief >>> sprawdzenie bledow na interface, ktore porty sa up/down czy podlaczony jest switch? czy cokolwiek jest podlaczone
#####
#####display  nat address-group all-systems >>> sprwadzenie cgnat i zaadresowanie loopback aby sprawdzic czy dziala cgnat
#####
#####display  firewall  session table  >> zliczenie sesji i z jakiego protokolu korzystaja
#####
#####sprawdzenie mocy optycznych wan portu
#####sprawdzenie na interface wan czy zgadzaja sie vlany
#####
#####wydrukowywanie na konsoli koncowej wnioskow z diagnostyki, szczeg????owej
#####
model_CPE = "uknown"

### model CPE sprawdzamy
###
adres = input("adres testowanego urz??dzenia ")
un=input("user ")
pwd=input("haslo ")

if czy_dostepne_urzadzenie(adres):
    model_CPE = sprawdz_model_CPE(polaczCPE(adres, "display version", un, pwd))
else:
    print("nie dostepne")
##### w sprawdz_model_cpe trzeba dodac regexa do wszystkich rodzajow CPE
##### w polacz cpe trzeba wpisac wszystkie komendy do sprwadzenia wersji czy to FG czy MT
print(model_CPE)
if "USG" in model_CPE:
    test = wykonaj_diagnostyke_Huawei(adres, un, pwd)

    print(f"  test1  i test 2 ")
    # przyk??ad odczytu s??ownika
    # print(test["VRF_instance"][0][0])
    # print(test["VRF_instance"][1][1])
    # print(test["VRF_instance"][2][0])
    # print(test["ARP"][0][0]) 192.168.0.1
    # print(test["ARP"][1][0]) 192.168.10.1
    # print(test["ARP"][2][0]) 192.168.10.230
    # print(test["ARP"][3][0]) 192.168.10.204
    # print(test["ARP"][1][1]) 2c97-b1f7-a9bf
    # print(test["ARP"][2][1]) a0f3-c184-245b
    # print(test["ARP"][3][1]) 0024-1d6a-cde2
    # print(test["ARP"][1][2]) VRF_1_DATA
    # print(test["ARP"][2][2]) VRF_1_DATA
    # print(test["ARP"][3][2]) VRF_1_DATA
    pp = pprint.pformat(test)
    print(pp)
