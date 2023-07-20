from var import COLOR, BOARD_LEFT, BOARD_TOP

class Mino:
    def __init__(self, shape, name, color, x=BOARD_LEFT + 4, y=BOARD_TOP-1):
        self.x = x
        self.y = y

        self.spin = 0

        self.shape = shape
        self.name = name
        self.color = color

        self.counter = 0

        self.state = [False, False, False, False, False]

    def spining(self, key):
        self.spin += key
        self.spin %= 4

    def move(self, x, y):
        self.x += x
        self.y += y

    def to_object(self):
        obj = []
        for block in self.shape[self.spin]:
            obj.append({'x' : self.x + block[0], 'y' : self.y + block[1], 'color' : self.color})
        
        return obj

class I_mino(Mino):
    def __init__(self):
        shape = [
            [
                [0, 1],
                [1, 1],
                [2, 1],
                [3, 1]
            ], 
            [
                [2, 0],
                [2, 1],
                [2, 2],
                [2, 3]
            ],
            [
                [0, 2],
                [1, 2],
                [2, 2],
                [3, 2]
            ],
            [
                [1, 0],
                [1, 1],
                [1, 2],
                [1, 3]
            ]
        ]

        name = 'I'

        color = COLOR['light_blue']
        super().__init__(shape, name, color, BOARD_LEFT + 4, BOARD_TOP-2)

class J_mino(Mino):
    def __init__(self):
        shape = [
            [
                [0, 0],
                [0, 1],
                [1, 1],
                [2, 1]
            ],
            [
                [1, 0],
                [2, 0],
                [1, 1],
                [1, 2]
            ],
            [
                [0, 1],
                [1, 1],
                [2, 1],
                [2, 2]
            ],
            [
                [1, 0],
                [1, 1],
                [0, 2],
                [1, 2]
            ]
        ]

        name = 'J'

        color = COLOR['blue']
        super().__init__(shape, name, color)

class L_mino(Mino):
    def __init__(self):
        shape = [
            [
                [2, 0],
                [0, 1],
                [1, 1],
                [2, 1]
            ],
            [
                [1, 0],
                [1, 1],
                [1, 2],
                [2, 2]
            ],
            [
                [0, 1],
                [1, 1],
                [2, 1],
                [0, 2]
            ],
            [
                [0, 0],
                [1, 0],
                [1, 1],
                [1, 2]
            ]
        ]

        name = 'L'

        color = COLOR['orange']
        super().__init__(shape, name, color)

class S_mino(Mino):
    def __init__(self):
        shape = [
            [
                [1, 0],
                [2, 0],
                [0, 1],
                [1, 1]
            ],
            [
                [1, 0],
                [1, 1],
                [2, 1],
                [2, 2]
            ],
            [
                [1, 1],
                [2, 1],
                [0, 2],
                [1, 2]
            ],
            [
                [0, 0],
                [0, 1],
                [1, 1],
                [1, 2]
            ]
        ]

        name = 'S'

        color = COLOR['green']
        super().__init__(shape, name, color)

class Z_mino(Mino):
    def __init__(self):
        shape = [
            [
                [0, 0],
                [1, 0],
                [1, 1],
                [2, 1]
            ],
            [
                [2, 0],
                [1, 1],
                [2, 1],
                [1, 2]
            ],
            [
                [0, 1],
                [1, 1],
                [1, 2],
                [2, 2]
            ],
            [
                [1, 0],
                [0, 1],
                [1, 1],
                [0, 2]
            ]
        ]

        name = 'Z'

        color = COLOR['red']
        super().__init__(shape, name, color)

class T_mino(Mino):
    def __init__(self):
        shape = [
            [
                [1, 0],
                [0, 1],
                [1, 1],
                [2, 1]
            ],
            [
                [1, 0],
                [1, 1],
                [2, 1],
                [1, 2]
            ],
            [
                [0, 1],
                [1, 1],
                [2, 1],
                [1, 2]
            ],
            [
                [1, 0],
                [0, 1],
                [1, 1],
                [1, 2]
            ]
        ]

        name = 'T'

        color = COLOR['purple']
        super().__init__(shape, name, color)

class O_mino(Mino):
    def __init__(self):
        shape = [
            [
                [1, 0],
                [2, 0],
                [1, 1],
                [2, 1]
            ],
            [
                [1, 0],
                [2, 0],
                [1, 1],
                [2, 1]
            ],
            [
                [1, 0],
                [2, 0],
                [1, 1],
                [2, 1]
            ],
            [
                [1, 0],
                [2, 0],
                [1, 1],
                [2, 1]
            ]
        ]

        name = 'O'

        color = COLOR['yellow']
        super().__init__(shape, name, color)
