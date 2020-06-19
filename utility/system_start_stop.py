#!/usr/bin/python

import os
import sys
import pexpect
import time
import NDutility as ND

def start_node(node):
    os.system('screen -S '+ND.get_cluster(node)+' -p '+node+' -X stuff "python /home/ubuntu/laspdev/utility/setup_lasp.py '+node+'^M"')
    #print("Started on session:"+ND.get_cluster(node)+" Terminal:"+node)

def stop_node(node):
    e = ND.get_cluster(node)
    i = node
    #print("Stopping node:"+i+" in session:"+e)
    os.system('screen -S '+e+' -p '+i+' -X stuff "^M"')
    os.system('screen -S '+e+' -p '+i+' -X stuff "^M"')
    time.sleep(2)
    os.system('screen -S '+e+' -p '+i+' -X stuff "lasp_peer_service:stop().^M"')
    time.sleep(4)
    #os.system('screen -S '+e+' -p '+i+' -X stuff "exit^M"')


#def find_key(node):
#    for e in nodeterms:
#        for i in nodeterms[e]:
#            if i == node:
#                return e

#def test(node):
#    print("Session:"+find_key(node)+" Terminal:"+node)

def exec_com(command, node):
    os.system('screen -S '+ND.get_cluster(node)+' -p '+node+' -X stuff "'+command+'^M"')

def exec_spec_com(command, node):
    os.system('screen -S '+ND.get_cluster(node)+' -p '+node+' -X stuff \''+command+'^M\'')
