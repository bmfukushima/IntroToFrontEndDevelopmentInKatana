from Katana import Callbacks

import logging


def createGSV(**kwargs):
    import os

    import NodegraphAPI
    options = os.environ['SHOTLIST'].split(';')

    # get GSV group param
    gsv_parm = NodegraphAPI.GetRootNode().getParameter('variables')

    # delete the GSV if it exists
    try:
        gsv_parm.deleteChild(gsv_parm.getChild('shot'))
    except TypeError:
        # exception for if the child does not exist
        pass
    # create GSV
    shot_gsv = gsv_parm.createChildGroup('shot')

    # set param flag to enabled
    shot_gsv.createChildNumber('enable', 1)

    # create GSV options
    shot_gsv.createChildString('value', options[0])
    optionsParam = shot_gsv.createChildStringArray('options', len(options))
    for optionParam, optionValue in zip(optionsParam.getChildren(), options):
            optionParam.setValue(optionValue, 0)


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


def contextMenu(**kwargs):
    from Katana import NodegraphAPI
    from UI4.FormMaster.NodeActionDelegate import (BaseNodeActionDelegate, RegisterActionDelegate)
    from UI4.Manifest import QtWidgets

    class UpdateGSVOptions(BaseNodeActionDelegate.BaseNodeActionDelegate):
        class _addAllGSVOptions(QtWidgets.QAction):
            def __init__(self, parent, node):
                # set node to private attribute
                self.__node = node

                # set menu display text
                var_name = self.__node.getParameter('variableName').getValue(0)
                QtWidgets.QAction.__init__(self, 'Add all GSV options for %s'%var_name, parent)

                # connect signal
                if node:
                    self.triggered.connect(self.__triggered)

                self.setEnabled(self.__node is not None
                                and not self.__node.isLocked(True))

            def __triggered(self):
                # get node data
                variable_switch = self.__node
                variable_name = variable_switch.getParameter('variableName').getValue(0)
                variable_patterns_parm = variable_switch.getParameter('patterns')
                gsv_parm = NodegraphAPI.GetNode('rootNode').getParameter('variables.%s'%variable_name)

                if gsv_parm:
                    # delete previous ports and patterns
                    # remove all input ports
                    for port in variable_switch.getInputPorts():
                        variable_switch.removeInputPort(port.getName())
                    # remove all child parameters
                    for child in variable_patterns_parm.getChildren():
                        variable_patterns_parm.deleteChild(child)

                    for child in gsv_parm.getChild('options').getChildren():
                        # create new port with pattern
                        name = child.getValue(0)
                        # mechanic on the variable switch will automagically create the
                        # parameters when you create the port
                        variable_switch.addInputPort(name)

        def addToContextMenu(self, menu, node):
            menu.addAction(self._addAllGSVOptions(menu, node))

    RegisterActionDelegate("VariableSwitch", UpdateGSVOptions())


Callbacks.addCallback(Callbacks.Type.onStartupComplete, contextMenu)
Callbacks.addCallback(Callbacks.Type.onStartupComplete, createGSV)
Callbacks.addCallback(Callbacks.Type.onSceneLoad, createGSV)
Callbacks.addCallback(Callbacks.Type.onStartupComplete, createMenuItem)