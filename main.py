## @mainpage 
# This document provides detailed documentation on the API's and functions used in building the Virtual Lab Assistant Project
# for the CSIRO Energy Business Unit. \n\n
# This system is a voice-based command system, which can interpret speech-based commands of the user and perform certain
# laboratory functions and interface with devices in the physical domain. \n\n
# To see detailed information about the software package, browse to the 'software' tab. For details of the implementation of the 
# class objects, see browse the 'class' tab. For an overview and API documentation on all the functions used in the implementation,
# see the 'files' tab

from PyQt5 import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, pyqtSignal
from QLed import QLed
from queue import Queue
from scipy.ndimage import imread
import numpy as np
import time
import queue
import threading
import importlib

## imported bt module
bt = importlib.import_module('bt_setup')
## imported gcp_dialogflow module
gcp_dialogflow = importlib.import_module('gcp_dialogflow')
## imported gcp_stt module
gcp_stt = importlib.import_module('gcp_stt')
## imported lm_control module
lm_control = importlib.import_module('lm_control')
## imported timer module
timer = importlib.import_module('timer')
## imported twd_detect module
twd_detect = importlib.import_module('twd_imitate')
## imported twd_engine module
twd_engine = improtlib.import_module('twd_engine')
## imported lm_status module
lm_status = importlib.import_module('lm_status')
## imported save_file module
save_file = importlib.import_module('save_file')
## imported quit module
quit_listen = importlib.import_module('quit')
## imported speech_engine file
speech_engine = importlib.import_module('speech_engine')

## dictionary to track status of lab machine
lab_machine_status = {
	"Lab Machine One": False,
	"Lab Machine Two": False,
	"Lab Machine Three": False,
	"Lab Machine Four": False
}
## GUI queue used to communicate and update GUi thread
gui_queue = queue.Queue()
## Log of conversation history
conv_hist = []
## Record of transcription history
trans_hist = " "
## Boolean to indicate if system should exit
exit = False

class Ui_MainWindow(object):
	""" Documentation for the Ui_MainWindow class
	Class object for UI Window

	"""
	def setupUi(self, MainWindow):
		""" 
		Function initialises PyQt main window, including all qWidgets and qThreads
		"""
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(735, 716)
		palette = QtGui.QPalette()
		brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
		brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
		brush = QtGui.QBrush(QtGui.QColor(170, 170, 170))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
		brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
		brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
		brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
		brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
		brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
		brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
		brush = QtGui.QBrush(QtGui.QColor(170, 170, 170))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
		brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
		brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
		brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
		brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
		brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
		brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
		brush = QtGui.QBrush(QtGui.QColor(170, 170, 170))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
		brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
		brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
		brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
		brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
		MainWindow.setPalette(palette)
		font = QtGui.QFont()
		font.setFamily("Calibri")
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		MainWindow.setFont(font)
		MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")

		palette = QtGui.QPalette()
		brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
		brush = QtGui.QBrush(QtGui.QColor(170, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
		brush = QtGui.QBrush(QtGui.QColor(212, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
		brush = QtGui.QBrush(QtGui.QColor(85, 127, 127))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
		brush = QtGui.QBrush(QtGui.QColor(113, 170, 170))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
		brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
		brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
		brush = QtGui.QBrush(QtGui.QColor(170, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
		brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
		brush = QtGui.QBrush(QtGui.QColor(212, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
		brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
		brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
		brush = QtGui.QBrush(QtGui.QColor(170, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
		brush = QtGui.QBrush(QtGui.QColor(212, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
		brush = QtGui.QBrush(QtGui.QColor(85, 127, 127))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
		brush = QtGui.QBrush(QtGui.QColor(113, 170, 170))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
		brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
		brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
		brush = QtGui.QBrush(QtGui.QColor(170, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
		brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
		brush = QtGui.QBrush(QtGui.QColor(212, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
		brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
		brush = QtGui.QBrush(QtGui.QColor(85, 127, 127))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
		brush = QtGui.QBrush(QtGui.QColor(170, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
		brush = QtGui.QBrush(QtGui.QColor(212, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
		brush = QtGui.QBrush(QtGui.QColor(85, 127, 127))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
		brush = QtGui.QBrush(QtGui.QColor(113, 170, 170))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
		brush = QtGui.QBrush(QtGui.QColor(85, 127, 127))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
		brush = QtGui.QBrush(QtGui.QColor(85, 127, 127))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
		brush = QtGui.QBrush(QtGui.QColor(170, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
		brush = QtGui.QBrush(QtGui.QColor(170, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
		brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
		brush = QtGui.QBrush(QtGui.QColor(170, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
		brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)

		self.scroll_area = QtWidgets.QScrollArea(self.centralwidget)
		self.scroll_area.setGeometry(QtCore.QRect(390, 400, 310, 250))
		self.conv_hist = QtWidgets.QListWidget()
		self.conv_hist.setPalette(palette)
		self.conv_hist.setObjectName("conv_hist")
		self.scroll_area.setWidget(self.conv_hist)
		self.scroll_area.setWidgetResizable(True)
		self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		conv_hist = []
		self.conv_hist.setFont(QtGui.QFont('Calibri', 12, QtGui.QFont.Bold))
		
		self.csiro_logo = QLabel(self.centralwidget)
		self.csiro_logo.setGeometry(QtCore.QRect(350, 10, 290, 160))
		self.csiro_logo.setPixmap(QPixmap('newPrefix/csiro-logo.png'))
		self.csiro_logo.resize(self.csiro_logo.width(), self.csiro_logo.height())
		self.csiro_logo.setObjectName("csiro_logo")
		
		self.LM_Status = QtWidgets.QListWidget(self.centralwidget)
		self.LM_Status.setGeometry(QtCore.QRect(390, 200, 280, 170))
		self.LM_Status.setObjectName("LM_Status")
		ls = ['Lab Machine 1', 'Lab Machine 2', 'Lab Machine 3', 'Lab Machine 4']
		self.LM_Status.addItems(ls)
		self.LM_Status.setFont(QtGui.QFont('Calibri', 13, QtGui.QFont.Bold))

		self.LED_LM1 = QLed(self.centralwidget, onColour = QLed.Red, shape = QLed.Circle)
		self.LED_LM1.setGeometry(QtCore.QRect(680, 205, 15, 15))
		self.LED_LM1.value = False

		self.LED_LM2 = QLed(self.centralwidget, onColour = QLed.Red, shape = QLed.Circle)
		self.LED_LM2.setGeometry(QtCore.QRect(680, 230, 15, 15))
		self.LED_LM2.value = False

		self.LED_LM3 = QLed(self.centralwidget, onColour = QLed.Red, shape = QLed.Circle)
		self.LED_LM3.setGeometry(QtCore.QRect(680, 255, 15, 15))
		self.LED_LM3.value = False

		self.LED_LM4 = QLed(self.centralwidget, onColour = QLed.Red, shape = QLed.Circle)
		self.LED_LM4.setGeometry(QtCore.QRect(680, 280, 15, 15))
		self.LED_LM4.value = False


		self.lm_status_label = QtWidgets.QLabel(self.centralwidget)
		self.lm_status_label.setGeometry(QtCore.QRect(390, 180, 121, 16))
		self.lm_status_label.setObjectName("lm_status_label")

		
		self.conv_hist_label = QtWidgets.QLabel(self.centralwidget)
		self.conv_hist_label.setGeometry(QtCore.QRect(390, 380, 131, 16))
		self.conv_hist_label.setObjectName("conv_hist_label")

		self.voice_commands = QtWidgets.QListWidget(self.centralwidget)
		self.voice_commands.setGeometry(QtCore.QRect(30, 270, 321, 101))
		self.voice_commands.setObjectName("voice_commands")
		command_ls = ['Turn on the Spin Coder', 'Start Timer', 'Take Notes', 'Save to Folder']
		self.voice_commands.addItems(command_ls)
		self.voice_commands.setFont(QtGui.QFont('Calibri', 12, QtGui.QFont.Bold))

		
		self.voice_commands_label = QtWidgets.QLabel(self.centralwidget)
		self.voice_commands_label.setGeometry(QtCore.QRect(30, 250, 101, 16))
		self.voice_commands_label.setObjectName("voice_commands_label")

		self.transcript_scroll = QtWidgets.QScrollArea(self.centralwidget)
		self.transcript_scroll.setGeometry(QtCore.QRect(30, 400, 320, 250))
		self.transcription = QtWidgets.QTextBrowser()
		self.transcription.setObjectName("transcription")
		self.transcription.setPalette(palette)
		self.transcript_scroll.setWidget(self.transcription)
		self.transcript_scroll.setWidgetResizable(True)
		trans_hist = ""
		self.transcription.setText(trans_hist)
		self.transcription.setFont(QtGui.QFont('Calibri', 12, QtGui.QFont.Bold))
		
		self.transcription_label = QtWidgets.QLabel(self.centralwidget)
		self.transcription_label.setGeometry(QtCore.QRect(30, 380, 101, 16))
		self.transcription_label.setObjectName("transcription_label")

		
		self.recognised_command = QtWidgets.QTextBrowser(self.centralwidget)
		self.recognised_command.setGeometry(QtCore.QRect(30, 200, 321, 41))
		self.recognised_command.setObjectName("recognised_command")
		self.recognised_command.setText("")
		self.recognised_command.setFont(QtGui.QFont('Calibri', 12, QtGui.QFont.Bold))
		
		self.recognised_command_label = QtWidgets.QLabel(self.centralwidget)
		self.recognised_command_label.setGeometry(QtCore.QRect(30, 180, 131, 16))
		self.recognised_command_label.setObjectName("recognised_command_label")

		self.assistant_status = QtWidgets.QTextBrowser(self.centralwidget)
		self.assistant_status.setGeometry(QtCore.QRect(30, 140, 285, 30))
		self.assistant_status.setObjectName("assistant_status")
		self.assistant_status.setText("Deactivated")
		self.assistant_status.setFont(QtGui.QFont('Calibri', 12, QtGui.QFont.Bold))
		
		self.LED_status1 = QLed(self.centralwidget, onColour = QLed.Blue, shape = QLed.Circle)
		self.LED_status1.setGeometry(QtCore.QRect(320, 140, 30, 30))
		self.LED_status1.value = False

		self.assistant_status_label = QtWidgets.QLabel(self.centralwidget)
		self.assistant_status_label.setGeometry(QtCore.QRect(30, 120, 111, 16))
		self.assistant_status_label.setObjectName("assistant_status_label")

		self.mic_status = QtWidgets.QTextBrowser(self.centralwidget)
		self.mic_status.setGeometry(QtCore.QRect(30, 80, 285, 30))
		self.mic_status.setObjectName("mic_status")
		self.mic_status.setText("Plantronics Voyager 3200 --Connected")
		
		self.LED_status2 = QLed(self.centralwidget, onColour = QLed.Red, shape = QLed.Circle)
		self.LED_status2.setGeometry(QtCore.QRect(320, 80, 30, 30))
		self.LED_status2.value = True

		self.mic_status_label = QtWidgets.QLabel(self.centralwidget)
		self.mic_status_label.setGeometry(QtCore.QRect(30, 60, 111, 16))
		self.mic_status_label.setObjectName("mic_status_label")

		self.lcd = QtWidgets.QLCDNumber(self.centralwidget)
		self.lcd.display(0)
		self.lcd.setGeometry(30,20,100,30)

		self.timer_label = QtWidgets.QLabel(self.centralwidget)
		self.timer_label.setGeometry(QtCore.QRect(140, 25, 100, 30))
		self.timer_label.setObjectName("Countdown Timer")

		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 735, 21))
		self.menubar.setObjectName("menubar")
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)
	
	def retranslateUi(self, MainWindow):
		"""
		Translates software tags to UI tags displayed on GUI
		"""
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "CSIRO Virtual Lab Assistant"))
		self.lm_status_label.setText(_translate("MainWindow", "Lab Machine Status"))
		self.conv_hist_label.setText(_translate("MainWindow", "Conversation History"))
		self.voice_commands_label.setText(_translate("MainWindow", "Voice Commands"))
		self.transcription_label.setText(_translate("MainWindow", "Transcription"))
		self.recognised_command_label.setText(_translate("MainWindow", "Recognised Command"))
		self.assistant_status_label.setText(_translate("MainWindow", "Assistant Status"))
		self.mic_status_label.setText(_translate("MainWindow", "Microphone Status"))
		self.timer_label.setText(_translate("MainWindow", "Countdown Timer"))

	def update_function(self):
		"""
		Function that creates a new Qthread and
		connects the signal emitted from the Qthread 
		to update_info()
		"""
		self.get_thread = updateThread()
		self.get_thread.new_info.connect(self.update_info)
		self.get_thread.start()
		print("GUI THREAD started successfully\n")

	def update_info(self, post_text):
		'''
		Function to update widgets in the UI Window
		based on post_text received
		'''
		if post_text['widget']=='timer':
			self.lcd.display(post_text['widget_update'])
			self.lcd.update()
		if post_text['widget']=='conv_hist':
			conv_hist.append(post_text['widget_update'])
			conv_hist.append("----------------")
			self.conv_hist.clear()
			self.conv_hist.addItems(conv_hist)
			self.conv_hist.update()
		if post_text['widget']=='transcription':          
			self.transcription.append(post_text['widget_update'])
			self.transcription.update()
		if post_text['widget']=='lm_control':
			LED_no = post_text['widget_update'][0]
			LED_no = str("LED_LM"+LED_no)
			self.LED_no.value = post_text['widget_update'][1:]
			self.LED_no.update()
		if post_text['widget']=='recognised_command':
			self.recognised_command.setText(post_text['widget_update'])
			self.recognised_command.update()
		if post_text['widget']=='mic_status':
			self.LED_status2.value = post_text['widget_update']
			self.LED_status2.update()
		if post_text['widget']=='assistant_status_LED':
			self.LED_status1.value = post_text['widget_update']
			self.LED_status1.update()
		if post_text['widget'] == 'assistant_status':
			self.assistant_status.setText("Activated")
			self.assistant_status.update()


class updateThread(QThread):
	""" Documentation for the updateThread class
	This class creates a QThread which continuously reads from a queue structure
	and emits a signal when new item is read from the queue

	"""
	new_info = pyqtSignal(dict)
	def __init__(self):
		"""
		The constructor
		"""
		QThread.__init__(self)
	def __del__(self):
		self.wait()
	def run(self):
		'''
		Run qthread to continuously polls the gui_queue for new info
		In another function, fill the queue (threaded)
		'''
		while True:
			if gui_queue.empty() is not True:
				queue_item = gui_queue.get()
				self.new_info.emit(queue_item)

def main():
	##
	# Initialise the UI, initialise QThreads

	import sys
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	ui.update_function()
	MainWindow.show()
	sys.exit(app.exec_())

def intent_to_function(detected_intent, params):
	##
	# Function that converts detected intent into actions and function calls
	# @param detected_intent: the intent detected and returned by the dialogflow agent
	# @param params: the parameters detected along with the user intent

	print("***********************************************************")
	if detected_intent == "Quit":
		quit_listen.quit_detect_intent(conv_hist, trans_hist)
	if detected_intent == "SaveFile":
		save_file.save_file(conv_hist, trans_hist)
	if detected_intent == "StartTranscription":
		gcp_stt.streaming_transcribe(gui_queue)
	if detected_intent == "StartCountdownTimer":
		print(params)
		timer.control_timer(queue = gui_queue, duration = params["duration"], start = True)
	if detected_intent == "StopcountdownTimer":
		timer.control_timer(start = False)
	if detected_intent == "LMControl":
		lm_control.control_equipment(params["LabMachine"], params["MachineControl"], gui_queue)
	if detected_intent == "LMStatus":
		lm_status.get_lm_status(lab_machine_status, params["LabMachine"], gui_queue)
	if detected_intent == "TimerStatus":
		timer.control_timer(status_check = True)
	print("***********************************************************")


if __name__ == "__main__":
	## Thread processing for maintaining and updating GUI
	gui_thread = threading.Thread(target=main)
	## Daemon indicates gui thread will terminate when main thread terminates
	gui_thread.daemon=True
	gui_thread.start()

	while True:
		# start trigger word detection, blocking until trigger word detected

		print("Processing in the main loop")
		twd_detect.twd_imitate(gui_queue)


		# Start dialogflow agent to capture intent returns nothing
		# if no intent detected else, returns the intent captured
		## HTTP response from dialogflow agent
		query_result = gcp_dialogflow.start_dialogflow_agent()
		print("Query result received in main loop")
		print(query_result)
		if query_result is not None:
			if query_result.intent.display_name != None:
				## Command recognised by dialogflow agent
				recognised_command = query_result.intent.display_name
				gui_queue.put({
					"widget": "conv_hist",
					"widget_update":"User: " + query_result.query_text
					})
				if query_result.fulfillment_text is not "":				
					gui_queue.put({
						"widget": "conv_hist",
						"widget_update":"CsiroBot: " + query_result.fulfillment_text
						})
				gui_queue.put({
					"widget":"recognised_command",
					"widget_update":recognised_command
					})
				print("======================================================================================")
				print(query_result.intent.display_name)
				print(query_result.parameters)
				speech_engine.speak(query_result.fulfillment_text)
				intent_to_function(query_result.intent.display_name, query_result.parameters)
				save_file.save_file(conv_hist, trans_hist)
				print("Finished Executing intent-based function")


