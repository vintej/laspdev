import utility.NDutility4net as ND
import itertools
import pickle

with open("utility/NodeDirectory.txt", "rb") as fp:
        node = pickle.load(fp)

for i in range(1, len(node)+1):
            print "\n Cluster"+str(i)+ " " #+ str(sorted(node['cluster'+str(i)].keys()))
            for d in node['cluster'+str(i)]:
                print("Node "+d+" : "+str(node['cluster'+str(i)][d]))
#print (ND.get_allNodes())
for node in ND.get_allNodes():
    if  ND.get_id(node) == 'a':
        print ("Edge Node in "+ND.get_cluster(node)+" Node:"+node+" nodeName:"+ND.get_id(node)+" ip:"+ND.get_ip(node)+" rate"+ND.get_rate(node))

cluster_switch = {}
i=1
for cluster in ND.get_allClusters():
    cluster_switch[cluster] = str('s'+str(cluster[7:8]))

#print (cluster_switch)
for i in range(1, len(cluster_switch)+1):
        print("Switch for cluster"+str(i)+": "+str(cluster_switch['cluster'+str(i)]))

node_objects = {}
for node in ND.get_allNodes():
        node_objects[node] = node+'object'
        #print(ND.get_ip(node))

#print (node_objects)

#print (ND.get_clusterNodes('cluster2'))
#for cluster in cluster_switch:
#    for anode in ND.get_clusterNodes(cluster):
#        print(node_objects[anode]+" & "+cluster_switch[cluster])

#for cluster in cluster_switch:
#    listtoping = []
#    for anode in ND.get_clusterNodes(cluster):
#        listtoping.append(node_objects[anode])
#    print("net.ping("+str(listtoping)+")")

#a_list = [1, 2, 3, 4]

#list_cycle = itertools.cycle(a_list)
#next(list_cycle)

#for i in range(8):
#        next_element = next(list_cycle)
#        print(next_element)

#node_objects = {}
#for node in ND.get_allNodes():
#        print ((ND.get_ip(node)))
