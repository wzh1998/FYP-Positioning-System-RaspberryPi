# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as mp
import sklearn.metrics as sm
import sklearn.ensemble as se  # 集合算法模块
import sklearn.utils as su  # 打乱数据
import sklearn.neighbors as nb

knn = nb.KNeighborsClassifier()
data = np.loadtxt('data.csv', unpack=False, dtype='U20', delimiter=',', encoding='utf-8')

rssi = np.array(data[1:, 0], dtype='f8')
# x_cor = np.array(data[1:, 1], dtype='f8')
# y_cor = np.array(data[1:, 2], dtype='f8')


column = 9
row = 12
rssi_current = -50
group = 4
point_per_group = int((row/group)*column)


rssi_ds1 = [0 for i in range(column*row)]
rssi_ds2 = [0 for i in range(column*row)]
rssi_ds3 = [0 for i in range(column*row)]
distance = [0 for i in range(group)]
print(distance)
# target_arr = [[0 for i in range(column)] for j in range(row)]

# Convert rssi array into 2 dimensions
for i in range(12):
	for j in range(9):
		rssi_ds1[9*i+j] = rssi[3*9*i+ 3*j]
		rssi_ds2[9*i+j] = rssi[3*9*i+ 3*j + 1]
		rssi_ds3[9*i+j] = rssi[3*9*i+ 3*j + 2]

print(rssi_ds3)

for i in range(group):
	for j in range(point_per_group):
		distance[i] += abs(rssi_current-rssi_ds1[point_per_group*i + j])
		distance[i] += abs(rssi_current-rssi_ds2[point_per_group*i + j])
		distance[i] += abs(rssi_current-rssi_ds3[point_per_group*i + j])

nearest = np.argsort(distance)
print(nearest)
# print(rssi_ds1)




# target = x_cor;
# rssi.reshape(-1, 1)
# print(rssi)

# print(target)
# print(rssi)

# knn.fit(rssi,target)
# predictedLabel = knn.predict()
# print (predictedLabel)