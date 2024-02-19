#include "mainwindow.h"
#include <iostream>
#include <numeric>

PolygonzugBeidseitig::PolygonzugBeidseitig(float& p_y0, float& p_x0, float& p_y1, float& p_x1, float& p_yN, float& p_xN, float& p_yN1, float& p_xN1,
                                           std::vector<float>& p_vector_richtungen, const std::vector<float>& p_vector_strecken):
    m_y0(p_y0), m_x0(p_x0), m_y1(p_y1), m_x1(p_x1), m_yN(p_yN), m_xN(p_xN), m_yN1(p_yN1), m_xN1(p_xN1),
    m_vector_richtungen(p_vector_richtungen), m_vector_strecken(p_vector_strecken) {}

std::tuple<std::map<std::string,Punkt>,float> PolygonzugBeidseitig::berechne(){
    // t01 = Richtungswinkel zwischen P0 und P1
    // tN = Richtungswinkel zwischen PN und PN+1
    float t01 = Strecke(Punkt(this->m_y0, this->m_x0), Punkt(this->m_y1, this->m_x1)).riwi_laenge()[0];
    float tN = roundoff(Strecke(Punkt(this->m_yN, this->m_xN), Punkt(this->m_yN1, this->m_xN1)).riwi_laenge()[0], 7);

    // Anzahl Richtungsmessungen
    float n_r = this->m_vector_richtungen.size();
    // Gesamtstrecke der Streckenmessungen
    float s_sum = std::accumulate(this->m_vector_strecken.begin(), this->m_vector_strecken.end(), 0.0f);
    // Summe aller Richtungsmessungen
    float r_sum = std::accumulate(this->m_vector_richtungen.begin(), this->m_vector_richtungen.end(), 0.0f);

    /// waf: Winkelabschlussfehler
    float waf = (tN-t01) - (r_sum);
    // Bestimmung des Winkelabschlussfehlers
    if(waf>0){
        waf -= (n_r) * 200;
    }
    else{waf += (n_r) *200;
    }
    waf = roundoff(waf, 8);

    // Berechnung der verbesserten Richtungswinkel
    std::vector<float> r_verbessert = {t01};
    float r0;
    for(int i = 0; i < n_r; i++){
        r0 = richtungswinkel_aus_richtung(r_verbessert[i], this->m_vector_richtungen[i]) + waf / n_r;
        r_verbessert.push_back(r0);
    }
    //Berechnung der Koordinatenabweichungen wx und wy
    std::vector<float> deltay;
    std::vector<float> deltax;
    float dy;
    for(int i = 1; i < n_r; i++){
        dy = umrechnen_koordinatenunterschiedey((this->m_vector_strecken[i-1]), r_verbessert[i]);
        deltay.push_back(dy);
    }
    float dx;
    for(int i = 1; i < n_r; i++){
        dx = umrechnen_koordinatenunterschiedex((this->m_vector_strecken[i-1]), r_verbessert[i]);
        deltax.push_back(dx);
    }
    for (auto el : deltay){
        std::cout<<el<<" |  ";
    }
    std::cout<<std::endl;
    // sumy: Summe der deltay Werte
    float sumy = std::accumulate(deltay.begin(), deltay.end(), 0.0f);
    std::cout<<"sumy = "<<sumy<<std::endl;
    // Summe der deltax Werte
    float sumx = std::accumulate(deltax.begin(), deltax.end(), 0.0f);
    std::cout<<"sumx = "<<sumx<<std::endl;
    // Koordinatenabweichung in y Richtung
    float wy = (this->m_yN - this->m_y1) - sumy;
    // Koordinatenabweichung in x Richtung
    float wx = (this->m_xN - this->m_x1) - sumx;
    //float z = roundoff(sizeof(werte)/2, 1);

    std::vector<float> Pkty;
    // Bestimmen der gesuchten Y Werte der Punkte
    for(unsigned int i = 0; i < deltay.size(); i++){
        this->m_y1 += deltay[i] + (wy / s_sum) * this->m_vector_strecken[i];
        Pkty.push_back(this->m_y1);
    }
    std::vector<float> Pktx;
    // Bestimmen der gesuchten X Werte der Punkte
    for(unsigned int i = 0; i < deltax.size(); i++){
        this->m_x1 += deltax[i] + (wx / s_sum) * this->m_vector_strecken[i];
        Pktx.push_back(this->m_x1);
    }
    // Erstellen einer leeren Map zur Speicherung der gesuchten Punkte
    std::map<std::string, Punkt> dict;
    std::cout<<"ooioitest  2, 3:  "<<Pkty.size()<<std::endl;
    for(unsigned int i = 0; i < Pkty.size()-1; i++){
        std::string nr = std::to_string(i+2);
        dict[nr] = Punkt(Pkty[i], Pktx[i], nr);
    }
    std::cout<<"ooioitest  2, 3:  "<<dict["2"].str()<<dict["3"].str()<<std::endl;
    auto res = std::make_tuple(dict, waf);
    return res;
}
