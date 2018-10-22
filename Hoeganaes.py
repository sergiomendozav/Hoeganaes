import pandas as pd
import os
import glob
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from bokeh.plotting import figure, show, output_file
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes 
from mpl_toolkits.axes_grid1.inset_locator import mark_inset


# Reading files and getting Dataframes
# ----------------------------------------------------------------------------------------------

PathCurrentPeriod = '/home/sergio/Documents/Hoeganaes/EAF/Logs/LogsOk/CurrentPeriod'
allFiles = glob.glob(PathCurrentPeriod + "/*.csv")
frame = pd.DataFrame()
Heats = pd.DataFrame()
Overview = pd.DataFrame()
list_ = []
 
for file_ in allFiles:
    df = pd.read_csv(file_) #index_col='Time', parse_dates=True
    df.HeatNumber0LSW = int(file_[-9:-4]) #This is to set the HeatNumber0LSW with the correct Heat Number since there is a Bug in the Reporter with the Heat No. during the conversion to CSV from RPH
    # df = df.loc[:, (df != 0).any(axis=0)] #remove all columns where data is always 0.
    df = df[['Current1', 'Current2', 'Current3', 'Voltage1', 'Voltage2', 'Voltage3', 'MVA1', 'MVA2', 'MVA3', 'MW1','MW2', 'MW3', 'MVAR1', 'MVAR2', 'MVAR3', 'PF1', 'PF2', 'PF3', 'MVATot', 'MWTot', 'MVARTot', 'PFTot', 'ZFeedback1', 'ZFeedback2', 'ZFeedback3', 'Res1', 'Res2', 'Res3', 'Reactance1', 'Reactance2', 'Reactance3', 'ArcLength1', 'ArcLength2','ArcLength3', 'RWI1', 'RWI2', 'RWI3', 'NeutralCurrent', 'NeutralVolts', 'Normalized Neutral Current', 'Normalized Neutral Voltage','PrimaryVolts', 'VoltageLineToLine12', 'VoltageLineToLine23', 'VoltageLineToLine31', 'PhasorAngleV1I1', 'PhasorAngleV1I2', 'PhasorAngleV1I3', 'PhasorAngleV1V2', 'PhasorAngleV1V3', 'CurrentLoadPercent1', 'CurrentLoadPercent2', 'CurrentLoadPercent3','CurrentLoadPercentAvg', 'Y1', 'Y2', 'Y3', 'ArcResistance1', 'ArcResistance2', 'ArcResistance3', 'ArcEfficiency1', 'ArcEfficiency2', 'ArcEfficiency3', 'ExtinctionVoltage1', 'ExtinctionVoltage2', 'ExtinctionVoltage3', 'ReignitionVoltage1', 'ReignitionVoltage2', 'ReignitionVoltage3', 'ArcMeanPower1', 'ArcMeanPower2', 'ArcMeanPower3', 'ArcVoltage1', 'ArcVoltage2','ArcVoltage3', 'ActFceTap_Px3', 'ActReaTap_Px3', 'HeatNumber0LSW', 'ActualCHRG_PX3', 'ChargeWt1Tons', 'ChargeWt2Tons', 'ChargeWt3Tons', 'Ontime_PX3', 'OffTime_PX3', 'EPos1_PX3', 'EPos2_PX3', 'EPos3_PX3', 'MWH_PX3', 'ElectrodeSpeed1_PX3', 'ElectrodeSpeed2_PX3','ElectrodeSpeed3_PX3', 'RawElectrodePosition1', 'RawElectrodePosition2', 'RawElectrodePosition3','RegOut1', 'RegOut2', 'RegOut3', 'Sp1CurrentReg', 'ChargeNumber', 'Sp1Imped', 'Sp2Imped', 'Sp3Imped', 'CIcounter1', 'CIcounter2', 'CIcounter3', 'SF1', 'SF2', 'SF3', 'VoltSF1', 'VoltSF2', 'VoltSF3',  'MeanSF1','MeanSF2', 'MeanSF3', 'MeanVoltSF1', 'MeanVoltSF2', 'MeanVoltSF3','MeanCurrent1', 'MeanCurrent2', 'MeanCurrent3', 'MeanVoltage1', 'MeanVoltage2', 'MeanVoltage3', 'MeanMVA1','MeanMVA2', 'MeanMVA3', 'MeanMW1', 'MeanMW2', 'MeanMW3', 'MeanMVAR1', 'MeanMVAR2', 'MeanMVAR3', 'MeanPF1','MeanPF2', 'MeanPF3', 'MeanTotMVA', 'MeanTotMW', 'MeanTotMVAR', 'MeanTotPF', 'MeanZ1', 'MeanZ2', 'MeanZ3','MeanRes1', 'MeanRes2', 'MeanRes3', 'MeanReac1', 'MeanReac2', 'MeanReac3', 'MeanLng1', 'MeanLng2', 'MeanLng3','NeutralCurrentMean', 'NeutralVoltageMean', 'PrimaryVoltageMean',  'NeutralCurrentSdev', 'NeutralVoltageSdev','I2H1', 'I2H2', 'I2H3', 'TransformerTap', 'HeatMWHPLC', 'ChrgMWH', 'ChargeNumb', 'ChargeWt1', 'ChargeWt2', 'ChargeWt3','PwrOnTime', 'TapTapTime', 'I2T1', 'I2T2', 'I2T3',  'Ph1Pressure', 'Ph2Pressure', 'Ph3Pressure', 'TiltAngle', 'PanelTemp1A', 'PanelTemp2A', 'PanelTemp2B', 'PanelTemp3A', 'PanelTemp3C','PanelTemp4A', 'PanelTemp4C','PanelTemp5D1', 'PanelTemp5D2', 'PanelTemp7A', 'PanelTemp7E', 'PanelTemp8A', 'PanelTemp8B', 'PanelTemp9A', 'TempSumpN','TempSumpS', 'RoofInlet', 'RoofOutlet', 'TC1', 'TC2', 'TC3', 'TC4', 'TC5', 'CarbInject', 'NScavenger', 'SScavenger','MainDamperPos', 'SuperBagSmpPos', 'DropBoxPsi', 'CurrentRef','ChargeWt', 'HeatWt',  'ScrapPercWt', 'HeatKWHperTon', 'PowerOnTime', 'ChargeKWHperTon', 'OperKwhPerTon','AvgSF', 'AvgCurent', 'HeatAvgMW', 'HeatI2HperMWH', 'HeatAvgI2H', 'ChargeAvgMW', 'ChrgI2HperMWH', 'ChrgAvgI2H','TotMeanMw',  'ValidTempSample', 'ValidPPMSample', 'ValidCarbonSample',  'Elec1PosFromTop', 'Elec2PosFromTop','Elec3PosFromTop','SetPointPX3','Charge_Carb', 'TotScrapWt','TempEstim', 'PPMEstim', 'CarbEstim', 'B1_GasFlow', 'B1_O2MainFlow', 'B1_CarbonFlow', 'B2_GasFlow', 'B2_O2MainFlow', 'B2_CarbonFlow', 'B3_GasFlow', 'B3_O2MainFlow', 'B3_LimeFlow', 'B1_GasRef', 'B1_O2MainRef', 'B1_CarbonRef', 'B2_GasRef', 'B2_O2MainRef', 'B2_CarbonRef', 'B3_GasRef', 'B3_O2MainRef', 'B1_GasCns', 'B1_O2MainCns','B1_CarbonCns', 'B2_GasCns', 'B2_O2MainCns', 'B2_CarbonCns', 'B3_GasCns', 'B3_O2MainCns', 'B3_LimeCns', 'TotalGasCns','TotalO2Cns', 'TotalCarbonCns', 'AdditionsCarbCharg', 'AdditionsLimeInj', 'AdditionsCarbInj', 'Scrap1Wt','Scrap2Wt', 'Scrap3Wt', 'Scrap4Wt', 'Scrap5Wt','Scrap6Wt', 'Scrap7Wt',  'TempSample', 'PPMSample', 'CarbSample', 'PPMestim', 'AimPPM',  'TotalCarbInjRef', 'TotalO2Flow', 'TotCarbonInjFlow', 'SP_B1_NG', 'SP_B2_NG', 'SP_B3_NG', 'SP_B1_MainO2', 'SP_B2_MainO2', 'SP_B3_MainO2', 'SP_Inj1_C', 'SP_Inj2_C','M3PpmEstimAtSample','M3PpmSample', 'M3TempAtSample', 'MasterProgramLog']]
    #df = df[['Scrap1Wt','Scrap2Wt', 'Scrap3Wt', 'Scrap4Wt', 'Scrap5Wt','Scrap6Wt', 'Scrap7Wt','HeatNumber0LSW']]
    list_.append(df)
    

frame = pd.concat(list_, axis='rows')


GradeCrew = pd.DataFrame()
GradeCrew = pd.read_csv('/home/sergio/Documents/Hoeganaes/EAF/Logs/Hoeganaes/GradeCrew.csv')


# #merging dataframes
frame = pd.merge(frame,GradeCrew, how='left', left_on='HeatNumber0LSW', right_on='HeatNo')

# Calculated Variables
# ----------------------------------------------------------------------------------------------
frame['O2scfCarbInjLb'] = frame['TotalO2Cns']/frame['AdditionsCarbInj']
frame['HeatNumber'] = frame['HeatNumber0LSW']
frame.loc[frame['OperKwhPerTon'] < 0, 'OperKwhPerTon'] = 0 #locate where OperKwhPerTon is negative and clamp it to zero.
# .loc[filter by, what to bring]
# ----------------------------------------------------------------------------------------------


# Getting Column Names
# ----------------------------------------------------------------------------------------------
Columns_list = frame.columns.values.tolist() #this will bring the columns to a list

# List = [X for X in Columns_list if 'SF' in X] used to look up the Column_list list
aggColumnList = Columns_list
# Remove non numerical columns
aggColumnList.remove('Crew')
aggColumnList.remove('Grade')
aggColumnList.remove('StartDate')

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
GroupHeatCharge = frame.groupby(['HeatNumber0LSW','ChargeNumber'])
GradeGroup = frame.groupby(['Grade','HeatNumber0LSW'])
GradeHeatChargeGroup = frame.groupby(['Grade','HeatNumber0LSW','ChargeNumber'])
CrewHeatGroup = frame.groupby(['Crew','HeatNumber0LSW'])

###################################################
## How to take a look at a Groupby               ##
## for key, item in HeatGroup:                   ##
##     print(HeatGroup.get_group(key), "\n\n")   ##
###################################################

for var in aggColumnList:
    Heats[var] = HeatGroup[var].mean()

# ----------------------------------------------------------------------------------------------

# Getting the last value of some variables for Heat and Overview Groups
# ----------------------------------------------------------------------------------------------
Heats['Current1'] = HeatGroupNoZeros['Current1'].mean()
Heats['Current2'] = HeatGroupNoZeros['Current2'].mean()
Heats['Current3'] = HeatGroupNoZeros['Current3'].mean()
Heats['ZFeedback1'] = HeatGroupNoZeros['ZFeedback1'].mean()
Heats['ZFeedback2'] = HeatGroupNoZeros['ZFeedback2'].mean()
Heats['ZFeedback3'] = HeatGroupNoZeros['ZFeedback3'].mean()

Heats['HeatNumber0LSW'] = HeatGroup['HeatNumber0LSW'].last()
Heats['ActualCHRG_PX3'] = HeatGroup['ActualCHRG_PX3'].last()
Heats['ChargeWt1Tons'] = HeatGroup['ChargeWt1Tons'].last()
Heats['ChargeWt2Tons'] = HeatGroup['ChargeWt2Tons'].last()
Heats['ChargeWt3Tons'] = HeatGroup['ChargeWt3Tons'].last()
Heats['Ontime_PX3'] = HeatGroup['Ontime_PX3'].last()
Heats['OffTime_PX3'] = HeatGroup['OffTime_PX3'].last()
Heats['MWH_PX3'] = HeatGroup['MWH_PX3'].last()

Heats['I2H1'] = HeatGroup['I2H1'].last()                   
Heats['I2H2'] = HeatGroup['I2H2'].last()
Heats['I2H3'] = HeatGroup['I2H3'].last()
Heats['TransformerTap'] = HeatGroup['TransformerTap'].max()
Heats['HeatMWHPLC'] = HeatGroup['HeatMWHPLC'].last()
Heats['ChrgMWH'] = HeatGroup['ChrgMWH'].last()
Heats['ChargeNumb'] = HeatGroup['ChargeNumb'].last()
Heats['ChargeWt1'] = HeatGroup['ChargeWt1'].last()
Heats['ChargeWt2'] = HeatGroup['ChargeWt2'].last()
Heats['ChargeWt3'] = HeatGroup['ChargeWt3'].last()
Heats['PwrOnTime'] = HeatGroup['PwrOnTime'].last()
Heats['TapTapTime'] = HeatGroup['TapTapTime'].last()
Heats['I2T1'] = HeatGroup['I2T1'].last()
Heats['I2T2'] = HeatGroup['I2T2'].last()
Heats['I2T3'] = HeatGroup['I2T3'].last()
Heats['CarbInject'] = HeatGroup['CarbInject'].last()
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
Heats['ValidTempSample'] = HeatGroup['ValidTempSample'].last()      
Heats['ValidPPMSample'] = HeatGroup['ValidPPMSample'].last()
Heats['ValidCarbonSample'] = HeatGroup['ValidCarbonSample'].last()
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
Heats['O2scfCarbInjLb'] = HeatGroup['O2scfCarbInjLb'].last()
Heats['MasterProgramLog'] = HeatGroup['MasterProgramLog'].last()

Overview['PON'] = Heats['Ontime_PX3']
Overview['T2T'] = Heats['TapTapTime']
Overview['MWH'] = Heats['MWH_PX3']
Overview['HeatkWhTon'] = Heats['OperKwhPerTon'] 
Overview['I2H1'] = Heats['I2H1']
Overview['I2H2'] = Heats['I2H2']
Overview['I2H3'] = Heats['I2H3']
Overview['AvgCurr'] = (Heats['Current1']+Heats['Current2']+Heats['Current3'])/3
#Overview['PrimVolts'] = Heats['PrimaryVolts']
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
#Overview['TotalCarbonCns'] = Heats['TotalCarbonCns']
Overview['O2scfCarbInjLb'] = Heats['O2scfCarbInjLb']
Overview['HeatNumber'] = Heats['HeatNumber0LSW']


# ----------------------------------------------------------------------------------------------

# Some other variables for plots
# ----------------------------------------------------------------------------------------------
OverviewShort = Overview[['PON','T2T','MWH','HeatkWhTon','HeatNumber']]
OverviewMelted = pd.melt(OverviewShort,id_vars='HeatNumber',var_name='KPI')


#GradeHeatChargeGroup[['Scrap1Wt','Scrap2Wt','Scrap3Wt','Scrap4Wt','Scrap5Wt','Scrap6Wt','Scrap7Wt']].max()







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
n, bins, patches = plt.hist(x = MWH1,bins=20, color='#0504aa', alpha=0.7, rwidth=0.9 )
plt.grid(axis='y', alpha=0.75)
plt.xlabel('MWH')
plt.ylabel('Frequency')
plt.title('MWH 1st Charge')
plt.savefig('MWH1stChargeHistogram.png', bbox_inches='tight')
plt.show()


plt.figure()
#x_pos = np.arange(len(GradeGroup.Grade.unique()))
x_pos =np.arange(len(MWH1))
bars = MWH1
plt.bar(x_pos, bars, align='center', alpha=0.5)
plt.xticks(x_pos,GroupHeatCharge.HeatNo.max().unstack()[1])
plt.ylabel('MWH')
plt.xlabel('Heat Number')
plt.xticks(rotation=90)
plt.ylim(5,12)
plt.title('MWH 1st Bucket')
plt.grid()
plt.savefig('MWH1stChargePlot.png', bbox_inches='tight')
plt.show()    


# this is another option...
# sns.distplot(MWH1)
# plt.xlim(0,16)
# plt.show()


# kWh/Ton 1st Charge Histogram
# +++++++++++++++++++
plt.figure()
kwhTon1 = GroupHeatCharge['OperKwhPerTon'].max().unstack()[1]  #this gets OperKwhPerTon of 1st Charge only
#k1 = kwhTon1 + 50  #this is just an example on how to make histograms overlap
plt.hist(kwhTon1, bins=49, alpha=0.5)   
#plt.hist(k1, bins=49, alpha=0.5 )    #this is just an example on how to make histograms overlap
plt.xlabel('kWh/Ton')
plt.ylabel('Frequency')
plt.title('kWh/Ton 1st Charge')
plt.savefig('kwhTon1stCharge.png', bbox_inches='tight')
plt.show()


plt.figure()
x = MWH1
y = Overview.HeatkWhTon
plt.scatter(x,y, s=Heats.TapTapTime*0.4)
plt.axhline(y=400, color='r', linestyle='-')    #draw a horizontal line at 400.
plt.legend(loc='best')
plt.show()



# Scatter with built in ZOOM
# +++++++++++++++++++
# fig = plt.figure()
# ax = plt.axes()
# x = Heats.TapTapTime
# y = Overview.HeatkWhTon
# ax.scatter(x,y)
# ax.title('kWh/Ton vs T2T Time')
# ax.set_ylim(0,600)
# x1 = 40
# x2 = 100
# # select y-range for zoomed region
# y1 = 300
# y2 = 400
# axins = zoomed_inset_axes(ax, 2, loc=1) # zoom = 2
# axins.scatter(x,y)
# axins.set_xlim(x1, x2)
# axins.set_ylim(y1, y2)
# plt.xticks(visible=False)
# plt.yticks(visible=False)
# mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5")
# plt.draw()
# plt.show()


# Multiple Histograms of MWH 1st Bucket by Grade
# +++++++++++++++++++
MWHChargePerGrade = GradeHeatChargeGroup.MWH_PX3.max().unstack()[1]
Grades = frame.Grade.unique()
plt.figure(1)
#r = np.arange(len(Grades)) + 1 #in order to avoid index 0
index = 1
for grd in Grades:
    plt.subplot(4,5,index)
    plt.hist(MWHChargePerGrade[grd], bins='auto', alpha=0.5, label=grd)
    index = index +1
    plt.legend(loc='best')
    plt.grid(alpha=0.5)
    plt.xlabel('MWH')
    plt.ylabel('Heats')
    plt.xlim(4,12)
    plt.ylim(0,30)
#plt.savefig('MWH1stChargebyGrade.png', bbox_inches='tight')
plt.suptitle('MWH 1st Charge by Grade')
plt.show()


# 2 Bushlings
# 3 Frag
# 4 Pit
# 5 Remelt
# 6 Skulls
# 7 other


# OverviewShort Pairplot
# +++++++++++++++++++
# sns.set()
# sns.pairplot(OverviewShort)
# plt.show()

# T2T vs HeatkWhTon
# +++++++++++++++++++
plt.figure()
sns.lmplot(x='T2T',y='HeatkWhTon',data=Overview, fit_reg=True)
plt.xlabel('Tap to Tap minutes')
plt.ylabel('Heat kWh/Ton')
plt.title('kWh/Ton vs T2T Time')
plt.ylim(300,500)
plt.xlim(25,125)
plt.show()



sns.set(style="darkgrid")
Over = sns.load_dataset("Overview")
sns.jointplot("T2T", "HeatkWhTon", data=Overview, kind="reg", xlim=(25, 125), ylim=(300, 500), color="slateblue")
plt.show()

# HeatAvgMW
# +++++++++++++++++++
Heats.HeatAvgMW.plot()
plt.show()


# All Overview Boxplot
# +++++++++++++++++++
# sns.boxplot(data=Overview)
# plt.show()

# KPI swarmplot
# +++++++++++++++++++
# sns.swarmplot(x='KPI',y='value',data=OverviewMelted, hue='HeatNumber',dodge=True)
# plt.legend(bbox_to_anchor=(1,1), loc=2)
# plt.show()




# GradeList = GradeGroup.Ontime_PX3.max().unstack()     not used

# Average Power On Time by Grade
PONperGrade = GradeGroup.Ontime_PX3.max().mean(level=0) 

# Amount of Heats per Grade
GradeCount = GradeGroup.HeatNumber.max().count(level=0)

#print(PONperGrade,GradeCount)

# plt.figure()
# #x_pos = np.arange(len(GradeGroup.Grade.unique()))
# x_pos =np.arange(0,7)
# bars = PONperGrade
# plt.bar(x_pos, bars, align='center', alpha=0.5)
# plt.xticks(x_pos,GradeGroup.Grade.unique())
# plt.ylabel('minutes')
# plt.title('Power On Time per Grade')
# plt.show()













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


# frame.to_pickle(frame)





# Heats.loc[19096,:]  #returns all columns for that specific Heat


# HeatGroup.PrimaryVolts.mean().plot(style='.')
# plt.show()

# toplot = frame['Current1'][frame['HeatNumber0LSW']==19096]  this way I can trend a specific variable of a specific heat
# toplot = frame['Current1'][frame['HeatNumber0LSW']==19096]
# toplot = frame['Current1'][frame['HeatNumber0LSW']==19096][500:1000] #to get specific time range from 600 to 1050
# toplot.plot()
# plt.show()
# toplot.mean()









ScrapDF = pd.DataFrame()
ScrapDF = pd.read_csv('/home/sergio/Documents/Hoeganaes/EAF/Logs/Hoeganaes/ScrapbyGrade.csv')

ScrapbyGradeGroup = ScrapDF.groupby(['Grade','HeatNo','Bucket'])
BundlesWtbyGrade =  ScrapbyGradeGroup.Bundles.mean().unstack()[1]

GradesScrap = ScrapDF.Grade.unique()

plt.figure()
plt.subplot(4,5,1)
# plt.hist(BundlesWtbyGrade['3CUBPF'], bins=20, alpha=0.5, label='150HP',rwidth=0.95)
# plt.legend(loc='best')
# plt.grid(alpha=0.5)
# plt.xlabel('Pounds')
# plt.ylabel('Heats')
# #plt.xlim(4,12)
# #plt.ylim(0,30)
# plt.suptitle('Bundles Bucket 1 [Lb] 150HP')
# plt.show()

index = 1
for grd in GradesScrap:
    plt.subplot(4,5,index)
    plt.hist(BundlesWtbyGrade[grd], bins=20, alpha=0.5, label=grd, rwidth=0.95)
    index = index +1
    plt.legend()
    plt.grid(alpha=0.5)
    plt.xlabel('Pounds')
    plt.ylabel('Heats')
    #plt.xlim(4,12)
    #plt.ylim(0,30)
plt.suptitle('Bundles Bucket 1 [Lb] for' + grd)
plt.show()



# Analysis on the Sillicon Sand trial for B's and C's Heats
#----------------------------------------------------------------------------------

GradeHeatGroup = frameNoZeros.groupby(['Grade','HeatNumber0LSW'])
GradeMeanSFx = GradeHeatGroup['AvgSF'].mean()

BeforeSand = GradeMeanSFx['LOWO2B'].loc[:19470]
AfterSand = GradeMeanSFx['LOWO2B'].loc[19482:]

plt.figure()
#plt.plot(GradeMeanSFx['LOWO2B'],'bo')
plt.hist(BeforeSand, alpha=0.5, label='Before', bins=20)
plt.hist(AfterSand, alpha=0.5, label='After', bins=20)
plt.title('AvgSF for LOWO2B Heats using Si Sand')
plt.xlabel('Heat Number')
plt.ylabel('Average SF')
plt.legend()
plt.show()



Heat19604 = frame.loc[frame['HeatNumber0LSW'] == 19604]

plt.figure()

TapX = frameNoZeros.loc[frameNoZeros.TransformerTap == 8]
TapX['AvgCurr'] = (TapX.Current1 + TapX.Current2 + TapX.Current3)/3
TapX['AvgMW'] = (TapX.MW1 + TapX.MW2 + TapX.MW3)/3
TapX['AvgZ'] = (TapX.ZFeedback1 + TapX.ZFeedback2 + TapX.ZFeedback3)/3
plt.scatter(TapX.AvgCurr, TapX.AvgZ)
plt.show()


Filter1 = TapX[TapX.AvgZ > 38]
SinglePhasing = Filter1[Filter1.AvgCurr > 20]
SinglePhasing.HeatNo.unique()
singlePhasing = frame[frame.HeatNo == 19560]

plt.figure()
plt.plot(singlePhasing.Current1)
plt.plot(singlePhasing.Current2)
plt.plot(singlePhasing.Current3)
plt.show()
