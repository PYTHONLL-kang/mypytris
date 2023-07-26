# rule : Mino.state : 0=l_collide, 1=r_collide, 2=b_collide

import pygame as pyg
import time

from utillity import Bag, Hold, Stack_manager
from var import COLOR, BLOCK_SIZE, SCREEN_SIZE, BOARD_SIZE, BOARD_LEFT, BOARD_TOP, KICK_TABLE, I_KICK_TABLE

pyg.init()

class Environment:
    def __init__(self):
        self.clock = pyg.time.Clock()
        self.screen = pyg.display.set_mode(SCREEN_SIZE)
        self.font = pyg.font.SysFont('arial', BLOCK_SIZE, True, True)

        self.mino = None

        self.bag = Bag()
        self.hold = Hold()
        self.stack = Stack_manager()

        self.done = False
        self.time = time.time()
        self.past_spin = 0
        self.cleard_line = 0

        self.collision = {
            (i, j) : True if i == BOARD_LEFT or i == BOARD_SIZE[0]+BOARD_LEFT+1 or j == BOARD_SIZE[1]+BOARD_TOP else False
            for i in range(BOARD_LEFT, BOARD_SIZE[0]+BOARD_LEFT+2)
            for j in range(BOARD_TOP-2, BOARD_SIZE[1]+BOARD_TOP+2)
        }

    def key_input(self):
        key = pyg.key.get_pressed()
        self.check_collide()
        if key[pyg.K_ESCAPE]:
            self.done = True

        if not self.mino.state[0] and key[pyg.K_LEFT]:
            self.mino.move(-1, 0)

        if not self.mino.state[1] and key[pyg.K_RIGHT]:
            self.mino.move(1, 0)

        if not self.mino.state[3]:
            if key[pyg.K_DOWN]:
                self.mino.move(0, 1)
            
            if self.mino.counter % 30 == 0:
                self.mino.move(0, 1)

        if key[pyg.K_x]:
            self.mino.spining(1)

        if key[pyg.K_z]:
            self.mino.spining(-1)

        if key[pyg.K_a]:
            self.mino.spining(2)

        if key[pyg.K_x] or key[pyg.K_z] or key[pyg.K_a]:
            time.sleep(0.1)
            self.srs_system()

        if key[pyg.K_SPACE]:
            self.hard_drop()

        if key[pyg.K_LSHIFT] and not self.hold.is_hold:
            self.mino = self.hold.change(self.mino)
            if self.mino is None:
                self.mino = self.bag.pop_()

        if not self.mino.state[3]:
            self.time = time.time()

        elif time.time() - self.time > 1:
            self.hard_drop()

        for i in range(4):
            self.mino.state[i] = False

    def srs_system(self):
        if self.mino.name == 'I':
            kick_table = I_KICK_TABLE
            print()

        else:
            kick_table = KICK_TABLE

        for x_m, y_m in kick_table[(self.past_spin, self.mino.spin)]:
            if not self.check_collide():
                break
            self.mino.move(x_m, y_m)

        self.past_spin = self.mino.spin

    def hard_drop(self):
        while not self.mino.state[3]:
            self.mino.move(0, 1)
            self.check_collide()

        time.sleep(0.01)
        self.stack.add(self.mino)
        self.add_collision()

        line = self.stack.clear_line()
        self.delete_collision(line)
        self.mino = self.bag.pop_()
        self.hold.is_hold = False
        self.past_spin = 0

        self.cleard_line += len(line)

    def add_collision(self):
        for block in self.mino.to_object():
            self.collision[(block['x'], block['y'])] = True

    def delete_collision(self, line):
        for y in line:
            for i in range(BOARD_LEFT+1, BOARD_LEFT+BOARD_SIZE[0]+1):
                for _y in range(BOARD_TOP, y+1):
                    if self.collision[(i, _y)]:
                        self.collision[(i, _y)] = False
                        break

    def check_collide(self):
        for block in self.mino.to_object():
            try:
                if self.collision[(block['x']-1, block['y'])]:
                    self.mino.state[0] = True

                if self.collision[(block['x']+1, block['y'])]:
                    self.mino.state[1] = True

                if self.collision[(block['x'], block['y']+1)]:
                    self.mino.state[3] = True

                if self.collision[(block['x'], block['y'])]:
                    return True

            except KeyError:
                return True

        return False

    def block_render(self, obj):
        for mino in obj:
            for block in mino:
                pyg.draw.rect(self.screen, block['color'], [block['x'] * BLOCK_SIZE, block['y'] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE])

    def show_render(self):
        for i, mino in enumerate(self.bag.shows):
            for block in mino.to_object():
                pyg.draw.rect(self.screen, block['color'], [(block['x']-BOARD_LEFT+BOARD_SIZE[0]+2) * BLOCK_SIZE, (block['y']+2+i*3) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE])

    def board_render(self):
        for i in range(BOARD_SIZE[1] + 1): # left, right
            pyg.draw.rect(self.screen, COLOR['white'], [BLOCK_SIZE*BOARD_LEFT, BLOCK_SIZE*(BOARD_TOP+i), BLOCK_SIZE, BLOCK_SIZE])
            pyg.draw.rect(self.screen, COLOR['white'], [BLOCK_SIZE*(BOARD_LEFT+BOARD_SIZE[0]+1), BLOCK_SIZE*(BOARD_TOP+i), BLOCK_SIZE, BLOCK_SIZE])

        for i in range(BOARD_SIZE[0] + 2): # bottom
            pyg.draw.rect(self.screen, COLOR['white'], [BLOCK_SIZE*(BOARD_LEFT+i), BLOCK_SIZE*(BOARD_TOP + BOARD_SIZE[1]), BLOCK_SIZE, BLOCK_SIZE])

        pyg.draw.rect(self.screen, COLOR['grey'], [BLOCK_SIZE*BOARD_LEFT, BLOCK_SIZE*BOARD_TOP, BLOCK_SIZE*(BOARD_SIZE[0]+2), 1]) # top

        for i in range(5):
            pyg.draw.rect(self.screen, COLOR['white'], [BLOCK_SIZE*(BOARD_LEFT+BOARD_SIZE[0]+2), BLOCK_SIZE*(BOARD_TOP+i*3), BLOCK_SIZE*4, BLOCK_SIZE*3], 1)

        pyg.draw.rect(self.screen, COLOR['white'], [BLOCK_SIZE*0, BLOCK_SIZE*BOARD_TOP, BLOCK_SIZE*4, BLOCK_SIZE*3], 1)

    def main(self):
        pyg.display.set_caption('pytris')

        start_time = int(time.time())
        self.mino = self.bag.pop_()

        while not self.done:
            self.clock.tick(20)
            self.screen.fill(color=COLOR['black'])

            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    self.done = True

            self.key_input()

            self.block_render(self.stack.stack_objects + [self.mino.to_object()])
            self.show_render()
            self.board_render()

            if self.hold.holding is not None:
                self.block_render(self.hold.holding_block())

            text = self.font.render(str(self.cleard_line), True, COLOR['white'], COLOR['black'])
            self.screen.blit(text, (BLOCK_SIZE*(BOARD_LEFT+BOARD_SIZE[0]//2), BLOCK_SIZE*(BOARD_TOP+BOARD_SIZE[1]+2)))

            sec = int(time.time()) - start_time
            sec_text = self.font.render('{0}:{1}'.format(sec//60, sec%60), True, COLOR['white'], COLOR['black'])
            self.screen.blit(sec_text, (0, 0))

            pyg.display.flip()
            self.mino.counter += 1

game = Environment()
game.main()