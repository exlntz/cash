import pandas as pd
import datetime
#вывод за неделю не работает,пофикшу позже
result = pd.read_csv("telemi_events.csv")
eventtype=result['EventType'].tolist()
time=result['Timestamp'].tolist()
firsttime=list(map(int,time[0][0:10].split('-')))
startdate=datetime.date(firsttime[0],firsttime[1],firsttime[2])
print(startdate)
def weekindexcount(index0,list, date0):
    k=0
    a=list[index0:][0][8:10]
    raznday=7-date0
    for s in list:
        if int(a)==int(s[8:10])-raznday:
            break
        else:
            k+=1
    return k
k=0

# for s in time:
#     print(s, s[8:10],k)
#     k+=1




print(weekindexcount(338,time, int(startdate.weekday())))
last=0
lastcount=0
for i in eventtype:

    if "ОШИБКА" in i.upper():
        last=lastcount
    lastcount+=1
print(last)

#print(eventtype[6,8])
k=0
while k<=lastcount:
    print("Ошибки за неделю")
    stopcount=weekindexcount(k,time, startdate.weekday())

    for item in eventtype:
        if k>=stopcount:
            break
        if "ОШИБКА" in item.upper():
            print(eventtype[k], time[k], k)
            firsttime = list(map(int, time[k][0:10].split('-')))
        k+=1
    startdate=datetime.date(firsttime[0],firsttime[1],firsttime[2])
    k=weekindexcount(k,time, startdate.weekday())