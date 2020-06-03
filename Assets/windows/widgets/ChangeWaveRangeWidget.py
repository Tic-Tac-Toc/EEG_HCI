from PySide2.QtWidgets import (QHBoxLayout, QProgressBar, QLabel, QWidget)

from Assets.mathematical_scripts.util import createWaveFilePatientXSLX, createWaveFilePatientMAT

import threading

#wavesToUpdate is an array contains the wave which have new range, other will not change.
class ChangeWaveRangeWidget(QWidget):
    def __init__(self, wavesToUpdate):
        QWidget.__init__(self) 

        self.setWindowTitle("Change range - EEG IHM")

        self.waves = wavesToUpdate
        WriteWavesRange() #Save the new range for next use

        self.layout = self.CreateLayout() 
        self.setLayout(self.layout)

        threading.Thread(target=self.createWavesAlphaBetaThetaDelta, daemon=True).start() #Launch the function in another thread to avoid GUI freezing

    def CreateLayout(self):
        layout = QHBoxLayout()

        self.progressBar = QProgressBar(self)
        layout.addWidget(self.progressBar)
        self.progressLabel = QLabel("0")
        layout.addWidget(self.progressLabel)
        layout.addWidget(QLabel("%"))

        return layout

    #Create new wave file with new range
    def createWavesAlphaBetaThetaDelta(self):
        n = 0
        for d in directories:
            filesxslx = [file.split('\\')[-1] for file in glob.glob('./Datas/Raw/'+ d +'/' + '*.xlsx')] #take only files with xlsx extension
            filesmat = [file.split('\\')[-1] for file in glob.glob('./Datas/Raw/'+ d +'/' + '*.mat')] #take only files with mat extension
            for file in filesxslx:
                for wave in self.waves:
                    n += 1
                    createWaveFilePatientXSLX(file, d, wave)
                    progress = round(n / (len(directories) * (len(files) + len(filesmat))  * len(self.waves)), 2) * 100
                    self.progressBar.setValue(progress)
                    self.progressLabel.setText(str(progress))
            for file in filesmat:
                for wave in self.waves:
                    n += 1
                    createWaveFilePatientMAT(file, d, wave)
                    progress = round(n / (len(directories) * (len(files) + len(filesmat))  * len(self.waves)), 2) * 100
                    self.progressBar.setValue(progress)
                    self.progressLabel.setText(str(progress))

        self.close()
