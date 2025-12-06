"""
Async orchestration for blocking Netmiko calls using asyncio.to_thread.
This scales by running the blocking ConnectHandler in threadpool while keeping async orchestration.
"""
import asyncio
from datetime import datetime
import os
from netmiko import ConnectHandler

os.makedirs("backups_async", exist_ok=True)

devices = [
    {"device_type":"cisco_ios", "host":"192.0.2.1", "username":"admin","password":"password"},
    {"device_type":"cisco_ios", "host":"192.0.2.2", "username":"admin","password":"password"},
    # extend for 100s/1000s of devices (ensure infrastructure supports it)
]

async def backup_device(d):
    def blocking():
        net = ConnectHandler(**d)
        cfg = net.send_command("show running-config")
        net.disconnect()
        return cfg
    host = d["host"]
    try:
        cfg = await asyncio.to_thread(blocking)
        fname = f"backups_async/{host}_{datetime.now().strftime('%Y%m%d-%H%M')}.txt"
        with open(fname, "w") as f:
            f.write(cfg)
        return (host, True, fname)
    except Exception as e:
        return (host, False, str(e))

async def main():
    tasks = [backup_device(d) for d in devices]
    results = await asyncio.gather(*tasks)
    for host, ok, info in results:
        if ok:
            print(f"[OK] {host} -> {info}")
        else:
            print(f"[ERR] {host} -> {info}")

if __name__ == '__main__':
    asyncio.run(main())
