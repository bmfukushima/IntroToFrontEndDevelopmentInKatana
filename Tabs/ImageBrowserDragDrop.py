import os

from PyQt5 import QtGui, QtCore, QtWidgets

try:
    from Katana import UI4, NodegraphAPI, CatalogAPI

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
        katana_root = os.environ["KATANA_ROOT"]
        self._image_dir = f'{katana_root}/bin/python/UI4/Resources/Icons'

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
        self.setDragEnabled(True)
        # populate
        self.populate()

    def populate(self):
        # get a list of all the files absolute file path in this directory
        image_list = ['/'.join([self._image_dir, image]) for image in os.listdir(self._image_dir) if os.path.isfile('/'.join([self._image_dir, image]))]

        # run through absolute file paths and create a thumbail
        for image in image_list:
            # create base item
            item = QtWidgets.QListWidgetItem()
            image_widget = QtGui.QImage(image)

            # check width/height and scale to fit our bound
            if not image_widget.isNull():
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

    """ SET UP DRAG / DROP EVENT """
    def setupEventFilter(self):
        """
        Installs an event filter on all monitor tabs and allows them
        to accept drops
        """
        monitor_tabs = UI4.App.Tabs.GetTabsByType('Monitor')
        for monitor in monitor_tabs:
            widget = monitor.getMonitorWidget()
            widget.removeEventFilter(self)
            widget.installEventFilter(self)
            widget.setAcceptDrops(True)

    def startDrag(self, *args, **kwargs):
        """
        When a user starts dragging an item, we install all
        of the event filters.  This is to ensure that all current
        Monitor widgets have this event filter installed.
        """
        self.setupEventFilter()
        return QtWidgets.QListWidget.startDrag(self, *args, **kwargs)

    def eventFilter(self, obj, event, *args, **kwargs):
        if event.type() in (
            QtCore.QEvent.DragEnter,
            QtCore.QEvent.DragMove,
            QtCore.QEvent.Drop
        ):
            if event.type() != QtCore.QEvent.Drop:
                # drag enter/drag move
                event.acceptProposedAction()
            else:
                # drop
                for item in self.selectedItems():
                    # print(dir(item))
                    file_path = str(item.data(QtCore.Qt.ToolTipRole))
                    file_name = str(file_path.split('/')[-1].split('.')[0])

                    # create nodes
                    catalog_item = CatalogAPI.CreateCatalogItem()
                    catalog_item.setDiskImageLocation(file_path, ('primary', 'main'))
                    catalog_item.setNodeName(file_name)
                    catalog_item.setPersistant(True)

                    # set the catalog_item as the viewed catalog_item
                    obj.parentWidget()._MonitorPanel__catalogWidgetA_catalogItemDropped_CB(catalog_item)

                    item.setSelected(False)

            return True
        return QtWidgets.QListWidget.eventFilter(self, obj, event, *args, **kwargs)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = ImageBrowser()
    w.show()
    sys.exit(app.exec_())
else:
    PluginRegistry = [("KatanaPanel", 2, "ImageBrowserDragDrop", ImageBrowserTab)]