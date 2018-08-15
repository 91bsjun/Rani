# -*- coding: cp949 -*-
import os, sys

__author__ = "Byeongsun Jun"
__maintainer__ = "Byeongsun Jun"
__email__ = "bsjun@hanyang.ac.kr"
__date__ = "15/8/2018"

# -- select file
files = [f for f in os.listdir("./") if '.mpt' in f]
print("# ------------------------------------------- #")
print("#  Maintainer   : Byeongsun Jun               #")
print("#  e-mail       : bsjun@hanyang.ac.kr         #")
print("#  Original URL : https://github.com/91bsjun  #")
print("# ------------------------------------------- #")


run = True
while run:
    print("\nAvailable files list (*.mpt)")
    for i, f in enumerate(files):
        print(str(i+1).ljust(2) + ": " + f)
    idx = int(input("Enter file number: ")) - 1
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
    # extract last +,- data of 0, +, -, +, -
    for i, idx in enumerate(change_idx):
        if (i + 1) % 5 == 3:
            groups.append(critical_data[change_idx[i]:change_idx[i+1]])
        elif (i + 1) % 5 == 4:
            if idx == change_idx[-1]:
                groups.append(critical_data[change_idx[i]:])
            else:
                groups.append(critical_data[change_idx[i]:change_idx[i+1]])


    '''
    # prev methods
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
    '''
    cycle = 1
    data = {}
    max_len = 0
    for i, group in enumerate(groups):
        if i % 2 == 0:        
            data[cycle] = group
        elif i % 2 == 1:
            data[cycle] += group
            if len(data[cycle]) > max_len:
                max_len = len(data[cycle])
            cycle += 1
    max_cycle = len(data.keys())

    datafilename = filename.replace(".mpt", ".csv")
    f = open(datafilename, "w")
    # header 1 : cycle number
    header1 = ""
    for i in range(max_cycle):
        header1 += "cycle" + str(i+1) + ",,,"
    header1 += "\n"
    f.write(header1)
        
    # header 2
    header2 = "time/s,Ewe/V,controm/mA," * max_cycle + "\n"
    f.write(header2)

    # handling short cycles
    for key in data.keys():
        if len(data[key]) < max_len:
            for i in range(max_len - len(data[key])):
                data[key].append(",,")

    # write data
    for i in range(max_len):
        each_line = ""
        for key in data.keys():
            each_line += data[key][i] + ","
        each_line += "\n"
        f.write(each_line)

    f.close()

    print("\n- Data file has been saved: %s\n" % datafilename)
    yn = input("- Quit? (y/n)")
    if yn == "y":
        run = False
    
