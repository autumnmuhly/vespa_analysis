class PhArrEvt:
    "ArrEvt pairs with phase specific resid and differential measurements"
    def __init__(self,arr,evt):
        self.array = arr
        self.evt = evt
        self.time={}
        self.slow={}
        self.backazi={}
        self.timeResid={}
        self.slowResid={}
        self.prem_time={}
        self.prem_slow={}
    def compute_resid(self,phase):
        self.timeResid[phase] = (self.time[phase]-self.prem_time[phase])
        #print(f' this is time resid {self.timeResid[phase]}')
        self.slowResid[phase] = (self.slow[phase]-self.prem_slow[phase])

class DiffArr:
    "holds two "
    def __init__(self,pair,phase1,phase2):
        self.arrayquake = pair
        self.phase1=phase1
        self.phase2=phase2
        self.diff_traveltime = None
        self.slow_diff = None
    def compute_diff(self):
        "Takes two arrivls and computes the diff"
        phase1=self.phase1
        phase2=self.phase2
        #print(f'{phase2} {self.array.timeResid[phase2]} {phase1} {self.array.timeResid[phase1]}')
        self.diff_traveltime = (self.arrayquake.timeResid[phase2]-self.arrayquake.timeResid[phase1])
        print(f'this is t_diff {self.diff_traveltime}')
        self.slow_diff = (self.arrayquake.slowResid[phase2]-self.arrayquake.slowResid[phase1])
        #print(f'this is slow {self.slow_diff}')

def read_in_vespa(array): 
    with open('*_BHR_*.dat', "r") as infile:
            for line in infile:
                items = line.split()
                gridnum=items[0]
                baseSta=items[9]