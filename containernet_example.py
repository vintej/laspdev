#!/usr/bin/python
"""
This is the most simple example to showcase Containernet.
"""
from mininet.net import Containernet
from mininet.node import Controller
from mininet.node import Node
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
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
net.addController('c0')
info('*** Adding docker containers\n')
d1 = net.addDocker('d1', ip='10.0.0.11/16', dimage="ubuntu:trusty", defaultRoute='via 10.0.0.10')
'''
d2 = net.addDocker('d2', ip='10.0.0.12', dimage="ubuntu:trusty")
d3 = net.addDocker('d3', ip='10.0.0.13', dimage="ubuntu:trusty")
d4 = net.addDocker('d4', ip='10.0.0.14', dimage="ubuntu:trusty")
d5 = net.addDocker('d5', ip='10.0.0.15', dimage="ubuntu:trusty")
d6 = net.addDocker('d6', ip='11.0.0.11', dimage="ubuntu:trusty", defaultRoute = 'via 11.0.0.10')
d7 = net.addDocker('d7', ip='11.0.0.12', dimage="ubuntu:trusty")
d8 = net.addDocker('d8', ip='11.0.0.13', dimage="ubuntu:trusty")
d9 = net.addDocker('d9', ip='11.0.0.14', dimage="ubuntu:trusty")
d10 = net.addDocker('d10', ip='11.0.0.15', dimage="ubuntu:trusty")
'''
d11 = net.addDocker('d11', ip='12.0.0.11', dimage="ubuntu:trusty", defaultRoute = 'via 12.0.0.10')
'''
d12 = net.addDocker('d12', ip='12.0.0.12', dimage="ubuntu:trusty")
d13 = net.addDocker('d13', ip='12.0.0.13', dimage="ubuntu:trusty")
d14 = net.addDocker('d14', ip='12.0.0.14', dimage="ubuntu:trusty")
d15 = net.addDocker('d15', ip='12.0.0.15', dimage="ubuntu:trusty")
d16 = net.addDocker('d16', ip='13.0.0.11', dimage="ubuntu:trusty", defaultRoute = 'via 13.0.0.10')
d17 = net.addDocker('d17', ip='13.0.0.12', dimage="ubuntu:trusty")
d18 = net.addDocker('d18', ip='13.0.0.13', dimage="ubuntu:trusty")
d19 = net.addDocker('d19', ip='13.0.0.14', dimage="ubuntu:trusty")
d20 = net.addDocker('d20', ip='13.0.0.15', dimage="ubuntu:trusty")
'''
info('*** Adding switches\n')
s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')
s3 = net.addSwitch('s3')
s4 = net.addSwitch('s4')
info('*** Creating links\n')
net.addLink(d1, s1, delay='100ms')
'''
net.addLink(d2, s1, delay='100ms')
net.addLink(d3, s1, delay='100ms')
net.addLink(d4, s1, delay='100ms')
net.addLink(d5, s1, delay='100ms')
net.addLink(d6, s2, delay='100ms')
net.addLink(d7, s2, delay='100ms')
net.addLink(d8, s2, delay='100ms')
net.addLink(d9, s2, delay='100ms')
net.addLink(d10, s2, delay='100ms')
'''
net.addLink(d11, s3, delay='100ms')
'''
net.addLink(d12, s3, delay='100ms')
net.addLink(d13, s3, delay='100ms')
net.addLink(d14, s3, delay='100ms')
net.addLink(d15, s3, delay='100ms')
net.addLink(d16, s4, delay='100ms')
net.addLink(d17, s4, delay='100ms')
net.addLink(d18, s4, delay='100ms')
net.addLink(d19, s4, delay='100ms')
net.addLink(d20, s4, delay='100ms')
'''
#router
router = net.addDocker('r0', cls=LinuxRouter, ip='10.0.0.10/8')
net.addLink(s1, router, intfName2='r0-eth1', params2={'ip':'10.0.0.10/8'}, delay='10000ms', bw=1)
net.addLink(s2, router, intfName2='r0-eth2', params2={'ip':'11.0.0.10/8'}, delay='10000ms', bw=1)
net.addLink(s3, router, intfName2='r0-eth3', params2={'ip':'12.0.0.10/8'}, delay='10000ms', bw=1)
net.addLink(s4, router, intfName2='r0-eth4', params2={'ip':'13.0.0.10/8'}, delay='10000ms', bw=1)
#net.addLink(s2, s3, cls=TCLink, delay='100ms', bw=1)
#net.addLink(s3, s4, cls=TCLink, delay='100ms', bw=1)
#net.addLink(s4, s1, cls=TCLink, delay='100ms', bw=1)
#net.addLink(s2, d2)
info('*** Starting network\n')
net.start()
info('*** Testing connectivity\n')
net.ping([d1, d2, d3, d4, d5])
net.ping([d6, d7, d8, d9, d10])
net.ping([d11, d12, d13, d14, d15])
net.ping([d16, d17, d18, d19, d20])
net.ping([d1, d6, d11, d16])

info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()

