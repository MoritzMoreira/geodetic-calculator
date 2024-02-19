#include "helmerttransformation_gui.h"
#include "ui_helmerttransformation_gui.h"
#include "mainwindow.h"
#include <QFileDialog>
#include <QMessageBox>
#include <QDir>
#include <QFile>
#include <QTextStream>
#include <map>
#include <nlohmann/json.hpp>
#include <QString>
#include <QPixmap>

Helmerttransformation_gui::Helmerttransformation_gui(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::Helmerttransformation_gui)
{
    ui->setupUi(this);
    QPixmap helmert(":/new/prefix1/helmert.png");
    ui->label_helmert->setPixmap(helmert.scaled(377, 362, Qt::KeepAspectRatio));
}

Helmerttransformation_gui::~Helmerttransformation_gui()
{
    delete ui;
}

void Helmerttransformation_gui::on_pushButton_test_clicked()
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

void Helmerttransformation_gui::on_pushButton_test2_clicked()
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


void Helmerttransformation_gui::on_pushButton_datei_clicked()
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


void Helmerttransformation_gui::on_pushButton_berechne_clicked()
{
    std::string json_in = ui->plainTextEdit_in->toPlainText().toStdString();
    // Raw string to json type
    nlohmann::ordered_json jsdata = nlohmann::ordered_json::parse(json_in);
    nlohmann::ordered_json json_punkte_alt = jsdata["p_a"];
    nlohmann::ordered_json json_punkte_neu = jsdata["p_n"];
    std::map<std::string, Punkt> punkte_alt = json2punktMap(json_punkte_alt);
    std::map<std::string, Punkt> punkte_neu = json2punktMap(json_punkte_neu);

   Transformation trafo_instanz(punkte_alt, punkte_neu);
   auto Ergebnis = trafo_instanz.berechne();
   auto restkl_punkte = std::get<1>(Ergebnis);

   std::array<long double,10> parameter = std::get<0>(Ergebnis);
   ui->lineEdit_m->setText(QString::number((float)parameter[6]));
   ui->lineEdit_winkel->setText(QString::number((float)parameter[8]));
   ui->lineEdit_transY->setText(QString::number((float)parameter[0]));
   ui->lineEdit_transX->setText(QString::number((float)parameter[1]));
   ui->lineEdit_a->setText(QString::number((float)parameter[2]));
   ui->lineEdit_o->setText(QString::number((float)parameter[3]));
   ui->plainTextEdit_out->setPlainText(QString::fromStdString(punktMap2json(restkl_punkte[1],4)));
   ui->plainTextEdit_rstklf->setPlainText(QString::fromStdString(punktMap2json(restkl_punkte[0],20)));
}

void Helmerttransformation_gui::on_pushButton_speichern_clicked()
{
    QString json_out = ui->plainTextEdit_out->toPlainText();
    QString dateipfad = QFileDialog::getSaveFileName(this, tr("Transformierte Punkte als json-Datei speichern"), QDir::homePath()).append(".json");
    QFile datei(dateipfad);
    if(!datei.open(QFile::WriteOnly | QFile::Text)){}
    QTextStream out(&datei);
    out << json_out; datei.close(); datei.flush(); datei.close();
}

