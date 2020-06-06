#!/usr/bin/python
"""
This is the most simple example to showcase Containernet.
"""
from mininet.net import Containernet
from mininet.node import Controller, RemoteController, Node
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
import utility.NDutility4net as ND
import os

scnode = ND.get_dict()
def start_screens():
    for cluster in scnode:
        #print "Session: "+session+" "+str(node[session])
        temp = scnode[cluster]
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
    for cluster in scnode:
        os.system("screen -S "+cluster+" -p 0 -X stuff 'screen -X quit^M'")

setLogLevel('info')

class LinuxRouter( Node ):
        "A Node with IP forwarding enabled."

        def config( self, **params ):
            super( LinuxRouter, self).config( **params )
            # Enable forwarding on the router
            self.cmd( 'sysctl net.ipv4.ip_forward=1' )

        def terminate( self ):
            self.cmd( 'sysctl net.ipv4.ip_forward=0' )
            super( LinuxRouter, self ).terminate()

net = Containernet(controller=Controller)
info('*** Adding controller\n')
#net.addController('pox', controller=RemoteController, ip='127.0.0.1', port=6633)
net.addController('c0')
info('*** Adding docker containers\n')
lasp_base="vinayaktj/lasp:base"
lasp_dev="vinayaktj/lasp:dev"
chosen_image = lasp_dev
#chosen_image = lasp_base
node_objects = {}
edgeNodes = []
for node in ND.get_allNodes():
    print("node_objects["+node+"] = net.addDocker("+node+", ip="+str(ND.get_ip(node))+", dimage=chosen_image)")
    node_objects[node] = net.addDocker(node, ip=str(ND.get_ip(node)), dimage=chosen_image)
    if ND.get_id(node)=='a':
        edgeNodes.append(node)
        #print ('node_objects[node].cmd("ip route add default via '+(str(ND.get_ip(node))[0:8]+'0')+' '+node+'-eth0)')
        #node_objects[node].cmd("ip route add default via "+(str(ND.get_ip(node))[0:8]+'0')+" "+node+"-eth0")
'''
d1 = net.addDocker('d1', ip='10.0.0.250', dimage=chosen_image)
d2 = net.addDocker('d2', ip='10.0.0.251', dimage=chosen_image)
d3 = net.addDocker('d3', ip='10.0.0.252', dimage=chosen_image)
d4 = net.addDocker('d4', ip='10.0.0.253', dimage=chosen_image)
d5 = net.addDocker('d5', ip='11.0.0.250', dimage=chosen_image)
d6 = net.addDocker('d6', ip='11.0.0.251', dimage=chosen_image)
d7 = net.addDocker('d7', ip='11.0.0.252', dimage=chosen_image)
d8 = net.addDocker('d8', ip='11.0.0.253', dimage=chosen_image)
'''
info('*** Adding switches\n')
cluster_switch = {}
for cluster in ND.get_allClusters():
    print("cluster_swithc["+cluster+"] = net.addSwitch("+'s'+cluster[7:8])
    cluster_switch[cluster] = net.addSwitch('s'+cluster[7:8])
'''
s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')
'''
info('*** Creating links\n')
router = net.addDocker('r0', cls=LinuxRouter, ip='10.0.0.10/8')
for i in range(1, len(cluster_switch)+1):
        net.addLink(cluster_switch['cluster'+str(i)], router, intfName2='r0-eth'+str(i), params2={'ip':'1'+str(i-1)+'.0.0.10/8'})
        print("net.addLink cluster_switch["+'cluster'+str(i)+"]),router, intfName2= 'r0-eth"+str(i)+", params2={'ip':'1"+str(i-1)+".0.0.10/8")
        #net.addLink(s1, router, intfName2='r0-eth1', params2={'ip':'10.0.0.10/8'})

#'''
#net.addLink(s1, s2, cls=TCLink, delay='100ms', bw=1)
#'''
for cluster in cluster_switch:
    for anode in ND.get_clusterNodes(cluster):
        print("net.addLink(node_objects"+anode+"__"+str(node_objects[anode])+", "+str(cluster_switch[cluster])+", delay='50ms', bw=1)")
        net.addLink(node_objects[anode], cluster_switch[cluster], delay='50ms', bw=1)
'''
net.addLink(d1, s1, cls=TCLink, delay='50ms', bw=1)
net.addLink(d2, s1, cls=TCLink, delay='50ms', bw=1)
net.addLink(d3, s1, cls=TCLink, delay='50ms', bw=1)
net.addLink(d4, s1, cls=TCLink, delay='50ms', bw=1)
net.addLink(d5, s2, cls=TCLink, delay='50ms', bw=1)
net.addLink(d6, s2, cls=TCLink, delay='50ms', bw=1)
net.addLink(d7, s2, cls=TCLink, delay='50ms', bw=1)
net.addLink(d8, s2, cls=TCLink, delay='50ms', bw=1)
'''
info('*** Starting network\n')
net.start()
info('*** Testing connectivity\n')
edgestoping = []
for cluster in cluster_switch:
    listtoping = []
    for anode in ND.get_clusterNodes(cluster):
        listtoping.append(node_objects[anode])
        if ND.get_id(anode) == 'a':
            edgestoping.append(node_objects[anode])
    print("net.ping("+str(listtoping)+")")
    net.ping(listtoping, timeout='1')

for node in edgeNodes:
    node_objects[node].cmd("ip route del default via 172.17.0.1 dev eth0")
    node_objects[node].cmd('ip route add default via '+(str(ND.get_ip(node))[0:8]+'0'))
net.ping(edgestoping, timeout='1')
'''
net.ping([d1, d2, d3, d4])
net.ping([d5, d6, d7, d8])
'''
info('*** Starting Screen Sessions \n')
start_screens()
#d1.cmd("ip route del default via 172.17.0.1 dev eth0 && ip route add default dev d1-eth0")
#d5.cmd("ip route del default via 172.17.0.1 dev eth0 && ip route add default dev d5-eth0")'''
info('*** Running CLI\n')
CLI(net)
info('*** Stopping network\n')
net.stop()
info('*** Stopping Screen Sessions \n')
stop_screens()

