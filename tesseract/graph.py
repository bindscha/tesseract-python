import networkx as nx


def neighborhood(e, G):
    return list(map(lambda edge: edge[1], list(G.edges(e))))


def is_connected(e, G):
    for i, u in enumerate(e):
        if i == 0:
            continue
        for v in e[:i]:
            if not G.has_edge(v, u):
                return False
    return True
