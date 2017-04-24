# -*- coding: utf-8 -*-
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import time
import random

# 建立 MongoDB 数据库连接
conn = MongoClient('localhost', 27017)

# 新建一个test数据库
db = conn.beijing_dongcheng_new


headers = {
    'Host' : 'esf.fang.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
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
    

    titles = soup.select('dd > p.title > a')            # 标题
    # print ("titles:", titles)
    hrefs = soup.select('dd > p.title > a')            # 链接
    # print ("hrefs:", hrefs)
    # details = soup.select('dd > p.mt12')                # 建筑信息
    # print ("details:", details)
    courts = soup.select('dd > p:nth-of-type(3) > a')   # 小区
    # print ("courts:", courts)
    adds = soup.select('dd > p:nth-of-type(3) > span')  # 地址
    # print ("adds:", adds)
    areas = soup.select('dd > div.area.alignR > p:nth-of-type(1)')     # 面积
    # print ("areas:", areas)
    prices = soup.select('dd > div.moreInfo > p:nth-of-type(1) > span.price')  # 总价
    # print ("prices:", prices)
    danjias = soup.select('dd > div.moreInfo > p.danjia.alignR.mt5')    # 单价
    # print ("danjias:", danjias)
    authors = soup.select('dd > p.gray6.mt10 > a')      # 发布者
    # print ("authors:", authors)

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



    for title, href, court, add, area, price, danjia, author in zip(titles, hrefs, courts, adds, areas, prices, danjias, authors):
        ### get the detail information for each unit /page
        each_href = 'http://esf.fang.com' + href.get('href')
        #print ("each_href",each_href)
        # example = 'http://esf.fang.com/chushou/14_789454.htm'
        try:
            each_response = requests.get(each_href, headers=headers, timeout=20)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print (e)
            continue

        each_soup = BeautifulSoup(each_response.text, 'lxml')

        update_times = each_soup.select('div.mainBoxL > div.title > p.gray9 > span')
        update_time_raw = find_str(update_times, '发布时间')                                #发布时间
        update_time_str = update_time_raw.get_text()
        update_time = update_time_str.strip("(")

        #print (update_time)


        details = each_soup.select('div.inforTxt > dl > dd')  #建筑信息
        # print ('len', len(details))
        # print ("build_time", details)
        if len(details) == 1:
            print("Different Template:", each_href)
            details_diff = each_soup.select('div.inforTxt > dl > dd > dd')
            details = details_diff
            # print ('len', len(details_diff))
            # print ("build_time", details_diff)
        # build_time = details[4]                               #建筑时间
        # # print ("build_time", build_time)
        # direction = details[5]                                #朝向
        # which_floor = details[6]                              #楼层
        # structure = details[7]                                #结构
        # decoration = details[8]                               #装修
        # house_form = details[9]                               #住宅类别
        # build_form = details[10]                              #建筑类别
        # property_right = details[11]                          #产权性质
        floor_plan = find_str(details, '户型')
        # print(floor_plan)
        down_payment = find_str(details, '参考首付')
        build_time = find_str(details,'年代')
        direction = find_str(details,'朝向')
        which_floor = find_str(details,'楼层')
        structure = find_str(details,'结构')
        decoration = find_str(details,'装修')
        house_form = find_str(details,'住宅类别')
        build_form = find_str(details,'建筑类别')
        property_right = find_str(details,'产权性质')

        districts= each_soup.select('div.inforTxt > dl > dt > a')

        # print ("district", districts)
        district = "东城"
        add_text = add.get_text()
        sub_num = add_text.find('-')
        sub_district = add_text[0:sub_num]
        # district_str = districts.get_text()
        # district = district_str.split(' ')[1].strip("()")     #区域
        # sub_district = district_str.split(' ')[2].strip("()") #sub 区域
        # print ("district_set:", sub_district)
        area_str = area.get_text()
        area_hex = "".join("{:02x}".format(ord(c)) for c in area_str)
        area_hex = area_hex.split('ff')
        area = ''.join(chr(int(area_hex[0][i:i+2], 16)) for i in range(0, len(area_hex[0]), 2)) #面积
        # print ("areas:", area)
        danjia_str = danjia.get_text()
        danjia_hex = "".join("{:02x}".format(ord(c)) for c in danjia_str)
        danjia_hex = danjia_hex.split('51')
        danjia = ''.join(chr(int(danjia_hex[0][i:i+2], 16)) for i in range(0, len(danjia_hex[0]), 2)) #单价
        # print ("danjias:", danjia)
      




        data = {
            'district': district,
            'sub_district': sub_district,
            'title': title.get_text(),
            'href': 'http://esf.fang.com' + href.get('href'),
            #'detail': list(detail.stripped_strings),
            'court': court.get_text(),
            'add': add.get_text(),
            'area': area,
            'total_price': price.get_text(),
            'unit_price': danjia,
            'down_payment': down_payment.get_text(),
            'author': author.get_text(),
            'update_time': update_time,
            'build_time': build_time.get_text(),
            'direction': direction.get_text(),
            'which_floor': which_floor.get_text(),
            'structure': structure.get_text(),
            'floor_plan': floor_plan.get_text(),
            'decoratioin': decoration.get_text(),
            'house_form': house_form.get_text(),
            'build_form': build_form.get_text(),
            'property_right': property_right.get_text()
        }
        db.test.insert_one(data)
        # print ("WU")
        # time.sleep(1000)
        

response = requests.get('http://esf.fang.com/', headers=headers)
soup = BeautifulSoup(response.text, 'lxml')

# regions = soup.select('#list_D02_10 > div.qxName > a')  # 区域
# http://esf.fang.com/house-a00/ 海淀
# http://esf.fang.com/house-a01/ 朝阳
# http://esf.fang.com/house-a02/ 东城
# http://esf.fang.com/house-a03/ 西城
regions = '/house-a02/'
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
