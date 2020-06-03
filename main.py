import sys

from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QIcon

from Assets.windows.MainWindow import MainWindow

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    app.setStyle("Fusion") #Apply a modern window style
    
    window = MainWindow()
    window.setWindowIcon(QIcon("Assets/pics/applogo.png")) #Design detail
    window.show() 

    # Run the main Qt loop
    sys.exit(app.exec_())