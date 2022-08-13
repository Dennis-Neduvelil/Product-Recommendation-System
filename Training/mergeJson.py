import os
import json
import re
import pandas as pd

def preProcess(file):
  try:
    json=pd.read_json(file)
    ext_data=pd.DataFrame(json['data'])
    transposed_data=ext_data.transpose()
  except:
    pass  
  return transposed_data

files = [f for f in os.listdir('.') if re.match(r'[0-9]+.*\.json', f)]
print(len(files))

counter=1
df=pd.DataFrame()
for i in files:
  temp=preProcess(i)
  df=df.append(temp)
  print(f'{counter} Files combined')
  counter+=1


df.to_csv('data_combined.csv', header=True, index=False)

print('File Saved')

