from obspy import read
from heatmap import Station,Location
import matplotlib.pyplot as plt
import taup
import requests

st=read('*.sac')

ev_cords=(-7.2968,122.5348)

for trace in st:
    print(trace.stats.location)
station_list=[]
eventfile='station_list_total'
with open(eventfile, "r") as infile:
        for line in infile:
            items = line.split()
            net=items[0]
            code=items[1]
            staLat=float(items[3])
            staLon=float(items[4])
            location=Location(staLat,staLon)
            start=items[7]
            stop=items[9]
            station_list.append(Station(net,code,location,start,stop))

staLatLons=[]

for trace in st:
    for sta in station_list:
        if trace.stats.network == sta.netwrk and trace.stats.station == sta.name:
                print('we have found a match')
                trace.stats.coordinates={'latitude':sta.loc.lat,'longitude':sta.loc.lon}
                staLatLons.append([sta.loc.lat,sta.loc.lon])
                #   trace.stats.coordinates.longitude=sta.loc.lon

for trace in st:
    print(
        trace.id,
        trace.stats.coordinates
    )
phase_list=['SKS','SKKS','SKKKS']
# for sta in staLatLon:
#     print(sta)
# with taup.TauPServer() as taupserver:
#     params = taup.DistazQuery()
#     params.geodetic(True)
#     params.event(-7.2968,122.5348)
#     #params.sourcedepth(559.1)
#     params.model('prem')
#     params.station(46.138771, -122.701202)
#     distazResult = params.calc(taupserver)
#     print(distazResult)
    # for sta in staLatLon:
#         params.station(*sta)
#         distazResult = params.calc(taupserver)
#         print(distazResult)



# st.filter('bandpass',freqmin=0.04,freqmax=0.20,corners=2)
# st.plot(type='section',dist_degree=True,ev_coord=(-7.2968,122.5348),orientation='horizontal')
distTime=[]
with taup.TauPServer() as taupserver:

    # query params correspond to the tools, may be any one of:
    # Time, Pierce, Path, Curve, Discon, Distaz, Find, Phase,
    # Refltrans, Table, Velmerge, Velplot, Version, Wavefront
    params = taup.TimeQuery()
    params.phase(["SKKS"])
    # params that will stay the same can be reused
    params.geodetic(True)


    eventLatLons = [[-7.2968,122.5348]]
    #staLatLons = [ [46.138771, -122.701202]]

    for sta in staLatLons:
        params.station( *sta )
        for evt in eventLatLons:
            params.event( *evt )
            jsonTimes = params.calc(taupserver)
            for a in jsonTimes.arrivals:
                distTime.append([a.distdeg, a.time])