from PyQt5 import QtWidgets, QtCore

from Katana import NodegraphAPI, RenderingAPI, LayeredMenuAPI, UI4, Utils


def PopulateCallback(layeredMenu):
    """
    The populate call back is given to the layeredMenu as an argument.  This
    function will determine what options are displayed to the user when the user
    displays the layered menu.
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
    """
    The ActionCallback is given to the LayeredMenu as an argument.  This function
    will determine what should happen when the user selects an option in the
    LayeredMenu.
    """
    # flip display flag
    display_flag = getGSVDisplayFlag()
    if display_flag is True:
        # set flags to allow recursion through menus
        setGSV(value)
        setGSVDisplayFlag(not display_flag)

        """
        hacky force update on the nodegraph tabs layer stack

        This is going to log an error, as we're manually removing the layer from the GL
        layer stack, and Katana will do this again during cleanup.
        """
        node_graph = UI4.App.Tabs.FindTopTab('Node Graph').getNodeGraphWidget()
        layer_stack = node_graph._NodegraphWidget__nodeGraphViewInteractionLayer.layerStack()
        last_layer = layer_stack.getLayers()[-1]
        node_graph._NodegraphWidget__nodeGraphViewInteractionLayer.layerStack().removeLayer(last_layer)
        # layer_stack.setGraphInteraction(True)

        global gsvMenu
        node_graph.showLayeredMenu(gsvMenu)
        return
    else:
        setGSVDisplayFlag(not display_flag)
        gsv_parm = NodegraphAPI.GetNode('rootNode').getParameter('variables')
        if display_flag is False:
            gsv_name = getGSV()
            gsv_parm = gsv_parm.getChild('%s.value'%gsv_name)
            gsv_parm.setValue(value, 0)

    return value


def getGSVDisplayFlag():
    """
    False = display options for a specific GSV
    True = display all GSVs
    """
    katana_main = UI4.App.MainWindow.CurrentMainWindow()
    if not hasattr(katana_main, 'layered_menu_gsv_display_flag'):
        katana_main.layered_menu_gsv_display_flag = True
    display_flag = katana_main.layered_menu_gsv_display_flag
    return display_flag


def setGSVDisplayFlag(flag):
    katana_main = UI4.App.MainWindow.CurrentMainWindow()
    katana_main.layered_menu_gsv_display_flag = flag


def getGSV():
    """
    stores the current GSV name as a string
    """
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

LayeredMenuAPI.RegisterLayeredMenu(gsvMenu, 'gsv')

