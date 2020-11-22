import seaborn as sns
import pandas as pd
import numpy as np
from scipy import stats


def set_up_statistic(marks, ax):
    # Arithmetical mean
    ax.text(ax.viewLim.intervalx.max(), ax.viewLim.intervaly.max() * 0.90,
            'Arithmetical mean: {0}'.format(np.mean(marks)), fontsize=9)
    # Median
    ax.text(ax.viewLim.intervalx.max(), ax.viewLim.intervaly.max() * 0.85,
            'Median: {0}'.format(np.median(marks)), fontsize=9)
    # Mode
    ax.text(ax.viewLim.intervalx.max(), ax.viewLim.intervaly.max() * 0.80,
            'Mode: {0}'.format(stats.mode(marks)[0]), fontsize=9)
    # Geometrical mean
    ax.text(ax.viewLim.intervalx.max(), ax.viewLim.intervaly.max() * 0.75,
            'Geometrical mean: {0}'.format(stats.hmean(marks)), fontsize=9)
    # Range of values(размах)
    ax.text(ax.viewLim.intervalx.max(), ax.viewLim.intervaly.max() * 0.70,
            'Range of values: {0}'.format(np.ptp(marks)), fontsize=9)
    # Interquartile range(межквартильный  размах)
    ax.text(ax.viewLim.intervalx.max(), ax.viewLim.intervaly.max() * 0.65,
            'Interquartile range: {0}'.format(stats.iqr(marks)), fontsize=9)
    # Interdecile range
    ax.text(ax.viewLim.intervalx.max(), ax.viewLim.intervaly.max() * 0.60,
            'Interdecile range: {0}'.format(stats.iqr(marks, rng=(10, 90))), fontsize=9)
    # Variation(дисперсия)
    ax.text(ax.viewLim.intervalx.max(), ax.viewLim.intervaly.max() * 0.55,
            'Variation: {0}'.format(stats.variation(marks)), fontsize=9)
    # Standard deviation
    ax.text(ax.viewLim.intervalx.max(), ax.viewLim.intervaly.max() * 0.50,
            'Standard deviation: {0}'.format(np.std(marks)), fontsize=9)
    # Skewness(коэффициент асимметрии)
    ax.text(ax.viewLim.intervalx.max(), ax.viewLim.intervaly.max() * 0.45,
            'Skewness : {0}'.format(stats.skew(marks)), fontsize=9)


dataframe = pd.read_csv('./data/sexy_dataframe')
subjects = [column for column in dataframe.columns][:-1]
groups = [group for group in dataframe['Группа'].unique()]
for subject in subjects:
    subject_dataframe = dataframe[[subject, 'Группа']]
    for group in groups:
        subject_group_dataframe = subject_dataframe[subject_dataframe['Группа'] == group]
        g = sns.displot(subject_group_dataframe, x=subject, col='Группа', binwidth=4, height=4,
                        facet_kws=dict(margin_titles=True), kde=True)

        subject_marks = np.array([mark for mark in subject_group_dataframe[subject]])
        set_up_statistic(subject_marks, g.ax)
        g.savefig('./graphs/{0}_{1}.svg'.format(group, subject))
