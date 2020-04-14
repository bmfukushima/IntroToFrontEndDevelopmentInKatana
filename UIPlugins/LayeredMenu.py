from PyQt5 import QtWidgets, QtCore

from Katana import NodegraphAPI, RenderingAPI, LayeredMenuAPI, UI4, Utils


def PopulateCallback(layeredMenu):
    for x in range(100):
        layeredMenu.addEntry(str(x), text=str(x), color=(x*.01, 0, 0))


def ActionCallback(value):
    print(value)
    return value


layeredMenu = LayeredMenuAPI.LayeredMenu(
    PopulateCallback,
    ActionCallback,
    't', alwaysPopulate=True,
    onlyMatchWordStart=False
)
LayeredMenuAPI.RegisterLayeredMenu(layeredMenu, 'Test')
