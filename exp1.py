#!/usr/bin/python3
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl -w net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl -w net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

class MyTopo(Topo):
    def build(self):
        # Routers
        r1 = self.addNode('r1', cls=LinuxRouter, ip='10.0.0.1/24')
        r2 = self.addNode('r2', cls=LinuxRouter, ip='10.0.1.2/24')  # doesn't matter, will override

        # Hosts
        h1 = self.addHost('h1', ip='10.0.0.3/24', defaultRoute='via 10.0.0.1')
        h2 = self.addHost('h2', ip='10.0.3.2/24', defaultRoute='via 10.0.3.4')
        h3 = self.addHost('h3', ip='10.0.2.2/24', defaultRoute='via 10.0.2.1')

        # Links
        self.addLink(h1, r1, intfName2='r1-eth0', params2={'ip': '10.0.0.1/24'})
        self.addLink(r1, r2,
                     intfName1='r1-eth1', params1={'ip': '10.0.1.1/24'},
                     intfName2='r2-eth0', params2={'ip': '10.0.1.2/24'})
        self.addLink(r2, h3, intfName1='r2-eth1', params1={'ip': '10.0.2.1/24'})
        self.addLink(r1, h2, intfName1='r1-eth2', params1={'ip': '10.0.3.4/24'})

if __name__ == '__main__':
    setLogLevel('info')
    topo = MyTopo()
    net = Mininet(topo=topo)
    net.start()

    r1 = net.get('r1')
    r2 = net.get('r2')

    # Force IP override in case Mininet ignores it
    r2.cmd('ifconfig r2-eth0 10.0.1.2/24')

    # Remove any bad default routes (sometimes get auto-added)
    r1.cmd('ip route del default || true')
    r2.cmd('ip route del default || true')

    # Add static routes
    r1.cmd('ip route add 10.0.2.0/24 via 10.0.1.2')
    r1.cmd('ip route add 10.0.3.0/24 dev r1-eth2')
    r2.cmd('ip route add 10.0.0.0/24 via 10.0.1.1')
    r2.cmd('ip route add 10.0.3.0/24 via 10.0.1.1')
    
    
    # Ping from inside Python using h1, h2, h3 directly
    h1 = net.get('h1')
    h2 = net.get('h2')
    h3 = net.get('h3')

    print("*** Ping: h1 -> h3")
    print(h1.cmd('ping -c 1 10.0.2.2'))

    print("*** Ping: h2 -> h3")
    print(h2.cmd('ping -c 1 10.0.2.2'))

    print("*** Ping: h3 -> h1")
    print(h3.cmd('ping -c 1 10.0.0.3'))
 
    print("*** Ping: h3 -> h2")
    print(h3.cmd('ping -c 1 10.0.3.2'))

    net.pingAll()

net.stop()


