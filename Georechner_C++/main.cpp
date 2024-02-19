#include "mainwindow.h"
#include <QApplication>
#include <QTranslator>
#include <QInputDialog>
#include <QSettings>
#include <QDebug>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

    a.QApplication::setWindowIcon(QIcon(":/new/prefix1/Geocalc.png"));

    QTranslator transl_inst;
    QSettings einstellung("mh", "Georechner");
    QString nutzerSprache = einstellung.value("sprache", "").toString();
    QString nutzerIndex = einstellung.value("index", "").toString();
    QString systemLang = QLocale::system().name();
    qDebug() << "Systemsprache ist: " <<systemLang;

    if (nutzerSprache == "");{
        std::cout<<"ist systemsprace"<<std::endl;
        if (systemLang == "en_US"){
            transl_inst.load(":/new/prefix1/lang_en.qm");
            a.installTranslator(&transl_inst);
            nutzerIndex = "2";
        }
        if (systemLang == "fr_FR"){
            transl_inst.load(":/new/prefix1/lang_fr.qm");
            a.installTranslator(&transl_inst); nutzerIndex = "1";
        }
        if (systemLang == "de_DE"){
            transl_inst.load(":/new/prefix1/lang_de.qm"); nutzerIndex = "0";
            a.installTranslator(&transl_inst);
        }
    }
    if (nutzerSprache == "deutsch"){std::cout<<"ist deutsch"<<std::endl;
        transl_inst.load(":/new/prefix1/lang_de.qm"); nutzerIndex = "0";}
    if (nutzerSprache == "englisch"){
        transl_inst.load(":/new/prefix1/lang_en.qm"); nutzerIndex = "2";
    }
    if (nutzerSprache == "französisch"){
        transl_inst.load(":/new/prefix1/lang_fr.qm"); nutzerIndex = "1";
    }
    a.installTranslator(&transl_inst);

    MainWindow w;
    w.ui->lang_comboBox->setCurrentIndex(nutzerIndex.toInt());
    w.show();
    return a.exec();
}
