# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Polarization.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1078, 856)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        MainWindow.setWindowOpacity(10.0)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setGeometry(QtCore.QRect(10, 790, 211, 41))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.pushButton_start = QtWidgets.QPushButton(self.splitter)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(14)
        self.pushButton_start.setFont(font)
        self.pushButton_start.setObjectName("pushButton_start")
        self.pushButton_stop = QtWidgets.QPushButton(self.splitter)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(14)
        self.pushButton_stop.setFont(font)
        self.pushButton_stop.setObjectName("pushButton_stop")
        self.pushButton_save = QtWidgets.QPushButton(self.splitter)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(14)
        self.pushButton_save.setFont(font)
        self.pushButton_save.setObjectName("pushButton_save")
        self.Polarization = QtWidgets.QTextEdit(self.centralwidget)
        self.Polarization.setGeometry(QtCore.QRect(710, 10, 231, 111))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(26)
        self.Polarization.setFont(font)
        self.Polarization.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.Polarization.setToolTipDuration(-1)
        self.Polarization.setAutoFillBackground(False)
        self.Polarization.setStyleSheet("background-color: rgb(240, 240, 240);\n"
"selection-color: rgb(240, 240, 240);\n"
"gridline-color: rgb(240, 240, 240);\n"
"border-color: rgb(240, 240, 240);\n"
"border-top-color: rgb(240, 240, 240);")
        self.Polarization.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Polarization.setReadOnly(True)
        self.Polarization.setObjectName("Polarization")
        self.Show_guess = QtWidgets.QCheckBox(self.centralwidget)
        self.Show_guess.setGeometry(QtCore.QRect(160, 550, 21, 21))
        self.Show_guess.setText("")
        self.Show_guess.setChecked(False)
        self.Show_guess.setTristate(False)
        self.Show_guess.setObjectName("Show_guess")
        self.Fit_8 = QtWidgets.QLabel(self.centralwidget)
        self.Fit_8.setGeometry(QtCore.QRect(10, 700, 111, 17))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(10)
        self.Fit_8.setFont(font)
        self.Fit_8.setObjectName("Fit_8")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(110, 110, 20, 281))
        self.line.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.Averages = QtWidgets.QSpinBox(self.centralwidget)
        self.Averages.setGeometry(QtCore.QRect(130, 700, 91, 22))
        self.Averages.setMinimum(1)
        self.Averages.setMaximum(10000)
        self.Averages.setProperty("value", 1)
        self.Averages.setObjectName("Averages")
        self.Fit_9 = QtWidgets.QLabel(self.centralwidget)
        self.Fit_9.setGeometry(QtCore.QRect(10, 550, 81, 17))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(10)
        self.Fit_9.setFont(font)
        self.Fit_9.setObjectName("Fit_9")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(10, 120, 211, 21))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.StartFreq_2 = QtWidgets.QLabel(self.centralwidget)
        self.StartFreq_2.setGeometry(QtCore.QRect(10, 20, 81, 17))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(10)
        self.StartFreq_2.setFont(font)
        self.StartFreq_2.setObjectName("StartFreq_2")
        self.EndFreq_2 = QtWidgets.QLabel(self.centralwidget)
        self.EndFreq_2.setGeometry(QtCore.QRect(10, 50, 71, 17))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(10)
        self.EndFreq_2.setFont(font)
        self.EndFreq_2.setObjectName("EndFreq_2")
        self.Center_freq = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.Center_freq.setGeometry(QtCore.QRect(120, 20, 91, 23))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(10)
        self.Center_freq.setFont(font)
        self.Center_freq.setKeyboardTracking(False)
        self.Center_freq.setMaximum(9999.0)
        self.Center_freq.setProperty("value", 2030.0)
        self.Center_freq.setObjectName("Center_freq")
        self.Span_freq = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.Span_freq.setGeometry(QtCore.QRect(120, 50, 91, 23))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(10)
        self.Span_freq.setFont(font)
        self.Span_freq.setKeyboardTracking(False)
        self.Span_freq.setMaximum(9999.0)
        self.Span_freq.setProperty("value", 20.0)
        self.Span_freq.setObjectName("Span_freq")
        self.Gamma_fit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.Gamma_fit.setGeometry(QtCore.QRect(130, 160, 91, 24))
        self.Gamma_fit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.Gamma_fit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.Gamma_fit.setReadOnly(True)
        self.Gamma_fit.setObjectName("Gamma_fit")
        self.r_fit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.r_fit.setGeometry(QtCore.QRect(130, 210, 91, 25))
        self.r_fit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.r_fit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.r_fit.setReadOnly(True)
        self.r_fit.setObjectName("r_fit")
        self.Fit = QtWidgets.QLabel(self.centralwidget)
        self.Fit.setGeometry(QtCore.QRect(10, 140, 121, 17))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(10)
        self.Fit.setFont(font)
        self.Fit.setObjectName("Fit")
        self.Fit_5 = QtWidgets.QLabel(self.centralwidget)
        self.Fit_5.setGeometry(QtCore.QRect(10, 240, 81, 17))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(10)
        self.Fit_5.setFont(font)
        self.Fit_5.setObjectName("Fit_5")
        self.A_fit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.A_fit.setGeometry(QtCore.QRect(130, 310, 91, 25))
        self.A_fit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.A_fit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.A_fit.setReadOnly(True)
        self.A_fit.setObjectName("A_fit")
        self.Fit_7 = QtWidgets.QLabel(self.centralwidget)
        self.Fit_7.setGeometry(QtCore.QRect(10, 440, 81, 17))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(10)
        self.Fit_7.setFont(font)
        self.Fit_7.setObjectName("Fit_7")
        self.n_scroll = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.n_scroll.setGeometry(QtCore.QRect(10, 460, 91, 23))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(10)
        self.n_scroll.setFont(font)
        self.n_scroll.setSuffix("")
        self.n_scroll.setDecimals(0)
        self.n_scroll.setMinimum(1.0)
        self.n_scroll.setMaximum(8.0)
        self.n_scroll.setSingleStep(1.0)
        self.n_scroll.setProperty("value", 3.0)
        self.n_scroll.setObjectName("n_scroll")
        self.Fit_2 = QtWidgets.QLabel(self.centralwidget)
        self.Fit_2.setGeometry(QtCore.QRect(10, 190, 91, 17))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(10)
        self.Fit_2.setFont(font)
        self.Fit_2.setObjectName("Fit_2")
        self.phi_scroll = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.phi_scroll.setGeometry(QtCore.QRect(10, 260, 91, 23))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(10)
        self.phi_scroll.setFont(font)
        self.phi_scroll.setMinimum(-4.0)
        self.phi_scroll.setMaximum(4.0)
        self.phi_scroll.setSingleStep(0.01)
        self.phi_scroll.setProperty("value", 1.5)
        self.phi_scroll.setObjectName("phi_scroll")
        self.Fit_3 = QtWidgets.QLabel(self.centralwidget)
        self.Fit_3.setGeometry(QtCore.QRect(10, 110, 79, 17))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Fit_3.setFont(font)
        self.Fit_3.setObjectName("Fit_3")
        self.r_scroll = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.r_scroll.setGeometry(QtCore.QRect(10, 210, 91, 23))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(10)
        self.r_scroll.setFont(font)
        self.r_scroll.setSuffix("")
        self.r_scroll.setMaximum(1.0)
        self.r_scroll.setSingleStep(0.01)
        self.r_scroll.setProperty("value", 0.1)
        self.r_scroll.setObjectName("r_scroll")
        self.Fit_4 = QtWidgets.QLabel(self.centralwidget)
        self.Fit_4.setGeometry(QtCore.QRect(130, 110, 16, 17))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Fit_4.setFont(font)
        self.Fit_4.setObjectName("Fit_4")
        self.Fit_6 = QtWidgets.QLabel(self.centralwidget)
        self.Fit_6.setGeometry(QtCore.QRect(10, 290, 81, 17))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(10)
        self.Fit_6.setFont(font)
        self.Fit_6.setObjectName("Fit_6")
        self.Gamma_scroll = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.Gamma_scroll.setGeometry(QtCore.QRect(10, 160, 91, 23))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(10)
        self.Gamma_scroll.setFont(font)
        self.Gamma_scroll.setDecimals(0)
        self.Gamma_scroll.setMaximum(9999.0)
        self.Gamma_scroll.setProperty("value", 100.0)
        self.Gamma_scroll.setObjectName("Gamma_scroll")
        self.A_scroll = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.A_scroll.setGeometry(QtCore.QRect(10, 310, 91, 23))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(10)
        self.A_scroll.setFont(font)
        self.A_scroll.setSuffix("")
        self.A_scroll.setMinimum(0.0)
        self.A_scroll.setMaximum(9999.0)
        self.A_scroll.setSingleStep(0.01)
        self.A_scroll.setProperty("value", 1.0)
        self.A_scroll.setObjectName("A_scroll")
        self.phi_fit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.phi_fit.setGeometry(QtCore.QRect(130, 260, 91, 25))
        self.phi_fit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.phi_fit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.phi_fit.setReadOnly(True)
        self.phi_fit.setObjectName("phi_fit")
        self.Fit_10 = QtWidgets.QLabel(self.centralwidget)
        self.Fit_10.setGeometry(QtCore.QRect(10, 730, 111, 17))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(10)
        self.Fit_10.setFont(font)
        self.Fit_10.setObjectName("Fit_10")
        self.Updating_speed = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.Updating_speed.setGeometry(QtCore.QRect(130, 730, 91, 22))
        self.Updating_speed.setMinimum(0.01)
        self.Updating_speed.setMaximum(999.0)
        self.Updating_speed.setSingleStep(0.1)
        self.Updating_speed.setProperty("value", 0.1)
        self.Updating_speed.setObjectName("Updating_speed")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(10, 500, 211, 21))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.Fit_11 = QtWidgets.QLabel(self.centralwidget)
        self.Fit_11.setGeometry(QtCore.QRect(10, 490, 79, 17))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Fit_11.setFont(font)
        self.Fit_11.setObjectName("Fit_11")
        self.graphicsView = PlotWidget(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(230, 100, 841, 481))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setAutoFillBackground(False)
        self.graphicsView.setFrameShape(QtWidgets.QFrame.Box)
        self.graphicsView.setFrameShadow(QtWidgets.QFrame.Plain)
        self.graphicsView.setMidLineWidth(0)
        self.graphicsView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.graphicsView.setObjectName("graphicsView")
        self.Fit_12 = QtWidgets.QLabel(self.centralwidget)
        self.Fit_12.setGeometry(QtCore.QRect(10, 640, 81, 17))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(10)
        self.Fit_12.setFont(font)
        self.Fit_12.setObjectName("Fit_12")
        self.Save_png = QtWidgets.QCheckBox(self.centralwidget)
        self.Save_png.setGeometry(QtCore.QRect(160, 640, 21, 21))
        self.Save_png.setText("")
        self.Save_png.setChecked(True)
        self.Save_png.setTristate(False)
        self.Save_png.setObjectName("Save_png")
        self.Fit_13 = QtWidgets.QLabel(self.centralwidget)
        self.Fit_13.setGeometry(QtCore.QRect(10, 670, 81, 17))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(10)
        self.Fit_13.setFont(font)
        self.Fit_13.setObjectName("Fit_13")
        self.Save_fit = QtWidgets.QCheckBox(self.centralwidget)
        self.Save_fit.setGeometry(QtCore.QRect(160, 670, 21, 21))
        self.Save_fit.setText("")
        self.Save_fit.setChecked(True)
        self.Save_fit.setTristate(False)
        self.Save_fit.setObjectName("Save_fit")
        self.Fit_14 = QtWidgets.QLabel(self.centralwidget)
        self.Fit_14.setGeometry(QtCore.QRect(10, 520, 81, 17))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(10)
        self.Fit_14.setFont(font)
        self.Fit_14.setObjectName("Fit_14")
        self.Show_fit = QtWidgets.QCheckBox(self.centralwidget)
        self.Show_fit.setGeometry(QtCore.QRect(160, 520, 21, 21))
        self.Show_fit.setText("")
        self.Show_fit.setChecked(False)
        self.Show_fit.setTristate(False)
        self.Show_fit.setObjectName("Show_fit")
        self.Fit_15 = QtWidgets.QLabel(self.centralwidget)
        self.Fit_15.setGeometry(QtCore.QRect(10, 760, 111, 17))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(10)
        self.Fit_15.setFont(font)
        self.Fit_15.setObjectName("Fit_15")
        self.Fit_speed = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.Fit_speed.setGeometry(QtCore.QRect(130, 760, 91, 25))
        self.Fit_speed.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.Fit_speed.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.Fit_speed.setReadOnly(True)
        self.Fit_speed.setObjectName("Fit_speed")
        self.SamplingTime = QtWidgets.QSpinBox(self.centralwidget)
        self.SamplingTime.setGeometry(QtCore.QRect(380, 20, 91, 22))
        self.SamplingTime.setMaximum(1000)
        self.SamplingTime.setSingleStep(1)
        self.SamplingTime.setProperty("value", 50)
        self.SamplingTime.setObjectName("SamplingTime")
        self.StartFreq_3 = QtWidgets.QLabel(self.centralwidget)
        self.StartFreq_3.setGeometry(QtCore.QRect(240, 20, 121, 17))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(10)
        self.StartFreq_3.setFont(font)
        self.StartFreq_3.setObjectName("StartFreq_3")
        self.StartFreq_4 = QtWidgets.QLabel(self.centralwidget)
        self.StartFreq_4.setGeometry(QtCore.QRect(240, 50, 121, 17))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(10)
        self.StartFreq_4.setFont(font)
        self.StartFreq_4.setObjectName("StartFreq_4")
        self.SamplingRate = QtWidgets.QSpinBox(self.centralwidget)
        self.SamplingRate.setGeometry(QtCore.QRect(380, 50, 91, 22))
        self.SamplingRate.setPrefix("")
        self.SamplingRate.setMinimum(1)
        self.SamplingRate.setMaximum(30)
        self.SamplingRate.setSingleStep(1)
        self.SamplingRate.setProperty("value", 15)
        self.SamplingRate.setDisplayIntegerBase(10)
        self.SamplingRate.setObjectName("SamplingRate")
        self.Channel = QtWidgets.QSpinBox(self.centralwidget)
        self.Channel.setGeometry(QtCore.QRect(540, 20, 91, 22))
        self.Channel.setSuffix("")
        self.Channel.setMaximum(4)
        self.Channel.setSingleStep(1)
        self.Channel.setProperty("value", 1)
        self.Channel.setDisplayIntegerBase(10)
        self.Channel.setObjectName("Channel")
        self.graphicsViewScope = PlotWidget(self.centralwidget)
        self.graphicsViewScope.setGeometry(QtCore.QRect(230, 590, 841, 241))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.graphicsViewScope.sizePolicy().hasHeightForWidth())
        self.graphicsViewScope.setSizePolicy(sizePolicy)
        self.graphicsViewScope.setAutoFillBackground(False)
        self.graphicsViewScope.setFrameShape(QtWidgets.QFrame.Box)
        self.graphicsViewScope.setFrameShadow(QtWidgets.QFrame.Plain)
        self.graphicsViewScope.setMidLineWidth(0)
        self.graphicsViewScope.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.graphicsViewScope.setObjectName("graphicsViewScope")
        self.Fit_17 = QtWidgets.QLabel(self.centralwidget)
        self.Fit_17.setGeometry(QtCore.QRect(10, 340, 91, 17))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(10)
        self.Fit_17.setFont(font)
        self.Fit_17.setObjectName("Fit_17")
        self.B_fit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.B_fit.setGeometry(QtCore.QRect(130, 360, 91, 25))
        self.B_fit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.B_fit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.B_fit.setReadOnly(True)
        self.B_fit.setObjectName("B_fit")
        self.B_scroll = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.B_scroll.setGeometry(QtCore.QRect(10, 360, 91, 23))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(10)
        self.B_scroll.setFont(font)
        self.B_scroll.setSuffix("")
        self.B_scroll.setMinimum(0.0)
        self.B_scroll.setMaximum(9999.0)
        self.B_scroll.setSingleStep(0.01)
        self.B_scroll.setProperty("value", 1.0)
        self.B_scroll.setObjectName("B_scroll")
        self.Fit_18 = QtWidgets.QLabel(self.centralwidget)
        self.Fit_18.setGeometry(QtCore.QRect(10, 580, 81, 17))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(10)
        self.Fit_18.setFont(font)
        self.Fit_18.setObjectName("Fit_18")
        self.Show_scope = QtWidgets.QCheckBox(self.centralwidget)
        self.Show_scope.setGeometry(QtCore.QRect(160, 580, 21, 21))
        self.Show_scope.setText("")
        self.Show_scope.setChecked(False)
        self.Show_scope.setTristate(False)
        self.Show_scope.setObjectName("Show_scope")
        self.Show_R_I = QtWidgets.QCheckBox(self.centralwidget)
        self.Show_R_I.setGeometry(QtCore.QRect(160, 610, 21, 21))
        self.Show_R_I.setText("")
        self.Show_R_I.setChecked(False)
        self.Show_R_I.setTristate(False)
        self.Show_R_I.setObjectName("Show_R_I")
        self.Fit_19 = QtWidgets.QLabel(self.centralwidget)
        self.Fit_19.setGeometry(QtCore.QRect(10, 610, 101, 17))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(10)
        self.Fit_19.setFont(font)
        self.Fit_19.setObjectName("Fit_19")
        self.Fit_20 = QtWidgets.QLabel(self.centralwidget)
        self.Fit_20.setGeometry(QtCore.QRect(130, 290, 81, 17))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(10)
        self.Fit_20.setFont(font)
        self.Fit_20.setObjectName("Fit_20")
        self.Fit_21 = QtWidgets.QLabel(self.centralwidget)
        self.Fit_21.setGeometry(QtCore.QRect(130, 140, 121, 17))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(10)
        self.Fit_21.setFont(font)
        self.Fit_21.setObjectName("Fit_21")
        self.D_fit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.D_fit.setGeometry(QtCore.QRect(130, 410, 91, 25))
        self.D_fit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.D_fit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.D_fit.setReadOnly(True)
        self.D_fit.setObjectName("D_fit")
        self.Fit_22 = QtWidgets.QLabel(self.centralwidget)
        self.Fit_22.setGeometry(QtCore.QRect(10, 390, 111, 17))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(10)
        self.Fit_22.setFont(font)
        self.Fit_22.setObjectName("Fit_22")
        self.D_scroll = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.D_scroll.setGeometry(QtCore.QRect(10, 410, 91, 23))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(10)
        self.D_scroll.setFont(font)
        self.D_scroll.setSuffix("")
        self.D_scroll.setMinimum(0.0)
        self.D_scroll.setMaximum(9999.0)
        self.D_scroll.setSingleStep(0.01)
        self.D_scroll.setProperty("value", 1.0)
        self.D_scroll.setObjectName("D_scroll")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_start.setText(_translate("MainWindow", "Start"))
        self.pushButton_stop.setText(_translate("MainWindow", "Stop"))
        self.pushButton_save.setText(_translate("MainWindow", "Save"))
        self.Polarization.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Segoe UI Historic\'; font-size:26pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:22pt;\">Polarization:</span></p></body></html>"))
        self.Fit_8.setText(_translate("MainWindow", "Averages:"))
        self.Fit_9.setText(_translate("MainWindow", "Show guess:"))
        self.StartFreq_2.setText(_translate("MainWindow", "Center freq.:"))
        self.EndFreq_2.setText(_translate("MainWindow", "Span freq.:"))
        self.Center_freq.setSuffix(_translate("MainWindow", " kHz"))
        self.Span_freq.setSuffix(_translate("MainWindow", " kHz"))
        self.Fit.setText(_translate("MainWindow", "<html><head/><body><p>Linewidth, Γ:</p></body></html>"))
        self.Fit_5.setText(_translate("MainWindow", "<html><head/><body><p>Phase, φ:</p></body></html>"))
        self.Fit_7.setText(_translate("MainWindow", "Peaks, n:"))
        self.Fit_2.setText(_translate("MainWindow", "Population, r:"))
        self.phi_scroll.setSuffix(_translate("MainWindow", " Pi"))
        self.Fit_3.setText(_translate("MainWindow", "Initial guess:"))
        self.Fit_4.setText(_translate("MainWindow", "Fit"))
        self.Fit_6.setText(_translate("MainWindow", "Amplitude, A:"))
        self.Gamma_scroll.setSuffix(_translate("MainWindow", " Hz"))
        self.Fit_10.setText(_translate("MainWindow", "Updating speed:"))
        self.Updating_speed.setSuffix(_translate("MainWindow", " s"))
        self.Fit_11.setText(_translate("MainWindow", "Controls"))
        self.Fit_12.setText(_translate("MainWindow", "Save png:"))
        self.Fit_13.setText(_translate("MainWindow", "Save fit:"))
        self.Fit_14.setText(_translate("MainWindow", "Show fit:"))
        self.Fit_15.setText(_translate("MainWindow", "Fitting speed:"))
        self.SamplingTime.setSuffix(_translate("MainWindow", " ms"))
        self.StartFreq_3.setText(_translate("MainWindow", "Sampling time:"))
        self.StartFreq_4.setText(_translate("MainWindow", "Sampling rate:"))
        self.SamplingRate.setSuffix(_translate("MainWindow", " MHz"))
        self.Channel.setPrefix(_translate("MainWindow", "Channel "))
        self.Fit_17.setText(_translate("MainWindow", "Background, B:"))
        self.Fit_18.setText(_translate("MainWindow", "Show Scope:"))
        self.Fit_19.setText(_translate("MainWindow", "Real and Imag:"))
        self.Fit_20.setText(_translate("MainWindow", "A0, A1, A2..."))
        self.Fit_21.setText(_translate("MainWindow", "<html><head/><body><p>Γ_0, Γ_1, Γ_2...</p></body></html>"))
        self.Fit_22.setText(_translate("MainWindow", "Peak seperation:"))

from pyqtgraph import PlotWidget
