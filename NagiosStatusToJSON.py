#!/usr/bin/python
""" Convert the nagios realtime status data to JSON. """
import json
import re

config = {
	'statusFile': '/var/log/nagios/status.dat'
}

statusFileHandle = open(config['statusFile'], 'r')
status = statusFileHandle.read().replace("\t"," ")

hosts = {}
hostsPattern = re.compile('hoststatus \{([\S\s]*?)\}', re.DOTALL)
hostsStatus = hostsPattern.findall(status)
for hostStatus in hostsStatus:
	thisHost = { 'services': {} }
	hostPartsPattern = re.compile('([\S]*?)=(.*?)\n', re.DOTALL)
	hostParts = hostPartsPattern.findall(hostStatus)
	for hostPart in hostParts:
		thisHost[hostPart[0]] = hostPart[1]
	hosts[thisHost['host_name']] = thisHost

servicesPattern = re.compile('servicestatus \{([\S\s]*?)\}', re.DOTALL)
servicesStatus = servicesPattern.findall(status)
for serviceStatus in servicesStatus:
	thisService = {}
	servicePartsPattern = re.compile('([\S]*?)=(.*?)\n', re.DOTALL)
	serviceParts = servicePartsPattern.findall(serviceStatus)
	for servicePart in serviceParts:
		thisService[servicePart[0]] = servicePart[1]
	hosts[thisService['host_name']]['services'][thisService['service_description']] = thisService

print json.dumps(hosts, indent=4)