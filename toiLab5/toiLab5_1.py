import pandas as pd
import numpy as np
from collections import defaultdict
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score


dataset = pd.read_csv('./data/october_schedule.csv',
                      parse_dates=["Date"])
dataset = dataset.drop(columns=['Unnamed: 6', 'Attend.'])

renamed_columns = ["Date", "Score Type", "Visitor Team", "VisitorPts", "Home Team", "HomePts", "OT?", "Notes"]
dataset.columns = renamed_columns

dataset["HomeWin"] = dataset["VisitorPts"] < dataset["HomePts"]
y_true = dataset["HomeWin"].values

dataset["VisitorLastWin"] = 0
dataset['HomeLastWin'] = 0

won_last = defaultdict(int)
for index, row in dataset.iterrows():
    home_team = row["Home Team"]
    visitor_team = row["Visitor Team"]
    row["HomeLastWin"] = won_last[home_team]
    row["VisitorLastWin"] = won_last[visitor_team]
    dataset.iloc[index] = row

    won_last[home_team] = row["HomeWin"]
    won_last[visitor_team] = not row["HomeWin"]

clf = DecisionTreeClassifier(random_state=14)
X_previouswins = dataset[["HomeLastWin", "VisitorLastWin"]].values
scores = cross_val_score(clf, X_previouswins, y_true, scoring='accuracy')
print("Accuracy: {0:.1f}%".format(np.mean(scores) * 100))

# print(dataset.tail(9))