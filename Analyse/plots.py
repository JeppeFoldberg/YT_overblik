# %%
from base64 import decode
from operator import index
import pandas as pd
import bar_chart_race as bcr
# %%
df = pd.read_csv('../Renset data/history_w_videoinfo.csv', index_col=0)

#%% 
def reshape_data(df): 
    '''
    Given a watch history dataframe, reshapes the data into a wide format 
    where each row corresponds to a date and each col contains the cumulated sum of views on that channels
    This dataframe is supposed to be used to create a bar chart race
    '''
    df['datetime'] = pd.to_datetime(df['date_watched'], utc=True)
    df['day_watched'] = df['datetime'].dt.date
    # Clean channel title so it can be written by bcr
    # df['channel_title'] = decode(df['channel_title']) # not quite sure that this works

    df['channel_title_cat'] = df['channel_title'].astype('category')

    # group by day watched and channel title and count daily viewed videos on the channel
    df = df.groupby(['day_watched', 'channel_title'], as_index=False)['video_title'].nunique()

    # pivot wider so we can see the daily views on all channels in a single row
    df = df.pivot(index='day_watched', columns='channel_title', values='video_title')

    # remove channels with less than n views. 
    df = df[df.columns[df.sum()>10]]

    # replace nans with 0
    df = df.fillna(0)

    # aggregate sums for each 
    df = df.cumsum()

    return df

   

# %%
def create_bcr(df, filename, n_bars = 15, period_length = 100, **kwargs):
    '''
    Takes in a dataframe in the correct format and produces a bar chart 
    '''
    bcr.bar_chart_race(df=df, filename=filename, n_bars=n_bars, filter_column_colors = True, period_length=period_length, **kwargs)

#%%
df = pd.read_csv('../Renset data/history_w_videoinfo.csv', index_col=0)
df = reshape_data(df)
create_bcr(df, "test_bcr_function.gif")

#%%
df['datetime'] = pd.to_datetime(df['date_watched'], utc=True)
df['day_watched'] = df['datetime'].dt.date

# Clean channel title so it can be written by bcr


df['channel_title_cat'] = df['channel_title'].astype('category')

# group by day watched and channel title and count daily viewed videos on the channel
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
bcr.bar_chart_race(df=temp2, filename="bcr_test2.gif", n_bars=15, filter_column_colors = True, period_length=100)
# %%
# how to clean strings... 
strings = df.channel_title.str

