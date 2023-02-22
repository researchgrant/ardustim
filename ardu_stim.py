# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 12:04:02 2022

@author: gweiss01
"""

from ardu_window import Ui_MainWindow
import sys, os
from PyQt5 import QtCore, QtWidgets, QtTest 
from PyQt5.QtGui import QPixmap
import pyfirmata
import time
from serial.tools import list_ports
import subprocess


app = QtWidgets.QApplication(sys.argv)
Dialog = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(Dialog)
Dialog.show()

script_dir=os.path.dirname(os.path.realpath(__file__))

ports = {port.device:port.description for port in list_ports.comports()}
ui.portBox.addItems([key+": "+value for key,value in reversed(ports.items())])


proc=None
# trainDurEdit
# pretrainDurEdit
# pulseWidthEdit
# patternRepeatsBox
# freqPatternEdit

def stopStim():
    global proc
    try:proc.kill()
    except:pass
    port=ui.portBox.currentText().split(":")[0]
    proc=subprocess.Popen(["python", os.path.join(script_dir,r"ardu_cli.py"),
                           str(1),'Sine Wave',str(0),str(0),str(0),str(0),str(port),str(0)])
    ui.startButton.setEnabled(False)
    ui.stopButton.setEnabled(False)
    QtTest.QTest.qWait(6000)
    ui.startButton.setEnabled(True)
    ui.stopButton.setEnabled(True)
    


def startStim():
    ui.startButton.setDisabled(True)
    global proc
    try:
        port=ui.portBox.currentText().split(":")[0]
        number_of_trains = ui.patternRepeatsBox.text()
        inter_train_interval= ui.pretrainDurEdit.text()
        train_dur = ui.trainDurEdit.text()
        freq_list = ui.freqPatternEdit.text()
        pulse_ratio = ui.pulseWidthEdit.text()
        shape = ui.waveShapeBox.currentText()
        wait=ui.waitEdit.text()
        # print(freq_list,pulse_ratio,script_dir)
        proc=subprocess.Popen(["python", os.path.join(script_dir,r"ardu_cli.py"),
                               number_of_trains,shape,
                               inter_train_interval,train_dur,freq_list,pulse_ratio,port,wait])
    finally:
        pass

    QtTest.QTest.qWait(int(float(number_of_trains)*(float(inter_train_interval)+float(train_dur))*1000)+6000)
    stopStim()

    
    
    
ui.startButton.clicked.connect(lambda:startStim())

def user_stop():
    print("ABORTING...")
    stopStim()

ui.stopButton.clicked.connect(lambda:user_stop())

if __name__ == '__main__': 
    app.exec_()