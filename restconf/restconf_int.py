from datetime import datetime
import ipaddress
import time
import requests
import json

start_time = datetime.now()


headers = {
      "Accept" : "application/yang-data+json", 
      "Content-Type" : "application/yang-data+json", 
   }

module = "ietf-interfaces:interfaces"

first_ip = ipaddress.IPv4Address('192.168.0.110')
last_ip = ipaddress.IPv4Address('192.168.0.112')
IP_Range = range(int(first_ip), int(last_ip))

for ip_int in IP_Range:
    try:
        default = {
            'host': str(ipaddress.IPv4Address(ip_int)),
            'username': "username",
            'password': "password",
            'port' : 443

        }
        url = f"https://{default['host']}:{default['port']}/restconf/data/{module}"
        requests.packages.urllib3.disable_warnings()
        response = requests.get(url, headers=headers, auth=(default['username'], default['password']), verify = False).json()
        response = requests.get(url, headers=headers, auth=(device['username'], device['password']), verify=False).json()

        interfaces = response['ietf-interfaces:interfaces']['interface']
        for interface in interfaces:
            if bool(interface['ietf-ip:ipv4']):
                print(f"({interface['name']} -- {interface['ietf-ip:ipv4']['address'][0]['ip']})")

    except (requests.exceptions.ConnectionError):
        print("Connection Timed Out - Attempting " + str(ipaddress.IPv4Address(IP_Range[+1])))
        time.sleep(1)
        continue



