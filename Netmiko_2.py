from netmiko import ConnectHandler
import getpass
import json

passwd = getpass.getpass('Please enter the password: ')

# List of device IPs
ip_list = ["192.168.1.53", "192.168.1.52"]

# Create a list of dictionaries for each device
device_list = []

# Populate the device list with device details
for ip in ip_list:
        device = {
                "device_type": "cisco_ios",
                "host": ip,
                "username": "cisco",
                "password": passwd, # Log in password from getpass
                "secret": passwd # Enable password from getpass
        }
        device_list.append(device)
# Print human-readable device details using JSON formatting
json_formatted = json.dumps(device_list, indent=4)
print(json_formatted)

# Iterate over each device and connect to it
for each_device in device_list:
        connection = ConnectHandler(**each_device)
        connection.enable()
        print(f'Connecting to {each_device["host"]}')
        output = connection.send_command('show run | include hostname')
        print(output)
        print(f'Closing Connection on {each_device["host"]}')
        connection.disconnect()
