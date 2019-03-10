#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- auther @icctw -*-
 
#tip: ��api  'https://www.sojson.com/open/api/weather/json.shtml?city=' ����û�ÿ��������2000�Σ����ù���ᱨ��
#     ��������ݮ�ɻ��߷���������
 
import time
import random
import requests
from wxpy import *
 
def get_html(url,data=None):
    #ģ�����������ȡ��ҳ��html����
    header={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'
    }
    #�趨��ʱʱ�䣬��ֹ����վ��Ϊ������
    timeout=random.choice(range(80,180))
    while True:
        try:
            rep=requests.get(url,headers=header,timeout=timeout)
            rep.encoding="utf-8"
            if rep.text[2] != 's':#��api����ʱ��ʧ�ܵĿ��ܣ�һ���򵥵��жϵ����Ƿ�ɹ�
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
 
    result = result+ '��������Ԥ��' + '\n' + '����:' + temp[index1 + 20:index_sunrise - 3] \
             + '����:' + temp[index_city + 7:index_count - 3] + '\n' \
             + '����¶�:' + temp[index_high + 9:index_low - 3] + ' ����¶�:' + temp[index_low + 9:index_sunset - 3] + '\n' \
             + '�ճ�ʱ��:' + temp[index_sunrise + 10:index_high - 3] + ' ����ʱ��:' + temp[index_sunset + 9:index_sunset + 14] + '\n' \
             + '��������:' + temp[index_type + 7:index_notice - 3] + '\n' \
             + temp[index_notice + 9:temp.find('}', index_notice) - 1]
 
    # print(datetime.datetime.now())
    # print('��������Ԥ��')
    # print('����:' + temp[index1 + 20:index_sunrise - 3])
    # print('����:' + temp[index_city + 7:index_count - 3])
    # print('����¶�:' + temp[index_high + 9:index_low - 3] + ' ����¶�:' + temp[index_low + 9:index_sunset - 3])
    # print('�ճ�ʱ��:' + temp[index_sunrise + 10:index_high - 3] + ' ����ʱ��:' + temp[index_sunset + 9:index_sunset + 14])
    # print('��������:' + temp[index_type + 7:index_notice - 3])
    # print(temp[index_notice + 9:temp.find('}', index_notice) - 1])
 
    return result
 
def auto_send(): #unixʱ����趨Ϊÿ������7��30���Զ�������Ϣ
    while True:
        time_now = int(time.time())
        if (time_now - 1527204600) % 86400 == 0:
            url = 'https://www.sojson.com/open/api/weather/json.shtml?city=%E6%9D%AD%E5%B7%9E'  # ���ݵ�����
            html = get_html(url)
            print(html)
            bot.self.send(html) #ѡ���������Ϣ
            time.sleep(86000)
 
 
if __name__ == "__main__":
 
    # url ='https://www.sojson.com/open/api/weather/json.shtml?city=%E6%9D%AD%E5%B7%9E' #���ݵ�����
    # html = get_html(url)
    # print (html)
    tuling = Tuling(api_key='')
    bot = Bot(cache_path=True)
    myself = bot.self
    bot.enable_puid('wxpy_puid.pkl')
    auto_send()
 
    bot.join()
    #print (':D')
