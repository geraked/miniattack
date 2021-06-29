import math
from mininet.topo import Topo


class FatTree(Topo):
    """Three-layer fat-tree with 2 pods"""

    def build(self, k=2):
        # Add nodes
        ss = {i: self.addSwitch(f's{i}') for i in range(1, 5*k+1)}
        hs = {i: self.addHost(f'h{i}') for i in range(1, 4*k+1)}

        # Add links of Edge layer
        for i in range(1, 4*k+1):
            j = int(math.ceil(i/2))
            self.addLink(hs[i], ss[j])

        # Add links of Aggregation layer
        for i in range(1, 2*k+1):
            j = i+4
            l = j+1 if i % 2 == 1 else j-1
            self.addLink(ss[i], ss[j])
            self.addLink(ss[i], ss[l])

        # Add links of Core layer
        for i in range(2*k+1, 4*k+1):
            self.addLink(ss[i], ss[5*k-1])
            self.addLink(ss[i], ss[5*k])
