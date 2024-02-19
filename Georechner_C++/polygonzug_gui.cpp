#include "polygonzug_gui.h"
#include "ui_polygonzug_gui.h"
#include "mainwindow.h"
#include <QFileDialog>
#include <QMessageBox>
#include <QDir>
#include <QFile>
#include <QTextStream>
#include <iostream>
#include <map>
#include <fstream>
#include <nlohmann/json.hpp>
#include <QString>
#include <QPixmap>

polygonzug_gui::polygonzug_gui(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::polygonzug_gui)
{
    ui->setupUi(this);
    QPixmap helmert(":/new/prefix1/poly.png");
    ui->label_poly->setPixmap(helmert.scaled(654, 179, Qt::KeepAspectRatio));
}

polygonzug_gui::~polygonzug_gui()
{
    delete ui;
}

void polygonzug_gui::on_pushButton_datei_p_clicked()
{
    QString dateiname = QFileDialog::getOpenFileName(this, "Lade json-Datei", QDir::homePath());
    ui->lineEdit_dateipfad_p->setText(dateiname);
    QString dateipfad = ui->lineEdit_dateipfad_p->text();
    QFile datei(dateipfad);
    if(!datei.open(QFile::ReadOnly | QFile::Text)){}
    QTextStream in(&datei);
    QString text  = in.readAll();
    ui->plainTextEdit_p->setPlainText(text);
    datei.close();
}


void polygonzug_gui::on_pushButton_datei_rs_clicked()
{
    QString dateiname = QFileDialog::getOpenFileName(this, "Lade json-Datei", QDir::homePath());
    ui->lineEdit_dateipfad_rs->setText(dateiname);
    QString dateipfad = ui->lineEdit_dateipfad_rs->text();
    QFile datei(dateipfad);
    if(!datei.open(QFile::ReadOnly | QFile::Text)){}
    QTextStream in(&datei);
    QString text  = in.readAll();
    ui->plainTextEdit_rs->setPlainText(text);
    datei.close();
}


void polygonzug_gui::on_pushButton_berechne_clicked(){
    std::string json_in = ui->plainTextEdit_p->toPlainText().toStdString();
    // Raw string to json type
    nlohmann::ordered_json jsdata = nlohmann::ordered_json::parse(json_in);
    float y0(jsdata["P0"]["y"]), x0(jsdata["P0"]["x"]), y1(jsdata["P1"]["y"]), x1(jsdata["P1"]["x"]),
          yN(jsdata["PN"]["y"]), xN(jsdata["PN"]["x"]), yN1(jsdata["PN+1"]["y"]), xN1(jsdata["PN+1"]["x"]);

    std::string json_rs = ui->plainTextEdit_rs->toPlainText().toStdString();
    // Raw string to json type
    nlohmann::ordered_json js_rs = nlohmann::ordered_json::parse(json_rs);
    std::vector<float> vector_richtungen;
    std::vector<float> vector_strecken;
    for(auto it = js_rs.begin(); it != js_rs.end(); ++it){
        if(it.key().substr(0,1) == "r"){
            vector_richtungen.push_back(it.value());
        }
        else{vector_strecken.push_back(it.value());}
    }
    std::cout<<"n_r: "<<vector_richtungen.size()<<std::endl;
    std::cout<<"n_r: "<<vector_strecken.size()<<std::endl;

   PolygonzugBeidseitig poly_instanz(y0, x0, y1, x1, yN, xN, yN1, xN1, vector_richtungen, vector_strecken);
   std::tuple<std::map<std::string,Punkt>,float> Erg = poly_instanz.berechne();
   std::map<std::string,Punkt> Ergebnis = std::get<0>(Erg);
   std::string gesuchtePunkte = punktMap2json(Ergebnis, 6);
   ui->plainTextEdit_pn->setPlainText(QString::fromStdString(punktMap2json(Ergebnis, 6)));
   ui->lineEdit_waf->setText(QString::number(std::get<1>(Erg)));
}

void polygonzug_gui::on_pushButton_test_clicked()
{
    ui->lineEdit_dateipfad_p->setText(":/new/prefix1/transformationen/punkte_polygon.json");
    QString dateipfad = ui->lineEdit_dateipfad_p->text();
    QFile datei(dateipfad);
    if(!datei.open(QFile::ReadOnly | QFile::Text)){}
    QTextStream in(&datei);
    QString text  = in.readAll();
    ui->plainTextEdit_p->setPlainText(text);
    datei.close();

    ui->lineEdit_dateipfad_rs->setText(":/new/prefix1/transformationen/runds_polygon.json");
    QString dateipfad_rs = ui->lineEdit_dateipfad_rs->text();
    QFile datei_rs(dateipfad_rs);
    if(!datei_rs.open(QFile::ReadOnly | QFile::Text)){}
    QTextStream in_rs(&datei_rs);
    QString text_rs  = in_rs.readAll();
    ui->plainTextEdit_rs->setPlainText(text_rs);
    datei.close();
}

void polygonzug_gui::on_pushButton_speichern_clicked()
{
    QString json_out = ui->plainTextEdit_pn->toPlainText();
    QString dateipfad = QFileDialog::getSaveFileName(this, "Gesuchte Punkte als json-Datei speichern", QDir::homePath()).append(".json");
    QFile datei(dateipfad);
    if(!datei.open(QFile::WriteOnly | QFile::Text)){}
    QTextStream out(&datei);
    out << json_out;
    datei.close();
    datei.flush();
    datei.close();
}

