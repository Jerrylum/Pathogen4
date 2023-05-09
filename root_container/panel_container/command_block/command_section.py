from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from root_container.panel_container.command_block.command_sequence_handler import CommandSequenceHandler
    from root_container.panel_container.tab.block_tab_contents_container import BlockTabContentsContainer


from entity_base.container_entity import Container
from entity_ui.group.variable_group.variable_group_container import VariableGroupContainer
import pygame

"""
A command section holds command blocks. Its usefulness lies in being able to
expand and collapse command sections, as well as show or hide the path section
pertaining to the command section.
"""

class CommandSection(Container):

    def __init__(self, parent: BlockTabContentsContainer, handler: CommandSequenceHandler):

        super().__init__(parent = parent)
    
        self.handler = handler
        self.vgc = VariableGroupContainer(parent = parent,
                         isHorizontal = False,
                         innerMargin = 2,
                         outerMargin = 2,
                         name = "section")
        
        # initialize first inserter inside command section
        inserterVariableContainer = self.handler._createInserter(self.vgc)
        self.vgc.containers.addToBeginning(inserterVariableContainer)

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        pygame.draw.rect(screen, (150, 150, 150), self.RECT, 0, border_radius = 5)