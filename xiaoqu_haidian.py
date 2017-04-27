# -*- coding: utf-8 -*-
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import time
import random

# 建立 MongoDB 数据库连接
conn = MongoClient('localhost', 27017)

# 新建一个test数据库
db = conn.beijing_haidian_xiaoqu_new_1


headers = {
    'Host' : 'esf.fang.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Connection' : 'Keep-Alive'
}

mobile_headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1',
    'Connection' : 'Keep-Alive'
}


# file_object = open('ip.txt')   #ip.txt保存可用代理ip
# ip_lists = file_object.readlines()

## error 
error_html = "<div>NULL<div>"
error_soup = BeautifulSoup(error_html, "lxml")
error_div = error_soup.div

def find_str(details, name):
    for item in details:
        item_text = item.get_text()
        #print (item_text)
        number = item_text.find(name)
        #print (number)
        if number >= 0:
            return item
    return error_div

court_set = []

xiaoqu = open("haidian_xiaoqu_1.txt", "a")


def spider_1(url):
    print ("url:", url)
    # if url in url_set:
    #    return
    try:
        response = requests.get(url, headers=headers, timeout=20)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print (e)
        return 

    soup = BeautifulSoup(response.text, 'lxml')
    
    courts = soup.select('dd > p:nth-of-type(3) > a')   # 小区
    # print ("courts:", courts)

    for court in courts:
        # print ("courts:", court.get_text())
        court_text = court.get_text()
        if court_text not in court_set:
            court_set.append(court_text)
            # print ("courts_href:", court.get('href'))
            href_text = court.get('href')
            href_num = href_text.find('xm')
            if href_num < 0:
                print ("href Error:", court)
                continue
            # print(href_text[href_num+2:len(href_text)-1])
            court_href = 'https://m.fang.com/xiaoqu/bj/' + href_text[href_num+2:len(href_text)-1] + '.html'
            print (court_href)
            xiaoqu.write("%s, %s, %s\n" % (court_text, href_text, court_href))

            try:
                each_response = requests.get(court_href, headers=mobile_headers, timeout=20)
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                print (e)
                continue

            each_response.encoding = 'gb18030'

            each_soup = BeautifulSoup(each_response.text, "lxml")
            #print (each_soup)
            address_html = each_soup.select('div.main > section.Nbigtitle.bb.pdX14 > p')
            # print(len(address_html))
            if len(address_html) == 0:
                print ("Address Error:", court_href)
                continue
            address = address_html[0].get_text()
            # print ("address:", address_html)

            average_price = each_soup.select('div.main > section.xqpers.mBox > h3 > span.red-df.f20.ml5')

            average_price_str = average_price[0].get_text()
            average_price_hex = "".join("{:02x}".format(ord(c)) for c in average_price_str)
            average_price_hex = average_price_hex.split('51')
            average_price = ''.join(chr(int(average_price_hex[0][i:i+2], 16)) for i in range(0, len(average_price_hex[0]), 2)) 
            # print (average_price)

            house_resource = each_soup.select('div.main > section.xqpers.mBox > ul.flexbox > li ')
            # print(house_resource)
            second_hand = find_str(house_resource, '二手房源(套)')
            second_hand_str = second_hand.get_text()
            if second_hand_str != 'NULL':
                bracket = second_hand_str.find(')')
                second_hand = second_hand_str[bracket+1: len(second_hand_str)]
            else:
                second_hand = 'NULL'
            # print (second_hand)

            second_hand_trading = find_str(house_resource, '最近成交(套)')
            second_hand_trading_str = second_hand_trading.get_text()
            if second_hand_trading_str != 'NULL': 
                bracket = second_hand_trading_str.find(')')
                second_hand_trading = second_hand_trading_str[bracket+1: len(second_hand_trading_str)]
            else:
                second_hand_trading = 'NULL'
            # print(second_hand_trading)

            basic_information = each_soup.select('div.main > section.mBox > div.pdX14 > ul.flextable.pdY10.pdX14 > li ')
            # print (basic_information)

            house_type = find_str(basic_information, '物业类型：')
            house_type_str = house_type.get_text()
            if house_type_str != 'NULL':
                colon = house_type_str.find('：')
                house_type = house_type_str[colon+1: len(house_type_str)]
            else:
                house_type = 'NULL'
            # print (house_type)
            build_time = find_str(basic_information, '建筑年代：')
            build_time_str = build_time.get_text()
            if build_time_str != 'NULL':
                colon = build_time_str.find('：')
                build_time = build_time_str[colon+1: len(build_time_str)]
            else:
                build_time = 'NULL'
            # print (build_time)

            map_information_html = each_soup.select('div.main > section.mBox > div.xqMap > a > img ')
            # print (len(map_information_html))
            if len(map_information_html) == 0:
                print ("map Error:", court_href)
                continue
            # print(map_information_html[0].get('src'))
            map_information = map_information_html[0].get('src')
            markers = map_information.find('markers')

            if markers > 0:
                comma = map_information.find(',', markers)
                marker = map_information.find('&marker', comma)
                longitude = map_information[markers+8:comma]
                latitude  = map_information[comma+1:marker]
            else:
                longitude = 0
                latitude  = 0

            # print(longitude, latitude)


            # print ("WU")
            # time.sleep(1000)

            data = {
                'district': '海淀',
                'court': court_text,
                'href': court_href,
                'address': address,
                'average price': average_price,
                'second hand resource': second_hand,
                'second hand trading': second_hand_trading,
                'house type': house_type,
                'build time': build_time,
                'longtitude':longitude,
                'latitude':latitude
            }
            db.test.insert_one(data)

    # print ("WU")
    # time.sleep(1000)


    # 区域
    # 发布时间
    # 楼层
    # 结构
    # 建筑类别
    # 产权性质
    # 经度纬度（街景地图）

    # http://esf.fang.com/house-a00/ 海淀
    # http://esf.fang.com/house-a01/ 朝阳
    # http://esf.fang.com/house-a02/ 东城
    # http://esf.fang.com/house-a03/ 西城

response = requests.get('http://esf.fang.com/', headers=headers)
soup = BeautifulSoup(response.text, 'lxml')

# regions = soup.select('#list_D02_10 > div.qxName > a')  # 区域
# http://esf.fang.com/house-a00/ 海淀
# http://esf.fang.com/house-a01/ 朝阳
# http://esf.fang.com/house-a02/ 东城
# http://esf.fang.com/house-a03/ 西城
regions = '/house-a00/'
totprices = soup.select('#list_D02_11 > p > a')  # 总价
housetypes = soup.select('#list_D02_12 > a')  # 户型
areas = soup.select('#list_D02_13 > p > a')  # 面积

totprices_len = len(totprices)
housetypes_len = len(housetypes)
areas_len = len(areas)

# 对于大于等于100页的进行细分
i = 1
while i < housetypes_len:
    resp1 = requests.get('http://esf.fang.com' + regions + housetypes[i].get('href')[7:], headers=headers)
    soup1 = BeautifulSoup(resp1.text, 'lxml')
    pages = soup1.select('#list_D10_01 > span > span')  # 页数
    if pages and pages[0].get_text().split('/')[1] == '100':
        m = 1
        while m < totprices_len:
            resp1 = requests.get('http://esf.fang.com' + regions + totprices[m].get('href')[7:-1] + '-' + housetypes[i].get('href')[7:], headers=headers)
            soup1 = BeautifulSoup(resp1.text, 'lxml')
            pages = soup1.select('#list_D10_01 > span > span')  # 页数
            if pages and pages[0].get_text().split('/')[1] == '100':
                j = 1
                while j < areas_len:
                    resp1 = requests.get('http://esf.fang.com' + regions + totprices[m].get('href')[7:-1] + '-' + housetypes[i].get('href')[7:-1] + '-' + areas[j].get('href')[7:], headers=headers)
                    soup1 = BeautifulSoup(resp1.text, 'lxml')
                    pages = soup1.select('#list_D10_01 > span > span')  # 页数
                    if pages:
                        k = int(pages[0].get_text().split('/')[1])
                        while k > 0:
                            spider_1('http://esf.fang.com' + regions + totprices[m].get('href')[7:-1] + '-' + housetypes[i].get('href')[7:-1] + '-' + areas[j].get('href')[7:-1] + '-i3' + str(k))
                            k = k - 1
                            time.sleep(2)
                    else:
                        pass
                    j = j + 1
            else:
                if pages:
                    k = int(pages[0].get_text().split('/')[1])
                    while k > 0:
                        spider_1('http://esf.fang.com' + regions + totprices[m].get('href')[7:-1] + '-' + housetypes[i].get('href')[7:-1] + '-i3' + str(k))
                        k = k - 1
                        time.sleep(2)
                else:
                    pass
            m = m + 1
    else:
        if pages:
            k = int(pages[0].get_text().split('/')[1])
            while k > 0:
                spider_1('http://esf.fang.com' + regions + housetypes[i].get('href')[7:-1] + '-i3' + str(k))
                k = k - 1
                time.sleep(2)
        else:
            pass
    i = i + 1

xiaoqu.close()
