from netfilterqueue import NetfilterQueue
import scapy.all as scapy
from scapy.layers.inet import IP

count=0
def changeport(pkt):
    scapy_pkt=IP(pkt.get_payload())
    scapy_pkt.dport=30001
    del scapy_pkt[scapy.IP].chksum
    del scapy_pkt[scapy.UDP].chksum
    pkt.set_payload(bytes(scapy_pkt))
    return scapy_pkt

def print_and_accept(pkt):
    global count
    if count<=10:
        pkt.accept()
        count+=1
    if count>10:
        pktmod=changeport(pkt)
        print("source ip=",pktmod.src)
        print("dst ip=", pktmod.dst)
        print("source port=",pktmod.sport)
        print("dst port=", pktmod.dport)
        pkt.accept()

if __name__ == '__main__':
    nfqueue = NetfilterQueue()
    nfqueue.bind(1, print_and_accept)
    try:
        nfqueue.run()
    except KeyboardInterrupt:
        print('')
    nfqueue.unbind()