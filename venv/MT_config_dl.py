import paramiko
import threading

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
target_host = '10.67.132.137'
target_port = 22
pwd = 'Ose!@#45'
un = 'ose'
ssh.connect( hostname = target_host , username = un, password = pwd )
stdin, stdout, stderr = ssh.exec_command('ip dhcp-server network print  ')
for line in stdout:
 print(line)


def VRF_500_10():
    stdin, stdout, stderr = ssh.exec_command(' ping routing-table=VRF_500 src-address=192.168.10.1 8.8.8.8 count=10   ')
    for line in stdout:
        print(line.strip('\n'))

def VRF_3000_10():
    stdin, stdout, stderr = ssh.exec_command(' ping routing-table=VRF_3000 src-address=192.168.30.1 8.8.8.8 count=10   ')
    for line in stdout:
        print(line.strip('\n'))

def VRF_550_10():
    stdin, stdout, stderr = ssh.exec_command(' ping routing-table=VRF_550 src-address=192.168.15.1 8.8.8.8 count=10   ')
    for line in stdout:
        print(line.strip('\n'))
###############dodanie parunastu warunowktore sa uruchamiane w zalezcnosci od konfiguracji 
#a=threading.Thread(VRF_550_10())
#b=threading.Thread(VRF_3000_10())
#c=threading.Thread(VRF_550_10())
#d=threading.Thread(VRF_550_10())
#e=threading.Thread(VRF_500_10())
#f=threading.Thread(VRF_550_10())

#a.start()
#b.start()
#c.start()
#d.start()
#e.start()
#f.start()

ssh.close()