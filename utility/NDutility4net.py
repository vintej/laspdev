import pickle
import os
import sys

with open("/home/ubuntu/laspdev/utility/NodeDirectory.txt", "rb") as fp:
    node = pickle.load(fp)

#print (node)
def flattenList(data):
        results = []
        for rec in data:
            if isinstance(rec, list):
                results.extend(rec)
                results = flattenList(results)
            else:
                results.append(rec)
        return list(results)

def get_allNodes():
    global node
    allNodes = []
    for cluster in node.keys():
        allNodes.append(list(node[cluster]))
    #print (list(allNodes))
    return list(flattenList(allNodes))

def get_dict():
        return node

def get_allClusters():
    global node
    allClusters = []
    for cluster in node.keys():
        allClusters.append(cluster)
    return list(allClusters)

def get_cluster(nodeName):
    for cluster in node:
        if nodeName in node[cluster]:
            return str(cluster)

def get_clusterNodes(clusterno):
    nodelist = []
    for cluster in node:
        if cluster == clusterno:
            return list(list(node[cluster]))


def get_ip(nodeName):
    for cluster in node:
        if nodeName in node[cluster]:
            return str(node[cluster][nodeName]['ip'])

def get_id(nodeName):
    for cluster in list(node):
        if nodeName in list(node[cluster]):
            return str(node[cluster][nodeName]['node'])

def get_rate(nodeName):
    for cluster in node:
        if nodeName in node[cluster]:
            return str(node[cluster][nodeName]['rate'])

#print get_allNodes()
if __name__ == '__main__':
    nodeName = sys.argv[1]
    print ('Node Name: '+nodeName)
    print ('Cluster: '+get_cluster(nodeName))
    print ('IP: '+get_ip(nodeName))
    print ('ID:'+get_id(nodeName))
    print('Rate:'+get_rate(nodeName))
