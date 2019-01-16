import paramiko
import time
import datetime
import getpass
import socket
import os

now = datetime.datetime.now()
cisco_switch_authentication_issue = []
cisco_switch_unreachable = []
cisco_asa_authentication_issue = []
cisco_asa_unreachable = []
netscreen_authentication_issue = []
netscreen_unreachable = []
srx_authentication_issue = []
srx_unreachable = []


def clear_screen():
    os.system('clear')


# 定义输入cisco switch ssh 用户名，vty密码，enable密码
def cisco_switch_creds():
    global cisco_switch_username, cisco_vty_password, cisco_enable_password
    print('\n\n')
    print('\t* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')
    print('\t*                                                           *')
    print('\t*                                                           *')
    print('\t*         Cisco Switch Auto Backup Configurator             *')
    print('\t*                                                           *')
    print('\t*                                                           *')
    print('\t* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')
    print('\n\n Please enter username, password, and enable password:\n')
    print('\t(Note that Username is the only one that shows up while typing, passwords are not shown.)\n\n')
    cisco_switch_username = input("username: ")
    cisco_vty_password = getpass.getpass("vty_password: ")
    cisco_enable_password = getpass.getpass("enable_password: ")


# 定义输入cisco asa ssh 用户名，vty密码，enable密码
def cisco_asa_creds():
    global cisco_asa_username, cisco_vty_password, cisco_enable_password
    print('\n\n')
    print('\t* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')
    print('\t*                                                           *')
    print('\t*                                                           *')
    print('\t*         Cisco ASA Auto Backup Configurator                *')
    print('\t*                                                           *')
    print('\t*                                                           *')
    print('\t* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')
    print('\n\n Please enter username, password, and enable password:\n')
    print('\t(Note that Username is the only one that shows up while typing, passwords are not shown.)\n\n')
    cisco_asa_username = input("username: ")
    cisco_vty_password = getpass.getpass("vty_password: ")
    cisco_enable_password = getpass.getpass("enable_password: ")


# 定义输入netscreen ssh 用户名，密码
def netscreen_creds():
    global netscreen_username, netscreen_vty_password
    print('\n\n')
    print('\t* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')
    print('\t*                                                           *')
    print('\t*                                                           *')
    print('\t*         Juniper Netscreen Auto Backup Configurator        *')
    print('\t*                                                           *')
    print('\t*                                                           *')
    print('\t* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')
    print('\n\n Please enter username, and password:\n')
    print('\t(Note that Username is the only one that shows up while typing, passwords are not shown.)\n\n')
    netscreen_username = input("username: ")
    netscreen_vty_password = getpass.getpass("password: ")


# 定义输入srx ssh 用户名，密码
def srx_creds():
    global srx_username, srx_vty_password
    print('\n\n')
    print('\t* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')
    print('\t*                                                           *')
    print('\t*                                                           *')
    print('\t*         Juniper SRX Auto Backup Configurator              *')
    print('\t*                                                           *')
    print('\t*                                                           *')
    print('\t* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')
    print('\n\n Please enter username, and password:\n')
    print('\t(Note that Username is the only one that shows up while typing, passwords are not shown.)\n\n')
    srx_username = input("username: ")
    srx_vty_password = getpass.getpass("password: ")


# 定义cisco switche自动备份
def cisco_switch_backup_config():
    cisco_switch_creds()
    cisco_switch_iplists = open("cisco_switch_iplists.txt", "r")
    for line in cisco_switch_iplists.readlines():
        try:
            cisco_switch_ip = line.strip()
            cisco_switch_ssh_client = paramiko.SSHClient()
            cisco_switch_ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            cisco_switch_ssh_client.connect(cisco_switch_ip, username=cisco_switch_username, password=cisco_vty_password)
            print("Sucessfully login to Cisco Switch ", cisco_switch_ip)
            cisco_switch_command = cisco_switch_ssh_client.invoke_shell()
            cisco_switch_command.send("enable" + "\r")
            cisco_switch_command.send(cisco_enable_password + "\r")
            cisco_switch_command.send("terminal length 0" + "\r")
            cisco_switch_command.send("show run" + "\r")
            time.sleep(5)
            show_run_output = cisco_switch_command.recv(65535).decode('utf8')
            cisco_switch_filename = "{}_{}-{}-{}.txt".format(cisco_switch_ip, now.month, now.day, now.year)
            file_show_run_output = open(cisco_switch_filename, "w")
            file_show_run_output.write(show_run_output)
            file_show_run_output.close()
        except paramiko.ssh_exception.AuthenticationException:
            print(cisco_switch_ip + "Authentication Failed.")
            cisco_switch_authentication_issue.append(cisco_switch_ip)
        except socket.error:
            print(cisco_switch_ip + " is Unreachable.")
            cisco_switch_unreachable.append(cisco_switch_ip)
            cisco_switch_iplists.close()
    cisco_switch_ssh_client.close()
    print('\nAuthentication Failed Cisco switches: ')
    for i in cisco_switch_authentication_issue:
        print(i)
    print('\nUnreachable Cisco switches: ')
    for i in cisco_switch_unreachable:
        print(i)
    backup_finisded()


# 定义cisco asa自动备份
def cisco_asa_backup_config():
    cisco_asa_creds()
    cisco_asa_iplists = open("cisco_asa_iplists.txt", "r")
    for line in cisco_asa_iplists.readlines():
        try:
            cisco_asa_ip = line.strip()
            cisco_asa_ssh_client = paramiko.SSHClient()
            cisco_asa_ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            cisco_asa_ssh_client.connect(cisco_asa_ip, username=cisco_asa_username, password=cisco_vty_password)
            print("Sucessfully login to Cisco ASA ", cisco_asa_ip)
            cisco_asa_command = cisco_asa_ssh_client.invoke_shell()
            cisco_asa_command.send("enable" + "\r")
            cisco_asa_command.send(cisco_enable_password + "\r")
            cisco_asa_command.send("terminal pager 0" + "\r")
            cisco_asa_command.send("show run" + "\r")
            time.sleep(5)
            asa_show_run_output = cisco_asa_command.recv(65535).decode('utf8')
            cisco_asa_filename = "{}_{}-{}-{}.txt".format(cisco_asa_ip, now.month, now.day, now.year)
            file_asa_show_run_output = open(cisco_asa_filename, "w")
            file_asa_show_run_output.write(asa_show_run_output)
            file_asa_show_run_output.close()
        except paramiko.ssh_exception.AuthenticationException:
            print(cisco_asa_ip + "Authentication Failed.")
            cisco_asa_authentication_issue.append(cisco_asa_ip)
        except socket.error:
            print(cisco_asa_ip + " is Unreachable.")
            cisco_asa_unreachable.append(cisco_asa_ip)
            cisco_asa_iplists.close()
            cisco_asa_ssh_client.close()
    print('\nAuthentication Failed Cisco ASA: ')
    for i in cisco_asa_authentication_issue:
        print(i)
    print('\nUnreachable Cisco ASA: ')
    for i in cisco_asa_unreachable:
        print(i)
    backup_finisded()


#  定义netscreen自动备份
def netscreen_backup_config():
    netscreen_creds()
    netscreen_iplists = open("netscreen_iplists.txt", "r")
    for line in netscreen_iplists.readlines():
        try:
            netscreen_ip = line.strip()
            netscreen_ssh_client = paramiko.SSHClient()
            netscreen_ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            netscreen_ssh_client.connect(netscreen_ip, username=netscreen_username, password=netscreen_vty_password)
            print("Sucessfully login to Juniper Netscreen ", netscreen_ip)
            netscreen_command = netscreen_ssh_client.invoke_shell()
            netscreen_command.send("set console page 0" + "\r")
            netscreen_command.send("get config" + "\r")
            netscreen_command.send("unset console page " + "\r")
            netscreen_command.send("save" + "\r")
            time.sleep(5)
            get_config_output = netscreen_command.recv(65535).decode('utf8')
            netscreen_filename = "{}_{}-{}-{}.txt".format(netscreen_ip, now.month, now.day, now.year)
            file_get_config_output = open(netscreen_filename, "w")
            file_get_config_output.write(get_config_output)
            file_get_config_output.close()
        except paramiko.ssh_exception.AuthenticationException:
            print(netscreen_ip + "Authentication Failed.")
            netscreen_authentication_issue.append(netscreen_ip)
        except socket.error:
            print(netscreen_ip + " is Unreachable.")
            netscreen_unreachable.append(netscreen_ip)
            netscreen_iplists.close()
    netscreen_ssh_client.close()
    print('\nAuthentication Failed Juniper Netscreen: ')
    for i in netscreen_authentication_issue:
        print(i)
    print('\nUnreachable Juniper Netscreen: ')
    for i in netscreen_unreachable:
        print(i)
    backup_finisded()


#  定义srx自动备份
def srx_backup_config():
    srx_creds()
    srx_iplists = open("srx_iplists.txt", "r")
    for line in srx_iplists.readlines():
        try:
            srx_ip = line.strip()
            srx_ssh_client = paramiko.SSHClient()
            srx_ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            srx_ssh_client.connect(srx_ip, username=srx_username, password=srx_vty_password)
            print("Sucessfully login to Juniper SRX ", srx_ip)
            srx_command = srx_ssh_client.invoke_shell()
            srx_command.send("show configuration | display set | no-more" + "\r")
            srx_command.send("show configuration | no-more" + "\r")
            time.sleep(5)
            show_config_output = srx_command.recv(65535).decode('utf8')
            srx_filename = "{}_{}-{}-{}.txt".format(srx_ip, now.month, now.day, now.year)
            file_show_config_output = open(srx_filename, "w")
            file_show_config_output.write(show_config_output)
            file_show_config_output.close()
        except paramiko.ssh_exception.AuthenticationException:
            print(srx_ip + "Authentication Failed.")
            srx_authentication_issue.append(srx_ip)
        except socket.error:
            print(srx_ip + " is Unreachable.")
            srx_unreachable.append(srx_ip)
            srx_iplists.close()
            srx_ssh_client.close()
    print('\nAuthentication Failed Juniper SRX: ')
    for i in srx_authentication_issue:
        print(i)
    print('\nUnreachable Juniper SRX: ')
    for i in srx_unreachable:
        print(i)
    backup_finisded()


def backup_finisded():
    clear_screen()
    print('\n\n')
    print('\t* * * * * * * * * * * * * * * * * * * * * * *')
    print('\t*                                           *')
    print('\t*         Backup Finished !!!               *')
    print('\t*                                           *')
    print('\t* * * * * * * * * * * * * * * * * * * * * * *')
    print('\n\n\tPlease choose the following:\n\n')
    print('\t\t1. Return to main_menu\n')
    print('\t\t2. Quit\n')
    choice = float(input("\n\nchoice: "))
    if choice == 1:
        main_menu()
    elif choice == 2:
        print("Thank You!!!")


def type_err_num():
    clear_screen()
    print('\n\n')
    print('\t* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')
    print('\t*                                                           *')
    print('\t*   Error Network Device Number !!!                         *')
    print('\t*                                                           *')
    print('\t*   Please type currect network devices number !!!          *')
    print('\t*                                                           *')
    print('\t* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')
    print('\n\n\tPlease choose the following:\n\n')
    print('\t\t1. Return to main_menu\n')
    print('\t\t2. Quit\n')
    choice = float(input("\n\nchoice: "))
    if choice == 1:
        main_menu()
    elif choice == 2:
        print("Thank You!!!")


# 定义主界面，选择网络设备
def main_menu():
    clear_screen()
    print('\n\n')
    print('\t* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')
    print('\t*                                                           *')
    print('\t*                                                           *')
    print('\t*   Welcome to Network Devices Auto Backup Configurator     *')
    print('\t*                                                           *')
    print('\t*                                                           *')
    print('\t*                          Developed by Sun                 *')
    print('\t*                                                           *')
    print('\t*                                                           *')
    print('\t* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')
    print('\n\n\tPlease choose Network Devices from the following:\n\n')
    print('\t\t1. Cisco Switch\n')
    print('\t\t2. Cisco ASA\n')
    print('\t\t3. Juniper Netscreen\n')
    print('\t\t4. Juniper SRX\n')
    print('\t\t0. Quit')
    choice = float(input("\n\nchoice network devices: "))
    if choice == 1:
        cisco_switch_backup_config()
    elif choice == 2:
        cisco_asa_backup_config()
    elif choice == 3:
        netscreen_backup_config()
    elif choice == 4:
        srx_backup_config()
    elif choice == 0:
        print("Thank You!!!")
    else:
        type_err_num()


if __name__ == '__main__':
    main_menu()
