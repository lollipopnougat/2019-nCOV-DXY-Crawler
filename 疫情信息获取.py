import requests as req
from bs4 import BeautifulSoup as bs
import re
import json
import csv
import datetime


url = 'https://ncov.dxy.cn/ncovh5/view/pneumonia_peopleapp'
header = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}

pat1 = re.compile('(\[[^\]]+?\])')
pat2 = re.compile('(\{[^\}\{]+?\})')


def task():
    res = req.get(url=url, headers=header)

    print(res.status_code)
    res.encoding = res.apparent_encoding

    soup = bs(res.text, 'html.parser')
    dat1 = str(soup.findAll(id='getListByCountryTypeService1')[0].string)
    dat2 = str(soup.findAll(id='getStatisticsService')[0].string)
    st1 = pat1.findall(dat1)[0]
    st2 = pat2.findall(dat2)[0]
    js = json.loads(st1)
    al = json.loads(st2)
    for i in js:
        print('%s 确诊数： %d， 治愈数： %d， 死亡数: %d' %
              (i['provinceName'], i['confirmedCount'], i['curedCount'],
               i['deadCount']))

    print('全国确诊： %d， 疑似数： %d， 治愈数： %d， 死亡数： %d， 重症数： %d' %
          (al['confirmedCount'], al['suspectedCount'], al['curedCount'],
           al['deadCount'], al['seriousCount']))



    input()


if __name__ == "__main__":
    task()
