import pandas as pd
import os
import glob
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import dask.dataframe as dd


path = '/home/sergio/Documents/Hoeganaes/EAF/Logs/LogsOk/CurrentPeriod/Hoeganaes*.csv'
frame = dd.read_csv(path, assume_missing='True')
frame.head()

GradeCrew = pd.DataFrame()
GradeCrew = pd.read_csv('/home/sergio/Documents/Hoeganaes/EAF/Logs/Hoeganaes/GradeCrew.csv')

# #merging dataframes
frame = pd.merge(frame,GradeCrew, how='left', left_on='HeatNumber0LSW', right_on='HeatNo')
