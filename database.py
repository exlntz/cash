import pandas as pd
import datetime
import json

from openpyxl.chart.series import attribute_mapping



result = pd.read_csv("telemi_events.csv")
event_type=result['EventType'].tolist()
time=result['Timestamp'].tolist()
AtmID=result['DeviceID'].tolist()
value=result['Value'].tolist()
first_time=list(map(int,time[0][0:10].split('-')))
start_date=datetime.date(first_time[0],first_time[1],first_time[2])
errors_list=[]
data={''}

# for x in value:
#     if ('ОШИБКА' or 'НЕ РАБОТАЕТ') in x.upper():
#         errorslist.append(x)
# print(errorslist)

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




print(weekindexcount(338,time, int(start_date.weekday())))
last=0
lastcount=0
errorlst=[]
for i in event_type:

    if "ОШИБКА" in i.upper():
        last=lastcount
        errorlst.append(i)
    lastcount+=1
print(set(errorlst))

k=0
week=1
while k<lastcount:
    print("------   ------\n-----------\n----------Ошибки за неделю---------------\n----------------------\n---------------------------")
    stopcount=weekindexcount(k,time, start_date.weekday())
    weeklist=[]
    for item in event_type[k: stopcount]:
        if k>=stopcount:
            break
        if "ОШИБКА" in item.upper():
            #print(event_type[k], time[k], AtmID[k], k,)
            with open('bankomat_data.json', 'a', encoding='utf-8') as file:
                file.write(json.dumps({('неделя '+str(week)):({AtmID[k]: event_type[k]})}, indent=4, ensure_ascii=False))
            print({AtmID[k]:event_type[k]})
            firsttime = list(map(int, time[k][0:10].split('-')))
        k+=1
    start_date=datetime.date(firsttime[0],firsttime[1],firsttime[2])
    week+=1
