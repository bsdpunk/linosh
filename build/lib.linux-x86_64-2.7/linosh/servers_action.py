import sys
import requests
import json
from pprint import pprint




#def set_db_root(imp_token, ddi, region, database):
#    headers = {'content-type': 'application/json', "X-Auth-Token":imp_token}
#    endpoint = "https://"+region+".databases.api.rackspacecloud.com/v1.0/"+ddi+"/instances/"+database+"/root"
    #"https://"+ region +".networks.api.rackspacecloud.com/v2.0/networks"
    #print(endpoint)
    #print(headers)
#    r = requests.put(endpoint, headers=headers)
    #print(r.text)
#    json_data = json.loads(r.text) 

#    return(json_data)

#def get_fg_servers(imp_token, ddi):
#    headers = {'content-type': 'application/json', "X-Auth-Token":imp_token}
#    endpoint = "https://servers.api.rackspacecloud.com/v1.0/"+ddi+"/servers"
    #"https://"+ region +".networks.api.rackspacecloud.com/v2.0/networks"
    #print(endpoint)
    #print(headers)
#    r = requests.get(endpoint, headers=headers)
    #print(r.text)
#    json_data = json.loads(r.text) 
   
#    return(json_data)

def list_servers(api_key):
    headers = {'content-type': 'application/json'}
    endpoint = "https://api.linode.com/?api_key=" + api_key + "&api_action=linode.list"
    r = requests.get(endpoint, headers=headers)
    json_data = json.loads(r.text) 
   
    return(json_data)

def avail_datacenters(api_key):
    headers = {'content-type': 'application/json'}
    endpoint = "https://api.linode.com/?api_key=" + api_key + "&api_action=avail.datacenters"
    r = requests.get(endpoint, headers=headers)
    json_data = json.loads(r.text) 
   
    return(json_data)
