import requests as req
from bs4 import BeautifulSoup as bs
import re
import json
import csv
import datetime
import matplotlib.pyplot as plt
import matplotlib

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
    prov_list = []
    conf_list = []
    for i in js:
        print('%s 确诊数： %d， 治愈数： %d， 死亡数: %d' %
              (i['provinceName'], i['confirmedCount'], i['curedCount'],
               i['deadCount']))
        prov_list.append(i['provinceName'])
        conf_list.append(i['confirmedCount'])

    print('全国确诊： %d， 疑似数： %d， 治愈数： %d， 死亡数： %d， 重症数： %d' %
          (al['confirmedCount'], al['suspectedCount'], al['curedCount'],
           al['deadCount'], al['seriousCount']))

    font = {
        'family': 'MicroSoft YaHei',
        'weight': 'light',
        'size': 10
        }
    matplotlib.rc("font", **font)
    fig = plt.figure(figsize=(10, 9),dpi=80)
    fig.canvas.set_window_title('全国各省感染人数占比')
    plt.axes(aspect=1)
    plt.pie(x=conf_list, labels=prov_list, autopct='%3.1f %%',pctdistance=1.2,labeldistance=1.0)
    plt.title('全国各省感染人数占比')
    plt.legend()
    plt.show()


    input('任意键继续')


if __name__ == "__main__":
    task()
