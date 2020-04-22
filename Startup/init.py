from Katana import Callbacks


def createMenuItem(**kwargs):
    # create file browser
    def openFileBrowser():
        def openFile():
            """
            This function is run when the user presses the "Accept" button in the dialog
            """
            file_path = browser.getResult()
            KatanaFile.Load(file_path)
            print('opening {}'.format(file_path))

        # create the asset browser widget
        dialog = AssetBrowser.Browser.BrowserDialog()
        dialog.addFileBrowserTab()

        # set up the initial path
        path = '/media/ssd01/Katana/dev/IntroToFrontEndDevelopmentInKatana/Scenes/'
        browser = dialog.getCurrentBrowser()
        browser.setLocation(path)

        # connect the accepted signal
        dialog._BrowserDialog__buttons.accepted.connect(openFile)

        # display the asset browser widget
        dialog.open()

        # create a dummy attr on the main instance to ensure that our widget
        # is not garbage collected
        katana_main = UI4.App.MainWindow.GetMainWindow()
        katana_main.dummy = dialog

    from PyQt5.QtWidgets import QAction
    from PyQt5.QtGui import QIcon

    from Katana import UI4, KatanaFile, AssetBrowser
    # create menu entry
    katana_main = UI4.App.MainWindow.GetMainWindow()
    menubar = katana_main.getMenuBar()
    fileMenu = menubar.addMenu('&Custom Menu')

    # create action in menu ( the clickable item in the menu )
    icon_path = '/media/ssd01/Katana/dev/resources/IntroToFrontEndDevelopmentInKatana/Icons/katana.png'
    action = QAction(QIcon(icon_path), '&Load Template', katana_main)

    # set up extra attributes on action
    action.setShortcut('Ctrl+T')
    action.setStatusTip('Loads a template')

    # connect action signal to our custom file browser
    action.triggered.connect(openFileBrowser)

    # add action to the menu
    fileMenu.addAction(action)


Callbacks.addCallback(Callbacks.Type.onStartupComplete, createMenuItem)