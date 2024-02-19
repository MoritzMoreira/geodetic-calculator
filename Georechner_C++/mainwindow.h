#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <map>
#include <iostream>
#include <nlohmann/json.hpp>
#include <QTranslator>
#include <QActionGroup>
#include <QLocale>
#include <QApplication>
#include <QDir>
#include <QAction>

#include "winkel_gui.h"
#include "erstegrund_gui.h"
#include "zweitegrund_gui.h"
#include "bogenschnitt_gui.h"
#include "rueckwaertsschnitt_gui.h"
#include "vorwaertsschnitt_gui.h"
#include "helmerttransformation_gui.h"
#include "affintransformation_gui.h"
#include "polygonzug_gui.h"
#include "ui_mainwindow.h"


QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
    Ui::MainWindow *ui;


private slots:
    void on_Winkel_clicked();
    void on_ersteGrund_clicked();
    void on_Bogenschnitt_clicked();
    void on_zweiteGrund_clicked();
    void on_rueckwSchnitt_clicked();
    void on_Vorwaertsschn_clicked();
    void on_HelmertTrafo_clicked();
    void on_AffinTrafo_clicked();
    void on_PolygonzugAngeschl_clicked();

    void on_lang_comboBox_activated(int index);

private:
    //Ui::MainWindow *ui;
    Winkel_gui *winkel_gui_ptr; ersteGrund_gui *erstegrund_gui_ptr; zweitegrund_gui *zweitegrund_gui_ptr;
    Bogenschnitt_gui *bogenschnitt_gui_ptr; vorwaertsschnitt_gui *vorwaertsschnitt_gui_ptr;
    rueckwaertsschnitt_gui *rueckwaertsschnitt_gui_ptr; Helmerttransformation_gui *helmerttransformation_gui_ptr;
    affintransformation_gui *affintransformation_gui_ptr; polygonzug_gui *polygonzug_gui_ptr;
};

// Funktionen
long double roundoff(long double value, int prec);
        // grundlagen/winkel.cpp
float rad2gon(float& p_rad);
long double rad2gon(long double& p_rad);float rad2deg(float& p_rad); float gon2rad(float& p_gon); float gon2deg(float& p_gon);
float deg2rad(float& p_deg); float deg2gon(double& p_deg); float cot(float& p_ctg); float richtungswinkel_aus_richtung(float t, float r);

        // grundlagen/erstegrund
float* umrechnen_koordinaten(float& y1, float& x1, float& s12, float& t12);
float umrechnen_koordinatenunterschiedey(float& s, float& t); float umrechnen_koordinatenunterschiedex(float& s, float& t);


// Klassen
class Punkt{
public:
    Punkt(const long double& p_y = 0.0f, const long double& p_x = 0.0f, const std::string& p_nr = "" );
    void setze_y(long double& set_y); void setze_x(long double& set_x);
    long double hole_y(); long double hole_x(); std::string str();
    void setze_nr(std::string& set_nr); std::string hole_nr();
private:
   long double m_y, m_x; std::string m_nr;
};

std::map<std::string,Punkt> json2punktMap(nlohmann::ordered_json& p_json_daten);
std::string punktMap2json(std::map<std::string,Punkt>&, int);

class Strecke{
public:
    Strecke(const Punkt&, const Punkt&, const int& p_d = 5, const std::string& p_dnr = "");
    Strecke(const Punkt&, float&, const std::string& p_dnr = "");
    void setze_nr(std::string&); std::string hole_nr();
    Punkt hole_p1(); Punkt hole_p2();
    std::array<float, 2> riwi_laenge(); std::string str_d();
private:
    Punkt m_p1, m_p2; int m_d; float m_laenge; std::string m_dnr;
};

class Winkel{
public:
    Winkel(const float& p_winkel = 0.0f, const std::string p_Einheit = "", const std::string& p_wnr = "");
    void setze_nr(std::string& set_wnr); std::string hole_nr();
    void setze_gon(float& set_gon); float hole_gon();
    void setze_deg(float& set_deg); float hole_deg();
    void setze_rad(float& set_rad); float hole_rad();
    std::string str();
private:
    float m_rad, m_winkel; std::string m_wnr;
};

class Bogenschnitt{
public:
    Bogenschnitt(Strecke&, Strecke&, Strecke&);
    // gemessene Strecken: s1: von Punkt 1 zum Neupunkt; s2: von Punkt 2 zum NP; s3: von Punkt 1 zu Punkt 2
    std::vector<float> berechne();
    // berechne keinen, einen oder zwei Neupunkte und ggf. ein Massstab
protected:
    Strecke m_s1, m_s2, m_s3;
};

class Rueckwaertsschnitt{
public:
    Rueckwaertsschnitt(Punkt&, Punkt&, Punkt&, float&, float&, float&);
    // p1-p3: bekannte Punkt, r1: Richtung auf Punkt 1, r2: Richtung auf Punkt 2, r3: Richtung auf Punkt 3

    std::vector<float> berechne();
private:
    Punkt m_p1, m_p2, m_p3; float m_r1, m_r2, m_r3;
};

class Vorwaertsschnitt{
public:
    Vorwaertsschnitt(Punkt&, Punkt&, Punkt&, Punkt&, float&, float&);
    // p1 - p4: bekannte Punkte; phi: Winkel auf Punkt 1 zwischen Punkt 4 und Punkt N
    // psi: Winkel auf Punkt 2 zwischen Punkt 3 und Punkt N
    std::vector<float> berechne();
private:
    Punkt m_p1, m_p2, m_p3, m_p4; float m_phi, m_psi;
};

class Transformation{
public:
    Transformation(std::map<std::string, Punkt>&, std::map<std::string, Punkt>&);
    // Elternklasse von AffinTransformation

    std::tuple<std::array<long double,10>, std::array<std::map<std::string,Punkt>,2>> berechne();

    std::tuple<std::vector<Punkt>, std::map<std::string,Punkt>> reduktion(std::tuple<std::map<std::string,Punkt>, std::vector<Punkt>, Punkt, Punkt>&);
    // Reduziert Passpunkte auf Schwerpunkt; s: Ausgabe von Funktion schwerpunkte
    // return: Liste der reduzierten Passpunkte im lokalen System, Map der reduzierten Punkte im übergeordneten System

    std::array<std::map<std::string,Punkt>,2> transformiere(std::vector<Punkt>&, std::map<std::string, Punkt>&, long double&, long double&, long double&, long double&, long double&, long double&);
    // Transformation der Punkte und Berechnung der Restklaffen
    // return: Restklaffen und transformierte Punkte

    std::tuple<std::map<std::string,Punkt>, std::vector<Punkt>, Punkt, Punkt> schwerpunkte();
    // Schwerpunkte der Passpunkte im alten und neuen System berechnen
    // return: identische_punkte_alt, identische_punkte_neu, Schwerpunkte

    std::array<long double,6> parameter_base(long double&, long double&, long double&, long double&, Punkt&, Punkt&);
    // return: Translation, Massstäbe, Drehwinkel

    virtual std::array<long double,10> parameter(std::vector<Punkt>&, std::map<std::string, Punkt>&, Punkt&, Punkt&);

private:
    std::map<std::string, Punkt> m_punkte_alt, m_punkte_neu;
};

class Affintransformation: public Transformation{
public:
    Affintransformation(std::map<std::string, Punkt>&, std::map<std::string, Punkt>&);
    std::array<long double,10> parameter(std::vector<Punkt>&, std::map<std::string, Punkt>&, Punkt&, Punkt&) override;
private:
    std::map<std::string, Punkt> m_punkte_alt, m_punkte_neu;
};

class PolygonzugBeidseitig{
public:
    PolygonzugBeidseitig(float&, float&, float&, float&, float&, float&, float&, float&,
                         std::vector<float>&, const std::vector<float>&);
    std::tuple<std::map<std::string,Punkt>,float> berechne();
protected:
    float m_y0, m_x0,  m_y1,  m_x1,  m_yN,  m_xN,  m_yN1,  m_xN1;
    std::vector<float> m_vector_richtungen = {};
    std::vector<float> m_vector_strecken = {};
};

#endif // MAINWINDOW_H
