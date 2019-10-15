# Below, we import our libraries
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtCore import QThread, QThreadPool
from PyQt5.QtWidgets import QDesktopWidget
from time import sleep
import getpass

# Sys is imported so we can use the sleep() command
import sys

# psutil allows us to get a list of all running processes in 1 line of code
import psutil

# Below, we load the .ui files
Ui_MainWindow, QtBaseClass = uic.loadUiType("newMainwindow.ui")
Ui_SmallIconWindow, QtBaseClass = uic.loadUiType("iconWindow.ui")
LandingPageUI, LandingPageBase = uic.loadUiType("popupwindow.ui")

# Below, is a global list that can be used to store a snapshot of all process ids running at a given momemnt.
running_processes = []
processNum = 0

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

class Icon(QtWidgets.QMainWindow, Ui_SmallIconWindow):
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		Ui_SmallIconWindow.__init__(self)
		self.setWindowSizeAndPosition()
		self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
		self.setupUi(self)

		self.OpenButton.clicked.connect(lambda: self.openWindow())

	def openWindow(self):
		window = MyApp()
		window.show()
		self.close()

	def setWindowSizeAndPosition(self):
		ag = QDesktopWidget().availableGeometry()
		sg = QDesktopWidget().screenGeometry()
		self.setFixedSize(50, 50)
		widget = self.geometry()
		x = ag.width()-widget.width()
		y = ag.height()/2
		self.move(x-200, y)	

# Class MyApp
# The class below is responsible for running the main window.
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    
    # Below, we initialize the thread that continuously monitors the computer's processes
	signal_start_background_job = QtCore.pyqtSignal()



	# Below, we initialize the MyApp class
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setWindowSizeAndPosition()
		self.setupUi(self)
		self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)

		# Here, we setup threading 
		self.worker = WorkerObject()
		self.thread = QtCore.QThread()
		self.worker.moveToThread(self.thread)


		# Here we tell the thread to execute the background_job function of class WorkerObject
		self.signal_start_background_job.connect(self.worker.background_job)

		# Here, we link the buttons of the main page to the functions below
		self.back_page_Button.clicked.connect(lambda: self.back_button_clicked())
		self.ProgramName.setText("Adobe Reader")
		self.exitButton.clicked.connect(lambda: self.exit_button_clicked())
		self.lockToProgram.clicked.connect(lambda:self.lock_button_clicked())
		self.unlockButton.clicked.connect(lambda:self.unlock_button_clicked())
		global lockActive
		if not lockActive:
			self.LockedPage.hide()

		# Start thread
		self.thread.start()
		self.signal_start_background_job.emit()

	def setWindowSizeAndPosition(self):
		ag = QDesktopWidget().availableGeometry()
		sg = QDesktopWidget().screenGeometry()
		self.setFixedSize(300, sg.height())
		widget = self.geometry()
		x = ag.width()-widget.width()
		self.move(x, 0)

	# Below are the functions that get executed when a button is clicked	
	def settings_button_clicked(self):
		self.stackedWidget.setCurrentIndex(1)

	def back_button_clicked(self):
		self.stackedWidget.setCurrentIndex(0)

	def popup_test_button_clicked(self):
		self.child_win = PopupWindow(self)
		self.child_win.show()

	def lock_button_clicked(self):
		#To-Do
		global lockActive
		lockActive = True
		self.LockedPage.show()

	def unlock_button_clicked(self):
		global lockActive
		lockActive = False
		self.LockedPage.hide()

	def exit_button_clicked(self):
		window = Icon()
		window.show()
		self.hide()



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
		global processNum
		while 1 < 2:

			# Inside this while loop, we can scan all the processes using psutil
			if lockActive == False:
				print("Lock Inactive")
			if lockActive == True:
				print("Lock Active")
				print("Scanning Processes")
				for proc in psutil.process_iter(attrs = ['username']):
					#print(proc.info['username'])
					#print(getpass.getuser())
					#if proc.pid not in running_processes:
					if proc.info['username'] == "DESKTOP-D7UQ8QR\Jimmy":
							#if  ignore_process(self, proc) == False:
							#print("New process Found: ")
							print(proc.name())
							running_processes.append(proc.pid)
							processNum = processNum+1
			sleep(1)
		pass

if __name__ == "__main__":
	app=QtWidgets.QApplication.instance()
	if not app: 
         app = QtWidgets.QApplication(sys.argv)
	window = Icon()
	window.show()

	sys.exit(app.exec_())