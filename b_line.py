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
from Identifiers import arpscan, gatewayscan
from Poisons import ARP


console = Console()

#MAIN Execution

if __name__ == "__main__":
    title_text = pyfiglet.figlet_format("-----------\n      B-Line \n----------", font= "slant", width=200)
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
        console.print("[bold green]Welcome to the B-Line Poison Tool! \n")
        console.print("[yellow]This tool allows you to perform network scans through ARP Requests and ARP Poison Attacks.\n")
        console.print("[red]Please ensure you have the necessary permissions/dependencies to use this tool.\n")
        choice = console.input("\n[yellow]Please Select: \n"
        "ARP Poison:   [1] \n"
        "Exit: [2] \n"
        "Attack: ").strip().lower() 

        if choice == "1":
            console.print(f"[red]{arp_poison_emoji}")
            console.print(f"[red]\n{arp_poison_text}\n")
            console.print("[yellow]------------------------------------------------------------ \n")
            target_ip = console.input("[yellow]| Enter Target IP:")
            ROUTER_INFO = gatewayscan.gateway_info
            if ROUTER_INFO:
                router_ip, router_mac = ROUTER_INFO
                ARP.arp_poison(target_ip=target_ip, router_ip=ROUTER_INFO[0],router_mac=ROUTER_INFO[1])
            else:
                console.print("[red]Router information is not available. Cannot proceed with ARP Poisoning.")

        elif choice == "2":
            console.print("[red]Exiting the tool. Goodbye!")
            break
        
        else:
            console.print("[red]Invalid choice. Please select a valid option.")
