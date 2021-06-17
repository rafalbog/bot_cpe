import paramiko
import subprocess
import re
diagnostyka_dict={}

## sprawdzenie czy
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
def polaczCPE_USG(hosta, command, un, pwd):
    ssh2 = paramiko.SSHClient()
    ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh2.connect(hostname=hosta, username=un, password=pwd)
    stdin, stdout, stderr = ssh2.exec_command(command)
    ## przy dluzszej komendzie, huawei oczekuje na potwierdzenie wydruku
    stdin.write("                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         ")
    print(stderr)

    stdout= stdout.readlines() ## czytanie linii z terminala
    for line in stdout:
        print(line)
    ssh2.close()
    return stdout

def sprawdz_model_CPE(stdout_ssh):
    for line in stdout_ssh:
        wersja = re.match("^USG?.{1}[0-9]{1,3}", line)
        if re.match("^USG?.{1}[0-9]{1,3}", line):
            return wersja.group()
    return False


def wykonaj_diagnostyke(hosta, command, un, pwd):

    if czy_dostepne_urzadzenie(hosta):
        for key, value in command.items():
            print(hosta, value, un, pwd)
            print("testing")
            print(polaczCPE_USG(hosta, value, un, pwd))
            #diagnostyka_dict=polaczCPE_USG(hosta, value, un, pwd)

        return diagnostyka_dict
    else:
        return False


### komendy do diagnostyki
command_dict={
"C_display_version" : "display version",
"C_display_ip_vpn_instance ": "display  ip vpn-instance",
"C_display_arp": "display arp",
"C_display_ip_interface_b": "display  ip interface  brief",
"C_display_in_b":  "display interface brief",
"C_display_nat_add": "display  nat address-group all-systems",
"C_display_curr_conf": "display  current-configuration",
"C_ping":"ping 192.168.100.21",
"C_display_route_static":" display  current-configuration | include  route-static",
## trudne do określenia działanie prawidłowe pingu powyżej c100
"C_ping_c10_f_s1472":"ping -c 10 -f -s 1472 192.168.100.21",
"C_display_firewall_session_table":"display  firewall  session table"
#"C_ssh_sw_ping":" system-view"
}


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
#####wydrukowywanie na konsoli koncowej wnioskow z diagnostyki, szczegółowej i opisanie co dlaczego dobrze dziala
#####z pinga tylko wydruk podsumowania i adresow pingow
#####
#####
#####





model_CPE = "uknown"
pwd = 'Ose!@#45'
un = 'ose'
test=wykonaj_diagnostyke("10.68.10.105", command_dict, un, pwd)
#test2=wykonaj_diagnostyke("10.65.16.161", command_dict, un, pwd)
#print(f"{test}  test1  i test 2 ")

print(test)