#!/usr/bin/python3
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier

train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

def checkNan(a,b):
    print(a[b].isnull().values.any())
checkNan(train, 'Age')

trainNumAge = train.copy()
trainNumAge['Sex'] = trainNumAge['Sex'].map({'female': 1, 'male': 0})
trainNumEmbarked['Embarked'] = trainNumEmbarked['Embarked'].map({'S': 1, 'C': 2, 'Q': 3})
