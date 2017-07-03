# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from lxml import html
import json
import csv
import requests
import json
import re




APIKEY = '**********' # 이 곳에 다음 API 키를 입력 (http://developer.naver.com/wiki/pages/OpenAPI)
MAPAPI = 'http://apis.daum.net/local/geo/addr2coord?apikey=%s&q=%s&output=json' # API 결과물을 json파일 형태로 받는다

def get_latlon(query):
    # query값으로 주소 형태의 데이터가 들어오면 다음 API를 통해서 위도, 경도 값을 반환
    resp = requests.get(MAPAPI % (APIKEY, query))
    try:
        # json형태의 API 결과물중에서 위도, 경도에 해당하는 결과값만을 호출
        lat = json.loads(resp.text)['channel']['item'][0]['lat']
        lng = json.loads(resp.text)['channel']['item'][0]['lng']
        return (lat, lng)
    except:
        # 위도, 경도 값을 얻을 수 없는 주소값이 존재
        # 이러한 경우 값을 0으로 받고 추후 수기로 위도, 경도 값을 추가
        return (0, 0)

def prep(category, name, address):
    # 크롤링한 데이터중 category, name, address > 위도, 경도 값을 반환
    name = name
    lat, lon = get_latlon(address)

    return {
        'name': name,
        'category': category,
        'lat': lat, 'lon': lon,
    }


# 미쉘린 가이드 서울 홈페이지에 올라온 데이터를 크롤링하는 코드
# 홈페이지의 데이터의 정보 중 category, name, address 값을 가지고 온다.
items = []
for num in range(1, 18):
    urls = ['https://guide.michelin.co.kr/ko/restaurant/page/{}'.format(num)]
    for url in urls:
        res = requests.get(url)
        content = res.content
        soup = BeautifulSoup(content, "html.parser")
        restaurants = soup.find_all('article', attrs ={'class' :"restaurant-list-wrap"})
        for restaurant in restaurants:
            category = restaurant.find('span', attrs={'class':"restaurant-list-category"}).get_text()
            name = restaurant.find(attrs={'class':"restaurant-list-title"}).get_text()
            address = restaurant.find('p', attrs={'class':"ellipsis"}).get_text().strip()
            items.append([category, name, address])

# 크롤링한 결과를 CSV파일로 저장하기 위한 형태로 정의
data = [prep(i[0],i[1],i[2]) for i in items[:]]

# 식당 이름, 위도, 경도 값을 CSV파일 형태로 저장
with open('places.csv', 'w') as f:
    f.write('name,lat,lon\n')
    for d in data:
        f.write('%(name)s,%(lat)s,%(lon)s\n' % d)