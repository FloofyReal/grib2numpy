import pygrib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.basemap import Basemap
import numpy as np
 
plt.figure(figsize=(12,8))
 
grib='../data/ECMWF/32x32/europe_thcc_201001.grb' # Set the file name of your input GRIB file
grbs=pygrib.open(grib)
 
grb = grbs.select(name='Temperature')[0]
data=grb.values
print data.shape
print max(data[0] - 273.15)
print min(data[0] - 273.15)

lat,lon = grb.latlons() # Set the names of the latitude and longitude variables in your input GRIB file
print len(lat)
print len(lon)
 

# BIG 
        # "area": "70/-15/30/30",
# m=Basemap(projection='mill', llcrnrlon=-15,urcrnrlon=30,llcrnrlat=30,urcrnrlat=70,resolution='h')

# 64x64
        # "area": "58.8/8.1/40/27",
# m=Basemap(projection='mill', llcrnrlon=8.1,urcrnrlon=27,llcrnrlat=40,urcrnrlat=58.8,resolution='h')
# 32x32
        # "area": "54.3/13/45/22",
m=Basemap(projection='mill', llcrnrlon=13,urcrnrlon=22,llcrnrlat=45,urcrnrlat=54.3,resolution='h')

x, y = m(lon,lat)

# cs = m.pcolormesh(x,y,data-273.15,cmap=plt.cm.hot)
cs = m.pcolormesh(x,y,data-273.15)

my_coast = m.drawcoastlines()
my_states = m.drawcountries()
# my_p = m.drawparallels(np.arange(40,60,2),labels=[1,1,0,0])
# my_m = m.drawmeridians(np.arange(10,28,2),labels=[0,0,0,1])
 
plt.colorbar(pad=0.10, label='Teplota')
plt.title('Teplota') # Set the name of the variable to plot
plt.savefig('temp_32_title.png') # Set the output file name
plt.show()
