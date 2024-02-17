"""
# Maya Custom Shelf Manager

* Description

    A basic shelf manager for adding repo functions to maya shelves.
    Shelves are cleared and rebuilt on maya startup.

* Update History

    `2023-09-21` - Init
"""


import pathlib

import maya.cmds as cmds


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Base Class
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def _null(*args):
    pass


class CustomMayaShelf:
    """
    A simple class to build shelves in Maya.

    Args:
        name(str): The shelf name in Maya.

        icon_path(str): The path containing any custom icon files.
    """
    def __init__(self, name: str = 'customShelf', icon_path: str = ''):
        self.name = name
        self.icon_path = icon_path

        self.label_background = (0, 0, 0, 0.5)
        self.label_color = (0.9, 0.9, 0.9)

        self._clean_old_shelf()
        cmds.setParent(self.name)
        self.build()
        self._last_item_alignment()

    def build(self) -> None:
        """
        This method should be overwritten in derived classes to actually build the shelf
        elements. Otherwise, nothing is added to the shelf.
        """

    def _clean_old_shelf(self) -> None:
        if cmds.shelfLayout(self.name, ex=1):
            if children := (cmds.shelfLayout(self.name, q=1, ca=1)):
                for child in children:
                    cmds.deleteUI(child)
        else:
            cmds.shelfLayout(self.name, p='ShelfLayout')

    def _last_item_alignment(self) -> None:
        """Last item is misaligned for some reason so another button is created and destroyed."""
        self.add_button('delete_me')
        items = cmds.shelfLayout(self.name, q=1, ca=1)
        cmds.deleteUI(items[-1])

    def add_button(self, label: str, icon: str = 'commandButton.png', command=_null, double_command=_null) -> None:
        """Adds a shelf button with the specified label, command, double click command, and image."""
        cmds.setParent(self.name)
        image = pathlib.Path(self.icon_path, icon)
        if not image.exists():
            image = 'commandButton.png'

        cmds.shelfButton(width=40, height=40, image=image, l=label, command=command, dcc=double_command,
                         imageOverlayLabel=label, olb=self.label_background, olc=self.label_color,
                         fn='tinyBoldLabelFont')

    def add_menu_item(self, parent, label, icon: str = '', command=_null):
        """Adds a shelf menu item with the specified label, command, double click command, and image."""
        image = pathlib.Path(self.icon_path, icon)
        if not image.exists():
            image = 'commandButton.png'

        return cmds.menuItem(p=parent, l=label, c=command, i=image)

    def add_sub_menu(self, parent: str, label: str, icon: str = ''):
        """Adds a sub menu item with the specified label, and optional image, to the specified parent popup menu."""
        image = pathlib.Path(self.icon_path, icon).as_posix()
        return cmds.menuItem(p=parent, l=label, i=image, subMenu = 1)

    @staticmethod
    def add_separator(style: str = 'none', height: int = 40, width: int = 16):
        """Adds a separator to space sections of the shelf apart."""
        return cmds.separator(style=style, h=height, w=width)


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Custom Shelves
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def test_func():
    print('hello world')


class ExampleShelf(CustomMayaShelf):
    """Example custom shelf."""
    def __init__(self):
        super().__init__('Example')

    def build(self):
        self.add_button('Hello\nWorld', command=test_func)
        self.add_separator()
        self.add_button('Sub\nMenus')
        menu1 = cmds.popupMenu(b=1)
        self.add_menu_item(menu1, 'You')
        self.add_menu_item(menu1, 'Lost')
        submenu1 = self.add_sub_menu(menu1, 'The')
        self.add_menu_item(submenu1, 'Game')


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Main block
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def main():
    ExampleShelf()
