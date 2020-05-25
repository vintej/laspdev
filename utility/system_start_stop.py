import os
import sys
import pexpect
import time

#operation = sys.argv[1]
#node = sys.argv[2]
#list1 = {""}
nodeterms = {"d1":["d1", "d2", "d3", "d4"], "d5":["d5", "d6", "d7", "d8"]}

#for e in nodeterms:
#    tempList = nodeterms[e]
#    tempSess = e
#    for i in tempList:
#        if i == node:
#            print ("Session: "+e+" terminal:"+i)
#            if operation == "start":
#                os.system('screen -S '+e+' -p '+i+' -X stuff "python /home/ubuntu/laspdev/utility/setup_lasp.py '+i+'^M"')
#            elif operation == "stop":
#                os.system('screen -S '+e+' -p '+i+' -X stuff "lasp_peer_service:stop().^M"')
#                time.sleep(2)
#                os.system('screen -S '+e+' -p '+i+' -X stuff "^M"')
#                os.system('screen -S '+e+' -p '+i+' -X stuff "^M"')
#                os.system('screen -S '+e+' -p '+i+' -X stuff "exit^M"')

def start_node(node):
    os.system('screen -S '+find_key(node)+' -p '+node+' -X stuff "python /home/ubuntu/laspdev/utility/setup_lasp.py '+node+'^M"')
    print("Started on session:"+find_key(node)+" Terminal:"+node)

def stop_node(node):
    e = find_key(node)
    i = node
    os.system('screen -S '+e+' -p '+i+' -X stuff "lasp_peer_service:stop().^M"')
    time.sleep(2)
    os.system('screen -S '+e+' -p '+i+' -X stuff "^M"')
    os.system('screen -S '+e+' -p '+i+' -X stuff "^M"')
    os.system('screen -S '+e+' -p '+i+' -X stuff "exit^M"')


def find_key(node):
    for e in nodeterms:
        for i in nodeterms[e]:
            if i == node:
                return e

def test(node):
    print("Session:"+find_key(node)+" Terminal:"+node)

def exec_com(command, node):
    os.system('screen -S '+find_key(node)+' -p '+node+' -X stuff "'+command+'^M"')
