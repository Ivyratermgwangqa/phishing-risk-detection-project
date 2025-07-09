# graph_features.py
import networkx as nx


def build_graph(records):
    """Constructs directed graph from sender→URL→domain records."""
    G = nx.DiGraph()
    for rec in records:
        sender = rec['sender_domain']
        url = rec['url']
        domain = rec['domain']
        G.add_node(sender, type='sender')
        G.add_node(url, type='url')
        G.add_node(domain, type='domain')
        G.add_edge(sender, url)
        G.add_edge(url, domain)
    return G


def extract_graph_metrics(G):
    """Computes graph-based features: degree, centrality."""
    deg = dict(G.degree())
    pagerank = nx.pagerank(G)
    features = {}
    for node in G.nodes():
        features[node] = {
            'degree': deg.get(node, 0),
            'pagerank': pagerank.get(node, 0)
        }
    return features
