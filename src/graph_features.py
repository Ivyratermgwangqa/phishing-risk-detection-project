# graph_features.py
import networkx as nx
import time
import csv
import pandas as pd
import argparse
import logging

logging.basicConfig(level=logging.INFO)


def build_graph(records):
    """Constructs directed graph from sender→URL→domain records."""
    G = nx.DiGraph()
    for rec in records:
        sender = rec.get('sender_domain') or rec.get('sender')
        url = rec.get('url')
        domain = rec.get('domain')
        if not url and not domain and not sender:
            continue
        if sender:
            G.add_node(sender, type='sender')
        if url:
            G.add_node(url, type='url')
        if domain:
            G.add_node(domain, type='domain')
        if sender and url:
            G.add_edge(sender, url)
        if url and domain:
            G.add_edge(url, domain)
    return G


def pagerank_sparse(G, alpha=0.85, max_iter=100, tol=1.0e-6, max_time_seconds=10):
    """Sparse, adjacency-list PageRank power iteration with time limit.

    Returns dict: node -> score
    """
    nodes = list(G.nodes())
    N = len(nodes)
    if N == 0:
        return {}
    idx = {n: i for i, n in enumerate(nodes)}
    out_links = {i: [idx[w] for w in G.successors(n) if w in idx] for n, i in idx.items()}
    ranks = [1.0 / N] * N
    teleport = (1.0 - alpha) / N
    start = time.time()
    for it in range(max_iter):
        new_ranks = [teleport] * N
        for i in range(N):
            if out_links.get(i):
                share = ranks[i] / len(out_links[i])
                for j in out_links[i]:
                    new_ranks[j] += alpha * share
            else:
                # sink: distribute equally
                for j in range(N):
                    new_ranks[j] += alpha * (ranks[i] / N)
        err = sum(abs(new_ranks[i] - ranks[i]) for i in range(N))
        ranks = new_ranks
        if err < tol:
            break
        if time.time() - start > max_time_seconds:
            logging.warning('PageRank timed out after %s seconds at iteration %d', max_time_seconds, it)
            break
    return {nodes[i]: ranks[i] for i in range(N)}


def extract_graph_metrics(G, use_sparse_pr=True, pr_time_limit=10):
    """Computes graph-based features: degree, pagerank.

    If `use_sparse_pr` is True the function will use `pagerank_sparse` (safer
    for large graphs) and fall back to NetworkX pagerank if needed.
    """
    deg = dict(G.degree())
    pagerank = {}
    try:
        if use_sparse_pr:
            pagerank = pagerank_sparse(G, max_time_seconds=pr_time_limit)
        else:
            pagerank = nx.pagerank(G)
    except Exception as e:
        logging.warning('nx.pagerank failed: %s; falling back to sparse pagerank', e)
        pagerank = pagerank_sparse(G, max_time_seconds=pr_time_limit)
    features = []
    for node in G.nodes():
        features.append({
            'node': node,
            'type': G.nodes[node].get('type'),
            'degree': deg.get(node, 0),
            'pagerank': pagerank.get(node, 0.0)
        })
    return features


def read_records_from_csv(path, sample_n=0):
    df = pd.read_csv(path)
    if sample_n and sample_n > 0:
        df = df.head(sample_n)
    # expected columns: sender_domain, url, domain (be permissive)
    return df.to_dict(orient='records')


def write_metrics(metrics, out_path):
    keys = ['node', 'type', 'degree', 'pagerank']
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for m in metrics:
            writer.writerow({k: m.get(k) for k in keys})


def cli():
    try:
        from . import config
    except Exception:
        import config
    parser = argparse.ArgumentParser(description='Build graph and compute metrics from CSV records')
    parser.add_argument('--input', '-i', default=getattr(config, 'PROCESSED_ENRON_SENDERS', 'data/processed/enron_senders.csv'))
    parser.add_argument('--output', '-o', default='data/processed/graph_metrics.csv')
    parser.add_argument('--sample', '-n', type=int, default=1000, help='Sample N rows (0 = full)')
    parser.add_argument('--pr-timeout', type=int, default=10, help='PageRank time limit in seconds')
    args = parser.parse_args()

    logging.info('Reading records from %s', args.input)
    records = read_records_from_csv(args.input, sample_n=args.sample)
    logging.info('Building graph with %d records', len(records))
    G = build_graph(records)
    logging.info('Graph has %d nodes and %d edges', G.number_of_nodes(), G.number_of_edges())
    metrics = extract_graph_metrics(G, use_sparse_pr=True, pr_time_limit=args.pr_timeout)
    logging.info('Writing metrics to %s', args.output)
    write_metrics(metrics, args.output)
    logging.info('Done')


if __name__ == '__main__':
    cli()
