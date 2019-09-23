"""
CS-4650 Project 1
Andrew Sison
Professor Lan Yang
"""
from pandas import Series, DataFrame
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Read csv file.
# The pad.csv contains purple air data from public purple air sensors,
# more specifically the sensor located in Cal Poly Pomona.
# The file includes information from PM levels of the atmosphere
# to the temperature from the dates of 6/10/19 to 9/10/19.
df = pd.read_csv("pad.csv")
df['created_at'] = pd.to_datetime(df['created_at'],format = "%Y-%m-%d %H:%M:%S %Z")

# 1 How much is each PM 1.0, 2.5, and 10 rising?
ax1 = df.plot(kind = 'line', x = 'created_at', y = 'PM1.0_CF_ATM_ug/m3', label = "PM 1.0",
             title = "PM Change")
df.plot(kind = 'line', x = 'created_at', y = 'PM2.5_CF_ATM_ug/m3', label = "PM 2.5", ax = ax1)
df.plot(kind = 'line', x = 'created_at', y = 'PM10.0_CF_ATM_ug/m3', label = "PM 10", ax = ax1)

# 2 Is there a correlation between temperature and PM?
ax2 = df.plot(kind = 'line', x = 'created_at', y = 'PM10.0_CF_ATM_ug/m3', label = "PM 10",
             title = "Temperature and PM")
df.plot(kind = 'line', x = 'created_at', y = 'Temperature_F', label = "Temperature (F)", ax = ax2)

# 3 Is there a correlation between Humidity and PM?
ax3 = df.plot(kind = 'line', x = 'created_at', y = 'PM10.0_CF_ATM_ug/m3', label = "PM 10",
             title = "Humidity and PM")
df.plot(kind = 'line', x = 'created_at', y = 'Humidity_%', label = "Humidity %", ax = ax3)

# 4 Is there a correlation between temperature and humidity?
ax4 = df.plot(kind = 'line', x = 'created_at', y = 'Temperature_F', label = "Temperature",
             title = "Temperature and humidity")
df.plot(kind = 'line', x = 'created_at', y = 'Humidity_%', label = "Humidity %", ax = ax4)
plt.figure()

# 5 What is the average temperature of each month?
df_my = df.groupby(df['created_at'].dt.strftime('%y%B'))['Temperature_F'].mean()
df_my.plot(kind = 'bar',  label = "Temperature", title = "Average temperature of each month")
plt.figure()

# 6 What is the average temperature of each day? 
# TODO: it currentl takes each months day and aggregates it
df_my = df.groupby(df['created_at'].dt.strftime('%y%b%a'))['Temperature_F'].mean()
df_my.plot(kind = 'bar',  label = "Temperature", title = "Average temperature of each day")
plt.show()
print(df.dtypes)