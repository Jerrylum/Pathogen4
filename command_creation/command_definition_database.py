from command_creation.command_definition import CommandType, CommandDefinition
from command_creation.preset_commands import CommandDefinitionPresets
from data_structures.observer import Observable
from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity
from root_container.panel_container.command_block.custom_command_block_entity import CustomCommandBlockEntity

from entity_handler.interactor import Interactor
from entity_handler.entity_manager import EntityManager

from adapter.path_adapter import PathAdapter, NullPathAdapter, PathAttributeID
from common.image_manager import ImageManager
from common.dimensions import Dimensions
from root_container.panel_container.element.readout.readout_definition import ReadoutDefinition
from root_container.panel_container.element.row.element_definition import ElementDefinition, ElementType
import json

"""
Stores all the different CommandDefinitions
"""

class CommandDefinitionDatabase(Observable):

    def __init__(self):

        # initialize empty list for each command type
        self.definitions : dict[CommandType, dict[str, CommandDefinition]] = {}
        for type in CommandType:
            self.definitions[type] = {}

        # initially populate with preset commands. make sure there's one command per type at least
        presets = CommandDefinitionPresets()
        for preset in presets.getPresets():
            self.registerDefinition(preset, False)

        self.lastUpdatedCommandID: str = None
        self.lastUpdatedCommandType: CommandType = None

    # add a (id, command) pair to definitions
    # notify observers for any new definitions except for the initial preset commands
    def registerDefinition(self, command: CommandDefinition, notifyObservers: bool = True):
        self.definitions[command.type][command.id] = command

        self.lastUpdatedCommandID = command.id
        self.lastUpdatedCommandType = command.type

        print("registered", command.name)

        if notifyObservers:
            print("registered", command)
            self.notify()

    def getDefinitionNames(self, type: CommandType, isInTask: bool = False) -> list[str]:
        return [definition.name for definition in self.definitions[type].values()
                if (not isInTask or definition.allowedInTask)]
    
    def getNumDefitions(self, type: CommandType) -> int:
        return len(self.definitions[type])
    
    def getDefinitionByIndex(self, type: CommandType, index: int = 0) -> CommandDefinition:
        return list(self.definitions[type].values())[index]
    
    def getDefinitionByID(self, type: CommandType, id: str) -> CommandDefinition:
        return self.definitions[type][id]
    
    def getDefinitionIDByName(self, type: CommandType, name: str) -> int:
        definitions = self.definitions[type]
        for id in definitions:
            if definitions[id].name == name:
                return id
        raise Exception("No definition with name " + name + " found")
    
    def importFromJson(self, json: dict):
        # initialize empty list for each command type
        self.definitions : dict[CommandType, dict[str, CommandDefinition]] = {}
        for type in CommandType:
            self.definitions[type] = {}

        self.lastUpdatedCommandID: str = None
        self.lastUpdatedCommandType: CommandType = None

        for definitionJson in json["commands"]:
            definition = CommandDefinition.importFromJson(definitionJson)
            self.registerDefinition(definition, False)
    
    def exportToJson(self) -> dict:
        return {
            "commands": [definition.exportToJson() for type in self.definitions for definition in self.definitions[type].values()]
        }