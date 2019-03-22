# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 23:16:30 2019

@author: THINK
"""
import pandas as pd
import csv


def todataframe(file:str) -> pd.core.frame.DataFrame:
    try:
        with open(file,'r') as f:
            columns = len(f.readline().split(' '))            #获取一行的总列数
            TranInfo = pd.read_csv(f,header=None,names=[i for i in range(columns)])    #将数据集当作csv文件转为DataFram对象
            
            interested_columns = {1,2,19,20,3,10,11,12,7,8,9,21,22,31,32}              #标出感兴趣的列
            drop_columns = set(range(columns)).difference(interested_columns)          #标记不感兴趣的列
            TranInfo.drop(labels=drop_columns,axis=1,inplace=True)                     #除去不感兴趣的列
            return TranInfo                                                            #返回感兴趣列的DataFrame数据类型
    except Exception as reason:
        print(reason)
    finally:
        pass
    
def time_insert(file:str):
    line_pre = ''
    time_interval = pd.to_timedelta('0 days 00:00:00.5')
    time_point1 = pd.to_datetime('21:00:00.0',format='%H:%M:%S.%f')
    time_middle = pd.to_datetime('00:00:00.0',format='%H:%M:%S.%f')
    time_point2 = pd.to_datetime('01:00:00.0',format='%H:%M:%S.%f')
    time_point3 = pd.to_datetime('09:00:00.0',format='%H:%M:%S.%f')
    time_point4 = pd.to_datetime('10:15:00.0',format='%H:%M:%S.%f')
    time_point5 = pd.to_datetime('10:30:00.0',format='%H:%M:%S.%f')
    time_point6 = pd.to_datetime('11:30:00.0',format='%H:%M:%S.%f')
    time_point7 = pd.to_datetime('13:30:00.0',format='%H:%M:%S.%f')
    time_point8 = pd.to_datetime('15:00:00.0',format='%H:%M:%S.%f')
    time_zone = ((time_point1,time_middle),(time_middle,time_point2),(time_point3,time_point4),(time_point5,time_point6),(time_point7,time_point8))
    time_stat = 0
    zone_stat = 0

    with open(file,'r') as f1,open('result.csv','w',newline='') as f2:
        for line in f1:
            timestamp = line.split(' ')[19]
            milisecond = line.split(' ')[20]
            time = pd.to_datetime(timestamp+'.'+milisecond,format='%H:%M:%S.%f')
            if time_point1 <= time:
                time_stat = 0
            elif time_middle <= time <= time_point2:
                time_stat = 1
            elif time_point3 <= time <= time_point4:
                time_stat = 2
            elif time_point5 <= time <= time_point6:
                time_stat = 3
            elif time_point7 <= time <= time_point8:
                time_stat = 4
            else:
                time_stat = 5
                continue
            if(len(line_pre)):
                timestamp_pre = line_pre.split(' ')[19]
                milisecond_pre = line_pre.split(' ')[20]
                time_pre = pd.to_datetime(timestamp_pre+'.'+milisecond_pre,format='%H:%M:%S.%f')
                diff = time-time_pre
                insert_count = int(diff.delta/500000000)
                
                if time_zone[time_stat-1][0] <= time_pre <= time_zone[time_stat-1][1]:
                    insert_count = int((time_zone[time_stat-1][1]-time_pre).delta/500000000) + 1
                    zone_stat = 1
                    
                f2.write(line_pre)
                csvwriter = csv.writer(f2,delimiter=' ',lineterminator='', quoting=csv.QUOTE_MINIMAL)
                for _ in range(insert_count-1):
                    time_pre += time_interval
                    miliseconds = int(time_pre.microsecond / 1000)
                    time_list = line_pre.split(' ')
                    time_list[19] = time_pre.ctime().split(' ')[4]
                    time_list[20] = str(miliseconds)
                    csvwriter.writerow(time_list)
                line_pre = line
                if zone_stat:
                    pass 
            else:
                line_pre = line
        f2.write(line)
            
if __name__ == '__main__':
    time_insert(r'C:\Users\THINK\Documents\python_test\newgaytest\al1901')
