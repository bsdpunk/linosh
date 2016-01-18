#What does linosh try to accomplinosh?

There is already a linode shell, that is called linosh. linosh tries to do these things

```
The Linode Shell (linosh) provides console access to all of your Linodes. It also allows you to perform actions like rebooting a Linode or switching to a different configuration profile without having to open the Linode Manager. linosh is also a good rescue tool. The console provides out-of-band access to your Linode, which means you can use linosh to access your Linode even when you are unable to connect directly via SSH. This is useful if firewall settings or a bad network configuration prevent you from accessing your Linode using SSH.
```

linosh is trying to be an api complete shell for linode. Anything you can do with the api you will be able to do with linosh. linosh provides a tab completion enviroment and easy to follow instructions for launching api calls. You can script with linosh, using the command you would use in linosh.

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
Currently autocompletion works in cygwin and linux, MacOS X and FreeBSD use a different form of readline, and the autocompletion does not work. I hope to fix this in a future patch.

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
list-servers : lists your linode servers
avail-datacenters : lists available datacenters
quit : exit the shell
help : show commands and usage
```

