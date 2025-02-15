from __future__ import annotations
from typing import TYPE_CHECKING
from common.draw_order import DrawOrder

from data_structures.observer import Observable
if TYPE_CHECKING:
    from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity


from command_creation.command_definition import CommandDefinition
from entity_base.container_entity import Container
from abc import ABC, abstractmethod

class AbstractElementsContainer(Container, ABC, Observable):
    
    def __init__(self, parentCommand: CommandBlockEntity, commandDefinition: CommandDefinition, pathAdapter: PathAdapter):
        
        super().__init__(parentCommand, drawOrder = DrawOrder.COMMAND_ELEMENTS)
        self.parentCommand = parentCommand
        self.commandDefinition = commandDefinition

    def getOpacity(self) -> float:
        return self.parentCommand.getAddonsOpacity()
    
    def defineCenterX(self) -> float:
        return self._px(0.5)
    
    def defineCenterY(self) -> float:
        midpoint = (self.parentCommand.ACTUAL_COLLAPSED_HEIGHT + self.parentCommand.ACTUAL_EXPANDED_HEIGHT) / 2
        return self._py(0) + midpoint
    
    @abstractmethod
    def getGeneratedText(self) -> str:
        pass