#!/usr/bin/python

import pexpect
import os
import sys
import time

def update_container():
    c_prompt = 'root@'
    child = pexpect.spawn ('docker exec -it mn.d3 /bin/bash')
    child.logfile = sys.stdout
    child.expect (c_prompt)
    child.sendline('cd /opt/lasp')
    child.expect(c_prompt)
    child.sendline('pkill -f rebar3')
    child.expect(c_prompt)
    child.sendline('ps -aef | grep rebar3')
    child.expect(c_prompt)
    child.sendline('git pull')
    child.expect(c_prompt)
    child.sendline('make')
    child.expect(c_prompt)
    child.sendline('rm log/*')
    child.expect(c_prompt)
    child.sendline('echo "" > log/error.log')
    child.expect(c_prompt)
    child.sendline('echo "" > log/console.log')
    child.expect(c_prompt)
    child.sendline('echo "" > log/crash.log')
    child.expect(c_prompt)
    child.sendline('rm /var/lib/vnstat/d3-eth0')
    child.expect(c_prompt)
    child.sendline('rm /var/lib/vnstat/.d3-eth0')
    child.expect(c_prompt)
    child.sendline("exit")
    time.sleep(2)
    child.close()

update_container()
with open('/home/ubuntu/laspdev/containernet_log') as f:
        tempIm = f.read()
        if 'vinayaktj/lasp:dev' in tempIm:
            image = 'devsquashed'
        elif 'vinayaktj/lasp:base' in tempIm:
            image = 'base'
print (image)
os.system('docker commit mn.d3 vinayaktj/lasp:'+image)
os.system('docker push vinayaktj/lasp:'+image)
