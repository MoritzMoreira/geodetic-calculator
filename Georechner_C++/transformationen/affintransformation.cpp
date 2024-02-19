#include "mainwindow.h"
#include <iostream>
#include <typeindex>
#include <typeinfo>
//#include <boost/typeof/typeof.hpp>


Affintransformation::Affintransformation(std::map<std::string, Punkt>& p_punkte_alt, std::map<std::string, Punkt>& p_punkte_neu)
  : Transformation(p_punkte_alt, p_punkte_neu){}


std::array<long double,10> Affintransformation::parameter(std::vector<Punkt>& punkte_alt_red, std::map<std::string, Punkt>& punkte_neu_red, Punkt& p_a_s, Punkt& p_n_s){
    // Definition der Summenvariablen
    long double summe_xX = 0.0, summe_yY = 0.0, summe_x_quad = 0.0, summe_yX = 0.0, summe_xY = 0.0, summe_xy = 0.0;
    long double summe_y_quad = 0.0;
    //Bildung der Summen durch for-Schleife durch Liste der alten reduzierten Passpunkte
    for(Punkt& p_r_a : punkte_alt_red){
        //Punktnummer holen
        std::string nr = p_r_a.hole_nr();
        //entsprechenden reduzierten neuen Passpunkt mit Punktnummer als Schlüssel holen
        Punkt p_r_n = punkte_neu_red[nr];

        // Aufaddieren der verschiedenen Produkte zur Summenbildung
        summe_xX += p_r_a.hole_x() * p_r_n.hole_x();
        summe_y_quad += pow(p_r_a.hole_y(),2);
        summe_x_quad += pow(p_r_a.hole_x(),2);
        summe_yX += p_r_a.hole_y() * p_r_n.hole_x();
        summe_xY += p_r_a.hole_x() * p_r_n.hole_y();
        summe_xy += p_r_a.hole_x() * p_r_a.hole_y();
        summe_yY += p_r_a.hole_y() * p_r_n.hole_y();
    }
    //Berechnung des Nenners N aus den Summen
            //      summe_x_quad * summe_y_quad - (summe_xy)**2   9021562.5992
    //long double* r = &roundoff(summe_y_quad,4);
    long double N = summe_x_quad * summe_y_quad - pow((summe_xy), 2);
    // Berechnun der Transforamtionsparameter a1-a4 durch Summen und Nenner
    long double a1 = (summe_xX * summe_y_quad - summe_yX * summe_xy) / N;
    long double a2 = (summe_xX * summe_xy - summe_yX * summe_x_quad) / N;
    long double a3 = (summe_yY * summe_x_quad - summe_xY * summe_xy) / N;
    long double a4 = (summe_xY * summe_y_quad - summe_yY * summe_xy) / N;
    std::cout<<"xquad = "<<std::setprecision(15)<<summe_x_quad<<", yquad = "<<std::setprecision(20)<<summe_y_quad<<std::endl;
    std::cout<<"yquad type = "<<typeid(summe_y_quad).name()[3]<<", N = "<<std::setprecision(10)<<N<<std::endl;
    std::cout<<"a1 = "<<a1<<",  a2 = "<<a2<<", a3 = "<<a3<<", a4 = "<<a4<<std::endl;
    if(summe_y_quad != 9021562.5992) std::cout<<"ja"<<std::endl;

    // Aufruf der von parameter_base mit Parametern a1-a4 und Schwerpunkten
    std::array<long double,6> param = this->parameter_base(a1, a2, a3, a4, p_a_s, p_n_s);
    // restliche Transformationsparameter aus Ergebnistupel holen
    // Translation
    long double Y0 = param[0]; long double X0 = param[1];
    //Massstab Abszisse / Ordinate
    long double m1 = param[2]; long double m2 = param[3];
    // Drehwinkel Abszisse / Ordinate
    long double alpha = rad2gon(param[4]); long double beta = rad2gon(param[5]);
    std::cout<<"alpha nach Konvertierung: "<<alpha<<"m1 = "<<m1<<std::endl;
    // Ausgabe der Transformationsarameter für Ausgabefelder und Funktion transformiere
    std::array<long double,10> arr = {Y0, X0, a1, a2, a3, a4, m1, m2, alpha, beta};
    return arr;
}


