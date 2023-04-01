from abc import ABC, abstractmethod

class ClickListener(ABC):

    def __init__(self, entity):
        self.entity = entity

    @abstractmethod
    def onLeftClick(self):
        pass

    @abstractmethod
    def onRightClick(self):
        pass

    @abstractmethod
    def onDoubleLeftClick(self):
        pass

class ClickLambda(ClickListener):

    def __init__(self, entity, FonLeftClick = lambda: None, FonRightClick = lambda: None, FOnDoubleClick = lambda: None):
        super().__init__(entity)

        self.FonLeftClick = FonLeftClick
        self.FonRightClick = FonRightClick
        self.FOnDoubleClick = FOnDoubleClick

    def onLeftClick(self):
        self.FonLeftClick()

    def onRightClick(self):
        self.FonRightClick()

    def onDoubleLeftClick(self):
        self.FOnDoubleClick()