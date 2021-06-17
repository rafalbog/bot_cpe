from typing import List, Any, Dict, Union
import paramiko
import subprocess
import re
diagnostyka_dict={}

## sprawdzenie czy urzadzenie jest dostepne
def czy_dostepne_urzadzenie(hosta):
    proc= subprocess.Popen(
        ['ping', '-c', '1', hosta],
        stdout=subprocess.DEVNULL
    )
    proc.wait()
    if proc.returncode == 0:
        return True
        #host dostepny
    else:
        return False
## polaceznie do USG
def polaczCPE_USG(hosta, command, un, pwd):
    ssh2 = paramiko.SSHClient()
    ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh2.connect(hostname=hosta, username=un, password=pwd)
    stdin, stdout, stderr = ssh2.exec_command(command)
    ## przy dluzszej komendzie, huawei oczekuje na potwierdzenie wydruku
    stdin.write("                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         ")
    print(stderr)
    wydruk_komendy=""
    stdout= stdout.readlines() ## czytanie linii z terminala
    for line in stdout:
        wydruk_komendy=wydruk_komendy+line
    #print(stdout)
    ssh2.close()
    #print(command, wydruk_komendy)
    return wydruk_komendy
#### do weryfikacji polacz cpe usg i polaczcpe
def polaczCPE(hosta, command, un, pwd):
    ssh2 = paramiko.SSHClient()
    ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh2.connect(hostname=hosta, username=un, password=pwd)
    stdin, stdout, stderr = ssh2.exec_command(command)
    ## przy dluzszej komendzie, huawei oczekuje na potwierdzenie wydruku
    stdin.write("                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         ")
    print(stderr)
    wydruk_komendy=""
    stdout= stdout.readlines() ## czytanie linii z terminala
    for line in stdout:
        wydruk_komendy=wydruk_komendy+line
    #print(stdout)
    ssh2.close()
    #print(command, wydruk_komendy)
    return wydruk_komendy
## sprawdzamy model CPE
def sprawdz_model_CPE(stdout_ssh):
    #print("model")
    #print(stdout_ssh)
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
# ## trudne do określenia działanie prawidłowe pingu powyżej c100
# "C_ping_c10_f_s1472": "ping -c 10 -f -s 1472 192.168.100.21",
# "C_display_firewall_session_table": "display  firewall  session table"
def wykonaj_diagnostyke_Huawei(hosta, un, pwd):
    diagnostyka_dict={}
    def C_display_ip_vpn_instance():
        stdout=polaczCPE_USG(hosta, "display  ip vpn-instance", un, pwd)
        ### regex który wyszukuje linie z VRF i default
        ### zapisuje następnie linie wyszukane jako listy z instancjami i vlan distinguisher
        ### przykład  [['VRF_1_DATA', '11:1', 'IPv4'], ['VRF_1_DATA', '11:1', 'IPv6'], ['VRF_1_NOSEC', '101:1', 'IPv4'], ['VRF_1_NOSEC', '101:1', 'IPv6'], ['VRF_1_WLAN', '51:1', 'IPv4'], ['VRF_1_WLAN', '51:1', 'IPv6'], ['default', 'IPv4']]
        regex_VRF=re.compile(r"(VRF)|(default)")
        VRF_dic: List[any]=[]
        for line in stdout.splitlines():
            if regex_VRF.search(line):
                 VRF_dic.append(line.split())
        return VRF_dic
    def C_display_arp():
        ## regex do ipv4 \b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b
        ## regex do MAC adresu \b([0-9a-f-]){14}(?=.*-)\b  >> ulepszony \b([0-9a-f-]){14}\b >> ulepszony \b([0-9a-f]|[-]){14}\b
        ## regex do VRF \b(VRF)[_0-9A-Z]{1,}|(default)
        stdout=polaczCPE_USG(hosta, "display arp", un, pwd)
        ARP_dic: List[any]=[]
        tempARP=[]
        for line in stdout.splitlines():
            ###regex na ipv4
            if re.search(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", line):
                tempARP.append(re.search(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", line).group())
                ###regex do MAC
            if re.search(r"\b([0-9a-f]|[-]){14}\b",line):
                tempARP.append(re.search(r"\b([0-9a-f]|[-]){14}\b",line).group())
                ###regex do VRF
            if re.search(r"\b(VRF)[_0-9A-Z]{1,}|(default)",line):
                tempARP.append(re.search(r"\b(VRF)[_0-9A-Z]{1,}|(default)",line).group())
                ### regex był OK, problemem było samo re.match rozwiazaniem bylo re.search
            #ARP_dic.append(tempARP)nie appenduje sie lista prawidlowo
            #ARP_dic.append(tempARP) >>> przez referencje dziala, stad po wyczyszczeniu jest czysto
            if  tempARP != [] :
                ARP_dic.append(tempARP[:])
            tempARP.clear()
        return ARP_dic
    def C_display_in_b ():
        ## regex do wyłapana tylko nazw interfacow \b(GigabitEthernet){1}\S{1,9}
        ## regex tylko na WAN (GigabitEthernet)[0-9][\/][0-9][\/][0-9][\.]\S{1,9}
        ## regex do up/down ale tez wylapuje inne interface \b(up)\b|\b(down)\b
        ### pomysł wyszukać linie zawierające interface, vlany i je podzielic do listy

        return polaczCPE_USG(hosta, "display interface brief", un, pwd)
    def C_display_ip_interface_b():
        ###pobranie adresacji z interfejsow i z vlanow, tyylko linie zawierajace ip4 brane pod uwage
        return polaczCPE_USG(hosta, "display  ip interface  brief", un, pwd)
    def C_display_nat_add ():
        ### pobranie adresacji cgnat i przypisane jej do ofpowiedniirgo vrf >>> nie wiem jak zrobic ;c
        return polaczCPE_USG(hosta,"display  nat address-group all-systems" , un, pwd)
    def C_display_curr_conf ():
        ## na chwile obecna nic z tego nie potrzebuje
        ## przyszlosciowo pobranie dnsow?
        ## sprawdzenie czy sa w konfiguracji informacje o rulce diagnostyka
        return polaczCPE_USG(hosta,"display  current-configuration", un, pwd)
    def C_ping ():
    ## tylko statystyki pingow zebrac, w przypadku wystepowania packet loss wywalic error
    ## w przypadku 100% start dodac tez pingowanie pozostalych adresow, jezeli brak pinga to nie podlaczony sw/ap
    ## dodac pingi na ap i sw
        return polaczCPE_USG(hosta, "ping 192.168.100.21" , un, pwd)

    def C_display_route_static ():
        ### pobrać z tego miejsca adresy do pingowania i nazwy VRF

        return polaczCPE_USG(hosta, "display  current-configuration | include  route-static" , un, pwd)
    def C_ping_c10_f_s1472 ():
        return polaczCPE_USG(hosta, "ping -c 10 -f -s 1472 192.168.100.21", un, pwd)
    def C_display_firewall_session_table ():
        ## regex do protokolow ^\s*([^ \t]+).* , ale tylko wtedy jezeli w linii jest adres ip
        # > nie krytyczna funkcjonalnosc
        #podusmować ilość sesji w każdym protokole, podsumowac ile adresów jest przychodzących i wychodzących
        #
        print(polaczCPE_USG(hosta, "display  firewall  session table", un, pwd))
    if czy_dostepne_urzadzenie(hosta):
        # dziala OK
        #diagnostyka_dict["VRF_instance"]=C_display_ip_vpn_instance()
        #diagnostyka_dict["ARP"]=C_display_arp()
        #diagnostyka_dict["firewall_session_table"]=C_display_firewall_session_table()
        # C_display_in_b()
        # C_display_ip_interface_b()
        # C_display_nat_add()
        # C_display_curr_conf()
        # C_ping()
        # C_display_route_static()
        # C_ping_c10_f_s1472()
        return diagnostyka_dict
    else:
        return False
### komendy do diagnostyki
###### należy dodać najpierw sprwadzenie modelu cpe, jezeli jest to model huawei, to mozna wykonac komendy huawei,
###### jeżeli jest to inny model CPE to należy przekazać inną listę z komendami
###### przygotować pare list z komendami
###### zapisać w słowniku dane do diagnostyki
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
#####wydrukowywanie na konsoli koncowej wnioskow z diagnostyki, szczegółowej
#####
#####
#####
#####
model_CPE = "uknown"
pwd = 'Ose!@#45'
un = 'ose'
### model CPE sprawdzamy
###
model_CPE=sprawdz_model_CPE(polaczCPE("10.68.10.105", "display version", un, pwd))
##### w sprawdz_model_cpe trzeba dodac regexa do wszystkich rodzajow CPE
##### w polacz cpe trzeba wpisac wszystkie komendy do sprwadzenia wersji czy to FG czy MT
print(model_CPE)
if "USG" in model_CPE:
    test=wykonaj_diagnostyke_Huawei("10.68.10.105", un, pwd)
    print(f"  test1  i test 2 ")
    # przykład odczytu słownika
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
