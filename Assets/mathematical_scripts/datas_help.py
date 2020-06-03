import pandas as pd

#Function to load matrix created by application (separator = space)
def getRawDatas(wbname, directory, wave):
    M = pd.read_csv('./Datas/'+ directory + '/' + wbname + '/' + 'm_' + wave + '.txt', sep=" ", header=0)
    return M