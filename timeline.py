import json
import numpy as np
from os import listdir
import os
# 只允許讀取 json
ALLOWED_PICTURE = set(['json'])
threshold = 0.5
# 篩選副檔名
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_PICTURE

# 篩選副檔名
def allowed_file_Week(filename , day):
    return '.' in filename and int(filename.rsplit('.', 1)[0].split(" ")[1]) == day

def getEveryDayTimeline(dirPath):
    # 取得檔案列表
    if dirPath == "":
        files = listdir(os.getcwd())
    else:
        files = listdir(dirPath)
    
    # 建立一天有 86400 秒的  陣列為 timeline
    timelineEveryDay = np.zeros((86401))
    count = 1
    for fileName in files:
        print("start: "+str(fileName))
        if allowed_file(fileName) :
            with open(fileName, mode="r") as file:
                data=json.load(file)
            
            # 將時間紀錄換算為以秒數為單位
            for x in data:
                f=data[x]["from"]
                t=data[x]["to"]
                # 將 from 的時間紀錄做換算
                f=str(f)
                hourf=int(f[0:2])*3600
                minf=int(f[3:5])*60
                secf=int(f[6:])
                f=(hourf+minf+secf)
                # 將 to 的時間紀錄做換算
                t=str(t)
                hourt=int(t[0:2])*3600
                mint=int(t[3:5])*60
                sect=int(t[6:])
                t=(hourt+mint+sect)
                # 以每秒紀錄;0表示沒有在使用手機的時間，1 為有在使用手機的時間
                timelineEveryDay[f-1:t] += 1.0 * (count / 1596)
            count += 1
    print(count)
    return timelineEveryDay
        
def getWeekTimeline(dirPath , day):
 # 取得檔案列表
    if dirPath == "":
        files = listdir(os.getcwd())
    else:
        files = listdir(dirPath)
    
    # 建立一天有 86400 秒的 int 陣列為 timeline
    timelineWeek = np.zeros((86401))
    countWeek = 1
    for fileName in files:
        if allowed_file(fileName) and allowed_file_Week(fileName , day) :
            print("start: "+str(fileName))
            with open(fileName, mode="r") as file:
                data=json.load(file)
            
            # 將時間紀錄換算為以秒數為單位
            for x in data:
                f=data[x]["from"]
                t=data[x]["to"]
                # 將 from 的時間紀錄做換算
                f=str(f)
                hourf=int(f[0:2])*3600
                minf=int(f[3:5])*60
                secf=int(f[6:])
                f=(hourf+minf+secf)
                # 將 to 的時間紀錄做換算
                t=str(t)
                hourt=int(t[0:2])*3600
                mint=int(t[3:5])*60
                sect=int(t[6:])
                t=(hourt+mint+sect)
                timelineWeek[f-1:t] += 1.0 * (countWeek / 28) 
            countWeek += 1
            print(countWeek)


    return timelineWeek
# 計算結果
def predictUsePhone(timelineList):
    timelineNextWeek = []

    for i in range(7):
        timelineNextWeek.append(np.zeros((86401)))
        for second in range(86400):
            ratio = timelineList[0][second] * 0.4 + timelineList[i+1][second] * 0.6
            if ratio > threshold :
                print("y:" + str(ratio))
                ratio = 1

            else:
                ratio = 0
            timelineNextWeek[i][second] = ratio
    
    return timelineNextWeek

def getTime(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d" % (h, m, s)

def outputJson(timeline , fileName):
    count = 0
    outputData = {}

    for i in range(86400):
        if timeline[i] == 0 and timeline[i+1]==1 :
            fromData = getTime(i+1)
        elif timeline[i] == 1 and timeline[i+1]==0 :
            toData = getTime(i)
            outputData.update({str(count) : {"from" : fromData , "to" : toData}}) 
            count += 1
        else:
            continue
    with open(fileName + '.json', 'w') as output:
        json.dump(outputData, output, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    # 輸入 json 檔案以做讀取
    dirPath=input("請輸入檔案路徑:")
    timeLineList = []
    # 取得8周統計之陣列
    everyDayTimeline = getEveryDayTimeline(dirPath)
    timeLineList.append(everyDayTimeline)
    for i in range(7):
        timeLineList.append(getWeekTimeline(dirPath , i + 1))
    result = predictUsePhone(timeLineList)
    for i in range(7):
        outputJson( result[i] , "d " + str(i + 1))
