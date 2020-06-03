from PySide2.QtWidgets import (QHBoxLayout, QSizePolicy, QWidget)

import os

from Assets.mathematical_scripts.util import getElectrodesList

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import scipy.io as sp
import seaborn as sns

class HeatMapWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.setWindowTitle("Heatmap")

        # QWidget Layout
        self.main_layout = QHBoxLayout()
        self.size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)   
        
        # generate the plot
        self.fig, self.ax = plt.subplots()
        self.fig.tight_layout = True
        self.fig.subplots_adjust(left=0.10, right=0.90, top=0.90, bottom=0.10)
        self.ax.margins(0,0)
        self.canvas = FigureCanvas(self.fig)       

        ## Main Layout
        self.size.setHorizontalStretch(4)
        self.canvas.setSizePolicy(self.size)
        self.main_layout.addWidget(self.canvas)

        # Set the layout to the QWidget
        self.setLayout(self.main_layout)

    def Load(self, wbname, directory, wave):
        # generate heatmap
        filename = 'matrix_PSC_' + directory + '_' + wbname + '_' + wave
        mat = sp.loadmat('./Datas/PSC Matrix/'+ directory + '/' + wave + '/' + filename + '.mat')
        M = mat['PSC']
        sns.heatmap(M, cmap="jet", yticklabels=False, xticklabels=getElectrodesList(), vmin=0, vmax=1)
        self.ax.set_title("Heatmap for synchronization " + wave + " waves for " + directory + ":" + wbname)
        self.ax.set_xlabel("Electrodes")
        self.ax.set_ylabel("Synchronization between electrodes")    
        # generate the canvas to display the plot  
        self.canvas.draw()
        self.canvas.flush_events()