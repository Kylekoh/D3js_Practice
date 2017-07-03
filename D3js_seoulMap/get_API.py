#! /usr/bin/python3
# -*- coding: utf-8 -*-

from lxml import html
import requests


APIKEY = '19259c4ac090d53129abf51271cb463b' # 이 곳에 다음 API 키를 입력 (http://developer.naver.com/wiki/pages/OpenAPI)
MAPAPI = 'http://apis.daum.net/local/geo/addr2coord?apikey=%s&q=%s&output=json' # API 결과물을 json파일 형태로 받는다


def get_latlon(query):
    resp = requests.get(MAPAPI % (APIKEY, query))   
    lat = json.loads(resp.text)['channel']['item'][0]['lat']
    lng = json.loads(resp.text)['channel']['item'][0]['lng']
    return (lat, lng)


def prep(item):
    n, name = item[0].split(' ', 1)
    lat, lon = get_latlon(item[3])
    return {
        'num': n, 'name': name,
        'lat': lat, 'lon': lon,
        'description': item[1],
        'phone': item[2],
        'addr': item[3]
    }
    
def prep(category, name, address):
    name = name
    lat, lon = get_latlon(address)

    return {
        'name': name,
        'category': category,
        'lat': lat, 'lon': lon,
    }

# get data from article
r = requests.get('http://m.wikitree.co.kr/main/news_view.php?id=217101')
root = html.document_fromstring(r.text)
string = '\n'.join(root.xpath('//div[@id="ct_size"]/div//text()'))

items = []
for i in range(1, 21):
    tmp = string.split('%s.' % i, 1)
    string = tmp[1]
    items.append([j.strip() for j in tmp[0].split('\n') if j and j!='\xa0'])

data = [prep(i[:4]) for i in items[1:]]


# save data to file
with open('places.csv', 'w') as f:
    f.write('name,lat,lon\n')
    for d in data:
        f.write('%(name)s,%(lat)s,%(lon)s\n' % d)