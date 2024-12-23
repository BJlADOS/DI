import pandas as pd
import os
import json

file_path = "./data/used_cars_300mb.csv"
file_size = os.path.getsize(file_path)
print(file_size)

df = pd.read_csv(file_path)
mem_usage = df.memory_usage(deep=True).sum()
print(mem_usage)

stats = []
for col in df.columns:
    col_mem = df[col].memory_usage(deep=True)
    stats.append({
        'column': col,
        'memory_bytes': col_mem,
        'share': col_mem / mem_usage,
        'dtype': str(df[col].dtype)
    })
stats.sort(key=lambda x: x['memory_bytes'], reverse=True)
with open('stats_no_optim.json', 'w') as f:
    json.dump(stats, f, indent=2)

for col in df.select_dtypes(include='object'):
    if df[col].nunique() < 0.5 * len(df[col]):
        df[col] = df[col].astype('category')

for col in df.select_dtypes(include=['int', 'float']):
    df[col] = pd.to_numeric(df[col], downcast='integer') \
        if str(df[col].dtype).startswith('int') \
        else pd.to_numeric(df[col], downcast='float')

mem_usage_optim = df.memory_usage(deep=True).sum()
print(mem_usage_optim)

stats_optim = []
for col in df.columns:
    col_mem = df[col].memory_usage(deep=True)
    stats_optim.append({
        'column': col,
        'memory_bytes': col_mem,
        'share': col_mem / mem_usage_optim,
        'dtype': str(df[col].dtype)
    })
stats_optim.sort(key=lambda x: x['memory_bytes'], reverse=True)
with open('stats_optim.json', 'w') as f:
    json.dump(stats_optim, f, indent=2)


use_cols = list(df.columns[:10])
chunk_iter = pd.read_csv(file_path, usecols=use_cols, chunksize=20000)
pd.concat(chunk_iter).to_csv("subset.csv", index=False)