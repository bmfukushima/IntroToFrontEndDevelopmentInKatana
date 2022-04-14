from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from Katana import UI4


class TestEditor(QWidget):
    """
    The editor is responsible for what we could consider the PyQt portion
    of our tool.  This could include but not be limited to:
        1.) Widget Layout/Custom Widgets
        2.) Events / Signal processing
    """
    def __init__(self, parent, node):
        super(TestEditor, self).__init__(parent)
        self.__node = node

        # Create Widgets
        label = QLabel('Hello')
        button = QPushButton('World')

        # Create a custom katana parameter widget
        """ This parameter is created in the "Node" file """
        parent = self.node().getParameters()
        locationPolicy = UI4.FormMaster.CreateParameterPolicy(None, parent.getChild("customParam"))
        factory = UI4.FormMaster.KatanaFactory.ParameterWidgetFactory
        custom_parameter_widget = factory.buildWidget(self, locationPolicy)

        # setup layout
        QVBoxLayout(self)
        self.layout().addWidget(label)
        self.layout().addWidget(button)
        self.layout().addWidget(custom_parameter_widget)

    def node(self):
        return self.__node
