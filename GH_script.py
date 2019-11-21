#!/usr/bin/python3
# DMT & HW 16/11/19

#####################################################
# Data analysis for Graphene Hackathon pressure mat #
#                                                   #
# This scripts reads data from graphene strain      #
# sensors via an arduino. An interpolation scheme   #
# is used between the data points, the resulting    #
# data is then used to produce a heat map of the    #
# pressure on the pad.                              #
#####################################################

import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import serial
import re

#Matplotlib parameter setup

mpl.rcParams['font.size'] = 40
mpl.rcParams['font.weight'] ='bold'
mpl.rcParams['axes.linewidth'] = 2
mpl.rcParams['xtick.labelsize'] = 0
mpl.rcParams['ytick.labelsize'] = 0

# Heat map colour code - google for other codes.
cmap_choice = 'PiYG'

#######################
# Array/figure setup. #
#######################

# Set up initial arrays. Obviously a better way to do this but oh well.
xs = [0,0,0,0,0.25,0.25,0.25,0.25,0.5,0.5,0.5,0.5,0.75,0.75,0.75,0.75]
ys = [0,0.25,0.5,0.75,0,0.25,0.5,0.75,0,0.25,0.5,0.75,0,0.25,0.5,0.75]

xs = np.array(xs, dtype=float)
ys = np.array(ys, dtype=float)

xx = np.linspace(min(xs), max(xs), 50)
yy = np.linspace(min(ys), max(ys), 50)

fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(5,5))
fig.subplots_adjust(bottom=0.15,top=0.9,left=0.05,right=0.80)
fig.text(0.45,0.92,"Back", ha="center")
fig.text(0.45,0.07,"Front", ha="center")
fig.text(0.02,0.5,"Right", rotation="vertical", ha="center")
fig.text(0.82,0.5,"Left", rotation=270, ha="center")
fig.text(0.95,0.89,"High", ha="center", fontsize=20)
fig.text(0.95,0.17,"Low", ha="center", fontsize=20)
fig.text(0.95,0.4,"Pressure", rotation=270, ha="center", fontsize=30)
cb_ax = fig.add_axes([0.89,0.15,0.02,0.75])

heatmap = plt.subplot(111)
heatmap.axes.set_xlim(0,0.75)
heatmap.axes.set_ylim(0,0.75)

###################################
# Read in Arduino data and update #
# plot.                           #
###################################

first_call=True
avgno = 50
initial_data=np.zeros(16)
k = 0 # frame counter
maxiter = 1000 # max frames before exit
ser = serial.Serial('/dev/ttyACM0',9600)
s = [0 for i in range(1,17)]
while True:
    k += 1
    if k == maxiter:
     break
    tot = np.zeros(16)
    for i in range(1,avgno):
         s  = str(ser.readline())
         num = re.findall(r'\d+', s)
         datain = list(map(int, num))
         if(len(datain)!=16):
              continue
         if(first_call):
              first_call=False
              initial_data=np.array(datain, dtype=float)
              continue
         tot+=np.array(datain, dtype=float)
    data=tot/avgno-initial_data
    cc = griddata((xs, ys), data, (xx[None, :], yy[:, None]), method='cubic')
    HCD=heatmap.contourf(xx, yy, cc, 300, cmap=cmap_choice, vmin=-20, vmax=20)
    heatmap.axes.tick_params(width=0, length=0, direction='in', top=True,
                             bottom=False)
    cbar = fig.colorbar(HCD, cax=cb_ax, ticks=[])
    plt.pause(0.0000000001)
