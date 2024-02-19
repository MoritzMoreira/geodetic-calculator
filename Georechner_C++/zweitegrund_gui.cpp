#include "zweitegrund_gui.h"
#include "ui_zweitegrund_gui.h"
#include "mainwindow.h"
#include <QPixmap>

zweitegrund_gui::zweitegrund_gui(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::zweitegrund_gui)
{
    ui->setupUi(this);
    QPixmap gauss(":/new/prefix1/carl-friedrich-gauss.jpg");
    ui->label_gauss->setPixmap(gauss.scaled(109, 139, Qt::KeepAspectRatio));
}

zweitegrund_gui::~zweitegrund_gui()
{
    delete ui;
}

void zweitegrund_gui::on_Testwerte_clicked()
{
    ui->lineEdit_y1->setText("528.15");
    ui->lineEdit_x1->setText("407.65");
    ui->lineEdit_y2->setText("795.17");
    ui->lineEdit_x2->setText("525.1");
}


void zweitegrund_gui::on_umrechnen_clicked()
{
    QString y1 = ui->lineEdit_y1->text();
    float y1_f = y1.toFloat();
    QString x1 = ui->lineEdit_x1->text();
    float x1_f = x1.toFloat();
    QString y2 = ui->lineEdit_y2->text();
    float y2_f = y2.toFloat();
    QString x2 = ui->lineEdit_x2->text();
    float x2_f = x2.toFloat();

    std::array<float, 2> zweiteGrund = Strecke(Punkt(y1_f, x1_f), Punkt(y2_f, x2_f)).riwi_laenge();
    ui->lineEdit_t12->setText(QString::number(zweiteGrund[1]));
    ui->lineEdit_s12->setText(QString::number(zweiteGrund[0]));
}

