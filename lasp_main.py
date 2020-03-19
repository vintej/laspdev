import pexpect
import subprocess
import sys
from setup_lasp import start

def exec_cmd(child, cmd, pmt, node):
    child.sendline(cmd)
    child.expect("("+node+"@"+pmt+")")

#Start laspA node
def laspA_s():
    laspA = pexpect.spawn ('docker exec -it laspvinA /bin/bash')
    laspA.logfile = sys.stdout
    ipA = '172.17.0.2'
    start(laspA, ipA, 'a')
    exec_cmd(laspA, "lasp_peer_service:stop().", ipA, 'a')
    laspA.sendline("exit")

#Start laspB node
def laspB_s():
    laspB = pexpect.spawn ('docker exec -it laspvinB /bin/bash')
    laspB.logfile = sys.stdout
    ipB = '172.17.0.3'
    start(laspB, ipB, 'b')
    exec_cmd(laspB, "lasp_peer_service:stop().", ipB, 'b')
    laspB.sendline("exit")

#Start main here
laspA_s()
