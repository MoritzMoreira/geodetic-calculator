#ifndef BOGENSCHNITT_GUI_H
#define BOGENSCHNITT_GUI_H

#include <QDialog>

namespace Ui {
class Bogenschnitt_gui;
}

class Bogenschnitt_gui : public QDialog
{
    Q_OBJECT

public:
    explicit Bogenschnitt_gui(QWidget *parent = nullptr);
    ~Bogenschnitt_gui();

private slots:
    void on_umrechnen_clicked();
    void on_test_1np_clicked();
    void on_test_2np_clicked();
    void on_test_keineLoesung_clicked();

private:
    Ui::Bogenschnitt_gui *ui;
};

#endif // BOGENSCHNITT_GUI_H
