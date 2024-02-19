#include "bogenschnitt_gui.h"
#include "ui_bogenschnitt_gui.h"
#include "mainwindow.h"

Bogenschnitt_gui::Bogenschnitt_gui(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::Bogenschnitt_gui)
{
    ui->setupUi(this);
    QPixmap bogen(":/new/prefix1/bogen.png");
    ui->label_bogen->setPixmap(bogen.scaled(387, 290, Qt::KeepAspectRatio));
}

Bogenschnitt_gui::~Bogenschnitt_gui()
{
    delete ui;
}

void Bogenschnitt_gui::on_umrechnen_clicked()
{
    QString y1 = ui->lineEdit_y1->text();
    float y1_f = y1.toFloat();
    QString x1 = ui->lineEdit_x1->text();
    float x1_f = x1.toFloat();

    QString y2 = ui->lineEdit_y2->text();
    float y2_f = y2.toFloat();
    QString x2 = ui->lineEdit_x2->text();
    float x2_f = x2.toFloat();

    QString st1 = ui->lineEdit_s1->text();
    float s1_f = st1.toFloat();
    QString st2 = ui->lineEdit_s2->text();
    float s2_f = st2.toFloat();
    QString st3 = ui->lineEdit_s3->text();
    float s3_f = st3.toFloat();

    // Definition der beiden gegebenen Punkte als Instanzen der Klasse Punkt
    Punkt p1 = Punkt(y1_f, x1_f);
    Punkt p2 = Punkt(y2_f, x2_f);
    // Definition der drei Strecken als Instanzen der Klasse Strecke
    Strecke s1(p1, s1_f);
    Strecke s2(p2, s2_f);
    Strecke s3(p1, s3_f);

    std::cout<<"  | s1 "<<s1_f<<s1_f<<"  | s2 "<<s2_f<<"  | s3 "<<s3_f<<std::endl;
    std::cout<<"  | s1 "<<s1_f<<s1.riwi_laenge()[1]<<"  | s2 "<<s2.riwi_laenge()[1]<<"  | s3 "<<s3.riwi_laenge()[1]<<std::endl;
    std::cout<<s1.hole_p2().str()<<"  p2 von s1 in gui  "<<std::endl;
    //Strecke s4(p1, p2);

    std::cout<<s1_f<<"  |  "<<std::endl;
    Bogenschnitt bg_Berechnung(s1, s2, s3);
    //ergebnis_Bogenschnitt e = bg_Berechnung.berechne();
    std::vector<float> e = bg_Berechnung.berechne();

    if(e[1] == 0.0f && e[2] == 0.0f){
        ui->lineEdit_np1->setText("         keine Lösung"); }
    else{
        QString pn1 = "yn1: " + QString::number(e[0]) + "  xn1: " + QString::number(e[1]);
        ui->lineEdit_np1->setText(pn1);}


    if(e[2] == 0.0f && e[3] == 0.0f){
        ui->lineEdit_np2->setText("         -");}
    else{
        QString pn2 = "yn1: " + QString::number(e[2]) + "  xn1: " + QString::number(e[3]);
        ui->lineEdit_np2->setText(pn2);}

    ui->lineEdit_m->setText(QString::number(e[4]));
}

void Bogenschnitt_gui::on_test_1np_clicked(){
    ui->lineEdit_y1->setText("328.76");
    ui->lineEdit_x1->setText("1207.85");
    ui->lineEdit_y2->setText("925.04");
    ui->lineEdit_x2->setText("954.33");
    ui->lineEdit_s1->setText("141.517");
    ui->lineEdit_s2->setText("506.42");
    ui->lineEdit_s3->setText("0.0");
}


void Bogenschnitt_gui::on_test_2np_clicked(){
    ui->lineEdit_y1->setText("328.76");
    ui->lineEdit_x1->setText("1207.85");
    ui->lineEdit_y2->setText("925.04");
    ui->lineEdit_x2->setText("954.33");
    ui->lineEdit_s1->setText("294.33");
    ui->lineEdit_s2->setText("506.42");
    ui->lineEdit_s3->setText("648.08");
}


void Bogenschnitt_gui::on_test_keineLoesung_clicked(){
    ui->lineEdit_y1->setText("328.76");
    ui->lineEdit_x1->setText("1207.85");
    ui->lineEdit_y2->setText("925.04");
    ui->lineEdit_x2->setText("954.33");
    ui->lineEdit_s1->setText("141.5169018662233");
    ui->lineEdit_s2->setText("200");
    ui->lineEdit_s3->setText("648.08");
}

