#!/usr/bin/python

ip_dict = {"d1":{ "ip":"10.0.0.250", "node":"a", "rate":"c2"}, "d2": {"ip":"10.0.0.251", "node":"b", "rate":"c3"}, "d3":{"ip":"10.0.0.252", "node":"c", "rate":"c1"}, "d4":{"ip":"10.0.0.253", "node":"d", "rate":"c2"}, "d5": { "ip":"11.0.0.250", "node":"a", "rate":"c2" }, "d6": { "ip":"11.0.0.251", "node":"b", "rate":"c2" }, "d7": { "ip":"11.0.0.252", "node":"c", "rate":"c1" }, "d8": { "ip":"11.0.0.253", "node":"d", "rate":"c3" }}
#childcont = pexpect.spawn('docker exec -it '+cont+' /bin/bash')
#start(childcont, ip_dict[sys.argv[1]]["ip"],ip_dict[sys.argv[1]]["node"])
#childcont.interact()

def getIp(nodeName):
        return ip_dict[nodeName]["ip"]

def getName(nodeName):
        return ip_dict[nodeName]["node"]

def getRate(nodeName):
        return ip_dict[nodeName]["rate"]
