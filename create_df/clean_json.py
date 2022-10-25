#%% 
import pandas as pd
import re
from dateutil.parser import parse
# %%
df = pd.read_json('watch-history.json')
#%% 
df = df[pd.isna(df.details)] # removing ads! 
# %%
df['date_watched'] = [parse(time) for time in df.time]
# %%

df['titleUrl'].fillna(df.title, inplace=True)

df['video_id'] = [re.search(r'https://www.youtube.com/watch\?v=(.*)', str(titleurl)) for titleurl in df.titleUrl]

# %%
df = df.dropna(subset = 'video_id') # some videos do not have a link – we remove them! 

df['video_id'] = [video_id.group(1) for video_id in df.video_id] # getting only the id! 

# %%
# rename title to video_title and clean the watched away! 
df['video_title'] = [re.search(r'Watched (.*)', title).group(1) for title in df.title] 

#%%
df = df.dropna(subset='subtitles')

df['channel_title'] = [info[0]['name'] for info in df.subtitles]
df['channel_link'] = [info[0]['url'] for info in df.subtitles]
# select the columns cleaned above! 

# %%

df.subtitles[0]
# %%
