from common.draw_order import DrawOrder
from entity_base.container_entity import Container
from entity_base.entity import Entity

class StaticCommandContentContainer(Container):

    def __init__(self, parent: Entity, drawOrder: DrawOrder):
        super().__init__(parent, drawOrder = drawOrder)
        self.recomputeEntity()

    def defineLeftX(self) -> float:
        return self._px(0.025)
    
    def defineRightX(self) -> float:
        return self._px(0.921)
    
    def defineTopY(self) -> float:
        return self._py(0.02)
    
    def defineBottomY(self) -> float:
        return self._py(0.9)
