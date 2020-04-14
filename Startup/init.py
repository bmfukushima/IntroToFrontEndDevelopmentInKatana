
from Katana import Callbacks


def createMenuItem(**kwargs):
    def actionFunction():
        print ('Hello World!')

    from PyQt5.QtWidgets import QAction
    from PyQt5.QtGui import QIcon

    from Katana import UI4
    katana_main = UI4.App.MainWindow.GetMainWindow()
    icon_path = '/media/ssd01/Katana/dev/resources/IntroToFrontEndDevelopmentInKatana/Icons/katana.png'
    action = QAction(QIcon(icon_path), '&Test', katana_main)
    action.setShortcut('Ctrl+T')
    action.setStatusTip('Hello Menu Item!')
    action.triggered.connect(actionFunction)

    menubar = katana_main.getMenuBar()
    fileMenu = menubar.addMenu('&Test')
    fileMenu.addAction(action)


Callbacks.addCallback(Callbacks.Type.onStartupComplete, createMenuItem)
