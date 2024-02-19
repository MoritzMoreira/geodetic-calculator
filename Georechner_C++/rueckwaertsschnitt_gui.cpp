#include "rueckwaertsschnitt_gui.h"
#include "ui_rueckwaertsschnitt_gui.h"
#include <mainwindow.h>
#include <QPixmap>

rueckwaertsschnitt_gui::rueckwaertsschnitt_gui(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::rueckwaertsschnitt_gui)
{
    ui->setupUi(this);
    QPixmap rueckwaertsschn(":/new/prefix1/rueckwaertsschnitt.png");
    ui->label_rueckwaertsschnitt->setPixmap(rueckwaertsschn.scaled(357, 214, Qt::KeepAspectRatio));
    QPixmap VermTurm(":/new/prefix1/turm.png");
    ui->label_turm->setPixmap(VermTurm.scaled(153, 325, Qt::KeepAspectRatio));
}

rueckwaertsschnitt_gui::~rueckwaertsschnitt_gui()
{
    delete ui;
}

void rueckwaertsschnitt_gui::on_test_1np_clicked()
{
    ui->lineEdit_y1->setText("49666.56");
    ui->lineEdit_x1->setText("4448.58");
    ui->lineEdit_y2->setText("46867.94");
    ui->lineEdit_x2->setText("5537.0");
    ui->lineEdit_y3->setText("51293.86");
    ui->lineEdit_x3->setText("6365.89");

    ui->lineEdit_r1->setText("66.8117");
    ui->lineEdit_r2->setText("294.7845");
    ui->lineEdit_r3->setText("362.8516");
}


void rueckwaertsschnitt_gui::on_umrechnen_clicked()
{
    QString y1 = ui->lineEdit_y1->text();
    float y1_f = y1.toFloat();
    QString x1 = ui->lineEdit_x1->text();
    float x1_f = x1.toFloat();

    QString y2 = ui->lineEdit_y2->text();
    float y2_f = y2.toFloat();
    QString x2 = ui->lineEdit_x2->text();
    float x2_f = x2.toFloat();

    QString y3 = ui->lineEdit_y3->text();
    float y3_f = y3.toFloat();
    QString x3 = ui->lineEdit_x3->text();
    float x3_f = x3.toFloat();

    QString r1 = ui->lineEdit_r1->text();
    float r1_f = r1.toFloat();
    QString r2 = ui->lineEdit_r2->text();
    float r2_f = r2.toFloat();
    QString r3 = ui->lineEdit_r3->text();
    float r3_f = r3.toFloat();

    // Definition der beiden gegebenen Punkte als Instanzen der Klasse Punkt
    Punkt p1 = Punkt(y1_f, x1_f);
    Punkt p2 = Punkt(y2_f, x2_f);
    Punkt p3 = Punkt(y3_f, x3_f);

    Rueckwaertsschnitt rueckSchn_Instanz(p1, p2, p3, r1_f, r2_f, r3_f);
    std::vector<float> r_e = rueckSchn_Instanz.berechne();
    ui->lineEdit_yn->setText(QString::number(r_e[0]));
    ui->lineEdit_xn->setText(QString::number(r_e[1]));
}

