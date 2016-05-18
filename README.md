#What does linosh try to accomplish?

There is already a linode shell, that is called lish. And their is a command line tool called the linode-cli. Linosh is a tool that aims to be very similiar to linode-cli and lish, but isn't complete yet.


linosh is trying to be an api complete shell for linode. Anything you can do with the api you will be able to do with linosh. linosh provides a tab completion enviroment and easy to follow instructions for launching api calls, as well as a connection agent to linode. You can script with linosh, using the command you would use in linosh.

The purpose is to more easily create scripts for things such as autoscaling and the like.

So:

```
linosh
linosh> list-servers
```
And:
```
linosh list-servers
```
Would give the same output, however the second one will not leave you in a shell so you can use it for scripting.

# Installing
To install untar, and use the python install.

```
tar -xvf linosh.tar.gz
cd linosh
sudo python setup.py install 
```
or

```
git clone https://github.com/bsdpunk/linosh.git
cd linosh
sudo python setup.py install
```
#Autocompletion

Tab completion now works on all systems

# Use
Before you can use linosh you need to generate an api key. The first time you run linosh you will be asked to supply this key.

#Linosh History
Linosh includes a history of supplied commands in ~/.linosh_history

### Example of ~/.linosh:

```
{ "default":[{ "api-key":"yourApiKey" }] } 
```

Commands currently implimented:

```
Types of arguements:
(requried) <optional>

list-servers : lists your linode servers
ip-list <linodeID> <IPAddress> : ip and server information 
avail-datacenters : lists available datacenters
avail-distributions : lists available linux distros
quit : exit the shell
help : show commands and usage
nodebal-list : get list of lode balancers    
nodebal-config-list (id): get lode balancer specifics using id from list
nodebal-node-list (config id): get node list of a balancer
```

