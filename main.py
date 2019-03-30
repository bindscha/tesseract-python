import argparse
import logging
import matplotlib.pyplot as plt
import networkx as nx
import random
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

    file = open(args.file, 'w') if args.file is not None else None
    output = io.PatternOutput(file, args.canonical, args.sort, log_patterns=args.log_patterns)

    if args.algorithm == 'clique':
        alg = algorithms.CliqueFinding(output, args.max if args.max else None)
    elif args.algorithm == 'cycle':
        alg = algorithms.CycleFinding(output, args.max if args.max else None)
    elif args.algorithm.startswith('example'):
        alg = algorithms.ExampleTree(output, args.max if args.max else None)
    else:
        alg = algorithms.Algorithm(output, args.max if args.max else None)

    if args.mode == 'static' or args.mode == 'both':
        alg.reset_stats()
        LOG.info('Running forwards exploration with algorithm \'%s\'' % args.algorithm)
        start = timer()
        mining.forwards_explore_all(G, alg)
        end = timer()
        LOG_STATS.info('Ran forwards exploration in %0.4f seconds' % (end - start))
        LOG_STATS.info(' - Found %d matches' % alg.num_found)
        LOG_STATS.info(' - Executed %d filters' % alg.num_filters)

    if args.mode == 'dynamic' or args.mode == 'both':
        alg.reset_stats()
        if args.mode == 'dynamic':
            updates = list(map(lambda t: list(t), list(G.edges)[:args.updates] if args.updates else list(G.edges)))  # get list of list, not list of tuples
            if args.reset:
                G = nx.Graph()  # reset graph
        elif args.graph == 'example':
            updates = [[1, 3], [0, 1]]
        else:
            updates = []
            for _ in range(0, args.updates):
                valid = False
                while not valid:
                    edge = [random.randint(0, len(G.nodes)), random.randint(0, args.vertices)]
                    if edge[0] != edge[1] and not G.has_edge(edge[0], edge[1]) and edge not in updates:
                        valid = True
                        updates.append(edge)

        LOG.info('Running middle-out exploration with algorithm \'%s\' and %d updates' % (args.algorithm, len(updates)))

        start = timer()
        for i, update in enumerate(updates):
            if i < 1000 and i % 100 == 0 or i % 1000 == 0:
                LOG.info('Processed updates: %d / %d' % (i, len(updates)))
            LOG.debug('Processing update %s' % str(update))
            mining.middleout_explore_update(G, alg, update, add_to_graph=True)
            LOG_STATS.debug('Found %d matches' % alg.num_found)
            LOG_STATS.debug('Executed %d filters' % alg.num_filters)
        end = timer()
        LOG_STATS.info('Ran middle-out exploration in %0.4f seconds' % (end - start))
        LOG_STATS.info(' - Found %d matches' % alg.num_found)
        LOG_STATS.info(' - Executed %d filters' % alg.num_filters)

    if file is not None:
        file.close()
