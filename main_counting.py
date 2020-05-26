import argparse
import logging
import matplotlib.pyplot as plt
import networkx as nx
import random
from tqdm import tqdm
from timeit import default_timer as timer

from tesseract import algorithms, canonical, graph, io, mining

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--algorithm', help='algorithm to run', default='clique', type=str)
    parser.add_argument('-g', '--graph', help='choice of graph', default='er', type=str)
    parser.add_argument('-m', '--mode', help='mode to run (static, dynamic, both)', default='both', type=str)
    parser.add_argument('-p', '--plot', help='plot graph', action='store_true')
    parser.set_defaults(plot=False)
    parser.add_argument('-n', '--vertices', help='number of vertices', default=1000, type=int)
    parser.add_argument('-e', '--edge_prob', help='probability of an edge', default=0.02, type=float)
    parser.add_argument('-u', '--updates', help='number of updates', type=int)
    parser.add_argument('-c', '--percent', help='percentage', type=float)
    parser.add_argument('-d', '--depth', help='max depth', type=int)
    parser.add_argument('--max', help='maximum pattern size', type=int)
    parser.add_argument('--seed', help='random graph generator seed', default=42, type=int)
    parser.add_argument('-f', '--file', help='output file for patterns', default=None, type=str)
    parser.add_argument('--log_patterns', help='log found patterns', action='store_true')
    parser.set_defaults(log_patterns=False)
    parser.add_argument('--canonical', help='canonicalize patterns à la Arabesque before outputting', action='store_true')
    parser.set_defaults(canonical=False)
    parser.add_argument('--sort', help='sort patterns before outputting', action='store_true')
    parser.set_defaults(sort=False)
    parser.add_argument('-r', '--reset', help='reset graph', action='store_true')
    parser.set_defaults(reset=False)
    parser.add_argument('-v', '--verbose', help='verbose', action='store_true')
    parser.set_defaults(verbose=False)
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-8s [%(name)s]  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S")

    LOG = logging.getLogger('MAIN')
    LOG_STATS = logging.getLogger('STAT')

    LOG.info('Loading graph \'%s\'...' % args.graph)
    start = timer()
    if args.graph == 'example1':
        G = nx.Graph()
        G.add_nodes_from(range(0, 6))
        G.add_edges_from([(0, 3), (0, 4), (0, 5), (1, 2), (1, 4), (1, 5), (2, 5), (3, 4)])
    elif args.graph == 'example2':
        G = nx.Graph()
        G.add_nodes_from(range(0, 5))
        G.add_edges_from([(0, 3), (2, 1), (2, 4), (3, 2)])
    elif '.xsc' in args.graph:
        G = nx.Graph()
        input_iter = io.read_xsc_graph(args.graph)
        for edge in input_iter:
            [u, v] = edge
            if not G.has_node(u):
                G.add_node(u)
            if not G.has_node(v):
                G.add_node(v)
            G.add_edge(u, v)
    else:
        G = nx.fast_gnp_random_graph(args.vertices, args.edge_prob, args.seed)
    end = timer()
    LOG_STATS.info('Read/generated graph in %0.4f seconds' % (end - start))
    LOG_STATS.info('Graph has %d vertices and %d edges' % (len(G.nodes), len(G.edges)))

    if args.plot:
        plt.subplot(121)
        nx.draw(G, with_labels=True, font_weight='bold')
        plt.show()

    neighborhoods = set()
    for edge in tqdm(G.edges, unit=' edges', total=len(G.edges)):
        u, v = edge
        if random.randint(0,999999) % 1000000 < args.percent * 10000:
            tree = nx.bfs_tree(G, source=u, depth_limit=args.depth)
            for x in tree:
                neighborhoods.add(x)
            tree = nx.bfs_tree(G, source=v, depth_limit=args.depth)
            for x in tree:
                neighborhoods.add(x)


    LOG_STATS.info('Neighborhoods have %d vertices, i.e., %0.4f%% of the graph' % (len(neighborhoods), (float(len(neighborhoods)) / len(G.nodes)) * 100))