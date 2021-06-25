import math
from mininet.topo import Topo

class FatTree(Topo):
    def build(self, h=8, s=10):
        ss = {i: self.addSwitch(f's{i}') for i in range(1, s+1)}
        hs = {i: self.addHost(f'h{i}') for i in range(1, h+1)}

        for i in range(1, 9):
            j = int(math.ceil(i/2))
            self.addLink(hs[i], ss[j])

        for i in range(1, 5):
            j = i+4
            k = j+1 if i % 2 == 1 else j-1
            self.addLink(ss[i], ss[j])
            self.addLink(ss[i], ss[k])

        for i in range(5, 9):
            self.addLink(ss[i], ss[9])
            self.addLink(ss[i], ss[10])