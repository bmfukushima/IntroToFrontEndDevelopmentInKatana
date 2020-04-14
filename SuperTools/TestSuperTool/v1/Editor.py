from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout


class TestEditor(QWidget):
    """
    The editor is responsible for what we could consider the PyQt portion
    of our tool.  This could include but not be limited to:
        1.) Widget Layout/Custom Widgets
        2.) Events / Signal processing
    """
    def __init__(self, parent, node):
        super(TestEditor, self).__init__(parent)
        layout = QVBoxLayout(self)
        label = QLabel('Hello')
        button = QPushButton('World')
        layout.addWidget(label)
        layout.addWidget(button)
        self.__node = node

