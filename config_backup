from datetime import datetime
from netmiko import ConnectHandler
import os

devices = [
    {"device_type": "cisco_ios", "host": "192.168.1.51", "username": "cisco", "password": "cisco"},
    {"device_type": "cisco_ios", "host": "192.168.1.52", "username": "cisco", "password": "cisco"},
    {"device_type": "cisco_ios", "host": "192.168.1.53", "username": "cisco", "password": "cisco"},
    {"device_type": "cisco_ios", "host": "192.168.1.62", "username": "cisco", "password": "cisco"},
    {"device_type": "cisco_ios", "host": "192.168.1.63", "username": "cisco", "password": "cisco"},
]

backup_dir = "backups"
os.makedirs(backup_dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

for dev in devices:
    with ConnectHandler(**dev) as conn:
        hostname = conn.find_prompt().strip("#>")
        print(f"Backing up {hostname} ({dev['host']})")

        running_config = conn.send_command("show running-config")
        filename = f"{backup_dir}/{hostname}_{dev['host']}_{timestamp}.cfg"
        with open(filename, "w") as f:
            f.write(running_config)

        print(f"Saved to {filename}")
