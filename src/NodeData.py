import math

class NodeData:
    def __init__(self, node_id: int, pos: tuple = None):
        self.node_id: int = node_id
        self.pos = pos
        self.dx = 0
        self.dy = 0
        self.parent = None
        self.distance = float('inf')

    def get_node_id(self) -> int:
        return self.node_id

    def get_position(self) -> tuple:
        return self.pos

    def to_dict(self):
        if self.pos is not None:
            return {'id': self.node_id, 'pos': ','.join(map(str, self.pos))}
        return {'id': self.node_id}

    def __repr__(self):
        if self.pos is not None:
            pos_str = ','.join(map(str, self.pos))
            return f'{{id: {self.node_id}, pos: {pos_str}}}'
        return f'{{id: {self.node_id}}}'
    
    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        is_same_node_id = self.node_id == other.get_node_id()
        is_same_position = self.pos == other.get_position() 

        return is_same_node_id and is_same_position

