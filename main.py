import matplotlib.pyplot as plt
import networkx as nx

from tesseract import algorithms, canonical, graph, mining

if __name__ == '__main__':
    G = nx.Graph()
    G.add_nodes_from(range(0,6))
    G.add_edges_from([(0, 3), (0, 4), (0, 5), (1, 2), (1, 4), (1, 5), (2, 5), (3, 4), (4, 5)])


    """
    plt.subplot(121)
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()
    """

    """    
    print(graph.is_connected([0, 1, 3], G))
    print(graph.is_connected([0, 2, 5], G))

    print(graph.neighborhood([1], G))
    print(graph.neighborhood([0, 5], G))
    """

    """
    e1 = [0, 3, 4, 1, 5]
    e2 = [3, 4, 0, 1, 5]
    e3 = [0, 4, 3, 1, 5]
    print(e1)
    print(canonical.canonical_r1(e1))
    print(canonical.canonical_r2(e1, G))
    print(e2)
    print(canonical.canonical_r1(e2))
    print(canonical.canonical_r2(e2, G))
    print(e3)
    print(canonical.canonical_r1(e3))
    print(canonical.canonical_r2(e3, G))
    """

    print('Forward exploration')
    #alg = algorithms.Algorithm()
    alg = algorithms.CliqueFinding()
    #alg = algorithms.ExampleTree()
    mining.forwards_explore_all(G, alg)

    print()

    print('Backwards exploration')
    mining.backwards_explore_update(G, alg, [1, 3])
