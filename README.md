# Maya Shelf
A simple maya shelf manager

<img src="https://i.imgur.com/AfQDLau.png" alt="ui"/>

## Getting Started

### Install as Module
You can install the module from the repo with:
```bash
pip install git+https://github.com/nate-maxwell/Maya_Shelf
```

### Creating a Shelf
Creating a shelf will add a shelf to maya's shelf section and then add each item.
If a shelf exists with the given name, it will be emptied and filled with the items
implemented in the custom shelf class.

You can create a shelf with the following code:
```python
from mayashelf.shelves import CustomMayaShelf
import my.func.lib


class ExampleShelf(CustomMayaShelf):
    """Example custom shelf."""
    def __init__(self):
        super().__init__('Example')

    def build(self):
        self.add_button('Hello\nWorld', command=my.func.lib.function)
        self.add_separator()
        self.add_button('Sub\nMenus')
        menu1 = self.add_popup_menu()
        self.add_menu_item(menu1, 'You')
        self.add_menu_item(menu1, 'Lost')
        submenu1 = self.add_sub_menu(menu1, 'The')
        self.add_menu_item(submenu1, 'Game')


def main():
    ExampleShelf()
    # And any other shelves you make.
```

Then, in your maya userSetup.py file, simply call the command that creates your shelves:
```python
import maya.cmds as cmds
import my.custom.shelf.lib

# Call our function to generate shelves.
cmds.evalDeferred(my.custom.shelf.lib.main, lowestPriority=True)
```

And that's it!
