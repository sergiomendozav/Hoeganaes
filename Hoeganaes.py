import pandas as pd
import os
import glob
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
# from bokeh.plotting import figure, show, output_file


# Reading files and getting Dataframes
# ----------------------------------------------------------------------------------------------

# path ='/home/sergiomendozav/Documents/Hoeganaes/EAF/Logs' #path on ubuntu at home
path = '/home/sergio/Documents/Hoeganaes/EAF/Logs/LogsOk/CurrentPeriod'
allFiles = glob.glob(path + "/*.csv")
frame = pd.DataFrame()
frameKwh = pd.DataFrame()
Heats = pd.DataFrame()
Overview = pd.DataFrame()
list_ = []
listkwh_  = []
kwhTarget = 400

for file_ in allFiles:
    df = pd.read_csv(file_) #index_col='Time', parse_dates=True
    df.HeatNumber0LSW = int(file_[-9:-4]) #This is to set the HeatNumber0LSW 
    #with the correct Heat Number since there is a Bug in the Reporter with the Heat No.
    #during the conversion to CSV from RPH
    list_.append(df)
    #this IF filters the dataframes and only those where the OperKwhPerTon max value is less or equal than kwhTarget, get appended to the list.
    if df['OperKwhPerTon'].max() <= kwhTarget:
        listkwh_.append(df)

frame = pd.concat(list_, axis='rows')
frameKwh = pd.concat(listkwh_, axis='rows') #this frame contains only heats where the final OperKwhPerTon is less than the kwhTarget value.
GradeCrew = pd.DataFrame()
GradeCrew = pd.read_csv('GradeCrew.csv')
#merging dataframes
frame = pd.merge(frame,GradeCrew, left_on='HeatNumber0LSW', right_on='HeatNo')

# Calculated Variables
# ----------------------------------------------------------------------------------------------
frame['O2scfCarbInjLb'] = frame['TotalO2Cns']/frame['AdditionsCarbInj']
frame['HeatNumber'] = frame['HeatNumber0LSW']
frameKwh['O2scfCarbInjLb'] = frameKwh['TotalO2Cns']/frameKwh['AdditionsCarbInj']




# ----------------------------------------------------------------------------------------------


# Getting Column Names
# ----------------------------------------------------------------------------------------------
Columns_list = frame.columns.values.tolist() #this will bring the columns to a list

List = [X for X in Columns_list if 'SF' in X]
del Columns_list[0]
# ----------------------------------------------------------------------------------------------

# Getting Real Average Current
# ----------------------------------------------------------------------------------------------
frame['AvgCurrent'] = (frame.Current1 + frame.Current2 + frame.Current3)/3
frameNoZeros = frame[frame['AvgCurrent']>5]  #Frame without zeros on current
# ----------------------------------------------------------------------------------------------

# Additional frames
# ----------------------------------------------------------------------------------------------
# Stability Factor by TAP in SFTap dataframe
df1 = pd.DataFrame()
SFTap = pd.DataFrame()
SFTapList = []

for Tap in frame.ActFceTap_Px3.unique(): #this generates a For for Tap from 1 to 8
    df1 = frame[['MeanSF1','MeanSF2','MeanSF3','ActFceTap_Px3','OperKwhPerTon']][frame.ActFceTap_Px3 == Tap]
    SFTapList.append(df1)

SFTap = pd.concat(SFTapList, axis='rows')
SFTap = SFTap[SFTap.MeanSF1 < 300]
SFTap = SFTap[SFTap.MeanSF2 < 300]
SFTap = SFTap[SFTap.MeanSF3 < 300]
# ----------------------------------------------------------------------------------------------

# HeatGroups
# ----------------------------------------------------------------------------------------------
HeatGroupNoZeros = frameNoZeros.groupby('HeatNumber0LSW') #This only to get the average current without zeros.
HeatGroup = frame.groupby('HeatNumber0LSW')
GoodHeatsGroup = frameKwh.groupby('HeatNumber0LSW')
GroupHeatCharge = frame.groupby(['HeatNumber0LSW','ChargeNumber'])
GradeGroup = frame.groupby(['Grade','HeatNumber0LSW'])


for var in Columns_list:
    Heats[var] = HeatGroup[var].mean()
# ----------------------------------------------------------------------------------------------

Heats['Current1'] = HeatGroupNoZeros['Current1'].mean()
Heats['Current2'] = HeatGroupNoZeros['Current2'].mean()
Heats['Current3'] = HeatGroupNoZeros['Current3'].mean()
Heats['ZFeedback1'] = HeatGroupNoZeros['ZFeedback1'].mean()
Heats['ZFeedback2'] = HeatGroupNoZeros['ZFeedback2'].mean()
Heats['ZFeedback3'] = HeatGroupNoZeros['ZFeedback3'].mean()

Heats['HeatNumber3MSW'] = HeatGroup['HeatNumber3MSW'].last()
Heats['HeatNumber2'] = HeatGroup['HeatNumber2'].last()
Heats['HeatNumber1'] = HeatGroup['HeatNumber1'].last()
Heats['HeatNumber0LSW'] = HeatGroup['HeatNumber0LSW'].last()
Heats['ActualCHRG_PX3'] = HeatGroup['ActualCHRG_PX3'].last()
Heats['ChargeWt1Tons'] = HeatGroup['ChargeWt1Tons'].last()
Heats['ChargeWt2Tons'] = HeatGroup['ChargeWt2Tons'].last()
Heats['ChargeWt3Tons'] = HeatGroup['ChargeWt3Tons'].last()
Heats['ChargeWt4Tons'] = HeatGroup['ChargeWt4Tons'].last()
Heats['ChargeWt5Tons'] = HeatGroup['ChargeWt5Tons'].last()
Heats['ChargeWt6Tons'] = HeatGroup['ChargeWt6Tons'].last()
Heats['ChargeWt7Tons'] = HeatGroup['ChargeWt7Tons'].last()
Heats['ChargeWt8Tons'] = HeatGroup['ChargeWt8Tons'].last()
Heats['ChargeWt9Tons'] = HeatGroup['ChargeWt9Tons'].last()
Heats['ChargeWt10Tons'] = HeatGroup['ChargeWt10Tons'].last()
Heats['ChargeWt11Tons'] = HeatGroup['ChargeWt11Tons'].last()
Heats['ChargeWt12Tons'] = HeatGroup['ChargeWt12Tons'].last()
Heats['PwrProgNumberOV'] = HeatGroup['PwrProgNumberOV'].last()
Heats['SmartArcNumberOV'] = HeatGroup['SmartArcNumberOV'].last()
Heats['Ontime_PX3'] = HeatGroup['Ontime_PX3'].last()
Heats['OffTime_PX3'] = HeatGroup['OffTime_PX3'].last()
Heats['MWH_PX3'] = HeatGroup['MWH_PX3'].last()
Heats['ChargeMWH_PX3'] = HeatGroup['ChargeMWH_PX3'].last()
Heats['PwrPrgNum'] = HeatGroup['PwrPrgNum'].last()
Heats['NCCcounter1'] = HeatGroup['NCCcounter1'].last()
Heats['NCCcounter2'] = HeatGroup['NCCcounter2'].last()
Heats['NCCcounter3'] = HeatGroup['NCCcounter3'].last()
Heats['CIcounter1'] = HeatGroup['CIcounter1'].last()
Heats['CIcounter2'] = HeatGroup['CIcounter2'].last()
Heats['CIcounter3'] = HeatGroup['CIcounter3'].last()
Heats['I2H1'] = HeatGroup['I2H1'].last()                   
Heats['I2H2'] = HeatGroup['I2H2'].last()
Heats['I2H3'] = HeatGroup['I2H3'].last()
Heats['ChargeI2H1'] = HeatGroup['ChargeI2H1'].last()
Heats['ChargeI2H2'] = HeatGroup['ChargeI2H2'].last()
Heats['ChargeI2H3'] = HeatGroup['ChargeI2H3'].last()
Heats['HeatRWI1'] = HeatGroup['HeatRWI1'].last()                   
Heats['HeatRWI2'] = HeatGroup['HeatRWI2'].last()
Heats['HeatRWI3'] = HeatGroup['HeatRWI3'].last()
Heats['ChargeRWI1'] = HeatGroup['ChargeRWI1'].last()
Heats['ChargeRWI2'] = HeatGroup['ChargeRWI2'].last()
Heats['ChargeRWI3'] = HeatGroup['ChargeRWI3'].last()
Heats['TransformerTap'] = HeatGroup['TransformerTap'].max()
Heats['HeatMWHPLC'] = HeatGroup['HeatMWHPLC'].last()
Heats['ChrgMWH'] = HeatGroup['ChrgMWH'].last()
Heats['ChargeNumb'] = HeatGroup['ChargeNumb'].last()
Heats['ChargeWt1'] = HeatGroup['ChargeWt1'].last()
Heats['ChargeWt2'] = HeatGroup['ChargeWt2'].last()
Heats['ChargeWt3'] = HeatGroup['ChargeWt3'].last()
Heats['ChargeWt4'] = HeatGroup['ChargeWt4'].last()
Heats['ChargeWt5'] = HeatGroup['ChargeWt5'].last()
Heats['PwrOnTime'] = HeatGroup['PwrOnTime'].last()
Heats['TapTapTime'] = HeatGroup['TapTapTime'].last()
Heats['I2T1'] = HeatGroup['I2T1'].last()
Heats['I2T2'] = HeatGroup['I2T2'].last()
Heats['I2T3'] = HeatGroup['I2T3'].last()
Heats['CarbInject'] = HeatGroup['CarbInject'].last()
Heats['MasterProgramLog'] = HeatGroup['MasterProgramLog'].last()
Heats['HeatWt'] = HeatGroup['HeatWt'].last()
Heats['HeatKWHperTon'] = HeatGroup['HeatKWHperTon'].last()
Heats['ChargeKWHperTon'] = HeatGroup['ChargeKWHperTon'].last()
Heats['OperKwhPerTon'] = HeatGroup['OperKwhPerTon'].last()
Heats['HeatAvgMW'] = HeatGroup['HeatAvgMW'].last()
Heats['HeatI2HperMWH'] = HeatGroup['HeatI2HperMWH'].last()
Heats['HeatAvgI2H'] = HeatGroup['HeatAvgI2H'].last()
Heats['ChargeAvgMW'] = HeatGroup['ChargeAvgMW'].last()                
Heats['ChrgI2HperMWH'] = HeatGroup['ChrgI2HperMWH'].last()
Heats['ChrgAvgI2H'] = HeatGroup['ChrgAvgI2H'].last()
Heats['PowerProg'] = HeatGroup['PowerProg'].last()
Heats['BalanceProg'] = HeatGroup['BalanceProg'].last()
Heats['BackChrgProg'] = HeatGroup['BackChrgProg'].last()
Heats['BurnerProg'] = HeatGroup['BurnerProg'].last()              #should be oxiprofile
Heats['ValidTempSample'] = HeatGroup['ValidTempSample'].last()      
Heats['ValidPPMSample'] = HeatGroup['ValidPPMSample'].last()
Heats['ValidCarbonSample'] = HeatGroup['ValidCarbonSample'].last()
Heats['ValidNewSample'] = HeatGroup['ValidNewSample'].last()
Heats['LimeCharged'] = HeatGroup['LimeCharged'].last()
Heats['Tot_LimeInj'] = HeatGroup['Tot_LimeInj'].last()
Heats['Charge_Carb'] = HeatGroup['Charge_Carb'].last()
Heats['B1_GasCns'] = HeatGroup['B1_GasCns'].last()
Heats['B1_O2MainCns'] = HeatGroup['B1_O2MainCns'].last()
Heats['B1_CarbonCns'] = HeatGroup['B1_CarbonCns'].last()
Heats['B2_GasCns'] = HeatGroup['B2_GasCns'].last()
Heats['B2_O2MainCns'] = HeatGroup['B2_O2MainCns'].last()
Heats['B2_CarbonCns'] = HeatGroup['B2_CarbonCns'].last()
Heats['B3_GasCns'] = HeatGroup['B3_GasCns'].last()
Heats['B3_O2MainCns'] = HeatGroup['B3_O2MainCns'].last()
Heats['B3_LimeCns'] = HeatGroup['B3_LimeCns'].last()
Heats['TotalGasCns'] = HeatGroup['TotalGasCns'].last()
Heats['TotalO2Cns'] = HeatGroup['TotalO2Cns'].last()
Heats['AdditionsLimeCharge'] = HeatGroup['AdditionsLimeCharge'].last()
Heats['AdditionsCarbCharg'] = HeatGroup['AdditionsCarbCharg'].last()
Heats['AdditionsLimeInj'] = HeatGroup['AdditionsLimeInj'].last()
Heats['AdditionsCarbInj'] = HeatGroup['AdditionsCarbInj'].last()
Heats['Scrap1Wt'] = HeatGroup['Scrap1Wt'].last()
Heats['Scrap2Wt'] = HeatGroup['Scrap2Wt'].last()
Heats['Scrap3Wt'] = HeatGroup['Scrap3Wt'].last()
Heats['Scrap4Wt'] = HeatGroup['Scrap4Wt'].last()
Heats['Scrap5Wt'] = HeatGroup['Scrap5Wt'].last()
Heats['Scrap6Wt'] = HeatGroup['Scrap6Wt'].last()
Heats['Scrap7Wt'] = HeatGroup['Scrap7Wt'].last()
Heats['Scrap8Wt'] = HeatGroup['Scrap8Wt'].last()
Heats['Scrap9Wt'] = HeatGroup['Scrap9Wt'].last()
Heats['Scrap10Wt'] = HeatGroup['Scrap10Wt'].last()
Heats['O2scfCarbInjLb'] = HeatGroup['O2scfCarbInjLb'].last()

Overview['PON'] = Heats['Ontime_PX3']
Overview['T2T'] = Heats['TapTapTime']
Overview['MWH'] = Heats['MWH_PX3']
Overview['HeatkWhTon'] = Heats['OperKwhPerTon'] 
Overview['I2H1'] = Heats['I2H1']
Overview['I2H2'] = Heats['I2H2']
Overview['I2H3'] = Heats['I2H3']
Overview['AvgCurr'] = (Heats['Current1']+Heats['Current2']+Heats['Current3'])/3
Overview['PrimVolts'] = Heats['PrimaryVolts']
Overview['B1Gas'] = Heats['B1_GasCns']
Overview['B1O2Main'] = Heats['B1_O2MainCns']
Overview['B1Carbon'] = Heats['B1_CarbonCns']
Overview['B2Gas'] = Heats['B2_GasCns']
Overview['B2O2Main'] = Heats['B2_O2MainCns']
Overview['B2Carbon'] = Heats['B2_CarbonCns']
Overview['B3Gas'] = Heats['B3_GasCns']
Overview['B3O2Main'] = Heats['B3_O2MainCns']
Overview['B3Lime'] = Heats['B3_LimeCns']
Overview['TotalGasCns'] = Heats['TotalGasCns']
Overview['TotalO2Cns'] = Heats['TotalO2Cns']
Overview['TotalCarbonCns'] = Heats['TotalCarbonCns']
Overview['O2scfCarbInjLb'] = Heats['O2scfCarbInjLb']
Overview['HeatNumber'] = Heats['HeatNumber0LSW']

OverviewShort = Overview[['PON','T2T','MWH','HeatkWhTon','HeatNumber']]
OverviewMelted = pd.melt(OverviewShort,id_vars='HeatNumber',var_name='KPI')



# Plotting
# ----------------------------------------------------------------------------------------------


# plt.figure()
# HeatGroup['O2scfCarbInjLb'].plot()
# plt.legend()
# GoodHeatsGroup['B1_O2MainFlow'].plot()
# HeatGroup['B1_O2MainFlow'].plot()
# plt.show()


# MWH 1st Charge Histogram
# +++++++++++++++++++
MWH1 = GroupHeatCharge['MWH_PX3'].max()
MWH1 = MWH1.unstack()[1]  #this obtains the max MWH from charge 1 of the heats
# n, bins, patches = plt.hist(x = MWH1,bins=20, color='#0504aa', alpha=0.7, rwidth=0.9 )
# plt.grid(axis='y', alpha=0.75)
# plt.xlabel('MWH')
# plt.ylabel('Frequency')
# plt.title('MWH 1st Charge')
# plt.show()

# this is another option...
# sns.distplot(MWH1)
# plt.xlim(0,16)
# plt.show()


# kWh/Ton 1st Charge Histogram
# +++++++++++++++++++
# plt.figure()
# kwhTon1 = GroupHeatCharge['OperKwhPerTon'].max().unstack()[1]  #this gets OperKwhPerTon of 1st Charge only
# k1 = kwhTon1 + 50  #this is just an example on how to make histograms overlap
# plt.hist(kwhTon1, bins=49, alpha=0.5)   
# plt.hist(k1, bins=49, alpha=0.5 )    #this is just an example on how to make histograms overlap
# plt.xlabel('kWh/Ton')
# plt.ylabel('Frequency')
# plt.title('kWh/Ton 1st Charge')
# plt.savefig('kwhTon1stCharge.png', bbox_inches='tight')
# plt.show()



# OverviewShort Pairplot
# +++++++++++++++++++
# sns.set()
# sns.pairplot(OverviewShort)
# plt.show()

# T2T vs HeatkWhTon
# +++++++++++++++++++
# sns.lmplot(x='T2T',y='HeatkWhTon',data=Overview, fit_reg=False)
# plt.ylim(300,500)
# plt.xlim(25,125)
# plt.show()

# HeatAvgMW
# +++++++++++++++++++
# Heats.HeatAvgMW.plot()
# plt.show()


# All Overview Boxplot
# +++++++++++++++++++
# sns.boxplot(data=Overview)
# plt.show()

# KPI swarmplot
# +++++++++++++++++++
# sns.swarmplot(x='KPI',y='value',data=OverviewMelted, hue='HeatNumber',dodge=True)
# plt.legend(bbox_to_anchor=(1,1), loc=2)
# plt.show()










MWH1 = GroupHeatCharge['MWH_PX3'].max()
MWH1 = MWH1.unstack()[1]  #this obtains the max MWH from charge 1 of the heats


GradeList = GradeGroup.Ontime_PX3.max().unstack()

GradeGroup.Ontime_PX3.max() #.reset_index()


plt.figure()
#x_pos = np.arange(len(GradeGroup.Grade.unique()))
x_pos =np.arange(0,7)
bars = GradeGroup.Ontime_PX3.max()
plt.bar(x_pos, bars, align='center', alpha=0.5)
plt.xticks(x_pos,GradeGroup.Grade.unique())
plt.ylabel('minutes')
plt.title('Power On Time per Grade')
plt.show()

# MeanSF Taps 3 to 6 Histograms
# +++++++++++++++++++
var13 = SFTap['MeanSF1'][SFTap.ActFceTap_Px3 == 3]
var23 = SFTap['MeanSF2'][SFTap.ActFceTap_Px3 == 3]
var33 = SFTap['MeanSF3'][SFTap.ActFceTap_Px3 == 3]
var14 = SFTap['MeanSF1'][SFTap.ActFceTap_Px3 == 4]
var24 = SFTap['MeanSF2'][SFTap.ActFceTap_Px3 == 4]
var34 = SFTap['MeanSF3'][SFTap.ActFceTap_Px3 == 4]
var15 = SFTap['MeanSF1'][SFTap.ActFceTap_Px3 == 5]
var25 = SFTap['MeanSF2'][SFTap.ActFceTap_Px3 == 5]
var35 = SFTap['MeanSF3'][SFTap.ActFceTap_Px3 == 5]
var16 = SFTap['MeanSF1'][SFTap.ActFceTap_Px3 == 6]
var26 = SFTap['MeanSF2'][SFTap.ActFceTap_Px3 == 6]
var36 = SFTap['MeanSF3'][SFTap.ActFceTap_Px3 == 6]

# plt.figure()
# plt.subplot(221)
# plt.hist([var13, var23, var33],bins = 10, rwidth = 0.85, alpha=0.5, label = ['SF1','SF2','SF3'])
# plt.legend(loc='upper right')
# plt.title('SF Tap 3')
# plt.ylabel('Frequency')
# plt.subplot(222)
# plt.hist([var14, var24, var34],bins = 10, rwidth = 0.85, alpha=0.5, label = ['SF1','SF2','SF3'])
# plt.title('SF Tap 4')
# plt.ylabel('Frequency')
# plt.legend(loc='upper right')
# plt.subplot(223)
# plt.hist([var15, var25, var35],bins = 10, rwidth = 0.85, alpha=0.5, label = ['SF1','SF2','SF3'])
# plt.title('SF Tap 5')
# plt.ylabel('Frequency')
# plt.legend(loc='upper right')
# plt.subplot(224)
# plt.hist([var16, var26, var36],bins = 10, rwidth = 0.85, alpha=0.5, label = ['SF1','SF2','SF3'])
# plt.title('SF Tap 6')
# plt.ylabel('Frequency')
# plt.legend(loc='upper right')
# plt.show()


# SF over OperKwhPerTon Tap 6
# +++++++++++++++++++
# +++++++++++++++++++
x = SFTap['OperKwhPerTon'][SFTap.ActFceTap_Px3 == 6]
y1 = SFTap['MeanSF1'][SFTap.ActFceTap_Px3 == 6]
y2 = SFTap['MeanSF2'][SFTap.ActFceTap_Px3 == 6]
y3 = SFTap['MeanSF3'][SFTap.ActFceTap_Px3 == 6]

# plt.figure()

# plt.subplot(131)
# plt.scatter(x,y1,alpha=0.8, s=10)
# plt.title('SF1 over OperKwhPerTon')
# plt.xlabel('kWh/ton')
# plt.ylabel('SF1')
# plt.xlim(220,340)
# plt.ylim(0,120)

# plt.subplot(132)
# plt.scatter(x,y2,alpha=0.8, s=10)
# plt.title('SF2 over OperKwhPerTon')
# plt.xlabel('kWh/ton')
# plt.ylabel('SF2')
# plt.xlim(220,340)
# plt.ylim(0,120)

# plt.subplot(133)
# plt.scatter(x,y3,alpha=0.8, s=10)
# plt.title('SF3 over OperKwhPerTon')
# plt.xlabel('kWh/ton')
# plt.ylabel('SF3')
# plt.xlim(220,340)
# plt.ylim(0,120)

# plt.show()


# T2T distplot
# +++++++++++++++++++
# sns.distplot(Overview.T2T)
# plt.xlim(0,120)
# plt.show()

# Moka Injection Trend
# +++++++++++++++++++
# CarbonCnsMax = HeatGroup[['B1_CarbonCns','B2_CarbonCns']].max()
# CarbonCnsMax.plot(style='.-')
# plt.show()

# Primary Volts Plot
# +++++++++++++++++++
# plt.figure()
# plt.subplot(111)
# plt.title('Primary Volts kV')
# plt.ylabel('kV')
# plt.ylim(13.0,15.0)
# plt.plot(Heats.PrimVolts)
# plt.show()

# Power On Time Histogram
# +++++++++++++++++++
# plt.figure()
# plt.subplot(111)
# plt.title('Power On Time')
# plt.ylabel('Frequency')
# plt.xlabel('Minutes')
# plt.plot(Heats.PON)
# plt.show()



# Write to Excel
# ----------------------------------------------------------------------------------------------
writer = pd.ExcelWriter('Heats.xlsx')
Heats.to_excel(writer,'Heats')
Overview.to_excel(writer,'Overview')
writer.save()






# Heats.loc[19096,:]  #returns all columns for that specific Heat


# HeatGroup.PrimaryVolts.mean().plot(style='.')
# plt.show()

# toplot = frame['Current1'][frame['HeatNumber0LSW']==19096]  this way I can trend a specific variable of a specific heat
# toplot = frame['Current1'][frame['HeatNumber0LSW']==19096]
# toplot = frame['Current1'][frame['HeatNumber0LSW']==19096][500:1000] #to get specific time range from 600 to 1050
# toplot.plot()
# plt.show()
# toplot.mean()