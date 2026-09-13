from scapy.all import sniff, IP

trusted_ips = [
    "192.168.1.1",
    "8.8.8.8",
    "1.1.1.1"
]

def is_trusted(ip):
    return ip in trusted_ips

def process_packet(packet):
    if packet.haslayer(IP):
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        protocol = packet[IP].proto

        print(f"Source: {src_ip} -> Destination: {dst_ip} | Protocol: {protocol}")

        if not is_trusted(src_ip) and not is_trusted(dst_ip):
            print(f"⚠ Unknown connection detected: {src_ip} <-> {dst_ip}")

sniff(prn=process_packet, count=10)