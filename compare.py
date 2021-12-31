import pandas as pd

# df = pd.read_excel('/tmp/audit_viettel/_ResourceMonitor_2021-11-26-14h_xml.csv')

from csv import reader
# skip first line i.e. read header first and then iterate over each row od csv as a list

total_list = []

df = pd.read_csv('full.csv')
full_saved_column = list(df.Hostname)
# print(full_saved_column)

df = pd.read_csv('old.csv')
old_saved_column = list(df.Hostname)
# print(old_saved_column)
difference = []
for i in old_saved_column:
    if i not in full_saved_column:
        difference.append(i)
print(difference)