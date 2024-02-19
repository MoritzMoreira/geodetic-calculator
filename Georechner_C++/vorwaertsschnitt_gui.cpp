#include "vorwaertsschnitt_gui.h"
#include "ui_vorwaertsschnitt_gui.h"
#include "mainwindow.h"
#include <QPixmap>

vorwaertsschnitt_gui::vorwaertsschnitt_gui(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::vorwaertsschnitt_gui)
{
    ui->setupUi(this);
    QPixmap vorwaertsschn(":/new/prefix1/Vorwaertsschnitt.png");
    ui->label_vorwaertsschnitt->setPixmap(vorwaertsschn.scaled(149, 178, Qt::KeepAspectRatio));
    QPixmap vorwaertsschn2(":/new/prefix1/Vorwaertsschnitt2.png");
    ui->label_vorwaertsschnitt2->setPixmap(vorwaertsschn2.scaled(362, 150, Qt::KeepAspectRatio));
}

vorwaertsschnitt_gui::~vorwaertsschnitt_gui()
{
    delete ui;
}

void vorwaertsschnitt_gui::on_test_1np_clicked()
{
    ui->lineEdit_y1->setText("24681.92");
    ui->lineEdit_x1->setText("90831.87");
    ui->lineEdit_y2->setText("24877.72");
    ui->lineEdit_x2->setText("89251.09");
    ui->lineEdit_y3->setText("22526.65");
    ui->lineEdit_x3->setText("89150.52");
    ui->lineEdit_y4->setText("23231.58");
    ui->lineEdit_x4->setText("91422.92");

    ui->lineEdit_phi->setText("331.6174");
    ui->lineEdit_psi->setText("60.751");
}


void vorwaertsschnitt_gui::on_umrechnen_clicked()
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

    QString y4 = ui->lineEdit_y4->text();
    float y4_f = y4.toFloat();
    QString x4 = ui->lineEdit_x4->text();
    float x4_f = x4.toFloat();

    QString phi = ui->lineEdit_phi->text();
    float phi_f = phi.toFloat();
    QString psi = ui->lineEdit_psi->text();
    float psi_f = psi.toFloat();

    // Definition der beiden gegebenen Punkte als Instanzen der Klasse Punkt
    Punkt p1 = Punkt(y1_f, x1_f);
    Punkt p2 = Punkt(y2_f, x2_f);
    Punkt p3 = Punkt(y3_f, x3_f);
    Punkt p4 = Punkt(y4_f, x4_f);

    Vorwaertsschnitt vorwSchn_Instanz(p1, p2, p3, p4, phi_f, psi_f);
    std::vector<float> v_e = vorwSchn_Instanz.berechne();
    ui->lineEdit_yn->setText(QString::number(v_e[0]));
    ui->lineEdit_xn->setText(QString::number(v_e[1]));
}

