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


}

void MainWindow::on_m1Home_clicked()
{
    QMessageBox::information(
        this,
        tr("Application Name"),
        tr("You've been browsing X application for X minutes!") );
}
