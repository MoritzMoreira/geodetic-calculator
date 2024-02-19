#include "mainwindow.h"
#include <iostream>
#include <vector>
//#include <json/value.h>
#include <fstream>
#include <typeindex>

Transformation::Transformation(std::map<std::string, Punkt>& p_punkte_alt, std::map<std::string, Punkt>& p_punkte_neu):
    m_punkte_alt(p_punkte_alt), m_punkte_neu(p_punkte_neu){}

std::tuple<std::array<long double,10>, std::array<std::map<std::string,Punkt>,2>> Transformation::berechne(){
        // Liste mit identischen Passpunkten im übergeordneten System, Map mit Passpunkten im lokalen System und die Schwerpunkte von der Funktion schwerpunkte()
        std::tuple<std::map<std::string,Punkt>, std::vector<Punkt>, Punkt, Punkt> s = this->schwerpunkte();

        // Liste der reduzierten Passpunkte im lokalen System und Dictionary der reduzierten Passpunkte im übergeordneten System von der Funktion reduktion()
        std::tuple<std::vector<Punkt>, std::map<std::string,Punkt>> r = this->reduktion(s);

        // Transformationsparameter mit der Funktion parameter() berechnen
        std::array<long double,10> p = this->parameter(std::get<0>(r), std::get<1>(r), std::get<2>(s), std::get<3>(s));

        // Transformation der Punkte und Berechnung der Restklaffen, json Dateien schreiben, Ausgabe der Dicts für Datendienst in GUI
        std::array<std::map<std::string,Punkt>,2> t = this->transformiere(std::get<1>(s), std::get<0>(s), p[2], p[3], p[4], p[5], p[0], p[1]);

        //Ausgabe der Transformationsparameter, transformierten Punkte und Restklaffen
        auto res = std::make_tuple(p, t); return res;
}

std::tuple<std::vector<Punkt>, std::map<std::string,Punkt>> Transformation::reduktion(std::tuple<std::map<std::string,Punkt>, std::vector<Punkt>, Punkt, Punkt>& s){
    Punkt p_a_s = std::get<2>(s);
    Punkt p_n_s = std::get<3>(s);
    // Definition von Liste und Dictionary für reduzierte Punkte
    std::vector<Punkt> punkte_alt_red;
    std::map<std::string, Punkt> punkte_neu_red;
    // Reduktion der Punkte im lokalen System
    for (auto & [key, item] : std::get<0>(s)){
        long double y_red = item.hole_y() - p_a_s.hole_y(), x_red = item.hole_x() - p_a_s.hole_x();
        // Punktobjekt aus Y- und X-Wert bilden und an Vektor anfügen
        Punkt p_red = Punkt(y_red, x_red, item.hole_nr()); punkte_alt_red.push_back(p_red);
    }
    std::cout<<std::endl;
    // Reduktion der Punkte im übergeordneten System
    for(Punkt el : std::get<1>(s)){
        long double y_red = el.hole_y() - p_n_s.hole_y();
        long double x_red = el.hole_x() - p_n_s.hole_x();
        // Punktobjekt aus Y und X Wert
        Punkt p_red = Punkt(y_red, x_red, el.hole_nr());
        // Punkt in Map mit Punktnummer als key einfügen
        punkte_neu_red[el.hole_nr()] = p_red;
    }
    //Ausgabe der reduzierten Punkte
    auto res = std::make_tuple(punkte_alt_red, punkte_neu_red); return res;
}

std::array<std::map<std::string,Punkt>,2> Transformation::transformiere(std::vector<Punkt>& p_ident_pkt_neu, std::map<std::string, Punkt>& p_ident_pkt_alt, long double& a1, long double& a2, long double& a3, long double& a4, long double& Y0, long double& X0){
    // Berechnung der Restklaffen -> über Passpunkte im übergeordneten System iterieren
    std::string nr; Punkt p_a; std::map<std::string, Punkt> Restklaffen;
    for(Punkt p_n : p_ident_pkt_neu){
        // Punktnummer holen
        nr = p_n.hole_nr();
        // entsprechenden Passpunkt aus lokalem System mit Punktnummer als Schlüssel holen
        p_a = p_ident_pkt_alt[nr];
        // Berechnung der Restklaffen
        long double Wy = -Y0 - a3 * p_a.hole_y() - a4 * p_a.hole_x() + p_n.hole_y();
        long double Wx = -X0 - a1 * p_a.hole_x() + a2 * p_a.hole_y() + p_n.hole_x();
        std::cout<<"wy = "<<std::setprecision(20)<<Wy<<std::endl;
        Restklaffen[nr] = (Punkt(Wy, Wx, nr));
    }
    // Transformation
    std::map<std::string, Punkt> transformierte_punkte;
    // über Punkte im lokalen System iterieren
    Punkt p_n;
    for (auto & [key, Pkt] : this->m_punkte_alt){
        // Rechts- und Hochwert des Punktes holen
        float y = Pkt.hole_y(); float x = Pkt.hole_x();
        // Transformation berechnen
        float Y = Y0 + a3 * y + a4 * x; float X = X0 + a1 * x - a2 * y;
        // Punktobjekt aus Y-, X-Wert und Punktnummer, Hinzufügen zur Map
        p_n = Punkt(Y, X, key); transformierte_punkte[key] = p_n;
    }
    std::array<std::map<std::string,Punkt>,2> ergebn; ergebn[0] = Restklaffen; ergebn[1] =transformierte_punkte;
    return ergebn;
}

std::tuple<std::map<std::string,Punkt>, std::vector<Punkt>, Punkt, Punkt> Transformation::schwerpunkte(){
    long double summe_y_a = 0.0, summe_x_a = 0.0, summe_y_n = 0.0, summe_x_n = 0.0;

    long double anzahl = 0.0d;
    // Map für Passpunkte alt, Vektor für Passpunkte neu
    std::map<std::string, Punkt> identischePktAlt; std::vector<Punkt> identischePktNeu;
    // Iteration über die Punkte im neuen System
    for(std::map<std::string, Punkt>::iterator it = this->m_punkte_neu.begin(); it != this->m_punkte_neu.end(); ++it){
        // Existiert der Punkt auch im alten Sys?
        if(this->m_punkte_alt.count(it->first) != 0){
            anzahl += 1.0d;
            // Alten Punkt aus Map holen
            Punkt p_a = this->m_punkte_alt[it->first];
            // Punkte der Map und dem Vektor hinzufügen
            identischePktAlt[it->first] = p_a; identischePktNeu.push_back(it->second);
            summe_y_a += p_a.hole_y(); summe_x_a += p_a.hole_x();
            summe_y_n += it->second.hole_y(); summe_x_n += it->second.hole_x();
        }
    }
    // Schwerpunkte berechnen
    Punkt p_a_s = Punkt(summe_y_a / anzahl, summe_x_a / anzahl, "pas");
    Punkt p_n_s = Punkt(summe_y_n / anzahl, summe_x_n / anzahl, "pns");
    std::cout<<"pns = "<<p_n_s.str()<<std::endl;
    //Ausgabe Punktlisten und Schwerpunkte
    std::tuple<std::map<std::string,Punkt>, std::vector<Punkt>, Punkt, Punkt> res = {identischePktAlt, identischePktNeu, p_a_s, p_n_s};
    return res;
}

std::array<long double,6> Transformation::parameter_base(long double& a1, long double& a2, long double& a3, long double& a4, Punkt& p_a_s, Punkt& p_n_s) {
// float* parameter(Punkt* punkte_alt_red, std::map<std::string,Punkt>& punkte_neu_red, float& p_a_s, float& p_n_s){
    // Translation berechnen
    long double Y0 = p_n_s.hole_y() - a3 * p_a_s.hole_y() - a4 * p_a_s.hole_x();
std::cout<<"Y0 long double = "<<std::setprecision(18)<<Y0<<", p_n_s_y = "<< p_n_s.hole_y()<<", a3 = "<<a3<<"pasY = "<< p_a_s.hole_y()<<",  a4 = "<<a4<<"pasx = "<<p_a_s.hole_x()<<std::endl;
    long double X0 = p_n_s.hole_x() - a1 * p_a_s.hole_x() + a2 * p_a_s.hole_y();
    //Punktobjekt aus Y und X Wert
    Punkt P0 = Punkt(Y0, X0,"P0");
    //Massstab
    long double m1 = sqrt(pow(a1,2) + pow(a4,2)); long double m2 = sqrt(pow(a2,2) + pow(a3,2));
    // Drehwinkel
    long double alpha = atan2(a4, a1); int n = alpha/400; alpha -= n*400;
    long double beta = atan2(a2, a3);
    //Ausgabe der Parameter
    std::array<long double,6> arr = {Y0, X0, m1,m2, alpha, beta}; return arr;
}

std::array<long double,10> Transformation::parameter(std::vector<Punkt>& punkte_alt_red, std::map<std::string, Punkt>& punkte_neu_red, Punkt& p_a_s, Punkt& p_n_s){

    long double zaehler_o = 0.0, zaehler_a = 0.0, nenner = 0.0; std::string nr; Punkt p_red_neu;

    // Bildung der Summen durch for-Schleife durch Liste der alten reduzierten Passpunkte
    for(Punkt p_red_alt : punkte_alt_red){
        // Punktnummer holen
        nr = p_red_alt.hole_nr();
        // entsprechenden reduzierten neuen Passpunkt mit Punktnummer als Schluessel holen
        p_red_neu = punkte_neu_red[nr];
        // Aufaddieren der verschiedenen Therme zur Summenbildung
        zaehler_o += p_red_alt.hole_x()*p_red_neu.hole_y()-p_red_alt.hole_y()*p_red_neu.hole_x();
        zaehler_a += p_red_alt.hole_x()*p_red_neu.hole_x()+p_red_alt.hole_y()*p_red_neu.hole_y();
        // Berechnung des Nenners aus den Summen
        nenner +=  pow(p_red_alt.hole_x(),2) + pow(p_red_alt.hole_y(),2);
    }
    // Berechnung der Transformationsparameter a1-a4 (bzw. a und o) durch Summen und Nenner. Doppelte Belegung der 4 Variablen für Nutzung der Elternklasse Transformation
    long double a1 = zaehler_a/nenner;    //a
    long double a3 = a1;                  //o
    long double a2 = zaehler_o/nenner;    //a
    long double a4 = a2;                  //o
    std::cout<<"a3 à l'origine = "<<std::setprecision(20)<<a3<<", Zaehler_a = "<<std::setprecision(15)<<zaehler_a<<", nenner = "<<std::setprecision(12)<<nenner<<std::endl;
    // Aufruf der base class method parameter mit Parametern a1-a4 und Schwerpunkten
    std::array<long double,6> param = this->parameter_base(a1, a2, a3, a4, p_a_s, p_n_s);
    // restliche von base class method berechnete Transformationsparameter aus Ergebnistupel holen
    Punkt P0 = Punkt(param[0], param[1]);           // Translation
    long double m1 = param[2];                      // Massstab
    long double m2 = 0.0f;
    long double alpha = rad2gon(param[4]);    // Drehwinkel
    std::cout<<"alpha nach Konvertierung: "<<alpha<<std::endl;
    long double beta = 0.0;
    // Ausgabe der Transformationsarameter
    std::array<long double, 10> vec = {param[0], param[1], a1, a2, a3, a4, m1, m2, alpha, beta};
    return vec;
}







