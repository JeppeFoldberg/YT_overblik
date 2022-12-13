#%% 
import pandas as pd
# %%
respondents = ['01', '03', '04', '07', '10']
# %%
dfs = [pd.read_csv(f'../cleaned_data/{respondent}/missing_tags.csv', index_col=0) for respondent in respondents]
# %%
total = pd.concat(dfs)
# %%
total.sort_values(['respondent', 'period'],
                ascending= True,
                inplace=True)


# %%
total['missing_tags_pct'] = round(total['missing_tags_pct'], 1)
# %%
print(total.to_latex(index=False))