from __future__ import print_function
import xml.etree.ElementTree as ET
import re
import readline
import threading
import sys
import requests
import json
import os
from pprint import pprint
import signal
#from pexpect import pxssh
import random
import getpass
import urlparse
#import spur
#import ssh_script
import argparse
import pkg_resources
#from pexpect import *
#Counters and Toggles
import readline
import codecs
import unicodedata
#import cloud_network
#import images
#import dbinstance
import servers_action


#version = pkg_resources.require("linosh")[0].version
arg_count = 0
no_auth = 0
server_count = 0
database_count = 0
ddb_count = 0
hist_toggle = 0
prompt_r = 0
COMMANDS = ['list-servers','avail-datacenters', 'help', 'quit']
for arg in sys.argv:
    arg_count += 1

#warnings are ignored because of unverified ssl warnings which could ruin output for scripting
import warnings
warnings.filterwarnings("ignore")



#These are lists of things that are persistent throughout the session
tokens = {}
servers = {}
databases = {}
username = ''
ddi_bast = {}
details = {}
def complete(text, state):
    #while not state:
        for cmd in COMMANDS:
            #while not state:
                if cmd.startswith(text):
                    if not state:
                        return cmd
                    else:
                        state -= 1

#readline.parse_and_bind("tab: complete")
#readline.set_completer(complete)

#os expand must be used for 
config_file = os.path.expanduser('~/.linosh')
hist_file = os.path.expanduser('~/.linosh_history')

hfile = open(hist_file, "a")
if os.path.isfile(config_file):
    config=open(config_file, 'r')
    config=json.load(config)
else:
    #username = raw_input("Username:")
    api_key = getpass.getpass("API-Key:")
    config= {"default":[{"username":username,"api-key":api_key}]}
    
    config_file_new = open(config_file, "w")
    config_f = str(config)
    config_f = re.sub("'",'"',config_f)
    config_file_new.write(config_f)
    config_file_new.close() 

#Ending when intercepting a Keyboard, Interrupt
def Exit_gracefully(signal, frame):
    sys.exit(0)


#Sanitize this shit

def sanitize(func_type, inputs):
    ipp =re.compile('(\d+|\d)\.(\d+|\d)\.(\d+|\d)\.(\d+|\d)')
    uuidp = re.compile(".{8}-.{4}-.{4}-.{4}-.{12}")
    if func_type == "get-ip-info":
        if re.match(ipp, inputs):
            return(True)
        else:
            return(False)
        
    if func_type == "get-rack-pass":
        if re.match(uuidp, inputs) or re.match(ipp, inputs):
            return(True)
        else:
            return(False)

    if func_type == "get-user":
            if inputs.isdigit():
                return(True)
            else:
                return(False)

#DUH
def get_racker_token(config):
    signal.signal(signal.SIGINT, Exit_gracefully)
    global username
    #username = config["default"][0]["username"]
    password = config["default"][0]["api-key"]

    headers = {'content-type': 'application/json'}
    #payload = {"auth":{"RAX-AUTH:domain":{"name":"Rackspace"},"passwordCredentials":{"username":username,"password":password}}}
    #r = requests.post("https://identity-internal.api.rackspacecloud.com/v2.0/tokens", data=json.dumps(payload), headers=headers)
    #json_data = json.loads(r.text)
    try:
        #racker_token = json_data["access"]["token"]["id"]
        #print("thing")        
        return(password)
    except KeyError:
        print("Bad Credentials!")
        os.unlink(config_file)
        bye()
    return(password)
#DUH
def get_linode_key(config):
    signal.signal(signal.SIGINT, Exit_gracefully)
    global username
    #username = config["default"][0]["username"]
    password = config["default"][0]["api-key"]

    headers = {'content-type': 'application/json'}
    #payload = {"auth":{"RAX-AUTH:domain":{"name":"Rackspace"},"passwordCredentials":{"username":username,"password":password}}}
    #r = requests.post("https://identity-internal.api.rackspacecloud.com/v2.0/tokens", data=json.dumps(payload), headers=headers)
    #json_data = json.loads(r.text)
    try:
        #racker_token = json_data["access"]["token"]["id"]
        #print(password)
        return(password)
    except KeyError:
        print("Bad Credentials!")
        os.unlink(config_file)
        bye()
    return(password)

linosh_p = 'linosh'

#main command line stuff
def cli():
    while True:
        valid = 0

        signal.signal(signal.SIGINT, Exit_gracefully)
#        except EOFError:
#            bye()
        try:
            readline.parse_and_bind("tab: complete")
            readline.set_completer(complete)
            readline.set_completer_delims(' ')
            cli = str(raw_input(PROMPT))
        except EOFError:
            bye()
        if hist_toggle == 1:
            hfile.write(cli + '\n')
        if 'racker_token' in locals():
            #print("tool")
            pass
        else:
            racker_token = get_linode_key(config)    
            #print("tool")

#This is not just a horrible way to take the commands and arguements, it's also shitty way to sanatize the input for one specific scenario

#I miss perl :(


#Apparently argparse is the solution I'm looking for,I put a simple argparse example in TODO.md        
        cli = re.sub('  ',' ', cli.rstrip())
        if len(cli.split(' ')) ==2:
            command,arguement = cli.split()
            if command == "get-rack-pass":
                if sanitize('get-rack-pass', arguement):
                    print(get_rack_pass(arguement, racker_token))
                    valid = 1
                else:
                    print("This does not appear to be a valid uuid or ip: get-rack-pass 10.0.0.1 or get-rack-pass 7d9a2738-1594-4461-8cd2-5d0e76625473")
            if command == "get-imp-token":
                new_token = get_imp_token(arguement, racker_token)
                temp_dict = {arguement:new_token}
                print(new_token)
                global tokens
                tokens.update(temp_dict)
                valid = 1
            if command == "goldservers" or command == "gold":
                goldservers(arguement, racker_token)
                valid = 1 
            if command == "get-ip-info":
                if sanitize("get-ip-info", arguement):
                    pprint(get_ip_info(arguement, racker_token))
                else:
                    print("This does not appear to be a valid IP address: get-ip-info 10.0.0.1")
                valid = 1 
            if command == "get-ng-servers":
                get_ng_servers(arguement, racker_token)
                if len(servers) > 0:
                    pprint(servers)
                valid = 1 
            if command == "get-databases" or command == "gdbin":
                get_databases(arguement, racker_token)
                pprint(databases)
                valid = 1 
            if command == "get-user":
                if sanitize("get-user", arguement):
                    print(get_user(arguement, racker_token))
                    valid = 1
                else:
                    print("This does not appear to be a valid ddi: get-user 922996")
            if command == "prompt-imp":
                imp_prompt(arguement, tokens[arguement])
                valid = 1
            if command == "ssh":
                print(ssh_expect(arguement, racker_token))
                valid = 1
##########################################################################################
# This starts the single linosh commands
#######################################################################################


        if cli == "servers":
            pprint(servers)
            valid = 1
        if cli == "databases":
            pprint(databases)
            valid = 1
        if cli == "list-servers":
            api_key = get_linode_key(config)
            pprint(servers_action.list_servers(api_key))
            valid = 1
        if cli == "avail-datacenters":
            api_key = get_linode_key(config)
            pprint(servers_action.avail_datacenters(api_key))
            valid = 1
        if cli == "tokens":
            pprint(tokens)
            valid = 1
        if cli == "quit" or cli == "exit":
            hfile.close()
            bye()
        if cli == "help":
            print(help_menu())
            valid = 1
        if cli == "mytoken":
            print(racker_token)
            valid = 1
        if cli == "get-token":
            print(get_racker_token(config))
            valid = 1
        if cli.isdigit() or re.match("^https", cli):
            if no_auth == 1:
                racker_token =0
            else:
                racker_token = get_racker_token(config)
            if re.match("^https",cli):
                thesplit = cli.split('/')
                cli = thesplit[4]
                print(cli)
            
            get_ng_servers(cli, racker_token)
            pprint(ddi_bast)
            ddb_choice = raw_input("Which Server > ")
            bastion = raw_input("Bastion> ")
            bastion = ssh_script.bastion_check(bastion)
            if bastion == False:
                print("bad bastion id, use lon, dfw, lon3, hkg, iad, or syd")
            else:
                ssh_expect_bast_through(username, bastion, int(ddb_choice),racker_token)
        	
    #####################
    # This is the ssh through bastion bit that, creates an expect script to connect and passes you
    # to the script
    ##################

    if len(cli.split(' ')) ==3:
        command,arg_one,arg_two = cli.split()
        print(arg_two)
        if cli.isdigit() or re.match("^https", arg_two):
            if no_auth == 1:
                racker_token =0
            else:
                racker_token = get_racker_token(config)
            if re.match("^https",cli):
                thesplit = cli.split('/')
                cli = thesplit[4]
                print(cli)
                
            get_ng_servers(cli, racker_token)
            pprint(ddi_bast)
            ddb_choice = raw_input("Which Server > ")
            bastion = raw_input("Bastion> ")
            ssh_expect_bast_through(username, bastion, int(ddb_choice),racker_token)
            
 

        if valid == 0:
            print("Unrecoginized Command")

def get_rack_pass(uuid,token):
    if re.match('(\d+|\d)\.(\d+|\d)\.(\d+|\d)\.(\d+|\d)', uuid):
        json_ip = get_ip_info(uuid, token)
        get_uuid=json.loads(json_ip)
        uuid = get_uuid['device']

    headers = {'content-type': 'application/json',"X-Auth-Token":token}
    second_r = requests.get("https://passwords.servermill.rackspace.net/v1/"+uuid+"/password/current", headers=headers)
    rack_pass=second_r.text
    rack_pass=rack_pass[1:-1]
    return(rack_pass)


def get_ip_info(ip,token):
    headers = {'content-type': 'application/json',"X-Auth-Token":token}
    second_r = requests.get("https://ipfinder.rackspace.com/json/"+ip, headers=headers, verify=False)
    ip_info=second_r.text
    return(ip_info)



def get_user(tenant_id,token):
    headers = {'content-type': 'application/json',"X-Auth-Token":token}
    second_r = requests.get("https://customer-admin.prod.dfw1.us.ci.rackspace.net/v3/customer_accounts/CLOUD/"+tenant_id+"/contacts?role=PRIMARY", headers=headers, verify=False)
    content = second_r.text
    content = unicodedata.normalize('NFKD', content).encode('ascii','ignore')
#    content = content.decode('utf-8')
#content = unicode(content.strip(codecs.BOM_UTF8), 'utf-8')
    #content.encode('ascii', 'ignore')
    root = ET.fromstring(content)#ET.parse(second_r)
    for child in root.findall('{http://customer.api.rackspace.com/v1}contact'):
        usersname = child.get('username')
        return usersname

##Ssh fucked###################################################################################################################

def ssh_expect(server_number, token):
    global servers
    #print(server_number)
    #print(server_count)
    try:
        server_number = int(server_number)
    except ValueError:
        pass
    if isinstance( server_number, (int) ) and server_count >= server_number:
        rack_pass = get_rack_pass(servers[int(server_number)]['id'],token)
        ssh_line = "ssh rack@"+servers[int(server_number)]['ip']+"    "+rack_pass[1:-1]
        
        ip = servers[int(server_number)]['ip']
#       username = 'rack'
        password = rack_pass
        #print(password) 
        ssh_script.ssh(ip, password)
        return ssh_line
    else: 
        print("This is not a valid option")

#        
#This is an actual working expect script creator        
#It logs you into the bastion then the server you choose        
#        
def ssh_expect_bast_through(user, bastion, server_number, token):
    global servers
    #print(server_number)
    #print(server_count)
    try:
        server_number = int(server_number)
    except ValueError:
        pass
    if isinstance( server_number, (int) ) and server_count >= server_number:
        rack_pass = get_rack_pass(servers[int(server_number)]['id'],token)
        ssh_line = "ssh rack@"+servers[int(server_number)]['ip']+"    "+rack_pass[1:-1]
        
        ip = ddi_bast[int(server_number)]['ip']
        password = rack_pass
           
        ssh_script.ssh_through_bastion(user, bastion, ip, password)
        return ssh_line
    else: 
        print("This is not a valid option")


#I'm pretty sure this is defunct, just afraid to remove it yet
def ssh_expect_b(user, bastion):
    #global servers
    #print(server_number)
    #print(server_count)
    #try:
    #    server_number = int(server_number)
    #except ValueError:
    #    pass
    #if isinstance( server_number, (int) ) and server_count >= server_number:
    #    rack_pass = get_rack_pass(servers[int(server_number)]['id'],token)
    #    ssh_line = "ssh rack@"+servers[int(server_number)]['ip']+"    "+rack_pass[1:-1]
        
    #    ip = servers[int(server_number)]['ip']
#       username = 'rack'
    #    password = rack_pass
        #print(password) 
    #    ssh_script.ssh(ip, password)
    #    return ssh_line
    #else: 
    #    print("This is not a valid option")
    print(bastion)
    print(user)
    if bastion == "dfw":
        bastion = "cbast1.dfw1.corp.rackspace.com"
    ssh_script.ssh_bastion(user, bastion)    


###If you want to know why this function exists you'll have to ask me in person
def gservers(ddi, token):
    headers = {'content-type': 'application/json',"X-Auth-Token":token}
    datacenters = ['hkg', 'lon', 'iad', 'ord', 'syd', 'dfw']
    for dc in datacenters:    
        second_r = requests.get("https://"+dc+".servers.api.rackspacecloud.com/v2/"+ddi+"/servers", headers=headers, verify=False)
        if second_r.text:
            server_json=json.loads(second_r.text)
            if server_json["servers"]:
                size = len(server_json["servers"])
                print(size)
                for i in range(size):
                    global servers
                    id_name = {server_json["servers"][i]["id"]:server_json["servers"][i]["name"]}
                    servers.update(id_name)
                    print(server_json["servers"][i]["id"])
    return(second_r.text)
#############################################################################################################################
#This is the main get server function, it's used by itself and in the ssh functions
#########################################################

def get_ng_servers(ddi, token):
    if ddi.isdigit():
        true_digit =1
    else:
        print("This does not appear to be a ddi")
        return     
    if re.match('^100', ddi):
        datacenters = ['lon']
    else:
        datacenters = ['hkg', 'iad', 'ord', 'syd', 'dfw']
    admin_user = get_user(ddi,token)
    if admin_user == None:
        return(admin_user)
    imp_token = get_imp_token(admin_user, token)
    headers = {'content-type': 'application/json',"X-Auth-Token":imp_token}
    for dc in datacenters:    
        second_r = requests.get("https://"+dc+".servers.api.rackspacecloud.com/v2/"+ddi+"/servers", headers=headers, verify=False)
        if second_r.text:
            server_json=json.loads(second_r.text)
            if server_json["servers"]:
                size = len(server_json["servers"])
                #print(size)
                #The ddb stuff is for a fresh list every time, used with: linosh <ddi>
                #ddb_count = 0
                for i in range(size):
                    global servers
                    global ddi_bast
                    global server_count
                    global ddb_count
                    ddb_count += 1
                    server_count += 1
                    second_r = requests.get("https://"+dc+".servers.api.rackspacecloud.com/v2/"+ddi+"/servers/"+server_json["servers"][i]["id"], headers=headers, verify=False)
                    #print(server_json)
                    if second_r.text:
                        details = json.loads(second_r.text)
                        #if details:
                        #    print("y")
                        #else:
                        #    print("n")
                        #print(details)
                        #print(details["server"]["addresses"]["public"])
                        size_ip = len(details["server"]["addresses"]["public"])
                        #print(size_ip)
                        #if size_ip == "1":
                            #server_count -= 1
                        #print(size_ip)
                        for ip in range(size_ip):
                            #print(ip)
                        
                            if str(details["server"]["addresses"]["public"][ip]["version"]) == "4":
                                pub_ip = details["server"]["addresses"]["public"][ip]["addr"]
                                #print(pub_ip)
                        if pub_ip:         
                            id_name ={server_count: {'admin':admin_user,'ddi':ddi,'id':server_json["servers"][i]["id"], 'name':server_json["servers"][i]["name"], 'ip':str(pub_ip)}}
                            ddb ={ddb_count: {'name':server_json["servers"][i]["name"], 'ip':pub_ip}}
                            #print(ddb_count)
                            #print(server_count)
                            servers.update(id_name)
                            ddi_bast.update(ddb)
                        else:
                            print("A server did not report an IPv4 address")
                            print(details["server"])
                    else:
                        print("no details")
                        details= ""
    
    return(details)
#########################


############################Standard Servers, old servers whatever############
#A function that will probably never be finished / implimented
def goldservers(ddi, token):
    datacenters = ['hkg', 'lon', 'iad', 'ord', 'syd', 'dfw']
    admin_user = get_user(ddi,token)
    if admin_user == None:
        return(admin_user)
    imp_token = get_imp_token(admin_user, token)
    headers = {'content-type': 'application/json',"X-Auth-Token":imp_token}
    #for dc in datacenters:    
    second_r = requests.get("https://servers.api.rackspacecloud.com/v1.0/"+ddi+"/servers/detail", headers=headers, verify=False)
    #if second_r.text:
        #print(second_r.text)
    return(servers)


#####As of right now I'm not going to document this, it's hella untested
def get_databases(ddi, token):
    datacenters = ['hkg', 'lon', 'iad', 'ord', 'syd', 'dfw']
    admin_user = get_user(ddi,token)
    if admin_user == None:
        return(admin_user)
    imp_token = get_imp_token(admin_user, token)
    headers = {'content-type': 'application/json',"X-Auth-Token":imp_token}
    for dc in datacenters:    
        second_r = requests.get("https://"+dc+".databases.api.rackspacecloud.com/v1.0/"+ddi+"/instances", headers=headers, verify=False)
        if second_r.text:
            db_json=json.loads(second_r.text)
            #print(db_json)
            if db_json["instances"]:
                size = len(db_json["instances"])
                #print(size)
                for i in range(size):
                    global databases
                    global database_count
                    database_count += 1	
                    #This is so broken
                    print(db_json["instances"])

                    id_name ={database_count: {'admin':admin_user,'ddi':ddi,'name':str(db_json["instances"][i]["name"]), 'status':str(db_json["instances"][i]["status"]),'hostname':str(db_json["instances"][i]["hostname"]),'id':str(db_json["instances"][i]['id']),'size':str(db_json["instances"][i]["volume"]['size']),'size':str(db_json["instances"][i]["datastore"]["type"])}}
                    
                    databases.update(id_name)
                        #print(server_json["servers"][i]["id"])

    return(db_json)


def get_imp_token(user_id,token):
    payload = {"RAX-AUTH:impersonation": {"user": {"username": user_id},"expire-in-seconds": 10800}}
    headers = {'content-type': 'application/json',"X-Auth-Token":token}
    second_r = requests.post("https://identity-internal.api.rackspacecloud.com/v2.0/RAX-AUTH/impersonation-tokens", data=json.dumps(payload), headers=headers)
    json_return = json.loads(second_r.text)
    #print(json_return)
    return json_return["access"]["token"]["id"]


#I'm pretty sure we don't have the perms for this one

def gtenant(token):
    headers = {'content-type': 'application/json',"X-Auth-Token":token}
    second_r = requests.get("https://identity.api.rackspacecloud.com/v2.0/tenants", headers=headers, verify=False)
    return(second_r.text)


#This is supposed to drop you in an impersonation shell, it does not currently do that correctly    
def imp_prompt(ident,token):
	ident_p = ident + "> "
	imp_prompt = str(raw_input(ident_p))   
        if len(imp_prompt.split(' ')) ==2:
            imp_prompt,arguement = imp_prompt.split()
            if imp_prompt == "gservers":
                print(get_ng_servers(arguement,token))
        if imp_prompt == "gtenant":
            print(gtenant(token))

def help_menu():
####Why did I space the help like this, cause something something, then lazy
    help_var = """
list-servers : lists your linode servers
avail-datacenters : lists available centers
quit : exit the shell
help : show commands and usage

"""
    return(help_var)

def bye():
    exit()

if arg_count == 2:
    command = sys.argv[1]
#noauth is essentially for testing
    if command == "noauth":
        no_auth = 1
#history is to toggle writing a history file, there is currently no clean up so it is off by default
    if command == "history":
        hist_toggle = 1
    if command == "roulette":
        rando = random.randint(1, 3)
    if command == "extra":
        linosh_p = config["default"][0]["prompt"]

    if command.isdigit() or re.match("^https", command):
        if no_auth == 1:
            racker_token =0
        else:
            racker_token = get_racker_token(config)
        if re.match("^https",command):
            thesplit = command.split('/')
            command = thesplit[4]
            print(command)
                
        get_ng_servers(command, racker_token)
        pprint(ddi_bast)
        ddb_choice = raw_input("Which Server> ")
        bastion = raw_input("Bastion> ")
        bastion = ssh_script.bastion_check(bastion)
        #print(bastion)
        if bastion == False:
            print("bad bastion id, use lon, dfw, lon3, hkg, iad, or syd")
            bye()
        else:
            ssh_expect_bast_through(username, bastion, int(ddb_choice),racker_token)
                   

    if command == "mytoken":
        racker_token = get_racker_token(config)
        print(racker_token)
        valid = 1
        bye() 

    if command == "list-servers":
        api_key = get_linode_key(config)
        pprint(servers_action.list_servers(api_key))
        valid = 1
        bye()
    if command == "avail-datacenters":
        api_key = get_linode_key(config)
        pprint(servers_action.avail_datacenters(api_key))
        valid = 1
        bye()
 


PROMPT = linosh_p + '> '

if no_auth == 1:
    racker_token =0
else:
    racker_token = get_linode_key(config)
    #print("here")

####Again, shit way to do this, Here's hoping it's better in beta :)
    ##You know what, fuck you, it's fine
if arg_count == 3:
    command = sys.argv[1]
    arguement = sys.argv[2]
    if command == "get-ip-info":
        if sanitize("get-ip-info", arguement):
            pprint(get_ip_info(arguement, racker_token))
        else:
            print("This does not appear to be a valid IP address: get-ip-info 10.0.0.1")
        valid = 1
    if command == "get-rack-pass":
        if sanitize('get-rack-pass', arguement):
            print(get_rack_pass(arguement, racker_token))
            valid = 1
        else:
            print("This does not appear to be a valid uuid or ip: get-rack-pass 10.0.0.1 or get-rack-pass 7d9a2738-1594-4461-8cd2-5d0e76625473")
    if command == "get-imp-token":
        if arguement.isdigit():
            arguement = get_user(arguement, racker_token)
        print(get_imp_token(arguement, racker_token))
        valid = 1
    if command == "get-fg-servers":
        racker_token = get_racker_token(config)
        guser = get_user(arguement, racker_token)
        imp_token = get_imp_token(guser, racker_token) 
        pprint(servers_action.get_fg_servers(imp_token, arguement))
        valid = 1
#    if command == "gservers":
#        print(gservers(arguement, racker_token))
#        valid = 1
    if command == "get-ng-servers":
        get_ng_servers(arguement, racker_token)
        pprint(servers)
        valid = 1
    if command == "get-databases" or command == "gdbin":
        get_databases(arguement, racker_token)
        pprint(databases)
        valid = 1 
    if command == "get-user":
        if sanitize("get-user", arguement):
            print(get_user(arguement, racker_token))
            valid = 1
        else:
            print("This does not appear to be a valid ddi: get-user 922996")
    if command == "mytoken":
        print(racker_token)
        valid = 1
    if command == "ssh":
        print(ssh_expect(arguement, racker_token))
        valid = 1
    if command == "bastion":
        ssh_expect_b(username, arguement)
    bye()	    

if arg_count == 4:
    command = sys.argv[1]
    arg_one = sys.argv[2]
    arg_two = sys.argv[3]
    if command == "through":
        if no_auth == 1:
            racker_token =0
        else:
            racker_token = get_racker_token(config)
        get_ng_servers(command, racker_token)
        pprint(ddb_bast)
        #server_choice = raw_input("Server number> ")
        #bastion = raw_input("Bastion> ")
        ssh_expect_bast_through(username, bastion, int(ddb_choice),racker_token)
    if command == "get-cloud-networks":
        #print("hammer")
        racker_token = get_racker_token(config)
        guser = get_user(arg_one, racker_token)
        imp_token = get_imp_token(guser, racker_token)
        print(cloud_network.get_cloud_networks(imp_token, arg_two))
        bye()
    if command == "get-images":
        #print("hammer")
        racker_token = get_racker_token(config)
        guser = get_user(arg_one, racker_token)
        imp_token = get_imp_token(guser, racker_token)
        print(images.get_images(imp_token, arg_one, arg_two))
        bye()
    if command == "get-db-flavors":
        #print("hammer")
        racker_token = get_racker_token(config)
        guser = get_user(arg_one, racker_token)
        imp_token = get_imp_token(guser, racker_token)
        print(dbinstance.get_db_flavors(imp_token, arg_one, arg_two))
        bye()
 
#


#

if arg_count == 5:
    command = sys.argv[1]
    arg_one = sys.argv[2]
    arg_two = sys.argv[3]
    arg_three = sys.argv[4]
    #arg_four = sys.argv[5]
    if command == "set-cloud-network":
        #print("hammer")
        racker_token = get_racker_token(config)
        guser = get_user(arg_one, racker_token)
        imp_token = get_imp_token(guser, racker_token)
        print(cloud_network.set_cloud_network(imp_token, arg_two, arg_three ))



if arg_count == 6:
    command = sys.argv[1]
    arg_one = sys.argv[2]
    arg_two = sys.argv[3]
    arg_three = sys.argv[4]
    arg_four = sys.argv[5] 
    if command == "create-cloud-subnet":
        #print("hammer")
        racker_token = get_racker_token(config)
        guser = get_user(arg_one, racker_token)
        imp_token = get_imp_token(guser, racker_token)
        print(cloud_network.create_cloud_subnet(imp_token, arg_two, arg_three, arg_four ))

#######################################################################################
#
#######################################################################################
#
#######################################################################################
#
#######################################################################################
#
#######################################################################################    
#
#######################################################################################
