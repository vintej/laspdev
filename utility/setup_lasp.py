#!/usr/bin/python

import pexpect
import subprocess
import sys
import NDutility as ND

print(sys.argv[1])
nodeId = sys.argv[1]
print("ip:"+ND.get_ip(nodeId))
print("node:"+ND.get_id(nodeId))
cont = "mn."+nodeId

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

start(ND.get_ip(nodeId), ND.get_id(nodeId), ND.get_rate(nodeId))
