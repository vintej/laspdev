import pickle
import os
import sys

nodes = {}
operate = sys.argv[1]
def flattenList(data):
        results = []
        for rec in data:
            if isinstance(rec, list):
                results.extend(rec)
                results = flattenList(results)
            else:
                results.append(rec)
        return results



def get_allNodes():
    global node
    with open("NodeDirectory.txt", "rb") as fp:
            node = pickle.load(fp)
    allNodes = []
    for cluster in node.keys():
        allNodes.append(node[cluster].keys())
    return flattenList(allNodes)

print get_allNodes()
sessions = []
for cluster in node:
    #print "Session: "+session+" "+str(node[session])
    temp = node[cluster]
    if operate == "start":
        os.system("screen -d -m -S "+cluster+"")
        for d in temp:
            print "screen -t command "+str(cluster)+" for node "+d
            os.system("screen -S "+cluster+" -X screen -t "+d)
            os.system("screen -S "+cluster+" -p "+d+" -X stuff 'screen -X logfile /home/ubuntu/laspdev/utility/log/"+d+"_log^M'")
            os.system("screen -S "+cluster+" -p "+d+" -X stuff 'screen -X log on^M'")
    elif operate == "stop":
        os.system("screen -S "+cluster+" -p 0 -X stuff 'screen -X quit^M'")
    #screen -S newsession -p $n -X stuff hello$n
    #if 'd1' in node[session]:
    #    print node[session]

print sessions

