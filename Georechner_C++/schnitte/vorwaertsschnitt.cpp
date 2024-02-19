#include "mainwindow.h"

Vorwaertsschnitt::Vorwaertsschnitt(Punkt& p_p1, Punkt& p_p2, Punkt& p_p3, Punkt& p_p4, float& p_phi, float& p_psi)
    : m_p1(p_p1), m_p2(p_p2), m_p3(p_p3), m_p4(p_p4), m_phi(p_phi), m_psi(p_psi){}

std::vector<float> Vorwaertsschnitt::berechne(){
        // Definition von Variablen für die Koordinaten
        float y1 = this->m_p1.hole_y();
        float x1 = this->m_p1.hole_x();
        float y2 = this->m_p2.hole_y();
        float x2 = this->m_p2.hole_x();
        float y3 = this->m_p3.hole_y();
        float x3 = this->m_p3.hole_x();
        float y4 = this->m_p4.hole_y();
        float x4 = this->m_p4.hole_x();

        // Berechnung der Richtungswinkel t14 und t23 aus den Koordinaten
        float t14 = Strecke(this->m_p1, this->m_p4).riwi_laenge()[1];
        float t23 = Strecke(this->m_p2, this->m_p3).riwi_laenge()[1];
        std::cout<<"t14: "<<t14<<std::endl;
        std::cout<<"t23: "<<t23<<std::endl;
        // Berechnung der Richtungskoeffizienten mit den orientierten Richtungen
        float arg1 = t14 + m_phi;
        float p4n = gon2rad(arg1);
        float arg2 = t23 + m_psi;
        float p2n = gon2rad(arg2);

        // Berechnung der Koordinaten des Ergebnispunktes
        float xn = x1 + ((y2-y1)-(x2-x1)*tan(p2n))/(tan(p4n)-tan(p2n));
        float yn = y1 + (xn-x1) * tan(p4n);

        // Umwandlung der Koordinaten in ein Punktobjekt
        Punkt pn = Punkt(yn, xn, "N");

        std::vector<float> arr = {yn, xn};
        return arr;
}


