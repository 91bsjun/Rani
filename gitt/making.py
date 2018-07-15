# -*- coding: cp949 -*-

print(u"분석즁..... 기다료.....\n")

import matplotlib.pyplot as plt
import os

   
def making(name, file1, file2, scale):
    try:
        os.mkdir(name)
    except:
        pass
    # process 1
    f = open(file1,"r")
    lines = f.readlines()
    f.close()

    all_ts = [] # total
    all_vs = []
    ts1 = [] # min
    vs1 = []
    ts2 = [] # max
    vs2 = []

    for i in range(len(lines)):
        line2 = lines[i].split(",")    
        if i>=2 and len(line2) == 5:
            line1 = lines[i-1].split(",")
            line2 = lines[i].split(",")

            c1 = line1[4].replace(" ","").replace("\n","")
            c2 = line2[4].replace(" ","").replace("\n","")
            
            t = float(line1[2].replace(" ",""))
            v = float(line1[3].replace(" ",""))

            all_ts.append(t)
            all_vs.append(v)
            if c1 != "0" and c2 == "0":
                ts1.append(t)
                vs1.append(v)
            if c1 == "0" and c2 != "0":
                ts2.append(t)
                vs2.append(v)
                
    # process 2
    f = open(file2,"r")
    lines = f.readlines()
    f.close()

    tmp_vs = []  # total
    tmp_qs = []  # total

    for i in range(len(lines)):
        if i>=2 and len(lines[i].split(",")) == 3:
            v = float(lines[i].split(",")[0].replace(" ",""))
            q = float(lines[i].split(",")[1].replace(" ",""))

            tmp_vs.append(v)
            tmp_qs.append(q)

    qss1 = [] # min
    vss1 = []
    qss2 = [] # max
    vss2 = []

    for i in range(len(tmp_vs)):
        for j in range(len(vs1)):
            try:
                if tmp_vs[i] == vs1[j] and tmp_vs[i] < tmp_vs[i+1]-scale:    # this is for detect increase rapidly
                    qss1.append(tmp_qs[i])
                    vss1.append(tmp_vs[i])
                    qss2.append(tmp_qs[i+1])
                    vss2.append(tmp_vs[i+1])
            except:
                pass
    '''
    if len(vs1) == len(qss1)+1 or len(vs1) == len(qss1)-1 or len(vs1) == len(qss1)+2 or len(vs1) == len(qss1)-2 or len(vs1) == len(qss1)+3 or len(vs1) == len(qss1)-3:
        pass
    elif len(vs1) < len(qss1):
        print("scale 을 증가 시킵니다")
        scale = scale*5.0
        making(name, file1, file2, scale)
        quit()

    elif len(vs1) > len(qss1):
        print("scale 을 감소 시킵니다")
        scale = scale/2.0
        making(name, file1, file2, scale)
        quit()
    '''
    fig = plt.figure(figsize=(10,8))
    plt.plot(all_ts,all_vs)
    plt.scatter(ts1,vs1,color="r")
    plt.scatter(ts2,vs2,color="g")
    plt.xlabel("Time [s]",fontsize=20)
    plt.ylabel("Voltage [V]",fontsize=20)
    plt.savefig(name+"/"+name+"_t-V.png",dpi=100)

    fig = plt.figure(figsize=(10,8))
    plt.plot(tmp_qs,tmp_vs)
    plt.scatter(qss1,vss1,color="r")
    plt.scatter(qss2,vss2,color="g")
    plt.xlabel("Q [mAh]",fontsize=20)
    plt.ylabel("V [V]",fontsize=20)
    plt.savefig(name+"/"+name+"_Q-V.png",dpi=100)
    plt.show()


    f = open(name+"/"+name+"_t-V_max.csv","w")
    f.write("Time [s],Voltage [V]\n")
    for i in range(len(ts2)):
        f.write(str(ts2[i])+","+str(vs2[i])+"\n")
    f.close()

    f = open(name+"/"+name+"_t-V_min.csv","w")
    f.write("Time [s],Voltage [V]\n")
    for i in range(len(ts1)):
        f.write(str(ts1[i])+","+str(vs1[i])+"\n")
    f.close()

    f = open(name+"/"+name+"_Q-V_max.csv","w")
    f.write("Q [mAh],V [V]\n")
    for i in range(len(qss2)):
        f.write(str(qss2[i])+","+str(vss2[i])+"\n")
    f.close()

    f = open(name+"/"+name+"_Q-V_min.csv","w")
    f.write("Q [mAh],V [V]\n")
    for i in range(len(qss1)):
        f.write(str(qss1[i])+","+str(vss1[i])+"\n")
    f.close()

'''
try:
    f = open("01-readme.txt","r")
    lines = f.readlines()
    f.close()
    scale = float(lines[0].split(":")[1].replace("\n",""))
except:
    scale = 0.0002
'''
scale = 0.0002

Profiles = []
VIs = []
names = []
all_dirs = os.listdir("./")
all_dirs.sort()

for i in all_dirs:
    if ".csv" in i and "Profile" in i:
        Profiles.append(i)
    elif ".csv" in i and "VI" in i:
        VIs.append(i)

for i in Profiles:
    names.append(i.split("_DisCh_Profile")[0])
print("0 : all")
for i in range(len(names)):
    print(str(i+1)+" : "+names[i])

get = input(u"\n Choose Number and Enter ! : ")

if get == 0:
    print("\n전체를 골랐넹?\n")
    for i in range(len(Profiles)):
        print(names[i]+" 분석중\n")
        print("그래프 창을 닫으면 다음 항목 분석시작함!")
        making(names[i], VIs[i], Profiles[i], scale)
else:    
    i = get-1
    print("\n"+names[i]+" 를 골랐넹?")
    making(names[i], VIs[i], Profiles[i], scale)
