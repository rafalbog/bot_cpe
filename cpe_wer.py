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
        ## regex do MAC adresu \b([0-9a-f-]){14}(?=.*-)\b  >> ulepszony \b([0-9a-f-]){14}\b
        ## regex do VRF \b(VRF)[_0-9A-Z]{1,}|(default)
        stdout=polaczCPE_USG(hosta, "display arp", un, pwd)

        # regex_ipv4=re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")
        # regex_MAC=re.compile(r"\b([0-9a-f-]){14}\b")
        # regex_VRF=re.compile(r"\b(VRF)[_0-9A-Z]{1,}|(default)")
        ARP_dic=[]
        tempARP=[]
        for line in stdout.splitlines():
            if re.match(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", line):
                tempARP.append(re.search(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", line).group())
            if re.match(r"\b([0-9a-f-]){14}\b",line):
                tempARP.append(re.search(r"\b([0-9a-f-]){14}\b",line).group())
            if re.match(r"\b(VRF)[_0-9A-Z]{1,}|(default)",line):
                tempARP.append(re.search(r"\b(VRF)[_0-9A-Z]{1,}|(default)",line).group())
                ############# do sprawdzenia regex!!!!!!!

            #print(tempARP)
            #ARP_dic.append(tempARP)
            #tempARP.clear()
        print(tempARP)
        return tempARP
    def C_display_in_b ():
        return polaczCPE_USG(hosta, "display interface brief", un, pwd)
    def C_display_ip_interface_b():
        return polaczCPE_USG(hosta, "display  ip interface  brief", un, pwd)
    def C_display_nat_add ():
        return polaczCPE_USG(hosta,"display  nat address-group all-systems" , un, pwd)
    def C_display_curr_conf ():
        return polaczCPE_USG(hosta,"display  current-configuration", un, pwd)
    def C_ping ():
        return polaczCPE_USG(hosta, "ping 192.168.100.21" , un, pwd)
    def C_display_route_static ():
        return polaczCPE_USG(hosta, "display  current-configuration | include  route-static" , un, pwd)
    def C_ping_c10_f_s1472 ():
        return polaczCPE_USG(hosta, "ping -c 10 -f -s 1472 192.168.100.21", un, pwd)
    def C_display_firewall_session_table ():
        return polaczCPE_USG(hosta, "display  firewall  session table", un, pwd)
    if czy_dostepne_urzadzenie(hosta):
        # dziala OK diagnostyka_dict["VRF_instance"]=C_display_ip_vpn_instance()
        diagnostyka_dict["ARP"]=C_display_arp()
        ### dodany jako słownik, przykład odwołania
        ### test["VRF_instance"][0][0] >>>  VRF_1_DATA
        ###test["VRF_instance"][1][1] >>>>11:1
        ###test["VRF_instance"][2][0]>>>> VRF_1_NOSEC

        # C_display_arp()
        # C_display_firewall_session_table
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
    print(test["VRF_instance"][0][0])
    print(test["VRF_instance"][1][1])
    print(test["VRF_instance"][2][0])
    print(test)