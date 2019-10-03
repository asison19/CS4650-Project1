"""
This file contains the data visualizations for the PM 2.5 Levels
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pytz
import datetime as dt
from pandas import Series, DataFrame


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
# The other two are from Santa Rosa, and LA respectively.
# The file includes information from PM levels of the atmosphere
# to the temperature from the approximate time of
# 2019-02-06 19:36:20+00:00 to 207857 2019-09-27 23:59:47+00:00  
df = pd.read_csv('CCA_CalPolyPomona (34.057830404602164 -117.82446560796507) Primary 01_01_2019 9_29_19.csv')
df2 = pd.read_csv('Santa_Rosa_Proctor_Heights (38.45648266062277 -122.6874994253784) Primary 02_6_2019 09_27_2019.csv')
df3 = pd.read_csv('USCEHC Lincoln Heights (34.0684583071038 -118.2063889503479) Primary 02_6_2019 09_27_2019.csv')

df['created_at'] = pd.to_datetime(df['created_at'],format = "%Y-%m-%d %H:%M:%S %Z")
df2['created_at'] = pd.to_datetime(df2['created_at'],format = "%Y-%m-%d %H:%M:%S %Z")
df3['created_at'] = pd.to_datetime(df3['created_at'],format = "%Y-%m-%d %H:%M:%S %Z")

# Remove outliers in the inputed columns
df = remove_outlier(df,'Temperature_F')
df = remove_outlier(df,'Humidity_%')
df = remove_outlier(df,'PM2.5_CF_ATM_ug/m3')
df2 = remove_outlier(df2,'Temperature_F')
df2 = remove_outlier(df2,'Humidity_%')
df2 = remove_outlier(df2,'PM2.5_CF_ATM_ug/m3')
df3 = remove_outlier(df3,'Temperature_F')
df3 = remove_outlier(df3,'Humidity_%')
df3 = remove_outlier(df3,'PM2.5_CF_ATM_ug/m3')

# top and bottom of the limits for the PM change over time graphs
ytop = 50
ybot = 0
# Healthy PM standards
pmStandard1 = 35 # 24-hour PM 2.5
pmStandard2 = 12 # Annual PM 2.5

# Figure_1 PM 2.5 change over time
df.plot(kind = 'line', color = 'orange',x = 'created_at', y = 'PM2.5_CF_ATM_ug/m3', label = "PM 2.5",title = "PM 2.5 change over time of Cal Poly Pomona")
plt.xlabel('Date')
plt.ylabel("ug/m3")
plt.axhline(y=pmStandard1, color='r', linestyle='dashed', label = str(pmStandard1) + " ug/m3")
plt.axhline(y=pmStandard2, color='r', linestyle='solid', label = str(pmStandard2) + " ug/m3")
plt.ylim(ybot,ytop)
plt.legend()
plt.figure()

# Figure_2 Median PM 2.5 of each month
df_my = df.groupby(df['created_at'].dt.strftime('%m-%Y'))['PM2.5_CF_ATM_ug/m3'].median()
df_my.plot(kind = 'bar',  label = "PM 2.5", title = "Median PM 2.5 of each month of Cal Poly Pomona")
plt.xlabel('Date: mm-yyyy')
plt.ylabel("ug/m3")
plt.axhline(y=pmStandard1, color='r', linestyle='dashed', label = str(pmStandard1) + " ug/m3")
plt.axhline(y=pmStandard2, color='r', linestyle='solid', label =  str(pmStandard2) + " ug/m3")
plt.ylim(ybot,ytop)
plt.legend()
plt.figure()

# Figure_3 Median PM 2.5 of each day
df_mdy = df.groupby(df['created_at'].dt.strftime('%m/%d/%y'))['PM2.5_CF_ATM_ug/m3'].median()
df_mdy.plot(kind = 'line',  label = "PM 2.5", title = "Median PM 2.5 of each day of Cal Poly Pomona")
plt.xlabel("Date")
plt.ylabel("ug/m3")
plt.axhline(y=pmStandard1, color='r', linestyle='dashed', label = str(pmStandard1) + " ug/m3")
plt.axhline(y=pmStandard2, color='r', linestyle='solid', label = str(pmStandard2) + " ug/m3")
semesterStart = mdates.date2num(dt.datetime(2019,8,22))
plt.axvline(semesterStart,color='r')
plt.ylim(ybot,ytop)
plt.legend()
plt.figure()

# Figure_4 Median PM 2.5 of each month including Santa Rosa and LA
df2_my = df2.groupby(df2['created_at'].dt.strftime('%m-%Y'))['PM2.5_CF_ATM_ug/m3'].median()
df3_my = df3.groupby(df3['created_at'].dt.strftime('%m-%Y'))['PM2.5_CF_ATM_ug/m3'].median()

df3_my.plot(kind = 'bar', stacked = True,  label = "Los Angeles", color = 'green')
df_my.plot(kind = 'bar', stacked = True, label = "Cal Poly Pomona", title = "Median PM 2.5 of each month")
df2_my.plot(kind = 'bar', stacked = True,  label = "Santa Rosa", color = 'orange')
plt.axhline(y=pmStandard1, color='r', linestyle='dashed', label = str(pmStandard1) + " ug/m3")
plt.axhline(y=pmStandard2, color='r', linestyle='solid', label = str(pmStandard2) + " ug/m3")
plt.xlabel('Date: mm-yyyy')
plt.ylabel("ug/m3")
plt.legend()
plt.ylim(ybot,ytop)
plt.figure()

# Figure_5 Median PM 2.5 of each day including Santa Rosa and LA
df2_mdy = df2.groupby(df2['created_at'].dt.strftime('%m/%d/%y'))['PM2.5_CF_ATM_ug/m3'].median()
df3_mdy = df3.groupby(df3['created_at'].dt.strftime('%m/%d/%y'))['PM2.5_CF_ATM_ug/m3'].median()

df_mdy.plot(kind = 'line', label = "Cal Poly Pomona", title = "Median PM 2.5 of each day")
df2_mdy.plot(kind = 'line',  label = "Santa Rosa", color = 'orange')
df3_mdy.plot(kind = 'line',  label = "Los Angeles", color = 'green')
plt.axhline(y=pmStandard1, color='r', linestyle='dashed', label = str(pmStandard1) + " ug/m3")
plt.axhline(y=pmStandard2, color='r', linestyle='solid', label = str(pmStandard2) + " ug/m3")
plt.axvline(semesterStart,color='r')
plt.xlabel('Date')
plt.ylabel("ug/m3")
plt.legend()
plt.ylim(ybot,ytop)
plt.figure()

# Figure_6 PM 2.5, Temperature, and Humidity by day
df_temp = df.groupby(df['created_at'].dt.strftime('%m/%d/%y'))['Temperature_F'].median()
df_hum = df.groupby(df['created_at'].dt.strftime('%m/%d/%y'))['Humidity_%'].median()

df_mdy.plot(kind = 'line', label = "PM 2.5", title = "PM 2.5, Temperature, and Humidity")
df_temp.plot(kind = 'line', label = "Temperature_F")
df_hum.plot(kind = 'line', label = "Humidity %")
plt.figure()

# Figure_7 PM 2.5, Temperature, and Humidity by month
df_temp = df.groupby(df['created_at'].dt.strftime('%m/%y'))['Temperature_F'].median()
df_hum = df.groupby(df['created_at'].dt.strftime('%m/%y'))['Humidity_%'].median()

df_my.plot(kind = 'line', label = "PM 2.5", title = "PM 2.5, Temperature, and Humidity")
df_temp.plot(kind = 'line', label = "Temperature_F")
df_hum.plot(kind = 'line', label = "Humidity %")
plt.xlabel('Date')
plt.legend()

plt.show()
