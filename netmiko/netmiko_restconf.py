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
from multiprocessing import Pool
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

IP_Group = [str(ip) for ip in ipaddress.IPv4Network('192.128.0.0/29')]

def run_script(ip):
    default = {
        'device_type': 'cisco_ios',
        'host': ip,
        'username': "admin",
        'password': "password",
        'timeout' : 1,
    }
    print("Connecting to " + str(ip))
    time.sleep(1)
    #Attempt logins via default creds
    try:
        net_connect = ConnectHandler(**default)
        output = net_connect.send_config_set("restconf")
        #print(f"\n\n---------- Device {a_router['device_type']} {a_router['host']}----------") - ignore for now
        net_connect.disconnect()
        print("Configuration successful")
        time.sleep(1)
        
    except (NetMikoTimeoutException):
        print("Device unreachable, continuing to next device")
        
    except (EOFError):
        print("Authentication failed, attempting logon with explicit credentials")
        time.sleep(3)
           
    except (NetMikoAuthenticationException):
        print("Authentication failed, attempting logon with explicit credentials")
        time.sleep(3)
        
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

if __name__ == "__main__":
    # Pool(5) means 5 process / devices will be run at a time, until youve gone through the device list
    with Pool(5) as p:
        print(p.map(run_script, IP_Group))


end_time = datetime.now()
total_time = end_time - start_time
print(total_time)


























##################################################################################################
#py render_template.py template.jinja2 data.yaml > TestTemplate.txt
# ^^^^Creates Template using the .jinja2 template and .yaml context - outputs to TestTemplate.txt^^^^
##################################################################################################
