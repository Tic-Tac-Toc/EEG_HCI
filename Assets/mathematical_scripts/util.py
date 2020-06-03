import xlrd #Read excel files
import xlsxwriter #Write excel files
import numpy as np
import os
from scipy.signal import butter, lfilter #Allow to deal with signal functions
import glob #Search file on directory
import scipy.io as sp #Load matlab file

fs = 100.0 #Common sampling frequency
waves = {} #Dictionnary with waves range value
waves['alpha'] = [8, 12]
waves['beta'] = [12, 25]
waves['theta'] = [4, 8]
waves['delta'] = [1, 4]
directories = ['Active', 'Control', 'Death']

#Function which order to write signal in txt format for each wave type (separator = space)
def WriteSignal(filename, electrode, wbname, directories, x, y): #wbname = workbook name
    separator = " "
    if not os.path.isdir('./Datas/'+ directories + '/' + wbname):
        os.mkdir('./Datas/'+ directories + '/' + wbname)
    if not os.path.isdir('./Datas/'+ directories + '/' + wbname+ '/' + electrode):
        os.mkdir('./Datas/'+ directories + '/' + wbname + '/' + electrode)

    fichier = open('./Datas/'+ directories + '/' + wbname + '/' + electrode + '/' + filename, 'w')
    for i in range(len(x)):
        fichier.write(str(x[i]) + separator + str(y[i]) + '\n')
    fichier.close()

    print('File created : /Datas/'+ directories + '/' + wbname + '/' + electrode + '/' + filename)
#Function which order to write PSC Matrix after calcul (deprecated since we use matlab matrix)
def WriteMatrix(filename, wbname, directory, m):
    if not os.path.isdir('./Datas/PSC Matrix/'+ directory + '/' + wbname):
        os.mkdir('./Datas/PSC Matrix/'+ directory + '/' + wbname)
    fichier = open('./Datas/PSC Matrix/'+ directory + '/' + wbname + '/' + filename, 'w')

    for i in range(len(m)):
        for j in range(len(m)):    
            fichier.write(str(m[i][j]) + " ")
        fichier.write('\n')
    
    fichier.close()
    
    print('File created : ./Datas/PSC Matrix/'+ directory + '/' + wbname + '/' + filename)

#Function which order to write wave signal from patient raw signal
def WriteWavesPatient(filename, wbname, directory, datas, electrode_names):
    wbname = wbname.split('.')[0]
    if not os.path.isdir('./Datas/'+ directory + '/' + wbname):
        os.mkdir('./Datas/'+ directory + '/' + wbname)

    fichier = open('./Datas/'+ directory + '/' + wbname + '/' + filename, 'w')

    #Write column header (electrode names)
    for elm in electrode_names:
            fichier.write(elm + " ")
    fichier.write('\n')

    #Write values
    for i in range(len(datas[0])):
        for j in range(len(datas)):
            fichier.write(str(datas[j][i]) + " ")
        fichier.write('\n')
    fichier.close()
    
    print('File created : ./Datas/'+ directory + '/' + wbname + '/' + filename)

#Couple of functions to load & custom waves range
def WriteWavesRange():   
    fichier = open('./Datas/waves_range.txt', 'w')
    for wave in waves: 
        fichier.write(wave + " " + str(waves[wave][0]) + " " + str(waves[wave][1]) + "\n")
    fichier.close()

    print('File created : ./Datas/waves_range.txt')
def LoadWavesRange():
    file = open('./Datas/waves_range.txt', "r")
    lines = file.readlines()
    file.close()

    for line in lines:
        datas = line.replace('\n','').split(' ')
        waves[datas[0]][0] = int(datas[1])
        waves[datas[0]][1] = int(datas[2])

#Multiple functions to handle the order of electrodes (20/30 etc)
def WriteElectrodesOrder(electrodes):
    fichier = open('./Datas/electrodes_order.txt', 'w')

    for i in range(len(electrodes)):
        fichier.write(str(electrodes[i]) + "\n")
    
    fichier.close()
    
    print('File created : ./Datas/electrodes_order.txt')
def getElectrodesId(electrode):
    electrodes = []

    file = open('./Datas/electrodes_order.txt', "r")
    lines = file.readlines()
    file.close()

    for line in lines:
        electrodes.append(str(line.replace('\n','').replace(' ','')))
    
    return electrodes.index(str.upper(electrode)) #Find electrode ID by its index on the list
def getElectrodesList():
    electrodes = []

    file = open('./Datas/electrodes_order.txt', "r")
    lines = file.readlines()
    file.close()

    for line in lines:
        electrodes.append(str(line.replace('\n','').replace(' ','')))
    
    return electrodes

#Trim empty axs to improve plot display
def trim_axs(axs, N):
    """
    Reduce *axs* to *N* Axes. All further Axes are removed from the figure.
    """
    axs = axs.flat
    for ax in axs[N:]:
        ax.remove()
    return axs[:N]

#Function to apply filter to the raw signal (especially to create wave subsignal)
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a
def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y
def bandpassFilter(wave, data):
    lowcut = waves[wave][0]
    highcut = waves[wave][1]
    
    y = butter_bandpass_filter(data, lowcut, highcut, fs)
    return y

#Load datas from file (xslx or .mat) 
#.mat Matrix have a specified format : Key 'epochTime' for time, 'epochRange' for electrode value. 
#epochTime[0][i], i -> epochNumber.
#epochRange[0][i][j], j -> electrodeid or line of the electrode in electrode_order.txt file.
def getRawDatasXSLX(wbname, directories, electrode):
    workbook = xlrd.open_workbook('./Datas/Raw/'+ directories + '/' + wbname)
    worksheets = workbook.sheets()
            
    x, y = [], []
    for worksheet in worksheets:
        if (worksheet.name != "Plan11"):
            values = worksheet.row(electrode)
            time = worksheet.row(worksheet.nrows - 1)
            for i in range(len(values)):
                if i != 0:
                    y.append(values[i].value)
                    x.append(time[i].value)
                else:
                    electrode_name = values[i].value
    return x,y, electrode_name
def getRawDatas(wbname, directories, electrode):
    mat = sp.loadmat('./Datas/Raw/'+ directories + '/' + wbname)
    x, y = [], []
    for i in range(len(mat["epochTime"][0])):
        values = mat["epochRange"][0][i][electrode]
        time = mat["epochTime"][0][i][0]
        for j in range(len(values)):
            x.append(time[j])
            y.append(values[j])
    electrode_name = mat['nameChannel'][electrode][0][0]
    return x, y, electrode_name

#Allow user to custom waves frequency range et rewrite wave signal
def createWaveFilePatientXSLX(wbname, directory, wave):
    m = []
    electrode_names = ['t']
    electrode_number = len(getElectrodesList())
    for i in range(electrode_number): #Parcourir les electrodes
        datas = getWaveDataByElectrode(wbname, directory, wave, i)
        if (i == 0):
            m.append(datas[0])
        m.append(datas[1])
        electrode_names.append(datas[2])
    WriteWavesPatient("m_" + wave + ".txt", wbname, directory, m, electrode_names)
def createWaveFilePatientMAT(wbname, directory, wave):
    m = []
    electrode_names = ['t']
    electrode_number = len(getElectrodesList())
    for i in range(electrode_number): #Parcourir les electrodes
        datas = getWaveDataByElectrodeMAT(wbname, directory, wave, i)
        if (i == 0):
            m.append(datas[0])
        m.append(datas[1])
        electrode_names.append(datas[2])
    WriteWavesPatient("m_" + wave + ".txt", wbname, directory, m, electrode_names)
def getWaveDataByElectrode(wbname, directories, wave, electrode):
    time, data, electrode_name = getRawDatasXSLX(wbname, directories, electrode)    
    select_wave = bandpassFilter(wave, data)

    return [time, select_wave, electrode_name]
def getWaveDataByElectrodeMAT(wbname, directories, wave, electrode):
    time, data, electrode_name = getRawDatas(wbname, directories, electrode)    
    select_wave = bandpassFilter(wave, data)

    return [time, select_wave, electrode_name]

#Create waves files if a matlab matrix is added.
def CheckIfFilesAllCreated():
    for d in directories:
        filesmat = [file.split('\\')[-1] for file in glob.glob('./Datas/Raw/'+ d +'/' + '*.mat')]
        for file in filesmat:
            if not os.path.isdir('./Datas/'+ d + '/' + file.split('.')[0]):
                for wave in waves.keys():
                    createWaveFilePatientMAT(file, d, wave)

LoadWavesRange() #Load Waves Range at startup
CheckIfFilesAllCreated() #Check at startup if there is no new matrix to handle
