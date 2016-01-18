import sys
import requests
import json
from pprint import pprint
def list_servers(api_key):
    headers = {'content-type': 'application/json'}
    endpoint = "https://api.linode.com/?api_key=" + api_key + "&api_action=linode.list"
    r = requests.get(endpoint, headers=headers)
    json_data = json.loads(r.text) 
   
    return(json_data)

