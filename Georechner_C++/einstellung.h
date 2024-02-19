#ifndef EINSTELLUNG_H
#define EINSTELLUNG_H

#include <QDialog>

namespace Ui {
class Einstellung;
}

class Einstellung : public QDialog
{
    Q_OBJECT

public:
    explicit Einstellung(QWidget *parent = nullptr);
    ~Einstellung();

private:
    Ui::Einstellung *ui;
};

#endif // EINSTELLUNG_H
