# %%
from base64 import decode
from operator import index
import pandas as pd
import bar_chart_race as bcr
import sys

def reshape_data(df, cutoff = 10): 
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
    df = df[df.columns[df.sum()>cutoff]]

    # replace nans with 0
    df = df.fillna(0)

    # aggregate sums for each 
    df = df.cumsum()

    return df

   
def create_bcr(df, filename, n_bars = 25, period_length = 100, **kwargs):
    '''
    Takes in a dataframe in the correct format and produces a bar chart 
    '''
    bcr.bar_chart_race(df=df, filename=filename, n_bars=n_bars, filter_column_colors = True, period_length=period_length, **kwargs)


def main():
    respondent = sys.argv[1]
    if len(sys.argv) > 2:
        n_bars = int(sys.argv[2])
        cutoff = int(sys.argv[3])
    else:
        n_bars = 25
        cutoff = 10

    df = pd.read_csv(f'cleaned_data/{respondent}/history_info_df.csv', index_col=0)
    df = reshape_data(df, cutoff)
    create_bcr(df, f'results/{respondent}/bcr.gif', n_bars)


if __name__ == '__main__':
    main()