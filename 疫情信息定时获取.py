import requests as req
from bs4 import BeautifulSoup as bs
import re
import json
import csv
import datetime
import sched
import time

url = 'https://ncov.dxy.cn/ncovh5/view/pneumonia_peopleapp'
header = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}

pat1 = re.compile('(\[\{.+\])\}catch')
pat2 = re.compile('=\s?(\{.+)\}catch')


def task():
    res = req.get(url=url, headers=header)
    try:
        f = open("data.csv", 'r')
        f.close()
    except IOError:
        f = open("data.csv", 'w', newline='')
        f_csv = csv.writer(f)
        f_csv.writerow(['时间', '全国确诊数', '全国疑似数', '全国治愈数', '全国死亡数', '全国重症数'])
        f.close()

    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
          res.status_code)
    res.encoding = res.apparent_encoding

    soup = bs(res.text, 'html.parser')
    dat1 = str(soup.findAll(id='getAreaStat')[0].string)
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

    with open('data.csv', 'a', newline='') as file:
        f_csv = csv.writer(file)
        f_csv.writerow([
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            al['confirmedCount'], al['suspectedCount'], al['curedCount'],
            al['deadCount'], al['seriousCount']
        ])
        print('输出到文件 data.csv 成功')

    #input()


s = sched.scheduler(time.time, time.sleep)


def perform(inc):
    s.enter(inc, 0, perform, (inc, ))
    task()


def main(inc=1800):
    s.enter(0, 0, perform, (inc, ))
    s.run()


if __name__ == "__main__":
    t = int(input('输入两次获取的时间间隔(单位秒,数值>=60): '))
    if t < 60:
        t = 60
    main(t)
    #task()
