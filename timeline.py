import json
import numpy as np
from os import listdir
import os
# 只允許讀取 json
ALLOWED_PICTURE = set(['json'])

# 篩選副檔名
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_PICTURE

def getEveryDayTimeline(dirPath):
    # 取得檔案列表
    if dirPath == "":
        files = listdir(os.getcwd())
        print(os.getcwd())
    else:
        files = listdir(dirPath)
    
    timeline = np.zeros((86400), dtype=int)
    for fileName in files:
        if allowed_file(fileName) :
            with open(fileName, mode="r") as file:
                data=json.load(file)
            # 建立一天有 86400 秒的 int 陣列為 timeline
            
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
                timeline[f-1:t] += int(1)
        return timeline
        

if __name__ == '__main__':
    # 輸入 json 檔案以做讀取
    dirPath=input("請輸入檔案路徑:")
    # 取得8周統計之陣列
    everyDayTimeline = getEveryDayTimeline(dirPath)
    # 輸出方便查看，可以不用
    np.savetxt("result", everyDayTimeline)