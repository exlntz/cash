import pandas as pd
import datetime
#вывод за неделю не работает,пофикшу позже
result = pd.read_csv("telemi_events.csv")
eventtype=result['EventType'].tolist()
time=result['Timestamp'].tolist()
firsttime=list(map(int,time[0][0:10].split('-')))

startdate=datetime.date(firsttime[0],firsttime[1],firsttime[2])
print(startdate.weekday())
for i in range(0,len(time),7):
    print("Ошибки за неделю")
    for item in eventtype[i:i+7]:
        if "ОШИБКА" in item.upper():
             print(item, time[(eventtype.index(item))])
