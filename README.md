# XmlRpcbf

It is a python script to brute force against the WordPress XML-RPC interface. This type of attack is only possible when this feature is enabled.

The following request to the target site reveals when XML-RPC is enabled.

```
root@parrot:~$ curl http://www.wpsite/xmlrpc.php
XML-RPC server accepts POST requests only.
```


## Installation

```
git clone https://github.com/ret2x-tools/xmlrpc-brute-force.git
pip install -r requirements.txt
```


## Usage

```
root@parrot:~$ python3 XmlRpcbf.py -h
usage: XmlRpcbf.py [-h] [-u url] [-l USERNAME] [-L USERFILE] [-P PASSFILE] [-t THREADS]

XML-RPC Simple Brute Force Attack

optional arguments:
  -h, --help         show this help message and exit
  -u url, --url url  target url (e.g. http://www.wpsite.com)
  -l USERNAME        username
  -L USERFILE        user_file.txt
  -P PASSFILE        pass_file.txt
  -t THREADS         default 5

Examples: 
XmlRpcbf.py -u http://www.wpsite.com -l admin -P passfile.txt
XmlRpcbf.py -u http://www.wpsite.com -L userfile.txt -P passfile.txt
```
