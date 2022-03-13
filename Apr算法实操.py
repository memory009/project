from matplotlib import pyplot as plt
import pandas as pd
# 将文字设置为中文字体
plt.rcParams['font.family'] = ['SimHei']

from apyori import apriori
# 以 gbk 的编码模式读取并查看【公众号用户访问数据.csv】数据
user_data = pd.read_csv('公众号用户访问数据.csv',encoding='gbk')
# print(user_data)


# 设置画布尺寸
plt.figure(figsize=(20, 8))

# 提取列数据（'用户编号', '文章类别','访问日期'），并进行赋值
analysis_data = user_data[['用户编号', '文章类别', '访问日期']]

# 去除重复数据
analysis_data = analysis_data.drop_duplicates()

# 定义函数，将数据类型转换成列表
def conversion_data(i):
    return [i]

# 获取'文章类别'列，调用 agg() 方法
analysis_data['文章类别'] = analysis_data['文章类别'].agg(conversion_data)
# 查看处理后的数据

adjusted_data = analysis_data.groupby(['访问日期', '用户编号']).sum()
# 执行Apriori 算法
results = apriori(adjusted_data['文章类别'], min_support=0.1, min_confidence=0.3)

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

        # 将前件、后件拼接成关联规则的形式
        related_catogory = str(head_set)+'→'+str(tail_set)

        # 提取置信度，并保留3位小数
        confidence = round(rule.confidence, 3)
        # 提取提升度，并保留3位小数
        lift = round(rule.lift, 3)

        # 将提取的数据保存到提取列表中
        extract_result.append(
            [related_catogory, support, confidence, lift])

# 将数据转成 dataframe 的形式
rules_data = pd.DataFrame(extract_result, columns=[
                            '关联规则', '支持度', '置信度', '提升度'])

# 将数据按照“支持度”排序
sorted_by_support = rules_data.sort_values(by='支持度')

width = 0.4
# 画出柱状图
plt.bar(sorted_by_support.index, sorted_by_support['提升度'], width=width)
# 设置标题
plt.title('提升度柱状图', fontsize=25)
# 设置刻度名称
plt.xticks(sorted_by_support.index, sorted_by_support['关联规则'], fontsize=15)

# 设置坐标轴标签
plt.xlabel('关联规则', fontsize=20)
plt.ylabel('提升度', fontsize=20)

# 设置数据标签
for a, b in zip(sorted_by_support.index, sorted_by_support['提升度']):
    plt.text(a, b, b, ha='center', va='bottom', fontsize=12)

plt.savefig('Apr实操.png')
