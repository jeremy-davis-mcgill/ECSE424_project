# Below, we import our libraries
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtCore import QThread, QThreadPool
from time import sleep

# Sys is imported so we can use the sleep() command
import sys

# psutil allows us to get a list of all running processes in 1 line of code
import psutil

# Below, we load the .ui files
Ui_MainWindow, QtBaseClass = uic.loadUiType("mainwindow.ui")
LandingPageUI, LandingPageBase = uic.loadUiType("popupwindow.ui")

# Below, is a global list that can be used to store a snapshot of all process ids running at a given momemnt.
running_processes = []

# Global Lock Status Variable
lockActive = False

# Below is a helper function for ther class WorkerObject
def ignore_process(self, proc):
	if proc.name() == "backgroundTaskHost.exe":
		return True
	if proc.name() == "dllhost.exe":
		return True
	if proc.name() == "svchost.exe":
		return True
	if proc.name() == "WmiPrvSE.exe":
		return True
	return False

# Class MyApp
# The class below is responsible for running the main window.
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    
    # Below, we initialize the thread that continuously monitors the computer's processes
	signal_start_background_job = QtCore.pyqtSignal()



	# Below, we initialize the MyApp class
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)

		# Here, we setup threading 
		self.worker = WorkerObject()
		self.thread = QtCore.QThread()
		self.worker.moveToThread(self.thread)

		# Here we tell the thread to execute the background_job function of class WorkerObject
		self.signal_start_background_job.connect(self.worker.background_job)

		# Here, we link the buttons of the main page to the functions below
		self.settingsButton.clicked.connect(lambda: self.settings_button_clicked())
		self.back_page_Button.clicked.connect(lambda: self.back_button_clicked())
		self.m1Home.clicked.connect(lambda: self.popup_test_button_clicked())
		self.actionSettings.triggered.connect(lambda: self.settings_button_clicked())
		self.lockButton.clicked.connect(lambda: self.lock_button_clicked())

		# Start thread
		self.thread.start()
		self.signal_start_background_job.emit()

	# Below are the functions that get executed when a button is clicked	
	def settings_button_clicked(self):
		self.stackedWidget.setCurrentIndex(1)

	def back_button_clicked(self):
		self.stackedWidget.setCurrentIndex(0)

	def popup_test_button_clicked(self):
		self.child_win = PopupWindow(self)
		self.child_win.show()

	def lock_button_clicked(self):
		global lockActive

		if lockActive == True:
			lockActive = False

			self.lockStatus.setText("Lock Inactive")
			return
		if lockActive == False:
			lockActive = True
			global running_processes
			running_processes.clear()
			for proc in psutil.process_iter():
				running_processes.append(proc.pid);
				print(proc)
			self.lockStatus.setText("Lock Active")
			return

# The class below is responsible for the popup window 
class PopupWindow(LandingPageBase, LandingPageUI):                       
    def __init__(self, parent=None):
        super().__init__()
        LandingPageBase.__init__(self, parent)
        self.setupUi(self)    
        self.okButton.clicked.connect(lambda: self.close_popup())

    def close_popup(self):
    	self.close()


# The class below is the process monitoring thread.
class WorkerObject(QtCore.QObject):
	@QtCore.pyqtSlot()

		# Below, we have an infinite while loop so that the thread never terminates
	def background_job(self):

		while 1 < 2:

			# Inside this while loop, we can scan all the processes using psutil
			if lockActive == False:
				print("Lock Inactive")
			if lockActive == True:
				print("Lock Active")
				print("Scanning Processes")
				for proc in psutil.process_iter():
					if proc.pid not in running_processes:
						if  ignore_process(self, proc) == False:
							print("New process Found: ")
							print(proc.name())
			sleep(1)
		pass

if __name__ == "__main__":
	app=QtWidgets.QApplication.instance()
	if not app: 
         app = QtWidgets.QApplication(sys.argv)
	window = MyApp()
	window.show()

	sys.exit(app.exec_())