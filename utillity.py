import random as rand

from var import BOARD_SIZE, BOARD_TOP
from block import I_mino, J_mino, L_mino, S_mino, Z_mino, T_mino, O_mino

class Bag:
    def __init__(self):
        self.bag = [
            I_mino(),
            J_mino(),
            L_mino(),
            O_mino(),
            S_mino(),
            T_mino(),
            Z_mino()
        ]

        self.shows = [self.bag_() for i in range(5)]

    def pop_(self):
        self.shows.append(self.bag_())
        return self.shows.pop(0)

    def bag_(self):
        if len(self.bag) == 0:
            self.bag = [
                I_mino(),
                J_mino(),
                L_mino(),
                O_mino(),
                S_mino(),
                T_mino(),
                Z_mino()
            ]
            return self.bag_()

        return self.bag.pop(rand.randrange(0, len(self.bag)))

class Hold:
    def __init__(self):
        self.holding = None
        self.is_hold = False

    def change(self, block):
        block.__init__()
        self.holding.__init__()
        hold_block = self.holding
        self.holding = block
        self.is_hold = True

        return hold_block

    def holding_block(self):
        self.holding.x = 0
        self.holding.y = 4
    
        return [self.holding.to_object()]

class Stack_manager:
    def __init__(self):
        self.stack_objects = [[] for i in range(BOARD_SIZE[1])]

    def add(self, mino):
        for block in mino.to_object():
            self.stack_objects[block['y']-BOARD_TOP].append(block)

    def clear_line(self):
        cleard_line = []
        for i, line in enumerate(self.stack_objects):
            if len(line) >= BOARD_SIZE[0]:
                for j in range(i):
                    for block in self.stack_objects[j]:
                        block['y'] += 1

                self.stack_objects.pop(i)
                self.stack_objects.insert(0, [])
                cleard_line.append(line[0]['y'])

        return cleard_line