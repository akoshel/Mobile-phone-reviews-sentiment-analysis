import requests
import bs4
from multiprocessing import Pool
from functools import reduce
import time
import random
import pandas as pd
import re

def parse_page(url):
    time.sleep(random.randint(0,10))
    try:
        req = requests.get(url)
    except:
        return(pd.DataFrame(columns=['comment', 'rating']))
    parser = bs4.BeautifulSoup(req.text, 'lxml')
    posts = parser.find_all('div', attrs={'class':'popular-review-item'})
    comments=[]
    ratings=[]
    for post in posts:
        try:
            comment = re.findall(r'Комментарий[^\>]*', post.text)[0].replace('Комментарий:', '').strip()
            rating = post.find('ul', attrs={'class':'goods-rating'}).find_all('li', attrs={'class':'full'})
            comments.append(comment)
            ratings.append(len(rating))
        except:
            pass
    return( pd.DataFrame(list(zip(comments,ratings)), columns=['comment', 'rating']))

if __name__ == '__main__':    
    p = Pool(10)
    url_list5 = ['https://imarket.by/category-reviews/mobilnye-telefony/?page={}&rating=5'.format(str(n)) for n in range(2, 100)]
    map_results5 = p.map(parse_page, url_list5)
    result5 = pd.concat(map_results5, ignore_index=True)
    url_list4 = ['https://imarket.by/category-reviews/mobilnye-telefony/?page={}&rating=4'.format(str(n)) for n in range(2, 100)]
    map_results4 = p.map(parse_page, url_list4)
    result4 = pd.concat(map_results4, ignore_index=True)
    url_list2 = ['https://imarket.by/category-reviews/mobilnye-telefony/?page={}&rating=2'.format(str(n)) for n in range(2, 100)]
    map_results2 = p.map(parse_page, url_list2)
    result2 = pd.concat(map_results2, ignore_index=True)
    url_list1 = ['https://imarket.by/category-reviews/mobilnye-telefony/?page={}&rating=1'.format(str(n)) for n in range(2, 100)]
    map_results1 = p.map(parse_page, url_list1)
    result1 = pd.concat(map_results1, ignore_index=True)
    conc_result = pd.concat([result1, result2, result4, result5], ignore_index=True)
    conc_result.to_pickle('parsing_results.pkl')
    
