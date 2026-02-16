import netifaces
import ipaddress
import requests

def gateway_info():
    try: 
        gateway = netifaces.gateways()
        gateway_ip, interface = gateway["default"][netifaces.AF_INET]
        return {"Gateway": gateway_ip}
    except Exception as e:
        print("[!]Error! {e}. Please try again. [!]")
        return {}
    