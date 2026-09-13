from scapy.all import sniff, IP
import tkinter as tk
import threading

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

window = tk.Tk()
window.title("Packet Sniffer")
window.geometry("500x400")
window.configure(bg="#0f1a0f")

title_label = tk.Label(
    window,
    text="📡 Packet Sniffer",
    font=("Segoe UI", 16, "bold"),
    bg="#0f1a0f",
    fg="#00ff66"
)
title_label.pack(pady=15)

output_box = tk.Text(window, height=15, width=58, bg="#1a2e1a", fg="#66ff99", font=("Consolas", 9))
output_box.pack(pady=10)


def process_packet(packet):
    if packet.haslayer(IP):
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        protocol = packet[IP].proto

        line = f"Source: {src_ip} -> Destination: {dst_ip} | Protocol: {protocol}\n"
        output_box.insert(tk.END, line)

        if not is_trusted(src_ip) and not is_trusted(dst_ip):
            output_box.insert(tk.END, f"⚠ Unknown connection: {src_ip} <-> {dst_ip}\n")

        output_box.see(tk.END)


def start_sniffing():
    output_box.insert(tk.END, "Starting capture (10 packets)...\n")
    sniff_thread = threading.Thread(target=lambda: sniff(prn=process_packet, count=10))
    sniff_thread.start()


start_button = tk.Button(
    window,
    text="Start Capture",
    command=start_sniffing,
    bg="#00cc44",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    padx=15,
    pady=8
)
start_button.pack(pady=10)

window.mainloop()