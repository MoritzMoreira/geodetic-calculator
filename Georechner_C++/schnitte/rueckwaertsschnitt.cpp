#include "mainwindow.h"
#include <iostream>

Rueckwaertsschnitt::Rueckwaertsschnitt(Punkt& p_p1, Punkt& p_p2, Punkt& p_p3, float& p_r1, float& p_r2, float& p_r3)
    : m_p1(p_p1), m_p2(p_p2), m_p3(p_p3), m_r1(p_r1), m_r2(p_r2), m_r3(p_r3){}

std::vector<float> Rueckwaertsschnitt::berechne(){
        // Definition von Variablen fuer die Koordinaten
        float y1 = this->m_p1.hole_y(); float x1 = this->m_p1.hole_x();
        float y2 = this->m_p2.hole_y(); float x2 = this->m_p2.hole_x();
        float y3 = this->m_p3.hole_y(); float x3 = this->m_p3.hole_x();

        //Berechnung der Winkel alpha und beta aus den Richtungswinkeln
        float arg1 = m_r1 - m_r3; float a = gon2rad(arg1);
        float arg2 = m_r2 - m_r1; float b = gon2rad(arg2);

        //Berchnung der Koordinaten der Hilfspunkte
        float yc = y1 + (x2-x1) * cot(a); float xc = x1 - (y2-y1) * cot(a); Punkt pc = Punkt(yc, xc);
        float yd = y3 + (x3-x2) * cot(b); float xd = x3 - (y3-y2) * cot(b); Punkt pd = Punkt(yd, xd);

        // Berechnung des Richtungswinkels tcd aus den Hilfskoordinaten
        float tcd = gon2rad(Strecke(pc, pd).riwi_laenge()[1]);
        std::cout<<"tcd: "<<tcd<<std::endl;

        // Berechnung der Koordinaten des Ergebnispunktes
        float xn = xc + (y2-yc+(x2-xc)* cot(tcd))/(tan(tcd)+ cot(tcd));
        float yn = yc + (xn-xc) * tan(tcd);

        // Umwandlung der Koordinaten in ein Punktobjekte
        Punkt pn = Punkt(yn, xn, "PN");

        // Definition der Map zur Weitergabe der Ergebnisse als Datei und an Webdienst
        std::map<std::string, std::string> dict = {{"pn", pn.str()}};

        // Ausgabe des Ergebnis als Vektor
        std::vector<float> arr = {yn, xn};
        return arr;
}


