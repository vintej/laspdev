import pickle
import os
import sys
#import NDutility as ND
import NDutility4net as ND



node = ND.get_dict()
def start_screens():
    for cluster in node:
        #print "Session: "+session+" "+str(node[session])
        temp = node[cluster]
        #if operate == "start":
        os.system("screen -d -m -S "+cluster+"")
        for d in temp:
                print ("screen -t command "+str(cluster)+" for node "+d)
                os.system("screen -S "+cluster+" -X screen -t "+d)
                os.system("screen -S "+cluster+" -p "+d+" -X stuff 'screen -X logfile /home/ubuntu/laspdev/utility/log/"+d+"_log^M'")
                os.system("screen -S "+cluster+" -p "+d+" -X stuff 'screen -X log on^M'")
        #elif operate == "stop":
        #    os.system("screen -S "+cluster+" -p 0 -X stuff 'screen -X quit^M'")

def stop_screens():
    for cluster in node:
        os.system("screen -S "+cluster+" -p 0 -X stuff 'screen -X quit^M'")

if __name__ == '__main__':
    operate = sys.argv[1]
    if operate == 'start':
        start_screens()
    elif operate == 'stop':
        stop_screens()

