#ifndef ERSTEGRUND_GUI_H
#define ERSTEGRUND_GUI_H

#include <QDialog>

namespace Ui {
class ersteGrund_gui;
}

class ersteGrund_gui : public QDialog
{
    Q_OBJECT

public:
    explicit ersteGrund_gui(QWidget *parent = nullptr);
    ~ersteGrund_gui();

private slots:
    void on_Testwerte_clicked();
    void on_umrechnen_clicked();

private:
    Ui::ersteGrund_gui *ui;
};

#endif // ERSTEGRUND_GUI_H
