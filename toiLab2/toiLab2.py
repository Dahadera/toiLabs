import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import math
import csv
import random
from numpy import genfromtxt


def calcDe(trainI, testI):
    return math.sqrt((float(trainI[0]) - float(testI[0])) ** 2 +
                     (float(trainI[1]) - float(testI[1])) ** 2 +
                     (float(trainI[2]) - float(testI[2])) ** 2 +
                     (float(trainI[3]) - float(testI[3])) ** 2
                     )


# Reading data from txt
dataset = genfromtxt('iris.data-input.txt', delimiter=',', dtype=str)
np.random.shuffle(dataset)
# Making two sets
testData = np.array(dataset[0:len(dataset) // 2])
# testData = [np.delete(i, len(i) - 1) for i in testData]
trainData = dataset[len(dataset) // 2:len(dataset) + 1]
# Add empty string for checking knn accurancy
trainData = [np.append(i, '') for i in trainData]

fig = plt.figure()
fig.tight_layout()

# print(testData[0])

for trainI in trainData:
    minDe = calcDe(trainI, testData[0])
    trainClass = testData[0][4]
    for testI in testData:
        De = calcDe(trainI, testI)
        if De < minDe:
            minDe = De
            trainClass = testI[4]

    trainI[5] = trainClass
    if trainI[4] == trainI[5]:
        print("YYY")
    else:
        print(trainI)


# print(type(trainData))
# print(testData)


# ax = fig.add_subplot(111, projection='3d')
#
# plt.show()

