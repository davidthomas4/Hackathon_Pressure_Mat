#!/usr/bin/python3
# Hackthon heat map script.

import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as FuncAnimation
from scipy.interpolate import griddata
import serial
import re

"""
Code designed to read in serialsed data from an 
arduino and plot the data as a heat map.
"""

#Matplotlib parameter setup

mpl.rcParams['font.size'] = 20
mpl.rcParams['font.weight'] ='bold'
mpl.rcParams['xtick.major.pad'] = '10'
mpl.rcParams['ytick.major.pad'] = '10'
mpl.rcParams['axes.linewidth'] = 2
mpl.rcParams['xtick.labelsize'] = 20
mpl.rcParams['ytick.labelsize'] = 20

# Heat map colour code - google for other codes.
cmap_choice = 'PiYG'

#plt.rc('text', usetex=True)
#mpl.rcParams['text.latex.preamble'] = [r"\usepackage{amsmath}"]
#mpl.rcParams['text.latex.preamble'] = [r"\boldmath"]

##################################
# Data read in starts here.      #
##################################

xs = [0,0,0,0,0.25,0.25,0.25,0.25,0.5,0.5,0.5,0.5,0.75,0.75,0.75,0.75]
ys = [0,0.25,0.5,0.75,0,0.25,0.5,0.75,0,0.25,0.5,0.75,0,0.25,0.5,0.75]

xs = np.array(xs, dtype=float)
ys = np.array(ys, dtype=float)

xx = np.linspace(min(xs), max(xs), 50)
yy = np.linspace(min(ys), max(ys), 50)

# Plot colours and parameters
lcol = 'k'
fcol = 'w'
lwid = 1.2
alph = 1.0

fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(5,5))
fig.subplots_adjust(bottom=0.15,top=0.9,left=0.1,right=0.85)

heatmap = plt.subplot(111)
heatmap.axes.set_xlim(0,0.75)
heatmap.axes.set_ylim(0,0.75)

###################################
# Read in Arduino data and update #
# plot.                           #
###################################

ser = serial.Serial('/dev/ttyACM0',9600)
s = [0 for i in range(1,17)]
while True:
    s  = str(ser.readline())
    num = re.findall(r'\d+', s)
    data = list(map(int, num))
    if(len(data)!=16):
        continue
    data=np.array(data, dtype=float)
    maxtot=max(data)
    cc = griddata((xs, ys), data, (xx[None, :], yy[:, None]), method='cubic')
    
    heatmap.contourf(xx, yy, cc, 300, cmap=cmap_choice, vmin=0.0, vmax=maxtot)
#    HCD = heatmap.contourf(xx, yy, cc, 30, cmap=cmap_choice, vmin=0.0, vmax=maxtot)
#    heatmap.axes.tick_params(width=2, length=10, direction='in', top=True, 
#                             bottom=False)
#    cb_ax = fig.add_axes([0.87,0.15,0.02,0.75])
#    cbar = fig.colorbar(HCD, cax=cb_ax, ticks=[0.0*maxtot, 0.25*maxtot, 
#                        0.5*maxtot, 0.75*maxtot, 2.0*maxtot])
#    cbar.set_clim(0.0,maxtot)
#    cbar.ax_set_yticklabels()
#    cbar.ax.tick_params(width=2, length=10)

    plt.pause(0.0000000001)
