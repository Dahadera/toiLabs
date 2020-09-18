import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import rcParams
import math
from matplotlib.ticker import MaxNLocator
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

# Task №1
# Plot first function: y = -+sqrt((1-x)/(1+x))
ax1 = plt.subplot2grid((3, 2), (0, 0))
ax1.set_title("Первое задание")
ax1.set_xlabel('x')
ax1.set_ylabel('y')

func1x = np.linspace(-0.9999, 1, N)
func1y = np.array([])
for xi in func1x:
    y = func1(xi)
    func1y = np.append(func1y, y)

ax1.plot(func1x, func1y, label='y = -+√((1-x)/(1+x))', c='r')
ax1.plot(func1x, -func1y, c='r')

# Plot second function: y = log2(x-2)
func2x = np.linspace(2.001, 5, N)
func2y = np.array([])
for xi in func2x:
    y = func2(xi)
    func2y = np.append(func2y, y)

ax1.plot(func2x, func2y, label='y = log2(x-2)', c='b')
ax1.set_ylim(-50, 50)
ax1.legend(loc='best', fontsize=6)

# Task №2
ax3 = plt.subplot2grid((3, 2), (1, 0))
ax3.set_title("2D изолинии")
ax3.set_xlabel('x')
ax3.set_ylabel('y')

ax3x, ax3y = np.mgrid[2.001:5:100j, -np.pi:np.pi:100j]
z = np.log2(ax3x) + np.sin(ax3y)
contour = ax3.contour(z)

labels = ['line 1', 'line 2', 'line 3', 'line 4',
          'line 5', 'line 6']
for i in range(len(labels)):
    contour.collections[i].set_label(labels[i])
ax3.legend(loc='best', fontsize=5.2)


# Average grade histogram for all semesters
ax2 = plt.subplot2grid((3, 2), (0, 1), rowspan=3)
ax2.set_title('Средний балл за каждый семестр')
ax2.set_xlabel('Семестр')
ax2.set_ylabel('Средний балл')
ax2.set_ylim(3, 5)

ax2data = np.array([[5, 5, 5, 3, 5, 5, 5, 5],
                    [4, 3, 4, 5, 4, 5, 4, 4, 5, 5, 5],
                    [3, 4, 4, 5, 5, 5, 5, 5, 4],
                    [5, 5, 5, 5, 4, 4, 4, 5, 5, 5],
                    [4, 5, 4, 4, 3, 4, 5, 5, 5, 5, 4],
                    [4, 4, 5, 5, 5, 5, 4, 4, 3]], dtype=object)

for i in range(len(ax2data)):
    label = '{0} семестр'.format(i + 1)
    averageGrade = np.average(ax2data[i])
    ax2.bar(i + 1, averageGrade, label=label)

ax2.set_xticks(np.arange(1, len(ax2data) + 1))
ax2.legend(loc='best', fontsize=7)

# Grade histogram for 4 semester
ax4 = plt.subplot2grid((3, 2), (2, 0))
ax4.set_title('Распределение баллов за 4 семестр')
ax4.set_xlabel('Балл')
ax4.set_ylabel('Количество')
ax4.xaxis.set_major_locator(MaxNLocator(integer=True))

grades = np.array([5, 5, 5, 5, 4, 4, 4, 5, 5, 5])
ax4data = Counter(grades)
for grade, count in ax4data.items():
    ax4.bar(grade, count, label=str(grade))

# Upper limit calculates from count of the most common grade + 1
ax4yUpperLimit = ax4data.most_common()[0][1] + 1
ax4.set_yticks(np.arange(1, ax4yUpperLimit)[::2])
ax4.legend(loc='best', fontsize=8)

plt.tight_layout()
plt.savefig('data.eps')
plt.savefig('data.svg')
plt.show()
