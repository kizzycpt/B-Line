import netifaces
import ipaddress
import requests
import sys
import subprocess


def arp_router_mac(ip: str) -> str | None:
    try:
        if sys.platform.startswith("linux"):
            # ip neigh show <ip>
                out = subprocess.check_output(["ip", "neigh", "show", ip], text=True, stderr=subprocess.DEVNULL)
                m = re.search(r"lladdr\s+([0-9a-f:]{17})", out, re.IGNORECASE)
                return m.group(1).lower() if m else None

        elif sys.platform == "darwin":
                # arp -n <ip>
                out = subprocess.check_output(["arp", "-n", ip], text=True, stderr=subprocess.DEVNULL)
                m = re.search(r"at\s+([0-9a-f:]{17})", out, re.IGNORECASE)
                return m.group(1).lower() if m else None

        elif sys.platform.startswith("win"):
            # arp -a <ip> (may list all entries; filter by IP)
            out = subprocess.check_output(["arp", "-a"], text=True, stderr=subprocess.DEVNULL)
            for line in out.splitlines():
                if ip in line:
                    m = re.search(r"([0-9a-f]{2}[-:]){5}[0-9a-f]{2}", line, re.IGNORECASE)
                    return m.group(0).replace("-", ":").lower() if m else None
            return None
        else:
            return None
    except Exception:
        return None

def gateway_info():
    try:
        gws = netifaces.gateways()
        default = gws.get("default", {}).get(netifaces.AF_INET)
        if not default:
            print("[!] Router information is not available (no IPv4 default gateway). Cannot proceed with ARP")
            return None

        router_ip, interface = default

        # Best-effort MAC lookup. Often requires that the router_ip is in ARP/neighbor cache.
        router_mac = arp_router_mac(router_ip)

        info = {"Gateway": router_ip, "Interface": interface, "MAC": router_mac}
        if not router_mac:
            print("[!] Found gateway IP but could not resolve MAC from neighbor/ARP table (yet).")
            # Optional: you can ping the gateway once to populate ARP cache, then retry.
        return info

    except Exception as e:
        print(f"[!]Error! {e}. Please try again. [!]")
        return None
