#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from basic_analysis import get_data
import networkx as nx # graphs
import matplotlib.pyplot as plt


df = get_data()
a = [item for sublist in df['AutořiAV'].values for item in sublist]
a = list(set(a))
no_unique_authors = len(a)

adj_matrix = np.zeros((no_unique_authors, no_unique_authors))


for paper_auth in df['AutořiAV']:
    # cross authors
    if len(paper_auth) > 1:
        for a1 in range(len(paper_auth)):
            for a2 in range(a1+1, len(paper_auth)):
                # increment both to obtain symmetric matrix
                adj_matrix[a.index(paper_auth[a1]), a.index(paper_auth[a2])] += 1
                adj_matrix[a.index(paper_auth[a2]), a.index(paper_auth[a1])] += 1
    # self loops
    elif len(paper_auth) == 1:
        adj_matrix[a.index(paper_auth[0]), a.index(paper_auth[0])] += 1

g = nx.Graph(adj_matrix)
# set names to nodes
nx.set_node_attributes(g, 'author', dict((idx, name.decode('utf-8')) for (idx, name) in zip(range(len(a)), a)))
degree_dist_bin = g.degree()
degree_dist_wei = g.degree(weight = 'weight')
to_remove = [n for n in degree_dist_wei if degree_dist_wei[n] <= 1.]
g.remove_nodes_from(to_remove)

# export to gephi - uncomment if needed
# nx.write_gexf(g, 'UI-cit-network-self-loops.gexf')

# graph stats
degree_dist_bin = g.degree()
degree_dist_wei = g.degree(weight = 'weight')
print "nodes: ", nx.number_of_nodes(g)
print "edges: ", g.number_of_edges()
print "density: ", nx.density(g)*100
print "bin. degree: ", np.mean(degree_dist_bin.values())
print "wei. degree: ", np.mean(degree_dist_wei.values())
print "# connected components: ", nx.number_connected_components(g) # 25 gephi
print "# triangles: ", np.sum(nx.triangles(g).values())//3 # 1643
print "avg. clustering: ", nx.average_clustering(g)
Gc = max(nx.connected_component_subgraphs(g), key=len)
print "char. path length [of largest connected component]: ", nx.average_shortest_path_length(Gc)
