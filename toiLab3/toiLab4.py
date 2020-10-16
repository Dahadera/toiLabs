import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import rcParams
import pandas as pd
from sklearn.cluster import KMeans, MeanShift, SpectralClustering, estimate_bandwidth

# Reading cvs file
df = pd.read_csv('iris.data-input.cvs')
# Deleting class column
df = df.drop('Class', axis=1)
processed_df = df.to_numpy()[:, :]

# K-means clustering
cluster_num = 3
k_means = KMeans(init='k-means++', n_clusters=cluster_num, n_init=12)
k_means.fit(processed_df)
k_means_labels = k_means.labels_

# Mean-shift clustering
bandwidth = estimate_bandwidth(processed_df, quantile=0.183, n_samples=150)
m_shift = MeanShift(bandwidth=bandwidth)
m_shift.fit(processed_df)
m_shift_labels = m_shift.labels_
# df['ms_cluster'] = m_shift.labels_

# Spectral clustering
spectral_c = SpectralClustering(n_clusters=3, assign_labels='discretize', random_state=0)
spectral_c.fit(processed_df)
spectral_c_labels = spectral_c.labels_

# Setting up mpl params
mpl.rcParams['font.family'] = 'Times New Roman'
mpl.rcParams['axes.unicode_minus'] = False
rcParams.update({'figure.autolayout': True})

fig = plt.figure(figsize=(12, 8))

colors = list(map(lambda x: '#3b4cc0' if x == 1 else '#b40426' if x == 2 else '#67c614', k_means_labels))
plt.figtext(0.5, 0.9885, 'K-means', va='center', ha='center', size=12, fontweight='bold')

ax1 = fig.add_subplot(3, 2, 1)
ax1.scatter(processed_df[:, 0], processed_df[:, 1], c=colors, alpha=0.8)
ax1.set_xlabel('Sepal length', fontsize=14)
ax1.set_ylabel('Sepal width', fontsize=14)

ax2 = fig.add_subplot(3, 2, 2)
ax2.scatter(processed_df[:, 2], processed_df[:, 3], c=colors, alpha=0.8)
ax2.set_xlabel('Petal length', fontsize=14)
ax2.set_ylabel('Petal width', fontsize=14)


colors = list(map(lambda x: '#3b4cc0' if x == 1 else '#b40426' if x == 2 else '#67c614', m_shift_labels))
plt.figtext(0.5, 0.681, 'Mean-shift', va='center', ha='center', size=13, fontweight='bold')

ax3 = fig.add_subplot(3, 2, 3)
ax3.scatter(processed_df[:, 0], processed_df[:, 1], c=colors, alpha=0.8)
ax3.set_xlabel('Sepal length', fontsize=14)
ax3.set_ylabel('Sepal width', fontsize=14)

ax4 = fig.add_subplot(3, 2, 4)
ax4.scatter(processed_df[:, 2], processed_df[:, 3], c=colors, alpha=0.8)
ax4.set_xlabel('Petal length', fontsize=14)
ax4.set_ylabel('Petal width', fontsize=14)

colors = list(map(lambda x: '#3b4cc0' if x == 1 else '#b40426' if x == 2 else '#67c614', spectral_c_labels))
plt.figtext(0.5, 0.350, 'Spectral clustering', va='center', ha='center', size=13, fontweight='bold')

ax5 = fig.add_subplot(3, 2, 5)
ax5.scatter(processed_df[:, 0], processed_df[:, 1], c=colors, alpha=0.8)
ax5.set_xlabel('Sepal length', fontsize=14)
ax5.set_ylabel('Sepal width', fontsize=14)

ax6 = fig.add_subplot(3, 2, 6)
ax6.scatter(processed_df[:, 2], processed_df[:, 3], c=colors, alpha=0.8)
ax6.set_xlabel('Petal length', fontsize=14)
ax6.set_ylabel('Petal width', fontsize=14)

plt.show()
