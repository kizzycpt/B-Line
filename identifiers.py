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



def get_mac(ip):
   
   #MAC variables 
    arp_req = ARP(pdst = ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
   
    #ARP Packet Formula
    arp_packet = broadcast/arp_req

    #Reply loop for ARP Request
    answered, _ = srp(arp_packet, timeout = 2, verbose = 1)
    for sent, received in answered:
        return received.hwsrc
        print(received.hwsrc)

    return "No Reply"


