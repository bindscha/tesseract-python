import argparse
import matplotlib.pyplot as plt
import networkx as nx
import random
from timeit import default_timer as timer

from tesseract import algorithms, canonical, graph, mining

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--algorithm', help='algorithm to run', default='clique', type=str)
    parser.add_argument('-g', '--graph', help='choice of graph', default='er', type=str)
    parser.add_argument('-m', '--mode', help='mode to run (static, dynamic, both)', default='both', type=str)
    parser.add_argument('-p', '--plot', help='plot graph', default=True, type=bool)
    parser.add_argument('-v', '--vertices', help='number of vertices', default=1000, type=int)
    parser.add_argument('-e', '--edge_prob', help='probability of an edge', default=0.02, type=float)
    parser.add_argument('-u', '--updates', help='number of updates', default=200, type=int)
    args = parser.parse_args()

    start = timer()
    if args.graph == 'example':
        G = nx.Graph()
        G.add_nodes_from(range(0,6))
        G.add_edges_from([(0, 3), (0, 4), (0, 5), (1, 2), (1, 4), (1, 5), (2, 5), (3, 4), (4, 5)])
    else:
        G = nx.fast_gnp_random_graph(args.vertices, args.edge_prob)
    end = timer()
    print('[TIMING] Generated graph in %0.4f seconds' % (end - start))

    if args.plot:
        plt.subplot(121)
        nx.draw(G, with_labels=True, font_weight='bold')
        plt.show()

    if args.algorithm == 'clique':
        alg = algorithms.CliqueFinding()
    elif args.algorithm == 'example':
        alg = algorithms.ExampleTree()
    else:
        alg = algorithms.Algorithm()

    if args.mode == 'static' or args.mode == 'both':
        print('Running forwards exploration with algorithm \'%s\'' % args.algorithm)
        start = timer()
        mining.forwards_explore_all(G, alg)
        end = timer()
        print('[TIMING] Ran forwards exploration in %0.4f seconds' % (end - start))

    print()

    if args.mode == 'dynamic' or args.mode == 'both':
        updates = []
        for _ in range(0, args.updates):
            valid = False
            while not valid:
                edge = [random.randint(0, len(G.nodes)), random.randint(0, args.vertices)]
                if edge[0] != edge[1] and not G.has_edge(edge[0], edge[1]) and edge not in updates:
                    valid = True
                    updates.append(edge)

        print('Running backwards exploration with algorithm \'%s\' and %d updates' % (args.algorithm, args.updates))

        start = timer()
        for update in updates:
            mining.backwards_explore_update(G, alg, update)
        end = timer()
        print('[TIMING] Ran backwards exploration in %0.4f seconds' % (end - start))
