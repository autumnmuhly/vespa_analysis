from heatmap import Station,EQ,Location,calcArthCenter,Center,calcBasestation
from cmb_xing import get_xing,PhaseArr #this will also run the file that contains this functin i think?
from parseDat import PhArrEvt,DiffArr
import jsonpickle
import os
from types import SimpleNamespace
from pathlib import Path
from datetime import datetime
import sys
import argparse

interestDepth=2891.0
arc_type='major'
infilename = "heatmap.json"
phase = ('SKKKS','SKKKKS')
#----------------------------------------

def parseArgs():
    parser = argparse.ArgumentParser(prog='ResidCalc',
                    description='Calculates DiffResid',
                    epilog='Text at the bottom of help')
    parser.add_argument('-o', '--outfile', default="residcalc.json", help="output file")
    return parser.parse_args()

with open(infilename, "r") as inf:
    mydata = jsonpickle.decode(inf.read())
mydata = SimpleNamespace(mydata)
evt=mydata.eq_list[0]

workingDirPath=os.getcwd()
workingDir=workingDirPath.split('/')[-1]



if Path('pdffile_list_*'):
      os.system('rm -rf pdffile_list_*')
for ph in phase:
    print(ph)
    os.system(f'pdftk_extract.sh *_hilbert_BHR_{ph}.pdf {ph}') #needs to be added to your path

baseSta_list={}
for ph in phase:
    sta_list=[]
    with open(f'pdffile_list_{ph}', "r") as infile:
        for line in infile:
            items = line.strip().split('_')
            baseSta=items[-3]
            sta_list.append(baseSta)
    baseSta_list[f'{ph}']=sta_list

print(baseSta_list)

matchedList=[]
for sta in baseSta_list['SKKKS']:
    for sta2 in baseSta_list['SKKKKS']:
        if sta == sta2:
            matchedList.append(sta)

baseSta_list=matchedList
ArrEvtPair=[]

for sta in baseSta_list:
    for arr in mydata.good_arrays:
        for evt in arr.eqlists:
            if sta == str(arr.basestation.name):
            #if sta == str(arr.array.basestation.name):
                ArrEvtPair.append(PhArrEvt(arr,evt))
print(f'this is the len of array list and checked list {len(ArrEvtPair),len(ArrEvtPair)}')


for ph in phase:
    print(ph)
    with open(f'TA_SubArray_SmKS_Search_hilbert{workingDir}_{ph}.dat', "r") as infile:
                    for line in infile:
                        for arr in ArrEvtPair:
                            items = line.split()
                            baseSta=items[8]
                            #if baseSta == arr.array.array.basestation.name:
                            if baseSta == arr.array.basestation.name:
                                arr.time[ph] = float(items[29])
                                arr.slow[ph] = float(items[30])
                                arr.backazi[ph] = float(items[31])
                                arr.timeResid[ph] = float(items[22])
                                arr.slowResid[ph] = float(items[23])
                                arr.prem_time[ph] = float(items[26])
                                arr.prem_slow[ph] = float(items[27])
                                arr.center=(Center(items[2],items[3]))
                                #print(arr.array2quake.center)
    get_xing(ArrEvtPair,evt,ph,evt.depth,interestDepth,arc_type)
    #getTurnPt(ArrEvtPair,evt,ph,evt.depth,interestDepth,arc_type)



diffArr=[]
for pair in ArrEvtPair:
    diffArr.append(DiffArr(pair,phase[0],phase[1]))

for pair in diffArr:
    pair.compute_diff()

# for pair in diffArr:
#      print('------------------')
#      print(pair.arrayquake.piercepoints['SKKKKS'])
    #  print(pair.arrayquake.array.array.basestation.name)
    #  print(pair.diff_traveltime)

# for arr in diffArr:
#     print(arr.arrival.array2quake.array.basestation.name)
#     print(arr.arrival.array2quake.array.basestation.name, arr.arrival.array2quake.center.lat, arr.arrival.array2quake.center.lon, arr.arrival.time, arr.arrival.prem_time, arr.arrival.timeResid)


mydata={"diffArr":diffArr,
        "phase": phase,
        }
args = parseArgs()
with open(args.outfile, "w") as outf:
        outf.write(jsonpickle.encode(mydata))