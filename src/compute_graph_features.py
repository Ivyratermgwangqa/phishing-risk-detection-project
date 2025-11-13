import os
import pandas as pd
import networkx as nx
import tldextract
from tqdm import tqdm
import math

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPATH = os.path.join(PROJECT_ROOT, 'data', 'processed', 'phishing_graph_features.csv')
OUTPATH = INPATH  # overwrite with extra cols

df = pd.read_csv(INPATH)
# Ensure url/domain/sender_domain columns exist
df['url'] = df.get('url', pd.Series(dtype=str))
df['domain'] = df.get('domain', df['url'].apply(lambda u: tldextract.extract(str(u)).registered_domain if pd.notna(u) and u != '' else None))
df['sender_domain'] = df.get('sender_domain', pd.Series(dtype=str))

# Build a lightweight bipartite/aggregated graph between sender_domain <-> domain
# Use aggregated weights (number of distinct URLs connecting them) to reduce size
agg = (
    df.dropna(subset=['domain'])
      .assign(sender_domain=df['sender_domain'].fillna(''))
      .groupby(['sender_domain', 'domain'])['url']
      .nunique()
      .reset_index(name='weight')
)

G = nx.Graph()
# add nodes and weighted edges for sender_domain <-> domain only (skip url nodes)
for _, row in agg.iterrows():
    s = row['sender_domain'] if row['sender_domain'] != '' else None
    d = row['domain']
    if s:
        G.add_node(f"sender::{s}", type='sender')
        G.add_node(f"domain::{d}", type='domain')
        G.add_edge(f"sender::{s}", f"domain::{d}", weight=int(row['weight']))
    else:
        # keep domain nodes even without sender
        G.add_node(f"domain::{d}", type='domain')

# Cheap node metrics on the aggregated graph
deg = dict(G.degree(weight=None))
deg_w = dict(G.degree(weight='weight'))
# clustering only defined for undirected graphs; clustering on aggregated graph
cluster = nx.clustering(G, weight='weight')

# approximate betweenness on aggregated graph using sampling (k nodes)
n_nodes = G.number_of_nodes()
# pick sample size:  min( max(50, 1% of nodes), 200 )
k = min(200, max(50, math.ceil(0.01 * n_nodes)))
if k >= 1 and n_nodes > 100:
    sampled_nodes = None  # let networkx choose k source nodes randomly (seed for reproducibility)
    bet = nx.betweenness_centrality(G, k=k, seed=42, normalized=True, weight='weight')
else:
    bet = nx.betweenness_centrality(G, normalized=True, weight='weight')

# Map aggregated metrics back to dataframe
def node_key(prefix, val):
    return f"{prefix}::{val}" if pd.notna(val) else None

df['domain_degree_agg'] = df['domain'].apply(lambda d: deg.get(node_key('domain', d), 0))
df['sender_degree_agg'] = df['sender_domain'].apply(lambda s: deg.get(node_key('sender', s), 0) if pd.notna(s) else 0)
df['domain_degree_weighted'] = df['domain'].apply(lambda d: deg_w.get(node_key('domain', d), 0))
df['domain_clustering_agg'] = df['domain'].apply(lambda d: cluster.get(node_key('domain', d), 0.0))
df['domain_betweenness_approx'] = df['domain'].apply(lambda d: bet.get(node_key('domain', d), 0.0))
df['sender_betweenness_approx'] = df['sender_domain'].apply(lambda s: bet.get(node_key('sender', s), 0.0) if pd.notna(s) else 0.0)

# Also attach simple url-level degrees from raw graph projection (count distinct senders/domains per URL)
# url_degree = number of unique domains + unique sender_domains connected to url (cheap counts)
url_sender_counts = (
    df.groupby('url').agg(
        unique_domains=('domain', lambda x: x.nunique()),
        unique_senders=('sender_domain', lambda x: x.nunique())
    ).reset_index()
)
url_sender_counts = url_sender_counts.set_index('url')
df['url_degree_simple'] = df['url'].apply(lambda u: int(url_sender_counts.at[u, 'unique_domains']) + int(url_sender_counts.at[u, 'unique_senders']) if pd.notna(u) and u in url_sender_counts.index else 0)

# Save enriched dataframe
df.to_csv(OUTPATH, index=False)
print('Aggregated graph features computed and saved to', OUTPATH)
print(f'Aggregated graph nodes={n_nodes}, betweenness_k={k}')