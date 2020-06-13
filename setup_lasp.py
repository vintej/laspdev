#!/usr/bin/python

import pexpect
import os

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
    child.sendline('rm log/*')
    child.expect(c_prompt)
    child.sendline('echo "" > log/error.log')
    child.expect(c_prompt)
    child.sendline('echo "" > log/console.log')
    child.expect(c_prompt)
    child.sendline('echo "" > log/crash.log')
    child.expect(c_prompt)
    child.sendline("exit")
    child.expect('root@csst-06:')
    child.close()

update_container()
os.system('docker commit mn.d3 vinayaktj/lasp:dev')
os.system('docker push vinayaktj/lasp:dev')
