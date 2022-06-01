import time
from turtle import right
import pygame as p
import random

p.init()

black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
light_blue = (0, 255, 255)
puple = (255, 0, 255)
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
    p.draw.rect(screen, white, [110, 0, 1, 540], 1)
    p.draw.rect(screen, white, [442-15, 0, 1, 540], 1)
    p.draw.rect(screen, white, [540, 110, 317, 1], 1)
    abcd = 1
    ran = [1, 2, 3, 4, 5]
    for abcd in ran:
        p.draw.line(screen, white, (442-15, (52*abcd)+(10*abcd)), (640, (52*abcd)+(10*abcd)), 1)
        abcd = abcd + 1



class Block:
    def __init__(self, X, Y, position, shape):
        self.X = X
        self.Y = Y
        self.position = position
        self.shape = shape

    def move(self, x, y):
        self.X += x
        self.Y += y

        
    def render(self):
        # print(self.X, self.Y)
        for shape in self.shape:
            draw_rect(shape["x"] + self.X, shape["y"] + self.Y, self.color)

            
    def go_to(self):
        self.X = 270
        self.Y = 0

    def to_dict(self):
        dict_object = []

        for shape in self.shape:
            dict_object.append({"x": shape["x"] + self.X, "y": shape["y"] + self.Y})

        return dict_object
    


class BlockJ(Block):
    def __init__(self, x, y, position):
        super().__init__(x, y, position, [
            {"x": 0, "y": 26},
            {"x": 26, "y": 26},
            {"x": 52, "y": 26},
            {"x": 0, "y": 0}
        ])

        self.color = blue

    def spin(self):
        pass

    
class BlockL(Block):
    def __init__(self, x, y, position):
        super().__init__(x, y, position, [
            {"x": 0, "y": 26},
            {"x": 26, "y": 26},
            {"x": 52, "y": 26},
            {"x": 52, "y": 0}
        ])
        self.color = orange



    def spin(self):
        pass

class BlockT(Block):
    def __init__(self, x, y, position):
        super().__init__(x, y, position, [
            {"x": 0, "y": 26},
            {"x": 26, "y": 26},
            {"x": 52, "y": 26},
            {"x": 26, "y": 0}
        ])
        self.color = puple


    

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
        ])
        self.color = yellow
        

    def spin(self):
        pass

class BlockZ(Block):
    def __init__(self, x, y, position):
        super().__init__(x, y, position, [
            {"x": 0, "y": 0},
            {"x": 26, "y": 26},
            {"x": 52, "y": 26},
            {"x": 26, "y": 0}
        ])
        self.color = red


    def spin(self):
        pass


class BlockS(Block):
    def __init__(self, x, y, position):
        super().__init__(x, y, position, [
            {"x": 26, "y": 0},
            {"x": 52, "y": 0},
            {"x": 26, "y": 26},
            {"x": 0, "y": 26}
        ])
        self.color = green
        

   
    def spin(self):
        pass

class BlockI(Block):
    def __init__(self, x, y, position):
        super().__init__(x, y, position, [
            {"x": 0, "y": 0},
            {"x": 26, "y": 0},
            {"x": 52, "y": 0},
            {"x": 78, "y": 0}
        ])
        self.color = light_blue
        
        

    def spin(self):
        pass


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

    def pop_(self):
        if len(self.bag) == 0:
            self.__init__()
            return self.pop_()

        print(len(self.bag))
        result = self.bag.pop(random.randrange(0, len(self.bag)))

        return result


class Objects:
    def __init__(self):
        self.objects = []

    def add(self, block):        
        self.objects.append(block)

    def render(self):
        for object in self.objects:
            object.render()


def check_collide(_object, stacks):
    for stack in stacks:
        for block in _object.to_dict():
            block_rct = p.Rect(block["x"], block["y"], 26 ,26)
            stack_rct = p.Rect(stack["x"], block["y"], 26, 26)

            if block_rct.colliderect(stack_rct):
                return True

    return False

def check_wall_collide(_object, direction):
    for block in _object:
        left_wall = p.Rect(110, 0, 1, 540)
        right_wall = p.Rect(4)


objects = Objects()

bag = Bag()
current_block = bag.pop_()

current_block.go_to()

start = 0
stack = []

while not done:
    clock.tick(30)
    screen.fill(black)
    
    current_x = current_block.X
    current_y = current_block.Y

    rct = p.Rect(current_x, current_y, 26, 26)

    current_block.move(0, 1)

    key_event = p.key.get_pressed()

    if key_event[p.K_LEFT] and current_x >= 136:
        current_block.move(-26, 0)

    if key_event[p.K_RIGHT]:
        current_block.right_wall()

    if key_event[p.K_DOWN]:
        current_block.move(0, 26)


    if  current_y >=  485 and key_event[p.K_DOWN] or check_collide(current_block, stack) and key_event[p.K_DOWN]:
        current_block.stop_bottom()
        #start = start + 1
        #if start == 50:
        
        for block in current_block.to_dict(): # 쌓인 블럭에 데이터 추가
            stack.append(block)
            
        objects.add(current_block)

        current_block = bag.pop_()
        current_block.go_to()
        start = 0

    elif current_y >= 485 or key_event[p.K_SPACE]:
        current_block.stop_bottom()
        
        for block in current_block.to_dict(): # 쌓인 블럭에 데이터 추가
            stack.append(block)
            
        time.sleep(0.1)
        objects.add(current_block)

        current_block = bag.pop_()
        current_block.go_to()
        start = 0
        
            

    for event in p.event.get():
        if event.type == p.QUIT:
            done = True

    objects.render()
    current_block.render()
    
    #print(objects.objects)
    draw_line()
    p.display.flip()

p.quit()
