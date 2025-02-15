from command_creation.command_type import CommandType
from root_container.field_container.node.path_node_entity import PathNodeEntity
from root_container.field_container.path_element import PathElement
from root_container.field_container.segment.path_segment_entity import PathSegmentEntity
from root_container.field_container.segment.segment_type import PathSegmentType
from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity

"""
In charge of linking the path entity (node or segment) from and to the command.
This is necessary for when path entities get deleted, so that the command can be deleted as well.
This is also useful for when the path entity needs to highlight the command, or vice versa.
The added complication is that one segment is linked to each segment command,
i.e. Straight, Arc, Bezier.
"""

class PathCommandLinker:

    def __init__(self):
        self.nodeToCommand: dict[PathNodeEntity, CommandBlockEntity] = {}
        self.segmentToCommands: dict[PathSegmentEntity, list[CommandBlockEntity]] = {}

        self.commandToPath: dict[CommandBlockEntity, PathElement] = {}

    def linkNode(self, node: PathNodeEntity, command: CommandBlockEntity):
        self.nodeToCommand[node] = command
        self.commandToPath[command] = node

    def linkSegment(self, segment: PathElement, command: CommandBlockEntity):

        if segment not in self.segmentToCommands:
            self.segmentToCommands[segment] = []

        self.segmentToCommands[segment].append(command)
        self.commandToPath[command] = segment

    def _getCommandTypeFromSegmentType(self, segmentType: PathSegmentType) -> CommandType:
        if segmentType == PathSegmentType.STRAIGHT:
            return CommandType.STRAIGHT
        elif segmentType == PathSegmentType.ARC:
            return CommandType.ARC
        elif segmentType == PathSegmentType.BEZIER:
            return CommandType.BEZIER
        else:
            raise Exception("PathCommandLinker: Unknown segment type " + str(segmentType))

    def getCommandFromPath(self, nodeOrSegment: PathElement) -> CommandBlockEntity:
        if isinstance(nodeOrSegment, PathNodeEntity):
            return self.nodeToCommand[nodeOrSegment]
        elif isinstance(nodeOrSegment, PathSegmentEntity):
            segment: PathSegmentEntity = nodeOrSegment
            pathType = segment.getSegmentType()
            for command in self.segmentToCommands[segment]:
                if command.getCommandType() == self._getCommandTypeFromSegmentType(pathType):
                    return command
            raise Exception("PathCommandLinker: No command found for segment " + str(segment))
    
    def getCommandFromSegmentAndType(self, segment: PathSegmentEntity, pathType: PathSegmentType) -> CommandBlockEntity:
        targetCommandType = self._getCommandTypeFromSegmentType(pathType)
        for command in self.segmentToCommands[segment]:
            if command.getCommandType() == targetCommandType:
                return command
        raise Exception("PathCommandLinker: No command found for segment " + str(segment) + " and type " + str(pathType))

    def getLastCommandFromSegment(self, segment: PathSegmentEntity) -> CommandBlockEntity:
        return self.segmentToCommands[segment][-1]
    
    def getCommandsFromSegment(self, segment: PathSegmentEntity) -> list[CommandBlockEntity]:
        return self.segmentToCommands[segment]

    def getPathFromCommand(self, command: CommandBlockEntity) -> PathElement:
        return self.commandToPath[command]
    
    def deleteNode(self, node: PathNodeEntity):
        command = self.nodeToCommand[node]
        del self.nodeToCommand[node]
        del self.commandToPath[command]

    def deleteSegment(self, segment: PathSegmentEntity):
        commands = self.segmentToCommands[segment]
        for command in commands:
            del self.commandToPath[command]
        del self.segmentToCommands[segment]