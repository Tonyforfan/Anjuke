# -*- coding:utf-8 -*-
'''  爬取安居客成都新房的信息，经Excel处理后可以看出成都的房价特征  '''  
import requests
import csv
import codecs
from bs4 import BeautifulSoup

class AnjukeSpider:
    def __init__(self):
        self.startUrl = 'http://cd.fang.anjuke.com/loupan/all/'
        self.headers = {
             'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
        }
        self.filepath = r'C:\Users\DELL\Desktop\anjuke.csv'

    def parseHouseInfo(self,url):
        html = requests.get(url = url,headers = self.headers).text
        soup = BeautifulSoup(html,'html.parser')
        houseInfoList = soup.find('div',{'class':'key-list'}).findAll('div',{'class':'item-mod'})
        dataList = []
        for houseInfo in houseInfoList:
            try:
                name = houseInfo.find('a',{'class':'items-name'}).get_text().encode('utf-8')
                address = houseInfo.find('a',{'class':'list-map'}).get_text().encode('utf-8')
                price = houseInfo.find('div',{'class':'favor-pos'}).find('p').get_text().encode('utf-8')
                dataList.append([name,address,price])
            except:
                pass
        return dataList

    def saveHouseInfo(self):
        urlList = map(lambda x:self.startUrl + 'p' + str(x) + '/',range(62))
        with open(self.filepath,'wb') as writedata:
            writedata.write(codecs.BOM_UTF8) # 为了解决中文内容在写入csv文件时乱码的问题
            writer = csv.writer(writedata)
            writer.writerow(['楼盘名','地址','价格'])
            for url in urlList:
                data = self.parseHouseInfo(url)
                writer.writerows(data)
        writedata.close()

Spider = AnjukeSpider()
Spider.saveHouseInfo()
