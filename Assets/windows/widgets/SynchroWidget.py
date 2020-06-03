from PySide2.QtWidgets import (QHBoxLayout, QVBoxLayout, QWidget, QLabel)
from PySide2.QtCore import Qt

from Assets.windows.widgets.LinearGradientBarWidget import LinearGradientBarWidget
from Assets.windows.widgets.QSliderSynchroWidget import QSliderSynchroWidget
from Assets.windows.widgets.ElectrodesSynchrowidget import ElectrodesSynchroWidget
from Assets.windows.WindowsTools import DefineLayoutChildAlignment

#Main widget from Synchro Window.
class SynchroWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self) 
        self.layout = self.CreateLayout() 
        self.setLayout(self.layout)

    # Define global design
    def CreateLayout(self):
        globalLayout = QVBoxLayout()
        
        self.label_file = QLabel("Sélectionnez un fichier (File->Open)")
        self.label_file.setMaximumHeight(20)
        firstRowLayout = QHBoxLayout()
        firstRowLayout.setMargin(10)
        firstRowLayout.setSpacing(10)
        firstRowLayout.addWidget(self.label_file)       

        DefineLayoutChildAlignment(firstRowLayout, Qt.AlignHCenter)
        globalLayout.addItem(firstRowLayout)

        self.gradientWidget = LinearGradientBarWidget()
        self.gradientWidget.setFixedHeight(30) 
        self.gradientWidget.setFixedWidth(600)
        globalLayout.addWidget(self.gradientWidget)  

        self.widget = ElectrodesSynchroWidget()
        globalLayout.addWidget(self.widget)   

        self.sliderwidgetupto = QSliderSynchroWidget()
        self.sliderwidgetupto.setMaximumHeight(40)
        globalLayout.addWidget(self.sliderwidgetupto)

        self.sliderwidgetdownto = QSliderSynchroWidget()
        self.sliderwidgetdownto.setMaximumHeight(40)
        globalLayout.addWidget(self.sliderwidgetdownto)

        return globalLayout

    #Update label when a file is selected
    def SetLabelFile(self, filename):
        self.label_file.setText(filename)
