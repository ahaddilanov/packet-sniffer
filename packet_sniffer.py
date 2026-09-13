from scapy.all import sniff, IP

trusted_ips = [
    "192.168.1.1",
    "8.8.8.8",
    "1.1.1.1"
]

def is_trusted(ip):
    return ip in trusted_ips

print(is_trusted("192.168.1.1"))
print(is_trusted("45.33.32.156"))

def process_packet(packet):
    if packet.haslayer(IP):
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        protocol = packet[IP].proto

        print(f"Source: {src_ip} -> Destination: {dst_ip} | Protocol: {protocol}")

sniff(prn=process_packet, count=10)

