import requests, bs4, openpyxl
import schedule
import time


def movie_spider():
        # 创建工作薄
    wb=openpyxl.Workbook()  
    # 获取工作薄的活动表
    sheet=wb.active 
    # 工作表重命名
    sheet.title='movies' 

    sheet['A1'] ='电影名'       # 加表头，给A1单元格赋值
    sheet['B1'] ='播放平台'     # 加表头，给B1单元格赋值
    sheet['C1'] ='上线天数'       # 加表头，给C1单元格赋值
    sheet['D1'] ='Id'

    headers={'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    url = 'http://piaofang.maoyan.com/dashboard/webHeatData?showDate=20201024&uuid=17558a884d4c8-0db41090c4f35f-c781f38-144000-17558a884d4c8&riskLevel=71&optimusCode=10&_token=eJxV0U1rwzAMBuD%2ForOW%2BNtOoIfCYHSww0q3S%2BnBabOkjDQlDftg7L9PFvFhJz2WX9nB%2BYFpc4JaIHy0E9QgC1E4QJhvUEsntNXeG0cF4fivV1lLQ830eg%2F1PugKvVKH1NjSei%2BtdhicOeBCRVQGU4FmQxHo5%2Flal%2BX1HMe3eOmKIY7f8VIcx6E8xVvfjHE6lZ9tc9e3caYvApocdmky0IFOUStohU4kqIC2Yji0gaEzBFqfIGnLMWjLMiRakyBChkWrGZThKwSNS4KvQgadIxgqQ6BJt%2FsQ0ASGQ%2BMZGo1jiAU%2BZLgMg8YyFBrDkAschTWDwophMnQCPcp7ehSqcalzXj%2FR%2F6Tk7dxdSO3j1%2B6l26zXD916%2B7xawe8fUGxyEg%3D%3D'
    res = requests.get(url, headers=headers)
    print(res.text)
    js=res.json()
    lists = js['dataList']['list']

    for item in lists:
        
        name=item['seriesInfo']['name']
        #adress=item['seriesInfo']['platformDesc']
        time=item['seriesInfo']['releaseInfo']
        seriesId=item['seriesInfo']['seriesId']
        try:
            adress =item['seriesInfo']['platformDesc']
                #查找评论
        except:
            adress = '无'
        sheet.append([name,adress,time,seriesId])  
        #print=(item['seriesInfo']['releaseInfo'])  
    wb.save('猫眼专业版.xlsx')


def job():
    print('开始一次任务')
    a=movie_spider
schedule.every(5).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)