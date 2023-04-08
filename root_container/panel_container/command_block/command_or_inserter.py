from data_structures.linked_list import LinkedListNode

class CommandOrInserter(LinkedListNode['CommandOrInserter']):

    def __init__(self, isCommand: bool):
        super().__init__()

        self.isCommand = isCommand

        self.CORNER_RADIUS = 3
        self.dragPosition = None
        self.normalY = 0

    
    # Called when linked list position changes. Update parent and children entity relationships
    def onUpdateLinkedListPosition(self):
        #print("update linked list position", self)
        #print("before:", self._parent, self._children)

        # only replace parent if not the first inserter
        # first inserter has special parent ScrollingContentContainer
        if isinstance(self._parent, CommandOrInserter):
            self._parent = self.getPrevious()

        self._children = [child for child in self._children if not isinstance(child, CommandOrInserter)]
        
        if self.getNext() is not None:
            self._children.append(self.getNext())

        #print("after:", "parent:", self._parent, "children:", self._children)

    # backtrack to find the real target height for this enttiy
    def _getTargetHeight(self):

        current = self
        height = 0
        while isinstance(current._parent, CommandOrInserter):
            if current.isCommand:
                height += current.ACTUAL_HEIGHT
            else:
                height += current.defineHeight()
            current = current._parent
        return height
    