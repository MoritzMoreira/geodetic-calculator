#ifndef POLYGONZUG_GUI_H
#define POLYGONZUG_GUI_H

#include <QDialog>

namespace Ui {
class polygonzug_gui;
}

class polygonzug_gui : public QDialog
{
    Q_OBJECT

public:
    explicit polygonzug_gui(QWidget *parent = nullptr);
    ~polygonzug_gui();

private slots:
    void on_pushButton_datei_p_clicked();

    void on_pushButton_datei_rs_clicked();

    void on_pushButton_berechne_clicked();

    void on_pushButton_test_clicked();

    void on_pushButton_speichern_clicked();

private:
    Ui::polygonzug_gui *ui;
};

#endif // POLYGONZUG_GUI_H
