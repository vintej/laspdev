#!/usr/bin/python

import pexpect
import subprocess
import time
import sys
import logging
from threading import Thread
from setup_lasp import start
#from nodeA import setup_table
#from nodeB import check_update
from propagation import *

A_ready_to_join = False
B_ready_to_join = False
membership = False
ipA = '172.17.0.2'
ipB = '172.17.0.3'


def exec_cmd(child, cmd, pmt, node):
    child.sendline(cmd)
    child.expect("("+node+"@"+pmt+")")

def setup_logger(logger_name, log_file, level=logging.INFO):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s '+logger_name+' %(message)s')
    fileHandler = logging.FileHandler("logs/"+log_file, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    l.setLevel(level)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler)

#Start laspA node
def laspA_s(node):
    global B_ready_to_join
    global A_ready_to_join
    global membership, update
    #import logging
    #logA = open("logs/ThreadA", 'w')
    #logging.basicConfig(filename="logs/ThreadA",filemode='w',format='%(asctime)s %(message)s',datefmt='%H:%M:%S',level=logging.DEBUG)
    setup_logger('ThreadA', "ThreadA.log")
    logger_1 = logging.getLogger('ThreadA')
    logger_1.info("++LOGS FOR NODE "+node+" ++")
    laspA = pexpect.spawn ('docker exec -it laspvinA /bin/bash')
    lfileA = open("logs/NodeA", 'w')
    laspA.logfile = lfileA
    #laspA.logfile.formatter('%(asctime)s %(message)s')
    #lfileA.write("++LOGS FOR NODE A++ \n \n")
    start(laspA, ipA, 'a')
    A_ready_to_join = True
    while(True):
        if B_ready_to_join == True:
            exec_cmd(laspA, "lasp_peer_service:join('b@"+ipB+"').", ipA, 'a')
            membership = True
            logger_1.info("Membership done")
            break
        else:
            logger_1.info("waiting for B ready")
            time.sleep(5)
    time.sleep(5)
    #print("Membership done")
    #start(laspA, ipA, 'a')
    def exec_cmd_a(cmda):
        exec_cmd(laspA, cmda, ipA, 'a')
    exec_cmd_a("lasp_config:set(mode, delta_based).")
    logger_1.info("Delta mode set")
    time.sleep(5)
    setup_table(laspA, ipA, update, logger_1)
    time.sleep(5)
    exec_cmd(laspA, "lasp_peer_service:stop().", ipA, 'a')
    logger_1.info("Execution ended for node "+node)
    laspA.sendline("exit")
    #logger_1.handlers.clear()
    #logger_1.shutdown()    
    laspA.logfile.close()
    lfileA.close()
    
#Start laspB node
def laspB_s(node):
    global B_ready_to_join
    global A_ready_to_join, update
    #import logging
    #logB = open("logs/ThreadB", 'w')
    #logging.basicConfig(filename="logs/ThreadB",filemode='w', format='%(asctime)s %(message)s',datefmt='%H:%M:%S',level=logging.DEBUG)
    setup_logger('ThreadB', "ThreadB.log")
    logger_2 = logging.getLogger('ThreadB')
    logger_2.info("++LOGS FOR NODE "+node+" ++")
    laspB = pexpect.spawn ('docker exec -it laspvinB /bin/bash')
    lfileB = open("logs/NodeB", 'w')
    laspB.logfile = lfileB
    #laspB.logfile.formatter('%(asctime)s %(message)s')
    #lfileB.write("++LOGS FOR NODE B++ \n \n")
    start(laspB, ipB, 'b')
    B_ready_to_join = True
    logger_2.info("B_set_to_true")
    while(membership==False):
        logger_2.info("Waiting for membership")
        time.sleep(5)
    exec_cmd(laspB, "lasp_peer_service:members().", ipB, 'b')
    lfileB.write("Membership established")
    def exec_cmd_b(cmdb):
                exec_cmd(laspB, cmdb, ipB, 'b')
    exec_cmd_b("lasp_config:set(mode, delta_based).")
    time.sleep(5)
    logger_2.info("Delta mode set")
    time.sleep(30)
    check_update(laspB, ipB, update,logger_2)
    exec_cmd(laspB, "lasp_peer_service:stop().", ipB, 'b')
    laspB.sendline("exit")
    logger_2.info("Execition ended for "+node)
    #logger_2.handlers.clear()
    #logger_2.shutdown()    
    laspB.logfile.close()
    lfileB.close()
    
#Start main here
if __name__ == "__main__":
    tA = Thread(target=laspA_s, args=('Node A',))
    tB = Thread(target=laspB_s, args=('Node B',))
    tA.start()
    tB.start()
