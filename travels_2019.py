import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cartopy.crs as ccrs
from cartopy import geodesic
import shapely

# Read in the CSV file
dat = pd.read_csv('airports.csv')

airports = ['LAX','SIN', 'OAX', 'LHR', 'LGW', 'BJX', 
        'BUD', 'PNQ', 'COK', 'MAA', 'DXB', 'WAW', 'NDC',
        'PMI','IBZ', 'BOM', 'SLC','FLL', 'BUR', 'FCA', 'INV',
        'MUC','ZRH','KUL']

trips = [('FLL','LAX'),('BUR','SLC'),
        ('LAX','LGW'),('LGW','EDI'),
        ('INV','LHR'),('LGW','LAX'),
        ('LAX','LHR'),('LHR','WAW'),
        ('WAW','MUC'),('MUC','PMI'),
        ('PMI','IBZ'),('PMI','ZRH'),
        ('ZRH','BUD'),('BUD','LHR'),
        ('LHR','LAX'),('LAX','SLC'),
        ('SLC','FCA'),('LAX','BJX'),
        ('BJX','OAX'),('OAX','LAX'),
        ('LAX','DXB'),('DXB','MAA'),
        ('MAA','PNQ'),('BOM','NDC'),
        ('PNQ','COK'),('COK','KUL'), ('KUL','SIN')]

# Make the map
fig, ax = plt.subplots(1,1,figsize=(16,9), subplot_kw={'projection': ccrs.PlateCarree()})
#ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines(color='white', linewidth=1.5)
ax.background_patch.set_facecolor('k')

for aa in airports:
#    print('Processing '+aa+'...')
    row = np.where(dat['iata_code']==aa)[0][0]
    lat = dat.loc[row,:]['latitude_deg']
    lon = dat.loc[row,:]['longitude_deg']
    ax.plot(lon,lat,'o',
            color='xkcd:electric pink',
         transform=ccrs.Geodetic(), alpha=0.7,
         markersize=3
         )
# Define the geometry for calculating cumulative distance
myGeod = geodesic.Geodesic()
totDist = 0
# Overlay the routes
for tt in trips:
    source = tt[0]
    dest = tt[1]
    sourceInd = np.where(dat['iata_code']==source)[0][0]
    destInd = np.where(dat['iata_code']==dest)[0][0]
    sourceLat = dat.loc[sourceInd,:]['latitude_deg']
    sourceLon = dat.loc[sourceInd,:]['longitude_deg']
    destLat = dat.loc[destInd,:]['latitude_deg']
    destLon = dat.loc[destInd,:]['longitude_deg']
    ax.plot([sourceLon, destLon],[sourceLat, destLat],
            color='xkcd:neon green',
         transform=ccrs.Geodetic(), linewidth=0.6, alpha=1,
        )
    shapelyObj = shapely.geometry.LineString([(sourceLon, destLon),(sourceLat, destLat)]) 
    # Cumulative distances
    totDist += myGeod.geometry_length(shapelyObj)

printStr = 'Total distance covered is {} km'.format(round(totDist/1e3, 3))
ax.text(0.1, 0.15, printStr, fontsize=18, color='xkcd:white', weight='heavy', transform=ax.transAxes)
print(printStr)
ax.set_xlim([-180,180])
ax.set_ylim([-90,90])
fig.savefig('map.pdf',bbox_inches='tight')
