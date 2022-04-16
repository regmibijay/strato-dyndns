# Strato-DynDNS

[![Join the chat at https://gitter.im/strato-dyndns/community](https://badges.gitter.im/strato-dyndns/community.svg)](https://gitter.im/strato-dyndns/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
![Build status](https://github.com/regmibijay/strato-dyndns/actions/workflows/main.yml/badge.svg)
[![Downloads](https://static.pepy.tech/personalized-badge/strato-dyndns?period=total&units=international_system&left_color=black&right_color=green&left_text=Downloads)](https://pepy.tech/project/strato-dyndns)


Strato-DynDNS updates your website's DNS records on DNS servers. Originally
designed for Strato. 

## Disclaimer

* This tool is in no way associated with [Strato AG](https://strato.de).
* You use this tool at your own sole responsibility.

## Currently Supported Registrars
- Strato
- Namecheap

## Installation

To install this tool, please download a suited version for your operating system from [releases](https://github.com/regmibijay/strato-dyndns/releases) page of github repository of this project. Alternatively, you can install it via pip:
```$ pip3 install strato-dyndns```

If you want v1 (which only supports strato), use ```$ pip3 install strato-dyndns==1.2.1```
## Usage:

Command Line Option | Function
------------ | -------------
```-c``` or ```--config```| inputs a configuration file, look below for configuration file syntax
```-u``` or ```--username``` | specify username
```-p``` or ```--password``` | specify password
```-d``` or ```--domain``` | specify domain
```-ip``` | specify ip address, accepts multiple IP addresses separated by spaces
```-v4``` | specifies to update IPv4 records
```-v6``` | specifies to update IPv6 records

## Python (3.6+) Library Documentation
The `DynDNSClient` library was written with importablity in mind. Full documentation to be found [here.](https://regdelivery.de/strato-dyndns)
 
## Quality of Life (QoL)
For QoL, this tool offers a functionality to read parameters from a config file.

### 1. Configuration file
A configuration file needs to be in JSON Format and needs to contain mandatory parameters ```username```, ```password``` and ```domain```.  An example config file could look like this:
```
{
  "username": "maindomain.de",
  "password": "S00p3rS3cur3_!",
  "domain": "subdomain.maindomain.de"
}
```
Please take into consideration that `username` for a Namecheap domain is actually the domain itself and `domain` is either  `@` or `www` etc. For more info about this, please read [this](https://www.namecheap.com/support/knowledgebase/article.aspx/29/11/how-to-dynamically-update-the-hosts-ip-with-an-http-request/) document.

### 2. Automation
While this script itself does not YET support chronic executions, scheduling updates are indeed possible with tools like ```crontab``` e.g.
```
#open cronjobs in editing mode
$ crontab -e  
#add strato-dyndns to list
10 10 * * 1 strato_dyndns strato -c config.conf -v4 -v6
#this would update your DNS records at 10:10 am every week.
```

### To-Do
- add a block scheduler for own scheduling mechanism
- add other domain registrars 

## Contributions
Any contribution to this tool are welcome. Any pull request, bug or issue reporting will be addressed as soon as possible.
