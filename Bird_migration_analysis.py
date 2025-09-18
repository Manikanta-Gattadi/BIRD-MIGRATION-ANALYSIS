import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Load data
birddata = pd.read_csv("bird_tracking.csv")

bird_names = pd.unique(birddata.bird_name)

# 1. Plot trajectories of all birds
plt.figure(figsize=(7,7))
for name in bird_names:
    ix = birddata.bird_name == name
    plt.plot(birddata.longitude[ix], birddata.latitude[ix], '.', label=name)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.legend(loc="lower right")
plt.show()

# 2. Speed histogram for Eric
speed = birddata.loc[birddata.bird_name == "Eric", "speed_2d"]
plt.figure(figsize=(8,4))
plt.hist(speed.dropna(), bins=np.linspace(0,30,20), density=True)
plt.xlabel("2D Speed (m/s)")
plt.ylabel("Frequency")
plt.show()

# 3. Add timestamp column
birddata["timestamp"] = pd.to_datetime(birddata.date_time.str[:-3], format="%Y-%m-%d %H:%M:%S")

# 4. Elapsed time for Eric
times = birddata.loc[birddata.bird_name=="Eric", "timestamp"]
elapsed_days = (times - times.iloc[0]).dt.total_seconds() / (24*3600)
plt.plot(elapsed_days)
plt.xlabel("Observation")
plt.ylabel("Elapsed Time (days)")
plt.show()

# 5. Daily mean speed for Eric
data = birddata[birddata.bird_name=="Eric"].copy()
elapsed_days = (data.timestamp - data.timestamp.iloc[0]).dt.days
daily_mean_speed = data.groupby(elapsed_days)["speed_2d"].mean()
plt.figure(figsize=(8,6))
plt.plot(daily_mean_speed, "rs-")
plt.xlabel("Day")
plt.ylabel("Mean Speed (m/s)")
plt.show()

# 6. Plot trajectories on map with Cartopy
proj = ccrs.Mercator()
plt.figure(figsize=(10,10))
ax = plt.axes(projection=proj)
ax.set_extent((-25.0, 20.0, 52.0, 10.0))
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')
for name in bird_names:
    ix = birddata.bird_name == name
    ax.plot(birddata.longitude[ix], birddata.latitude[ix], '.', transform=ccrs.Geodetic(), label=name)
plt.legend(loc="upper left")
plt.show()

