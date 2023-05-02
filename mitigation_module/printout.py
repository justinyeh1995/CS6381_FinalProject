import scapy.all as scapy

# Open the pcap file
pcap = scapy.rdpcap('testfile.pcap')

# Loop through the packets and extract the source and destination IP addresses
for packet in pcap:
    if packet.haslayer(scapy.IP):
        src_ip = packet[scapy.IP].src
        dst_ip = packet[scapy.IP].dst
        print(f"Source IP: {src_ip}, Destination IP: {dst_ip}")


