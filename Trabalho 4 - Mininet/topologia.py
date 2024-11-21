from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.cli import CLI
from mininet.link import TCLink

class Topologia(Topo):
    def build(self):
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')
        s6 = self.addSwitch('s6')
        s7 = self.addSwitch('s7')

        h1 = self.addHost('h1', mac='00:00:00:00:00:01')
        h2 = self.addHost('h2', mac='00:00:00:00:00:02')
        h3 = self.addHost('h3', mac='00:00:00:00:00:03')
        h4 = self.addHost('h4', mac='00:00:00:00:00:04')
        h5 = self.addHost('h5', mac='00:00:00:00:00:05')
        h6 = self.addHost('h6', mac='00:00:00:00:00:06')
        h7 = self.addHost('h7', mac='00:00:00:00:00:07')

        self.addLink(s1, s2)
        self.addLink(s2, h1)
        self.addLink(s2, s3)
        self.addLink(s3, s7)
        self.addLink(s3, h6)
        self.addLink(s4, h5)
        self.addLink(s4, s5)
        self.addLink(s5, h4)
        self.addLink(s5, s6)
        self.addLink(s6, h2)
        self.addLink(s6, h3)

def run():
    topo = Topologia()
    net = Mininet(topo=topo, controller=Controller, switch=OVSSwitch, link=TCLink)

    c0 = net.addController('c0', controller=Controller)

    net.start()

    CLI(net)
    
    net.stop()

if __name__ == '__main__':
    run()
