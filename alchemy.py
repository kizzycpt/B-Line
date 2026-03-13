from scapy.all import Ether, srp, sendp, conf, get_if_list, RandShort, RandIP, RandMAC
import ipaddress, socket, time
from rich.console import Console
from rich.table import Table
from rich.live import Live
import time
import pyfiglet
from termcolor import colored
import netifaces
import ipaddress
from identifiers.mac import get_mac, get_my_mac
from identifiers.gateway import gateway_info
from poisons.ARP import arp_cache_poison, arp_vlan_poison, arp_monitor_callback


console = Console()
gatewayscan = gateway_info()

#MAIN Execution

if __name__ == "__main__":
    title_text = pyfiglet.figlet_format("-----------\n      Alchemy \n----------", font= "slant", width=200)
    arp_scan_text = pyfiglet.figlet_format("-----------\n ARP Scan \n----------", font= "slant", width=200)
    arp_poison_emoji = r"""
                          ++++++++++++                
                      ++++++++++++++++++++            
                    ++++++++++++++++++++++++          
                   ++++++++++++++++++++++++++         
                   ++++++++++++++++++++++++++++        
                   ++++++++++++++++++++++++++++         
                   ++++++++++++++++++++++++++++         
                    ++++++++++++++++++++++++++         
                    ++++++++++++++++++++++++++         
            +++++   ++++     ++++++++     ++++    +++++
            +++++   ++++       ++++       ++++    +++++
            ++++++ +++++      ++++++      +++++ ++++++ 
            +++++++++ ++++++++++++++++++++++++ +++++++++
            ++++++++++ +++++++++   +++++++++ ++++++++++
                    +  ++++++++++++++++++  +          
                        ++++++++++++++++               
                      ++ ++++++++++++++ ++             
             ++++++++++   ++++++++++++ +++++++++++     
                ++++++++               +++++++++    
                ++++++                  ++++++       
                  ++++                    ++++       
"""
    arp_poison_text = pyfiglet.figlet_format("-----------\n ARP POISON\n----------", font= "slant", width=200)


    while True:
        console.print(f"[red]{title_text}")
        console.print("[bold green]Welcome to the Alchemy Poison Tool! \n")
        console.print("[yellow]This tool allows you to perform network scans through Requests and execute Poison (MITM) Attacks.\n")
        console.print("[red]Please ensure you have the necessary permissions/dependencies to use this tool.\n")
        choice = console.input("\n[yellow]Please Select: \n"
        "ARP Poison: [1] \n"
        "Exit: [2] \n"
        "Attack: ").strip().lower() 

        if choice == "1":
            #introductory to poison
            console.print(f"[red]{arp_poison_emoji}")
            console.print(f"[red]\n{arp_poison_text}\n")
            console.print("[yellow]------------------------------------------------------------ \n")
            
            ROUTER_INFO = gateway_info()

            arp_type = console.input("[yellow]Classic Cache Poison [1] \nVlan Cache Poison [2] \nPlease Select: ")

            if arp_type == "1":
                arp_cache_poison()
                
            elif arp_type == "2":
                arp_vlan_poison()
            else:
                        console.print("[red]Invalid choice. Please select a valid option.")
        elif choice == "2":
            console.print("[red]Exiting the tool. Goodbye!")
            break
        
        else:
            console.print("[red]Invalid choice. Please select a valid option.")
