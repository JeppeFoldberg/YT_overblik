#%% 
# from venv import create
import pandas as pd
# from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
import sys
#%% 
# stopwords = stopwords.words('english')
# print(sys.getsizeof(tags_list))

# tags_list = [tags.split(',') for tags in tag_lists]

# remove stopwords as well! 
# tags_list = [[word for word in tag_list if word not in stopwords] for tag_list in tags_list] 
# print(sys.getsizeof(tags_list))
#%% 
def create_cooc_matrix(df, missing_df, period = False):
    '''takes a df, gets the tags and creates a coocurrence matrix'''
    # way of getting only the rows with actual tags
    tag_lists = df.tag[~pd.isna(df.tag) == True]
    no_tags = df.shape[0]-tag_lists.shape[0]
    pct_no_tags = no_tags / df.shape[0] * 100
    if period: 
        period = df.reset_index().loc[0, 'period_watched']
    else:
        period = df.reset_index().loc[0, 'year_watched']

    print(f'{no_tags} videos did not have tags in {period}. This amounts to {pct_no_tags:.2f}%')

    respondent = sys.argv[1]
    missing = pd.DataFrame({'respondent': respondent, 'period': period, 'missing_tags_pct': pct_no_tags}, index = [0])
    missing_df = pd.concat([missing_df, missing], ignore_index=True)

    # splits on ',' because we trust the tokens used by creators! 
    cv = CountVectorizer(token_pattern=r'[^,]*', min_df=0.01, max_df=0.95) # Maybe set min and max df to minimize the size of the network! could be max_df = 0.95, min_df = 0.4

    X = cv.fit_transform(tag_lists)
    Xc = (X.T * X) # This is the matrix manipulation step
    Xc.setdiag(0) # We set the diagonals to be zeroes as it's pointless to be 1

    names = cv.get_feature_names_out()
    df = pd.DataFrame(data = Xc.toarray(), columns = names, index = names)

    return df, missing_df

#%%
def create_yearly_plots(df):
    df['date_watched'] = pd.to_datetime(df['date_watched'], utc=True)
    df['year_watched'] = df['date_watched'].dt.year 
    years = df.year_watched.unique()
    missing_df = pd.DataFrame(columns=['respondent', 'period', 'missing_tags_pct'])
    yearly_dfs = {}
    for year in years:
        year_df = df[df.year_watched == year]
        year_cooc, missing_df = create_cooc_matrix(year_df, missing_df)

        yearly_dfs[str(year)] = year_cooc

    return yearly_dfs, missing_df

# %%
def create_period_plots(df, period):
    df['date_watched'] = pd.to_datetime(df['date_watched'], utc=True)
    df['period_watched'] = df.date_watched.dt.to_period(period)

    periods = df.period_watched.unique()

    missing_df = pd.DataFrame(columns=['respondent', 'period', 'missing_tags_pct'])
    period_dfs = {}
    for period in periods:
        period_df = df[df.period_watched == period]
        period_cooc, missing_df = create_cooc_matrix(period_df, missing_df, period = True)

        period_dfs[str(period)] = period_cooc

    return period_dfs, missing_df

#%% 
def main():
    respondent_nr = sys.argv[1]

    df = pd.read_csv(f'cleaned_data/{respondent_nr}/history_info_df.csv', index_col=0)

    if len(sys.argv) <= 2:
    # cooc_matrix = create_cooc_matrix(df)
        yearly_dfs, missing_df = create_yearly_plots(df)
        for key, value in yearly_dfs.items():
            value.to_csv(f'cleaned_data/{respondent_nr}/{key}.csv', sep = ',')
    elif len(sys.argv) == 3:
        # if we want a network of all the watch history
        if sys.argv[2] == 'all':
            df['date_watched'] = pd.to_datetime(df['date_watched'], utc=True)
            df['year_watched'] = df['date_watched'].dt.year
            missing_df = pd.DataFrame(columns=['respondent', 'period', 'missing_tags_pct'])
            cooc_all, missing_df = create_cooc_matrix(df, missing_df)
            cooc_all.to_csv(f'cleaned_data/{respondent_nr}/all.csv', sep = ',')
        else:
            # if we want specific periodic networks! 
            period = sys.argv[2]
            period_dfs, missing_df = create_period_plots(df, period)
            for key, value in period_dfs.items():
                value.to_csv(f'cleaned_data/{respondent_nr}/{key}.csv', sep = ',')
    
    missing_df.to_csv(f'cleaned_data/{respondent_nr}/missing_tags.csv')

if __name__ == "__main__":
    main()
