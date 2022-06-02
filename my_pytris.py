import time
import pygame as p
import random

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
    # print(x,y)

    p.draw.rect(screen, color, [x, y, 25, 25], 1)


def draw_line(): # 충돌부분 만들게 Ok
    p.draw.rect(screen, white, [164, 0, 1, 520], 1)
    p.draw.rect(screen, white, [442-15, 0, 1, 520], 1)
    p.draw.rect(screen, white, [164, 520, 264, 1], 1)
    abcd = 1
    ran = [1, 2, 3, 4, 5]
    for abcd in ran:
        p.draw.line(screen, white, (442-15, (52*abcd)+(10*abcd)), (640, (52*abcd)+(10*abcd)), 1)
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

    def render(self):
        # if time.time() - self.last_decent > self.decent_margin:
        #     self.move(0, 26)
        #     self.last_decent = time.time()

        for shape in self.shape:
            draw_rect(shape["x"] + self.X, shape["y"] + self.Y, self.color)

            
    def go_to(self):
        self.X = 270
        self.Y = 0

    def to_dict(self):
        dict_object = []

        for shape in self.shape:
            dict_object.append({"x": shape["x"] + self.X, "y": shape["y"] + self.Y, "color": self.color})

        return dict_object

class BlockJ(Block):
    def __init__(self, x, y, position):
        super().__init__(x, y, position, [
            {"x": 0, "y": 26},
            {"x": 26, "y": 26},
            {"x": 52, "y": 26},
            {"x": 0, "y": 0}
        ], blue)

    def spin(self):
        pass

    
class BlockL(Block):
    def __init__(self, x, y, position):
        super().__init__(x, y, position, [
            {"x": 0, "y": 26},
            {"x": 26, "y": 26},
            {"x": 52, "y": 26},
            {"x": 52, "y": 0}
        ], orange)


    def spin(self):
        pass

class BlockT(Block):
    def __init__(self, x, y, position):
        super().__init__(x, y, position, [
            {"x": 0, "y": 26},
            {"x": 26, "y": 26},
            {"x": 52, "y": 26},
            {"x": 26, "y": 0}
        ], purple)

    def spin1(self):
        self.shape = [
            {"x": 26, "y": 0},
            {"x": 26, "y": 26},
            {"x": 52, "y": 26},
            {"x": 26, "y": 52},
        ]

class BlockO(Block):
    def __init__(self, x, y, position):
        super().__init__(x, y, position, [
            {"x": 0, "y": 0},
            {"x": 0, "y": 26},
            {"x": 26, "y": 26},
            {"x": 26, "y": 0}
        ], yellow)

    def spin(self):
        pass

class BlockZ(Block):
    def __init__(self, x, y, position):
        super().__init__(x, y, position, [
            {"x": 0, "y": 0},
            {"x": 26, "y": 26},
            {"x": 52, "y": 26},
            {"x": 26, "y": 0}
        ], red)


    def spin(self):
        pass


class BlockS(Block):
    def __init__(self, x, y, position):
        super().__init__(x, y, position, [
            {"x": 26, "y": 0},
            {"x": 52, "y": 0},
            {"x": 26, "y": 26},
            {"x": 0, "y": 26}
        ], green)


    def spin(self):
        pass

class BlockI(Block):
    def __init__(self, x, y, position):
        super().__init__(x, y, position, [
            {"x": 0, "y": 0},
            {"x": 26, "y": 0},
            {"x": 52, "y": 0},
            {"x": 78, "y": 0}
        ], light_blue)
        
    def spin(self):
        pass


class Bag:
    def __init__(self):
        """
        self.bag = [
            BlockI(0, 0, 0), 
            BlockJ(0, 0, 0), 
            BlockL(0, 0, 0), 
            BlockO(0, 0, 0), 
            BlockS(0, 0, 0), 
            BlockT(0, 0, 0), 
            BlockZ(0, 0, 0)
        ]
        """
        self.bag = [BlockT(0, 0, 0), BlockO(0, 0, 0)]

    def pop_(self):
        if len(self.bag) == 0:
            self.__init__()
            return self.pop_()
        result = self.bag.pop(random.randrange(0, len(self.bag)))

        return result



def check_collide(_object, stacks, directionX = 0, directionY = 0):
    for stack in stacks:
        for block in _object.to_dict():
            block_rct = p.Rect(block["x"] + directionX, block["y"] + directionY, 26 ,26)
            stack_rct = p.Rect(stack["x"], stack["y"], 26, 26)

            if block_rct.colliderect(stack_rct):
                return True

    return False

def check_wall_collide(_object, directionX = 0, directionY = 0):
    for block in _object.to_dict():
        block_rect = p.Rect(block["x"] + directionX, block["y"] + directionY, 26, 26)
        left_wall = p.Rect(146, 0, 1, 520)
        right_wall = p.Rect(442-15, 0, 1, 520)
        bottom_wall = p.Rect(146, 520, 286, 1)

        if block_rect.colliderect(left_wall) or block_rect.colliderect(right_wall) or block_rect.colliderect(bottom_wall):
            return True

    return False



class Objects:
    def __init__(self):
        self.objects = {}
        self.delY = 0 #지워지는 줄
        self.ya = 0 #줄 지워질 때 y축에 26(한 칸) 더하는 거 
        # 자신.야 = 0

    def add(self, blocks):
        for block in blocks.to_dict():
            blockY = str(block["y"])
            try:
                self.objects[blockY].append({"x" : block["x"], "color": block["color"]})
            except KeyError:
                self.objects[blockY] = [{"x" : block["x"], "color": block["color"]}]
            # self.objects.append(block)

    def render(self, stack):
        self.stack_ = stack
        for blockY in self.objects:
            for block in self.objects[blockY]:
                if self.delY <= int(blockY): #지워지는 줄보다 쌓인 줄이 더 낮게 있으면
                    draw_rect(block["x"], int(blockY), block["color"]) #냅두고
                else:
                    for i in range(len(self.objects)):
                        print(block)
                        if not check_collide(block[i], self.stack_, directionY=26) and not check_wall_collide: #겹치지 않으면
                            draw_rect(block["x"], int(blockY) + 26, block["color"]) #아니면 한칸 낮추는 거
            # draw_rect(object["x"], object["y"], object["color"])

    def clear_line(self):
        for blockY in self.objects:
            if len(self.objects[blockY]) == 10 and self.objects[blockY][0]["x"] > 0 and self.objects[blockY][0]["x"] < 540:
                self.ya = self.ya + 26
                self.delY = int(blockY)
                print("지워지는 줄: ")
                print(self.delY)
                #print(self.objects[blockY])
                for block_index in range(len(self.objects[blockY])):
                    self.objects[blockY][block_index]["x"] = -100

    # def pull_down(self):
    #     for blockY in self.objects:


"""
def hold_block(_object):
    hold  = _object
    return hold
"""


objects = Objects()

bag = Bag()
current_block = bag.pop_()

current_block.go_to()

start = 0
stack = []
holding = 0

while not done:
    clock.tick(20)
    screen.fill(black)
    
    current_x = current_block.X
    current_y = current_block.Y

    print(current_block)

    rct = p.Rect(current_x, current_y, 26, 26)

    #current_block.move(0, 15)
    if time.time() - current_block.last_decent > current_block.decent_margin and not check_wall_collide(current_block, directionY= 26) and not check_collide(current_block, stack,  directionY= 26):
        current_block.move(0, 26)
        current_block.last_decent = time.time()

    key_event = p.key.get_pressed()

    if key_event[p.K_LEFT] and not check_wall_collide(current_block, directionX= -26) and not check_collide(current_block, stack,  directionX= -26):
        current_block.move(-26, 0)

    if key_event[p.K_RIGHT] and not check_wall_collide(current_block, directionX= 26) and not check_collide(current_block, stack, directionX= 26):
        current_block.move(26, 0) 

    if key_event[p.K_DOWN] and not check_wall_collide(current_block, directionY= 26) and not check_collide(current_block, stack, directionY= 26):
        current_block.move(0, 26)

    if  check_wall_collide(current_block, directionY= 26) and key_event[p.K_DOWN] or check_collide(current_block, stack, directionY= 26) and key_event[p.K_DOWN]:
        for block in current_block.to_dict(): # 쌓인 블럭에 데이터 추가
            stack.append(block)
            
        objects.add(current_block)

        current_block = bag.pop_()
        current_block.go_to()

        objects.clear_line()
        

    elif check_collide(current_block, stack, directionY=26) or check_wall_collide(current_block, directionY=26) or key_event[p.K_SPACE]:
        #current_block.stop_bottom()
        
        for block in current_block.to_dict(): # 쌓인 블럭에 데이터 추가
            stack.append(block)

        objects.add(current_block)

        current_block = bag.pop_()
        current_block.go_to()

        objects.clear_line()

    for event in p.event.get():
        if event.type == p.QUIT:
            done = True

    objects.render(stack)
    current_block.render()
    
    #print(objects.objects)
    draw_line()
    p.display.flip()

p.quit()
