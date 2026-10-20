import jsonpickle
import os
from types import SimpleNamespace

phase = ('SKKKS','SKKKKS')
#-----------------------------
infilename = "residCalc.json"
with open(infilename, "r") as inf:
    mydata = jsonpickle.decode(inf.read())
mydata = SimpleNamespace(mydata)
evt=mydata.eq_list[0]

# for ph in phase:
#     for arr in mydata.diffArr:
#         for arrival in arr:
            