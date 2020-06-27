#!/usr/bin/python

import pexpect
import subprocess
import sys
import time
import NDutility as ND

print(sys.argv[1])
nodeId = sys.argv[1]
print("ip:"+ND.get_ip(nodeId))
print("node:"+ND.get_id(nodeId))
cont = "mn."+nodeId

def start(ip, node, rate):
    global nodeId
    child  = pexpect.spawn('docker exec -it '+cont+' /bin/bash')
    child.logfile_read = sys.stdout
    c_prompt = 'root@'
    child.expect (c_prompt)
    child.sendline('service vnstat start')
    child.expect(c_prompt)
    time.sleep(1)
    child.sendline('vnstat -u -i '+nodeId+'-eth0')
    child.expect(c_prompt)
    child.sendline('vnstat -u')
    child.expect(c_prompt)
    child.sendline('vnstat')
    child.expect(c_prompt)
    child.sendline('export PEER_SERVICE=partisan_hyparview_peer_service_manager')
    child.expect(c_prompt)
    child.sendline('export RATE_CLASS='+rate)
    child.expect(c_prompt)
    child.sendline('export RATE_C1=13000')
    child.expect(c_prompt)
    child.sendline('export RATE_C2=40000')
    child.expect(c_prompt)
    child.sendline('export RATE_C3=70000')
    child.expect(c_prompt)
    child.sendline('export PROPAGATE_ON_UPDATE=false')
    child.expect(c_prompt)
    child.sendline('export MAX_ACTIVE_SIZE=50')
    child.expect(c_prompt)
    child.sendline('cd /opt/lasp')
    child.expect(c_prompt)
    child.sendline('epmd -daemon')
    child.expect(c_prompt)
    time.sleep(5)
    child.sendline('rebar3 shell --name '+node+'@'+ip)
    child.expect("Application lasp started on node '"+node+"@"+ip+"'", timeout=300)
    child.sendline("")
    def exp():
        child.expect(node+'@'+ip, timeout=120)
    exp()
    #child.sendline("partisan_config:set(max_active_size, 50).")
    #exp()
    #child.sendline("partisan_config:set(max_passive_size, 80).")
    #exp()
    #child.sendline("partisan_config:set(min_active_size, 9).")
    #exp()
    child.sendline("erlang:set_cookie(node(),'RPJVCXYDYULBNZFEFPHJ').")
    exp()
    #child.sendline("lager:set_loglevel(lager_console_backend, '=debug').")
    #exp()
    child.sendline("application:get_env(partisan, max_active_size).")
    exp()
    child.sendline("application:get_env(partisan, max_passive_size).")
    exp()
    child.sendline("application:get_env(partisan, min_active_size).")
    exp()
    #child.sendline("partisan_config:set(max_active_size, 50).")
    #exp()
    #child.sendline("application:get_env(partisan, max_active_size).")
    #exp()
    child.logfile_read = None
    child.interact()
    #child.logfile_read = None
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
