from PyQt5 import QtWidgets

from Katana import UI4


# Create Tab
class HelloTab(UI4.Tabs.BaseTab):
    """
    Hello world example of creating a tab in Katana.
    """
    def __init__(self, parent=None):
        super(HelloTab, self).__init__(parent)

        # create widgets
        layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel('Hello Tab')

        # setup layout
        self.setLayout(layout)
        layout.addWidget(label)


# Register plugin
PluginRegistry = [("KatanaPanel", 2, "ImageBrowser", HelloTab)]
