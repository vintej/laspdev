import pickle

node = {}
session = "cluster1"
tempnode = 'd1'
numberOfnodes = 100
nodesPerCluster = 10
c1_nodes = ['a', 'c', 'd', 'e', 'f', 'i', 'j', 'g', 'h']
c3_nodes = []
#until j
nodename = 'a'
network = 10
ip = 10



def node_name(nodename, i):
    global nodesPerCluster
    if i%nodesPerCluster == 0:
        return str(chr(ord(nodename)+i%nodesPerCluster+nodesPerCluster-1))
    else:
        return str(chr(ord(nodename)+i%nodesPerCluster-1))

for i in range(1,numberOfnodes+1):
    if i%nodesPerCluster == 1 and i>nodesPerCluster:
                session = session[0:7] + str((int(session[7:8])+1))
                nodename = 'a'
                network = network + 1
                ip = 10
    #print("node at session "+session+":"+node_name(nodename, i))
    if session in node:
        nodetemp = node[session]
    else:
        nodetemp = {}
    ip = ip + 1
    nodeinfo = {}
    nodeinfo['ip'] = str(str(network)+".0.0."+str(ip))
    nodeinfo['node'] = node_name(nodename, i)
    if node_name(nodename, i) in c1_nodes:
        nodeinfo['rate'] = 'c1'
    elif node_name(nodename, i) in c3_nodes:
        nodeinfo['rate'] = 'c3'
    else:
        nodeinfo['rate'] = 'c2'
    nodetemp["d"+str(i)] = nodeinfo
    node.update({session:nodetemp})
    #print node[session]

for x in node:
        print ("\n "+(x)+ " " + str(node[x]))

with open("/home/ubuntu/laspdev/utility/NodeDirectory.txt", 'wb') as fp:
    pickle.dump(node, fp)


'''
def flattenList(data):
        results = []
        for rec in data:
            if isinstance(rec, list):
                results.extend(rec)
                results = flattenList(results)
            else:
                results.append(rec)
        return results

#for x in node:
#            print "\n "+(x)+ " " + str(node[x])

print (node.keys())

def get_allNodes():
    with open("NodeDirectory.txt", "rb") as fp:
            node = pickle.load(fp)
    allNodes = []
    for cluster in node.keys():
        allNodes.append(node[cluster].keys())
    return flattenList(allNodes)
'''
#print (get_allNodes())
