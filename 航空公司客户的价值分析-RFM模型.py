import pandas as pd
import matplotlib.pyplot as plt
import warnings

# 关闭警告显示
warnings.filterwarnings("ignore")

# 读取【air_new_data.xlsx】工作簿的数据
airline_data = pd.read_excel('air_new_data.xlsx')
# 查看数据的前 10 行信息
airline_data.head(10)

# 查看数据是否有空值
airline_data.isna()
# 去除“最近一次间隔天数”为空的记录
airline_notnull = airline_data.dropna(subset=['最近一次间隔天数'])
# 去除“近2年乘机次数”为空的记录
airline_notnull = airline_notnull.dropna(subset=['近2年乘机次数'])
# 去除“消费金额”为空的记录
airline_notnull = airline_notnull.dropna(subset=['消费总金额'])

# 查看是否有重复值
airline_notnull[airline_notnull.duplicated()]

# 查看数据描述性统计的信息
airline_notnull.describe()
# 只保留消费金额非零的记录，同时去除年龄大于 100 的记录
airline = airline_notnull[airline_notnull['消费总金额'] != 0]
airline = airline[airline['年龄'] <= 100]

# 关键字段提取
airline = airline[['会员卡号', '最近一次间隔天数', '近2年乘机次数', '近2年乘机金额']]
# 保存清洗后的数据
airline.to_excel('clean_dfile.xlsx', index=False)

# 创建画布
plt.figure(figsize=(6, 6)) 
# 获取 airline 的【最近一次间隔天数】列数据
x = airline['最近一次间隔天数'].sort_values()
# 获取 airline 的索引
y = airline.index

# 绘制折线图
plt.plot(x,y) 

# 定义函数按照区间划分标记 R 值
def caculate_r(s):
    if s <= 140:
        return 5
    elif s <= 280:
        return 4
    elif s <= 420:
        return 3
    elif s <= 560:
        return 2
    else:
        return 1

# 标记 R 值
airline['R评分'] = airline['最近一次间隔天数'].agg(caculate_r)

# 创建画布
plt.figure(figsize=(6, 6)) 
# 获取 airline 的【近2年乘机次数】列数据
x = airline['近2年乘机次数'].sort_values()
# 获取 airline 的索引
y = airline.index

# 绘制折线图
plt.plot(x,y) 
plt.show()

# 定义函数按照区间划分标记 F 值
def caculate_f(s):
    if s <= 4:
        return 1
    elif s <= 7:
        return 2
    elif s <= 10:
        return 3
    elif s <= 20:
        return 4
    else:
        return 5

# 标记 F 值
airline['F评分'] = airline['近2年乘机次数'].agg(caculate_f)

# 创建画布
plt.figure(figsize=(6, 6)) 
# 获取 airline 的【近2年乘机金额】列数据
x = airline['近2年乘机金额'].sort_values()
# 获取 airline 的索引
y = airline.index

# 绘制折线图
plt.plot(x,y) 

# 定义函数按照区间划分标记 M 值
def caculate_m(s):
    if s <= 5000:
        return 1
    elif s <= 10000:
        return 2
    elif s <= 15000:
        return 3
    elif s <= 20000:
        return 4
    else:
        return 5
    
# 标记 M 值
airline['M评分'] = airline['近2年乘机金额'].agg(caculate_m)

# 计算R评分、F评分、M评分的平均数
r_avg = airline['R评分'].mean()
f_avg = airline['F评分'].mean()
m_avg = airline['M评分'].mean()

print('R评分的均值为：{}，F评分的均值为{},M评分的均值为{}'.format(r_avg, f_avg, m_avg))

# 将R评分、F评分、M评分 的数据分别与对应的平均数做比较
airline['R评分'] = (airline['R评分'] > r_avg) * 1
airline['F评分'] = (airline['F评分'] > f_avg) * 1
airline['M评分'] = (airline['M评分'] > m_avg) * 1

# 拼接R评分、F评分、M评分
rfm_score = airline['R评分'].astype(str) + airline['F评分'].astype(str) + airline['M评分'].astype(str)

# 定义字典标记 RFM 评分档对应的用户分类名称
transform_label = {
    '111':'重要价值用户',
    '101':'重要发展用户',
    '011':'重要保持用户',
    '001':'重要挽留用户',
    '110':'一般价值用户',
    '100':'一般发展用户',
    '010':'一般保持用户',
    '000':'一般挽留用户'
}
# 将RFM评分替换成具体的客户类型
airline['客户类型'] = rfm_score.replace(transform_label)

# 对【客户类型】进行分组，再聚合【会员卡号】计算数量
customer_data = airline.groupby('客户类型')['会员卡号'].count()
# 图像文本中文化
plt.rcParams['font.sans-serif'] = ['SimHei']
# 创建画布，大小为 10x10
plt.figure(figsize=(10, 10)) 
# 绘制柱状图
plt.bar(customer_data.index, customer_data)
# 设置 x 轴的标签
plt.xlabel('客户类型', fontsize=12)
# 设置 y 轴的标签
plt.ylabel('人数', fontsize=12)
# 设置柱状图的标题
plt.title('不同客户的数量分布', fontsize=16)

plt.savefig('航空公司客户价值分析-RFM模型.png')