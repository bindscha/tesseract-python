import networkx as nx


def neighborhood(e, G):
    return {edge[1] for edge in G.edges(e)}


def is_connected(v, e, G):
    for i, u in enumerate(e):
        if i == 0:
            continue
        found = False
        for v in e[:i]:
            if G.has_edge(v, u):
                found = True
                break
        if not found:
            return False
    return True


def is_connected_fast(v, e, G):
    for i, u in enumerate(e):
        if u != v and G.has_edge(u, v):
            return True
    return False
