# Copyright (c) 2012 The Foundry Visionmongers Ltd. All Rights Reserved.

import Katana
import v1 as Test

if Test:
    PluginRegistry = [
        ("SuperTool", 2, "Test",
                (Test.TestNode,
                        Test.GetEditor)),
    ]
