#ifndef ZWEITEGRUND_GUI_H
#define ZWEITEGRUND_GUI_H

#include <QDialog>

namespace Ui {
class zweitegrund_gui;
}

class zweitegrund_gui : public QDialog
{
    Q_OBJECT

public:
    explicit zweitegrund_gui(QWidget *parent = nullptr);
    ~zweitegrund_gui();

private slots:
    void on_Testwerte_clicked();

    void on_umrechnen_clicked();

private:
    Ui::zweitegrund_gui *ui;
};

#endif // ZWEITEGRUND_GUI_H
