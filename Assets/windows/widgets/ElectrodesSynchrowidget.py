from PySide2.QtWidgets import QWidget
from PySide2.QtCore import Qt, QPoint
from PySide2.QtGui import QPainter, QPen, QColor, QFont

import os
import math

from Assets.mathematical_scripts.util import getElectrodesList

class ElectrodesSynchroWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setBaseSize(800,850)   
        self.setMaximumWidth(800)
        self.drawConnection = False

    #Function which load electrodes position, all are based on the up-left-quarter electrodes positions
    def LoadElectrodesInfos(self):
        self.electrodesPos = {}
        self.electrodesPos["FP1"] = [QPoint(self.center.x() - (self.rx*1/10), self.center.y() - (self.ry*9/10)), False]
        self.electrodesPos["F3"] = [QPoint(self.center.x() - (self.rx*2/10), self.center.y() - (self.ry*5/10)), False]
        self.electrodesPos["FZ"] = [QPoint(self.center.x(), self.center.y() - (self.ry*9/20)), False]
        self.electrodesPos["F7"] = [QPoint(self.center.x() - (self.rx*8/20), self.center.y() - (self.ry*16/20)), False]
        self.electrodesPos["FC7"] = [QPoint(self.center.x(), self.center.y() - (self.ry*2/10)), False]
        self.electrodesPos["FT7"] = [QPoint(self.center.x() - (self.rx*15/20), self.center.y() - (self.ry*10/20)), False]
        self.electrodesPos["T3"] = [QPoint(self.center.x() - (self.rx*9/10), self.center.y()), False]
        self.electrodesPos["C3"] = [QPoint(self.center.x() - (self.rx*5/10), self.center.y()), False]
        self.electrodesPos["FC3"] = [QPoint(self.center.x() - (self.rx * 3/10), self.center.y() - (self.ry*5/20)), False]

        self.electrodesPos["FP2"] = [QPoint(-self.electrodesPos["FP1"][0].x() + 2 * self.center.x(), self.electrodesPos["FP1"][0].y()), False]
        self.electrodesPos["F4"] = [QPoint(-self.electrodesPos["F3"][0].x() + 2 * self.center.x(), self.electrodesPos["F3"][0].y()), False]
        self.electrodesPos["F8"] = [QPoint(-self.electrodesPos["F7"][0].x() + 2 * self.center.x(), self.electrodesPos["F7"][0].y()), False]
        self.electrodesPos["CZ"] = [self.center, False]
        self.electrodesPos["C4"] = [QPoint(-self.electrodesPos["C3"][0].x() + 2 * self.center.x(), self.electrodesPos["C3"][0].y()), False]
        self.electrodesPos["T4"] = [QPoint(-self.electrodesPos["T3"][0].x() + 2 * self.center.x(), self.electrodesPos["T3"][0].y()), False]
        self.electrodesPos["FT8"] = [QPoint(-self.electrodesPos["FT7"][0].x() + 2 * self.center.x(), self.electrodesPos["FT7"][0].y()), False]
        self.electrodesPos["FC4"] = [QPoint(-self.electrodesPos["FC3"][0].x() + 2 * self.center.x(), self.electrodesPos["FC3"][0].y()), False]

        self.electrodesPos["T5"] = [QPoint(self.electrodesPos["F7"][0].x(), -self.electrodesPos["F7"][0].y() + 2 * self.center.y()), False]
        self.electrodesPos["P3"] = [QPoint(self.electrodesPos["F3"][0].x(), -self.electrodesPos["F3"][0].y() + 2 * self.center.y()), False]
        self.electrodesPos["PZ"] = [QPoint(self.electrodesPos["FZ"][0].x(), -self.electrodesPos["FZ"][0].y() + 2 * self.center.y()), False]
        self.electrodesPos["CPZ"] = [QPoint(self.electrodesPos["FC7"][0].x(), -self.electrodesPos["FC7"][0].y() + 2 * self.center.y()), False]
        self.electrodesPos["TP8"] = [QPoint(self.electrodesPos["FT8"][0].x(), -self.electrodesPos["FT8"][0].y() + 2 * self.center.y()), False]
        self.electrodesPos["CP4"] = [QPoint(-self.electrodesPos["FC3"][0].x() + 2 * self.center.x(), -self.electrodesPos["FC3"][0].y() + 2 * self.center.y()), False]

        self.electrodesPos["P4"] = [QPoint(self.electrodesPos["F4"][0].x(), -self.electrodesPos["F4"][0].y() + 2 * self.center.y()), False]
        self.electrodesPos["T6"] = [QPoint(self.electrodesPos["F8"][0].x(), -self.electrodesPos["F8"][0].y() + 2 * self.center.y()), False]
        self.electrodesPos["O1"] = [QPoint(self.electrodesPos["FP1"][0].x(), -self.electrodesPos["FP1"][0].y() + 2 * self.center.y()), False]
        self.electrodesPos["O2"] = [QPoint(self.electrodesPos["FP2"][0].x(), -self.electrodesPos["FP2"][0].y() + 2 * self.center.y()), False]
        self.electrodesPos["TP7"] = [QPoint(-self.electrodesPos["TP8"][0].x() + 2 * self.center.x(), self.electrodesPos["TP8"][0].y()), False]
        self.electrodesPos["CP3"] = [QPoint(self.electrodesPos["FC3"][0].x(), -self.electrodesPos["FC3"][0].y() + 2 * self.center.y()), False]
        self.electrodesPos["OZ"] = [QPoint(self.center.x(), self.center.y() + (self.ry*19/20)), False]

        self.electrodesList = getElectrodesList()

    #Function which load the connection from the PSC Matrix Size : Nelec x Nelec
    def LoadConnection(self, mat, limitdownvalue, limitupvalue):
        self.mat = mat
        self.drawConnection = True
        self.limitUpValue = limitupvalue
        self.limitDownValue = limitdownvalue
        self.update()

    #Stuff to draw head, connection, electrodes using QPainter
    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawHead(qp)

        self.LoadElectrodesInfos()

        if self.drawConnection:
            self.drawConnections(qp)

        self.drawElectrode(qp, QPoint(self.center.x() - self.rx - 20, self.center.y()), "A1") #left ear
        self.drawElectrode(qp, QPoint(self.center.x() + self.rx + 20, self.center.y()), "A2") #right ear

        for key in self.electrodesPos.keys():
            self.drawElectrode(qp,self.electrodesPos[key][0], key)
        

        qp.end()
    def drawConnections(self, qp):
        already_draw = []
        for i in range(len(self.mat)):
            for j in range(len(self.mat[0])):
                if ((i,j) in already_draw or (j,i) in already_draw):
                    continue
                if self.mat[i][j] < self.limitUpValue:
                    continue
                if self.mat[i][j] > self.limitDownValue:
                    continue
                
                if (self.electrodesPos[self.electrodesList[i]][1] == False):
                    self.drawElectrode(qp,self.electrodesPos[self.electrodesList[i]][0], self.electrodesList[i])
                    self.electrodesPos[self.electrodesList[i]][1] = True
                if (self.electrodesPos[self.electrodesList[j]][1] == False):
                    self.drawElectrode(qp,self.electrodesPos[self.electrodesList[j]][0], self.electrodesList[j])
                    self.electrodesPos[self.electrodesList[j]][1] = True

                self.drawLine(qp, self.electrodesPos[self.electrodesList[i]][0], self.electrodesPos[self.electrodesList[j]][0], round(self.mat[i][j],2))
                already_draw.append((i,j))
    def drawHead(self, qp):      
        pen = QPen(Qt.black, 1, Qt.SolidLine)
        qp.setPen(pen)
        self.center = QPoint(self.size().width()/2, self.size().height()/2)
        self.rx = (self.size().width() - 150)/2
        self.ry = (self.size().height() - 100)/2
        qp.drawEllipse(self.center, self.rx, self.ry)        

        pen.setStyle(Qt.DashLine)
        qp.setPen(pen)
        qp.drawEllipse(self.center, self.rx - 1/10*self.rx, self.ry - 1/10*self.ry) 
        qp.drawLine(self.center.x() - self.rx, self.center.y(), self.center.x() + self.rx, self.center.y())
        qp.drawLine(self.center.x(), self.center.y() -self.ry, self.center.x(), self.center.y() + self.ry)
    def drawElectrode(self, qp, center, name):
        pen = QPen(Qt.black, 1, Qt.SolidLine)
        qp.setPen(pen)
        qp.setBrush(Qt.black)
        qp.drawEllipse(center, 5, 5)

        qp.setFont(QFont('Arial', 13))
        qp.setBrush(Qt.black)
        qp.drawText(center.x() - 25,center.y() + 5, 50, 40, Qt.AlignCenter, name)
    def drawLine(self, qp, start, end, width):
        color = self.floatRgb(width, 0, 1)
        pen = QPen(QColor(color[0], color[1], color[2], 255), 3, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(start, end)
    def floatRgb(self, n, cmin, cmax):
        R,G,B = 1.0,1.0,1.0
        if (n < cmin):
            n = cmin
        if (n > cmax):
            n = cmax
        dv = cmax - cmin

        if (n < (cmin + 0.25 * dv)):
            R = 0
            G = 4 * (n - cmin) / dv
        elif (n < (cmin + 0.5 * dv)):
            R = 0
            B = 1 + 4 * (cmin + 0.25 * dv - n) / dv
        elif (n < (cmin + 0.75 * dv)):
            R = 4 * (n - cmin - 0.5 * dv) / dv
            B = 0
        else:
            G = 1 + 4 * (cmin + 0.75 * dv - n) / dv
            B = 0
        
        return R*255,G*255,B*255

