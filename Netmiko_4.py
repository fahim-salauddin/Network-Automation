from netmiko import ConnectHandler
from getpass import getpass

cisco1 =[ {
    "device_type": "cisco_ios",
    "host": "ESW2",
    "username": "cisco",
    "password": "cisco",
},
{
    "device_type": "cisco_ios",
    "host": "ESW3",
    "username": "cisco",
    "password": "cisco",
}
]

# Show command that we execute.
command = "show ip int brief"

with ConnectHandler(**cisco1) as net_connect:
    output = net_connect.send_command(command)

# Automatically cleans-up the output so that only the show output is returned
print()
print(output)
print()
