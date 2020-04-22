from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget

if __name__ is not '__main__':
    from Katana import UI4, NodegraphAPI

class NewTab(QWidget):
#class NewTab(UI4.Tabs.BaseTab):
    def __init__(self, parent=None):
        super(NewTab, self).__init__(parent)
        layout = QVBoxLayout(self)
        button = QPushButton('New Tab')
        button.clicked.connect(self.buttonFun)

        layout.addWidget(button)
        #        self.setCentralWidget(edit)

    def buttonFun(self):
        NodegraphAPI.CreateNode("Group", NodegraphAPI.GetRootNode())

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = NewTab()
    w.show()
    sys.exit(app.exec_())
else:
    from Katana import UI4, NodegraphAPI
    PluginRegistry = [("KatanaPanel", 2, "NewTab", NewTab)]
