import os

__author__ = "Byeongsun Jun"
__maintainer__ = "Byeongsun Jun"
__email__ = "bsjun@hanyang.ac.kr"
__date__ = "06/12/2019"

print(" # ------------------------------------------- #")
print(" #  Maintainer   : Byeongsun Jun               #")
print(" #  e-mail       : bsjun@hanyang.ac.kr         #")
print(" #  Original URL : https://github.com/91bsjun  #")
print(" #       EDV (End of Discharge Voltage)        #")
print(" # ------------------------------------------- #\n")

li = [f for f in os.listdir("./") if ".csv" in f]
li.sort()

for i, f in enumerate(li):
    print(i, ": ", f)
n = int(input("\nChoose file number: "))    
fname = li[n]

lines = open(fname, 'r').read()
lines = lines.split("\n")
data = {}
for i, l in enumerate(lines[1:]):
    spl = l.split(",")
    if len(spl) >= 2:
        cycle = int(spl[0])
        v = float(spl[1])
        if cycle not in data.keys():
            data[cycle] = []
        data[cycle].append(v)

cycles = list(data.keys())
rdata = []
ecycles = []

PSOC = int(input('Enter PSOC : ')) - 1

for c in cycles:
    try:
        rdata.append(data[c][PSOC])
    except:
        ecycles.append(c)

fname = fname.replace(".csv", "_m.csv")
f = open(fname, "w")
f.write(lines[0] + "\n")
for i, d in enumerate(rdata):
    f.write("%d,%f\n" % (i + 1, d))
f.close()    
print("\nFinish !")
print("\nTotal cycles           : ", len(cycles))
print("Effective cycles       : ", len(rdata))
print("Excluded cycle numbers : ", ecycles)
print("Data saved             : ", fname)

q = input("\nEnter to quit.")
