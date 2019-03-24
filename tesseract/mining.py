import copy

from tesseract import algorithms, canonical, graph


def forwards_explore(G, alg, c):
    if len(c) > alg.max:
        return
    else:
        V = set(graph.neighborhood(c, G))
        for v in V:
            if v not in c:
                cc = copy.deepcopy(c)
                cc.append(v)
                if canonical.canonical(cc, G):
                    if alg.filter(cc, G):
                        alg.process(cc, G)
                        forwards_explore(G, alg, cc)


def forwards_explore_all(G, f):
    for v in G.nodes:
        forwards_explore(G, f, [v])


def backwards_explore(G, alg, c):
    if len(c) > alg.max:
        return
    else:
        V = set(graph.neighborhood(c, G))
        for v in V:
            if v not in c:
                cc = copy.deepcopy(c)
                for i in range(0, len(cc) + 1):
                    ccc = cc[:i] + [v] + cc[i:]
                    if not graph.is_connected(ccc, G) or not canonical.canonical_r2(ccc, G):  # is_connected check has bad complexity here, do better!
                        continue
                    elif not canonical.canonical_r1(ccc):
                        if alg.filter(ccc, G):
                            backwards_explore(G, alg, ccc)
                    else:
                        if alg.filter(ccc, G):
                            alg.process(ccc, G)
                        backwards_explore(G, alg, ccc)


def backwards_explore_update(G, alg, edge):
    if len(edge) != 2:
        return
    GG = copy.deepcopy(G)
    GG.add_edge(edge[0], edge[1])
    backwards_explore(GG, alg, edge)
    backwards_explore(GG, alg, [edge[1], edge[0]])
