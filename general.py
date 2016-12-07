# -*- coding:utf-8 -*-

import requests
import csv
import codecs
from bs4 import BeautifulSoup

class AnjukeSpider:
    def __init__(self):
        self.startUrl = 'http://sh.fang.anjuke.com/loupan/all/'
        self.headers = {
             'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
        }
        self.filepath = r'C:\Users\DELL\Desktop\anjuke_bj.csv'

    def saveHouseInfo(self):
        url = self.startUrl
        pageNum = 1
        with open(self.filepath,'wb') as writedata:
            writedata.write(codecs.BOM_UTF8) # 为了解决中文内容在写入csv文件时乱码的问题
            writer = csv.writer(writedata)
            writer.writerow(['楼盘名','地址','价格'])
            print '正在爬取第%d页的信息' % pageNum
            pageNum += 1
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
            writer.writerows(dataList) # 写入第一页的内容
            # 判断有无下页
            nextPageInfo = soup.find('a',{'class':'next-page next-link'})
            while nextPageInfo: # 若存在下一页的信息就一直爬取下去
                url = nextPageInfo.get('href')
                print '正在爬取第%d页的信息' % pageNum
                pageNum += 1
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
                writer.writerows(dataList)
                nextPageInfo = soup.find('a',{'class':'next-page next-link'})
        writedata.close()

Spider = AnjukeSpider()
Spider.saveHouseInfo()
