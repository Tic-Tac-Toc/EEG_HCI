from PySide2.QtWidgets import QBoxLayout
from PySide2.QtCore import Qt

#Place an element with the specified alignement (design help function)
def DefineLayoutChildAlignment(layout, alignment):        
    for i in range(layout.count()):
        layout.setAlignment(layout.itemAt(i).widget(), alignment)
    