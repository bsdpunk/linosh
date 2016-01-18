#What does linosh try to accomplish?

There is already a linode shell, that is called lish. Lish tries to do these things

```
The Linode Shell (Lish) provides console access to all of your Linodes. It also allows you to perform actions like rebooting a Linode or switching to a different configuration profile without having to open the Linode Manager. Lish is also a good rescue tool. The console provides out-of-band access to your Linode, which means you can use Lish to access your Linode even when you are unable to connect directly via SSH. This is useful if firewall settings or a bad network configuration prevent you from accessing your Linode using SSH.
```

Lish is trying to be an api complete shell for linode. Anything you can do with the api you will be able to do with linosh. Lish provides a tab completion enviroment and easy to follow instructions for launching api calls. You can script with linosh, using the command you would use in linosh.

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

# Use
Before you can use linosh you need to generate an api key. The first time you run linosh you will be asked to supply this key.

### Example:

```
{ "default":[{ "api-key":"yourApiKey" }] } 
```

Commands:

```
list-servers : lists your linode servers
quit : exit the shell
help : show commands and usage
```
