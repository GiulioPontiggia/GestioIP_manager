import json
import itertools
import platform
import os
import sys
import requests
import time

from dotenv import load_dotenv
from prettytable import PrettyTable

load_dotenv()
cred = os.getenv("KEY")
cred = 'Basic ' + cred

def match_sm_ip(ip, sm):
    net = ''
    for (x, y) in zip(ip.split('.'), sm.split('.')):
        x = int(x)
        y = int(y)
        net += str(x & y)
        net += '.'
    return(net[:-1])


def clear_screen():
    op_sys = platform.platform()
    if "Windows" in op_sys:
        os.system("cls")
    else:
        os.system("clear")
class GestioIP():

    def __init__(self):
        self.choice = ''

    def get_net(self, ip):
        net_table = PrettyTable()
        net_table.align = 'l'
        headers= {
        'Authorization' : cred
        }

        query_params={
                    'request_type' : 'readNetwork',
                    'output_type' : 'json',
                    'client_name' : 'DEFAULT',
                    'ip' : ip
                }

        url="http://10.123.86.151/gestioip/api/api.cgi"
        try:
            response = requests.get(url, headers=headers, params=query_params, verify=False)
            response = response.json()
            response = response["readNetworkResult"]["Network"]
            net_table.field_names = ["Field", "Value"]
            for entry in response:
                if response[entry]:
                    if type(response[entry]) == dict:
                        for entr in response[entry]:
                            if response[entry][entr]:
                                net_table.add_row([entr, response[entry][entr]])
                    else:
                        net_table.add_row([entry, response[entry]])
            return([response, net_table])
        except:
            None
        
    def get_host(self, ip):
        clear_screen()
        host_table = PrettyTable()
        host_table.align = 'l'
        headers= {
        'Authorization' : cred
        }

        query_params={
                    'request_type' : 'readHost',
                    'output_type' : 'json',
                    'client_name' : 'DEFAULT',
                    'ip' : ip
                }

        url="http://10.123.86.151/gestioip/api/api.cgi"
        try:
            response = requests.get(url, headers=headers, params=query_params, verify=False)
            response = response.json()
            response = response["readHostResult"]["Host"]
            host_table.field_names = ["Field", "Value"]
            for entry in response:
                if response[entry]:
                    if type(response[entry]) == dict:
                        for entr in response[entry]:
                            if response[entry][entr]:
                                host_table.add_row([entr, response[entry][entr]])
                    else:
                        host_table.add_row([entry, response[entry]]) 
            print(host_table)
        except:
            print(f"Host not found, check the IP address ({ip})...")
    
    def quick_menu(self):
        while True:
            clear_screen()
            if self.choice == 'q':
                break
            menu = '''
                  ____           _   _      ___ ____  
                 / ___| ___  ___| |_(_) ___|_ _|  _ \ 
                | |  _ / _ \/ __| __| |/ _ \| || |_) |
                | |_| |  __/\__ \ |_| | (_) | ||  __/ 
                 \____|\___||___/\__|_|\___/___|_|    

                [*]  QUICK MENU:
                [x.x.x.x] IP
                [m]  Full Menu                        
                [q]  Exit
                '''
            print(menu)
            self.choice = input("Insert choice: ")
            if self.choice.lower().strip() == 'm':
                self.menu()
            elif self.choice.lower().strip() == 'q':
                break
            else:
                self.get_host(self.choice)
                net_requested = []
                for i in range(0, 17):
                    if i <= 8:
                        m = '255.255.255.' + str(2**i - 1)
                    else:
                        m = ('255.255.' + str(2**(8-(i-8)) -1) +  '.0')

                    network = match_sm_ip(self.choice, m)
                    
                    try:
                        if network not in net_requested:
                            net_requested.append(network)
                            resp = self.get_net(network)
                            data = resp[0]
                            table = resp[1]
                            if int(data['BM']) <= 24:
                                sub_mas = '255.255.' + str(2**(int(data['BM'])-16)-1) + '.0'
                            else:
                                sub_mas = '255.255.255.' + str(2**(int(data['BM'])-24)-1)
                            if match_sm_ip(self.choice, sub_mas) == data['IP']:
                                print(table)
                    except:
                        continue
                input("Press ENTER to continue...")

    def list_networks(self, site):
        net_table = PrettyTable()
        net_table.align = 'l'

        headers= {
        'Authorization' : cred
        }

        query_params={
                    'request_type' : 'listNetworks',
                    'client_name' : 'DEFAULT',
                    'output_type' : 'json',
                    'filter' : 'site::' + site,
                }

        url="http://10.123.86.151/gestioip/api/api.cgi"
        response = requests.get(url, headers=headers, params=query_params, verify=False)
        response = response.json()['listNetworksResult']['NetworkList']['Network']
        networks = []
        net_table.field_names = ["Network", "Site", "Category","Comment", "VLAN"]
        for entry in response:
            net = entry.split(',')
            add_row = []
            for i in net:
                if i:
                    add_row.append(i)
            net_table.add_row(net)
            networks.append(add_row)
        
        return([networks, net_table])
        
    def update_network(self, net_ip, new_site):

        headers= {
        'Authorization' : cred
        }

        query_params={
                    'request_type' : 'updateNetwork',
                    'client_name' : 'DEFAULT',
                    'ip' : net_ip,
                    'new_site' : new_site
                }

        url="http://10.123.86.151/gestioip/api/api.cgi"
        response = requests.get(url, headers=headers, params=query_params, verify=False)
        print(response)

    def menu(self):
        
        while True:
            clear_screen()
            menu = '''
                  ____           _   _      ___ ____  
                 / ___| ___  ___| |_(_) ___|_ _|  _ \ 
                | |  _ / _ \/ __| __| |/ _ \| || |_) |
                | |_| |  __/\__ \ |_| | (_) | ||  __/ 
                 \____|\___||___/\__|_|\___/___|_|    

                [*]  MENU:                        
                [1]  get network 
                [2]  change network site    
                [3]  get site's networks        
                [q]  Exit
                '''
            print(menu)
            self.choice = input("\n[ ] choice: ")
            if self.choice == '1':
                clear_screen()
                ip = input("Network IP [x.x.x.x]: ")
                self.get_net(ip)
                input("Press ENTER to continue...")
            elif self.choice == '2':
                clear_screen()
                net_ip = input("Network IP [x.x.x.x] or site name: ")
                new_site = input("New site: ")
                if len(net_ip.split('.')) == 4:
                    self.update_network(net_ip, new_site)
                else:
                    net_list = self.list_networks(net_ip)[0]
                    for net in net_list:
                        network = net[0]
                        index = network.find('/')
                        network = network[:index]
                        self.update_network(network, new_site)
                input("Press ENTER to continue...")

            elif self.choice == '3':
                clear_screen()
                site = input('Site: ')
                print(self.list_networks(site)[1])
                input("Press ENTER to continue...")
            elif self.choice == '4':
                clear_screen()
                print("WIP")
            elif self.choice.lower().strip() == 'q':
                print("Exiting...")
                break
            else:
                print("Input Error...")
 
if __name__ == '__main__':
    Gestio = GestioIP()
    Gestio.quick_menu()
