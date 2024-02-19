from math import *
from grundlagen import winkel

def umrechnen_koordinaten(y1,x1,s12,t12):
    sin_t12=sin(winkel.gon2rad(t12))
    cos_t12=cos(winkel.gon2rad(t12))

    y2=y1+s12*sin_t12
    x2=x1+s12*cos_t12

    return y2,x2

def umrechnen_koordinatenunterschiedey(s, t):
    sin_t = sin(winkel.gon2rad(t))
    dy = round(s*sin_t,2)
    return dy

def umrechnen_koordinatenunterschiedex(s, t):
    cos_t = cos(winkel.gon2rad(t))
    dx = round(s*cos_t,2)
    return dx

