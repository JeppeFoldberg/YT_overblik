from bs4 import BeautifulSoup as bs
import re
from dateutil.parser import parse
import pandas as pd
import sys
from datetime import datetime, date
import locale

def parse_html(path): 
    with open(path) as f:
        # read file
        content = f.read()
        # parse with bs
        soup = bs(content, 'lxml')

    return soup

def is_a_video(tag, da=False): 
    '''
    Filter to remove ads and videos that still ex
    takes a block of html code and returns a boolean with whether this is an ad or not
    '''
    if da:
        not_an_ad = not(bool(re.search('Fra Google Annoncer', tag.get_text())))
    else:
        not_an_ad = not(bool(re.search('From Google Ads', tag.get_text())))

    not_deleted = len(tag.find_all('a')) > 2
    
    return (not_an_ad & not_deleted)   

def parse_watch_history(soup, da = False):
    '''takes a parsed tree of watch history (wh) from beautiful soup and returns a simple df with the relevant data'''
    # hver yderste blok har klassen 'outer-cell mdl-cell mdl-cell--12-col mdl-shadow--2dp' - Her henter vi dem alle sammen
    blocks = soup.find_all(class_ = 'outer-cell mdl-cell mdl-cell--12-col mdl-shadow--2dp')
    blocks_cleaned = [block for block in blocks if is_a_video(block, da)]
    print(f'{len(blocks)} entries - {len(blocks_cleaned)} after cleaning. {len(blocks) - len(blocks_cleaned)} ads removed!')
    return blocks_cleaned

def make_df(blocks, da=False):
    '''
    takes in the blocks of watch history and parses them to create the dataframe with all of their data
    '''
    video_titles = []
    video_id = []
    channel_titles = []
    channel_links = []
    date_watched = []

    # i = 0 # debugging! 
    for block in blocks:
        links = block.find_all('a')
        
        video_titles.append(links[0].text)
        video_id.append(re.search(r'https://www.youtube.com/watch\?v=(.*)', links[0]['href']).group(1))
        channel_title = links[1].text # get channel title for date search! 
        channel_titles.append(channel_title)
        channel_links.append(links[1]['href'])


        temp = block.text
        # Useful for debugging
        # i += 1
        # print(f'{len(links)} links; entry {i} with title {links[0].text}')

        if da: 
             # find out if text has the weird watched at text so we can avoid it! 
            watched_at = re.search(r'Set \d\d:\d\d', block.text) 
            channel_title = re.escape(channel_title) # escape so we avoid problems with channel titles full of weird characters! 

            if watched_at:
                search_string = fr'{channel_title}{watched_at.group()}(\d?\d\.? \w{{3,4}}\.? \d{{4}} \d{{2}}\.\d{{2}}\.?\d{{2}}[^P]*)'  
            else:
                search_string = fr'{channel_title}(\d?\d\.? \w{{3,4}}\.? \d{{4}} \d{{2}}\.\d{{2}}\.\d{{2}}[^P]*)' 

            date_string = re.search(search_string, block.text)
            # remaking date string into a format that can be parsed! 
            date_string = date_string.group(1).replace('.', ':').replace(':', '', 1)

            replacements = {
                'jan:': 'January', 
                'feb:': 'February', 
                'mar:': 'March', 
                'apr:': 'April', 
                'maj': 'May', 
                'jun:': 'June', 
                'jul:': 'July', 
                'aug:': 'August', 
                'sep:': 'September', 
                'okt:': 'October', 
                'nov:': 'November', 
                'dec:': 'December'
                }
            for short, long in replacements.items():
                date_string = date_string.replace(short.lower(), long)

            date_watched.append(parse(date_string))

        else:
            # find out if text has the weird watched at text so we can avoid it! 
            watched_at = re.search(r'Watched at \d\d:\d\d', block.text) 
            channel_title = re.escape(channel_title) # escape so we avoid problems with channel titles full of weird characters! 

            if watched_at:
                search_string = fr'{channel_title}{watched_at.group()}(\d?\d \w{{3,4}} \d{{4}}, \d{{2}}:\d{{2}}:\d{{2}}[^P]*)'  
            else:
                search_string = fr'{channel_title}(\d?\d \w{{3,4}} \d{{4}}, \d{{2}}:\d{{2}}:\d{{2}}[^P]*)' 

            date_string = re.search(search_string, block.text)

            if date_string:
                date_watched.append(parse(date_string.group(1)))
            else:
                # to catch weird AM/PM format of some watch histories! 
                search_string = fr'{channel_title}(\w{{3}} \d?\d, \d{{4}}, \d{{1,2}}:\d{{2}}:\d{{2}} [PA]M [^P]*)' 
                date_string = re.search(search_string, block.text)
                date_watched.append(parse(date_string.group(1)))


    return(
    pd.DataFrame({
        'video_title' : video_titles,
        'video_id' : video_id,
        'channel_title' : channel_titles,
        'channel_link' : channel_links,
        'date_watched' : date_watched
    }))

def main():
    respondent = sys.argv[1]
    if len(sys.argv) > 2:
        da = sys.argv[2]
    else:
        da = False

    if da: 
        path = f'raw_data/{respondent}/afspilningshistorik.html'
    else: 
        path = f'raw_data/{respondent}/watch-history.html'

    watch_history = parse_html(path)

    watch_history_blocks = parse_watch_history(watch_history)

    df = make_df(watch_history_blocks, da)
        
    df.to_csv(f'cleaned_data/{respondent}/history_df.csv')


if __name__ == '__main__':
    main()
    
# notes:
# remember to turn strings into unicode before storing them! 
# If you want to use a NavigableString outside of Beautiful Soup, you should call unicode() on it to turn it into a normal Python Unicode string. 
# If you don’t, your string will carry around a reference to the entire Beautiful Soup parse tree, even when you’re done using Beautiful Soup.
# This is a big waste of memory.