#include <iostream>
#include <map>
#include <fstream>
#include <nlohmann/json.hpp>
#include "mainwindow.h"
#include <sstream>


Punkt::Punkt(const long double& p_y, const long double& p_x, const std::string& p_nr): m_y(p_y), m_x(p_x), m_nr(p_nr) {}

void Punkt::setze_y(long double& set_y){
    this->m_y = set_y;
}
void Punkt::setze_x(long double& set_x){
          m_x = set_x;
}
long double Punkt::hole_y(){
    return this->m_y;
}
long double Punkt::hole_x(){
    return this->m_x;
}

std::string Punkt::str(){
    std::string zeichenkette = "Nr. " + this->m_nr + ":  y = " + std::to_string(this->m_y) + ", x = " + std::to_string(this->m_x);
    return zeichenkette;
}
void Punkt::setze_nr(std::string& set_nr){
    this->m_nr = set_nr;
}
std::string Punkt::hole_nr(){
    return this->m_nr;
}

std::map<std::string,Punkt> json2punktMap(nlohmann::ordered_json& p_json_daten){
    std::map<std::string, Punkt> punktMap;
    for(auto it = p_json_daten.begin(); it != p_json_daten.end(); ++it){
        punktMap[it.value()["_Punkt__nr"]] = Punkt(it.value()["_Punkt__y"], it.value()["_Punkt__x"], it.value()["_Punkt__nr"]);
    }
    return punktMap;
}

std::string punktMap2json(std::map<std::string,Punkt>& p_punktmap, int n){
    std::string js = "";
    for(auto& it : p_punktmap){
        std::ostringstream outy, outx;
        outy.precision(n); outx.precision(n);
        outy << it.second.hole_y(); outx << it.second.hole_x();
        js += "    '" + it.first +
                "': {\n        '_Punkt__nr': '" + it.first +
                "',\n        '_Punkt__x': " + std::move(outx).str() +
                ",\n        '_Punkt__y': " + std::move(outy).str() + "\n    },\n";
    }
    js = "{\n" + js.substr(0, js.length()-1) + "\n}";
    return js;
}

