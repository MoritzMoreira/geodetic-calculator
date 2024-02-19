#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QMessageBox>
#include <QTranslator>
#include <QInputDialog>
#include <QStatusBar>
#include <QMenu>
#include <QSettings>
#include <QDebug>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_Winkel_clicked(){
    winkel_gui_ptr = new Winkel_gui(this);
    winkel_gui_ptr->show();
}

void MainWindow::on_ersteGrund_clicked()
{
    erstegrund_gui_ptr = new ersteGrund_gui(this);
    erstegrund_gui_ptr->show();
}

void MainWindow::on_zweiteGrund_clicked()
{
    zweitegrund_gui_ptr = new zweitegrund_gui(this);
    zweitegrund_gui_ptr->show();
}

void MainWindow::on_Bogenschnitt_clicked()
{
    bogenschnitt_gui_ptr = new Bogenschnitt_gui(this);
    bogenschnitt_gui_ptr->show();
}

void MainWindow::on_rueckwSchnitt_clicked()
{
    rueckwaertsschnitt_gui_ptr = new rueckwaertsschnitt_gui(this);
    rueckwaertsschnitt_gui_ptr->show();
}


void MainWindow::on_Vorwaertsschn_clicked()
{
    vorwaertsschnitt_gui_ptr = new vorwaertsschnitt_gui(this);
    vorwaertsschnitt_gui_ptr->show();
}


void MainWindow::on_HelmertTrafo_clicked()
{
    helmerttransformation_gui_ptr = new Helmerttransformation_gui(this);
    helmerttransformation_gui_ptr->show();
}


void MainWindow::on_AffinTrafo_clicked()
{
    affintransformation_gui_ptr = new affintransformation_gui(this);
    affintransformation_gui_ptr->show();
}


void MainWindow::on_PolygonzugAngeschl_clicked()
{
    polygonzug_gui_ptr = new polygonzug_gui(this);
    polygonzug_gui_ptr->show();
}

void MainWindow::on_lang_comboBox_activated(int index)
{
    QSettings einstellung("mh", "Georechner");
    switch (index){
    //case 0: {qDebug()<<"aktive Sprache ist Betriebssystemsprache";
        //einstellung.setValue("sprache", "Systemsprache"); einstellung.setValue("index", 0); break;}

    case 0: {qDebug()<<"aktive Sprache ist deutsch";
        einstellung.setValue("sprache", "deutsch"); einstellung.setValue("index", 0); break;}

    case 1: {qDebug()<<"aktive Sprache ist französisch";
                    einstellung.setValue("sprache", "französisch"); einstellung.setValue("index", 1);break;}

    case 2: {qDebug()<<"aktive Sprache ist englisch";
        einstellung.setValue("sprache", "englisch"); einstellung.setValue("index", 2);break;}
    }
}

