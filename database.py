import pandas as pd
import datetime
import json

from openpyxl.chart.series import attribute_mapping



result = pd.read_csv("csvfiles/telemi_events.csv")
event_type=result['EventType'].tolist()
time=result['Timestamp'].tolist()
AtmID=result['DeviceID'].tolist()
value=result['Value'].tolist()
details=result['Details'].tolist()
first_time=list(map(int,time[0][0:10].split('-')))
start_date=datetime.date(first_time[0],first_time[1],first_time[2])
errors_list=[]
data={''}

date=datetime.datetime.strptime(time[0], '%Y-%m-%d %H:%M:%S')
date2=datetime.datetime.strptime(time[1], '%Y-%m-%d %H:%M:%S')
date3=date=datetime.datetime.strptime(time[2], '%Y-%m-%d %H:%M:%S')


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
def monthindexcount(index0,list, date0):
    k=0
    month0=list[index0:][0][5:7]
    a=list[index0:][0][8:10]
    if str(int(month0)) in '1357810' or str(int(month0)) in '12':
        raznday=31-date0
    elif str(int(month0)) in '246911':
        raznday=30-date0
    else:
        raznday = 28 - date0
    for s in list:
        if int(a)==int(s[5:7])-raznday:
            break
        else:
            k+=1
    return k

print()
# for s in time:
#     print(s, s[8:10],k)
#     k+=1

all_value=set(value)
all_errors=[]
for status in all_value:
    if str(status).isdigit()==0:
        if len(str(status).split())>1:
            all_errors.append(status)


all_errors.sort()
non_critical_errors=[]
critical_errors=[]
incass_critical_errors=[]
service_critical_errors=[]
incass_non_critical_errors=[]
service_non_critical_errors=[]
non_critical_errors.extend(all_errors[20:23])
non_critical_errors.extend(all_errors[24:30])
non_critical_errors.extend(all_errors[31:33])
non_critical_errors.extend(all_errors[35:39])
non_critical_errors.append(all_errors[12])
critical_errors.extend((all_errors)[8:10])
critical_errors.extend(all_errors[13:19])
critical_errors.append(all_errors[33])
critical_errors.append(all_errors[39])
critical_errors.append(all_errors[4])

incass_critical_errors.append(critical_errors[0])
incass_critical_errors.append(critical_errors[6])

service_critical_errors.append(critical_errors[1])
service_critical_errors.extend(critical_errors[3:6])
service_critical_errors.extend(critical_errors[7:])

incass_non_critical_errors.append(non_critical_errors[0])

service_non_critical_errors.extend(non_critical_errors[1:])

print(non_critical_errors)
print()
print(incass_non_critical_errors)
print()
print(service_non_critical_errors)
print()
print(incass_critical_errors)
print()
print(all_errors)
print()
print(critical_errors)
print()
print(service_critical_errors)



print(weekindexcount(338,time, int(start_date.weekday())))
last=0
lastcount=0
errorlst=[]
for i in event_type:

    if "ОШИБКА" in i.upper():
        last=lastcount
        errorlst.append(i)
    lastcount+=1
# print(set(errorlst))



k=0
week=1
with open('jsons/atm_errors_data.json', 'w', encoding='utf-8') as file:
    file.write('')


monthdata={}
weekEndData={}
monthstopcount=monthindexcount(0, time, int(start_date.weekday()))
monthcount=1
while k<lastcount:
    if k>monthstopcount:
        monthdata[('month'+str(monthcount))]=weekEndData
        weekEndData={}
        monthcount+=1
        monthstopcount=monthindexcount(k, time, start_date.weekday())
    stopcount_week=weekindexcount(k,time, start_date.weekday())
    weekdata= {}

    for item in event_type[k: stopcount_week]:
        if k>=stopcount_week:
            break
        if "ОШИБКА" in item.upper():
            weekdata[AtmID[k]]=event_type[k]
            firsttime = list(map(int, time[k][0:10].split('-')))
        k+=1
    key='неделя '+str(week)

    weekEndData[key]=weekdata
    start_date=datetime.date(firsttime[0],firsttime[1],firsttime[2])
    week+=1
monthdata[('month'+str(monthcount))]=weekEndData
print(monthdata)
with open('jsons/atm_errors_data.json', 'a', encoding='utf-8') as file:
    file.write(json.dumps(monthdata, indent=4, ensure_ascii=False))
#print(all_errors)
repair_needs={}
# critical_errorsDATA={}
# errorsDATA={}
# non_errorsDATA={}
critical_errorsLIST=[]
errorsLIST=[]
non_errorsLIST=[]
index=0
#r


for event in value:
    deltaDATA={}
    if event in all_errors:
        deltaDATA['id'] = AtmID[index]
        deltaDATA['date'] = time[index]
        deltaDATA['error'] = value[index]
        if value[index] in critical_errors:
            critical_errorsLIST.append(deltaDATA)

        elif value[index] in non_critical_errors:
            errorsLIST.append(deltaDATA)
        else:
            non_errorsLIST.append(deltaDATA)
    index+=1
# print(errorsLIST)
# print(non_errorsLIST)
# print(critical_errorsLIST)
repair_needs['critical_errors']=critical_errorsLIST
repair_needs['errors']=errorsLIST
repair_needs['non_errors']=non_errorsLIST
with open('jsons/atm_data.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(repair_needs, indent=4, ensure_ascii=False))
print(details[4769])


AtmStatus={}
one_more_index=0
for event in value:
    if str(event).isdigit():
        AtmStatus[AtmID[one_more_index]]={'lvl' : 0 , 'askfor' : 'None'}
    else:
        if event in incass_critical_errors:
            AtmStatus[AtmID[one_more_index]]={'lvl' : 2 , 'askfor' : 'incass'}
        elif event in service_critical_errors:
            AtmStatus[AtmID[one_more_index]]={'lvl' : 2 , 'askfor' : 'service'}
        elif event in incass_non_critical_errors:
            AtmStatus[AtmID[one_more_index]] = {'lvl': 1, 'askfor': 'incass'}
        elif event in service_non_critical_errors:
            AtmStatus[AtmID[one_more_index]]={'lvl' : 1 , 'askfor' : 'service'}
        else:
            AtmStatus[AtmID[one_more_index]] = {'lvl' : 0 , 'askfor' : 'None'}
    one_more_index+=1
sorted_AtmStatus=sorted(AtmStatus.items())
AtmStatus={}
for Atm in sorted(AtmID):
    for key, value in sorted_AtmStatus:
        if Atm==key:
            AtmStatus[key]=value
with open('jsons/AtmStatus.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(AtmStatus, indent=4, ensure_ascii=False))


AtmWorkingTimePercent={}
for Atm in sorted(AtmID):
    flag=0
    i=0
    count_OnStatus=0
    count_OffStatus=0
    date_start=''
    date_end=''
    for event in details:
        if event[:31]=='Состояние устройства Банкомат'+Atm[8:] and flag==0:
            date_start=datetime.datetime.strptime(time[i], '%Y-%m-%d %H:%M:%S')
            flag=1
        elif event[:31]=='Состояние устройства Банкомат'+Atm[8:] and flag==1:
            date_end=datetime.datetime.strptime(time[i], '%Y-%m-%d %H:%M:%S')
            delta=(date_end-date_start).total_seconds()
            count_OnStatus=count_OnStatus+delta
            flag=2
        if event[:31]=='Состояние устройства Банкомат'+Atm[8:] and flag==2:
            date_start=datetime.datetime.strptime(time[i], '%Y-%m-%d %H:%M:%S')
            delta = (date_start - date_end).total_seconds()
            count_OffStatus=count_OffStatus+delta
            flag=1
        i+=1
    if (count_OnStatus+count_OffStatus)!=0:
        AtmWorkingTimePercent[Atm]={'timeON' : count_OnStatus, 'timeOFF' : count_OffStatus, 'Percent' : round((count_OnStatus/(count_OnStatus+count_OffStatus))*100)}
    else:
        AtmWorkingTimePercent[Atm] = {'Percent': 100}


with open('jsons/AtmWorkingTimePercent.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(AtmWorkingTimePercent, indent=4, ensure_ascii=False))
