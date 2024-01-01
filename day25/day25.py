from collections import defaultdict
import numpy as np


def day25(filename):
    with open(filename, "r") as file:
        data = file.read()

    lines = data.split("\n")

    graph = defaultdict(set)
    for line in lines:
        line_split = line.split(" ")
        key = line_split[0][:-1]

        for i in range(1, len(line_split)):
            graph[key].add(line_split[i])
            graph[line_split[i]].add(key)

    nodes_to_idx = {key: idx for idx, key in enumerate(graph.keys())}
    idx_to_nodes = {idx: key for idx, key in enumerate(graph.keys())}

    num_nodes = len(graph)

    # from https://en.wikipedia.org/wiki/Algebraic_connectivity#Partitioning_a_graph_using_the_Fiedler_vector
    # partitions the graph into 2 sections, based off the connectivity of components

    # laplacian matrix = degree matrix - adjacency matrix
    laplacian_matrix = np.identity(num_nodes)
    for i in range(num_nodes):
        laplacian_matrix[i][i] = len(graph[idx_to_nodes[i]])

        for neighbor in graph[idx_to_nodes[i]]:
            laplacian_matrix[i][nodes_to_idx[neighbor]] = -1

    eigenvalues, eigenvectors = np.linalg.eig(laplacian_matrix)
    eigen_map = sorted(
        {eigenvalues[i]: eigenvectors[:, i] for i in range(len(eigenvalues))}.items(),
        key=lambda item: item[0],
    )

    # second smallest eigenvalue
    fielder_vector = eigen_map[1][1]

    # nodes are on a number line => all nodes that are positive are in one section, negatives in the other
    positive = len(list(filter(lambda x: x >= 0, fielder_vector)))
    negative = len(fielder_vector) - positive
    result1 = positive * negative
    print(f"result1: {result1}")


day25("sample.txt")
day25("input.txt")
