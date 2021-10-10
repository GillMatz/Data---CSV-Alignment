# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 17:33:21 2021

Transformation of the CSV file.

@author: Gill
"""

import pandas as pd
import numpy as np



def zerolistmaker(n):
    listofzeros = [0] * n
    return listofzeros

def CSVtransform(fullpath):
    FsPPG = 64                  # 64 Hz
    DelayPPG    = 19*FsPPG-1    # 19 [sec] delay
    
    # Reading the CSV file
    data = pd.read_csv(fullpath)
    
    # PPG - peak based events: 
    # -------------------------
    
    # Vpeak - peaks location
    Vpeak   = data[' Vpeak'].to_numpy()                                 # Converting DataFrame series into NumPy array
    IndexOriginal   = np.asarray(np.where(Vpeak!=0))
    Val     = Vpeak[IndexOriginal]
    
    Vpeak[IndexOriginal] = 0                                            # zeroing all original Vpeak values.
    IndexAligned = IndexOriginal - Val - DelayPPG                       # Aliging peak location and Delay compensation.          
    Vpeak[IndexAligned[IndexAligned>0]]  = 1                            # subtitute with 1 in the right location. 
    
    data[" Vpeak"] = Vpeak 
    
    
    
    # hrPPG - heart rate
    hrPPG   = data[' HRppg'].to_numpy()
    hrPPG[IndexAligned[IndexAligned>0]]  = hrPPG[IndexOriginal[IndexAligned>0]]
    hrPPG[IndexOriginal] = 0
    data[' HRppg']= hrPPG
    
 #   V= data[[" PPG"," Vpeak"," HRppg"]]
    
    # Flags delay compensation: 
    # -----------------------------------------
    
    AccFlag = data[' Acc'].tolist()                         # 6D flag
    ArtFlag = data[' Art'].tolist()                         # Artifact flag
    SnrFlag = data[' Ppg'].tolist()                         # SNR flag
    AF_PPG = data[' PpgAF'].tolist()                        # AF PPG flag
    FindParameters = data[' PrePostFP'].tolist()
    
    data[' Acc'] = AccFlag[DelayPPG:] + zerolistmaker(DelayPPG)
    data[' Art'] = ArtFlag[DelayPPG:] + zerolistmaker(DelayPPG)
    data[' Ppg'] = SnrFlag[DelayPPG:] + zerolistmaker(DelayPPG)
    data[' PpgAF'] = AF_PPG[DelayPPG:] + zerolistmaker(DelayPPG)
    data[' PrePostFP'] = FindParameters[DelayPPG:] + zerolistmaker(DelayPPG)

    fullpath = fullpath.replace('.csv','_aligned.csv')
    data.to_csv(fullpath,index=False)
    # data.to_csv('new.csv',index=False)

# reading file name and path from txt
with open ("FileName.txt", "r") as myfile:
    filename = myfile.readlines()

filename = str(filename) # casting 
filename = filename[1:-1]
filename = filename.replace('\\\\','\\')

# call function with the name from the FileName.txt
CSVtransform(filename[1:-1])

#CSVtransform(filename)