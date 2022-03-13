import numpy as np

import skfuzzy as fuzz

import skfuzzy.control as ctrl

import matplotlib.pyplot as plt


x_stain_range=np.arange(1,11,1,np.float32)        #左取右不取，np.arange(起点，终点，步长)    float:将之转换为float32类型

x_oil_range=np.arange(1,11,1,np.float32)

y_powder_range=np.arange(1,11,1,np.float32)


# 创建模糊控制变量

x_stain=ctrl.Antecedent(x_stain_range, 'stain')

x_oil=ctrl.Antecedent(x_oil_range, 'oil')

y_powder=ctrl.Consequent(y_powder_range, 'powder')


# 定义模糊集和其隶属度函数

x_stain['N']=fuzz.trimf(x_stain_range,[0,0,5])        #不是很理解三角形隶属度括号内表示的内容（推测代表三角形三个顶点的位置）
x_stain['M']=fuzz.trimf(x_stain_range,[0,5,10])
x_stain['P']=fuzz.trimf(x_stain_range,[5,10,10])

x_oil['N']=fuzz.trimf(x_oil_range,[0,0,5])
x_oil['M']=fuzz.trimf(x_oil_range,[0,5,10])
x_oil['P']=fuzz.trimf(x_oil_range,[5,10,10])

y_powder['N']=fuzz.trimf(y_powder_range,[0,0,13])
y_powder['M']=fuzz.trimf(y_powder_range,[0,13,25])
y_powder['P']=fuzz.trimf(y_powder_range,[13,25,25])



# 设定输出powder的解模糊方法——质心解模糊方式

y_powder.defuzzify_method='centroid'


# #可视化输出和隶属函数
# x_stain.automf(3)
# x_oil.automf(3)
# y_powder.automf(3)
# x_stain.view()
# x_oil.view()
# y_powder.view()
# plt.show()


# 输出为N的规则

rule0 = ctrl.Rule(antecedent=((x_stain['N'] & x_oil['N']) |(x_stain['M'] & x_oil['N']) ), consequent=y_powder['N'], label='rule N')

# 输出为M的规则

rule1 = ctrl.Rule(antecedent=((x_stain['P'] & x_oil['N']) |(x_stain['N'] & x_oil['M']) |(x_stain['M'] & x_oil['M']) |(x_stain['P'] & x_oil['M']) | (x_stain['N'] & x_oil['P']) ),consequent=y_powder['M'], label='rule M')

# 输出为P的规则

rule2 = ctrl.Rule(antecedent=((x_stain['M'] & x_oil['P']) | (x_stain['P'] & x_oil['P']) ), consequent=y_powder['P'], label='rule P')

# 系统和运行环境初始化

system = ctrl.ControlSystem(rules=[rule0, rule1, rule2])

sim = ctrl.ControlSystemSimulation(system)


sim.input['stain'] = 4

sim.input['oil'] = 7

sim.compute()   # 运行系统

output_powder = sim.output['powder']

 

# 打印输出结果

print(output_powder)





#参考文献：'https://blog.csdn.net/dcyywin8/article/details/103460871'     三角形隶属度
#          'http://www.10qianwan.com/articledetail/624390.html'       plt.show()可视化