#include "einstellung.h"
#include "ui_einstellung.h"

Einstellung::Einstellung(QWidget *parent)
    : QDialog(parent)
    , ui(new Ui::Einstellung)
{
    ui->setupUi(this);
}

Einstellung::~Einstellung()
{
    delete ui;
}
