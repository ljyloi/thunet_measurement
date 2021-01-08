with open("scanlist", "r") as f:
    iplist = f.read().split("\n")[:-1]

outputlist = []
for ip in iplist:
    num = int(ip.split(".")[2])
    if (num & (128 + 64 + 32 + 16) == 0):
        outputlist.append(ip)

ipmap = {}
with open("mainiplist", "w") as f:
    for ip in outputlist:
        ipmap[ip] = 1
        f.write(ip + "\n")


filename = "mainiplist.xml"
with open(filename, "r") as f:
    strs = f.read()

# 存储 IP 节点的相关信息
class IpInfo():
    def __init__(self, seg):
        self.ip = seg[0]
        self.ports = port_p.findall(seg[1])
        self.routes = route_p.findall(seg[1])

    def output(self):
        print("IP: ", self.ip)
        print("PORTS: ")
        for port in self.ports:
            print(" ", port)
        print("ROUTES:")
        for route in self.routes:
            print(" ", route)


filename = "mainiplist.xml"
with open(filename, "r") as f:
    content = f.read()
# print(content)

import re

host_p = re.compile("(<host(?:.|\n)*?</host>)")
addr_p = re.compile("<address addr=\"([\d\.]+)\" ")
trace_p = re.compile("(<trace(?:.|\n)*?</trace>)")
ports_p = re.compile("(<ports(?:.|\n)*?</ports>)")
port_p = re.compile("<port protocol=\"(\w+)\" portid=\"(\d+)\"><state state=\"(\w+)\"")
hop_p = re.compile("<hop ttl=\"(\d*)\" ipaddr=\"([\d\.]+)\"")
hosts = host_p.findall(content)

hostlist = []

outputfile = open("wash.xml", "w")

for host in hosts:
    addr = addr_p.findall(host)[0]
    if (ipmap.get(addr, 0) != 0):
        outputfile.write(host+"\n")