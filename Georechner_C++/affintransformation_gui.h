#ifndef AFFINTRANSFORMATION_GUI_H
#define AFFINTRANSFORMATION_GUI_H

#include <QDialog>

namespace Ui {
class affintransformation_gui;
}

class affintransformation_gui : public QDialog
{
    Q_OBJECT

public:
    explicit affintransformation_gui(QWidget *parent = nullptr);
    ~affintransformation_gui();

private slots:
    void on_pushButton_datei_clicked();

    void on_pushButton_berechne_clicked();

    void on_pushButton_test_clicked();

    void on_pushButton_test2_clicked();

    void on_pushButton_speichern_clicked();

private:
    Ui::affintransformation_gui *ui;
};

#endif // AFFINTRANSFORMATION_GUI_H
