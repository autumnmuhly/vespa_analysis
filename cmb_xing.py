import taup
import requests


# def get_xing(station,event,phase):
#     with taup.TauPServer(verbose=True) as taupserver:
#         params = taup.PathQuery()
#         params.phase(phase)
#         params.model('prem')
#         params.geodetic(True)

#         params.event(event.loc)
#         params.sourcedepth(event.depth)
#         for sta in station:
#             params.station (sta.loc)
#             timeResult = params.calc(taupserver)
#     return timeResult
# eventLatLons = [ [43.75, 130.67]]
# staLatLons = [ [-39.31, 174.18]]

class PhaseArr:
    def __init__(self,array,time):
        "PhaseArr takes in a station class and a time"
        self.array=array
        self.time=time




def get_xing(array_list,event,phase,evtdepth,depth,arctype):
    print(phase)
    with taup.TauPServer(verbose=True) as taupserver:
        evtlatlon=([[event.loc.lat,event.loc.lon]])
        for arr in array_list:
            staLatLons=(arr.center.lat,arr.center.lon)
            params = taup.PierceQuery()
            params.phase([phase])
            params.model('prem')
            params.geodetic(True)
            params.event( *evtlatlon[0] )
            params.sourcedepth(evtdepth)
            params.station(staLatLons[0],staLatLons[1])
            timeResult = params.calc(taupserver)
            phase_arr=[]
            arr.piercepoints = {}
            print('this is the event and sta info')
            print(evtdepth,staLatLons)
            for a in timeResult.arrivals:
                #print(a.phase,a.puristdist)
                if arctype == 'major':
                    if a.puristdist >=180 and a.puristdist<=360:
                        print('this is major arc')
                        for path in a.pierce:
                            if path.depth >= depth:
                                #phase_arr.append([path.lat,path.lon,path.distdeg,path.depth,path.time])
                                phase_arr.append(path)
                arr.piercepoints[phase]=phase_arr
    return


# def getTurnPt(array_list,event,phase,evtdepth,depth,arctype):
#     print(phase)
#     with taup.TauPServer(verbose=True) as taupserver:
#         evtlatlon=([[event.loc.lat,event.loc.lon]])
#         for arr in array_list:
#             staLatLons=(arr.center.lat,arr.center.lon)
#             params = taup.PierceQuery()
#             params.phase([phase])
#             params.model('prem')
#             params.geodetic(True)
#             params.turn(True)
#             params.event( *evtlatlon[0] )
#             params.sourcedepth(evtdepth)
#             params.station(staLatLons[0],staLatLons[1])
#             timeResult = params.calc(taupserver)
#             print('this right before i print out the timeresult')
#             #print(timeResult)
#             for a in timeResult.arrivals:
#                 if arctype == 'major':
#                     if a.puristdist >=180 and a.puristdist<=360:
#                         print('this is major arc')
#                         for path in a.pierce:
#                             if path.depth > depth:
#                                 print(path.depth)
#                                 arr.turnpt
#     return