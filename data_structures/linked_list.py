from typing import TypeVar, Generic
from entity_base.entity import Entity

T = TypeVar('T')
class LinkedListNode(Generic[T]):
    def __init__(self):
        self._next: T | LinkedListNode | Entity = None
        self._prev: T | LinkedListNode | Entity = None

    def getPrevious(self) -> T | 'LinkedListNode':
        return self._prev
    
    def getNext(self) -> T | 'LinkedListNode':
        return self._next
    
    # override this
    def onUpdateLinkedListPosition(self):
        pass

class LinkedList(Generic[T]):
    def __init__(self):
        self.head: LinkedListNode | T = None
        self.tail: LinkedListNode | T = None

    def addToBeginning(self, node: LinkedListNode):
        
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            node._next = self.head
            self.head._prev = node
            self.head = node
            node._next.onUpdateLinkedListPosition()
        node.onUpdateLinkedListPosition()

    def addToEnd(self, node: LinkedListNode):

        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail._next = node
            node._prev = self.tail
            self.tail = node
            node._prev.onUpdateLinkedListPosition()
        node.onUpdateLinkedListPosition()

    def insertBeforeEnd(self, node: LinkedListNode):
        self.insertBefore(self.tail, node)

    def insertBefore(self, node: LinkedListNode, newNode: LinkedListNode):

        if self.head is None:
            return
        if self.head is node:
            self.addToBeginning(newNode)
            return
                
        newNode._prev = node._prev
        node._prev._next = newNode
        newNode._next = node
        node._prev = newNode

        newNode._prev.onUpdateLinkedListPosition()
        newNode.onUpdateLinkedListPosition()
        newNode._next.onUpdateLinkedListPosition()

    def insertAfter(self, node: LinkedListNode, newNode: LinkedListNode):

        if self.tail is node or node is None:
            self.addToEnd(newNode)
            return
        
        self.printList()
        print(node)
        assert(self.contains(node))

        newNode._next = node._next
        node._next._prev = newNode
        node._next = newNode
        newNode._prev = node

        newNode._prev.onUpdateLinkedListPosition()
        newNode.onUpdateLinkedListPosition()
        newNode._next.onUpdateLinkedListPosition()

    def remove(self, node: LinkedListNode):

        if self.head is self.tail:
            self.head = None
            self.tail = None
        elif self.head is node:
            self.head = self.head._next
            self.head._prev = None
            self.head.onUpdateLinkedListPosition()
        elif self.tail is node:
            self.tail = self.tail._prev
            self.tail._next = None
            self.tail.onUpdateLinkedListPosition()
        else:
            node._prev._next = node._next
            node._next._prev = node._prev
            node._prev.onUpdateLinkedListPosition()
            node._next.onUpdateLinkedListPosition()

    def contains(self, node: LinkedListNode):
        current = self.head
        while current is not None:
            if current is node:
                return True
            current = current.getNext()
        return False

    def printList(self):
        current = self.head
        while current is not None:
            print(current)
            current = current._next

        print()