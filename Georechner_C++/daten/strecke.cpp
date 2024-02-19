#include <iostream>
#include "mainwindow.h"
#include <typeinfo>

Strecke::Strecke(const Punkt& p_p1, const Punkt& p_p2, const int& p_d, const std::string& p_dnr): m_p1(p_p1), m_p2(p_p2), m_d(p_d), m_dnr(p_dnr) {}

Strecke::Strecke(const Punkt& p_p1, float& p_laenge, const std::string& p_dnr ): m_p1(p_p1), m_laenge(p_laenge), m_dnr(p_dnr){
    std::cout<<"Konstruktor 2 aufgerufen"<<std::endl;
    std::string l_str = std::to_string(this->m_laenge);
    int m_d = sizeof(l_str.substr(l_str.find(".") + 1))/16;

    this->m_p2 = Punkt(this->m_p1.hole_y(), this->m_p1.hole_x() + this->m_laenge);
    std::cout<<m_p1.str()<<"   "<<m_p2.str()<<std::endl;
}

void Strecke::setze_nr(std::string& set_dnr){
    this->m_dnr = set_dnr;}

std::string Strecke::hole_nr(){
    return this->m_dnr;}

Punkt Strecke::hole_p1(){
    return this->m_p1;}
Punkt Strecke::hole_p2(){
        return this->m_p2;}

std::array<float, 2> Strecke::riwi_laenge(){
        float t12 = atan2((this->m_p2.hole_y() - this->m_p1.hole_y()), (this->m_p2.hole_x() - this->m_p1.hole_x()));
        float s12 = sqrt(pow(this->m_p2.hole_y() - this->m_p1.hole_y(), 2) + pow(this->m_p2.hole_x() - this->m_p1.hole_x(), 2));
        std::cout<<m_p1.str()<<" in riwi laenge  "<<m_p2.str()<<std::endl;        //s12 = roundoff(s12, 5);
        t12 = rad2gon(t12);
        std::array<float, 2> arr_t12_s12 = {t12, s12};
        return arr_t12_s12;
}

std::string Strecke::str_d(){
    std::array<float, 2> ts = this->riwi_laenge();
    std::string zeichen = "Nr:" + this->m_dnr + "p1:" + this->m_p1.str() + ", p2:" + this->m_p2.str() + ", t=" + std::to_string(ts[0]) + ", s=" + std::to_string(ts[1]);
    return zeichen;
}

