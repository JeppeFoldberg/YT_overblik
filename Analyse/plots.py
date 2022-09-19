# %%
from operator import index
import pandas as pd
import bar_chart_race as bcr
# %%
df = pd.read_csv('../Renset data/history_w_videoinfo.csv', index_col=0)
# %%
df['datetime'] = pd.to_datetime(df['date_watched'], utc=True)
df['day_watched'] = df['datetime'].dt.floor("D")
df['channel_title_cat'] = df['channel_title'].astype('category')

# group by day watched and channel title and count daily views on the channel
temp = df.groupby(['day_watched', 'channel_title'], as_index=False)['video_title'].nunique()

# pivot wider so we can see the daily views on all channels in a single row
temp2 = temp.pivot(index='day_watched', columns='channel_title', values='video_title')

# remove channels with less than n views. 
temp2 = temp2[temp2.columns[temp2.sum()>10]]

# replace nans with 0
temp2 = temp2.fillna(0)

# aggregate sums for each 
temp2 = temp2.cumsum()

# %%
pd.to_datetime(df['date_watched'], utc = True)
# df.datetime
# %%
df.groupby(['datetime', 'channel_title']).count()
# %%
df.groupby(['datetime.floor("W")', 'channel_title']).sum()

# %%
bcr.bar_chart_race(df=temp2, filename="bcr_test.gif")
# %%
