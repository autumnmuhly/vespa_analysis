import jsonpickle
import os
from types import SimpleNamespace
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib import cm
import glob
import statistics
import pyproj

interestDepth=2891.0
#infilename = "residcalc.json"
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
print(f'this is the len of diff arr {len(diffArr)}')
t_diff_values=[]
for pair in diffArr:
    #print(arr)
    #print(arr.arrival.array2quake.array.basestation.name)
    t_diff_values.append(pair.diff_traveltime)
    # print(arr.arrival.array2quake.piercepoints['SKKKKS'])
    # print(arr.arrival.array2quake.piercepoints['SKKKKS'][4][3])

fig1=plt.figure()
ax1=fig1.add_subplot(111,projection=ccrs.PlateCarree(central_longitude=180))
ax1.add_feature(cfeature.OCEAN, color='lightblue')
ax1.add_feature(cfeature.LAND, color="oldlace")

fig2=plt.figure()
ax2=fig2.add_subplot(111,projection=ccrs.PlateCarree(central_longitude=180))
ax2.add_feature(cfeature.OCEAN, color='lightblue')
ax2.add_feature(cfeature.LAND, color="oldlace")

fig3=plt.figure()
ax3=fig3.add_subplot(111)

fig4=plt.figure()
ax4=fig4.add_subplot(111,projection=ccrs.PlateCarree(central_longitude=-30))
ax4.add_feature(cfeature.OCEAN, color='lightblue')
ax4.add_feature(cfeature.LAND, color="oldlace")


max_value=max(t_diff_values)
min_value=min(t_diff_values)
norm=plt.Normalize(min_value,max_value)
real_points=[]
for pair in diffArr:
    real_points.append(pair.diff_traveltime)
max_value=max(real_points)
min_value=min(real_points)
norm=plt.Normalize(min_value,max_value)
cmap=cm.cividis
bar=cm.ScalarMappable(norm=norm,cmap=cmap)
def interGC(lon1,lat1,lon2,lat2):
    g = pyproj.Geod(ellps='clrk66',proj='orthographic')
    (az12, az21, dist) = g.inv(lon1,lat1, lon2,lat2)
    lonlats = g.npts(lon1,lat1,lon2,lat2, 1 + int(dist / 10))
    lonlats = lonlats[:-600]
    lonlats = lonlats[300:]
    minorlons, minorlats = zip(*lonlats)
    return minorlats,minorlons



cnt=0
for pair in diffArr:
    # print(pair.arrayquake.piercepoints['SKKKKS'])
    # lat=[]
    # lon=[]
    # for i in range(len(pair.arrayquake.piercepoints['SKKKKS'])-1):
    #     prevlat=pair.arrayquake.piercepoints['SKKKKS'][i].lat
    #     prevlon=pair.arrayquake.piercepoints['SKKKKS'][i].lon
    #     lat.append(prevlat)
    #     lon.append(prevlon)
    #     morelats,morelons=interGC(prevlon,prevlat,pair.arrayquake.piercepoints['SKKKKS'][i+1].lon,pair.arrayquake.piercepoints['SKKKKS'][i+1].lat)
    #     lat.extend(morelats)
    #     lon.extend(morelons)
    # lat.append(pair.arrayquake.piercepoints['SKKKKS'][-1].lat)
    # lon.append(pair.arrayquake.piercepoints['SKKKKS'][-1].lon)
    # # print(pair.arrayquake.piercepoints['SKKKKS'][4].lon)
    # entrylat=pair.arrayquake.piercepoints['SKKKKS'][0].lat
    # entrylon=pair.arrayquake.piercepoints['SKKKKS'][0].lon
    # exitlat=pair.arrayquake.piercepoints['SKKKKS'][-1].lat
    # exitlon=pair.arrayquake.piercepoints['SKKKKS'][-1].lon
    # plt.figure(4)
    # lineColor=cmap(norm(pair.diff_traveltime))
    # resid=plt.plot(lon,lat,c='blue',linewidth=.5,alpha=.3,transform=ccrs.PlateCarree())
    # plt.scatter(entrylon,entrylat,marker='o',s=2,c=pair.diff_traveltime,cmap=cm.cividis, norm=norm,transform=ccrs.PlateCarree())
    # plt.scatter(exitlon,exitlat,marker='o',s=2,c=pair.diff_traveltime,cmap=cm.cividis, norm=norm,transform=ccrs.PlateCarree())
    # plt.scatter(pair.arrayquake.piercepoints['SKKKKS'][4].lon,pair.arrayquake.piercepoints['SKKKKS'][4].lat,marker='o',s=2,c=pair.diff_traveltime,cmap=cm.cividis, norm=norm,transform=ccrs.PlateCarree())
    if pair.diff_traveltime >=15:
        #print(pair.arrayquake.array.basestation.name,pair.diff_traveltime,pair.arrayquake.evt)
        print(pair,pair.diff_traveltime,pair.arrayquake.evt)
    cnt+=1
    plt.figure(1)
    lat=float(pair.arrayquake.piercepoints['SKKKKS'][4].lat)
    lon=float(pair.arrayquake.piercepoints['SKKKKS'][4].lon)
    resid=plt.scatter(lon,lat,c=pair.diff_traveltime,cmap=cm.cividis, norm=norm,transform=ccrs.PlateCarree())
    plt.figure(2)
    plt.scatter(pair.arrayquake.array.array.pt.loc.lon,pair.arrayquake.array.array.pt.loc.lat,marker='^',c='red',transform=ccrs.PlateCarree())
    plt.scatter(pair.arrayquake.evt.loc.lon,pair.arrayquake.evt.loc.lat,marker='*',c='yellow',transform=ccrs.PlateCarree())
    plt.figure(3)
    plt.scatter(pair.diff_traveltime,pair.arrayquake.piercepoints['SKKKKS'][1].depth,c='pink')
print(f'this is what is in count {cnt}')
print(f'this is the mean, median, and mode of the residuals {statistics.mean(real_points),statistics.median(real_points),statistics.mode(real_points)}')
plt.figure(1)
cbar=fig1.colorbar(resid)
ax1.set_extent([-180, 180, -90, 90], crs=ccrs.PlateCarree())
cbar.set_label(f'Time Resid at S4KS mid bounce point at CMB ', rotation=90)
plt.savefig(f'Plot1_residual', dpi=900, bbox_inches='tight', pad_inches=0.1)

plt.figure(2)
ax2.set_extent([-180, 180, -90, 90], crs=ccrs.PlateCarree())
plt.savefig('location', dpi=900, bbox_inches='tight', pad_inches=0.1)

plt.figure(3)
plt.axvline(x=0,color='gray',linewidth=2, alpha=.3)
ax3.tick_params(axis='x',top=True, labeltop = True, bottom = False, labelbottom = False)
ax3.invert_yaxis()
plt.xlabel('S4KS-S3KS Travel Time Diff')
plt.ylabel('Ray Turning Point depth')
plt.savefig('diff_turnpt', dpi=900, bbox_inches='tight', pad_inches=0.1)

plt.figure(4)
bar.set_array([])
cbar=fig4.colorbar(bar,ax=ax1)
ax4.set_extent([-180, 180, -90, 90], crs=ccrs.PlateCarree())
cbar.set_label(f'Time diff S3KS-S4KS', rotation=90)
plt.savefig(f'Plot4_diff', dpi=900, bbox_inches='tight', pad_inches=0.1)