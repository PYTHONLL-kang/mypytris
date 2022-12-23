import time
import pygame as p
import random

import copy

p.init()

black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
light_blue = (0, 255, 255)
purple = (255, 0, 255)
blue = (30, 128, 255)
orange = (255, 140, 0)
green = (0, 221, 0)
red = (255, 0, 0)

size = [640, 640]
screen = p.display.set_mode(size)

p.display.set_caption("pytris")
done = False
clock = p.time.Clock()


def draw_rect(x, y, color):
    p.draw.rect(screen, color, [x, y, 25, 25], 1)


def draw_line():
    p.draw.rect(screen, white, [164, 0, 1, 520], 1) #게임판 왼쪽
    p.draw.rect(screen, white, [427, 0, 1, 520], 1) #게임판 오른쪽
    p.draw.rect(screen, white, [164, 520, 264, 1], 1) #게임판 밑쪽
    p.draw.rect(screen, white, [0, 0, 130, 130], 1) # 홀드 자리
    abcd = 1
    ran = [1, 2, 3, 4, 5]
    for abcd in ran:
        p.draw.line(screen, white, (442-15, (52*abcd)+(10*abcd)), (640, (52*abcd)+(10*abcd)), 1) #넥스트 블록
        abcd = abcd + 1
class Block:
    def __init__(self, X, Y, position, shape, color):
        self.X = X
        self.Y = Y
        self.position = position
        self.shape = shape
        self.last_decent = time.time()
        self.decent_margin = 1
        self.color = color

    def move(self, x, y):
        self.X += x
        self.Y += y

    def render(self, spin):     
        for shape in self.shape[spin]:
            draw_rect(shape["x"] + self.X, shape["y"] + self.Y, self.color)

    def go_to(self):
        self.X = 270-26
        self.Y = 0

    def go(self, num):
        self.Y = num

    def to_dict(self, spin):
        dict_object = []

        for shape in self.shape[spin]:
            dict_object.append({"x": shape["x"] + self.X, "y": shape["y"] + self.Y, "color": self.color})

        return dict_object

class BlockJ(Block):
    def __init__(self, x, y, position):
        super().__init__(x, y, position, 
        [   [   {"x": 0, "y": 26},
                {"x": 26, "y": 26},
                {"x": 52, "y": 26},
                {"x": 0, "y": 0}
            ], 
            [   {"x": 26, "y": 0},
                {"x": 52, "y": 0},
                {"x": 26, "y": 26},
                {"x": 26, "y": 52}
            ], 
            [   {"x": 0, "y": 0},
                {"x": 26, "y": 0},
                {"x": 52, "y": 0},
                {"x": 52, "y": 26}
            ], 
            [   {"x": 26, "y": 52},
                {"x": 52, "y": 0},
                {"x": 52, "y": 26},
                {"x": 52, "y": 52}
            ]], blue)

class BlockL(Block):
    def __init__(self, x, y, position):
        super().__init__(x, y, position,
        [   [
                {"x": 0, "y": 26},
                {"x": 26, "y": 26},
                {"x": 52, "y": 26},
                {"x": 52, "y": 0}
            ],
            [
                {"x": 26, "y": 0},
                {"x": 26, "y": 26},
                {"x": 26, "y": 52},
                {"x": 52, "y": 52}
            ],
            [
                {"x": 0, "y": 0},
                {"x": 26, "y": 0},
                {"x": 52, "y": 0},
                {"x": 0, "y": 26}
            ],
            [
                {"x": 26, "y": 0},
                {"x": 52, "y": 0},
                {"x": 52, "y": 26},
                {"x": 52, "y": 52}
            ]],
            orange)
class BlockT(Block):
    def __init__(self, x, y, position):
        super().__init__(x, y, position,
        [   [
                {"x": 0, "y": 26},
                {"x": 26, "y": 26},
                {"x": 52, "y": 26},
                {"x": 26, "y": 0}
            ],
            [
                {"x": 26, "y": 52},
                {"x": 26, "y": 26},
                {"x": 26, "y": 0},
                {"x": 52, "y": 26}
            ],
            [
                {"x": 0, "y": 26},
                {"x": 26, "y": 26},
                {"x": 52, "y": 26},
                {"x": 26, "y": 52}
            ],
            [
                {"x": 0, "y": 26},
                {"x": 26, "y": 0},
                {"x": 26, "y": 26},
                {"x": 26, "y": 52}
            ]],
            purple)

class BlockO(Block):
    def __init__(self, x, y, position):
        super().__init__(x, y, position,
        [   [
                {"x": 26, "y": 0},
                {"x": 26, "y": 26},
                {"x": 52, "y": 26},
                {"x": 52, "y": 0}
            ],
            [
                {"x": 0, "y": 0},
                {"x": 0, "y": 26},
                {"x": 26, "y": 26},
                {"x": 26, "y": 0}
            ],
            [
                {"x": 0, "y": 0},
                {"x": 0, "y": 26},
                {"x": 26, "y": 26},
                {"x": 26, "y": 0}
            ],
            [
                {"x": 0, "y": 0},
                {"x": 0, "y": 26},
                {"x": 26, "y": 26},
                {"x": 26, "y": 0}
            ]],
            yellow)

class BlockZ(Block):
    def __init__(self, x, y, position):
        super().__init__(x, y, position,
        [   [
                {"x": 0, "y": 0},
                {"x": 26, "y": 26},
                {"x": 52, "y": 26},
                {"x": 26, "y": 0}
            ],
            [
                {"x": 52, "y": 0},
                {"x": 52, "y": 26},
                {"x": 26, "y": 26},
                {"x": 26, "y": 52}
            ],
            [
                {"x": 26, "y": 26},
                {"x": 52, "y": 26},
                {"x": 52, "y": 52},
                {"x": 78, "y": 52}
            ],
            [
                {"x": 26, "y": 0},
                {"x": 0, "y": 26},
                {"x": 26, "y": 26},
                {"x": 0, "y": 52}
            ]],
            red)
class BlockS(Block):
    def __init__(self, x, y, position):
        super().__init__(x, y, position,
        [   [
                {"x": 26, "y": 0},
                {"x": 52, "y": 0},
                {"x": 26, "y": 26},
                {"x": 0, "y": 26}
            ],
            [
                {"x": 0, "y": 0},
                {"x": 0, "y": 26},
                {"x": 26, "y": 26},
                {"x": 26, "y": 52}
            ],
            [
                {"x": 0, "y": 26},
                {"x": 26, "y": 0},
                {"x": 26, "y": 26},
                {"x": 52, "y": 0}
            ],
            [
                {"x": 26, "y": 0},
                {"x": 26, "y": 26},
                {"x": 52, "y": 26},
                {"x": 52, "y": 52}
            ]],
            green)

class BlockI(Block):
    def __init__(self, x, y, position):
        super().__init__(x, y, position,
        [   [
                {"x": 0, "y": 26},
                {"x": 26, "y": 26},
                {"x": 52, "y": 26},
                {"x": 78, "y": 26}
            ],
            [
                {"x": 52, "y": 0},
                {"x": 52, "y": 26},
                {"x": 52, "y": 52},
                {"x": 52, "y": 78}
            ],
            [
                {"x": 0, "y": 52},
                {"x": 26, "y": 52},
                {"x": 52, "y": 52},
                {"x": 78, "y": 52}
            ],
            [
                {"x": 26, "y": 0},
                {"x": 26, "y": 26},
                {"x": 26, "y": 52},
                {"x": 26, "y": 78}
            ]],
            light_blue)
class Bag:
    def __init__(self):
            
        self.bag = [
            BlockI(0, 0, 0), 
            BlockJ(0, 0, 0), 
            BlockL(0, 0, 0), 
            BlockO(0, 0, 0), 
            BlockS(0, 0, 0), 
            BlockT(0, 0, 0), 
            BlockZ(0, 0, 0)
        ]
        
        # self.bag = [
        #     BlockS(0, 0, 0)
        # ]

    def pop_(self):
        if len(self.bag) == 0:
            self.__init__()
            return self.pop_()
        result = self.bag.pop(random.randrange(0, len(self.bag)))

        return result

def check_collide(_object, spin, stacks, directionX = 0, directionY = 0):
    blocks = _object.to_dict(spin)
    for stackY in stacks:
        for stack in stacks[stackY]:
            for block in blocks:
                block_rct = p.Rect(block["x"] + directionX, block["y"] + directionY, 26, 26)
                stack_rct = p.Rect(stack["x"], stackY, 26, 26)

                if block_rct.colliderect(stack_rct):
                    return True

    return False
                
def check_wall_collide(_object, spin, directionX = 0, directionY = 0):
    for block in _object.to_dict(spin):
        block_rect = p.Rect(block["x"] + directionX, block["y"] + directionY, 26, 26)
        left_wall = p.Rect(146, 0, 1, 520)
        right_wall = p.Rect(442-15, 0, 1, 520)
        bottom_wall = p.Rect(146, 520, 286, 1)
        left_space = p.Rect(0, 0, 146, 520)
        right_space = p.Rect(427, 0, 500, 520)
        bottom_space = p.Rect(0, 520, 1000, 1000)


        if block_rect.colliderect(left_wall) or block_rect.colliderect(right_wall) or block_rect.colliderect(bottom_wall) or block_rect.colliderect(left_space) or block_rect.colliderect(right_space) or block_rect.colliderect(bottom_space):
            return True

    return False



class Objects:
    def __init__(self):
        self.objects = {}
        self.yyy = 0

    def add(self, blocks, spin):
        for block in blocks.to_dict(spin):
            blockY = block["y"]
            try:
                self.objects[blockY].append({"x" : block["x"], "color": block["color"]})
            except KeyError:
                self.objects[blockY] = [{"x" : block["x"], "color": block["color"]}]

    def render(self):
        for blockY in self.objects:
            for block in self.objects[blockY]: # {"x":12,"color"} [{"x":12,"color"},{"x":12,"color"},{"x":12,"color"},{"x":12,"color"},{"x":12,"color"},]    
                draw_rect(block["x"], blockY, block["color"])

    def clear_line(self):
        #print("self.objects:", self.objects)
        _objects = copy.deepcopy(self.objects)
        for clearblockY in self.objects:
            if len(self.objects[clearblockY]) == 10 and self.objects[clearblockY][0]["x"] > 0 and self.objects[clearblockY][0]["x"] < 540:
                del _objects[clearblockY]

                for blockY in self.objects:
                    if blockY < clearblockY:
                        shift_line = _objects[blockY]
                        del _objects[blockY]
                        _objects[blockY + 26] = shift_line

                break

        self.objects = _objects

        # print(clearY)
        # for y in clearY:
        #     del self.objects[y]

    # def pull_down(self):
    #     for blockY in self.objects:



class Hold:
    def __init__(self):
        self.holding = None
        
    def pop(self, block):
        hold_block = self.holding
        self.holding = block
        return hold_block

    def render(self, spin):
        if self.holding == None:
            return None

        self.holding.X = 26
        self.holding.Y = 26
        self.holding.render(spin)


objects = Objects()

bag = Bag()
hold = Hold()

current_block = bag.pop_()

current_block.go_to()

stack = []
holding = 0
spin = 0

def kick(spin, dir, current_block):
    kick_table = [
        [ [ 0, 0], [ 0,-1], [-1,-1], [ 2, 0], [ 2,-1], [ 0, 0] ],#0 -> 1
        [ [ 0, 0], [ 0, 1], [ 1, 1], [-2, 0], [-2, 1], [ 0, 0] ],#1 -> 2
        [ [ 0, 0], [ 0, 1], [-1, 1], [ 2, 0], [ 2, 1], [ 0, 0] ],#2 -> 3
        [ [ 0, 0], [ 0,-1], [ 1,-1], [-2, 0], [-2,-1], [ 0, 0] ],#3 -> 0
        [ [ 0, 0], [ 0, 1], [ 1, 1], [-2, 0], [-2, 1], [ 0, 0] ],#1 -> 0
        [ [ 0, 0], [ 0,-1], [-1,-1], [ 2, 0], [ 2,-1], [ 0, 0] ],#2 -> 1
        [ [ 0, 0], [ 0,-1], [ 1,-1], [-2, 0], [-2,-1], [ 0, 0] ],#3 -> 2
        [ [ 0, 0], [ 0, 1], [-1, 1], [ 2, 0], [ 2, 1], [ 0, 0] ],#0 -> 3

        [ [ 0, 0], [-1, 0], [-1, 1], [-1,-1], [ 0, 1], [ 0,-1] ],#0 -> 2
        [ [ 0, 0], [ 1, 0], [ 1,-1], [ 1, 1], [ 0,-1], [ 0, 1] ],#2 -> 0
        [ [ 0, 0], [ 0, 1], [-2, 1], [-1, 1], [-2, 0], [-1, 0] ],#1 -> 3
        [ [ 0, 0], [ 0,-1], [-2,-1], [-1,-1], [-2, 0], [-1, 0] ] #3 -> 1
                ]
    if dir == 1:
        for i in range(len(kick_table[spin])):
            if check_wall_collide(current_block, spin, directionY= 26) or check_collide(current_block, spin, objects.objects, directionY= 26):
                current_block.move(26 * kick_table[spin][i][0], 26 * kick_table[spin][i][1])
                break
    if dir == 0:
        for i in range(len(kick_table[spin+3])):
            if check_wall_collide(current_block, spin, directionY= 26) or check_collide(current_block, spin, objects.objects, directionY= 26):
                current_block.move(26 * kick_table[spin+3][i][0], 26 * kick_table[spin+3][i][1])
                break

while not done:
    clock.tick(20)
    screen.fill(black)
    
    current_x = current_block.X
    current_y = current_block.Y

    rct = p.Rect(current_x, current_y, 26, 26)
    hold.render(0)

    #current_block.move(0, 15)
    if time.time() - current_block.last_decent > current_block.decent_margin and not check_wall_collide(current_block, spin, directionY= 26) and not check_collide(current_block, spin, objects.objects,  directionY= 26):
        current_block.move(0, 26)
        current_block.last_decent = time.time()

    key_event = p.key.get_pressed()

    if key_event[p.K_LEFT] and not check_wall_collide(current_block, spin, directionX= -26) and not check_collide(current_block, spin, objects.objects,  directionX= -26):
        current_block.move(-26, 0)

    if key_event[p.K_RIGHT] and not check_wall_collide(current_block, spin, directionX= 26) and not check_collide(current_block, spin, objects.objects, directionX= 26):
        current_block.move(26, 0) 

    if key_event[p.K_DOWN] and not check_wall_collide(current_block, spin, directionY= 26) and not check_collide(current_block, spin, objects.objects, directionY= 26):
        current_block.move(0, 26)

    if key_event[p.K_x] or key_event[p.K_UP]:
        kick(spin, 1, current_block)
        if spin == 3:
            spin = 0
        else:
            spin = spin + 1

    if key_event[p.K_z]:
        kick(spin, 0, current_block)
        if spin == 0:
            spin = 3
        else:
            spin = spin -1
            
    if key_event[p.K_a]:
        spin = spin + 2
        if spin >= 4:
            spin = spin - 2

        current_block.render(spin)
        current_block.to_dict(spin)

    if key_event[p.K_c] and holding == 0:
        holding = 1
        popped_block = hold.pop(current_block)
        if popped_block != None:
            current_block = popped_block
        else:
            current_block = bag.pop_()
        current_block.go_to()

    if  check_wall_collide(current_block, spin, directionY= 26) and key_event[p.K_DOWN] or check_collide(current_block, spin, objects.objects, directionY= 26) and key_event[p.K_DOWN] or key_event[p.K_SPACE]:
        while not check_wall_collide(current_block, spin, directionY= 26) and not check_collide(current_block, spin, objects.objects, directionY= 26):
            current_block.move(0, 26)

        # for block in current_block.to_dict(): # 쌓인 블럭에 데이터 추가
        #     stack.append(block)
            
        objects.add(current_block, spin)

        current_block = bag.pop_()
        current_block.go_to()
        holding = 0
        spin = 0

    for event in p.event.get():
        if event.type == p.QUIT:
            done = True

    objects.render()
    objects.clear_line()
    current_block.render(spin)

    #print(objects.objects)
    draw_line()
    p.display.flip()

p.quit()
