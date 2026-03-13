#imports
import netifaces
from scapy.all import *
import ipaddress
import subprocess
import sys
import requests
from identifiers.gateway import gateway_info

#Gateway Variables
gws = netifaces.gateways()
router_ip, iface = gws["default"][netifaces.AF_INET]
ip_info = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]
addr  = ip_info["addr"]
mask = ip_info["netmask"]
subnet = ipaddress.IPv4Network(f"{addr}/{mask}", strict = False)







#unwanted prefixes
bad_iface_prefixes = ("lo", "docker", "wg", "br-", "veth", "virbr", "zt", "vboxnet")
