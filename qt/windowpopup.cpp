#include "windowpopup.h"
#include "mainwindow.h"
#include "popupwindow.h"
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

windowpopup::~windowpopup()
{
    delete m_ui;
}

windowpopup::windowpopup()
{

}
