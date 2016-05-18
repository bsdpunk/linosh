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
import random
import getpass
import urlparse
import argparse
import pkg_resources
#Counters and Toggles
import readline
import codecs
import unicodedata
import servers_action
import lin_utility
import node_balance
import readline
import rlcompleter
import domain
#version = pkg_resources.require("linosh")[0].version

arg_count = 0
no_auth = 0
server_count = 0
database_count = 0
ddb_count = 0
hist_toggle = 0
prompt_r = 0

#For tab completion
COMMANDS = ['list-images','linode-disk-dist','domain-resource-list','domain-resource-create','list-domains','linode-shutdown', 'avail-stackscripts','avail-plans','linode-create','nodebal-create', 'nodebal-config-list','nodebal-node-list','nodebal-list', 'list-servers','ip-list', 'avail-datacenters', 'avail-distributions', 'help', 'quit']

#For X number of arguements
ONE = ['list-images','list-domains', 'ip-list', 'list-servers', 'avail-datacenters', 'avail-distributions', 'avail-plans', 'avail-stackscripts', 'nodebal-list']
TWO = ['ip-list', 'nodebal-node-list', 'nodebal-config-list', 'nodebal-create', 'linode-shutdown','domain-resource-list']
THREE = ['linode-create','domain-resource-list']
FOUR = ['domain-resource-create']
FIVE = ['domain-resource-create']
SIX = ['linode-disk-dist']
#For what class
DOMAIN= ['domain-resource-create','list-domains','domain-resource-list']
SA = ['list-images','list-servers','ip-list','linode-create', 'linode-shutdown','linode-disk-dist']
LU = ['avail-datacenters', 'avail-distributions', 'avail-plans', 'avail-stackscripts']
NB = ['nodebal-list', 'nodebal-node-list', 'nodebal-config-list', 'nodebal-create']
HELPER = ['help', 'quit', 'exit']


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
        for cmd in COMMANDS:
                if cmd.startswith(text):
                    if not state:
                        return cmd
                    else:
                        state -= 1


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



#DUH
def get_linode_key(config):
    signal.signal(signal.SIGINT, Exit_gracefully)
    global username
    password = config["default"][0]["api-key"]

    headers = {'content-type': 'application/json'}
    try:
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
            #readline.parse_and_bind("tab: complete")
            if 'libedit' in readline.__doc__:
                readline.parse_and_bind("bind ^I rl_complete")
            else:
                readline.parse_and_bind("tab: complete")

            readline.set_completer(complete)
            readline.set_completer_delims(' ')
            cli = str(raw_input(PROMPT))
        except EOFError:
            bye()
        if hist_toggle == 1:
            hfile.write(cli + '\n')
        if 'linode_token' in locals():
            #print("tool")
            pass
        else:
            linode_token = get_linode_key(config)    
            #print("tool")

#This is not just a horrible way to take the commands and arguements, it's also shitty way to sanatize the input for one specific scenario

#I miss perl :(


#Apparently argparse is the solution I'm looking for,I put a simple argparse example in TODO.md        
        cli = re.sub('  ',' ', cli.rstrip())
            

#        if len(cli.split(' ')) ==3:
#            command,arg_one,arg_two = cli.split()
#            if command == "linode-create":
#                api_key = get_linode_key(config)
#                print(servers_action.linode_create(api_key,arg_one,arg_two))
#                valid = 1
 

##########################################################################################
# This starts the single linosh commands
#######################################################################################

        api_key = get_linode_key(config)
        #Write try statement here for error catching
        command = cli.split(' ', 1)[0]

        if command in DOMAIN:
            l_class = 'domain'
        elif command in SA:
            l_class = 'servers_action'
        elif command in LU:
            l_class = 'lin_utility'
        elif command in NB:
            l_class = 'node_balance'
        else:
            l_class = ''       

        if len(cli.split(' ')) > 0:
            if len(cli.split(' ')) ==6:
                command,arg_one,arg_two,arg_three,arg_four,arg_five = cli.split()
                if command in SIX:
                    command = command.replace("-", "_")
                    l_class = eval(l_class)
                    result = getattr(l_class, command)(api_key, arg_one, arg_two,arg_three,arg_four,arg_five)
                    print(result)
                    valid = 1

            if len(cli.split(' ')) ==5:
                command,arg_one,arg_two,arg_three,arg_four = cli.split()
                if command in FIVE:
                    command = command.replace("-", "_")
                    l_class = eval(l_class)
                    result = getattr(l_class, command)(api_key, arg_one, arg_two,arg_three,arg_four)
                    print(result)
                    valid = 1

            if len(cli.split(' ')) ==4:
                command,arg_one,arg_two,arg_three = cli.split()
                if command in FOUR:
                    command = command.replace("-", "_")
                    l_class = eval(l_class)
                    result = getattr(l_class, command)(api_key, arg_one, arg_two,arg_three)
                    print(result)
                    valid = 1

            if len(cli.split(' ')) ==3:
                command,arg_one,arg_two = cli.split()
                if command in THREE:
                    command = command.replace("-", "_")
                    l_class = eval(l_class)
                    result = getattr(l_class, command)(api_key, arg_one, arg_two)
                    print(result)
                    valid = 1

                valid = 1
            elif len(cli.split(' ')) ==2:
                command,arguement = cli.split()
                if command in TWO:
                    command = command.replace("-", "_")
                    l_class = eval(l_class)
                    result = getattr(l_class, command)(api_key, arguement)
                    print(result)
                    valid = 1
                
                else:
                    print("Invalid Arguements")

            else:
               if cli in ONE:                    
                    cli = cli.replace("-", "_")
                    l_class = eval(l_class)
                    result = getattr(l_class, cli)(api_key)
                    print(result)
                    valid = 1
               elif cli in HELPER:
                    if cli == "quit" or cli == "exit":
                        hfile.close()
                        bye()
                    if cli == "help":
                        print(help_menu())
                        valid = 1
               else:
                    print("Invalid Command")



        if valid == 0:
            print("Unrecoginized Command")


def help_menu():
####Why did I space the help like this, cause something something, then lazy
    help_var = """
(required) <optional>

list-servers : lists your linode servers
linode-create (DatacenterID) (PlanID) <PaymentTerm>: create Linode
ip-list <linode_id> <IPaddress> : return JSON information about ip address and server 
avail-datacenters : lists available centers
avail-distributions : lists available distribution centers
quit : exit the shell
nodebal-list : get list of lode balancers    
nodebal-config-list (id): get lode balancer specifics using id from list
nodebal-node-list (config id): get node list of a balancer
nodebal-create (DatacenterID): create node balancer
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

                 

    if command == "list-servers":
        api_key = get_linode_key(config)
        pprint(servers_action.list_servers(api_key))
        valid = 1
        bye()
    if command == "avail-datacenters":
        api_key = get_linode_key(config)
        pprint(lin_utility.avail_datacenters(api_key))
        valid = 1
        bye()
    if command == "avail-stackscripts":
        api_key = get_linode_key(config)
        pprint(lin_utility.avail_stackscripts(api_key))
        valid = 1
        bye()
    if command == "avail-distributions":
        api_key = get_linode_key(config)
        pprint(lin_utility.avail_distributions(api_key))
        valid = 1
        bye()
    if command == "avail-plans":
        api_key = get_linode_key(config)
        pprint(lin_utility.avail_plans(api_key))
        valid = 1
        bye()
    if command == "nodebal-list":
        api_key = get_linode_key(config)
        pprint(node_balance.nodebal_list(api_key))
        valid = 1
        bye()
    if command == "ip-list":
        api_key = get_linode_key(config)
        pprint(servers_action.ip_list(api_key))
        valid = 1
        bye()



PROMPT = linosh_p + '> '

if no_auth == 1:
    api_key =0
else:
    api_key = get_linode_key(config)

####Again, shit way to do this, Here's hoping it's better in beta :)
    ##You know what, fuck you, it's fine
if arg_count == 3:
    command = sys.argv[1]
    arguement = sys.argv[2]
    if command == "ip-list":
        print(servers_action.ip_list(api_key, arguement))
        valid = 1
        bye()
    if command == "linode-shutdown":
        print(servers_action.linode_shutdown(api_key, arguement))
        valid = 1
        bye()
    if command == "nodebal-node-list":
        api_key = get_linode_key(config)
        print(node_balance.nodebal_node_list(api_key, arguement))
        valid = 1
        bye()
    if command == "nodebal-config-list":
        api_key = get_linode_key(config)
        print(node_balance.nodebal_config_list(api_key, arguement))
        valid = 1
        bye()
    if command == "nodebal-config-list":
        api_key = get_linode_key(config)
        print(node_balance.nodebal_create(api_key, arguement))
        valid = 1
        bye()

 

if arg_count == 4:
    command = sys.argv[1]
    arg_one = sys.argv[2]
    arg_two = sys.argv[3]
    arg_three = sys.argv[4]
    arg_four = sys.argv[5]

    if command == "linode-create":
        api_key = get_linode_key(config)
        print(servers_action.linode_create(api_key, arg_one, arg_two))
        valid = 1
        bye()


 

if arg_count == 5:
    command = sys.argv[1]
    arg_one = sys.argv[2]
    arg_two = sys.argv[3]
    arg_three = sys.argv[4]
    arg_four = sys.argv[5]

if arg_count == 6:
    command = sys.argv[1]
    arg_one = sys.argv[2]
    arg_two = sys.argv[3]
    arg_three = sys.argv[4]
    arg_four = sys.argv[5] 
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
