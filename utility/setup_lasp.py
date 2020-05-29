#!/usr/bin/python

import pexpect
import subprocess
import sys
import node_directory as ND

#print(ND.getIp('d1'))
#print(ND.getName('d1'))
#print(ND.getRate('d1'))
print(sys.argv[1])
ip_dict = {"d1":{ "ip":"10.0.0.250", "node":"a", "rate":"c2"}, "d2": {"ip":"10.0.0.251", "node":"b", "rate":"c3"}, "d3":{"ip":"10.0.0.252", "node":"c", "rate":"c1"}, "d4":{"ip":"10.0.0.253", "node":"d", "rate":"c2"}, "d5": { "ip":"11.0.0.250", "node":"a", "rate":"c2" }, "d6": { "ip":"11.0.0.251", "node":"b", "rate":"c2" }, "d7": { "ip":"11.0.0.252", "node":"c", "rate":"c1" }, "d8": { "ip":"11.0.0.253", "node":"d", "rate":"c3" }}
nodeId = sys.argv[1]
print("ip:"+ND.getIp(nodeId))
print("node:"+ND.getName(nodeId))
cont = "mn."+nodeId
#print("ip:"+ip_dict[nodeId]["ip"])
#print("node:"+ip_dict[nodeId]["node"])
#childcont = pexpect.spawn('docker exec -it '+cont+' /bin/bash')
#start(childcont, ip_dict[sys.argv[1]]["ip"],ip_dict[sys.argv[1]]["node"])
#childcont.interact()


def start(ip, node, rate):
    child  = pexpect.spawn('docker exec -it '+cont+' /bin/bash')
    c_prompt = 'root@'
    child.expect (c_prompt)
    child.sendline('export PEER_SERVICE=partisan_hyparview_peer_service_manager')
    child.expect(c_prompt)
    child.sendline('export RATE_CLASS='+rate)
    child.expect(c_prompt)
    child.sendline('export PROPAGATE_ON_UPDATE=false')
    child.expect(c_prompt)
    child.sendline('cd /opt/lasp')
    child.expect(c_prompt)
    child.sendline('epmd -daemon')
    child.expect(c_prompt)
    child.sendline('rebar3 shell --name '+node+'@'+ip)
    child.expect("Application lasp started on node '"+node+"@"+ip+"'")
    child.sendline("")
    def exp():
        child.expect(node+'@'+ip)
    exp()
    child.sendline("erlang:set_cookie(node(),'RPJVCXYDYULBNZFEFPHJ').")
    exp()
    child.interact()
    #return child

def stop():
    child  = pexpect.spawn('lasp_peer_service:stop().')
    c_prompt = 'root@'
    child.expect (c_prompt)
    child.sendline('export PEER_SERVICE=partisan_hyparview_peer_service_manager')
    child.expect (c_prompt)
    child.sendline("exit")
    child.close()

start(ND.getIp(nodeId), ND.getName(nodeId), ND.getRate(nodeId))
#start(ip_dict[nodeId]["ip"], ip_dict[nodeId]["node"], ip_dict[nodeId]["rate"])
