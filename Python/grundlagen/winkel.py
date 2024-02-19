from math import *

rho_deg = 180.0 / pi
rho_gon = 200.0 / pi

def rad2gon(p_rad):
    return p_rad * rho_gon

def rad2deg(p_rad):
    return p_rad * rho_deg

def gon2rad(p_gon):
    return p_gon / rho_gon

def gon2deg(p_gon):
    return rad2deg(gon2rad(p_gon))

def deg2rad(p_deg):
    return p_deg / rho_deg

def deg2gon(p_deg):
    return rad2gon(deg2rad(p_deg))
def cot(p_ctg):
    return cos(p_ctg)/sin(p_ctg)

def richtungswinkel_aus_richtung(t, r):
    t = t
    r = r
    winkel = t+r
    if winkel>200:
        winkel -= 200
        return winkel
    else:
        winkel += 200
        return winkel