from types import SimpleNamespace
import jsonpickle

infilenameOLD = "residcalc_old.json"
with open(infilenameOLD, "r") as inf:
    mydataOLD = jsonpickle.decode(inf.read())
mydataOLD = SimpleNamespace(mydataOLD)


infilenameNEW = "residcalc.json"
with open(infilenameNEW, "r") as inf:
    mydataNEW = jsonpickle.decode(inf.read())
mydataNEW = SimpleNamespace(mydataNEW)

diffArrOLD=mydataOLD.diffArr
diffArrNew=mydataNEW.diffArr

for pair in diffArrOLD:
    #print(arr)
    #print(arr.arrival.array2quake.array.basestation.name)
    print('these are from the old')
    print(pair.diff_traveltime)

for pair in diffArrNew:
    print('these are from the new')
    print(pair.diff_traveltime)