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
import matplotlib.animation as FuncAnimation
from scipy.interpolate import griddata
import serial
import re

#Matplotlib parameter setup

mpl.rcParams['font.size'] = 20
mpl.rcParams['font.weight'] ='bold'
#mpl.rcParams['xtick.major.pad'] = '10'
#mpl.rcParams['ytick.major.pad'] = '10'
mpl.rcParams['axes.linewidth'] = 2
#mpl.rcParams['xtick.labelsize'] = 20
#mpl.rcParams['ytick.labelsize'] = 20

# Heat map colour code - google for other codes.
cmap_choice = 'PiYG'

#plt.rc('text', usetex=True)
#mpl.rcParams['text.latex.preamble'] = [r"\usepackage{amsmath}"]
#mpl.rcParams['text.latex.preamble'] = [r"\boldmath"]

##################################
# Data read in starts here.      #
##################################

# Set up initial arrays. Obviously a better way to do this but oh well.
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

k = 0 # frame counter
ser = serial.Serial('/dev/ttyACM0',9600)
s = [0 for i in range(1,17)]
while True:
    k += 1
    if k == 1000:
     break
    tot = np.zeros(16)
    for i in range(1,5):
        s  = str(ser.readline())
        num = re.findall(r'\d+', s)
        datain = list(map(int, num))
        if(len(datain)!=16):
             continue
        tot += np.array(datain, dtype=float)
    data=tot/5
    maxtot=max(data)
    cc = griddata((xs, ys), data, (xx[None, :], yy[:, None]), method='cubic')
    heatmap.contourf(xx, yy, cc, 300, cmap=cmap_choice, vmin=0.0, vmax=1000)

    Bottom = [data[0], data[4], data[8], data[12]]
    Top = [data[3], data[7], data[11], data[15]]
    RHS = [data[12], data[13], data[14], data[15]]
    LHS = [data[0], data[1], data[2], data[3]]

    RHSAv = np.average(RHS)
    LHSAv = np.average(LHS)
    TopAv = np.average(Top)
    BotAv = np.average(Bottom)

    if(1.1*LHSAv > RHSAv):
        txth = "Leaning too far to the left"
    elif(1.1*RHSAv > LHSAv):
        txth = "Leaning too far to the right"
    else:
        txth = "Looking good (left/right)"
    if(1.1*TopAv > BotAv):
        txtv = "Leaning too far forward"
    elif(1.1*BotAv > TopAv):
        txtv = "Leaning too far backward"
    else:
        txtv = "Looking good (forward/backward)"

    HCD = heatmap.contourf(xx, yy, cc, 300, cmap=cmap_choice, vmin=0.0,
                           vmax=1000)
    heatmap.axes.tick_params(width=2, length=10, direction='in', top=True,
                             bottom=False)
    cb_ax = fig.add_axes([0.87,0.15,0.02,0.75])
    cbar = fig.colorbar(HCD, cax=cb_ax, ticks=[0, 250, 500, 750, 1000])
#    cbar.set_clim(0,1000)
#    cbar.ax_set_yticklabels([0,0.25,0.5,0.75,1])
    cbar.ax.tick_params(width=2, length=10)

    for txt in fig.texts:
        txt.set_visible(False)
    fig.text(0.15, 0.8, txth)
    fig.text(0.15, 0.7, txtv)
    plt.pause(0.0000000001)
