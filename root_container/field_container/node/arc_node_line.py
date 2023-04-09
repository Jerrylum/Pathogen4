from __future__ import annotations
from typing import TYPE_CHECKING
from common.draw_order import DrawOrder
from common.reference_frame import *
from entity_base.entity import Entity

from utility.pygame_functions import drawDottedLine, shade
if TYPE_CHECKING:
    from root_container.field_container.node.arc_curve_node import ArcCurveNode
import pygame

"""
Drawn from the ArcCurveNode to the midpoint.
Dotted line drawn behind the nodes and segments.
Same color as ArcCurveNode
"""
class ArcNodeLine(Entity):

    # segmentFunction is either getPrevious or getNext
    def __init__(self, arcCurveNode: ArcCurveNode):

        self.arcCurveNode = arcCurveNode

        super().__init__(parent = arcCurveNode, drawOrder = DrawOrder.THETA_LINE)

        self.recomputePosition()

    def isTouching(self, point: tuple) -> bool:
        return False

    # draw from self.a to self.b, which is from the arcCurveNode to the midpoint
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool):


        center = self.arcCurveNode.arc.CENTER.screenRef
        r = self.dimensions.FIELD_DIAGONAL

        # draw line from arcCurveNode to midpoint
        color = self.arcCurveNode.COLOR_H if isHovered else self.arcCurveNode.COLOR
        acn = self.arcCurveNode.positionRef.screenRef
        drawDottedLine(screen, color, acn, center, length = 10, fill = 0.5, width = 1)
        pygame.draw.circle(screen, shade(color, 0.9), center, 3)

        # Draw line extending before start of arc
        startNode = self.arcCurveNode.arc.p1
        theta1 = self.arcCurveNode.arc.THETA1 + math.pi
        if not self.arcCurveNode.segment.getPrevious().constraints.hasConstraint(startNode.fieldRef, theta1):
            # only draw if there isn't already green constraints indicator
            extended = startNode.screenRef[0] + r*math.cos(theta1), startNode.screenRef[1] + r*math.sin(theta1)
            drawDottedLine(screen, (0,0,0), startNode.screenRef, extended, length = 10, fill = 0.5, width = 1)

        # Draw line extending past end of arc
        endNode = self.arcCurveNode.arc.p3
        theta2 = self.arcCurveNode.arc.THETA2
        if not self.arcCurveNode.segment.getNext().constraints.hasConstraint(endNode.fieldRef, theta2):
            # only draw if there isn't already green constraints indicator
            extended = endNode.screenRef[0] + r*math.cos(theta2), endNode.screenRef[1] + r*math.sin(theta2)
            drawDottedLine(screen, (0,0,0), endNode.screenRef, extended, length = 10, fill = 0.5, width = 1)