import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import rcParams
import math
from collections import OrderedDict, Counter
import csv
import random
from numpy import genfromtxt


# Calculates euclidean distance from train element to test element
def calcDe(trainI, testI):
    return math.sqrt((float(trainI[0]) - float(testI[0])) ** 2 +
                     (float(trainI[1]) - float(testI[1])) ** 2 +
                     (float(trainI[2]) - float(testI[2])) ** 2 +
                     (float(trainI[3]) - float(testI[3])) ** 2
                     )


def knn(trainData, testData, k=1):
    for testI in testData:
        dataDic = OrderedDict()
        for trainI in trainData:
            De = calcDe(trainI, testI)
            # Keys are euclidean distance and the value is an array
            # that's has train data element and type of its neighbour
            dataDic[De] = [testI, trainI[4]]

        # Sorting dict by its euclidean distance
        sortedDataDic = OrderedDict(sorted(dataDic.items()))
        # Taking first k elements in dict
        neighbours = list(sortedDataDic.values())[0:k]
        # Classifying the type of test element
        type = classify(neighbours)
        testI[5] = type


def classify(neighbours):
    types = Counter()
    # Counting types of neighbours
    for neighbour in neighbours:
        types[neighbour[1]] += 1
    # Return the most common type of neighbours
    return types.most_common()[0][0]


def calcAccurancy(data):
    hits = 0
    for feature in data:
        if feature[4] == feature[5]:
            hits += 1

    return hits / len(data)


# Reading data from txt
dataset = genfromtxt('iris.data-input.txt', delimiter=',', dtype=str)
np.random.shuffle(dataset)
trainData = np.array(dataset[0:len(dataset) // 2])
testData = dataset[len(dataset) // 2:len(dataset) + 1]
# Add empty string for checking knn accurancy
testData = [np.append(i, '') for i in testData]

knn(trainData, testData, k=3)
print(calcAccurancy(testData))


# mpl.rcParams['font.family'] = 'Times New Roman'
# mpl.rcParams['axes.unicode_minus'] = False
# rcParams.update({'figure.autolayout': True})

# fig = plt.figure()
# fig.tight_layout()
#
# ax1 = plt.subplot2grid((1, 2), (0, 0))
# ax1.set_title("Соотношение длины чашелистика к его ширине")
# ax1.set_xlabel('Sepal width')
# ax1.set_ylabel('Sepal length')

# sepalWidthArr = [float(row[0]) for row in trainData] + [float(row[0]) for row in testData]
# sepalLengthArr = [float(row[1]) for row in trainData] + [float(row[1]) for row in testData]

# IrisSetosa = [item for item in]


# print(trainData)
# ax1.scatter(sepalWidthArr, sepalLengthArr, c='y')

# ax = fig.add_subplot(111, projection='3d')
#
# plt.show()

