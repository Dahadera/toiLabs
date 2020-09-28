import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import rcParams
import math
from collections import OrderedDict, Counter
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
            # Keys are euclidean distance from trainI to testI and the value is an array
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


def calcAccuracy(data):
    hits = 0
    for feature in data:
        if feature[4] == feature[5]:
            hits += 1

    return hits / len(data)


# Setting up mpl params
mpl.rcParams['font.family'] = 'Times New Roman'
mpl.rcParams['axes.unicode_minus'] = False
rcParams.update({'figure.autolayout': True})

# Reading data from txt
dataset = genfromtxt('iris.data-input.txt', delimiter=',', dtype=str)
np.random.shuffle(dataset)
trainData = np.array(dataset[0:len(dataset) // 2])
testData = dataset[len(dataset) // 2:len(dataset) + 1]
# Add empty string for checking knn accuracy
testData = np.array([np.append(i, '') for i in testData])

knn(trainData, testData, k=3)
accuracy = calcAccuracy(testData)
print("KNN accuracy = {0}".format(accuracy))

# Delete last string from every array in testData
testData = np.array([i[0:len(i) - 1] for i in testData])
# Concatenate train and test dataset to plot graph
processedDataset = np.array(testData)
processedDataset = np.concatenate((processedDataset, trainData))

# Using generators to make seperate arrays [ EXP for x in seq if COND ]
irisSetosa = np.array([item for item in processedDataset if item[4] == 'Iris-setosa'])
irisVersicolour = np.array([item for item in processedDataset if item[4] == 'Iris-versicolor'])
irisVirginica = np.array([item for item in processedDataset if item[4] == 'Iris-virginica'])

fig = plt.figure()
fig.tight_layout()

ax1 = plt.subplot2grid((1, 2), (0, 0))
ax1.scatter([float(item[0]) for item in irisSetosa],
            [float(item[2]) for item in irisSetosa], label='Iris Setosa', marker='o', alpha=0.8)
ax1.scatter([float(item[0]) for item in irisVersicolour],
            [float(item[2]) for item in irisVersicolour], label='Iris Versicolour', marker='*', alpha=0.9)
ax1.scatter([float(item[0]) for item in irisVirginica],
            [float(item[2]) for item in irisVirginica], label='Iris Virginica', marker='^', alpha=0.8)

ax1.set_title("Измерения длины цветков ириса")
ax1.set_xlabel('Длина чашелистика')
ax1.set_ylabel('Длина лепестка')
ax1.legend(loc='upper left', fontsize=7)


ax2 = plt.subplot2grid((1, 2), (0, 1))
ax2.scatter([float(item[1]) for item in irisSetosa],
            [float(item[3]) for item in irisSetosa], label='Iris Setosa', marker='o', alpha=0.8)
ax2.scatter([float(item[1]) for item in irisVersicolour],
            [float(item[3]) for item in irisVersicolour], label='Iris Versicolour', marker='*', alpha=0.9)
ax2.scatter([float(item[1]) for item in irisVirginica],
            [float(item[3]) for item in irisVirginica], label='Iris Virginica',marker='^', alpha=0.8)

ax2.set_title("Измерения ширины цветков ириса")
ax2.set_xlabel('Ширина чашелистика')
ax2.set_ylabel('Ширина лепестка')
ax2.legend(loc='upper right', fontsize=7)

plt.savefig('data.svg')
plt.show()

