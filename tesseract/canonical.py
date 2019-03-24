import networkx as nx


def canonical_r1(e):
    if e is None or not isinstance(e, list) or len(e) == 0:
        return False
    else:
        root = e[0]
        rest = e[1:]
        return all(map(lambda v: v > root, rest))


def canonical_r2(e, G):
    for i, u in enumerate(e):
        if i == 0:
            continue
        found_neighbor = False
        for v in e[:i]:
            if not found_neighbor and G.has_edge(v, u):
                found_neighbor = True
            elif found_neighbor and v > u:
                return False
    return True


def canonical(e, G):
    return canonical_r1(e) and canonical_r2(e, G)
