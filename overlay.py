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
import time
from threading import Thread
import sys

scnode = ND.get_dict()
screens_ready = []
def start_screens(temp, cluster):
        os.system("screen -d -m -S "+cluster+"")
        for d in temp:
                print ("screen -t command "+str(cluster)+" for node "+d)
                os.system("screen -S "+cluster+" -X screen -t "+d)
                os.system("screen -S "+cluster+" -p "+d+" -X stuff 'screen -X logfile /home/ubuntu/Vin/laspdev/utility/log/"+d+"_log.%n^M'")
                os.system("screen -S "+cluster+" -p "+d+" -X stuff 'screen -X log on^M'")
                time.sleep(2)
                screens_ready.append("Ready")
        #elif operate == "stop":
        #    os.system("screen -S "+cluster+" -p 0 -X stuff 'screen -X quit^M'")

def stop_screens():
    for cluster in scnode:
        os.system("screen -S "+cluster+" -p 0 -X stuff 'screen -X quit^M'")
    os.system("rm /home/ubuntu/Vin/laspdev/utility/log/*")

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
lasp_dev="vinayaktj/lasp:devsquashed"
#chosen_image = lasp_dev
#Default
chosen_image = lasp_base
if sys.argv[1] == 'dev':
    chosen_image=lasp_dev
else:
    chosen_image=lasp_base
print("CHOSEN IMAGE "+chosen_image)
node_objects = {}
edgeNodes = []
container_ready = []

def start_container(cluster):
    global chosen_image, net
    for node in cluster:
        print("node_objects["+node+"] = net.addDocker("+node+", ip="+str(ND.get_ip(node))+", dimage=chosen_image)")
        node_objects[node] = net.addDocker(node, ip=str(ND.get_ip(node)), dimage=chosen_image)
        if ND.get_id(node)=='a':
            #print("node_objects["+node+"] = net.addDocker("+node+", ip="+str(ND.get_ip(node))+", dimage=chosen_image)")
            #node_objects[node] = net.addDocker(node, ip=str(ND.get_ip(node)), dimage=chosen_image)
            edgeNodes.append(node)
        container_ready.append("Ready")
        #print ('node_objects[node].cmd("ip route add default via '+(str(ND.get_ip(node))[0:8]+'0')+' '+node+'-eth0)')
        #node_objects[node].cmd("ip route add default via "+(str(ND.get_ip(node))[0:8]+'0')+" "+node+"-eth0")


threads_container = []
for cluster in scnode:
    threads_container.append(Thread(target=start_container, args=(scnode[cluster],)))
    threads_container[-1].start()

while container_ready.count("Ready") != len(ND.get_allNodes()):
    time.sleep(10)
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
    print("cluster_swithc["+cluster+"] = net.addSwitch("+'s'+cluster[7:len(cluster)])
    cluster_switch[cluster] = net.addSwitch('s'+cluster[7:len(cluster)])
'''
s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')
'''
info('*** Creating links\n')
router = net.addDocker('r0', cls=LinuxRouter, ip='10.0.0.10/8')
for i in range(1, len(cluster_switch)+1):
        print("cluster_switch['cluster"+str(i)+"'] ="+str(cluster_switch['cluster'+str(i)])+" r0-eth"+str(i)+" ip:1"+str(i-1)+".0.0.10/8")
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
for node in edgeNodes:
    node_objects[node].cmd("ip route del default via 172.17.0.1 dev eth0")
    print(node+':'+str(overlay_dict[node]))
    #overlaytocon = overlay_dict[node]
    for overlays in overlay_dict[node]:
        if node=='d21':
            print("From node "+node+" overlays are "+str(overlay_dict[node]))
            print("Trying to get ip for "+overlays+" :"+str(ND.get_ip(overlays)))
        print('ip route add '+(str(ND.get_ip(overlays))[0:7]+'0/8 via '+(str(ND.get_ip(node))[0:8]+'0')))
        node_objects[node].cmd('ip route add '+(str(ND.get_ip(overlays))[0:7]+'0/8 via '+(str(ND.get_ip(node))[0:8]+'0')))
time.sleep(5)
print('')
net.ping(edgestoping, timeout='1')
'''
net.ping([d1, d2, d3, d4])
net.ping([d5, d6, d7, d8])
'''
info('*** Starting Screen Sessions \n')
threads_screen = []
for cluster in scnode:
    threads_screen.append(Thread(target=start_screens, args=(scnode[cluster],cluster)))
    threads_screen[-1].start()
while screens_ready.count("Ready") != len(ND.get_allNodes()):
    time.sleep(5)
info('*** Running CLI\n')
CLI(net)
info('*** Stopping network\n')
net.stop()
info('*** Stopping Screen Sessions \n')
stop_screens()

