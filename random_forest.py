'''
    集合算法:
        1.正向激励
        2.自助聚合：每次从总样本矩阵中以有放回抽样的方式随机抽取部分样本构建决策树，这样形成多棵包含不同训练样本的决策树，
                    以削弱某些强势样本对模型预测结果的影响，提高模型的泛化特性。
        3.随机森林：在自助聚合的基础上，每次构建决策树模型时，不仅随机选择部分样本，而且还随机选择部分特征，这样的集合算法，
                    不仅规避了强势样本对预测结果的影响，而且也削弱了强势特征的影响，使模型的预测能力更加泛化。(中庸-->真值)
            随机森林相关API：
                import sklearn.ensemble as se
                # 随机森林回归模型    （属于集合算法的一种）
                # max_depth：决策树最大深度10
                # n_estimators：构建1000棵决策树，训练模型
                # min_samples_split: 子表中最小样本数 若小于这个数字，则不再继续向下拆分
                model = se.RandomForestRegressor(max_depth=10, n_estimators=1000, min_samples_split=2)

    案例：分析共享单车的需求，从而判断如何进行共享单车的投放。
        1.读取数据  bike_day.csv
        2.整理输入集和输出集     划分测试集与训练集
        3.选择模型----随机森林，训练模型
        4.使用测试集输出r2得分
        5.输出特征重要性，并绘制图像
'''
import numpy as np
import matplotlib.pyplot as mp
import sklearn.metrics as sm
import sklearn.ensemble as se  # 集合算法模块
import sklearn.utils as su  # 打乱数据

'''=================================分析bike_day.csv==============================='''
# 读取数据方法1
# data = []
# with open('./ml_data/bike_day.csv','r') as f:
#     for line in f.readlines():
#         data.append(line[:-1].split(','))
# print(data)
# data = np.array(data)

# 读取数据方法2
data = np.loadtxt('bike_day.csv', unpack=False, dtype='U20', delimiter=',')
# print(data.shape)
day_headers = data[0, 2:13]
# print(day_headers)
x = np.array(data[1:, 2:13], dtype='f8')
y = np.array(data[1:, -1], dtype='f8')

# Debug Code
# x = np.array(data[1:3, 2:13],dtype='f8')
# y = np.array(data[1:3, -1],dtype='f8')

# 划分测试集和训练集
x, y = su.shuffle(x, y, random_state=7)  # 打乱样本

train_size = int(len(x) * 0.9)
train_x, test_x, train_y, test_y = x[:train_size], x[train_size:], y[:train_size], y[train_size:]


# 训练模型
model = se.RandomForestRegressor(max_depth=10, n_estimators=1000, min_samples_split=3)
model.fit(train_x, train_y)

# 模型测试
pred_test_y = model.predict(test_x)


'''
# 模型评估
print('bike_day r2_score score:', sm.r2_score(test_y, pred_test_y))

# 输出模型特征重要性
day_fi = model.feature_importances_

# =================================分析bike_hour.csv===============================
# 读取数据
data = []
with open('bike_hour.csv', 'r') as f:
    for line in f.readlines():
        data.append(line[:-1].split(','))

data = np.array(data)
hour_headers = data[0, 2:14]
print(hour_headers)
x = np.array(data[1:, 2:14], dtype='f8')
y = np.array(data[1:, -1], dtype='f8')

# 划分测试集和训练集
x, y = su.shuffle(x, y, random_state=7)  # 打乱样本
train_size = int(len(x) * 0.9)
train_x, test_x, train_y, test_y = x[:train_size], x[train_size:], y[:train_size], y[train_size:]

# 训练模型
model = se.RandomForestRegressor(max_depth=10, n_estimators=1000, min_samples_split=3)
model.fit(train_x, train_y)

# 模型测试
pred_test_y = model.predict(test_x)

# 模型评估
print('bike_hour r2_score score:', sm.r2_score(test_y, pred_test_y))

# 输出模型特征重要性
hour_fi = model.feature_importances_

# 画出bike_day的特征重要性图像
mp.figure('Feature Importance', facecolor='lightgray')
mp.rcParams['font.sans-serif'] = 'SimHei'
mp.subplot(211)
mp.title('Bike_day FI')
mp.ylabel('Feature Importance')
mp.grid(linestyle=":")
sorted_indexes = day_fi.argsort()[::-1]  # 下标排序,从大到小
x = np.arange(day_headers.size)
mp.bar(x, day_fi[sorted_indexes], 0.7, color='dodgerblue', label='BDFI')
mp.xticks(x, day_headers[sorted_indexes])  # 设置x轴坐标
mp.tight_layout()
mp.legend()



# 画出bike_hour的特征重要性图像

mp.subplot(212)
mp.title('Bike_hour FI')
mp.ylabel('Feature Importance')
mp.grid(linestyle=":")
sorted_indexes = hour_fi.argsort()[::-1]  # 下标排序,从大到小
x = np.arange(hour_headers.size)
mp.bar(x, hour_fi[sorted_indexes], 0.7, color='orangered', label='BHFI')
mp.xticks(x, hour_headers[sorted_indexes])  # 设置x轴坐标
mp.tight_layout()
mp.legend()

mp.show()
'''



# 输出结果：
# (732, 16)
# ['season' 'yr' 'mnth' 'holiday' 'weekday' 'workingday' 'weathersit' 'temp'
#  'atemp' 'hum' 'windspeed']
# bike_day的r2_score得分： 0.8929064136199945
# ['season' 'yr' 'mnth' 'hr' 'holiday' 'weekday' 'workingday' 'weathersit'
#  'temp' 'atemp' 'hum' 'windspeed']
# bike_hour的r2_score得分： 0.9185230199218621
