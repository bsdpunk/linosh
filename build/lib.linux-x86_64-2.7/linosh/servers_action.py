import sys
import requests
import json
import re
from pprint import pprint

def list_servers(api_key):
    headers = {'content-type': 'application/json'}
    endpoint = "https://api.linode.com/?api_key=" + api_key + "&api_action=linode.list"
    r = requests.get(endpoint, headers=headers)
    json_data = json.loads(r.text) 
   
    return(json_data)

def ip_list(api_key, arguement=0):
    headers = {'content-type': 'application/json'}
    ip_addy = re.compile('(\d+|\d)\.(\d+|\d)\.(\d+|\d)\.(\d+|\d)')
    lin_name = re.compile('linode(\d+)')
    #print(arguement)
    if(arguement == 0):
        endpoint = "https://api.linode.com/?api_key=" + api_key + "&api_action=linode.ip.list"
        r = requests.get(endpoint, headers=headers)
        json_data = json.loads(r.text) 

    elif re.match(ip_addy, arguement) is not None:
        print("not implimented yet")
    elif re.match(lin_name, arguement) is not None:
        p = re.match(lin_name, arguement)
        lin_id = p.group(1)
        #print(lin_id)
        endpoint = "https://api.linode.com/?api_key=" + api_key + "&api_action=linode.ip.list&LinodeID="+ lin_id
        r = requests.get(endpoint, headers=headers)
        json_data = json.loads(r.text)
        #pprint(json_data)
        json_data = json_data["DATA"][0]["IPADDRESS"]
        
        
    return(json_data)
