from PyQt5.QtWidgets import QVBoxLayout, QPushButton

from Katana import UI4, NodegraphAPI


class NewTab(UI4.Tabs.BaseTab):
    def __init__(self, parent=None):
        super(NewTab, self).__init__(parent)
        layout = QVBoxLayout(self)
        button = QPushButton('New Tab')
        button.clicked.connect(self.buttonFun)

        layout.addWidget(button)
        #        self.setCentralWidget(edit)

    def buttonFun(self):
        NodegraphAPI.CreateNode("Group", NodegraphAPI.GetRootNode())


PluginRegistry = [("KatanaPanel", 2, "NewTab", NewTab)]