#ifndef RUECKWAERTSSCHNITT_GUI_H
#define RUECKWAERTSSCHNITT_GUI_H

#include <QDialog>

namespace Ui {
class rueckwaertsschnitt_gui;
}

class rueckwaertsschnitt_gui : public QDialog
{
    Q_OBJECT

public:
    explicit rueckwaertsschnitt_gui(QWidget *parent = nullptr);
    ~rueckwaertsschnitt_gui();

private slots:
    void on_test_1np_clicked();

    void on_umrechnen_clicked();

private:
    Ui::rueckwaertsschnitt_gui *ui;
};

#endif // RUECKWAERTSSCHNITT_GUI_H
