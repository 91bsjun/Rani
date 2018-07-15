# -*- coding: cp949 -*-
import os, sys

# -- select file
files = [f for f in os.listdir("./") if '.mpt' in f]
print("\n분석할 파일 고르세용~")
for i, f in enumerate(files):
    print(str(i).ljust(2) + ": " + f)
idx = int(input("Choose file: "))
filename = files[idx]

# -- reduce file
lines = open(filename, 'r').readlines()
rlines = []
main_start = False
for i, l in enumerate(lines):    
    if not main_start and 'mode' in l and 'time/s' in l and 'control/mA' in l:
        main_start = True
        l = l.replace("\t",",")
        rlines.append(l)
    elif main_start:
        l = l.replace("\t",",")
        rlines.append(l)

# -- reduce file to csv
'''
csv_filename = filename.replace(".mpt", ".csv")
f = open(csv_filename, "w")
for l in rlines:
    f.write(l)
f.close()
print("Reduced data file saved: " + csv_filename)
'''

# -- grouping current
t = 8
crt = 9
ewe = 10

change_idx = []
data_lines = rlines[1:]
critical_data = []          # time, ewe, crt
for i, line in enumerate(data_lines):
    spl_line = line.split(",")
    critical_data.append(spl_line[t] + "," + spl_line[ewe] + "," + spl_line[crt])
    if i >= 1:
        prev_line = data_lines[i-1].split(",")
        prst_line = data_lines[i].split(",")
        # when former current - current != 0
        if abs(float(prev_line[crt]) - float(prst_line[crt])) != 0:
            change_idx.append(i)

groups = []
# 0, +, -, +, -
for i, idx in enumerate(change_idx):
    if (i + 1) % 5 == 3:
        groups.append(critical_data[change_idx[i]:change_idx[i+1]])
    elif (i + 1) % 5 == 4:
        if idx == change_idx[-1]:
            groups.append(critical_data[change_idx[i]:])
        else:
            groups.append(critical_data[change_idx[i]:change_idx[i+1]])

# -- write data
dirname = filename.replace(".mpt", "")
if dirname not in os.listdir("./"):
    os.mkdir(dirname)
os.chdir(dirname)
cycle = 1
for i, group in enumerate(groups):
    if i % 2 == 0:        
        datafilename = filename.replace(".mpt", "_cycle" + str(cycle) + ".csv")
        f = open(datafilename, "w")
        f.write("time/s,Ewe/V,control/mA\n")
        for g in group:
            f.write(g + "\n")
    elif i % 1 == 0:
        f = open(datafilename, "a")
        for g in group:
            f.write(g + "\n")
        cycle += 1
    f.close()





