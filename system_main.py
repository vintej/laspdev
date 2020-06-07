from threading import Thread
import multiprocessing
import os
import time
import sys
import utility.system_start_stop as systemFun
import utility.NDutility as ND
import datetime
import fnmatch
from random import randint

allNodes = ND.get_allNodes()
#allNodes = ['d1', 'd3', 'd5', 'd7']
d1_ready = False
ready_to_join = False
node_status = []
bw_threads = []
deltaRcvSys = []
ready_to_join = []

def start_system(nodeName):
    logFile = ''
    deltaRecv = False
    time.sleep(randint(1,12))
    files = os.listdir('/home/ubuntu/laspdev/utility/log/')
    for name in files:
            if fnmatch.fnmatch(name, nodeName+"_log*"):
                print("Found match")
                logFile = name
    print("Logfile: "+logFile)
    os.system('echo "" > /home/ubuntu/laspdev/utility/log/'+logFile)
    time.sleep(4)
    systemFun.exec_com("", nodeName)
    systemFun.exec_com("", nodeName)
    global d1_ready, ready_to_join
    time.sleep(2)
    systemFun.start_node(nodeName)
    time.sleep(2)
    if ND.get_id(nodeName) != 'a':
        #For every other node
        while (ready_to_join.count("Ready")) != len(ND.get_allEdges()):
            print('Waiting ready_to_join from:'+nodeName+" EdgesReady:"+str(ready_to_join))
            time.sleep(20)
        print("Joining internal network in 10 sec from:"+nodeName)
        time.sleep(10)
        join_system_internal(nodeName, logFile)
        node_status.append("Ready")
    else:
        ready_to_join.append(nodeName)
        if nodeName=='d1':
            d1_ready = True
            node_status.append("Ready")
            ready_to_join.append("Ready")
        else:
            #For nodes other edges than d1 and node_id= 'a'
            while d1_ready==False:
                print('Waiting for d1 from:'+nodeName)
                time.sleep(10)
            #systemFun.exec_com("ping -c 2 "+ND.get_ip('d1'), nodeName)
            join_system_overlay('d1', nodeName, logFile)
            ready_to_join.append("Ready")
            node_status.append("Ready")
    print("Node Status Ready count: "+str(node_status.count("Ready")))
    #Doing operations on node d3
    if nodeName == 'd3':
        while (node_status.count("Ready")) != len(allNodes):
            print("Waiting for nodes to be ready for Executing operation")
            time.sleep(60)
        print("Executing operation")
        exec_operation('d3')
    while deltaRecv == False:
        with open('/home/ubuntu/laspdev/utility/log/'+logFile) as f:
            if 'Received delta' in f.read():
                print("Delta Received at Node "+nodeName)
                deltaRcvSys.append("True")
                deltaRecv = True
                break
        time.sleep(30)
    print("***********Test Completed at "+nodeName+"*********")

def exec_operation(nodeName):
    while node_status.count("Ready") != len(allNodes):
        print("***********Waiting 10 secs for nodes to be ready*******")
        time.sleep(10)
    print("Executing operations after 20 secs")
    time.sleep(20)
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


def join_system_overlay(ToNode, FromNode, logFile):
    time.sleep(5)
    execCom = False
    systemFun.exec_com("lasp_peer_service:join('"+ND.get_id(ToNode)+"@"+ND.get_ip(ToNode)+"').", FromNode)
    time.sleep(20)
    systemFun.exec_com("lasp_peer_service:members().", FromNode)
    time.sleep(20)
    with open('/home/ubuntu/laspdev/utility/log/'+logFile) as f:
                lines = f.readlines()
    while execCom == False:
        with open('/home/ubuntu/laspdev/utility/log/'+logFile) as f:
            temp = f.read()
            if 'lasp_peer_service:join(' in temp and 'CRASH REPORT' not in temp:
                #if "{ok,['d@14.0.0.14','c@14.0.0.13','b@14.0.0.12','a@14.0.0.11']}"
                if (",'"+ND.get_id(ToNode)+"@"+ND.get_ip(ToNode)) in temp or ("'"+ND.get_id(ToNode)+"@"+ND.get_ip(ToNode)+"',") in temp or ("'"+ND.get_id(ToNode)+"@"+ND.get_ip(ToNode)+"']}") in temp:
                    print(FromNode+" Joined System Overlay")
                    execCom = True
                    break
                else:
                    print(FromNode+" Not found Peer:"+ToNode)
                    systemFun.exec_com("lasp_peer_service:join('"+ND.get_id(ToNode)+"@"+ND.get_ip(ToNode)+"').", FromNode)
                    time.sleep(20)
                    systemFun.exec_com("lasp_peer_service:members().", FromNode)
                    time.sleep(20)
            else:
                systemFun.exec_com("lasp_peer_service:join('"+ND.get_id(ToNode)+"@"+ND.get_ip(ToNode)+"').", FromNode)
                time.sleep(20)
                systemFun.exec_com("lasp_peer_service:members().", FromNode)
                time.sleep(20)
                for line in lines:
                    if line.strip("\n") != "CRASH REPORT":
                        f.write(line)
        time.sleep(30)

def join_system_internal(nodeName, logFile):
    time.sleep(5)
    execCom = False
    systemFun.exec_com("lasp_peer_service:join('"+ND.get_id(ND.get_edge(ND.get_cluster(nodeName)))+"@"+ND.get_ip(ND.get_edge(ND.get_cluster(nodeName)))+"').", nodeName)
    time.sleep(20)
    systemFun.exec_com("lasp_peer_service:members().", nodeName)
    time.sleep(20)
    while execCom == False:
        print ("Checking from "+nodeName)
        with open('/home/ubuntu/laspdev/utility/log/'+logFile) as f:
            temp = f.read()
            lines = f.readlines()
            if 'lasp_peer_service:join(' in temp and 'CRASH REPORT' not in temp:
                if (",'"+ND.get_id(ND.get_edge(ND.get_cluster(nodeName)))+"@"+ND.get_ip(ND.get_edge(ND.get_cluster(nodeName)))) in temp or ("'"+ND.get_id(ND.get_edge(ND.get_cluster(nodeName)))+"@"+ND.get_ip(ND.get_edge(ND.get_cluster(nodeName)))+"',") in temp or ("'"+ND.get_id(ND.get_edge(ND.get_cluster(nodeName)))+"@"+ND.get_ip(ND.get_edge(ND.get_cluster(nodeName)))+"']}") in temp:
                    print(nodeName+" Joined internal system ")
                    execCom = True
                    break
                else:
                    print(nodeName+"Not found edge Peer in "+ND.get_id(ND.get_edge(ND.get_cluster(nodeName)))+"@"+ND.get_ip(ND.get_edge(ND.get_cluster(nodeName))))
                    systemFun.exec_com("lasp_peer_service:join('"+ND.get_id(ND.get_edge(ND.get_cluster(nodeName)))+"@"+ND.get_ip(ND.get_edge(ND.get_cluster(nodeName)))+"').", nodeName)
                    time.sleep(20)
                    systemFun.exec_com("lasp_peer_service:members().", nodeName)
                    time.sleep(20)
            else:
                systemFun.exec_com("lasp_peer_service:join('"+ND.get_id(ND.get_edge(ND.get_cluster(nodeName)))+"@"+ND.get_ip(ND.get_edge(ND.get_cluster(nodeName)))+"').", nodeName)
                time.sleep(20)
                systemFun.exec_com("lasp_peer_service:members().", nodeName)
                print(nodeName+" Crashed... Retrying ")
                for line in lines:
                    if line.strip("\n") != "CRASH REPORT":
                        f.write(line)
        time.sleep(30)

def stop_system(nodeName):
    systemFun.stop_node(nodeName)
    print("Executed stop_node() sleep 4")
    time.sleep(4)
    systemFun.exec_com("", nodeName)
    systemFun.exec_com("", nodeName)
    print("2 enters sleep 4")
    time.sleep(4)
    systemFun.exec_com("", nodeName)
    systemFun.exec_com("", nodeName)
    systemFun.exec_com("exit", nodeName)
    print("exit sleep 4")
    time.sleep(4)
    systemFun.exec_com("", nodeName)
    print('Stopped Node:'+nodeName)

def bw_log(nodeName):
        os.system('docker exec mn.'+nodeName+' bash -c "date > /opt/'+nodeName+'_bwLogs"')
        os.system('docker exec mn.'+nodeName+' bash -c "iftop -i '+nodeName+'-eth0 -t >> /opt/'+nodeName+'_bwLogs"')

def bw_threads_stop():
    while deltaRcvSys.count("True") != len(allNodes):
            print("Waiting for Delta To be received by all")
            time.sleep(60)
    time.sleep(10)
    for thread in bw_threads:
        thread.terminate()
    print("BW threads stopped")

def start_testing():
    threads_main = []
    for node in allNodes:
            print node
            threads_main.append(Thread(target=start_system, args=(node,)))
            #bw_threads.append(multiprocessing.Process(target=bw_log, args=(node,)))
            #bw_threads[-1].start()
            threads_main[-1].start()
    bw_threads_stop()

def stop_testing():
    threads_main=[]
    for node in allNodes:
            print node
            threads_main.append(Thread(target=stop_system, args=(node,)))
            threads_main[-1].start()
    print("Stopped")
    folder = str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    os.system("mkdir /home/ubuntu/laspdev/results/"+folder)
    os.system("cp /home/ubuntu/laspdev/utility/log/* /home/ubuntu/laspdev/results/"+folder)
    for node in allNodes:
                os.system("docker cp mn."+node+":/opt/"+node+"_bwLogs /home/ubuntu/laspdev/results/"+folder)

#Start main here
if __name__ == "__main__":
        start_testing()
        stop_testing()
        '''
        operation = sys.argv[1]
        threads_main = []
        for node in allNodes:
            print node
            if operation == "start":
                threads_main.append(Thread(target=start_system, args=(node,)))
                bw_threads.append(multiprocessing.Process(target=bw_log, args=(node,)))
                bw_threads[-1].start()
            elif operation == "stop":
                threads_main.append(Thread(target=stop_system, args=(node,)))
            threads_main[-1].start()
        if operation=="start":
            bw_threads_stop()
        if operation == "stop":
            print("Stopped")
            folder = str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
            os.system("mkdir /home/ubuntu/laspdev/results/"+folder)
            os.system("cp /home/ubuntu/laspdev/utility/log/* /home/ubuntu/laspdev/results/"+folder)
            for node in allNodes:
                os.system("docker cp mn."+node+":/opt/"+node+"_bwLogs /home/ubuntu/laspdev/results/"+folder)
        '''
