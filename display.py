import matplotlib.pyplot as plt
import networkx as nx
import sys

fa = {}
all_edges = []
def get_root(ip):
    s = ip
    while fa.get(ip, 0) != 0:
        ip = fa[ip]
    while fa.get(s, 0) != 0:
        b = fa.get(s, 0)
        fa[s] = ip
        s = b
    fa[ip] = 0
    return ip

for i in range(1, len(sys.argv)):
    filename = sys.argv[i]
    with open(filename + ".graph", "r") as f:
        s = f.readline()
        nodes_cnt = int(s.split(" ")[0])
        edges_cnt = int(s.split(" ")[1])
        print(nodes_cnt)
        print(edges_cnt)
        for i in range(0, nodes_cnt):
            s = f.readline()
            nodes = s.split(" ")[:-1]
            get_root(nodes[0])
            for j in range(1, len(nodes)):
                a = get_root(nodes[j])
                b = get_root(nodes[0])
                print(a, b)
                if (a != b):
                    fa[a] = b
        for i in range(0, edges_cnt):
            ab = f.readline().split(" ")[:-1]
            print(ab)
            a = ab[0]
            b = ab[1]
            all_edges.append((a, b))

cnt = 1
color = {}
groups = {}
roots = []
du = {}

for addr in fa:
    root = get_root(addr)
    du[root] = 0
    if (color.get(root, 0) == 0):
        # print(root)
        color[root] = cnt
        cnt += 1
        groups[root] = [root]
        roots.append(root)
        continue
    grouplist = groups.get(root)
    grouplist.append(addr)
 
print(roots)

nodes = roots
edges = {}
for edge in all_edges:
    a = get_root(edge[0])
    b = get_root(edge[1])
    if (a > b):
        du[a] = du[a] + 1
        du[b] = du[b] + 1
    else:
        du[a] = du[a] + 1
        du[b] = du[b] + 1

for edge in all_edges:
    a = get_root(edge[0])
    b = get_root(edge[1])
    if (du[a] == 1 or du[b] == 1): 
        continue
    if (a > b):
        edges[(a, b)] = 1
    else:
        edges[(b, a)] = 1

G=nx.Graph()

for node in nodes:
    if du[node] != 1:
        G.add_node(node)
r=G.add_edges_from(edges)
nx.draw(G, with_labels=True, font_size = 6,node_size=4, node_color='r', font_color='b')
plt.show()

