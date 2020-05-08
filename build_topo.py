#!/usr/bin/python
"""
This is the most simple example to showcase Containernet.
"""
from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
setLogLevel('info')

net = Containernet(controller=Controller)
info('*** Adding controller\n')
net.addController('c0')
info('*** Adding docker containers\n')
d1 = net.addDocker('d1', ip='10.0.0.250', dimage="vinayaktj/lasp:dev")
d2 = net.addDocker('d2', ip='10.0.0.251', dimage="vinayaktj/lasp:base")
d3 = net.addDocker('d3', ip='10.0.0.252', dimage="vinayaktj/lasp:base")
d4 = net.addDocker('d4', ip='10.0.0.253', dimage="vinayaktj/lasp:base")
d5 = net.addDocker('d5', ip='11.0.0.250', dimage="vinayaktj/lasp:base")
d6 = net.addDocker('d6', ip='11.0.0.251', dimage="vinayaktj/lasp:base")
d7 = net.addDocker('d7', ip='11.0.0.252', dimage="vinayaktj/lasp:base")
d8 = net.addDocker('d8', ip='11.0.0.253', dimage="vinayaktj/lasp:base")
info('*** Adding switches\n')
s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')
info('*** Creating links\n')
net.addLink(s1, s2, cls=TCLink, delay='100ms', bw=1)
net.addLink(d1, s1, cls=TCLink, delay='50ms', bw=1)
net.addLink(d2, s1, cls=TCLink, delay='50ms', bw=1)
net.addLink(d3, s1, cls=TCLink, delay='50ms', bw=1)
net.addLink(d4, s1, cls=TCLink, delay='50ms', bw=1)
net.addLink(d5, s2, cls=TCLink, delay='50ms', bw=1)
net.addLink(d6, s2, cls=TCLink, delay='50ms', bw=1)
net.addLink(d7, s2, cls=TCLink, delay='50ms', bw=1)
net.addLink(d8, s2, cls=TCLink, delay='50ms', bw=1)
info('*** Starting network\n')
net.start()
info('*** Testing connectivity\n')
net.ping([d1, d2, d3, d4])
net.ping([d5, d6, d7, d8])
info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()

