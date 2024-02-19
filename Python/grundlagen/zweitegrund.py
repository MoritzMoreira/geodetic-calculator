from math import *
from grundlagen import winkel

def umrechnen_koordinaten(y1,x1,y2,x2):
    t12 = atan2((y2-y1), (x2-x1))
    s12 = sqrt((y2-y1)**2 + (x2-x1)**2)
    t12 = winkel.rad2gon(t12)
    return t12, s12