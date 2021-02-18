import pandas as pd
import numpy as np
import csv

#Read dataset
df = pd.read_csv("wasall_02445.txt", sep="	")

#Create a dictionary and group by horse
data_sets = {}
by_class = df.groupby('horse')
for groups, data in by_class:
    data_sets[groups] = data

#Create loop with test and train sets;
for i in (np.unique(df["horse"])):
    test = data_sets[i]

    train = {}
    for key, value in data_sets.items():
        if key not in i:
            train[key] = data_sets[key]

    #Random Forest model here;

with open('train.csv', 'w') as f:  # You will need 'wb' mode in Python 2.x
    w = csv.DictWriter(f, train.keys())
    w.writeheader()
    w.writerow(train)