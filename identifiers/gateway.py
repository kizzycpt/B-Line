import netifaces
import ipaddress
import requests

def gateway_info():
    try: 
        gateway = netifaces.gateways()
        
        router_ip, interface = gateway["default"][netifaces.AF_INET]
        router_link = gateway.get(netifaces.AF_LINK)
        router_mac = router_link[0].get("gateway")
        return {"Gateway": router_ip,"MAC": router_mac}
    
    except Exception as e:
        print(f"[!]Error! {e}. Please try again. [!]")
        return {}
    