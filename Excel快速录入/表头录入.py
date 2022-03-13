import csv
#调用csv模块
with open('target.csv', 'a', newline='') as csvfile:
#调用open()函数打开csv文件，传入参数：文件名“assets.csv”、追加模式“a”、newline=''。
    writer = csv.writer(csvfile, dialect='excel')
    # 用csv.writer()函数创建一个writer对象。
    header=['id(aid)', 'coins', 'play', 'video_review', '排行']
    writer.writerow(header)
    #用writerow()函数将表头写进csv文件里