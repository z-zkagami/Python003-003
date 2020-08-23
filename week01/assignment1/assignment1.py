# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

# get movie's url and name
def get_movie_info(myurl): 
    """
        emulate chrome and get movie name/catagory/release data use split list
    """
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    header = {'user-agent': user_agent, "cookie" : "__mta=151852934.1587443709643.1587598935122.1587600366133.43; uuid_n_v=v1; uuid=F37C1E10838811EA8ABB63E31D5D873EFCF954692DBF4022A2CA534951698F60; _lxsdk_cuid=1719b014425c8-0c9bf88d1425e9-4313f6b-1fa400-1719b014425c8; _lxsdk=F37C1E10838811EA8ABB63E31D5D873EFCF954692DBF4022A2CA534951698F60; mojo-uuid=d174ce0bb6042f1360f126301f67ba77; t_lxid=1719b0145b6c8-091e3087e85102-4313f6b-1fa400-1719b0145b6c8-tid; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; __mta=219069734.1587443484067.1587459109767.1587475084518.17; _csrf=1d00bd0bae5d97db8d8b75aba18f671878162878089874b0349b5d2a5037d688; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1587531265,1587558230,1587564223,1587598925; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1587600366; _lxsdk_s=171a4e020da-6c5-2ad-67c%7C%7C1"}
    response = requests.get(myurl, headers=header)
    bs_info = bs(response.text, 'html.parser')

    # with open(myurl, 'r', encoding='utf-8') as maoyan:
    #     bs_info = bs(maoyan.read(), 'html.parser')
    
    top10 = []
    movie_list = bs_info.find_all('div', attrs={'class': 'movie-hover-info'}, limit=10)
    for movie in range(10):
        movie_name = movie_list[movie].find('span', attrs={'class', 'name'}).text
        # movie_name = movie_list[movie].test.split('\n')[2].strip()
        movie_catagories = movie_list[movie].text.split('\n')[7].strip()
        movie_release_date = movie_list[movie].text.split('\n')[15].strip()

        # gen single movie dict
        single = {}
        single[f'电影名称'] = movie_name
        single[f'电影类型'] = movie_catagories
        single[f'上映时间'] = movie_release_date

        # gen top10 list
        top10.append(single)
    return top10

top10_info = get_movie_info('https://maoyan.com/films?showType=3')
# top10_info = get_movie_info('/Users/XXXX/Python003-003/week01/assignment1/maoyan.html')
# to csv file
top10_movies = pd.DataFrame(data=top10_info)
top10_movies.to_csv('./top10_movies.csv', encoding='utf-8', index=False)
