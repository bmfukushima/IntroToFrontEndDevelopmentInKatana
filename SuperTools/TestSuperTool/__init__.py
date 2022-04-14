
import Katana
from .Node import TestNode


def GetEditor():
    from .Editor import TestEditor
    return TestEditor


# Register Supertool
PluginRegistry = [("SuperTool", 2, "Test", (TestNode, GetEditor)), ]
