#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QSerialPort>
#include <QMutex>
#include <QTimer>
#include <QElapsedTimer>
#include <QQueue>
#include <QListWidget>


namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);

    ~MainWindow();

private slots:
    //void handleReadyRead();



    void on_m1Home_clicked();

    void on_settingsButton_clicked();

    void on_back_page_Button_clicked();

    void on_horizontalSlider_valueChanged(int value);

private:
    Ui::MainWindow *m_ui;

};

#endif // MAINWINDOW_H
