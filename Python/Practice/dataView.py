#!/usr/bin/python3
import pandas as pd
import sys

ext = (".xls", ".xlsx")
if(sys.argv[1].endswith(ext)):
    df = pd.read_excel("/var/www/html/DataProcessor/assets/data/show/"+sys.argv[1], header=None)
else:
    df = pd.read_csv("/var/www/html/DataProcessor/assets/data/show/"+sys.argv[1], sep="|,^", header=None)
df.columns = pd.RangeIndex(1, len(df.columns)+1)
print(df.head().to_html(index=False,classes="table table-hover listing-table v-align-middle text-center"))
