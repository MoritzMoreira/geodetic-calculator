#include "winkel_gui.h"
#include "ui_winkel_gui.h"
#include "mainwindow.h"

Winkel_gui::Winkel_gui(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::Winkel_gui)
{
    ui->setupUi(this);
}

Winkel_gui::~Winkel_gui()
{
    delete ui;
}

void Winkel_gui::on_umrechnen_rad_clicked()
{
    QString umr_rad = ui->lineEdit_rad->text();
    float rad = umr_rad.toFloat();
    Winkel Winkeleingabe_rad(rad, "rad");

    QString ergebnis_gon_f = QString::number(Winkeleingabe_rad.hole_gon());
    ui->lineEdit_gon->setText(ergebnis_gon_f);

    QString ergebnis_grad_f = QString::number(Winkeleingabe_rad.hole_deg());
    ui->lineEdit_grad->setText(ergebnis_grad_f);
}


void Winkel_gui::on_umrechnen_gon_clicked()
{
    QString umr_gon = ui->lineEdit_gon->text();
    float gon = umr_gon.toFloat();
    Winkel Winkeleingabe_gon(gon, "gon");

    QString ergebnis_rad_f = QString::number(Winkeleingabe_gon.hole_rad());
    ui->lineEdit_rad->setText(ergebnis_rad_f);

    QString ergebnis_grad_f = QString::number(Winkeleingabe_gon.hole_deg());
    ui->lineEdit_grad->setText(ergebnis_grad_f);
}


void Winkel_gui::on_umrechnen_grad_clicked()
{
    QString umr_grad = ui->lineEdit_grad->text();
    float grad = umr_grad.toFloat();
    Winkel Winkeleingabe_grad(grad, "grad");

    QString ergebnis_rad_f = QString::number(Winkeleingabe_grad.hole_rad());
    ui->lineEdit_rad->setText(ergebnis_rad_f);

    QString ergebnis_gon_f = QString::number(Winkeleingabe_grad.hole_gon());
    ui->lineEdit_gon->setText(ergebnis_gon_f);
}



