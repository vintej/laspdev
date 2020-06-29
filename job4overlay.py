from threading import Thread
import multiprocessing
import os
import time
import string
import random
import sys
import utility.system_start_stop as systemFun
import utility.NDutility as ND
from datetime import datetime
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
edges_ready = []
sub_fail = []
delta_fail = []
testFor = ''
delta_waiting = []
stopped_node = []
test_completed = []
bw_collected = []
delta_val = ['TMP']
delta_changed = False
jobId = ''
start_time = ''
with open('/home/ubuntu/Vin/laspdev/containernet_log') as f:
    tempIm = f.read()
    if 'vinayaktj/lasp:dev' in tempIm:
        testFor = 'dev'
    elif 'vinayaktj/lasp:base' in tempIm:
        testFor = 'base'

OpsDone = []
d1_overlay = ['d11','d71','d61']
d11_overlay = ['d81', 'd91', 'd1']
d21_overlay = ['d51','d31', 'd81'] #d21 doesnot connect to d81
d31_overlay = ['d41', 'd91', 'd21'] #cluster 4
d41_overlay = ['d31', 'd91', 'd51']
d51_overlay = ['d41', 'd21', 'd71', 'd61']
d61_overlay = ['d51', 'd81', 'd1']
d71_overlay = ['d1', 'd81', 'd51']
d81_overlay = ['d11', 'd71', 'd61', 'd21']
d91_overlay = ['d11', 'd31', 'd41']
overlay_dict = {'d1':d1_overlay, 'd11':d11_overlay, 'd21':d21_overlay,'d31':d31_overlay,'d41':d41_overlay,'d51':d51_overlay, 'd61':d61_overlay,'d71':d71_overlay,'d81':d81_overlay,'d91':d91_overlay}

def start_system(nodeName):
    global testFor, delta_changed
    logFile = ''
    deltaRecv = False
    time.sleep(randint(1,12))
    files = os.listdir('/home/ubuntu/Vin/laspdev/utility/log/')
    for name in files:
            if fnmatch.fnmatch(name, nodeName+"_log*"):
                #print("Found match")
                logFile = name
    print("Logfile: "+logFile)
    os.system('echo "" > /home/ubuntu/Vin/laspdev/utility/log/'+logFile)
    time.sleep(4)
    systemFun.exec_com("", nodeName)
    systemFun.exec_com("", nodeName)
    global d1_ready, ready_to_join, jobId
    time.sleep(2)
    systemFun.start_node(nodeName)
    time.sleep(2)
    if ND.get_id(nodeName) != 'a':
        #For every other node
        while (ready_to_join.count("Ready")) != len(ND.get_allEdges()):
            #print('Waiting ready_to_join from:'+nodeName+" EdgesReady:"+str(ready_to_join))
            time.sleep(30)
        print("Joining internal network in 20 sec from:"+nodeName)
        time.sleep(20)
        join_system_internal(nodeName, logFile)
        #node_status.append("Ready")
    else:
        ready_to_join.append(nodeName)
        if nodeName=='d1':
            time.sleep(5)
            d1_ready = True
            #node_status.append("Ready")
            #ready_to_join.append("Ready")
            time.sleep(60)
            edges_ready.append(nodeName)
            #edgeToJoin = (overlay_dict[nodeName])[1]
            JoinedOverlay = False
            while JoinedOverlay == False:
                joiningStatus = []
                for edgeToJoin in overlay_dict[nodeName]:
                    while edgeToJoin not in edges_ready:
                        time.sleep(5)
                    print (nodeName+" Joining to edge in 10 sec "+edgeToJoin)
                    time.sleep(10)
                    joiningStatus.append(join_system_overlay(edgeToJoin, nodeName, logFile))
                if joiningStatus.count('Success') == len(overlay_dict[nodeName]):
                    JoinedOverlay = True
                    break
            ready_to_join.append("Ready")
        else:
            #For nodes other edges than d1 and node_id= 'a'
            #edgeToJoin = (ND.get_edge((ND.get_cluster(nodeName)[0:7])+str(int((ND.get_cluster(nodeName)[7:len(ND.get_cluster(nodeName))]))-1)))
            #edgeToJoin = (overlay_dict[nodeName])[1]
            time.sleep(60)
            edges_ready.append(nodeName)
            JoinedOverlay = False
            while JoinedOverlay == False:
                joiningStatus = []
                for edgeToJoin in overlay_dict[nodeName]:
                    while edgeToJoin not in edges_ready: #d1_ready==False:
                        #print('Waiting for edge '+edgeToJoin+' to be ready from:'+nodeName)
                        time.sleep(5)
                    #systemFun.exec_com("ping -c 2 "+ND.get_ip('d1'), nodeName)
                    print (nodeName+" Joining to edge in 10 sec "+edgeToJoin)
                    time.sleep(10)
                    joiningStatus.append(join_system_overlay(edgeToJoin, nodeName, logFile))
                if joiningStatus.count('Success') == len(overlay_dict[nodeName]):
                    JoinedOverlay = True
                    break
            ready_to_join.append("Ready")
            #edges_ready.append(nodeName)
    #print("Node Status Ready count: "+str(node_status.count("Ready")))
    if ND.get_rate(nodeName) == 'c1' and testFor == 'dev' and jobId != 'start':
        check_subscription(nodeName, logFile)
    node_status.append("Ready")
    print("Node Status Ready count: "+str(node_status.count("Ready")))
    #Doing operations on node d3
    if nodeName == 'd3' and jobId!="start":
        while (node_status.count("Ready")) != len(allNodes):
            print("Waiting for nodes to be ready for Executing operation")
            time.sleep(60)
        if not sub_fail:
            print("Executing operation")
            exec_operation('d3')
        else:
            print("Aborting as sub failed "+str(sub_fail))
    tmpchk = 0
    delta_waiting.append(nodeName)
    while (node_status.count("Ready")) != len(allNodes) and not sub_fail:
        time.sleep(10)
    os.system('docker exec mn.'+nodeName+' bash -c "vnstat -u"')
    time.sleep(5)
    os.system('docker exec mn.'+nodeName+' bash -c "vnstat -u"')
    time.sleep(5)
    os.system('docker exec mn.'+nodeName+' bash -c "vnstat > /opt/'+nodeName+'_bwLogsControl"')
    OpsCount = 1
    while deltaRecv == False and not sub_fail and jobId != 'start':
        #print ('Waiting deltaRecv '+nodeName+' '+str(tmpchk))
        if len(OpsDone) == OpsCount and nodeName!='d3':
            os.system('docker exec mn.'+nodeName+' bash -c "vnstat -u"')
            time.sleep(5)
            os.system('docker exec mn.'+nodeName+' bash -c "vnstat > /opt/'+nodeName+'_bwLogs'+str(OpsDone[-1])+'Ops"')
            OpsCount = OpsCount + 1
        with open('/home/ubuntu/Vin/laspdev/utility/log/'+logFile) as f:
            if delta_val[-1] in f.read() and delta_changed == True:
                print(str(tmpchk)+"Delta Received at Node "+nodeName)
                deltaRcvSys.append("True")
                deltaRecv = True
                delta_waiting.remove(nodeName)
                break
        time.sleep(34)
        tmpchk = tmpchk + 1
        if tmpchk > 20:
            print(str(tmpchk)+"Delta not yet Recevied at "+nodeName)
        if tmpchk >= 40:
            print ("MaxCheck expired, delta not received even after 20 mins at "+nodeName)
            if testFor == 'dev':
                check_subscription(nodeName, logFile)
            delta_fail.append(nodeName)
            deltaRcvSys.append("True")
            deltaRecv = True
            delta_waiting.remove(nodeName)
            break
        if delta_changed == False:
            tmpchk = tmpchk - 1
    print("\t ***********Test Completed at "+nodeName+"*********")
    time.sleep(5)
    while deltaRcvSys.count("True") != len(allNodes) and not sub_fail and len(delta_fail) < len(allNodes)/10 and jobId != 'start':
        #print(nodeName+" Waiting to close on Bandwidth")
        time.sleep(10)
    os.system('docker exec mn.'+nodeName+' bash -c "vnstat -u"')
    os.system('docker exec mn.'+nodeName+' bash -c "vnstat > /opt/'+nodeName+'_bwLogsData"')
    bw_collected.append(nodeName)
    test_completed.append(nodeName)

def check_subscription(nodeName, logFile):
    time.sleep(10)
    sub=False
    tmpchk = 0
    while sub==False and not sub_fail and len(delta_fail) < len(allNodes)/10:
        if tmpchk % 4 == 0:
            print (str(tmpchk)+' Subscription not yet done at '+nodeName)
        systemFun.exec_spec_com( 'lasp_delta_based_synchronization_backend:get_members(peer_rates).', nodeName)
        time.sleep(30)
        with open('/home/ubuntu/Vin/laspdev/utility/log/'+logFile) as f:
            temp = f.read()
            if '{"subscription",' in temp:
                print (str(tmpchk)+" Subscription done at "+nodeName)
                sub=True
                break
        #print(str(tmpchk)+"Subscription not yet done at "+nodeName)
        if tmpchk > 50:
            sub=True
            print(str(tmpchk)+" Max sub check exceeded for "+nodeName)
            sub_fail.append(nodeName)
            break
        tmpchk = tmpchk + 1


def exec_operation(nodeName):
    global delta_changed
    while node_status.count("Ready") != len(allNodes):
        print("***********Waiting 10 secs for nodes to be ready*******")
        time.sleep(10)
    print("Executing operations after 20 secs")
    valString = str(datetime.utcnow().strftime('timeis_%H_%M_%S_%f')[:-3])
    #valString = str('timeis_')+str(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20)))
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
    time.sleep(3)
    systemFun.exec_spec_com( 'AwMapVal = #{what => '+valString+'}.', nodeName)
    time.sleep(3)
    #systemFun.exec_spec_com( 'AwMapVal2 = #{what => i_am_vin_tej2}.', nodeName)
    #time.sleep(2)
    systemFun.exec_spec_com( '{ok, {AwMap, _, _, _}} = lasp:declare({AwMapVarName, AwMapType}, AwMapType).', nodeName)
    time.sleep(2)
    systemFun.exec_spec_com( '{ok, {AwMap1, _, _, _}} = lasp:update(AwMap, {apply, Key1, {set, Timestamp(), AwMapVal}}, self()).', nodeName)
    systemFun.exec_spec_com( 'lasp_delta_based_synchronization_backend:time_stamp().', nodeName)
    delta_val.pop(-1)
    delta_val.append(valString)
    time.sleep(5)
    time.sleep(5)
    for i in range(1, 300):
        if i % 50 == 49:
            print(str(i+1)+' updates done at '+nodeName)
            OpsDone.append(str(i+1))
            os.system('docker exec mn.'+nodeName+' bash -c "vnstat -u"')
            time.sleep(5)
            os.system('docker exec mn.'+nodeName+' bash -c "vnstat > /opt/'+nodeName+'_bwLogs'+str(OpsDone[-1])+'Ops"')
        valString = str(datetime.utcnow().strftime('timeis_%H_%M_%S_%f')[:-3])#+str(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20)))
        #valString = str('timeis_')+str(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20)))
        delta_val.append(valString)
        systemFun.exec_spec_com( 'AwMapVal'+str(i)+' = #{what => '+valString+'}.', nodeName)
        time.sleep(1)
        systemFun.exec_spec_com( '{ok, _} = lasp:update(AwMap, {apply, Key1, {set, nil, AwMapVal'+str(i)+'}}, self()).', nodeName)
        time.sleep(5)
    print("Operation execution completed")
    delta_changed = True


def join_system_overlay(ToNode, FromNode, logFile):
    time.sleep(5)
    execCom = False
    systemFun.exec_com("lasp_peer_service:join('"+ND.get_id(ToNode)+"@"+ND.get_ip(ToNode)+"').", FromNode)
    time.sleep(5)
    systemFun.exec_com("lasp_peer_service:members().", FromNode)
    time.sleep(5)
    tempCheck = 0
    tempConnection = 0
    while execCom == False and tempCheck <= 20 and not sub_fail and len(delta_fail) < len(allNodes)/10:
        if tempCheck % 4 == 0:
            print(str(tempCheck)+' Waiting overlay '+FromNode)
        with open('/home/ubuntu/Vin/laspdev/utility/log/'+logFile) as f:
            temp = f.read()
            if 'lasp_peer_service:join(' in temp and 'CRASH REPORT' not in temp:
                #if "{ok,['d@14.0.0.14','c@14.0.0.13','b@14.0.0.12','a@14.0.0.11']}"
                if (",'"+ND.get_id(ToNode)+"@"+ND.get_ip(ToNode)) in temp or ("'"+ND.get_id(ToNode)+"@"+ND.get_ip(ToNode)+"',") in temp or ("'"+ND.get_id(ToNode)+"@"+ND.get_ip(ToNode)+"']}") in temp:
                    print(str(tempCheck)+" "+FromNode+" Joined System Overlay")
                    execCom = True
                    break
                else:
                    if 'Node not yet connected' in temp:
                        f.close()
                        with open('/home/ubuntu/Vin/laspdev/utility/log/'+logFile, 'r') as f2:
                            lines = f2.readlines()
                        f2.close()
                        with open('/home/ubuntu/Vin/laspdev/utility/log/'+logFile, 'w') as f3:
                            for line in lines:
                                if "Node not yet connected" not in line.strip("\n"):
                                    f3.write(line)
                                else:
                                    f3.write("node Was not connected")
                        tempCheck = tempCheck - 1
                        tempConnection = tempConnection + 1
                        if tempConnection >= 10:
                            tempCheck = 30
                            tempConnection = 12
                            break
                        time.sleep(20)
                        f3.close()
                    if tempCheck % 4 == 0:
                        print(str(tempCheck)+" "+FromNode+" Not found Peer:"+ToNode)
                    systemFun.exec_com("lasp_peer_service:join('"+ND.get_id(ToNode)+"@"+ND.get_ip(ToNode)+"').", FromNode)
                    time.sleep(5)
                    systemFun.exec_com("lasp_peer_service:members().", FromNode)
                    time.sleep(20)
            else:
                systemFun.exec_com("lasp_peer_service:join('"+ND.get_id(ToNode)+"@"+ND.get_ip(ToNode)+"').", FromNode)
                time.sleep(5)
                systemFun.exec_com("lasp_peer_service:members().", FromNode)
                time.sleep(20)
                if 'CRASH REPORT' in temp:
                    if tempCheck % 4 == 0:
                        print (FromNode+" Crashed..."+str(tempCheck))
                    f.close()
                    with open('/home/ubuntu/Vin/laspdev/utility/log/'+logFile, 'r') as f2:
                        lines = f2.readlines()
                    f2.close()
                    with open('/home/ubuntu/Vin/laspdev/utility/log/'+logFile, 'w') as f3:
                        for line in lines:
                            if 'CRASH REPORT' not in line.strip("\n"):
                                f3.write(line)
                    f3.close()
                    return 'CRASHED'
                if tempCheck % 4 == 0:
                    print (FromNode+" Retrying")
        time.sleep(5)
        if tempCheck >= 20:
            execCom = True
            break
        tempCheck = tempCheck + 1
    return 'Success'


def join_system_internal(nodeName, logFile):
    time.sleep(5)
    execCom = False
    systemFun.exec_com("lasp_peer_service:join('"+ND.get_id(ND.get_edge(ND.get_cluster(nodeName)))+"@"+ND.get_ip(ND.get_edge(ND.get_cluster(nodeName)))+"').", nodeName)
    time.sleep(5)
    systemFun.exec_com("lasp_peer_service:members().", nodeName)
    time.sleep(5)
    tempCheck = 0
    tempConnection = 0
    while execCom == False and tempCheck <= 20 and not sub_fail and len(delta_fail) < len(allNodes)/10:
        if tempCheck % 4 == 0:
            print (str(tempCheck)+" Checking from "+nodeName)
        with open('/home/ubuntu/Vin/laspdev/utility/log/'+logFile) as f:
            temp = f.read()
            if 'lasp_peer_service:join(' in temp and 'CRASH REPORT' not in temp:
                if (",'"+ND.get_id(ND.get_edge(ND.get_cluster(nodeName)))+"@"+ND.get_ip(ND.get_edge(ND.get_cluster(nodeName)))) in temp or ("'"+ND.get_id(ND.get_edge(ND.get_cluster(nodeName)))+"@"+ND.get_ip(ND.get_edge(ND.get_cluster(nodeName)))+"',") in temp or ("'"+ND.get_id(ND.get_edge(ND.get_cluster(nodeName)))+"@"+ND.get_ip(ND.get_edge(ND.get_cluster(nodeName)))+"']}") in temp:
                    print(str(tempCheck)+" "+nodeName+" Joined internal system ")
                    execCom = True
                    break
                else:
                    if 'Node not yet connected' in temp:
                        f.close()
                        with open('/home/ubuntu/Vin/laspdev/utility/log/'+logFile, 'r') as f2:
                            lines = f2.readlines()
                        f2.close()
                        with open('/home/ubuntu/Vin/laspdev/utility/log/'+logFile, 'w') as f3:
                            for line in lines:
                                if "Node not yet connected" not in line.strip("\n"):
                                    f3.write(line)
                                else:
                                    f3.write("node Was not connected")
                        tempCheck = tempCheck - 1
                        tempConnection = tempConnection + 1
                        if tempConnection > 10:
                            tempCheck = 30
                            tempConnection = 22
                            break
                        time.sleep(20)
                        f3.close()
                    if tempCheck % 4 == 0:
                        print(str(tempCheck)+" "+nodeName+"Not found edge Peer in "+ND.get_id(ND.get_edge(ND.get_cluster(nodeName)))+"@"+ND.get_ip(ND.get_edge(ND.get_cluster(nodeName))))
                    systemFun.exec_com("lasp_peer_service:join('"+ND.get_id(ND.get_edge(ND.get_cluster(nodeName)))+"@"+ND.get_ip(ND.get_edge(ND.get_cluster(nodeName)))+"').", nodeName)
                    time.sleep(5)
                    systemFun.exec_com("lasp_peer_service:members().", nodeName)
                    time.sleep(20)
            else:
                systemFun.exec_com("lasp_peer_service:join('"+ND.get_id(ND.get_edge(ND.get_cluster(nodeName)))+"@"+ND.get_ip(ND.get_edge(ND.get_cluster(nodeName)))+"').", nodeName)
                time.sleep(5)
                systemFun.exec_com("lasp_peer_service:members().", nodeName)
                time.sleep(20)
                if 'CRASH REPORT' in temp:
                    if tempCheck % 4 == 0:
                        print(nodeName+" Crashed...")
                    f.close()
                    with open('/home/ubuntu/Vin/laspdev/utility/log/'+logFile, 'r') as f2:
                        lines = f2.readlines()
                    f2.close()
                    with open('/home/ubuntu/Vin/laspdev/utility/log/'+logFile, 'w') as f3:
                        for line in lines:
                            if "CRASH REPORT" not in line.strip("\n"):
                                f3.write(line)
                    f3.close()
                if tempCheck % 4 == 0:
                    print(str(tempCheck)+" "+"Retrying from "+nodeName)
        time.sleep(5)
        if tempCheck >= 20:
            execCom = True
            break
        tempCheck = tempCheck + 1

def stop_system(nodeName):
    systemFun.stop_node(nodeName)
    #print("Executed stop_node() sleep 4")
    time.sleep(4)
    systemFun.exec_com("", nodeName)
    systemFun.exec_com("", nodeName)
    #print("2 enters sleep 4")
    time.sleep(4)
    systemFun.exec_com("", nodeName)
    systemFun.exec_com("", nodeName)
    systemFun.exec_com("exit", nodeName)
    #print("exit sleep 4")
    time.sleep(4)
    systemFun.exec_com("", nodeName)
    #print('Stopped Node:'+nodeName)
    stopped_node.append(nodeName)

def bw_log(nodeName):
        os.system('docker exec mn.'+nodeName+' bash -c "date > /opt/'+nodeName+'_bwLogs"')
        os.system('docker exec mn.'+nodeName+' bash -c "iftop -i '+nodeName+'-eth0 -t >> /opt/'+nodeName+'_bwLogs"')

def bw_threads_stop():
    tmp = 0
    while len(bw_collected) != len(allNodes): #and not sub_fail and not delta_fail:
            #print('Waiting For delta to be received by all')
            if tmp % 4 == 0:
                print("Delta Waiting for"+str(delta_waiting))
            #print("Waiting for Delta To be received by all")
            time.sleep(60)
            tmp = tmp + 1
    time.sleep(10)
    #for thread in bw_threads:
    #    thread.terminate()
    #print("Threads stopped")
    if sub_fail:
        print("******FAILED SUB "+str(sub_fail)+" ******")
    if delta_fail:
        print("******FAILED delta "+str(delta_fail)+" ******")

def start_testing():
    global jobId
    threads_main = []
    print("AllNodes: "+str(allNodes))
    for node in allNodes:
            #print node
            threads_main.append(Thread(target=start_system, args=(node,)))
            #if jobId != 'start': #and jobId != 'deltaTest':
                #bw_threads.append(multiprocessing.Process(target=bw_log, args=(node,)))
                #bw_threads[-1].start()
            threads_main[-1].start()
    if jobId != 'start': #and jobId != 'deltaTest':
        bw_threads_stop()

def stop_testing(jobId):
    global testFor, start_time
    threads_main=[]
    for node in allNodes:
            #print node
            threads_main.append(Thread(target=stop_system, args=(node,)))
            threads_main[-1].start()
    #print("Stopped")
    mainfolder = jobId
    folder = testFor #str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    if not (os.path.isdir("/home/ubuntu/Vin/laspdev/results/"+mainfolder)):
        os.system("mkdir /home/ubuntu/Vin/laspdev/results/"+mainfolder)
    os.system("mkdir /home/ubuntu/Vin/laspdev/results/"+mainfolder+"/"+folder)
    os.system("mkdir /home/ubuntu/Vin/laspdev/results/"+mainfolder+"/"+folder+"/nodeLogs")
    os.system("mkdir /home/ubuntu/Vin/laspdev/results/"+mainfolder+"/"+folder+"/BWLogs")
    os.system("cp /home/ubuntu/Vin/laspdev/utility/log/* /home/ubuntu/Vin/laspdev/results/"+mainfolder+"/"+folder+"/nodeLogs")
    os.system("cp /home/ubuntu/Vin/laspdev/utility/NodeDirectory.txt /home/ubuntu/Vin/laspdev/results/"+mainfolder+"/")
    for node in allNodes:
        #os.system('docker exec mn.'+nodeName+' bash -c "vnstat -u"')
        #os.system('docker exec mn.'+nodeName+' bash -c "vnstat > /opt/'+nodeName+'_bwLogs"')
        os.system("docker cp mn."+node+":/opt/"+node+"_bwLogsControl /home/ubuntu/Vin/laspdev/results/"+mainfolder+"/"+folder+"/BWLogs")
        os.system("docker cp mn."+node+":/opt/"+node+"_bwLogsData /home/ubuntu/Vin/laspdev/results/"+mainfolder+"/"+folder+"/BWLogs")
        for ops in OpsDone:
            os.system("docker cp mn."+node+":/opt/"+node+"_bwLogs"+str(ops)+"Ops /home/ubuntu/Vin/laspdev/results/"+mainfolder+"/"+folder+"/BWLogs")
    while len(stopped_node) != len(allNodes):
        #print('Waiting to stop')
        time.sleep(10)
    print("delta_vals: "+str(delta_val))
    print("Stopped Nodes: "+str(stopped_node))
    print("*******JOB "+jobId+" FINISHED at "+str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])+" StartTime:"+start_time+"*******")

#Start main here
if __name__ == "__main__":
    print ("Starting")
    global start_time
    start_time = str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
    os.system("date")
    #if len(sys.argv) > 1:
    #    if sys.argv[1] == "start":
    #        print ("Starting")
    #        start_testing()
    #    elif sys.argv[1] == "stop":
    #        print ("Stopping")
    #        stop_testing()
    #else:
    #    print ("Do both")
    global jobId
    if len(sys.argv) > 1:
        jobId = sys.argv[1]
        if jobId == "start":
                print ("Starting")
                start_testing()
                while len(test_completed) != len(allNodes):
                    print('Waiting test_completed '+str(list(set(allNodes) - set(test_completed))))
                    time.sleep(50)
                print ("*******JOB "+jobId+" FINISHED*******")
        elif jobId == "deltaTest":
            print ("Starting DeltaTest")
            start_testing()
            while len(test_completed) != len(allNodes):
                print('Waiting test_completed '+str(list(set(allNodes) - set(test_completed))))
                time.sleep(50)
            print ("*******JOB "+jobId+" FINISHED*******")
        else:
            print("********STARTING "+jobId+" ***********")
            start_testing()
            stop_testing(jobId)
    #print("\t******AUTO TESTING COMPLETED*****")
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
            os.system("mkdir /home/ubuntu/Vin/laspdev/results/"+folder)
            os.system("cp /home/ubuntu/Vin/laspdev/utility/log/* /home/ubuntu/Vin/laspdev/results/"+folder)
            for node in allNodes:
                os.system("docker cp mn."+node+":/opt/"+node+"_bwLogs /home/ubuntu/Vin/laspdev/results/"+folder)
    '''
