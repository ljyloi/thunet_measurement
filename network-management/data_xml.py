import re
import sys
import networkx as nx
# ------------------------------------------
#  xml 解析
# ------------------------------------------

class HostInfo():
    def __init__(self, addr, routes, ports):
        self.addr = addr
        self.routes = routes
        self.ports = ports
        self.hops = routes[-1][0]

    def output(self):
        print("ADDR: ", self.addr)
        print("PORTS: ")
        for port in self.ports:
            print(" ", port)
        print("ROUTES:")
        for route in self.routes:
            print(" ", route)
        print("HOPS:")
        print(self.hops)

filename = sys.argv[1]
with open(filename + ".xml", "r") as f:
    content = f.read()
# print(content)


host_p = re.compile("(<host(?:.|\n)*?</host>)")
addr_p = re.compile("<address addr=\"([\d\.]+)\" ")
trace_p = re.compile("(<trace(?:.|\n)*?</trace>)")
ports_p = re.compile("(<ports(?:.|\n)*?</ports>)")
port_p = re.compile("<port protocol=\"(\w+)\" portid=\"(\d+)\"><state state=\"(\w+)\"")
hop_p = re.compile("<hop ttl=\"(\d*)\" ipaddr=\"([\d\.]+)\"")
hosts = host_p.findall(content)

hostlist = []

for host in hosts:
    addr = addr_p.findall(host)[0]
    trace = trace_p.findall(host)
    hops = hop_p.findall(trace[0])
    port_seg = ports_p.findall(host)
    ports = port_p.findall(port_seg[0])
    hostlist.append(HostInfo(addr, hops, ports))


# ------------------------------------------
#  拓扑
# ------------------------------------------

hostdis = {}
for i in range(0, len(hostlist)):
    hostdis[hostlist[i].addr] = int(hostlist[i].hops)

def get_peer(ip):
    segs = ip.split(".")
    num = int(segs[-1])
    a = num - 1
    b = num + 1
    segs[-1] = str(a)
    str_a = ".".join(segs)
    segs[-1] = str(b)
    str_b = ".".join(segs)

    if (hostdis.get(str_a, 0) == hostdis.get(ip, 0) - 1):
        return str_a
    if (hostdis.get(str_b, 0) == hostdis.get(ip, 0) - 1):
        return str_b

    return ""

fa = {}

for host in hostlist:
    for route in host.routes:
        fa[route[1]] = 0

def get_root(ip):
    s = ip
    while fa.get(ip, 0) != 0:
        ip = fa[ip]
    while fa.get(s, 0) != 0:
        b = fa.get(s, 0)
        fa[s] = ip
        s = b
    return ip


for i in range(0, len(hostlist)):
    nowhost = hostlist[i]
    for j in range(0, len(nowhost.routes) - 1):
        if (int(nowhost.routes[j][0]) + 1 == int(nowhost.routes[j + 1][0])):
            peer = get_peer(nowhost.routes[j + 1][1])
            if peer != "":
                a = get_root(peer)
                b = get_root(nowhost.routes[j][1])
                if (a != b):
                   fa[a] = b


cnt = 1
color = {}
groups = {}
roots = []
for addr in fa:
    root = get_root(addr)
    if (color.get(root, 0) == 0):
        # print(root)
        color[root] = cnt
        cnt += 1
        groups[root] = [root]
        roots.append(root)
        continue
    grouplist = groups.get(root, [])
    grouplist.append(addr)

for root in roots:
    print(root, ":")
    print(" ", groups.get(root, []))
    
import matplotlib.pyplot as plt
 
G=nx.Graph()

edges = {}
nodes = {}
for i in range(0, len(hostlist)):
    nowhost = hostlist[i]
    for j in range(0, len(nowhost.routes) - 1):
        if (int(nowhost.routes[j][0]) + 1 == int(nowhost.routes[j + 1][0])):
            a = get_root(nowhost.routes[j][1])
            b = get_root(nowhost.routes[j + 1][1])
            if (a > b):
                edges[(a, b)] = 1
            else:
                edges[(b, a)] = 1
            nodes[a] = 1
            nodes[b] = 1

for node in nodes:
    G.add_node(node)

outputfile = open(filename + ".graph", "w")


outputfile.write("{} {}\n".format(len(nodes), len(edges)))
for node in nodes:
    for gnode in groups[node]:
        outputfile.write(gnode+" ")
    outputfile.write("\n")

for edge in edges:
    outputfile.write(edge[0]+" "+ edge[1] + " \n")
r=G.add_edges_from(edges)
nx.draw(G, with_labels=True, font_size = 4,node_size=4, node_color='r',)
plt.show()