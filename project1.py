"""
CS-4650 Project 1
Andrew Sison
Professor Lan Yang
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas import Series, DataFrame
from datetime import datetime, timedelta

# Remove any outliers from the given dataframe's column and 
# return the cleaned data in a new dataframe
def remove_outlier(df_in, col_name):
    q1 = df_in[col_name].quantile(0.25)
    q3 = df_in[col_name].quantile(0.75)
    iqr = q3-q1 # Interquartile range
    fence_low  = q1-1.5*iqr
    fence_high = q3+1.5*iqr
    return df_in.loc[(df_in[col_name] > fence_low) & (df_in[col_name] < fence_high)]

# Read csv file.
# The .csv  file contains purple air data from https://www.purpleair.com/sensorlist,
# more specifically the sensor located in Cal Poly Pomona.
# The file includes information from PM levels of the atmosphere
# to the temperature from the approximate time of
# 2019-02-06 19:36:20+00:00 to 207857 2019-09-27 23:59:47+00:00  
df = pd.read_csv('CCA_CalPolyPomona (34.057830404602164 -117.82446560796507) Primary 01_01_2019 9_29_19.csv')
df['created_at'] = pd.to_datetime(df['created_at'],format = "%Y-%m-%d %H:%M:%S %Z")

# Remove outliers in the inputed columns
df = remove_outlier(df,'Temperature_F')
df = remove_outlier(df,'Humidity_%')
df = remove_outlier(df,'PM1.0_CF_ATM_ug/m3')
df = remove_outlier(df,'PM2.5_CF_ATM_ug/m3')
df = remove_outlier(df,'PM10.0_CF_ATM_ug/m3')

# top and bottom of the limits for the PM change over time graphs
ytop = 60
ybot = -5
# Healthy PM standards
pmStandard1 = 35 # 24-hour PM 2.5
pmStandard2 = 12 # Annual PM 2.5
pmStandard3 = 150 # Annual PM 10.0

# Figure_1 PM 1.0, 2.5, and 10 change over time
ax1 = df.plot(kind = 'line', x = 'created_at', y = 'PM1.0_CF_ATM_ug/m3', label = "PM 1.0",
             title = "PM change over time")
df.plot(kind = 'line', x = 'created_at', y = 'PM2.5_CF_ATM_ug/m3', label = "PM 2.5", ax = ax1)
df.plot(kind = 'line', x = 'created_at', y = 'PM10.0_CF_ATM_ug/m3', label = "PM 10", ax = ax1)
plt.xlabel("")
plt.ylim(ybot,ytop)

# Figure_2 PM 1.0 change over time
df.plot(kind = 'line', color = 'orange',x = 'created_at', y = 'PM1.0_CF_ATM_ug/m3', label = "PM 1.0", title = "PM 1.0 change over time")
plt.xlabel("")
plt.ylim(ybot,ytop)

# Figure_3 Is there a correlation between temperature and PM?
ax2 = df.plot(kind = 'line', x = 'created_at', y = 'PM10.0_CF_ATM_ug/m3', label = "PM 10",
             title = "Temperature and PM")
df.plot(kind = 'line', x = 'created_at', y = 'Temperature_F', label = "Temperature (F)", ax = ax2)
plt.xlabel("")

# Figure_4 Is there a correlation between Humidity and PM?
ax3 = df.plot(kind = 'line', x = 'created_at', y = 'PM10.0_CF_ATM_ug/m3', label = "PM 10",
             title = "Humidity and PM")
df.plot(kind = 'line', x = 'created_at', y = 'Humidity_%', label = "Humidity %", ax = ax3)
plt.xlabel("")

# Figure_5 Is there a correlation between temperature and humidity?
ax4 = df.plot(kind = 'line', x = 'created_at', y = 'Temperature_F', label = "Temperature",
             title = "Temperature and humidity")
df.plot(kind = 'line', x = 'created_at', y = 'Humidity_%', label = "Humidity %", ax = ax4)
plt.xlabel("")
plt.figure()

# Figure_6 median temperature of each month 
df_my = df.groupby(df['created_at'].dt.strftime('%m-%y'))['Temperature_F'].median()
df_my.plot(kind = 'bar',  label = "Temperature", title = "Median temperature of each month")
plt.xlabel('Date: mm-yy')
plt.ylabel("Degrees Fahrenheit")
plt.figure()

# Figure_7 median temperature of each day
df_mt = df.groupby(df['created_at'].dt.strftime('%m/%d/%y'))['Temperature_F'].median()
# df_m25 = df.groupby(df['created_at'].dt.strftime('%m/%d/%y'))['PM2.5_CF_ATM_ug/m3'].median()
# ax5 = df_m25.plot(kind = 'line',  label = "PM2.5_CF_ATM_ug/m3")
df_mt.plot(kind = 'line',  label = "Temperature", title = "Median temperature of each day")
plt.ylim(0,120)
plt.xlabel("")
plt.ylabel("Degrees Fahrenheit")
plt.figure()

# Figure_8 median humidity of each month
df_my = df.groupby(df['created_at'].dt.strftime('%m-%y'))['Humidity_%'].median()
df_my.plot(kind = 'bar',  label = "Temperature", title = "Median humididty % of each month")
plt.xlabel('Date: mm-yy')
plt.ylabel("Humidity %")
plt.figure()

# Figure_9 median humidity of each day
df_my = df.groupby(df['created_at'].dt.strftime('%m/%d/%y'))['Humidity_%'].median()
df_my.plot(kind = 'line',  label = "Temperature", title = "Median humidity % of each day")
plt.ylim(0,100)
plt.xlabel("")
plt.ylabel("Humidity %")

# 10 PM 2.5 vs Temperature
df.plot(kind = 'scatter', x = 'Temperature_F', y ='PM2.5_CF_ATM_ug/m3', title = "PM 2.5 vs Temperature")

# 11 PM 2.5 vs Humidity
df.plot(kind = 'scatter', x = 'Humidity_%', y ='PM2.5_CF_ATM_ug/m3', title = "PM 2.5 vs Humidity")


plt.show()
