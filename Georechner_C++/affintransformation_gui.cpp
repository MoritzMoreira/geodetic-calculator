#include "affintransformation_gui.h"
#include "ui_affintransformation_gui.h"
#include "mainwindow.h"

#include <QFileDialog>
#include <QMessageBox>
#include <QDir>
#include <QFile>
#include <QTextStream>
#include <iostream>
#include <map>
#include <nlohmann/json.hpp>
#include <QString>
#include <QPixmap>
#include <QTranslator>

affintransformation_gui::affintransformation_gui(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::affintransformation_gui)
{
    ui->setupUi(this);
    QPixmap affin(":/new/prefix1/Affine.gif");
    ui->label_affin->setPixmap(affin.scaled(387, 290, Qt::KeepAspectRatio));
}

affintransformation_gui::~affintransformation_gui()
{
    delete ui;
}

void affintransformation_gui::on_pushButton_datei_clicked()
{
    QString dateiname = QFileDialog::getOpenFileName(this, tr("Lade json-Datei"), QDir::homePath());
    ui->lineEdit_dateipfad->setText(dateiname);
    QString dateipfad = ui->lineEdit_dateipfad->text();
    QFile datei(dateipfad);
    if(!datei.open(QFile::ReadOnly | QFile::Text)){}
    QTextStream in(&datei);
    QString text  = in.readAll();
    ui->plainTextEdit_in->setPlainText(text);
    datei.close();

}

void affintransformation_gui::on_pushButton_berechne_clicked()
{
    std::string json_in = ui->plainTextEdit_in->toPlainText().toStdString();
    // String zu json type konvertieren
    nlohmann::ordered_json jsdata = nlohmann::ordered_json::parse(json_in);
    nlohmann::ordered_json json_punkte_alt = jsdata["p_a"];
    nlohmann::ordered_json json_punkte_neu = jsdata["p_n"];
    std::map<std::string, Punkt> punkte_alt = json2punktMap(json_punkte_alt);
    std::map<std::string, Punkt> punkte_neu = json2punktMap(json_punkte_neu);

   Affintransformation affintrafo_instanz(punkte_alt, punkte_neu);
   auto Ergebnis = affintrafo_instanz.berechne();

   std::array<long double,10> parameter = std::get<0>(Ergebnis);
   auto restkl_punkte = std::get<1>(Ergebnis);
   std::cout<<typeid(parameter[8]).name()[0];

   ui->lineEdit_my->setText(QString::number((float)parameter[6]));
   ui->lineEdit_mx->setText(QString::number((float)parameter[7]));
   ui->lineEdit_alpha->setText(QString::number((float)rad2gon(parameter[8])));
   ui->lineEdit_beta->setText(QString::number((float)rad2gon(parameter[9])));
   ui->lineEdit_transY->setText(QString::number((float)parameter[0]));
   ui->lineEdit_transX->setText(QString::number((float)parameter[1]));
   ui->lineEdit_a1->setText(QString::number((float)parameter[2]));
   ui->lineEdit_a2->setText(QString::number((float)parameter[3]));
   ui->lineEdit_a3->setText(QString::number((float)parameter[4]));
   ui->lineEdit_a4->setText(QString::number((float)parameter[5]));
   ui->plainTextEdit_out->setPlainText(QString::fromStdString(punktMap2json(std::get<1>(restkl_punkte), 5)));
   ui->plainTextEdit_rstklf->setPlainText(QString::fromStdString(punktMap2json(restkl_punkte[0], 20)));
}


void affintransformation_gui::on_pushButton_test_clicked()
{
    ui->lineEdit_dateipfad->setText(":/new/prefix1/transformationen/lokale_Punkte.json");
    QString dateipfad = ui->lineEdit_dateipfad->text();
    QFile datei(dateipfad);
    if(!datei.open(QFile::ReadOnly | QFile::Text)){}
    QTextStream in(&datei);
    QString text  = in.readAll();
    ui->plainTextEdit_in->setPlainText(text);
    datei.close();

}


void affintransformation_gui::on_pushButton_test2_clicked()
{
    ui->lineEdit_dateipfad->setText(":/new/prefix1/transformationen/lokale_Punkte2.json");
    QString dateipfad = ui->lineEdit_dateipfad->text();
    QFile datei(dateipfad);
    if(!datei.open(QFile::ReadOnly | QFile::Text)){}
    QTextStream in(&datei);
    QString text  = in.readAll();
    ui->plainTextEdit_in->setPlainText(text);
    datei.close();
}


void affintransformation_gui::on_pushButton_speichern_clicked()
{
    QString json_out = ui->plainTextEdit_out->toPlainText();
    QString dateipfad = QFileDialog::getSaveFileName(this, tr("Transformierte Punkte als json-Datei speichern"), QDir::homePath()).append(".json");
    QFile datei(dateipfad);
    if(!datei.open(QFile::WriteOnly | QFile::Text)){}
    QTextStream out(&datei);
    out << json_out; datei.close(); datei.flush(); datei.close();
}

