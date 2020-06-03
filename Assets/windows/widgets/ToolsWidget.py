from PySide2.QtWidgets import (QHBoxLayout, QLineEdit, QVBoxLayout, QWidget, QLabel, QPushButton)
from PySide2.QtCore import Qt

from Assets.windows.WindowsTools import DefineLayoutChildAlignment
from Assets.windows.widgets.ChangeWaveRangeWidget import ChangeWaveRangeWidget
from Assets.mathematical_scripts.util import *

class ToolsWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self) 

        self.setWindowTitle("Options - EEG IHM")

        self.layout = self.CreateLayout() 
        self.setLayout(self.layout)

    def CreateLayout(self):
        layout = QVBoxLayout()

        firstRow = QHBoxLayout()
        firstRow.setSpacing(10)
        firstRow.setMargin(10)

        label_alpha = QLabel("Alpha Wave (Hz) - Min/Max")
        self.alphaMin = QLineEdit(str(waves["alpha"][0]))
        self.alphaMax = QLineEdit(str(waves["alpha"][1]))

        firstRow.addWidget(label_alpha)
        firstRow.addWidget(self.alphaMin)
        firstRow.addWidget(self.alphaMax)

        secondRow = QHBoxLayout()
        secondRow.setSpacing(10)
        secondRow.setMargin(10)

        label_beta = QLabel("Beta Wave (Hz) - Min/Max")
        self.betaMin = QLineEdit(str(waves["beta"][0]))
        self.betaMax = QLineEdit(str(waves["beta"][1]))

        secondRow.addWidget(label_beta)
        secondRow.addWidget(self.betaMin)
        secondRow.addWidget(self.betaMax)

        thirdRow = QHBoxLayout()
        thirdRow.setSpacing(10)
        thirdRow.setMargin(10)

        label_theta = QLabel("Theta Wave (Hz) - Min/Max")
        self.thetaMin = QLineEdit(str(waves["theta"][0]))
        self.thetaMax = QLineEdit(str(waves["theta"][1]))

        thirdRow.addWidget(label_theta)
        thirdRow.addWidget(self.thetaMin)
        thirdRow.addWidget(self.thetaMax)

        fourthRow = QHBoxLayout()
        fourthRow.setSpacing(10)
        fourthRow.setMargin(10)

        label_delta = QLabel("Delta Wave (Hz) - Min/Max")
        self.deltaMin = QLineEdit(str(waves["delta"][0]))
        self.deltaMax = QLineEdit(str(waves["delta"][1]))

        fourthRow.addWidget(label_delta)
        fourthRow.addWidget(self.deltaMin)
        fourthRow.addWidget(self.deltaMax)

        fifthRow = QHBoxLayout()
        fifthRow.setSpacing(10)
        fifthRow.setMargin(10)

        saveBtn = QPushButton("Save")
        saveBtn.clicked.connect(self.saveButtonClick)

        fifthRow.addWidget(saveBtn)

        DefineLayoutChildAlignment(firstRow, Qt.AlignHCenter) 
        DefineLayoutChildAlignment(secondRow, Qt.AlignHCenter) 
        DefineLayoutChildAlignment(thirdRow, Qt.AlignHCenter) 
        DefineLayoutChildAlignment(fourthRow, Qt.AlignHCenter) 
        DefineLayoutChildAlignment(fifthRow, Qt.AlignHCenter) 

        layout.addItem(firstRow)
        layout.addItem(secondRow)
        layout.addItem(thirdRow)
        layout.addItem(fourthRow)
        layout.addItem(fifthRow)

        return layout
        
    #Check if value is changed and if yes update wave signal
    def saveButtonClick(self):
        wavesToUpdate = []

        if (waves["alpha"][0] != int(self.alphaMin.text()) or waves["alpha"][1] != int(self.alphaMax.text())):
            wavesToUpdate.append("alpha")
            waves["alpha"][0] = int(self.alphaMin.text())
            waves["alpha"][1] = int(self.alphaMax.text())

        if (waves["beta"][0] != int(self.betaMin.text()) or waves["beta"][1] != int(self.betaMax.text())):
            wavesToUpdate.append("beta")
            waves["beta"][0] = int(self.betaMin.text())
            waves["beta"][1] = int(self.betaMax.text())

        if (waves["theta"][0] != int(self.thetaMin.text()) or waves["theta"][1] != int(self.thetaMax.text())):
            wavesToUpdate.append("theta")
            waves["theta"][0] = int(self.thetaMin.text())
            waves["theta"][1] = int(self.thetaMax.text())

        if (waves["delta"][0] != int(self.deltaMin.text()) or waves["delta"][1] != int(self.deltaMax.text())):
            wavesToUpdate.append("delta")
            waves["delta"][0] = int(self.deltaMin.text())
            waves["delta"][1] = int(self.deltaMax.text())
        
        if len(wavesToUpdate) > 0:
            self.changeWaveWidget = ChangeWaveRangeWidget(wavesToUpdate)
            self.changeWaveWidget.show()

        self.close()