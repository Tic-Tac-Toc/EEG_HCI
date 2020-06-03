from PySide2.QtWidgets import QWidget
from PySide2.QtCore import Qt, QPointF
from PySide2.QtGui import QPainter, QFont, QLinearGradient

#Widget to display LinearGradientBar.
class LinearGradientBarWidget(QWidget):
    def __init__(self):
        super().__init__() 
        self.update()

    # Stuff to draw gradient
    def paintEvent(self, e):  
        qp = QPainter()
        qp.begin(self)
        
        self.drawGradient(qp)

        qp.end()
    def drawGradient(self, qp):
        gradient = QLinearGradient(QPointF(200,15), QPointF(600,60))
        gradient.setColorAt(0,Qt.blue)
        gradient.setColorAt(0.25,Qt.cyan)
        gradient.setColorAt(0.5,Qt.green)
        gradient.setColorAt(0.75,Qt.yellow)
        gradient.setColorAt(1,Qt.red)
        qp.setBrush(gradient)
        qp.drawRect(200, 15, 600, 60)

        qp.setFont(QFont('Arial', 8))
        qp.setBrush(Qt.black)
        qp.drawText(200, 0, 205, 15, Qt.AlignLeft, "0")
        qp.drawText(395, 0, 405, 15, Qt.AlignLeft, "0.5")
        qp.drawText(595, 0, 600, 15, Qt.AlignLeft, "1")