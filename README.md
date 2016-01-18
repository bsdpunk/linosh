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
