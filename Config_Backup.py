"""
Multi-device backup (threaded) using ThreadPoolExecutor to scale.
"""
from netmiko import ConnectHandler
from datetime import datetime
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

os.makedirs("backups", exist_ok=True)

devices = [
    {"device_type": "cisco_ios", "host": "192.168.1.52", "username": "cisco", "password": "cisco"},
    {"device_type": "cisco_ios", "host": "192.168.1.53", "username": "cisco", "password": "cisco"},
]

def backup_device(d):
    host = d["host"]
    try:
        net = ConnectHandler(**d)
        cfg = net.send_command("show running-config")
        timestamp = datetime.now().strftime("%Y%m%d-%H%M")
        fname = f"backups/{host}_backup_{timestamp}.txt"
        with open(fname, "w") as f:
            f.write(cfg)
        net.disconnect()
        return (host, True, fname)
    except Exception as e:
        return (host, False, str(e))

with ThreadPoolExecutor(max_workers=10) as ex:
    futures = [ex.submit(backup_device, d) for d in devices]
    for fut in as_completed(futures):
        host, ok, info = fut.result()
        if ok:
            print(f"[OK] {host} -> {info}")
        else:
            print(f"[ERR] {host} -> {info}")
