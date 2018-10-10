import networkx as nx
import numpy as np

graph = nx.Graph()
graph.add_node("v1")
graph.add_node("v2")
graph.add_edge("v1", "v2")
graph.node["v1"]["weight"] = 3.0
graph.node["v2"]["weight"] = 2.0
print(list(graph.nodes(data=True)))
print(list(graph.edges()))

# print(graph)
# for g in graph:
#     print(g, )
