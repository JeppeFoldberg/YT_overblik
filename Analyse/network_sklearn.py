#%% 
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
import sys
#%% 
stopwords = stopwords.words('english')
#%% 
df = pd.read_csv('../Renset data/test_af_nyt_script.csv', index_col=0)
# way of getting only the rows with actual tags
tag_lists = df.tag[~pd.isna(df.tag) == True]
# print(sys.getsizeof(tags_list))

# tags_list = [tags.split(',') for tags in tag_lists]

# remove stopwords as well! 
# tags_list = [[word for word in tag_list if word not in stopwords] for tag_list in tags_list] 
# print(sys.getsizeof(tags_list))
# %%
cv = CountVectorizer(token_pattern=r'[^,]*', min_df=0.01, max_df=0.95) # Maybe set min and max df to minimize the size of the network! could be max_df = 0.95, min_df = 0.4
X = cv.fit_transform(tag_lists)

# %%
Xc = (X.T * X) # This is the matrix manipulation step
Xc.setdiag(0) # We set the diagonals to be zeroes as it's pointless to be 1
# %%
names = cv.get_feature_names_out()
df = pd.DataFrame(data = Xc.toarray(), columns = names, index = names)
df.to_csv('to gephi.csv', sep = ',')
# %%
# %%
