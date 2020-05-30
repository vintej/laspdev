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
allNodes = ['d1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8' ]
#allNodes = ['d1', 'd3', 'd5', 'd7']
d1_ready = False
ready_to_join = False
node_status = []

def start_system(nodeName):
    systemFun.exec_com("script /home/ubuntu/laspdev/utility/log/"+nodeName+"_log", nodeName)
    global d1_ready, ready_to_join
    time.sleep(2)
    systemFun.start_node(nodeName)
    time.sleep(2)
    if nodeName != 'd1' and nodeName != 'd5':
        #For every other node
        while ready_to_join == False:
            print('Waiting ready_to_join from:'+nodeName)
            time.sleep(2)
        print("Joining internal network in 5 sec from:"+nodeName)
        time.sleep(5)
        join_system_internal(nodeName)
        node_status.append("Ready")
    else:
        if nodeName=='d1':
            #systemFun.start_node('d1') #Can change argument to nodeName
            d1_ready = True
            node_status.append("Ready")
        else:
            #For node d5
            while d1_ready==False:
                print('Waiting for d1 from:'+nodeName)
                time.sleep(2)
            #systemFun.start_node('d5') #Can change argument to nodeName
            join_system_overlay('d1', 'd5')
            #os.system('python utility/test.py')
            ready_to_join = True
            node_status.append("Ready")
    print("Node Status count: "+str(node_status.count("Ready")))
    #Doing operations on node d3
    if nodeName == 'd3':
        time.sleep(5)
        print("Executing operation")
        exec_operation('d3')

def exec_operation(nodeName):
    while node_status.count("Ready") != len(allNodes):
        print("Waiting for nodes to be ready")
        time.sleep(2)
    print("Executing operations after 5 secs")
    time.sleep(5)
    systemFun.exec_spec_com( 'lasp_delta_based_synchronization_backend:time_stamp().', nodeName)
    systemFun.exec_spec_com( 'f().', nodeName)
    time.sleep(2)
    systemFun.exec_spec_com( 'Key1 = <<"key1">>.', nodeName)
    time.sleep(2)
    systemFun.exec_spec_com( 'Key2 = <<"key2">>.', nodeName)
    time.sleep(2)
    systemFun.exec_spec_com( 'Timestamp = fun () -> erlang:unique_integer([monotonic, positive]) end.', nodeName)
    time.sleep(2)
    systemFun.exec_spec_com( 'AwMapType = {state_awmap, [state_mvregister]}.', nodeName)
    time.sleep(2)
    systemFun.exec_spec_com( 'AwMapVarName = <<"awmap">>.', nodeName)
    time.sleep(2)
    systemFun.exec_spec_com( 'AwMapVal = #{what => i_am_vin_tej1}.', nodeName)
    time.sleep(2)
    systemFun.exec_spec_com( 'AwMapVal2 = #{what => i_am_vin_tej2}.', nodeName)
    time.sleep(2)
    systemFun.exec_spec_com( '{ok, {AwMap, _, _, _}} = lasp:declare({AwMapVarName, AwMapType}, AwMapType).', nodeName)
    time.sleep(2)
    systemFun.exec_spec_com( '{ok, {AwMap1, _, _, _}} = lasp:update(AwMap, {apply, Key1, {set, Timestamp(), AwMapVal}}, self()).', nodeName)
    systemFun.exec_spec_com( 'lasp_delta_based_synchronization_backend:time_stamp().', nodeName)
    time.sleep(2)
    print("Operation completed")


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
    time.sleep(1)
    systemFun.exec_com("exit", nodeName)
    print('Stopped Node:'+nodeName)


#Start main here
if __name__ == "__main__":
        operation = sys.argv[1]
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
