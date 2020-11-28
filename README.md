# Strato-DynDNS

Strato-DynDNS updates your website's DNS records on Strato Servers. 

## Disclaimer

* This tool is in no way associated with [Strato AG](https://strato.de).
* You use this tool at your own sole responsibility.

## Installation

To install this tool, please download a suited version for your operating system from [releases](https://github.com/regmibijay/strato-dyndns/releases) page of this website. Alternatively, you can install it via pip:
```$ pip3 install strato-dyndns```

## Usage:
Command Line Option | Function
------------ | -------------
```-i``` or ```--input```| inputs a configuration file, look below for configuration file syntax
```-v4``` | specifies to update IPv4 records
```-v6``` | specifies to update IPv6 records
```-c or``` ```--config``` | configuration wizard, creates a config file
```-q``` or ```--quiet``` | quiet mode, only fatal errors are shown in console
```-v``` or ```--version``` | shows installed version of tool
```-s``` or ```--secure``` | hides password from logs and messages

 
## Quality of Life (QoL)
For QoL, this tool offers a functionality to read parameters from a config file.

##### Configuration file
A configuration file needs to be in JSON Format and needs to contain mandatory parameters ```username```, ```password``` and ```domain```. A configuration file can be created via script with `-c` or `-config`. An example config file could look like this:
```
{
  "username": "maindomain.de",
  "password": "S00p3rS3cur3_!",
  "domain": "subdomain.maindomain.de"
}
```
##### Automation
While this script itself does not support chronic executions, scheduling updates are indeed possible with tools like ```crontab``` e.g.
```
#open cronjobs in editing mode
$ crontab -e  
#add strato-dyndns to list
10 10 * * 1 strato-dyndns -i config.conf -v4 -v6
#this would update your DNS records at 10:10 am every week.
```

## Contributions
Any contribution to this tool are welcome. Any pull request, bug or issue reporting will be addressed as soon as possible.
