import os

from PyQt5 import QtGui, QtCore, QtWidgets, Qt

try:
    from Katana import UI4

    class ImageBrowserTab(UI4.Tabs.BaseTab):
        def __init__(self, parent=None):
            super(ImageBrowserTab, self).__init__(parent)

            self._layout = QtWidgets.QVBoxLayout(self)
            self._image_browser_widget = ImageBrowser(self)
            self._layout.addWidget(self._image_browser_widget)

except ImportError:
    pass


class ImageBrowser(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super(ImageBrowser, self).__init__(parent)

        # setup contact sheet size attributes
        self._image_size = 100
        self._spacing = 10
        self._image_dir = '/opt/katana/3.5v2/bin/python/UI4/Resources/Icons'

        # set widget to wrap
        self.setFlow(QtWidgets.QListView.LeftToRight)
        self.setResizeMode(QtWidgets.QListView.Adjust)
        self.setWrapping(True)

        # set image size
        self.setGridSize(QtCore.QSize(
            self._image_size + self._spacing, self._image_size + self._spacing)
        )

        # enable multi selection
        self.setSelectionMode(QtWidgets.QListView.MultiSelection)

        # populate
        self.populate()

    def populate(self):
        # get a list of all the files absolute file path in this directory
        image_list = ['/'.join([self._image_dir, image]) for image in os.listdir(self._image_dir)]

        # run through absolute file paths and create a thumbail
        for image in image_list:
            # create base item
            item = QtWidgets.QListWidgetItem()
            image_widget = QtGui.QImage(image)
            if not image_widget.isNull():
                # check width/height and scale to fit our bound
                if image_widget.width() > image_widget.height():
                    image_widget = image_widget.scaledToWidth(self._image_size, QtCore.Qt.FastTransformation)
                else:
                    image_widget = image_widget.scaledToHeight(self._image_size, QtCore.Qt.FastTransformation)

                # set display data
                item.setData(QtCore.Qt.DecorationRole, image_widget)

                # set file path
                # we store it on the ToolTipRole as the QImage does not store the
                # absolute path to the file.  So we will need this in order to recall
                # the file path later.
                item.setData(QtCore.Qt.ToolTipRole, image)

                # add item to the widget
                self.addItem(item)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = ImageBrowser()
    w.show()
    sys.exit(app.exec_())
else:
    PluginRegistry = [("KatanaPanel", 2, "ImageBrowser", ImageBrowserTab)]