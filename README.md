# Network-migration
Network migration program in netfilterqueue framework for UDP and TCP, including server1, server2, gate and client. ( server1, server2 and client are socket programs in UDP or TCP)

udpgate.py for UDP migration, which can redirect UDP network traffic which is orginally sent from client to server1 to server2 after 10 packets have been sent (gate and two servers are all on the same virtual machine VM1 using ubuntu, client is on the VM2).
 
tcpgate.py for TCP migration,  which can redirect TCP network traffic which is orginally sent from client to server1 to server2, DST_SERVER and DST_PORT are the ip address and port of server2( gate and server1 are on the VM1, server2 is on the VM2, and client is on the VM3).

For TCP migration, iptables is needed to be used on the VM1 including gate and server1 to let nfqueue catch the pkts sent to and from the server1, iptables commands are:

1.iptables -A INPUT -p tcp --dport 30000 -j NFQUEUE --queue-num 1

2.iptables -A OUTPUT -p tcp --sport 30000 -j NFQUEUE --queue-num 1

3.iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP

For UDP migration,iptables is needed to be used on the VM1 to let nfqueue catch the pkts sent to server1, iptables command is :
iptables -A INPUT -p udp --dport 30000 -j NFQUEUE --queue-num 1
