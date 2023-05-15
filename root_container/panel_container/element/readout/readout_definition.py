from enum import Enum
from adapter.path_adapter import PathAttributeID
from root_container.panel_container.element.readout.readout_entity import ReadoutEntity
from root_container.panel_container.element.row.element_definition import ElementDefinition, ElementType

"""
A CommandDefinition holds a list of DefinedReadouts.
A defined readout holds information for position relative to command
"""

class ReadoutDefinition(ElementDefinition):

    def __init__(self, pathAttributeID: Enum, variableName: str):

        super().__init__(ElementType.READOUT, variableName, pathAttributeID)

    # overriding
    def makeElement(self, parent, parentCommand, pathAdapter) -> ReadoutEntity:
        return ReadoutEntity(parent, parentCommand, pathAdapter, self)
    
    def importFromJson(json: dict):
        return ReadoutDefinition(PathAttributeID(json["pathAttributeID"]), json["variableName"])

    def exportToJson(self) -> dict:
        return {
            "class": "ReadoutDefinition",
            "variableName": self.variableName,
            "pathAttributeID": self.pathAttributeID.value
        }
