
from netfilterqueue import NetfilterQueue
from scapy.all import *
from scapy.layers.inet import IP,TCP
from scapy.fields import *


class TCPSession:
    def __init__(self):
        # shakehand 1 state
        self.state = 'sk1'

#dest server
DST_SERVER = '192.168.1.103'
#dest port
DST_PORT = 30001
#client -> server1 session

#netfilterqueue callback
def print_and_accept(pkt):
    global dst_sport,dst_seq,dst_ack,tcpsession
    ip = IP(pkt.get_payload())
    tcp = ip.getlayer(TCP)
    # handshake 1
    if tcp.flags == 'S':
        tcpsession = TCPSession()
        tcpsession.src = ip.src
        tcpsession.dst = ip.dst
        tcpsession.sport = tcp.sport
        tcpsession.dport = tcp.dport
        pkt.accept()
    # handshake 2
    if tcp.flags == 'SA':
        if tcpsession.state == 'sk1':
            tcpsession.state = 'sk2'
        pkt.accept()
    elif 'A' in tcp.flags:
        if tcpsession.state == 'sk2':
            tcpsession.state = 'sk3'
            pkt.accept()
        #start send/revice message
        elif tcpsession.state == 'sk3' and ip.dst == tcpsession.dst:
            # shakehand to server2 for 3 times
            ans = sr1(IP(dst=DST_SERVER) / TCP(dport=DST_PORT, sport=RandShort(), seq=RandInt(), flags='S'),verbose=False)
            dst_sport = ans[TCP].dport
            dst_seq = ans[TCP].ack
            dst_ack = ans[TCP].seq + 1
            send(IP(dst=DST_SERVER) / TCP(dport=DST_PORT, sport=dst_sport, ack=dst_ack, seq=dst_seq, flags='A'),verbose=False)
            tcpsession.state = 'skdone'
            #send first pkg to server2
            tcp_payload = tcp.getlayer(Raw)
            ans = sr1(IP(dst=DST_SERVER) / TCP(dport=DST_PORT, sport=dst_sport, ack=dst_ack, seq=dst_seq, flags='A') / tcp_payload,verbose=False)
            data_len = ans[TCP].ack - dst_seq
            dst_seq = ans[TCP].ack
            dst_ack  = ans[TCP].seq
            #send first ack to client
            send(IP(dst=ip.src) / TCP(dport=tcp.sport, sport=tcp.dport, ack=tcp.seq + data_len, seq=tcp.ack,flags='A'),verbose=False)
            pkt.drop()
        elif tcpsession.state == 'skdone':
            #client -> server
            if ip.dst == tcpsession.dst and tcp.haslayer(Raw):
                tcp_payload = tcp.getlayer(Raw)
                ans = sr1(IP(dst=DST_SERVER) / TCP(dport=DST_PORT, sport=dst_sport, ack=dst_ack, seq=dst_seq,flags='A') / tcp_payload, verbose=False)
                data_len = ans[TCP].ack - dst_seq
                dst_seq = ans[TCP].ack
                dst_ack = ans[TCP].seq
                # send first ack to client
                send(IP(dst=ip.src) / TCP(dport=tcp.sport, sport=tcp.dport, ack=tcp.seq + data_len, seq=tcp.ack,flags='A'), verbose=False)
                pkt.drop()

if __name__ == '__main__':
    nfqueue = NetfilterQueue()
    nfqueue.bind(1, print_and_accept)
    try:
        nfqueue.run()
    except KeyboardInterrupt as e:
        print(e)