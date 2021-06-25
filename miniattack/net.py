import sys
import os
import csv
from subprocess import Popen
from time import sleep
from mininet.log import setLogLevel, info
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from gui import gui
from topo import FatTree


class Net:
    def __init__(self, opt1='--flood', opt2='--udp'):
        self.idle_dur = 5
        self.attack_dur = 5
        self.tmp = 'tmp.txt'
        self.opt1 = opt1
        self.opt2 = opt2
        self.data = {}

    def run(self):
        self.remove_tmp()
        self.clean_net()
        self.start_net()
        self.start_monitor()
        sleep(self.idle_dur)
        self.start_attack()
        sleep(self.attack_dur)
        self.stop_attack()
        sleep(self.idle_dur)
        self.stop_monitor()
        self.fill_data()
        self.remove_tmp()
        self.stop_net()
        self.plot()

    def clean_net(self):
        info('*** Clean net\n')
        cmd = "mn -c"
        Popen(cmd, shell=True).wait()

    def start_net(self):
        self.net = Mininet(FatTree())
        self.net.start()
        for i in range(1, 11):
            s = self.net.get(f's{i}')
            s.cmd(f'ovs-vsctl set bridge s{i} stp-enable=true')
        print("Dumping host connections")
        dumpNodeConnections(self.net.hosts)
        print("Testing network connectivity")
        self.net.pingAll()
        self.net.pingAll()

    def stop_net(self):
        self.net.stop()

    def start_monitor(self):
        info('*** Start monitor\n')
        cmd = f"bwm-ng -o csv -T rate -C ',' > {self.tmp} &"
        Popen(cmd, shell=True).wait()

    def stop_monitor(self):
        info('*** Stop monitor\n')
        cmd = "killall -9 top bwm-ng"
        Popen(cmd, shell=True).wait()

    def start_attack(self):
        info('*** Start attack\n')
        h1 = self.net.get('h1')
        h5 = self.net.get('h5')
        ip2 = self.net.get('h2').IP()
        ip3 = self.net.get('h3').IP()
        ip7 = self.net.get('h7').IP()
        ip8 = self.net.get('h8').IP()
        h1.cmd(f"hping3 {self.opt1} {self.opt2} {ip2} &")
        h1.cmd(f"hping3 {self.opt1} {self.opt2} {ip3} &")
        h5.cmd(f"hping3 {self.opt1} {self.opt2} {ip7} &")
        h5.cmd(f"hping3 {self.opt1} {self.opt2} {ip8} &")

    def stop_attack(self):
        info('*** Stop attack\n')
        cmd = "killall -9 top hping3"
        Popen(cmd, shell=True).wait()

    def fill_data(self):
        with open('tmp.txt') as csvf:
            csvr = csv.reader(csvf, delimiter=',')
            for row in csvr:
                key = row[1]
                value = float(row[4]) * 8
                if key in self.data:
                    self.data[key].append(value)
                else:
                    self.data[key] = []

    def plot(self):
        info('*** Plot\n')
        gui(self.data)

    def remove_tmp(self):
        if os.path.exists(self.tmp):
            os.remove(self.tmp)

    def stop_all(self):
        try:
            self.stop_attack()
            self.stop_monitor()
            self.remove_tmp()
            self.stop_net()
        except Exception as e:
            pass


def main():
    setLogLevel('info')
    opt1 = sys.argv[1] if len(sys.argv) > 1 else '--flood'
    opt2 = sys.argv[2] if len(sys.argv) > 2 else '--udp'
    n = Net(opt1, opt2)
    try:
        n.run()
    except KeyboardInterrupt:
        n.stop_all()


if __name__ == '__main__':
    main()
