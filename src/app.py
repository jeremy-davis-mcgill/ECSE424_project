from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtCore import QThread, QThreadPool
from time import sleep
import sys
import psutil

Ui_MainWindow, QtBaseClass = uic.loadUiType("mainwindow.ui")
LandingPageUI, LandingPageBase = uic.loadUiType("popupwindow.ui")



class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    
    # Below, we initialize the process thread
	signal_start_background_job = QtCore.pyqtSignal()

	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)

		self.worker = WorkerObject()
		self.thread = QtCore.QThread()
		self.worker.moveToThread(self.thread)

		self.signal_start_background_job.connect(self.worker.background_job)

		self.settingsButton.clicked.connect(lambda: self.settings_button_clicked())
		self.back_page_Button.clicked.connect(lambda: self.back_button_clicked())
		self.m1Home.clicked.connect(lambda: self.popup_test_button_clicked())
		self.actionSettings.triggered.connect(lambda: self.settings_button_clicked())

		# Start thread
		self.thread.start()
		self.signal_start_background_job.emit()

	def settings_button_clicked(self):
		self.stackedWidget.setCurrentIndex(1)

	def back_button_clicked(self):
		self.stackedWidget.setCurrentIndex(0)

	def popup_test_button_clicked(self):
		self.child_win = PopupWindow(self)
		self.child_win.show()

def Start():
	window = MyApp()
	window.show()
	return window

class PopupWindow(LandingPageBase, LandingPageUI):                       
    def __init__(self, parent=None):
        super().__init__()
        LandingPageBase.__init__(self, parent)
        self.setupUi(self)    

class WorkerObject(QtCore.QObject):
	@QtCore.pyqtSlot()

	def background_job(self):


		while 1 < 2:
			print("Scanning Processes")
			PROCNAME = "OculusClient.exe"

			for proc in psutil.process_iter():
				if proc.name() == PROCNAME:
					print("Oculus Found")
			sleep(1)
		pass

if __name__ == "__main__":
	app=QtWidgets.QApplication.instance()
	if not app: 
         app = QtWidgets.QApplication(sys.argv)


	window = Start()
	PROCNAME = "python.exe"

	for proc in psutil.process_iter():
		print(proc)

	sys.exit(app.exec_())