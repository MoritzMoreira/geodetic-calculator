#ifndef HELMERTTRANSFORMATION_GUI_H
#define HELMERTTRANSFORMATION_GUI_H

#include <QDialog>

namespace Ui {
class Helmerttransformation_gui;
}

class Helmerttransformation_gui : public QDialog
{
    Q_OBJECT

public:
    explicit Helmerttransformation_gui(QWidget *parent = nullptr);
    ~Helmerttransformation_gui();

private slots:
    void on_pushButton_test_clicked();
    void on_pushButton_datei_clicked();
    void on_pushButton_berechne_clicked();

    void on_pushButton_test2_clicked();

    void on_pushButton_speichern_clicked();

private:
    Ui::Helmerttransformation_gui *ui;
};

#endif // HELMERTTRANSFORMATION_GUI_H
