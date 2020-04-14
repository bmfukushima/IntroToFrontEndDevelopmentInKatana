# Copyright (c) 2012 The Foundry Visionmongers Ltd. All Rights Reserved.

from Katana import NodegraphAPI, Utils, UniqueName, DrawingModule


import logging

log = logging.getLogger("Test.Node")


class TestNode(NodegraphAPI.SuperTool):
    """
    The node portion of the SuperTool is responsible for the creation
    of the node.  This could include but not be limited to:
        1.) Port Creation
        2.) Port Connection
        3.) Internal node creation
    """
    def __init__(self):
        self.addOutputPort('out')
        self.addInputPort('in')
        self.getSendPort('in').connect(self.getReturnPort('out'))