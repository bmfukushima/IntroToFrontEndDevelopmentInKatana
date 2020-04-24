"""
appears to be stuck on a gl drawing layer?
    - potentially call a second layered menu?
    - check showLayeredMenu() function manually?


"""

from PyQt5 import QtWidgets, QtCore

from Katana import NodegraphAPI, RenderingAPI, LayeredMenuAPI, UI4, Utils


def PopulateCallback(layeredMenu):
    """
    flags...
        display all gsvs
            vs
        display all options for a specific gsv

        which gsv to display options for
    """
    display_flag = getGSVDisplayFlag()
    gsv_parm = NodegraphAPI.GetNode('rootNode').getParameter('variables')
    if display_flag is False:
        gsv_name = getGSV()
        gsv_entry = gsv_parm.getChild('%s.options'%gsv_name)
        for child in gsv_entry.getChildren():
            layeredMenu.addEntry(str(child.getValue(0)), text=str(child.getValue(0)), color=(128, 0, 128))
    else:
        for child in gsv_parm.getChildren():
            layeredMenu.addEntry(str(child.getName()), text=str(child.getName()), color=(0, 128, 128))


def ActionCallback(value):
    # flip display flag
    display_flag = getGSVDisplayFlag()
    if display_flag is True:
        # set flags to allow recursion through menus
        setGSV(value)
        setGSVDisplayFlag(not display_flag)

        # hacky force update on the nodegraph tabs layer stack
        ng = UI4.App.Tabs.FindTopTab('Node Graph')
        f = ng.getNodeGraphWidget()
        layer_stack = f._NodegraphWidget__nodeGraphViewInteractionLayer.layerStack()
        last_layer = layer_stack.getLayers()[-1]
        f._NodegraphWidget__nodeGraphViewInteractionLayer.layerStack().removeLayer(last_layer)
        # layer_stack.setGraphInteraction(True)

        global gsvMenu
        f.showLayeredMenu(gsvMenu)
        return
    else:
        setGSVDisplayFlag(not display_flag)
        gsv_parm = NodegraphAPI.GetNode('rootNode').getParameter('variables')
        if display_flag is False:
            gsv_name = getGSV()
            gsv_parm = gsv_parm.getChild('%s.value'%gsv_name)
            gsv_parm.setValue(value, 0)
        #print(value)
    return value

# False = display options for a specific GSV
# True = display all GSVs
def getGSVDisplayFlag():
    katana_main = UI4.App.MainWindow.CurrentMainWindow()
    if not hasattr(katana_main, 'layered_menu_gsv_display_flag'):
        katana_main.layered_menu_gsv_display_flag = True
    display_flag = katana_main.layered_menu_gsv_display_flag
    return display_flag


def setGSVDisplayFlag(flag):
    katana_main = UI4.App.MainWindow.CurrentMainWindow()
    katana_main.layered_menu_gsv_display_flag = flag


def getGSV():
    katana_main = UI4.App.MainWindow.CurrentMainWindow()
    layered_menu_gsv = katana_main.layered_menu_gsv
    return layered_menu_gsv


def setGSV(gsv):
    katana_main = UI4.App.MainWindow.CurrentMainWindow()
    katana_main.layered_menu_gsv = gsv


gsvMenu = LayeredMenuAPI.LayeredMenu(
    PopulateCallback,
    ActionCallback,
    'T',
    alwaysPopulate=True,
    onlyMatchWordStart=False
)
"""
#def populateGSVOptions(layeredMenu):
gsvOptionsLayeredMenu = LayeredMenuAPI.LayeredMenu(
    PopulateCallback,
    ActionCallback,
    'Ctrl+Alt+Shift+L',
    alwaysPopulate=True,
    onlyMatchWordStart=False
)
"
self.layerStack().idleUpdate()
ng = UI4.App.Tabs.FindTopTab('Node Graph')
f = ng.getNodeGraphWidget()

f._NodegraphWidget__nodeGraphViewInteractionLayer.layerStack().idleUpdate()
layer_stack = f._NodegraphWidget__nodeGraphViewInteractionLayer.layerStack()
layer_stack.setGraphInteraction(True)
layer_stack.getLayers()

self.layerStack().removeLayer(self)

ng = UI4.App.Tabs.FindTopTab('Node Graph')
f = ng.getNodeGraphWidget()
f.setGraphInteraction(True)
i = f._NodegraphWidget__nodeInteractionLayer.setEnabled(False)
print(i.setInteractive(False))
for x in dir(f):
    if 'nodeInter' in x:
        print x
f.clearFocus()
"""
LayeredMenuAPI.RegisterLayeredMenu(gsvMenu, 'gsv')
#LayeredMenuAPI.RegisterLayeredMenu(gsvOptionsLayeredMenu, 'gsvOptions')
#layered_menu = GSVMenu(PopulateCallback, ActionCallback, 'T')

