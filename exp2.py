#!/usr/bin/python3
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info

class Exp2Topo(Topo):
    def build(self):
        # Hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')

        # Switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # Topology
        self.addLink(h1, s1)  # s1-eth1
        self.addLink(h2, s1)  # s1-eth2
        self.addLink(s1, s2)  # s1-eth3 <-> s2-eth1
        self.addLink(s2, h3)  # s2-eth2 <-> h3-eth0

if __name__ == '__main__':
    setLogLevel('info')
    topo = Exp2Topo()
    net = Mininet(topo=topo, switch=OVSKernelSwitch, controller=None)
    net.start()

    # Assign static IPs
    info("*** Assigning IPs...\n")
    h1 = net.get('h1')
    h2 = net.get('h2')
    h3 = net.get('h3')
    
    h1.setIP('10.0.0.1/24')
    h2.setIP('10.0.0.2/24')
    h3.setIP('10.0.0.3/24')
    
    

    CLI(net)
    net.stop()
	
