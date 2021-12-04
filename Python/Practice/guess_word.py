from random import shuffle
import pandas as pd

df = pd.read_csv('/home/varun.singh/Dev/Python/Practice/corncob_lowercase.txt', header=None )
string = input()
string = list(map(str, string))
suffString= ''
lists = []
while(1):

    shuffle(string)
    suffString = ''.join(string)
    data = df[df[0] == suffString]
    datas=list(data[0])
    if datas not in lists:
        lists.append(datas)
        print(str(datas))
