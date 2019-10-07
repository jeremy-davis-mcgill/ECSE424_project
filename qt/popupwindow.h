#ifndef POPUPWINDOW_H
#define POPUPWINDOW_H

#include <QDialog>

namespace Ui {
class popupWindow;
}

class popupWindow : public QDialog
{
    Q_OBJECT

public:
    explicit popupWindow(QWidget *parent = nullptr);
    ~popupWindow();

private slots:
    void on_okButton_clicked();

private:
    Ui::popupWindow *ui;
};

#endif // POPUPWINDOW_H
