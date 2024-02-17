"""
# Maya User Setup

* Description

    User setup file regenerating shelves.

* Update History

    `2023-09-21` - Init
"""


import maya.cmds as cmds

import shelves


cmds.evalDeferred(shelves.main, lowestPriority=True)
