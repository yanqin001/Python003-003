import requests
from bs4 import BeautifulSoup as bs
from time import sleep
import re
import pandas

myuser_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"
Cookie = '__mta=46077339.1598158522320.1598160585422.1598188622905.10; uuid_n_v=v1; uuid=D900EEF0E4FC11EA928CD948005EDA814BA327FB0E59484FA6C2FA497D73A1A5; _csrf=297067f4549e8756dd0e916b529b904118b4a0abbf5d73d5a1eae82827b6bb1a; _lxsdk_cuid=17419abc558c8-0d2ebfd974b73e-3323766-1fa400-17419abc558c8; _lxsdk=D900EEF0E4FC11EA928CD948005EDA814BA327FB0E59484FA6C2FA497D73A1A5; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1598158522; mojo-uuid=0f8b28b940ae1607a769104b8974ea6d; __mta=46077339.1598158522320.1598159074839.1598159736446.7; mojo-session-id={"id":"6b72f9bb1d6623e7e82cb0bfbd57e1f7","time":1598188619958}; mojo-trace-id=2; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1598188622; _lxsdk_s=1741b770842-916-b79-15b%7C%7C3'
Referer = "https://maoyan.com/films"
UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"

header = {
    "User-Agent": UserAgent,
    "Cookie": Cookie,
    "Referer": Referer,
}
myurl = 'https://maoyan.com/films?sortId=1'

response = requests.get(myurl, headers=header)
bs_info = bs(response.text, 'html.parser')

i = 1
movielist = []
for tags in bs_info.find_all('div', attrs={'class': 'channel-detail movie-item-title'}):
    if i > 10:
        break
    i += 1
    title = tags.get('title')
    id = tags.find('a').get('href')
    myurl2 = "https://maoyan.com" + id

    Referer2 = "https://maoyan.com/films?sortId=3"
    header2 = {
        "User-Agent": UserAgent,
        "Cookie": Cookie,
        "Referer": Referer,
    }
    response2 = requests.get(myurl2, headers=header2)
    bs_info2 = bs(response2.text, 'html.parser')

    typelist = []
    for tags2 in bs_info2.find_all('div', attrs={'class': 'movie-brief-container'}):
        for litag in tags2.find_all('li', attrs={'class': 'ellipsis'}):
            for atag in litag.find_all('a'):
                type = atag.text
                typelist.append(type)
        m = r'.*中国大陆[上|重]映.*'
        timetag = tags2.find_all(text=re.compile(m))
        onlinedate = timetag[0][0:10]
    type = ','.join(typelist)
    movie_info = title+","+type+","+onlinedate
    movielist.append(movie_info)

movies = pandas.DataFrame(data = movielist)

# windows需要使用gbk字符集
movies.to_csv('./movies.csv', encoding='gbk', index=False, header=False)
