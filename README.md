# Hackathon_Pressure_Mat
Code associated with the pressure mat designed by Innovation INKlined at the Graphene Hackathon 2019.

The arduino in underneath the chair sends sends an array of data containing resistance measurements 
from the graphene strain sensors on top of the chair. 

This data is read by python, and average of avgno (=50) data sets is taken these are then "normalised" 
to the initial reading. Finally, the resulting data is displayed as a colour contour map using matplotlib.
The plot should refresh as soon as matplot lib is able to regenerate the display.
