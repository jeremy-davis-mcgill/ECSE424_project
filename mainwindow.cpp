#include "mainwindow.h"
#include <unistd.h>
#include "ui_mainwindow.h"
#include "treatplan.h"
#include <QSerialPort>
#include <QSerialPortInfo>
#include <QDebug>
#include <QIntValidator>
#include <QElapsedTimer>
#include <QStringList>
#include <QFileDialog>
#include <QMessageBox>
#include <QFuture>
#include <qtconcurrentrun.h>
#include <QThread>
#include <QWidget>
#include "popupwindow.h"


int current_page = 0;
// page 0 = main page
// page 1 = settings page
void init_listWidget(Ui::MainWindow* m_ui);

MainWindow::~MainWindow()
{
    delete m_ui;
}

MainWindow::MainWindow(QWidget *parent) :

    // Initialize program flags
    QMainWindow           (parent),
    m_ui                  (new Ui::MainWindow)

{
    m_ui->setupUi(this);
    init_listWidget(m_ui);

}

void init_listWidget(Ui::MainWindow* m_ui){
    // Below, we set the text color to black
    m_ui->listWidget->addItem("Notification Type 1");
    m_ui->listWidget->addItem("Notification Type 2");
    m_ui->listWidget->addItem("Notification Type 3");
    m_ui->listWidget->addItem("Notification Type 4");
    m_ui->listWidget->item(0)->setForeground(Qt::black);
    m_ui->listWidget->item(1)->setForeground(Qt::black);
    m_ui->listWidget->item(2)->setForeground(Qt::black);
    m_ui->listWidget->item(3)->setForeground(Qt::black);
}

void MainWindow::on_m1Home_clicked()
{
   popupWindow popup;
   popup.setModal(true);
   popup.move(0, 0);
   popup.setWindowTitle("Notification");
   popup.exec();
}



void MainWindow::on_settingsButton_clicked()
{
    current_page = 1;
    m_ui->stackedWidget->setCurrentIndex(current_page);
}

void MainWindow::on_back_page_Button_clicked()
{
    current_page = 0;
    m_ui->stackedWidget->setCurrentIndex(current_page);
}

void MainWindow::on_horizontalSlider_valueChanged(int value)
{

}
