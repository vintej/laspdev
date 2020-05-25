from threading import Thread
import multiprocessing
import os
import time

d1_ready = False
ready_to_join = False

def start_node(nodeName):
    global d1_ready, ready_to_join
    if nodeName != 'd1' and nodeName != 'd5':
        while ready_to_join == False:
            print('Waiting for d1 from:'+nodeName)
            time.sleep(2)
        os.system('python utility/test.py')
    else:
        if nodeName=='d1':
            os.system('python utility/test.py')
            d1_ready = True
        else:
            while d1_ready==False:
                print('Waiting fro d1 from:'+nodeName)
                time.sleep(2)
            os.system('python utility/test.py')
            ready_to_join = True

#Start main here
if __name__ == "__main__":
        allNodes = ['d1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8' ]
        threads = []
        for node in allNodes:
            print node
            threads.append(Thread(target=start_node, args=(node,)))
            threads[-1].start()
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
