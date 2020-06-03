import sys
from PySide2.QtWidgets import QSlider, QWidget, QLabel
from PySide2.QtCore import Qt

#Simple class to facilitate the use of a QSlider Widget (easier to serealize)
class QSliderSynchroWidget(QWidget):
    
    def __init__(self):
        super().__init__() 
    
        self.slider = QSlider( Qt.Horizontal, self )
        self.slider.setGeometry( 200, 10, 400, 40 )        
        
        self.labelvalue = QLabel( self )
        self.labelvalue.setGeometry(650, 10, 50, 35)