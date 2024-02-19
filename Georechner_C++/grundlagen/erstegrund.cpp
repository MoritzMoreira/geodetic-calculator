#include "mainwindow.h"
#include <iostream>

float* umrechnen_koordinaten(float& y1, float& x1, float& s12, float& t12){
    float sin_t12 = sin(gon2rad(t12));
    float cos_t12 = cos(gon2rad(t12));

    float y2 = y1+s12*sin_t12;
    float x2 = x1+s12*cos_t12;

    static float arr_y2_x2[] = {y2, x2};
    return arr_y2_x2;
}

float umrechnen_koordinatenunterschiedey(float& s, float& t){
    float sin_t = sin(gon2rad(t));
    float dy = floor(s*sin_t + 0.5);
    return dy;
}

float umrechnen_koordinatenunterschiedex(float& s, float& t){
    float cos_t = cos(gon2rad(t));
    float dx = floor(s*cos_t +0.5);
    return dx;
}
