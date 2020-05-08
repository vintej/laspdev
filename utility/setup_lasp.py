#!/usr/bin/python

import pexpect
import subprocess
import sys

print(sys.argv[1])
ip_dict = {"d1":{ "ip":"10.0.0.250", "node":"a"}, "d2": {"ip":"10.0.0.251", "node":"b"}, "d3":{"ip":"10.0.0.252", "node":"c"}, "d4":{"ip":"10.0.0.253", "node":"d"}}
print("ip:"+ip_dict[sys.argv[1]]["ip"])
print("node:"+ip_dict[sys.argv[1]]["node"])
cont = "mn."+sys.argv[1]
childcont = pexpect.spawn('docker exec -it '+cont+' /bin/bash')
#start(childcont, ip_dict[sys.argv[1]]["ip"],ip_dict[sys.argv[1]]["node"])
#childcont.interact()

def start(child, ip, node):
    c_prompt = 'root@'
    #child = pexpect.spawn ('docker exec -it '+cont+' /bin/bash')
    #child.logfile = sys.stdout
    child.expect (c_prompt)
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
    #return child

start(childcont, ip_dict[sys.argv[1]]["ip"],ip_dict[sys.argv[1]]["node"])
childcont.interact()
