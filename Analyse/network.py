#%% 
import pandas as pd
# %%
df = pd.read_csv('../Renset data/test_af_nyt_script.csv', index_col=0)
# %%
# way of getting only the rows with actual tags
# test.tag[~pd.isna(test.tag) == True]
