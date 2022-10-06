#%% 
import pandas as pd
from nltk import bigrams
import itertools
from collections import Counter
import networkx as nx
import matplotlib.pyplot as plt
# %%
df = pd.read_csv('../Renset data/test_af_nyt_script.csv', index_col=0)
# %%
# way of getting only the rows with actual tags
tags_list = df.tag[~pd.isna(df.tag) == True]
# for each list split into tags that becomes its own string
tags_list = [tags.split(',') for tags in tags_list]

# %%
terms_bigram = [list(bigrams(tags)) for tags in tags_list]
# %%
# Flatten list of bigrams in 
bigrams = list(itertools.chain(*terms_bigram))

# Create counter of words in clean bigrams
bigram_counts = Counter(bigrams)

temp = bigram_counts.most_common(200)
# %%
bigram_df = pd.DataFrame(bigram_counts.most_common(50), columns=['bigram', 'count'])
# Create dictionary of bigrams and their counts
d = bigram_df.set_index('bigram').T.to_dict('records')
# %%
G = nx.Graph()

# Create connections between nodes
for k, v in d[0].items():
    G.add_edge(k[0], k[1], weight=(v * 10))

# %%
fig, ax = plt.subplots(figsize=(10, 8))

pos = nx.spring_layout(G, k=2)

# Plot networks
nx.draw_networkx(G, pos,
                 font_size=16,
                 width=3,
                 edge_color='grey',
                 node_color='purple',
                 with_labels = False,
                 ax=ax)

# Create offset labels
for key, value in pos.items():
    x, y = value[0]+.135, value[1]+.045
    ax.text(x, y,
            s=key,
            bbox=dict(facecolor='red', alpha=0.25),
            horizontalalignment='center', fontsize=13)
    
plt.show()
# %%
