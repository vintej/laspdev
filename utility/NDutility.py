import pickle
import os
import sys

with open("NodeDirectory.txt", "rb") as fp:
    node = pickle.load(fp)

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
    allNodes = []
    for cluster in node.keys():
        allNodes.append(node[cluster].keys())
    return flattenList(allNodes)

def get_cluster(nodeName):
    for cluster in node:
        if nodeName in node[cluster]:
            return cluster

def get_ip(nodeName):
    for cluster in node:
        if nodeName in node[cluster]:
            return node[cluster][nodeName]['ip']

def get_id(nodeName):
    for cluster in node:
        if nodeName in node[cluster]:
            return node[cluster][nodeName]['node']

def get_rate(nodeName):
    for cluster in node:
        if nodeName in node[cluster]:
            return node[cluster][nodeName]['rate']

#print get_allNodes()
if __name__ == '__main__':
    nodeName = sys.argv[1]
    print ('Node Name: '+nodeName)
    print ('Cluster: '+get_cluster(nodeName))
    print ('IP: '+get_ip(nodeName))
    print ('ID:'+get_id(nodeName))
    print('Rate:'+get_rate(nodeName))
