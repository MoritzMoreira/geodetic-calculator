#include "erstegrund_gui.h"
#include "ui_erstegrund_gui.h"
#include "mainwindow.h"
#include <iostream>

ersteGrund_gui::ersteGrund_gui(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::ersteGrund_gui)
{
    ui->setupUi(this);
}

ersteGrund_gui::~ersteGrund_gui()
{
    delete ui;
}

void ersteGrund_gui::on_Testwerte_clicked()
{
    ui->lineEdit_y1->setText("16.1");
    ui->lineEdit_x1->setText("23.06");
    ui->lineEdit_s12->setText("17.11");
    ui->lineEdit_t12->setText("214.199");
}

void ersteGrund_gui::on_umrechnen_clicked()
{
    QString y1 = ui->lineEdit_y1->text();
    float y1_f = y1.toFloat();
    QString x1 = ui->lineEdit_x1->text();
    float x1_f = x1.toFloat();
    QString s12 = ui->lineEdit_s12->text();
    float s12_f = s12.toFloat();
    QString t12 = ui->lineEdit_t12->text();
    float t12_f = t12.toFloat();

    float* rechts_hoch = umrechnen_koordinaten(y1_f, x1_f, s12_f, t12_f);
    ui->lineEdit_y2->setText(QString::number(rechts_hoch[0]));
    ui->lineEdit_x2->setText(QString::number(rechts_hoch[1]));
}

