from __future__ import annotations
from typing import TYPE_CHECKING

from adapter.path_adapter import PathAttributeID
if TYPE_CHECKING:
    from root_container.panel_container.element.row.element_entity import ElementContainer

from enum import Enum
from root_container.panel_container.element.readout.readout_entity import ReadoutEntity
from root_container.panel_container.element.row.label_entity import LabelEntity
from root_container.panel_container.element.widget.widget_entity import WidgetContainer

from common.font_manager import FontID

from abc import ABC, abstractmethod

class ElementType(Enum):
    READOUT = 1
    CHECKBOX = 2
    DROPDOWN = 3
    TEXTBOX = 4

"""
An element is either a widget or a readout.
A list of element definitions are used to convert into a list of rows
"""

class ElementDefinition(ABC):

    def __init__(self, elementType: ElementType, variableName, pathAttributeID: PathAttributeID = PathAttributeID.NONE):
        self.elementType = elementType
        self.variableName = variableName
        self.pathAttributeID = pathAttributeID


        self.LABEL_FONT = FontID.FONT_NORMAL
        self.LABEL_SIZE = 11

    def setID(self, id):
        self.id = id

    def getPathAttributeID(self) -> PathAttributeID:
        return self.pathAttributeID

    @abstractmethod
    def makeElement(self, parent, parentCommand, pathAdapter) -> ElementContainer:
        pass
    
    def makeLabel(self, parent) -> LabelEntity:
        return LabelEntity(parent, self.LABEL_FONT, self.LABEL_SIZE, staticText = self.variableName)

    def getName(self) -> str:
        return self.variableName
    
    def importFromJson(json: dict) -> ElementDefinition:
        from root_container.panel_container.element.readout.readout_definition import ReadoutDefinition
        from root_container.panel_container.element.widget.checkbox_widget import CheckboxWidgetDefinition
        from root_container.panel_container.element.widget.dropdown_widget import DropdownWidgetDefinition
        from root_container.panel_container.element.widget.textbox_widget import CodeTextboxWidgetDefinition, ValueTextboxWidgetDefinition

        class_ = json["class"]
        if class_ == "ReadoutDefinition":
            return ReadoutDefinition.importFromJson(json)
        elif class_ == "CheckboxWidgetDefinition":
            return CheckboxWidgetDefinition.importFromJson(json)
        elif class_ == "DropdownWidgetDefinition":
            return DropdownWidgetDefinition.importFromJson(json)
        elif class_ == "CodeTextboxWidgetDefinition":
            return CodeTextboxWidgetDefinition.importFromJson(json)
        elif class_ == "ValueTextboxWidgetDefinition":
            return ValueTextboxWidgetDefinition.importFromJson(json)
        else:
            raise Exception("Unknown class: " + class_)

    def exportToJson(self) -> dict:
        return { "class": "<unknown>" }
