from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity


from entity_base.listeners.click_listener import ClickLambda
from entity_base.listeners.key_listener import KeyLambda
from entity_base.listeners.select_listener import SelectLambda, SelectorType

from root_container.panel_container.element.widget.widget_entity import WidgetEntity
from root_container.panel_container.element.widget.widget_definition import WidgetDefinition

from entity_ui.text.text_editor_entity import TextEditorEntity, TextEditorMode

from common.font_manager import FontID, DynamicFont
from common.image_manager import ImageID
from common.draw_order import DrawOrder
from common.reference_frame import PointRef, Ref



class TextboxWidgetEntity(WidgetEntity['TextboxWidgetDefinition']):

    def __init__(self, parentCommand: CommandBlockEntity, definition: 'TextboxWidgetDefinition'):

        if definition.pwidth is None:
            width = None
        else:
            width = lambda: parentCommand.dimensions.PANEL_WIDTH * definition.pwidth

        font: DynamicFont = parentCommand.fonts.getDynamicFont(definition.fontID, definition.fontSize)

        self.textEditor = TextEditorEntity(
            font,
            parentCommand.dimensions.px, parentCommand.dimensions.py,
            getOpacity = self.getOpacity,
            isDynamic = definition.isDynamic,
            isNumOnly = definition.isNumOnly,
            defaultText = definition.defaultText
        )
        self.parentCommand.entities.addEntity(self.textEditor, self)

        # Sends notification when text height changes
        self.textEditor.subscribe(onNotify = self._parent.updateTargetHeight)

        super().__init__(parentCommand, definition,
            key = KeyLambda(self,
                            FonKeyDown = self.textEditor.onKeyDown,
                            FonKeyUp = self.textEditor.onKeyUp
                            ),
            select = SelectLambda(self, "text editor", type = SelectorType.SOLO, greedy = True,
                                  FonSelect = self.textEditor.onSelect,
                                  FonDeselect = self.textEditor.onDeselect
                            )
        )

        self.onModifyDefinition()


    def onModifyDefinition(self):
        # width is a lambda so is automatically updated
        self.textEditor.setRows(self.definition.rows)
        # isDynamic is immutable once set

    # top left corner, screen ref
    def getX(self) -> float:
        return self.getPosition().screenRef[0] - self.textEditor.defineWidth() / 2
    
    # top left corner, screen ref
    def getY(self) -> float:
        return self.getPosition().screenRef[1] - self.textEditor.originalHeight / 2
    
    # for dynamic widgets. how much to stretch command height by
    def getCommandStretch(self) -> int:
        return self.textEditor.getHeightOffset()
    
    
    def getValue(self) -> bool:
        return self.textEditor.getText()

    def isTouchingWidget(self, position: PointRef) -> bool:
        return self.textEditor.isTouching(position)



class TextboxWidgetDefinition(WidgetDefinition):

    def __init__(self, name: str, px: int, py: int, pwidth: float, rows: int, fontID: FontID, fontSize: float, defaultText: str, isDynamic: bool, isNumOnly: bool):
        super().__init__(name, px, py)

        self.pwidth = pwidth
        self.rows = rows
        self.fontID = fontID
        self.fontSize = fontSize
        self.defaultText = defaultText
        self.isDynamic = isDynamic
        self.isNumOnly = isNumOnly

    def make(self, parentCommand) -> TextboxWidgetEntity:
        return TextboxWidgetEntity(parentCommand, self)
    
# dynamic, no text restrictions
class CodeTextboxWidgetDefinition(TextboxWidgetDefinition):
    def __init__(self, name: str, px: int, py: int, pwidth: float):
        super().__init__(name, px, py, pwidth, 1, fontID = FontID.FONT_CODE, fontSize = 10, defaultText = "", isDynamic = True, isNumOnly = False)

# numbers only, static
class ValueTextboxWidgetDefinition(TextboxWidgetDefinition):

    def __init__(self, name: str, px: int, py: int, defaultValue: float):
        defaultText = str(round(defaultValue, 3))
        super().__init__(name, px, py, None, 1, fontID = FontID.FONT_NORMAL, fontSize = 15, defaultText = defaultText, isDynamic = False, isNumOnly = True)