import paramiko
import os
import subprocess
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
target_domena= '.ose.net.pl'
typ_urzadzenia='swl'
wezly=["kra","gda","szc", "tor", "ols", "bia", "waw", "poz", "zgo", "lod", "lub", "kie", "rze", "kra", "kat", "opo","wro" ]

def polaczswl(hosta):
    #print(f" host {hosta} ")
    pwd = 'Operator!@3'
    un = 'noc'
   # target_port = 22
    proc = subprocess.Popen(
        ['ping', '-c', '1', hosta],
        stdout=subprocess.DEVNULL
    )
    proc.wait()
    #response = os.system("ping -c 1 " + hosta)
    if proc.returncode == 0:
        #print(response)
        ssh.connect(hostname=str(hosta), username=un, password=pwd)
        stdin, stdout, stderr = ssh.exec_command('show interfaces descriptions | match ae | match down ')
        ssh2=ssh.invoke_shell()
        ssh2.send("dsds")

        #print(f" host {hosta} ")
        for line in stdout:
            print(f" host {hosta} link {line} ")
        ssh.close()
    #polaczswl(wezly[0] + typ_urzadzenia + "0"+str(numer) + target_domena)

for urzadzenie in range(len(wezly)):
    for numer in range(9):
        host_docel=(wezly[urzadzenie] + typ_urzadzenia + "0" + str (numer) + target_domena)
        polaczswl(host_docel)
#print(wezly[0]+typ_urzadzenia+"01"+target_domena)
print("koniec")