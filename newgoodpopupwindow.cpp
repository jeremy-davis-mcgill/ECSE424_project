#include "newgoodpopupwindow.h"

// here is ALL the code in MyWidget constructor
newGoodPopupWindow::newGoodPopupWindow(QWidget *parent, Qt::Window)
    : QWidget(parent)
{
    QHBoxLayout *layout = new QHBoxLayout( this );
           layout->setMargin( 0 );

           //QPushButton *rewind = new QPushButton( QPixmap( rewind_xpm ), 0, this, "vcr_rewind" );
           //layout->addWidget( rewind );
}
