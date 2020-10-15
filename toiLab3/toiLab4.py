import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import rcParams
import pandas as pd
from sklearn.cluster import KMeans


df = pd.read_csv('iris.data-input.cvs')
df = df.drop('Class', axis=1)
print(df.head(3))
processed_df = df.to_numpy()[:, :]

cluster_num = 4
k_means = KMeans(init='k-means++', n_clusters=cluster_num, n_init=12)
k_means.fit(processed_df)
labels = k_means.labels_
df['kmean_cluster'] = labels
print(df.head(3))

# Setting up mpl params
mpl.rcParams['font.family'] = 'Times New Roman'
mpl.rcParams['axes.unicode_minus'] = False
rcParams.update({'figure.autolayout': True})

fig = plt.figure()
# fig = plt.figure(figsize=plt.figaspect(2.))
ax1 = fig.add_subplot(2, 1, 1)

ax1.scatter(processed_df[:, 0], processed_df[:, 1], c=labels.astype(np.float), alpha=0.8)
ax1.set_xlabel('Sepal length', fontsize=16)
ax1.set_ylabel('Sepal width', fontsize=16)

ax2 = fig.add_subplot(2, 1, 2)
ax2.scatter(processed_df[:, 2], processed_df[:, 3], c=labels.astype(np.float), alpha=0.8)
ax2.set_xlabel('Petal length', fontsize=16)
ax2.set_ylabel('Petal width', fontsize=16)

plt.show()