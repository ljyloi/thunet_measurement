import sys
import os



with open("namelist", "r") as f:
    namelist = f.read().split("\n")[:-1]

with open("networklist", "r") as f:
    networklist = f.read().split("\n")[:-1]

with open("portlist", "r") as f:
    portlist = f.read().split("\n")[:-1]

ip_map = {}

for name in namelist:
    for network in networklist:
        for port in portlist:
            with open("data/" + name + "/" + network + "/" + port, "r") as f:
                ip_list = f.read().split("\n")[:-1]
                for ip in ip_list:
                    ip_map[ip] = 1

with open("iplist", "w") as f:
    for ip in ip_map:
        f.write(ip + "\n")

print(len(ip_map))
