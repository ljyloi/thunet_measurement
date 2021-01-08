import re
import sys

# ------------------------------------------------------
# 预处理
# ------------------------------------------------------

filename = sys.argv[1]
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

segment_p = re.compile("Nmap scan report for ([\d.]*)((?:.|\n)*?)\n\n(?!TRACEROUTE)")
port_p = re.compile("(\d+)/([a-z]+) +(open|filtered) +(.*)")
route_p = re.compile("(\d+) +[\w\.]+ ms +([\d\.]*)")
result = segment_p.findall(strs)
iplist = []
ipmap ={}

for seg in result:
    ipinfo = IpInfo(seg)
    iplist.append(ipinfo)
    ipmap[ipinfo.ip] = 1
    # ipinfo.output()
    
# ------------------------------------------------------
# 路径合并
# ------------------------------------------------------

with open("scanlist", "w") as f:
    for k in ipmap:
        f.write(k + "\n")

for one in iplist:
    for i in range(0, len(one.routes) - 2):
        break
