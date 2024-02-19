#include <math.h>
#include "mainwindow.h"

float rho_deg = 180.0f / M_PI, rho_gon = 200.0f / M_PI;

float rad2gon(float& p_rad) {return p_rad * rho_gon;}
long double rad2gon(long double& p_rad) {return p_rad * rho_gon;}

float rad2deg(float& p_rad) {return p_rad * rho_deg;}

float gon2rad(float& p_gon) {return p_gon / rho_gon;}

float gon2deg(float& p_gon) {float winkel_rad = gon2rad(p_gon); return rad2deg(winkel_rad);}

float deg2rad(float& p_deg) {return p_deg / rho_deg;}

float deg2gon(float& p_deg) {float winkel_deg = deg2rad(p_deg); return rad2gon(winkel_deg);}

float cot(float& p_ctg) {return cos(p_ctg)/sin(p_ctg);}

float richtungswinkel_aus_richtung(float t, float r) {float winkel = t+r;
    if(winkel>200){winkel -= 200; return winkel;}
    else{winkel += 200; return winkel;}
}
