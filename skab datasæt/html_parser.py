from functools import wraps
import time
from bs4 import BeautifulSoup as bs
import re
import pandas as pd

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result

    return timeit_wrapper


@timeit
def parse_html(path): 
    with open(path) as f:
        # read file
        content = f.read()
        # parse with bs
        soup = bs(content, 'lxml')

    return soup

def is_a_video(tag): 
    '''
    Filter to remove ads
    takes a block of html code and returns a boolean with whether this is an ad or not
    '''
    return not(bool(re.search('From Google Ads', tag.get_text())))
    

def parse_watch_history(soup):
    '''takes a parsed tree of watch history (wh) from beautiful soup and returns a simple df with the relevant data'''
    # hver yderste blok har klassen 'outer-cell mdl-cell mdl-cell--12-col mdl-shadow--2dp' - Her henter vi dem alle sammen
    blocks = soup.find_all(class_ = 'outer-cell mdl-cell mdl-cell--12-col mdl-shadow--2dp')
    blocks_cleaned = [block for block in blocks if is_a_video(block)]
    print(f'{len(blocks)} entries - {len(blocks_cleaned)} after cleaning. {len(blocks) - len(blocks_cleaned)} ads removed!')
    return blocks_cleaned


watch_history = parse_html('Rådata/Takeout/YouTube and YouTube Music/history/watch-history.html')

watch_history_blocks = parse_watch_history(watch_history)

# print(watch_history_blocks[:4])

# notes:
# remember to turn strings into unicode before storing them! 
# If you want to use a NavigableString outside of Beautiful Soup, you should call unicode() on it to turn it into a normal Python Unicode string. 
# If you don’t, your string will carry around a reference to the entire Beautiful Soup parse tree, even when you’re done using Beautiful Soup.
# This is a big waste of memory.