#!/usr/bin/env python
# coding: utf-8

# In[1]:

import pandas as pd
import warnings

# 关闭警告显示
warnings.filterwarnings('ignore')

# 读取并查看【商品销售数据.xlsx】工作簿的数据
data=pd.read_excel('商品销售数据.xlsx',sheet_name='data')

data.head(10)

# In[2]:

# 清洗【用户 ID】列的缺失值
data = data.dropna(subset=['用户 ID'])
# 查看清洗后的数据基本信息总结
data.info()

# In[3]:

# 查找重复数据
data[data.duplicated()]

# In[4]:

# 删除重复值
data = data.drop_duplicates()
# 查找清洗后的数据是否存在重复数据
data[data.duplicated()]

# In[5]:

# 查看数据描述性统计的信息
data.describe()

# In[6]:

# 筛选【数量】列大于 0 的数据
data = data[(data['数量'] > 0)]
# 查看数据描述性统计的信息
data.describe()

# In[7]:

# 计算“总金额”
data['总金额'] = data['数量'] * data['价格']
data

# In[8]:

# 按【订单号】和【用户 ID】分组后，获取【发货日期】列的最大值和【总金额】列的总和
grouped_data = data.groupby(['订单号', '用户 ID'], as_index=False).agg({'发货日期': 'max', '总金额': 'sum'})
grouped_data.head(10)

# In[9]:

# 计算时间间隔  
today = '2012-01-01 00:00:00'
pd.to_datetime(today) - pd.to_datetime(grouped_data['发货日期'])

# In[10]:

# 计算时间间隔
today = '2012-01-01 00:00:00'
grouped_data['时间间隔'] = (pd.to_datetime(today) - pd.to_datetime(grouped_data['发货日期'])).dt.days
grouped_data

# In[11]:

# 按【用户 ID】分组后，获取【时间间隔】列的最小值、【订单号】列的数量，以及【总金额】列的总和
rfm_data = grouped_data.groupby('用户 ID', as_index=False).agg({'时间间隔': 'min', '订单号': 'count', '总金额': 'sum'})

# In[12]:

# 修改列名
rfm_data.columns = ['用户ID', '时间间隔', '总次数', '总金额']

# In[13]:

import matplotlib.pyplot as plt

# 设置中文显示字体
plt.rcParams['font.sans-serif'] = ['SimHei']

# 画 R 值（时间间隔）的折线图，便于后续对数据进行分组
plt.figure(figsize=(10, 8))
x = rfm_data['时间间隔'].sort_values()
y = rfm_data.index
plt.plot(x, y)


# In[14]:


# 定义函数按照区间划分 R 值
def caculate_r(s):
    if s <= 100:
        return 5
    elif s <= 200:
        return 4
    elif s <= 300:
        return 3
    elif s <= 400:
        return 2
    else:
        return 1


# In[15]:


# 对 R 值进行评分
rfm_data['R评分'] = rfm_data['时间间隔'].agg(caculate_r)
rfm_data


# In[16]:


# 画 F 值（总次数）的折线图，便于后续对数据进行分组
plt.figure(figsize=(10, 8))
x = rfm_data['总次数'].sort_values()
y = rfm_data.index
plt.plot(x, y)


# In[17]:


# 定义函数按照区间划分 F 值
def caculate_f(s):
    if s <= 5:
        return 1
    elif s <= 10:
        return 2
    elif s <= 15:
        return 3
    elif s <= 20:
        return 4
    else:
        return 5


# In[18]:


# 对 F 值进行评分
rfm_data['F评分'] = rfm_data['总次数'].agg(caculate_f)
rfm_data


# In[19]:


# 画 M 值（总金额）的折线图，便于后续对数据进行分组
plt.figure(figsize=(10, 8))
x = rfm_data['总金额'].sort_values()
y = rfm_data.index
plt.plot(x, y)


# In[20]:


# 定义函数按照区间划分 M 值
def caculate_m(s):
    if s <= 2000:
        return 1
    elif s <= 4000:
        return 2
    elif s <= 6000:
        return 3
    elif s <= 8000:
        return 4
    else:
        return 5


# In[21]:


# 对 M 值进行评分
rfm_data['M评分'] = rfm_data['总金额'].agg(caculate_m)
rfm_data


# In[22]:


# 计算 R评分、F评分、M评分的平均数
r_avg = rfm_data['R评分'].mean()
f_avg = rfm_data['F评分'].mean()
m_avg = rfm_data['M评分'].mean()

print('R评分的均值为：{}，F评分的均值为{},M评分的均值为{}'.format(r_avg, f_avg, m_avg))


# In[23]:


# 查看 R 值的分数与阈值对比后得到的返回值
rfm_data['R评分'] > r_avg


# In[24]:


num1 = bool(1) * 1
num2 = bool(0) * 1
print('num1 的值为{}，num2 的值为{}'.format(num1, num2))


# In[25]:


# 将R评分、F评分、M评分 的数据分别与对应的平均数做比较
rfm_data['R评分'] = (rfm_data['R评分'] > r_avg) * 1
rfm_data['F评分'] = (rfm_data['F评分'] > f_avg) * 1
rfm_data['M评分'] = (rfm_data['M评分'] > m_avg) * 1
rfm_data


# In[26]:


# 拼接R评分、F评分、M评分
rfm_score = rfm_data['R评分'].astype(str) + rfm_data['F评分'].astype(str) + rfm_data['M评分'].astype(str)
rfm_score


# In[27]:


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


# In[28]:


# 将RFM评分替换成具体的客户类型
rfm_data['客户类型'] = rfm_score.replace(transform_label)
rfm_data


# In[29]:


# 按【客户类型】分组，统计用户的数量
customer_data = rfm_data.groupby('客户类型')['用户ID'].count()
customer_data


# In[30]:


# 设置中文字体
plt.rcParams['font.family'] = ['SimHei']

# 绘制柱状图
plt.figure(figsize=(12, 8))
plt.bar(customer_data.index, customer_data)
plt.xlabel('客户类型', fontsize=12)
plt.ylabel('人数', fontsize=12)
plt.title('不同客户的数量分布', fontsize=16)


# In[31]:


# 绘制饼图
plt.figure(figsize=(14, 10))
plt.pie(customer_data, labels=customer_data.index, autopct='%0.1f%%')
plt.title('不同客户占比情况', fontsize=16)


# In[ ]:




