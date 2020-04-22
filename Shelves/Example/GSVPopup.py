"""
NAME: GSV Popup
ICON: icon.png
KEYBOARD_SHORTCUT: Alt+Shift+Q
SCOPE:
Opens a Graph State Variables editor
"""
from PyQt5 import QtWidgets, QtGui, QtCore

from Katana import UI4, NodegraphAPI

# ----------------------------------------------------------------- create menu
katana_main = UI4.App.MainWindow.CurrentMainWindow()
menu = QtWidgets.QMenu(katana_main)
menu_layout = QtWidgets.QVBoxLayout()
menu.setLayout(menu_layout)

# -------------------------------------------------- set up graph state variables
gsv_param = NodegraphAPI.GetNode('rootNode').getParameter('variables')
param_policy = UI4.FormMaster.CreateParameterPolicy(None, gsv_param)
gsv_widget = UI4.FormMaster.KatanaFactory.ParameterWidgetFactory.buildWidget(
    None, param_policy
)
menu_layout.addWidget(gsv_widget)

# ------------------------------------------------------- menu display settings
# setup transparency
menu.setAttribute(QtCore.Qt.WA_NoSystemBackground | QtCore.Qt.WA_TranslucentBackground)
menu.setWindowFlags(menu.windowFlags() | QtCore.Qt.FramelessWindowHint)
menu.setStyleSheet("background-color:rgba(50,50,50, 128);")
menu.setMinimumWidth(400)

# ---------------------------------------------------------- display and position
# show menu

menu.popup(QtGui.QCursor.pos())
# move menu to center of cursor

menu.move(
    menu.pos().x() - (menu.width() * .5),
    menu.pos().y() - (menu.height() * .5)
)


