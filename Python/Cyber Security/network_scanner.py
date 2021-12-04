# !usr/bin/env python

import scapy.all as scapy


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    # arp_request.show()
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # broadcast.show()
    arp_request_broadcast = broadcast/arp_request
    # print(arp_request_broadcast.summary())
    # arp_request_broadcast.show()
    answered_list = scapy.srp(arp_request_broadcast, timeout=1)[0]
    # print(answered_list)

    for element in answered_list:
        print(element[1].psrc)
        print(element[1].hwsrc)
        print


scan("10.0.2.1/24")
