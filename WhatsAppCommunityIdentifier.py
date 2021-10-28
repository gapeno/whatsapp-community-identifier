"""
Authors: Gabriel Peres Nobre, Carlos Henrique Gomes Ferreira, Jussara Marques de Almeida
2021
"""

import csv
import networkx as nx
import itertools
from community import community_louvain

from BackboneExtractor import backbone_from_DisparityFilter

csv_file = 'whatsapp_messages.csv'

network_content = {}
full_networks = {}
backbones = {}
communities = {}

def csv_parser():
    with open(csv_file, newline='') as csvfile:
        whatsapp_messages = csv.reader(csvfile, delimiter=',')
        for row in whatsapp_messages:
            snap_id = row[1]
            if snap_id not in network_content:
                network_content[snap_id] = {}

            messageID = row[4]
            if messageID not in network_content[snap_id]:
                network_content[snap_id][messageID] = set()

            userID = row[3]
            network_content[snap_id][messageID].add(userID)


def network_generator():
    for snapshot in network_content:
        graph = nx.Graph()

        for messageID in network_content[snapshot]:
            for pair in itertools.combinations(network_content[snapshot][messageID], 2):
                if graph.has_edge(pair[0], pair[1]):
                    graph[pair[0]][pair[1]]['weight'] += 1
                else:
                    graph.add_edge(pair[0], pair[1], weight=1)

        full_networks[snapshot] = graph


def backbone_extractor():
    for snapshot in full_networks:
        confidence_value = 0.90
        backbones[snapshot] = backbone_from_DisparityFilter(full_networks[snapshot], confidence_value)


def community_identifier():
    for snapshot in backbones:
        communities[snapshot] = community_louvain.best_partition(backbones[snapshot], weight='weight', resolution=1)

def analysis():
    for snapshot in backbones:
        graph = backbones[snapshot]

        print("----------")
        print("Snapshot ID:", snapshot)
        print("Number of edges:", graph.number_of_edges())
        print("Number of nodes:", graph.number_of_nodes())
        print("Average degree:", "{:.2f}".format(sum([d for (n, d) in nx.degree(graph)]) / float(graph.number_of_nodes())))
        print("Average weigth:", "{:.2f}".format(sum(nx.get_edge_attributes(graph, 'weight').values()) / float(graph.number_of_edges())))
        print("Average clustering:", "{:.2f}".format(nx.average_clustering(graph)))
        print("Louvain communities:", len(set(communities[snapshot].values())))
        print("Louvain communities modularity:", "{:.2f}".format(community_louvain.modularity(communities[snapshot], graph, weight='weight')))


csv_parser()
network_generator()
backbone_extractor()
community_identifier()
analysis()