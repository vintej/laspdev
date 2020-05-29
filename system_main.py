from threading import Thread
import multiprocessing
import os
import time
import sys
import utility.system_start_stop as systemFun
import utility.node_directory as ND
import datetime

#print(ND.getIp('d1'))
#print(ND.getName('d1'))
#print(ND.getRate('d1'))

#start_node("d4")
#stop_node("d4")
#exec_com("lasp_peer_service:stop().", "d4")
d1_ready = False
ready_to_join = False

def start_system(nodeName):
    systemFun.exec_com("script /home/ubuntu/laspdev/utility/log/"+nodeName+"_log", nodeName)
    global d1_ready, ready_to_join
    systemFun.start_node(nodeName)
    if nodeName != 'd1' and nodeName != 'd5':
        #For every other node
        while ready_to_join == False:
            print('Waiting ready_to_join from:'+nodeName)
            time.sleep(2)
        join_system_internal(nodeName)
    else:
        if nodeName=='d1':
            #systemFun.start_node('d1') #Can change argument to nodeName
            d1_ready = True
        else:
            #For node d5
            while d1_ready==False:
                print('Waiting for d1 from:'+nodeName)
                time.sleep(2)
            #systemFun.start_node('d5') #Can change argument to nodeName
            join_system_overlay('d1', 'd5')
            #os.system('python utility/test.py')
            ready_to_join = True

def join_system_overlay(ToNode, FromNode):
    time.sleep(5)
    systemFun.exec_com("lasp_peer_service:join('"+ND.getName(ToNode)+"@"+ND.getIp(ToNode)+"').", FromNode)

def join_system_internal(nodeName):
    time.sleep(5)
    systemFun.exec_com("lasp_peer_service:join('"+ND.getName(systemFun.find_key(nodeName))+"@"+ND.getIp(systemFun.find_key(nodeName))+"').", nodeName)

def stop_system(nodeName):
    systemFun.stop_node(nodeName)
    time.sleep(2)
    systemFun.exec_com("", nodeName)
    time.sleep(1)
    systemFun.exec_com("", nodeName)
    systemFun.exec_com("exit", nodeName)
    print('Stopped Node:'+nodeName)


#Start main here
if __name__ == "__main__":
        operation = sys.argv[1]
        allNodes = ['d1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8' ]
        #allNodes = ['d1', 'd3', 'd5', 'd7']
        threads = []
        for node in allNodes:
            print node
            if operation == "start":
                threads.append(Thread(target=start_system, args=(node,)))
            elif operation == "stop":
                threads.append(Thread(target=stop_system, args=(node,)))
            threads[-1].start()
        if operation == "stop":
            folder = str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
            os.system("mkdir /home/ubuntu/laspdev/utility/results/"+folder)
            os.system("mv /home/ubuntu/laspdev/utility/log/* /home/ubuntu/laspdev/utility/results/"+folder)

        #tA = Thread(target=laspA_s, args=('Node A',))
        #tB = Thread(target=laspB_s, args=('Node B',))
        #tA.start()
        #tB.start()
        #pBW = multiprocessing.Process(target=bw_log, args=('bw',))
        #pBW.start()
        #while tA.isAlive() or tB.isAlive():
        #    pass
        #pBW.terminate()
        #os.system("mkdir results/"+run_name)
        #os.system("mv logs/* results/"+run_name)
        #os.system("docker cp laspvinA:/tmp/bwLogs results/"+run_name)
        #print("Execution Ended")
