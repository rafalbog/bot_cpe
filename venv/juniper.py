
import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
target_host = '10.67.132.138'
target_port = 22
pwd = 'Operator!@3'
un = 'noc'
ssh.connect( hostname = target_host , username = un, password = pwd , port= target_port)
stdin, stdout, stderr = ssh.exec_command('show configuration interfaces | match 10.67.132.138 | display set ')


for line in stdout:
    print(line.strip('\n'))


ssh.close()