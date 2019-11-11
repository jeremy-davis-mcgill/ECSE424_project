# Below, we import our libraries
from PyQt5 import QtWidgets, QtCore, uic, QtGui
from PyQt5.QtCore import QThread, QThreadPool, QFileInfo, QPoint
#from PyQt5.QtWidgets import QDesktopWidget, QFileDialog
from win32gui import GetWindowText, GetForegroundWindow
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from time import sleep
import getpass
import win32gui
import win32process
import math
import time

# Sys is imported so we can use the sleep() command
import sys

# psutil allows us to get a list of all running processes in 1 line of code
import psutil

# Below, we load the .ui files
Ui_MainWindow, QtBaseClass = uic.loadUiType("newMainwindow.ui")
Ui_SmallIconWindow, QtBaseClass = uic.loadUiType("iconWindow.ui")
LandingPageUI, LandingPageBase = uic.loadUiType("popupwindow.ui")
LandingPageUI1, LandingPageBase1 = uic.loadUiType("bigpopupwindow.ui")

# Below, is a global list that can be used to store a snapshot of all process ids running at a given momemnt.
process_dict = {}
processNum = 0
currentProcessName = ""

# Global Lock Status Variable
lockActive = False
threadProcessRunning = False
isNotifyType1 = True
NotificatonTriggered = False

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
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint|QtCore.Qt.FramelessWindowHint)
		self.setupUi(self)
		self.checkButtonIcon()
		self.OpenButton.clicked.connect(lambda: self.openWindow())
		self.mainWindow = MyApp(self)
		self.oldPos = self.pos()

	def openWindow(self):
		self.mainWindow.show()
		self.close()

	def setWindowSizeAndPosition(self):
		ag = QDesktopWidget().availableGeometry()
		sg = QDesktopWidget().screenGeometry()
		self.setFixedSize(50, 50)
		widget = self.geometry()
		x = ag.width()-widget.width()
		y = ag.height()/2
		self.move(x-200, y)	

	def checkButtonIcon(self):
		global lockActive
		btn = self.OpenButton
		icon = QtGui.QIcon()
		if lockActive:
			icon.addPixmap(QtGui.QPixmap("lock.png"))
		else:
			icon.addPixmap(QtGui.QPixmap("unlock.png"))
		btn.setIcon(icon)
		btn.setIconSize(QtCore.QSize(50,50))

	def mousePressEvent(self, event):
		self.oldPos = event.globalPos()

	def mouseMoveEvent(self, event):
		delta = QPoint (event.globalPos() - self.oldPos)
		self.move(self.x() + delta.x(), self.y() + delta.y())
		self.oldPos = event.globalPos()


# Class MyApp
# The class below is responsible for running the main window.
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    
    # Below, we initialize the thread that continuously monitors the computer's processes
	signal_start_background_job = QtCore.pyqtSignal()

	# Below, we initialize the MyApp class
	def __init__(self, icon):
		QtWidgets.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.iconWindow = icon
		self.setWindowSizeAndPosition()
		self.setupUi(self)
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint|QtCore.Qt.FramelessWindowHint)

		# Here, we setup threading 
		self.worker = WorkerObject(self)
		self.thread = QtCore.QThread()
		self.worker.moveToThread(self.thread)
		# Here we tell the thread to execute the background_job function of class WorkerObject
		self.signal_start_background_job.connect(self.worker.background_job)

		# Here, we link the buttons of the main page to the functions below
		self.back_page_Button.clicked.connect(lambda: self.back_button_clicked())
		self.exitButton.clicked.connect(lambda: self.exit_button_clicked())
		self.lockToProgram.clicked.connect(lambda:self.lock_button_clicked(False))
		self.SetNotification.clicked.connect(lambda:self.setNotification_button_clicked())
		self.setAndLock.clicked.connect(lambda: self.lock_button_clicked(True))
		self.unlockButton.clicked.connect(lambda:self.unlock_button_clicked())
		self.return_2.clicked.connect(lambda:self.return_button_clicked())
		self.AddMoreButton.clicked.connect(lambda:self.AddMoreButton_clicked())
		self.SetNotifyTime.clicked.connect(lambda:self.on_notificationTime_changed())
		self.RemoveButton.clicked.connect(lambda:self.RemoveButton_clicked())
		self.NoNotifyButton.clicked.connect(lambda:self.setNotificationTimeToInfinity())
		self.checkBox1.clicked.connect(lambda:self.checkBoxClicked(1))
		self.checkBox2.clicked.connect(lambda:self.checkBoxClicked(2))
		self.minInput.setText("0")

		global lockActive
		if not lockActive:
			self.LockedPage.hide()
		self.SettingPage.hide()

		# Start thread
		global threadProcessRunning
		if not threadProcessRunning:
			self.thread.start()
			self.signal_start_background_job.emit()
			threadProcessRunning = True;

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
		global isNotifyType1
		if isNotifyType1:
			self.child_win = PopupWindowBig(self)
			self.child_win.show()
		else:
			self.child_win = PopupWindow(self)
			self.child_win.show()

	def lock_button_clicked(self, setted):
		global lockActive
		global currentProcessName
		global process_dict
		lockActive = True
		if not currentProcessName == "":
			if(setted):
				process_dict[format(currentProcessName)] = self.minInput.text()
			else:
				process_dict[format(currentProcessName)] = math.inf
			self.SettingPage.hide()
			self.showLockedPage()
		else:
			self.ProgramName.setStyleSheet('QLabel { color: red }')

	def unlock_button_clicked(self):
		global lockActive
		lockActive = False
		self.LockedPage.hide()

	def setNotification_button_clicked(self):
		if currentProcessName == "":
			self.ProgramName.setStyleSheet('QLabel { color: red }')
		else:
			self.SettingPage.show()

	def exit_button_clicked(self):
		self.iconWindow.checkButtonIcon()
		self.iconWindow.show()
		self.hide()

	def return_button_clicked(self):
		self.SettingPage.hide()

	def AddMoreButton_clicked(self):
		global filename
		global process_dict
		fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '/home')
		filename = QFileInfo(fname).fileName()
		if not filename == "":
			index = self.ListPrograms.currentRow()
		#filename[index] = ("%s" % (filename))
			process_dict[filename] = "0"
			self.renewItemList()

	def RemoveButton_clicked(self):
		for item in self.ListPrograms.selectedItems():
			currentText = item.text()
			currentFileName = [currentFileName.strip() for currentFileName in currentText.split()]
			del process_dict[format(currentFileName[0])]
		self.renewItemList()



	def setNotificationTimeToInfinity(self):
		global process_dict
		for item in self.ListPrograms.selectedItems():
			currentText = item.text()
			currentFileName = [currentFileName.strip() for currentFileName in currentText.split()]
			process_dict[format(currentFileName[0])] = math.inf
		self.renewItemList()

	def on_notificationTime_changed(self):
		for item in self.ListPrograms.selectedItems():
			currentText = item.text()
			currentFileName = [currentFileName.strip() for currentFileName in currentText.split()]
			process_dict[format(currentFileName[0])] = self.notificationTime.text()
			self.renewItemList()

	def setForegroundProgramName(self, theProcessName):
		self.ProgramName.setText(theProcessName)
		self.ProgramName.setStyleSheet('QLabel { color: black }')

	def checkBoxClicked(self, checkBoxNum):
		global isNotifyType1
		if checkBoxNum == 1:
			isNotifyType1 = True
			self.checkBox2.setChecked(False)
			self.checkBox1.setChecked(True)
		else:
			isNotifyType1 = False
			self.checkBox1.setChecked(False)
			self.checkBox2.setChecked(True)

	def showLockedPage(self):
		self.renewItemList()
		self.LockedPage.show()


	def renewItemList(self):
		self.ListPrograms.clear()
		for process in process_dict.keys():
			if process_dict[process] == math.inf:
				self.ListPrograms.addItem(process + "    no Notification")
			else:
				self.ListPrograms.addItem(process + "    " + process_dict[process] + " min")

# The class below is responsible for the popup window 
class PopupWindow(LandingPageBase, LandingPageUI):                       
    def __init__(self, parent=None):
    	print("1")
    	global currentProcessName
    	print("2")
    	global process_dict
    	print("3")
    	super().__init__()
    	print("4")
    	#LandingPageBase.__init__(self, parent)
    	self.setupUi(self)
    	print("5")
    	self.message.setText("You have been using " + currentProcessName + 
        	" for " + str(process_dict[currentProcessName]) + " min")    
    	self.okButton.clicked.connect(lambda: self.close_popup())
    	print("6")
    	ag = QDesktopWidget().availableGeometry()
    	widget = self.geometry()
    	x = ag.width()-widget.width()
    	self.move(x, 0)

    def close_popup(self):
    	self.close()

class PopupWindowBig(LandingPageBase1, LandingPageUI1):                       
    def __init__(self, parent=None):
    	global currentProcessName
    	global process_dict
    	super().__init__()
    	LandingPageBase.__init__(self)
    	self.setupUi(self)
    	self.message.setText("You have been using " + currentProcessName + 
        	" for " + str(process_dict[currentProcessName]) + " min")    
    	self.okButton.clicked.connect(lambda: self.close_popup())
    	ag = QDesktopWidget().availableGeometry()
    	widget = self.geometry()
    	x = ag.width()-widget.width()
    	self.setFixedSize(ag.width(),  ag.height())
    	self.message.setFixedSize(ag.width()-100, ag.height()-100)
    	self.move(0-20,0-20)
    	self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint|QtCore.Qt.FramelessWindowHint)
    	bWidget = self.okButton.geometry()
    	self.okButton.move(ag.width()/2-bWidget.width()/2,ag.height()-ag.height()/4)


    def close_popup(self):
    	#global NotificatonTriggered
    	#NotificatonTriggered = False
    	self.close()


# The class below is the process monitoring thread.
class WorkerObject(QtCore.QObject):
	@QtCore.pyqtSlot()
	def __init__(self, mainWindow):
		QtCore.QThread.__init__(self)
		self.window = mainWindow
		
		# Here, we initialize our stopwatch info
		self.startTime = 0
		self.notificationTime = 0
		self.currentTime = 0
		self.timerRunning = False

	# Below, we have an infinite while loop so that the thread never terminates
	def background_job(self):
		global processNum
		global currentProcessName
		self.window.setForegroundProgramName("Please click on the program")

		while 1 < 2:
		# Alway be running
			foregroundWindow = GetForegroundWindow()
			tid,pid = win32process.GetWindowThreadProcessId(foregroundWindow)
			print(pid)
			try:
				theProcessName = psutil.Process(pid).name()
				print(theProcessName)
				if(theProcessName != "LockIt.exe" and theProcessName!="python.exe"):				
					if theProcessName != (currentProcessName):
						currentProcessName = theProcessName
						self.window.setForegroundProgramName(theProcessName)
			except:
				print("error catched")
				pass
			# Inside this while loop, we can scan all the processes using psutil
			if lockActive == False:
				#todo
				pass
			if lockActive == True:
				# Get all blacklisted PIDs
				processIDs = []
				for proc in process_dict.keys():
					try:
					# Get process name & pid from process object.
						processIDs.append(proc)
					except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
						pass
        		# Check if the current foreground process is blacklisted, and has a notification time set
				if currentProcessName in processIDs and process_dict[format(currentProcessName)] != math.inf:
					# If the user is using a blacklisted app, start a stopwatch
					if self.timerRunning == False:
						print("Starting Timer")
						startTime = time.time()
						self.timerRunning = True
					else:
						currentTime = time.time()
						elapedTime = currentTime-startTime
						print("elapsed time: %d"%(elapedTime))

						if elapedTime >= int(process_dict[format(currentProcessName)])*60:
						#if elapedTime >= 5:
							# If the elapsed time becomes greater than the notification time, trigger a popup
								self.timerRunning = False
								self.trigger_popup()

				else:
					print("Stopwatch paused")


				pass
			sleep(1)
		pass
	def trigger_popup(self):
		print("triggering popup")	
		global isNotifyType1
		if isNotifyType1:
			dialog = PopupWindowBig(self)
			dialog.__init__()
			dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
			dialog.exec_()
		else:
			dialog = PopupWindow(self)
			dialog.__init__()
			dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
			dialog.exec_()

if __name__ == "__main__":
	app=QtWidgets.QApplication.instance()
	if not app: 
         app = QtWidgets.QApplication(sys.argv)
	window = Icon()
	window.show()

	sys.exit(app.exec_())