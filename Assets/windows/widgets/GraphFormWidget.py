from PySide2.QtWidgets import (QHBoxLayout, QVBoxLayout, QWidget, QLabel, QComboBox, QPushButton)
from PySide2.QtCore import Qt

import os

from Assets.windows.WindowsTools import DefineLayoutChildAlignment
from Assets.windows.widgets.GraphWidget import GraphWidget
from Assets.windows.widgets.HeatmapWidget import HeatMapWidget

from Assets.mathematical_scripts.datas_help import getRawDatas
from Assets.mathematical_scripts.util import getElectrodesList

# Main widget from the OneGraph window.
class GraphFormWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)        

        self.layout = self.CreateLayout() 
        self.setLayout(self.layout)

    #Layout design
    def CreateLayout(self):
        globalLayout = QVBoxLayout()
        
        label_cat = QLabel("Category : ")
        self.cb_cat = QComboBox()
        self.cb_cat.addItems(["Active", "Control", "Death"])
        self.cb_cat.currentIndexChanged.connect(self.cb_category_index_changed)

        label_patient = QLabel("Patient : ")
        self.cb_patient = QComboBox()
        self.cb_patient.addItems(GraphFormWidget.FindPatients(self.cb_cat.currentText()))
        
        label_electrode = QLabel("Electrode : ")
        self.cb_electrode = QComboBox()
        self.cb_electrode.addItems(getElectrodesList())

        label_wave = QLabel("Wave type : ")
        self.cb_wave = QComboBox()
        self.cb_wave.addItems(["Alpha", "Beta", "Theta", "Delta"])

        firstRowLayout = QHBoxLayout()
        firstRowLayout.setMargin(10)
        firstRowLayout.setSpacing(10)
        firstRowLayout.addWidget(label_cat)
        firstRowLayout.addWidget(self.cb_cat)
        firstRowLayout.addWidget(label_patient)
        firstRowLayout.addWidget(self.cb_patient)
        firstRowLayout.addWidget(label_electrode)
        firstRowLayout.addWidget(self.cb_electrode)
        firstRowLayout.addWidget(label_wave)
        firstRowLayout.addWidget(self.cb_wave)

        DefineLayoutChildAlignment(firstRowLayout, Qt.AlignHCenter)

        globalLayout.addItem(firstRowLayout)

        self.heatMapBtn = QPushButton("Show heatmap") 
        self.heatMapBtn.clicked.connect(self.heatMapBtnClick)

        showBtn = QPushButton("Show graph")
        showBtn.clicked.connect(self.showBtnClick)
        
        secondRowLayout = QHBoxLayout()
        secondRowLayout.setMargin(10)
        secondRowLayout.setSpacing(10)
        secondRowLayout.addWidget(self.heatMapBtn)
        secondRowLayout.addWidget(showBtn)
        
        DefineLayoutChildAlignment(secondRowLayout, Qt.AlignHCenter)

        globalLayout.addItem(secondRowLayout)

        self.graphWidget = GraphWidget()
        globalLayout.addWidget(self.graphWidget)                

        return globalLayout

    #Get list of patients
    def FindPatients(directory):
       return os.listdir('./Datas/' + directory)

    #Update list of patients when combobox changed
    def cb_category_index_changed(self, index):
        self.cb_patient.clear()
        self.cb_patient.addItems(GraphFormWidget.FindPatients(self.cb_cat.currentText()))

    #Load graph
    def showBtnClick(self):
        datas = getRawDatas(self.cb_patient.currentText(), self.cb_cat.currentText(), self.cb_wave.currentText())
        datas = [datas['t'], datas[self.cb_electrode.currentText()]]
        self.graphWidget.Load(datas)   

    #Load heatmap
    def heatMapBtnClick(self):
        self.htmapwidget = HeatMapWidget()
        self.htmapwidget.Load(self.cb_patient.currentText(), self.cb_cat.currentText(), self.cb_wave.currentText())
        self.htmapwidget.show()
       