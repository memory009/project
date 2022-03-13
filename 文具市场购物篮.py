import pandas as pd
from apyori import apriori
import matplotlib.pyplot as plt

# 读取【StationeryOrder.csv】文件的数据
data = pd.read_csv('StationeryOrder.csv', encoding='gbk')

# 查看数据的前 10 行信息
data.head(10)


# 查看数据基本信息
data.info()
# 查看数据中的重复行
data[data.duplicated()]
# 查看数据的描述性统计信息
data.describe()

# 定义函数，将数据类型转换成列表        
def conversion_data(s):
    return [s]


# 将“文具”列数据由“字符串”转变为“包含单个字符串的列表”
data['文具'] = data['文具'].agg(conversion_data)
# 将同一“id”的“包含单个字符串的列表”数据聚合为“包含多个字符串的列表”数据，并重置索引
new_data = data.groupby('id').sum().reset_index()


# 设置最小支持度、最小置信度以及最小提升度分别为：0.02、0.45、1
results = apriori(new_data['文具'], min_support=0.02,
                min_confidence=0.45, min_lift=1)
# 创建列表
extract_result = []

for result in results:
    # 获取支持度,并保留3位小数
    support = round(result.support, 3)

    # 遍历ordered_statistics对象
    for rule in result.ordered_statistics:
        # 获取前件和后件并转成列表
        head_set = list(rule.items_base)
        tail_set = list(rule.items_add)

        # 跳过前件为空的数据
        if head_set == []:
            continue

        # 提取置信度，并保留3位小数
        confidence = round(rule.confidence, 3)
        # 提取提升度，并保留3位小数
        lift = round(rule.lift, 3)

        # 将提取的数据保存到提取列表中
        extract_result.append([head_set, tail_set, support, confidence, lift])

# 将数据转化为 DataFrame 的格式
result_df = pd.DataFrame(extract_result, columns=[
                        '前件', '后件', '支持度', '置信度', '提升度'])


# 将“前件”、“后件”列转成字符串，方便后续提取数据
result_df['前件'] = result_df['前件'].astype('str')
result_df['后件'] = result_df['后件'].astype('str')
# 提取后件中“中性笔”的数据
gel_pens = result_df[result_df['后件'] == "['中性笔']"]
# 按照“支持度”对提取的数据进行排序
gel_pens = gel_pens.sort_values('支持度')


# 获取重置后的索引
df_index = gel_pens.reset_index().index
# 设置 柱子的宽度
width = 0.2
# 设置 x 的坐标值
x = df_index
x1 = x-width/2
x2 = x+width/2
# 设置 y 的坐标值
y1 = gel_pens['支持度']
y2 = gel_pens['置信度']

# 设置字体
plt.rcParams['font.family'] = ['SimHei']

# 设置画布尺寸
plt.figure(figsize=(18, 10))

# 绘制多组柱状图
plt.bar(x1, y1, width=width)
plt.bar(x2, y2, width=width)

# 设置图表标题名及字体大小
plt.title('“中性笔”对应前件的支持度、置信度数值比较', fontsize=20)

# 设置 x 坐标轴的刻度
plt.xticks(x, gel_pens['前件'])

# 设置坐标轴的标题名及字体大小
plt.xlabel('前件', fontsize=15)
plt.ylabel('数值', fontsize=15)

# 设置 y 轴的数值显示范围
plt.ylim(0, 0.6)

# 设置图例
plt.legend(['支持度', '置信度'], fontsize=15)

# 设置数据标签
for a, b in zip(x1, y1):
    plt.text(a, b, str(round(b*100, 1))+'%',
            ha='center', va='bottom', fontsize=12)
for a, b in zip(x2, y2):
    plt.text(a, b, str(round(b*100, 1))+'%',
            ha='center', va='bottom', fontsize=12)

plt.savefig('文具市场购物篮.png')