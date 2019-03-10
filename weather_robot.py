#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- auther @icctw -*-
 
#tip: 该api  'https://www.sojson.com/open/api/weather/json.shtml?city=' 免费用户每天最多调用2000次，调用过多会报错
#     建议在树莓派或者服务器上跑
 
import time
import random
import requests
from wxpy import *
 
def get_html(url,data=None):
    #模拟浏览器来获取网页的html代码
    header={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'
    }
    #设定超时时间，防止被网站认为是爬虫
    timeout=random.choice(range(80,180))
    while True:
        try:
            rep=requests.get(url,headers=header,timeout=timeout)
            rep.encoding="utf-8"
            if rep.text[2] != 's':#该api调用时有失败的可能，一个简单的判断调用是否成功
                break
        except socket.timeout as e:
            print("3:",e)
            time.sleep(random.choice(range(8,15)))
 
        except socket.error as e:
            print("4:",e)
            time.sleep(random.choice(range(20,60)))
        except http.client.BadStatusLine as e:
            print("5:",e)
            time.sleep(random.choice(range(30,80)))
 
        except http.client.IncompleteRead as e:
            print("6:",e)
            time.sleep(random.choice(range(5,15)))
 
 
    result=''
    temp=rep.text
    print (rep.text)
    index1 = temp.find('forecast')
    index_sunrise = temp.find('sunrise', index1)
    index_sunset = temp.find('sunset', index1)
    index_high = temp.find('high', index1)
    index_low = temp.find('low', index1)
    index_city = temp.find('city')
    index_count = temp.find('count')
    index_type = temp.find('type', index1)
    index_notice = temp.find('notice', index1)
 
    result = result+ '今日天气预报' + '\n' + '日期:' + temp[index1 + 20:index_sunrise - 3] \
             + '城市:' + temp[index_city + 7:index_count - 3] + '\n' \
             + '最高温度:' + temp[index_high + 9:index_low - 3] + ' 最低温度:' + temp[index_low + 9:index_sunset - 3] + '\n' \
             + '日出时间:' + temp[index_sunrise + 10:index_high - 3] + ' 日落时间:' + temp[index_sunset + 9:index_sunset + 14] + '\n' \
             + '天气类型:' + temp[index_type + 7:index_notice - 3] + '\n' \
             + temp[index_notice + 9:temp.find('}', index_notice) - 1]
 
    # print(datetime.datetime.now())
    # print('今日天气预报')
    # print('日期:' + temp[index1 + 20:index_sunrise - 3])
    # print('城市:' + temp[index_city + 7:index_count - 3])
    # print('最高温度:' + temp[index_high + 9:index_low - 3] + ' 最低温度:' + temp[index_low + 9:index_sunset - 3])
    # print('日出时间:' + temp[index_sunrise + 10:index_high - 3] + ' 日落时间:' + temp[index_sunset + 9:index_sunset + 14])
    # print('天气类型:' + temp[index_type + 7:index_notice - 3])
    # print(temp[index_notice + 9:temp.find('}', index_notice) - 1])
 
    return result
 
def auto_send(): #unix时间戳设定为每天早上7：30分自动发送消息
    while True:
        time_now = int(time.time())
        if (time_now - 1527204600) % 86400 == 0:
            url = 'https://www.sojson.com/open/api/weather/json.shtml?city=%E6%9D%AD%E5%B7%9E'  # 杭州的天气
            html = get_html(url)
            print(html)
            bot.self.send(html) #选择对象发送消息
            time.sleep(86000)
 
 
if __name__ == "__main__":
 
    # url ='https://www.sojson.com/open/api/weather/json.shtml?city=%E6%9D%AD%E5%B7%9E' #杭州的天气
    # html = get_html(url)
    # print (html)
    tuling = Tuling(api_key='')
    bot = Bot(cache_path=True)
    myself = bot.self
    bot.enable_puid('wxpy_puid.pkl')
    auto_send()
 
    bot.join()
    #print (':D')
