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

#Unwanted interface prefixes
bad_iface_prefixes = ("lo", "docker", "wg", "br-", "veth", "virbr", "zt", "vboxnet")



def get_mac(ip):
   
   #MAC variables 
    arp_req = ARP(pdst = ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
   
    #ARP Packet Formula
    arp_packet = broadcast/arp_req

    #Reply loop for ARP Request
    answered, _ = srp(arp_packet, timeout = 2, verbose = 0)
    for sent, received in answered:
        return received.hwsrc

    return None


def get_my_mac():
    try:
        for iface in netifaces.interfaces():
            if iface.startswith(bad_iface_prefixes):
                continue
            
        addrs = netifaces.ifaddresses()

        iface_link = addrs.get(netifaces.AF_LINK)
        

        my_mac = iface_link[0].get("addrs")
        if my_mac and my_mac != "00:00:00:00:00:00":
            return {"Interface": iface, "MAC": my_mac}



    except Exception as e:
        print(f"Error in resolving MAC Address. {e}.")
        return {}


