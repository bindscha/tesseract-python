import argparse
import logging
import matplotlib.pyplot as plt
import networkx as nx
import os
from pymongo import MongoClient
from tqdm import tqdm
import random
from timeit import default_timer as timer

from tesseract import io, utils


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--graph', help='choice of graph', type=str)
    parser.add_argument('-c', '--connection', help='database connection', default='labostrex132.iccluster.epfl.ch:27017', type=str)
    parser.add_argument('-d', '--db', help='database', default='tesseract', type=str)
    parser.add_argument('--name', help='output name', type=str)
    parser.add_argument('-n', '--vertices', help='number of vertices', default=2**32, type=int)
    parser.add_argument('-s', '--start-vertex', help='start vertex', default=0, type=int)
    parser.add_argument('--drop-db', help='delete database if exists', action='store_true')
    parser.add_argument('-v', '--verbose', help='verbose', action='store_true')
    parser.set_defaults(verbose=False)
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-8s [%(name)s]  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S")

    LOG = logging.getLogger('MAIN')
    LOG_STATS = logging.getLogger('STAT')

    name = args.name if args.name is not None else os.path.basename(args.graph)

    min_vertex, max_vertex = args.start_vertex, args.start_vertex + args.vertices

    LOG.info('Loading graph \'%s\'...' % args.graph)
    start = timer()
    G = nx.DiGraph()  #nx.Graph()
    input_iter = io.read_xsc_graph(args.graph)
    for edge in tqdm(input_iter, unit=' edges'):
        [u, v] = edge
        src, dst = (u, v) if u < v else (v, u)
        if src != dst and min_vertex <= src < max_vertex:
            if not G.has_node(src):
                G.add_node(src)
            if not G.has_node(dst):
                G.add_node(dst)
            G.add_edge(src, dst)
    end = timer()

    LOG_STATS.info('Loaded graph in %0.4f seconds' % (end - start))
    LOG_STATS.info('Graph has %d vertices and %d edges' % (len(G.nodes), len(G.edges)))

    """
    plt.subplot(121)
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()
    """

    LOG.info('Writing graph \'%s\' to \'%s/%s\'...' % (name, args.connection, args.db))

    client = MongoClient(args.connection)
    db = client[args.db]
    collection = db[name]

    if args.drop_db:
        collection.drop()

    start = timer()
    last_vertex_to_write = min(max(G.nodes), max_vertex) if len(G.nodes) > 0 else max_vertex
    autots = utils.AutoTimestamp()
    for v in tqdm(range(min_vertex, last_vertex_to_write), unit=' vertices', total=last_vertex_to_write-min_vertex):
        if G.has_node(v) and len(G.adj[v]) > 0:
            adjacency_list = sorted(list(G.adj[v]))
            vertex = {'_id': str(v), 'neighbors': {str(i): {'ts': str(autots.timestamp())} for i in adjacency_list if i != v}}
            collection.insert_one(vertex)
    end = timer()

    LOG_STATS.info('Written graph in %0.4f seconds' % (end - start))

    LOG.info('Done!')
