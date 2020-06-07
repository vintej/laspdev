import pickle
import os
import sys

with open("/home/ubuntu/laspdev/utility/NodeDirectory.txt", "rb") as fp:
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

def get_dict():
    return node

def get_allClusters():
    global node
    allClusters = []
    for cluster in node.keys():
        allClusters.append(cluster)
    return allClusters

def get_cluster(nodeName):
    for cluster in node:
        if nodeName in node[cluster]:
            return cluster

def get_clusterNodes(clusterno):
    nodelist = []
    for cluster in node:
        if cluster == clusterno:
            return node[cluster].keys()


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

def get_edge(cluster):
    for nodeName in node[cluster]:
        if get_id(nodeName)=='a':
            return nodeName

def get_allEdges():
        edge = []
        for cluster in node:
            edge.append(get_edge(cluster))
        return edge

#print get_allNodes()
if __name__ == '__main__':
    nodeName = sys.argv[1]
    print ('Node Name: '+nodeName)
    print ('Cluster: '+get_cluster(nodeName))
    print ('IP: '+get_ip(nodeName))
    print ('ID:'+get_id(nodeName))
    print ('Rate:'+get_rate(nodeName))
    print ('EdgeNode:'+str(get_edge(get_cluster(nodeName))))
    print (get_id(get_edge(get_cluster(nodeName))))
    print (get_ip(get_edge(get_cluster(nodeName))))
    print (get_allEdges())
    print (str(len(get_allEdges())))
