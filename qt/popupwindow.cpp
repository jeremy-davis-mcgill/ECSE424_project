#include "popupwindow.h"
#include "ui_popupwindow.h"

popupWindow::popupWindow(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::popupWindow)
{
    ui->setupUi(this);
}

popupWindow::~popupWindow()
{
    delete ui;
}

void popupWindow::on_okButton_clicked()
{
    close();
}
