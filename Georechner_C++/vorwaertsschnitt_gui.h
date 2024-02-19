#ifndef VORWAERTSSCHNITT_GUI_H
#define VORWAERTSSCHNITT_GUI_H
#include <QDialog>

namespace Ui {
class vorwaertsschnitt_gui;
}

class vorwaertsschnitt_gui : public QDialog
{
    Q_OBJECT

public:
    explicit vorwaertsschnitt_gui(QWidget *parent = nullptr);
    ~vorwaertsschnitt_gui();

private slots:
    void on_test_1np_clicked();

    void on_umrechnen_clicked();

private:
    Ui::vorwaertsschnitt_gui *ui;
};

#endif // VORWAERTSSCHNITT_GUI_H
