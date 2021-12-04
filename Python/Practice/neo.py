import numpy as np
import pandas as pd
import sklearn.datasets
from sklearn.metrics import accuracy_score

breast_cancer=sklearn.datasets.load_breast_cancer()
X=breast_cancer.data
Y=breast_cancer.target

data=pd.DataFrame(breast_cancer.data,columns=breast_cancer.feature_names)
data['class']=breast_cancer.target
data.head()
#print(data)

from sklearn.model_selection import train_test_split
X=data.drop('class',axis=1)
Y=data['class']

X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.1,random_state=1,stratify=Y)
X_bin_train=X_train.apply(pd.cut,bins=2,labels=[0,1])
X_bin_test=X_test.apply(pd.cut,bins=2,labels=[0,1])
#print(type(X_bin_train),type(X_bin_test))



class MPNeuron:
    def __init__(self):
        self.b=None

    def model(self,X):
        return sum(X)>=self.b

    def predict(self,X):
        y=[]
        #print(X.shape[0])
        for i in range(X.shape[0]):
            # print(X.iloc[i])
            res=self.model(X.iloc[i])
            y.append(res)
        return np.array(y)

    def fit(self,X,Y):
        acc={}
        for b in range(X.shape[1]+1):
            self.b=b
            y_pred=self.predict(X)
            acc[b]=accuracy_score(y_pred,Y)

        best=max(acc,key=acc.get)
        self.b=b



mp=MPNeuron()
#print(X_bin_train)
#print(Y_train)
mp.fit(X_bin_train,Y_train)

y_test_pred=mp.predict(X_bin_test)
acc_test=accuracy_score(X_bin_test,Y_test)
print(acc_test)
