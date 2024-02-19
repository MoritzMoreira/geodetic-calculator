#include <math.h>
#include "mainwindow.h"
#include <iostream>

std::array<float, 2> umrechnen_koordinaten2(const float& y1, const float& x1, const float& y2, const float& x2){
    float t12 = atan2((y2-y1), (x2-x1));
    float s12 = sqrt(pow(y2-y1, 2) + pow(x2-x1, 2));
    //s12 = roundoff(s12, 5);
    t12 = rad2gon(t12);
    std::array<float, 2> arr_t12_s12 = {t12, s12};
    return arr_t12_s12;
}
