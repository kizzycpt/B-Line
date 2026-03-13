from scapy.all import ARP, Ether, srp
import netifaces
from identifiers.gateway import gateway_info

bad_iface_prefixes = ("lo", "vir", "docker", "br-", "veth", "vmnet", "tun", "tap")


def get_mac(ip):
    try:
        arp_req = ARP(pdst=str(ip))
        broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_packet = broadcast / arp_req

        answered, _ = srp(arp_packet, timeout=2, verbose=0)

        for _, received in answered:
            return received.hwsrc

        return None

    except Exception as e:
        print(f"[!] error [!] {e}. Please try again.")
        return None


def get_my_mac():
    try:
        for iface in netifaces.interfaces():
            if iface.startswith(bad_iface_prefixes):
                continue

            addrs = netifaces.ifaddresses(iface)
            iface_link = addrs.get(netifaces.AF_LINK)

            if not iface_link:
                continue

            my_mac = iface_link[0].get("addr")
            if my_mac and my_mac != "00:00:00:00:00:00":
                return {"Interface": iface, "MAC": my_mac}

        return None

    except Exception as e:
        print(f"Error in resolving Host MAC Address. {e}.")
        return None


def node_id(subnet, quiet=False):
    hosts = {}

    try:
        arp_req = ARP(pdst=str(subnet))
        broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_packet = broadcast / arp_req

        answered, _ = srp(arp_packet, timeout=2, verbose=0)

        for _, received in answered:
            if not quiet:
                print(f"[+] Host found: {received.psrc} - MAC: {received.hwsrc}")
            hosts[received.psrc] = received.hwsrc

        return hosts

    except Exception as e:
        print(f"Error discovering hosts: {e}")
        return {}


hosts = node_id("192.168.1.0/24")

gw = gateway_info()
router_ip = gw.get("Gateway") if gw else None
router_mac = hosts.get(router_ip) if router_ip else None
