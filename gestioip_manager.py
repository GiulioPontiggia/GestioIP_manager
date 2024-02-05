import ipaddress
import platform
import os
import requests
import time

from dotenv import load_dotenv
from prettytable import PrettyTable

# Gets credentials from .env file encrypted
load_dotenv()
cred = os.getenv("KEY")
cred = 'Basic ' + cred


# Clear screen
def clear_screen():
    op_sys = platform.platform()
    if "Windows" in op_sys:
        os.system("cls")
    else:
        os.system("clear")

class GestioIP():

    def __init__(self):
        self.choice = ''

    # Function to get a network information through API
    def get_net(self, ip, single_request=True):
        # Initialization of the table
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
            # Add each entry in the table
            for entry in response:
                if response[entry]:
                    if type(response[entry]) == dict:
                        for entr in response[entry]:
                            if response[entry][entr]:
                                net_table.add_row([entr, response[entry][entr]])
                    else:
                        net_table.add_row([entry, response[entry]])
            # Return both the response as dictionary and the table formatted
            return([response, net_table])
        except:
            if single_request:
                print(f"[*] Network {ip} not found")
    
    # Get host information through API
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
    
    def list_networks(self, site):
        net_table = PrettyTable()
        net_table.align = 'l'

        headers= {
        'Authorization' : cred
        }
        # Filter the networks based on the site name
        query_params={
                    'request_type' : 'listNetworks',
                    'client_name' : 'DEFAULT',
                    'output_type' : 'json',
                    'filter' : 'site::' + site,
                }

        url="http://10.123.86.151/gestioip/api/api.cgi"
        try:
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
        except:
            print(f"Site not found check for errors {site}")
            return None          
        
    # Change the network with a new site
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
    
    # First menu visualised at the beginning of the execution
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
                
                # Iterate from subnet mask /10 to /31
                net_requested = []
                for i in range(16, 31):
                    sm = ipaddress.IPv4Network(f"0.0.0.0/{i}", strict=False).netmask        # Finds sub mask in format x.x.x.x
                    network = ipaddress.IPv4Network(f"{self.choice}/{sm}", strict=False).network_address    # Finds the network based on ip inserted and sm
                    # For any network recall the get_network function to find network information
                    try:
                        # Request the network
                        if network not in net_requested:
                            resp = self.get_net(network, False)
                            net_requested.append(network)
                            net = resp[0]['IP']
                            mask = resp[0]['BM'] 
                            # Check if the host ip is in the network requested
                            net_obj = ipaddress.IPv4Network(f"{net}/{mask}", strict=False)
                            ip_obj = ipaddress.IPv4Address(self.choice)
                            if ip_obj in net_obj:
                                print(resp[1])

                    except:
                        continue

                input("Press ENTER to continue...")

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
                print(self.get_net(ip)[1])
                input("Press ENTER to continue...")

            elif self.choice == '2':
                clear_screen()
                net_ip = input("Network IP [x.x.x.x] or site name: ")
                new_site = input("New site: ")
                # Check if the user inserted a site or a network
                if len(net_ip.split('.')) == 4:
                    self.update_network(net_ip, new_site)
                else:
                    # Goes through all the networks of the site and print the table
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
                net_list = self.list_networks(site)
                if net_list:
                    print(net_list[1])
                input("Press ENTER to continue...")

            elif self.choice.lower().strip() == 'q':
                print("Exiting...")
                break
            else:
                continue
 
if __name__ == '__main__':
    Gestio = GestioIP()
    Gestio.quick_menu()
