from scapy.all import *

def packet_callback(packet):
    if packet.haslayer(IP):
        print(f"Source IP: {packet[IP].src}  Destination IP: {packet[IP].dst}")

sniff(prn=packet_callback, filter="tcp", iface="ens3")
#sniff(prn=packet_callback, filter="ip", iface="ens3")
#sniff(prn=packet_callback, filter="icmp", iface="ens3")
