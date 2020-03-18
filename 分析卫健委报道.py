import re

cur_con = re.compile('现有确诊病例(\d+)例')
ser_cou = re.compile('重症病例(\d+)例')
cur_con = re.compile('治愈出院病例(\d+)例')
all_dea = re.compile('累计死亡病例(\d+)例')
cur_sus = re.compile('现有疑似病例(\d+)例')
all_con = re.compile('累计报告确诊病例(\d+)例')
while True:
    st = input()

    ccc = cur_con.findall(st)[0]
    scc = ser_cou.findall(st)[0]
    ccuc = cur_con.findall(st)[0]
    adc = all_dea.findall(st)[0]
    csc = cur_sus.findall(st)[0]
    acc = all_con.findall(st)[0]
    
    print(acc,csc,adc,ccuc,scc)

