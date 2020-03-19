#!/usr/bin/python

import pexpect
import subprocess
import time
from threading import Thread
from setup_lasp import start

A_ready_to_join = False
B_ready_to_join = False
membership = False
ipA = '172.17.0.2'
ipB = '172.17.0.3'

def exec_cmd(child, cmd, pmt, node):
    child.sendline(cmd)
    child.expect("("+node+"@"+pmt+")")

#Start laspA node
def laspA_s(node):
    global B_ready_to_join
    global A_ready_to_join
    global membership
    print("Starting execution for "+node)
    laspA = pexpect.spawn ('docker exec -it laspvinA /bin/bash')
    lfileA = open("logs/NodeA", 'w')
    laspA.logfile = lfileA
    lfileA.write("++LOGS FOR NODE A++ \n \n")
    start(laspA, ipA, 'a')
    A_ready_to_join = True
    while(True):
        if B_ready_to_join == True:
            exec_cmd(laspA, "lasp_peer_service:join('b@"+ipB+"').", ipA, 'a')
            membership = True
            print("Membership done")
            break
        else:
            print("waiting for B ready")
            time.sleep(5)
    time.sleep(5)
    #print("Membership done")
    #start(laspA, ipA, 'a')    
    exec_cmd(laspA, "lasp_peer_service:stop().", ipA, 'a')
    laspA.sendline("exit")
    laspA.logfile.close()
    lfileA.close()
    print("Execition ended for "+node)

#Start laspB node
def laspB_s(node):
    global B_ready_to_join
    global A_ready_to_join
    print("Starting execution for "+node)
    laspB = pexpect.spawn ('docker exec -it laspvinB /bin/bash')
    lfileB = open("logs/NodeB", 'w')
    laspB.logfile = lfileB
    lfileB.write("++LOGS FOR NODE B++ \n \n")
    start(laspB, ipB, 'b')
    B_ready_to_join = True
    print("B_set_to_true")
    while(membership==False):
        print("Waiting for membership")
        time.sleep(5)
    exec_cmd(laspB, "lasp_peer_service:members().", ipB, 'b')
    lfileB.write("Membership established")
    time.sleep(3)
    exec_cmd(laspB, "lasp_peer_service:stop().", ipB, 'b')
    laspB.sendline("exit")
    laspB.logfile.close()
    lfileB.close()
    print("Execition ended for "+node)

#Start main here
if __name__ == "__main__":
    tA = Thread(target=laspA_s, args=('Node A',))
    tB = Thread(target=laspB_s, args=('Node B',))
    tA.start()
    tB.start()
