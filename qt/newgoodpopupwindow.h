#ifndef NEWGOODPOPUPWINDOW_H
#define NEWGOODPOPUPWINDOW_H

#include <QWidget>
#include <Qwindow>
#include <QHBoxLayout>

class newGoodPopupWindow : public QWidget
{
    Q_OBJECT
public:
    explicit newGoodPopupWindow (QWidget *parent, Qt::Window);
    // ...
};

#endif // NEWGOODPOPUPWINDOW_H
