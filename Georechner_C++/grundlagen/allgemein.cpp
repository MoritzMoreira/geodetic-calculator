#include <iostream>
#include <math.h>
#include "mainwindow.h"

long double roundoff(long double value, int prec){
    long double pow_10 = pow(10.0f, prec);
    return round(value * pow_10) / pow_10;
}
