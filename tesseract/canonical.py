import networkx as nx

from tesseract import graph


def canonical_r1_all(e):
    if e is None or not isinstance(e, list) or len(e) == 0:
        return False
    else:
        root = e[0]
        rest = e[1:]
        return all(map(lambda v: v > root, rest))


def canonical_r2_all(e, G):
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


def canonical_all(e, G):
    return canonical_r1_all(e) and canonical_r2_all(e, G)


def canonical_r1(e, v):
    return e[0] < v


def canonical_r2(e, v, G, ignore=[]):
    found_neighbor = False
    for u in e:
        if not found_neighbor and G.has_edge(u, v):
            found_neighbor = True
        elif found_neighbor and u not in ignore and u > v:
            return False
    return True


def canonical(e, v, G, ignore=[]):
    return canonical_r1(e, v) and canonical_r2(e, v, G, ignore=ignore)


def canonicalize(e, G):
    if len(e) <= 1:
        return e
    else:
        e = sorted(e)
        e_c = [e[0]]
        e = e[1:]

        while len(e) > 0:
            V = graph.neighborhood(e_c, G)
            for i, u in enumerate(e):
                if u in V:
                    e_c.append(u)
                    e.pop(i)
                    break

        return e_c
