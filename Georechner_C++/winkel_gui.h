#ifndef WINKEL_GUI_H
#define WINKEL_GUI_H

#include <QDialog>

namespace Ui {
class Winkel_gui;
}

class Winkel_gui : public QDialog
{
    Q_OBJECT

public:
    explicit Winkel_gui(QWidget *parent = nullptr);
    ~Winkel_gui();

private slots:
    void on_umrechnen_rad_clicked();
    void on_umrechnen_gon_clicked();
    void on_umrechnen_grad_clicked();


private:
    Ui::Winkel_gui *ui;
};

#endif // WINKEL_GUI_H
