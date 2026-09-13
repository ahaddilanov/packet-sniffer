# 📡 Packet Sniffer

A Python network monitoring tool that captures live packets moving through your local machine, parses their key details, and flags connections to unrecognized IP addresses using a trusted-IP whitelist — presented through a custom Tkinter GUI.

![Python](https://img.shields.io/badge/Python-3.14-blue) ![Scapy](https://img.shields.io/badge/Library-Scapy-green) ![License](https://img.shields.io/badge/License-MIT-lightgrey)

<p float="left">
  <img width="500" alt="Packet Sniffer GUI capturing live traffic and flagging an unknown connection" src="https://github.com/user-attachments/assets/9d2f71d3-1099-444a-8269-d0560e177dae" />
  <img width="500" alt="image" src="https://github.com/user-attachments/assets/296b8367-3eaa-46d0-ba99-9279dff8a802" />
</p>


---

## 📖 What It Does

Every time a device sends or receives data over a network, that data travels in small units called packets. This tool captures those packets as they pass through your own network interface and displays what's happening at a low level — the same fundamental technique tools like Wireshark are built on, simplified into something readable and self-built.

1. **Captures** live packets in real time using Scapy
2. **Parses** each packet's IP layer to extract the source address, destination address, and protocol
3. **Checks** both addresses against a local whitelist of trusted IPs
4. **Flags** any connection where neither the source nor destination is recognized
5. Presents everything through a live-updating **Tkinter GUI**, with capturing running in a background thread so the interface never freezes

---

## ⚙️ How It Works

**Packet layers:** network packets are structured in nested layers — Ethernet wraps IP, which wraps TCP/UDP, and so on. Scapy lets code check for and access each layer independently. This tool checks specifically for the IP layer (`packet.haslayer(IP)`) and reads its `src`, `dst`, and `proto` fields.

**Whitelist logic:** rather than trying to flag every single unfamiliar packet (which would create constant noise, since the internet involves millions of legitimate addresses), this tool only raises a warning when **both** the source and destination are unrecognized:

```python
if not is_trusted(src_ip) and not is_trusted(dst_ip):
    # flag as unknown connection
```

Most everyday traffic involves at least one recognizable endpoint (a home router, a known DNS server). Requiring both ends to be unfamiliar produces a stronger, more specific signal — though it's still a simplified model compared to production network monitoring tools, which maintain much larger and more dynamic allowlists.

**Threading:** Scapy's `sniff()` function normally blocks all other code while running, which would freeze the GUI entirely during a capture. Running it inside a separate thread (`threading.Thread`) lets the capture happen in the background while the interface stays responsive.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or later
- [Npcap](https://npcap.com/#download) — the underlying packet-capture driver required on Windows
- Scapy (`pip install scapy`)
- **Administrator/root privileges** — packet capturing requires elevated permissions. On Windows, this means running your terminal or IDE "as Administrator"; on macOS/Linux, running with `sudo`.

### Installation

```bash
git clone https://github.com/ahaddilanov/packet-sniffer.git
cd packet-sniffer
pip install scapy
```

### Running the App

Run PyCharm (or your terminal) as Administrator, then:

```bash
python packet_sniffer.py
```

Click **Start Capture** to begin. Captured packets and any unknown-connection warnings will appear live in the output window.

**Note:** edit the `trusted_ips` list near the top of the file to match your own network — check your router's actual address (via `ipconfig` on Windows) for accurate results.

---

## 🧠 Design Choices

- **Requiring both endpoints to be unrecognized before flagging:** an early design decision to reduce false positives. Checking only one side would either over-flag (if only the router is whitelisted) or under-flag (if too many external IPs are added).
- **Threading over blocking capture:** without this, clicking "Start Capture" would freeze the entire window until the capture finished — a poor experience for what's meant to be a live monitoring tool.
- **A small, honest whitelist rather than a fake "complete" one:** this project intentionally uses a short, editable list rather than pretending to ship with comprehensive threat intelligence. It's meant to demonstrate the *technique* of allowlisting, not to be a production-ready detection system.

---

## 📚 What I Learned

- How network packets are structured in layers, and how to access specific layers with Scapy
- The difference between blocking and threaded code execution, and why GUIs need non-blocking background work for long-running tasks
- Working with `threading.Thread` and `lambda` to run a function with pre-set arguments on a separate thread
- Why elevated/administrator permissions are required for low-level network operations, and the OS-level driver dependencies (Npcap) that sit underneath a Python networking library
- Designing detection logic around reducing noise (flagging only when both endpoints are unfamiliar) rather than flagging everything unfamiliar

---

## 🔮 Possible Future Improvements

- [ ] Resolve the numeric protocol value into a readable name (TCP/UDP/ICMP) instead of a raw number
- [ ] Persist flagged connections to a log file for later review
- [ ] Allow adding IPs to the whitelist directly from the GUI
- [ ] Support filtering captures by protocol or port
- [ ] Add a packet count / running statistics display

---

## 📄 License

MIT — free to use, modify, and learn from.

---

*Built as part of a personal cybersecurity portfolio project of mine
