# Hemlock ARP Spoofer

A modern GUI-based ARP poisoning tool for ethical network security testing, featuring intuitive controls and visual feedback.

## Features

- **ARP Cache Poisoning** - Execute man-in-the-middle attacks between router and target
- **Customizable Timing** - Adjust spoofing interval (1-30 seconds)
- **Input Validation** - Strict input validation
- **Visual Indicators** - Color-coded status (🟢/🔴)
- **Automatic iptables** - Handles FORWARD policy during operation

## Requirements

- Python 3.8+
- Linux system
- Root privileges
- Required packages:
```bash
pip install customtkinter scapy CTkMessagebox
```
## Usage
1. Run with root privileges:

```bash
sudo python3 hemlock.py
```
2. Enter your MAC address when prompted (format: FF:FF:FF:FF:FF:FF)

3. Specify target IPs and spoofing interval

4. Toggle the switch to start/stop poisoning

<p align="center">
  <img width="441" height="462" alt="Hemlock Interface" src="https://github.com/user-attachments/assets/d59b4542-fe9d-490e-b54f-28ce3efcc96d">
</p>
