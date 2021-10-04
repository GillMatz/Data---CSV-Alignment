# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 17:33:21 2021

Transformation of the CSV file.

@author: Gill
"""

import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog

def zerolistmaker(n):
    listofzeros = [0] * n
    return listofzeros


# Choosing file: 
# ---------------
root = tk.Tk()
root.withdraw()
files = filedialog.askopenfilenames(parent=root, initialdir="/", title='Please select files')

FsPPG = 64                  # 64 Hz
DelayPPG    = 19*FsPPG-1    # 19 [sec] delay

# Reading the CSV file
data = pd.read_csv(files[0])

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
# AfibAB  = data[' AfibAB'].to_numpy() 
# Debug   = data[' Debug'].to_numpy() 


# AfibAB  = AfibAB[IndexOriginal]
# Debug   = Debug[IndexOriginal]

hrPPG[IndexAligned[IndexAligned>0]]  = hrPPG[IndexOriginal[IndexAligned>0]]
hrPPG[IndexOriginal] = 0
data[' HRppg']= hrPPG

V= data[[" PPG"," Vpeak"," HRppg"]]

# V.to_csv('mmm.csv')


AccFlag = data[' Acc'].tolist()
ArtFlag = data[' Art'].tolist()
SnrFlag = data[' Ppg'].tolist()


data[' Acc'] = AccFlag[DelayPPG:] + zerolistmaker(DelayPPG)
data[' Art'] = ArtFlag[DelayPPG:] + zerolistmaker(DelayPPG)
data[' Ppg'] = SnrFlag[DelayPPG:] + zerolistmaker(DelayPPG)

V= data[[" PPG"," Vpeak"," HRppg"," Acc"," Art"," Ppg"]]
data.to_csv('mmm.csv')





