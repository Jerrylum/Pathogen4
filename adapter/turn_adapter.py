from adapter.path_adapter import PathAdapter
from command_creation.command_type import CommandType

from enum import Enum, auto

from entity_base.image.image_state import ImageState

class TurnAttributeID(Enum):
    THETA1 = auto()
    THETA2 = auto()

class TurnAdapter(PathAdapter):

    def __init__(self, iconImageStates: list[ImageState]):

        super().__init__(CommandType.TURN, iconImageStates, TurnAttributeID)

        self.turnEnabled: bool = True # if set to false, means THETA1 ~= THETA2)

    def set(self, attribute: TurnAttributeID, value: float, string: str):
        super().set(attribute, value, string)

    def setTurnEnabled(self, turnEnabled: bool):
        self.turnEnabled = turnEnabled

    def isTurnEnabled(self) -> bool:
        return self.turnEnabled