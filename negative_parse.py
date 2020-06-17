import requests
import bs4
from multiprocessing import Pool
from functools import reduce
import time
import random
import pandas as pd
import re

def get_review_link(url):
    try:
        req = requests.get(url)
        parser = bs4.BeautifulSoup(req.text, 'lxml') 
        model_reviews = parser.find_all('div', attrs={'class':'find-list-box'})
        return(['https://nanegative.ru' + select_phone.find('a', attrs={'class':'ss'})['href']  for select_phone in model_reviews])
    except:
        return(['error'])
def get_comments(url):
    time.sleep(random.randint(0,10))
    try:
        req = requests.get(url)
    except:
        return(pd.DataFrame(columns=['comment', 'rating']))
    parser = bs4.BeautifulSoup(req.text, 'lxml')
    reviews = parser.find_all('div', attrs={'class':'reviewers-box'})
    comments = []
    ratings=[]
    for review in reviews:
        try:
            comments.append((review.find('td', attrs={'itemprop':'contra'}).text +
                                review.find('td', attrs={'itemprop':'reviewBody'}).text).strip())
            ratings.append(5-len(review.find('ul', attrs={'class':'rate'}).find_all('span', attrs={'class': 'star e'})))
        except:
            pass
    return(pd.DataFrame(list(zip(comments,ratings)), columns=['comment', 'rating']))

if __name__ == '__main__':    
    res_df = pd.DataFrame(columns=['comment', 'rating'])
    parse_links = ['https://nanegative.ru/mobilnye-telefony-otzivy?page={}'.format(str(n)) for n in range(1, 15)]
    for link in parse_links:
        p = Pool(10)
        phone_model_links = get_review_link(link)
        map_results = p.map(get_comments, phone_model_links)
        map_df = pd.concat(map_results, ignore_index=True)
        res_df = pd.concat([res_df, map_df], ignore_index=True)
    res_df.to_pickle('negative_parsing_results.pkl')
