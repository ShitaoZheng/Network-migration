# Network-migration
Network migration program in netfilterqueue framework for UDP and TCP, including server1, server2, gate and client
udpgate.py for UDP migration, which can redirect UDP network traffic which is orginally sent from client to server1 to server2 after 10 packets have been sent. (gate and two servers are all on the same virtual machine using ubuntu, client is on the other VM)
tcpgate.py for TCP migration,  which can redirect TCP network traffic which is orginally sent from client to server1 to server2, DST_SERVER and DST_PORT are the ip address and port of server2. ( gate and server1 are on the same first VM, server2 is on the second VM, and client is on the third VM.)
