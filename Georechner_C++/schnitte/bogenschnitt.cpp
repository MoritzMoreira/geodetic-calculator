#include "mainwindow.h"
#include <iostream>
#include <map>

Bogenschnitt::Bogenschnitt(Strecke& p_s1, Strecke& p_s2, Strecke& p_s3): m_s1(p_s1), m_s2(p_s2), m_s3(p_s3) {}

std::vector<float> Bogenschnitt::berechne(){
        // bekannte Punkte aus Streckenobjekten holen
        Punkt p1 = this->m_s1.hole_p1();
        Punkt p2 = this->m_s2.hole_p1();

        // Koordinaten von Punkt 1 holen
        float y1 = p1.hole_y();
        float x1 = p1.hole_x();

        // einfache Strecken aus Streckenobjekten holen
        float s1 = this->m_s1.riwi_laenge()[1];
        float s2 = this->m_s2.riwi_laenge()[1];
        float s3 = this->m_s3.riwi_laenge()[1];
        std::cout<<"s1 (distanz): "<<s1<<std::endl;
        std::cout<<"s2 (distanz): "<<s2<<std::endl;
        std::cout<<"s3 (distanz): "<<s3<<std::endl;
        std::cout<<"s1 :"<<m_s1.riwi_laenge()[0]<<std::endl;
        // Schaffen einer Instanz der Klasse Strecke aus den gegebenen Punkten
        Strecke s12 = Strecke(p1, p2);
        // Aufteilung von Strecke und Richtungswinkel des Objekts Strecke in zwei Variablen
        float str0 = s12.riwi_laenge()[1];
        std::cout<<"str0 (distanz): "<<str0<<std::endl;
        float t0 = s12.riwi_laenge()[0];

        // Prüfen, ob s3 eingegeben wurde
        float m;
        if(s3 == 0.0){    // wenn nicht, Maßstab auf 1 setzen
            m = 1.0;
        }
        else{             // wenn ja, Maßstab berechnen. str0 ist die aus den Koordinaten berechnete, s3 die gemessene Strecke zwischen den bekannten Punkten
            m = str0 / s3;
            // gemessene Strecken mit Maßstab korrigieren
            s1 *= m;
            s2 *= m;
        }
        std::cout<<"m: "<<m<<std::endl;
        std::cout<<"s1 (distanz): "<<s1<<std::endl;
        std::cout<<"s2 (distanz): "<<s2<<std::endl;
        std::cout<<"s2 +s1 (distanz): "<<s2+s1<<std::endl;
        std::cout<<"str0 (distanz): "<<str0<<std::endl;

        // Prüfen ob der Sonderfall "schlechter Schnitt" vorliegt (nur 1 Neupunkt)
        if(s1+s2 - str0 < 0.001 && s1+s2 - str0 > -0.001){          //wenn ja: Koordinaten des Neupunktes durch erste Grundaufgabe berechnen
            std::cout<<"schlechter Schnitt"<<std::endl;
            float yn1 = umrechnen_koordinaten(y1,x1,s1,t0)[0];
            float xn1 = umrechnen_koordinaten(y1,x1,s1,t0)[1];
            //Belegung der Variable pn2 mit String für die Anzeige im Ergebnisfeld und Übergabe eines einheitlichen Structs für das Ergebnis
            std::string s = "schlechter Schnitt (nur eine Lösung)";
            std::cout<<"yn1: "<<std::endl;
            // Ausgabe Ergebnis
            float yn2(0.0f), xn2(0.0f);
            std::vector<float> arr = {yn1, xn1, yn2, xn2, m};
            return arr;
        }

        // Prüfen ob Sonderfall "keine Lösung" vorliegt
        else if(s1+s2 < str0){
            std::cout<<"keine Lösung"<<std::endl;
            //wenn ja, Definition des Ergebnisstructs mit 2 Strings als Eintrag
            std::map<std::string, float> dict = {{"yn1",0.0f}, {"xn1",0.0f}, {"yn2",0.0f}, {"xn2",0.0f}, {"Wiederspruch in Eingangsdaten", 0.0f}};

            // Ausgabe von 3 Strings und dem Dictionary als Tupel
            Punkt pn1, pn2;
            //ergebnis_Bogenschnitt ergebnis = {pn1, pn2, "", 0.0f, dict};
            std::vector<float> ergebnis = {0.0f,0.0f,0.0f,0.0f,0.0f};
            return ergebnis;
        }

        //Wenn kein Sonderfall vorliegt: Bogenschnitt berechnen (Zwischenvariablen siehe Formeln im Handbuch)
        else{
            std::cout<<"kein Sonderfall"<<std::endl;
            float a = acos((pow(s1,2.0f) + pow(str0,2.0f) - pow(s2,2.0f)) / (2.0f * str0 * s1));
            //Definition des Richtungswinkels durch Indexslicing der Streckeninstanz s und Umrechnung in rad (Strecke zwischen bekannten Punkten)
            float t = gon2rad(s12.riwi_laenge()[0]);

            float t1n1 = t + a;
            float t1n2 = t - a;
            //Berechnung der Koordinaten des Ergebnispunktes
            float yn1 = y1 + s1 * sin(t1n1);
            float xn1 = x1 + s1 * cos(t1n1);
            float yn2 = y1 + s1 * sin(t1n2);
            float xn2 = x1 + s1 * cos(t1n2);

            std::vector<float> ergebnis = {yn1,xn1,yn2,xn2,m};
            return ergebnis;
        }
}




