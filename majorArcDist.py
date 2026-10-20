from heatmap import Station,EQ,Location,calcArthCenter,Center,DistAz
from cmb_xing import get_xing,PhaseArr #this will also run the file that contains this functin i think?
from parseDat import PhArrEvt,DiffArr
import jsonpickle
import os
from types import SimpleNamespace
from pathlib import Path
from datetime import datetime
import sys
import glob
import matplotlib.pyplot as plt

arc_type='major'
phase = ('SKKKS','SKKKKS')
#----------------------------
diffArray=[]
for infilename in glob.glob('*.json'):
    with open(infilename, "r") as inf:
        mydata = jsonpickle.decode(inf.read())
    mydata = SimpleNamespace(mydata)
    #print(mydata)
    for pair in mydata.diffArr:
        diffArray.append(pair)
diffArr=diffArray

distances=[]
for pair in diffArr:
    dist=DistAz(pair.arrayquake.array.array.pt.loc.lat,pair.arrayquake.array.array.pt.loc.lon,pair.arrayquake.evt.loc.lat,pair.arrayquake.evt.loc.lon)
    if arc_type == 'major':
        major_dist=360-dist.delta
        distances.append(major_dist)

fig,axs=plt.subplots(1,1, tight_layout=True)
plt.hist(distances,50)
plt.xlabel('GC Distances')
plt.savefig('DisDistribution', dpi=900, bbox_inches='tight', pad_inches=0.1)