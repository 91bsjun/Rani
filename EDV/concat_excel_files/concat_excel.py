import os
import pandas as pd

total_xl_files = [xl for xl in os.listdir('./') if '.xls' in xl]
total_xl_files.sort()

print('Choose files to Concatenate')
for i, f in enumerate(total_xl_files):
    print(i, ": ", f)

numbs = input("\nChoose file numbers (ex: 3,4,5)\n: ")
numbs = numbs.split(',')
xl_files = []
for n in numbs:
    n = int(n)
    xl_files.append(total_xl_files[n])

ext = os.path.splitext(xl_files[0])[1]
m_file = xl_files[0].replace(ext, '_sum.csv')

dfs = []

print('')
for xl_file in xl_files:
    print('* Read Excel...', xl_file)
    xl = pd.ExcelFile(xl_file)

    sheets = xl.sheet_names
    main_sheets = [s for s in sheets if 'Detail' in s]

    for ms in main_sheets:
        df = xl.parse(ms)
        df = df[['Cycle', 'Voltage(V)', 'Cur(A)']]
        dfs.append(df)

print('\n* Concatenate data files ...')
tot_df = pd.concat(dfs)

tot_df.to_csv(m_file, index=False)
print('\n* Data saved : ', m_file)
q = input("\nEnter to quit.")

