#!/usr/bin/python

import pexpect
import subprocess
import sys

def start(child, ip, node):
    c_prompt = 'root@'
    #child = pexpect.spawn ('docker exec -it '+cont+' /bin/bash')
    #child.logfile = sys.stdout
    child.expect (c_prompt)
    child.sendline('cd /opt/lasp')
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
