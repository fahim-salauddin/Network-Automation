from netmiko import ConnectHandler
# Define device details for Cisco devices
devices = [
{
'device_type': 'cisco_ios',
'ip': '192.168.1.62',
'username': 'cisco',
'password': 'cisco',
#'secret': 'cisco123',
},
{
'device_type': 'cisco_ios',
'ip': '192.168.1.63',
'username': 'cisco',
'password': 'cisco',
#'secret': 'cisco123',
},
]
# Iterate through a list of device dictionaries
for device in devices:
print(f"Connecting to {device['ip']}...")
net_connect = ConnectHandler(**device)
net_connect.enable()
# Configure the device
config_commands = ['run show interface description']
net_connect.send_config_set(config_commands)
net_connect.save_config()
# Display the updated configuration
output = net_connect.send_command('show running-config | section username')
print(output)
print(f'Closing Connection on {device["ip"]}')
net_connect.disconnect()
