from netmiko import ConnectHandler
from datetime import datetime
import ipaddress
from netmiko .ssh_exception import NetMikoAuthenticationException, NetMikoTimeoutException
from getpass import getpass
import time
from multiprocessing import Process
from multiprocessing import Manager
#Begin Timer
start_time = datetime.now()
#Devices initially configured for restconf

##########################################
### If using IP's from a file -   ########
### Replace for statement as well ########
##########################################
"""
with open("ips.txt", "r") as f:
    ips = [line.strip() for line in f]
    map(ipaddress.IPv4Address, ips)
"""
##########################################
### If using subnet with unknown hosts:###
##########################################
<<<<<<< HEAD

IP_Group = [str(ip) for ip in ipaddress.IPv4Network('192.168.0.112/28')]
#Iterate through IP's and create netmiko framework for each
device_list = []
def devices():
    for ip_address in IP_Group:
        device = {
            "ip": ip_address,
            "username": "username",
            "password": "password",
            "device_type": "cisco_ios"
=======
first_ip = ipaddress.IPv4Address('192.168.0.110')
last_ip = ipaddress.IPv4Address('192.168.0.115')
IP_Range = range(int(first_ip), int(last_ip))
#Using for-loop with manual intervention
for ip_int in IP_Range:
    default = {
        'device_type': 'cisco_ios',
        'host': str(ipaddress.IPv4Address(ip_int)),
        'username': "admin",
        'password': "password",
        'timeout' : 1,
    }
    print("Connecting to " + str(ipaddress.IPv4Address(ip_int)))
    time.sleep(1)
    #Attempt logins via default creds
    try:
        net_connect = ConnectHandler(**default)
        output = net_connect.send_config_set("restconf")
        #print(f"\n\n---------- Device {a_router['device_type']} {a_router['host']}----------") - ignore for now
        net_connect.disconnect()
        print("Configuration successful")
        time.sleep(1)
        continue
    except (NetMikoTimeoutException):
        print("Device unreachable, continuing to next device")
        continue
    except (EOFError):
        print("Authentication failed, attempting logon with explicit credentials")
        time.sleep(3)
        pass   
    except (NetMikoAuthenticationException):
        print("Authentication failed, attempting logon with explicit credentials")
        time.sleep(3)
        pass
    try:
        explicit = {
            'device_type': 'cisco_ios',
            'host': str(ipaddress.IPv4Address(ip_int)),
            'username': str(input("What is your username: ")),
            'password': str(getpass()),
            'timeout' : int("1"),
>>>>>>> main
        }
        device_list.append(device)
    return device_list
#def function to connect with netmiko framework defined per ip
def send_cmd(device, L):
    try:
        with ConnectHandler(**device) as conn:
            conn.send_config_set("restconf")
            print("Connection to %s Successful" % device["ip"])
    except:
        print(f"Connection to Device {device['ip']} failed.")
        L.append(device["ip"])
#empty list to append failed devices
Failed_Devices = []
#check if running locally
if __name__ == '__main__':
    #create shared list for failed devices, start process per netmiko framework defined
    with Manager() as manager:
        L = manager.list()
        processes = []
        for device in devices():
            p = Process(target=send_cmd, args=(device, L))
            processes.append(p)
            p.start()
        # wait for process to end before termination
        for process in processes:
            process.join()
        #apply shared list to global
        Failed_Devices = list(L)

end_time = datetime.now()
total_time = end_time - start_time
print(total_time)
#Attempt manual credentials for authorization failures
if Failed_Devices == None:
    print("All Configurations Successful, Goodbye!")
else:
    choice = input("Would you like to retry failed devices with manual login? Y/n ").lower()
    if choice == "y":
        for ip_address in Failed_Devices:
            try:
                explicit = {
                    'device_type': 'cisco_ios',
                    'host': ip_address,
                    'username': str(input("What is your username: ")),
                    'password': str(getpass()),
                    'timeout' : int("1"),
                }
                net_connect = ConnectHandler(**explicit)
                output = net_connect.send_config_set("restconf")
                net_connect.disconnect()
                print("Configuration successful")
                time.sleep(1)
            except (NetMikoAuthenticationException, NetMikoTimeoutException):
                print('Failed to Connect to ' + explicit['host'])
    else:
        print("ok, goodbye")
##################################################################################################
#py render_template.py template.jinja2 data.yaml > TestTemplate.txt
# ^^^^Creates Template using the .jinja2 template and .yaml context - outputs to TestTemplate.txt^^^^
##################################################################################################
