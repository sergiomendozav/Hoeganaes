import pandas as pd
import os
import glob
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from bokeh.plotting import figure, show, output_file


path ='/home/sergiomendozav/Documents/Hoeganaes/EAF/Logs'
allFiles = glob.glob(path + "/*.csv")
frame = pd.DataFrame()
Heats = pd.DataFrame()
list_ = []
for file_ in allFiles:
    df = pd.read_csv(file_) #index_col='Time', parse_dates=True
    df.HeatNumber0LSW = int(file_[-9:-4]) #This is to set the HeatNumber0LSW 
    #with the correct Heat Number since there is a Bug in the Reporter with the Heat No.
    #during the conversion to CSV from RPH
    list_.append(df)
frame = pd.concat(list_, axis='rows')

Columns_list = frame.columns.values.tolist() #this will bring the columns to a list

List = [X for X in Columns_list if 'Heat' in X]

frame['Impedance1'] = frame.Voltage1/frame.Current1
frame['Impedance2'] = frame.Voltage2/frame.Current2
frame['Impedance3'] = frame.Voltage3/frame.Current3

frame['AvgCurrent'] = (frame.Current1 + frame.Current2 + frame.Current3)/3
frameNoZeros = frame[frame['AvgCurrent']>5]  #Frame without zeros on current

HeatGroupNoZeros = frameNoZeros.groupby('HeatNumber0LSW') #This only to get
#the average current without zeros.
HeatGroup = frame.groupby('HeatNumber0LSW')



Heats['Current1'] = HeatGroupNoZeros['Current1'].mean()
Heats['HeatKWHperTon'] = HeatGroup['HeatKWHperTon'].max()

#Heats.loc[18801,:]  returns all columns for that specific Heat







#CarbonCnsMax = HeatGroup[['B1_CarbonCns','B2_CarbonCns']].max()
#CarbonCnsMax.plot(style='.-')
#plt.show()

#HeatGroup.PrimaryVolts.mean().plot(style='.')
#plt.show()
