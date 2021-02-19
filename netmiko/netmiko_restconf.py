import sys
import yaml
from jinja2 import Environment, FileSystemLoader
from netmiko import ConnectHandler
from datetime import datetime
import os.path
import ipaddress
from netmiko .ssh_exception import NetMikoAuthenticationException, NetMikoTimeoutException
from getpass import getpass
import time
from multiprocessing import Process
from multiprocessing import Manager

start_time = datetime.now()
"""
THIS IS FOR TEMPLATING


jinjadir =  '.\jinjatemp'
#Initialize the jinja2 Environment to load templates
#from current directory
env = Environment(loader=FileSystemLoader(jinjadir))
template = env.get_template(sys.argv[1])


file = "\YAML\data.yaml"
path = os.getcwd()+file
#Load the context YAML file into a python dictionary (context)
with open(path, 'r') as datafile:
    context = yaml.load(datafile, Loader = yaml.FullLoader)

#Render the template and print the resulting document
rendered_template = template.render(**context)
print(rendered_template)

#Output result to new template file for configuration export via Netmiko
with open("FinalTemplate.py", "w") as New_Template:
    New_Template.write(rendered_template)
    New_Template.close
# testing sys.argv - print(str(sys.argv))
"""


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

IP_Group = [str(ip) for ip in ipaddress.IPv4Network('192.168.0.112/28')]

device_list = []
def devices():
    for ip_address in IP_Group:
        device = {
            "ip": ip_address,
            "username": "username",
            "password": "password",
            "device_type": "cisco_ios"
        }
        device_list.append(device)
    return device_list




def send_cmd(device, L):
    try:
        with ConnectHandler(**device) as conn:
            conn.send_config_set("restconf")
            print("Connection to %s Successful" % device["ip"])
    except:
        print(f"Connection to Device {device['ip']} failed.")
        L.append(device["ip"])

Failed_Devices = []
if __name__ == '__main__':
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
        Failed_Devices = list(L)
print(Failed_Devices)
end_time = datetime.now()
total_time = end_time - start_time
print(total_time)



if Failed_Devices == None:
    print("OK BYE")
else:
    choice = input("Would you like to retry failed devices with manual login? Y/n ").lower()
    if choice == "y":
        for ip_address in Failed_Devices:
                device = {
                    "ip": ip_address,
                    "username": prompt("Give a Username: "),
                    "password": getpass(),
                    "device_type": "cisco_ios"
                }
        try:
            with ConnectHandler(**device) as connection:
                conn.send_config_set("restconf")
                print("Configuration Successful")
        except:
            print("Ya failed again chief")
        else:
            print("Too Bad!")


"""
def run_script(ip):
    default = {
        'device_type': 'cisco_ios',
        'host': ip,
        'username': "username",
        'password': "password",
        'timeout' : 1,
    }
    print("test")
    #Attempt logins via default creds
    try:
        net_connect = ConnectHandler(**default)
        output = net_connect.send_config_set("restconf")
        #print(f"\n\n---------- Device {a_router['device_type']} {a_router['host']}----------") - ignore for now
        net_connect.disconnect()
        print("successful")
    except (NetMikoTimeoutException) as e:
        Failed_IPs.append(ip)      
    except (EOFError) as e:
        Failed_IPs.append(ip)      
    except (NetMikoAuthenticationException) as e:
        Failed_IPs.append(ip)      
"""




"""

    try:
        explicit = {
            'device_type': 'cisco_ios',
            'host': ip,
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



"""














##################################################################################################
#py render_template.py template.jinja2 data.yaml > TestTemplate.txt
# ^^^^Creates Template using the .jinja2 template and .yaml context - outputs to TestTemplate.txt^^^^
##################################################################################################
