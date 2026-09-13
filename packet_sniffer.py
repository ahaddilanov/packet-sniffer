from scapy.all import sniff, IP

def process_packet(packet):
    if packet.haslayer(IP):
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        protocol = packet[IP].proto

        print(f"Source: {src_ip} -> Destination: {dst_ip} | Protocol: {protocol}")

sniff(prn=process_packet, count=10)