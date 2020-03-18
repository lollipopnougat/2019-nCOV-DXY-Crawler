import time
import requests as req
import datetime
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as mdate
import json


class point:
    date_list = []
    conf_list = []
    susp_list = []
    cure_list = []
    dead_list = []


def get_info_json():
    url = 'https://lab.isaaclin.cn/nCoV/api/overall?latest=0'
    ua = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    res = req.get(url, headers=ua)
    res.encoding = res.apparent_encoding
    #print(res.text)
    return json.loads(res.text)['results']


def get_data(js):
    data = point()
    #last = datetime.datetime.fromtimestamp(js[len(js) - 1]['updateTime'] / 1000)
    last = datetime.datetime.fromtimestamp(js[0]['updateTime'] / 1000 + 43200)
    for i in js:
        ltime = datetime.datetime.fromtimestamp(i['updateTime'] / 1000)
        if ltime.date() == last.date() and last.hour - ltime.hour < 12:
            continue
        data.date_list.append(mdate.date2num(ltime))
        data.conf_list.append(i['confirmedCount'])
        data.cure_list.append(i['curedCount'])
        data.susp_list.append(i['suspectedCount'])
        data.dead_list.append(i['deadCount'])
        last = ltime

    data.conf_list.reverse()
    data.cure_list.reverse()
    data.date_list.reverse()
    data.susp_list.reverse()
    data.dead_list.reverse()
    return data


#.strftime('%Y-%m-%d %H:%M:%S')


def show_plt(dat, mode=0):
    target = None
    titlep = ''
    axt = ''
    if mode == 0:
        target = dat.conf_list
        titlep = '全国新冠确诊统计图'
        axt = '感染人数'
    elif mode == 1:
        target = dat.susp_list
        titlep = '全国新冠疑似统计图'
        axt = '疑似感染人数'
    elif mode == 2:
        target = dat.cure_list
        titlep = '全国新冠治愈统计图'
        axt = '治愈人数'
    elif mode == 3:
        target = dat.dead_list
        titlep = '全国新冠死亡统计图'
        axt = '死亡人数'
    font = {'family': 'MicroSoft YaHei', 'weight': 'light', 'size': 12}
    matplotlib.rc("font", **font)
    fig = plt.figure(figsize=(16, 10), dpi=80)
    fig.canvas.set_window_title('全国疫情统计图')
    ax1 = fig.add_subplot(1, 1, 1)
    plt.plot(dat.date_list, target, linewidth=2, marker='o', markersize=6)
    ax1.xaxis.set_major_formatter(
        mdate.DateFormatter('%Y-%m-%d %H:%M'))  #设置时间标签显示格式
    plt.xticks(dat.date_list)
    fig.autofmt_xdate(rotation=45)
    plt.xlabel('时间')
    plt.ylabel(axt)
    plt.title(titlep)
    plt.grid()
    plt.show()
    input(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +
          ': 窗体关闭，任意键继续')


print('感谢https://lab.isaaclin.cn/nCoV/ 提供的Api')
print('design by lnp: https://github.com/lollipopnougat')
print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': 从丁香园获取数据...')
jdata = get_info_json()
print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': 获取到数据')
print('准备解析...')
res = get_data(jdata)
print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': 解析完成')
print('1: 全国新冠确诊人数折线图\n2: 全国新冠疑似人数折线图\n3: 全国新冠治愈人数折线图\n4: 全国新冠死亡人数折线图\n0: 退出')

while (True):
    cmd = input('选择要显示的图: ')
    if cmd == '1':
        print('准备显示...')
        show_plt(res, 0)
    elif cmd == '2':
        print('准备显示...')
        show_plt(res, 1)
    elif cmd == '3':
        print('准备显示...')
        show_plt(res, 2)
    elif cmd == '4':
        print('准备显示...')
        show_plt(res, 3)
    elif cmd == '0':
        print('准备退出·...')
        break
    else:
        print('输入有误！')
