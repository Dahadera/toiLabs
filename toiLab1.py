import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import rcParams
import math
from matplotlib.ticker import MultipleLocator
from collections import Counter


def func1(x):
    return math.sqrt((1 - x) / (1 + x))


def func2(x):
    return math.log2(x - 2)


# FONTFAMILY
mpl.rcParams['font.family'] = 'Times New Roman'
mpl.rcParams['axes.unicode_minus'] = False
# to not cut off bottom axes
rcParams.update({'figure.autolayout': True})

fig = plt.figure()
fig.tight_layout()

# Values count
N = 10000
x = np.linspace(-10, 10, N)

# First function: y = -+sqrt((1-x)/(1+x))
ax1 = plt.subplot2grid((3, 2), (0, 0))
ax1y = np.array([])
ax1x = np.array([])
for xi in x:
    try:
        y = func1(xi)
        ax1y = np.append(ax1y, y)
        ax1x = np.append(ax1x, xi)
    except ValueError:
        continue

ax1.plot(ax1x, ax1y)
ax1.plot(ax1x, -ax1y)

# Average grade histogram for all semesters
ax2 = plt.subplot2grid((3, 2), (0, 1), rowspan=3)
ax2data = np.array([[5, 5, 5, 3, 5, 5, 5, 5],
                    [4, 3, 4, 5, 4, 5, 4, 4, 5, 5, 5],
                    [3, 4, 4, 5, 5, 5, 5, 5, 4],
                    [5, 5, 5, 5, 4, 4, 4, 5, 5, 5],
                    [4, 5, 4, 4, 3, 4, 5, 5, 5, 5, 4],
                    [4, 4, 5, 5, 5, 5, 4, 4, 3]], dtype=object)

for i in range(len(ax2data)):
    label = '{0} semester'.format(i + 1)
    averageGrade = np.average(ax2data[i])
    ax2.bar(label, averageGrade)

# Second function: y = log2(x-2) (x >=2)
ax3 = plt.subplot2grid((3, 2), (1, 0))
ax3y = np.array([])
ax3x = np.array([])
for xi in x:
    try:
        y = func2(xi)
        ax3y = np.append(ax3y, y)
        ax3x = np.append(ax3x, xi)
    except ValueError:
        continue

ax3.plot(ax3x, ax3y)

# Grade histogram for 4 semester
ax4 = plt.subplot2grid((3, 2), (2, 0))
scores = np.array([5, 5, 5, 5, 4, 4, 4, 5, 5, 5])
ax4data = Counter(scores)
ax4.bar(ax4data.keys(), ax4data.values())

plt.tight_layout()
plt.show()
