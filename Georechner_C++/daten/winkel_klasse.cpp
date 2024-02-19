#include <iostream>
#include "mainwindow.h"

Winkel::Winkel(const float& p_winkel, const std::string p_Einheit, const std::string& p_wnr): m_winkel(p_winkel), m_wnr(p_wnr){
    if(p_Einheit == "rad"){
        this->m_rad = this->m_winkel;
    }
    else if(p_Einheit == "gon"){
        this->m_rad = gon2rad(this->m_winkel);
    }
    else if(p_Einheit == "grad"){
        this->m_rad = deg2rad(this->m_winkel);
    }
}
//Winkel::Winkel(const float& p_deg, const std::string& p_wnr): m_rad(deg2rad(p_deg)), m_wnr(p_wnr){}
//Winkel::Winkel(const float& p_gon = 0.0, const std::string& p_wnr = ""): m_rad(gon2rad(p_deg)), m_wnr(p_wnr){}

void Winkel::setze_nr(std::string& set_wnr){
    this->m_wnr = set_wnr;
}
std::string Winkel::hole_nr(){
    return this->m_wnr;
}
void Winkel::setze_gon(float& set_gon){
    this->m_rad = gon2rad(set_gon);
}
float Winkel::hole_gon(){
    return rad2gon(this->m_rad);
}
void Winkel::setze_deg(float& set_deg){
    this->m_rad = deg2rad(set_deg);
}
float Winkel::hole_deg(){
    return rad2deg(this->m_rad);
}
void Winkel::setze_rad(float& set_rad){
    this->m_rad = set_rad;
}
float Winkel::hole_rad(){
    return this->m_rad;
}
std::string Winkel::str(){
        std::string zeichen = "Nr:" + this->m_wnr + \
                      " rad:" + std::to_string(this->m_rad) + \
                      " deg" + std::to_string(rad2deg(this->m_rad)) + \
                      " gon" + std::to_string(rad2gon(this->m_rad));
        return zeichen;
}


