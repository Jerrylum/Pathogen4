from __future__ import annotations
from typing import TYPE_CHECKING

from entity_base.entity import Entity
if TYPE_CHECKING:
    from root_container.panel_container.command_block.command_sequence_handler import CommandSequenceHandler
    from root_container.panel_container.tab.block_tab_contents_container import BlockTabContentsContainer
    from root_container.panel_container.command_block_section.command_section import CommandSection

from entity_base.container_entity import Container
from entity_ui.group.variable_group.variable_group_container import VariableGroupContainer
import pygame

"""
A command section holds command blocks. Its usefulness lies in being able to
expand and collapse command sections, as well as show or hide the path section
pertaining to the command section.
"""

class CommandSectionHeader(Container):

    def __init__(self, parent: CommandSection):

        super().__init__(parent = parent)
        self.section = parent
    
    # This container is dynamically fit to VariableGroupContainer
    def defineHeight(self) -> float:
        return self._aheight(self.section.HEADER_HEIGHT)
    
    def defineTopY(self) -> float:
        return self._py(0)