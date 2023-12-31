import pygame
import random
import sys


pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("Tetris.wav")

width, height = 900, 650
info_section_width = 300
queue_piece_width = 300
block_size = 30
clock = pygame.time.Clock()
fps = 144
white = (255, 255, 255)
gray = (40, 40, 40)
black = (0, 0, 0)

tetris_shapes_dict = {
    'I': [[0, 0, 0, 0],
          [1, 1, 1, 1],
          [0, 0, 0, 0],
          [0, 0, 0, 0]],
    'O': [[1, 1],
          [1, 1]],
    'T': [[0, 1, 0],
          [1, 1, 1],
          [0, 0, 0]],
    'S': [[0, 1, 1],
          [1, 1, 0],
          [0, 0, 0]],
    'Z': [[1, 1, 0],
          [0, 1, 1],
          [0, 0, 0]],
    'J': [[1, 0, 0],
          [1, 1, 1],
          [0, 0, 0]],
    'L': [[0, 0, 1],
          [1, 1, 1],
          [0, 0, 0]],
}

piece_colors = {
    'I': (0, 255, 255),  # Light blue
    'O': (255, 255, 0),  # Yellow
    'T': (128, 0, 128),  # Magenta
    'S': (0, 255, 0),    # Green
    'Z': (255, 0, 0),    # Red
    'J': (0, 0, 255),    # Dark blue
    'L': (255, 165, 0),  # Orange
}

shapes_list = ['I','O','T','S','Z','J','L']

wall_kick = {
    '0R':[(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
    'R0':[(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
    'R2':[(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
    '2R':[(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
    '2L':[(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
    'L2':[(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    'L0':[(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    '0L':[(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)]
}

wall_kick_I = {
    '0R':[(0, 0), (-2, 0), (1, 0), (-2, 1), (1, -2)],
    'R0':[(0, 0), (2, 0), (-1, 0), (2, -1), (-1, 2)],
    'R2':[(0, 0), (-1, 0), (2, 0), (-1, -2), (2, 1)],
    '2R':[(0, 0), (1, 0), (-2, 0), (1, 2), (-2, -1)],
    '2L':[(0, 0), (2, 0), (-1, 0), (2, -1), (-1, 2)],
    'L2':[(0, 0), (-2, 0), (1, 0), (-2, 1), (1, -2)],
    'L0':[(0, 0), (1, 0), (-2, 0), (1, 2), (-2, -1)],
    '0L':[(0, 0), (-1, 0), (2, 0), (-1, -2), (2, 1)]
}

clock_wise = {
    '0':'R',
    'R':'2',
    '2':'L',
    'L':'0'
}

anti_clock_wise = {
    '0':'L',
    'R':'0',
    '2':'R',
    'L':'2'
}


random.shuffle(shapes_list)

class Tetris:
    def __init__(self, high_score = 0):
        #tablero
        self.width = 10
        self.height = 20
        self.board = [[None] * self.width for _ in range(self.height)]
        #piezas
        self.bag = random.shuffle(shapes_list.copy())
        self.queue_pieces = [self.next_bag() for _ in range(3)]
        self.current_piece = self.new_piece()
        self.hold = False
        self.save_piece = None
        #info
        self.game_over_bool = False
        self.level = 1
        self.score = 0
        self.high_score = high_score
        self.lines = 0
        #combos
        self.combos = -1
        #caida
        self.last_time = pygame.time.get_ticks()
        self.drop_time = self.fall_time()
        #musica
        pygame.mixer.music.play(-1)

    def new_piece(self):
        #entrega la primera pieza en la queue de salida
        shape = self.queue_pieces.pop(0)
        self.queue_pieces.append(self.next_bag())
        return shape
    
    def next_bag(self):
        #si la bolsa esta vacia, la llena
        if not self.bag:
            self.bag = shapes_list.copy()
            random.shuffle(self.bag)
        #saca un valor de la bolsa
        shape_name = self.bag.pop(0)
        #le asigna este valor a una pieza y la entrega
        color = piece_colors.get(shape_name)
        shape = tetris_shapes_dict.get(shape_name)
        piece = {'shape': shape, 'x': self.width // 2 - len(shape[0]) // 2, 'y': -2, 'color': color, 'state': '0', 'shape_name':shape_name}
        return piece

    def check_collision(self, piece = None):
        current_piece = piece or self.current_piece
        for y, row in enumerate(current_piece['shape']):
            for x, cell in enumerate(row):
                if cell and (current_piece['x'] + x < 0 or #borde izquierdo
                             current_piece['x'] + x >= self.width or #borde derecho
                             current_piece['y'] + y >= self.height or #borde inferior
                             (current_piece['y'] + y >=0 and #borde superior
                              self.board[current_piece['y'] + y][current_piece['x'] + x])): #punto en el tablero 
                    return True
        return False

    def merge_piece(self):
        #posiciona las piezas unidas en el tablero
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    if self.current_piece['y'] + y <0:
                        self.game_over()
                    self.board[self.current_piece['y'] + y][self.current_piece['x'] + x] = self.current_piece['color']
        
        #revisa las filas completas
        complete_rows = []
        for y, row in enumerate(self.board):
            if all(cell is not None for cell in row):
                complete_rows.append(y)
        #Limpia las filas
        for row in complete_rows:
            #elimina la fila
            del self.board[row]
            #inserta una nueva con None en el inicio.
            self.board.insert(0, [None] * self.width)
        if len(complete_rows) > 0:
            self.combos +=1
        else:
            self.combos = -1
        #Se inserto una pieza, se libera la opcion hold.
        self.hold = False
        #se cuentan las lineas para el nivel.
        self.lines += len(complete_rows)
        #se actualiza el score con las lineas.
        self.update_score(len(complete_rows))
        #se actualiza el nivel.
        self.update_level()
        
        #pieza nueva
        self.current_piece = self.new_piece()
        if not self.can_place_new_piece():
            self.game_over()

    def can_place_new_piece(self):
        #si no hay pieza se retorna
        if self.current_piece is None:
            return True
        #pieza actual
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell: #celdas con 1
                    #posicion de cada celda en el tablero
                    board_x = self.current_piece['x'] + x
                    board_y = self.current_piece['y'] + y
                    if (
                        board_x < 0 #borde izquierdo
                        or board_x >= self.width #borde derecho
                        or board_y >= self.height #borde inferior
                        or (board_y >= 0 and self.board[board_y][board_x] is not None) #celda
                    ):
                        return False

        return True

    def rotate_piece(self, clockwise=True):
        old_piece = self.current_piece.copy()
        rot = self.current_piece['state']
        if clockwise:
            self.current_piece['shape'] = list(zip(*reversed(self.current_piece['shape'])))
            self.current_piece['state']= clock_wise[rot]
            rot = rot + clock_wise[rot]
        else:
            self.current_piece['shape'] = list(reversed(list(zip(*self.current_piece['shape']))))
            self.current_piece['state']= anti_clock_wise[rot]
            rot = rot + anti_clock_wise[rot]
        if self.check_collision():
            if self.current_piece['shape_name'] == 'O':
                kick = []
            elif self.current_piece['shape_name'] == 'I':
                kicks = wall_kick_I[rot]
            else:
                kicks = wall_kick[rot]
            for kick in kicks:
                #prueba el kick
                self.move_piece(kick[0], kick[1])
                if not self.check_collision():
                    return
                #invierte el kick
                self.move_piece(-kick[0], -kick[1])

            self.current_piece = old_piece

    def move_piece(self, dx, dy):
        self.current_piece['x'] += dx
        self.current_piece['y'] += dy
    
    def hard_drop(self):
        while not self.check_collision():
            self.move_piece(0, 1)
            self.score += 2
        self.move_piece(0, -1)
        self.score = self.score-2
        self.merge_piece()

    def hold_piece(self):
        if not self.hold:
            piece = self.current_piece
            if self.save_piece:
                self.current_piece = self.save_piece
            else:
                self.current_piece = self.new_piece()
            
            self.save_piece = piece
            self.save_piece['shape'] = tetris_shapes_dict[piece['shape_name']]
            self.save_piece['state'] = '0'
            self.save_piece['x'] = self.width // 2 - len(self.save_piece["shape"][0])
            self.save_piece['y'] = -1
            self.hold = True

    def calculate_shadow_position(self):
        shadow_piece = self.current_piece.copy()
        while not self.check_collision(piece=shadow_piece):
            shadow_piece['y'] += 1
        shadow_piece['y'] -= 1
        return shadow_piece
            
    def game_over(self):
        pygame.mixer.music.stop()
        if self.high_score < self.score: self.high_score = self.score 
        self.game_over_bool = True
    
    def fall_time(self):
        return (0.8 - ((self.level - 1) *0.007))**(self.level - 1)*1000

    def update_score(self, complete_lines):
        if all(all(cell is None for cell in row) for row in self.board):
            if complete_lines == 1:
                self.score += 800 * self.level
            elif complete_lines == 2:
                self.score += 1200 * self.level
            elif complete_lines == 3:
                self.score += 1800 * self.level
            elif complete_lines == 4:
                self.score += 2000 * self.level
        else:
            if complete_lines == 1:
                self.score += 100 * self.level
            elif complete_lines == 2:
                self.score += 300 * self.level
            elif complete_lines == 3:
                self.score += 500 * self.level
            elif complete_lines == 4:
                self.score += 800 * self.level
        if self.combos>0:
            self.score += 50 * self.combos * self.level

    def update_level(self):
        self.level = self.lines//10 + 1

    def update(self):
        draw_info(self, 10)
        if not self.game_over_bool:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.last_time
            self.last_time = current_time

            self.drop_time -= elapsed_time
            if self.drop_time <= 0:
                self.move_piece(0, 1)
                if self.check_collision():
                    self.move_piece(0, -1)
                    self.merge_piece()
                self.drop_time = self.fall_time()

            draw_board(self, info_section_width)
            draw_piece(self, info_section_width)
            draw_next_pieces(self, width-queue_piece_width + 10)
            draw_hold_piece(self, 10)
            if self.combos > 0:
                draw_combo(self, 10)
        else:
            font = pygame.font.Font(None, 50)
            text = font.render("Game Over", True, white)
            restart = text.get_rect(center=(width // 2, height // 2))
            screen.blit(text, restart)



def draw_rect(x, y, color, back_color = black):
    pygame.draw.rect(screen, color, (x, y, block_size, block_size), 0)
    pygame.draw.rect(screen, back_color, (x, y, block_size, block_size), 1)

def draw_text(x,y, text):
    font = pygame.font.Font(None, 36)
    show_text = font.render(text, True, white)
    screen.blit(show_text, (x,y))

def draw_board(tetris: Tetris, width):
    height = 25
    for y, row in enumerate(tetris.board):
        for x, cell in enumerate(row):
            draw_rect(width + x * block_size, height + (y) * block_size, black, gray)
            if cell:
                draw_rect(width + x * block_size, height + (y) * block_size, cell)

def draw_piece(tetris: Tetris, width):
    height = 25
    shape = tetris.current_piece['shape']

    shadow_piece = tetris.calculate_shadow_position()
    for y, row in enumerate(shadow_piece['shape']):
        for x, cell in enumerate(row):
            if cell:
                if shadow_piece['y']+y >= 0:
                    shadow_color = (100, 100, 100)
                    draw_rect(width + (shadow_piece['x'] + x) * block_size,
                            height + (shadow_piece['y'] + (y)) * block_size, 
                            shadow_color)  


    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                if tetris.current_piece['y']+y >= 0:
                    draw_rect(width + (tetris.current_piece['x'] + x) * block_size,
                            height + (tetris.current_piece['y'] + (y)) * block_size, 
                            tetris.current_piece['color'])

def draw_next_pieces(tetris: Tetris, width):
    draw_text(width, 10, "next:")

    next_pieces = tetris.queue_pieces # Muestra las siguientes tres piezas
    for i, piece in enumerate(next_pieces):
        shape = piece["shape"]
        color = piece["color"]
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    draw_rect((width + 50) + x* block_size,
                              60 + (y + i * 3) * block_size,
                              color)

def draw_info(tetris: Tetris, width):
    draw_text(width, 10, f"Level: {tetris.level}")
    draw_text(width, 60, f"Score: {tetris.score}")
    draw_text(width, 110, f"High Score: {tetris.high_score}")
    draw_text(width, 160, f"Lines: {tetris.lines}")

def draw_hold_piece(tetris: Tetris, width):
    draw_text(width,260,"stored:")
    if tetris.save_piece:
        shape = tetris.save_piece['shape']
        color = tetris.save_piece['color']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    draw_rect((width) + x * block_size,
                                300 + y * block_size,
                                color)

def draw_combo(tetris:Tetris, width):
    draw_text(width, 400, f"Combo {tetris.combos}")

tetris = Tetris()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tetris")

while True:
    screen.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if not tetris.game_over_bool:
                if event.key == pygame.K_LEFT:
                    tetris.move_piece(-1, 0)
                    if tetris.check_collision():
                        tetris.move_piece(1, 0)
                elif event.key == pygame.K_RIGHT:
                    tetris.move_piece(1, 0)
                    if tetris.check_collision():
                        tetris.move_piece(-1, 0)
                elif event.key == pygame.K_DOWN:
                    tetris.move_piece(0, 1)
                    if tetris.check_collision():
                        tetris.move_piece(0, -1)
                    else:
                        tetris.score += 1
                elif event.key == pygame.K_UP:
                    tetris.rotate_piece(True)
                elif event.key == pygame.K_z or event.key == pygame.K_LCTRL:
                    tetris.rotate_piece(False)
                elif event.key == pygame.K_SPACE:  
                    tetris.hard_drop()
                elif event.key == pygame.K_c or event.key == pygame.K_LSHIFT:
                    tetris.hold_piece()
            elif event.key == pygame.K_r:
                tetris = Tetris(tetris.high_score)
    
    tetris.update()
    pygame.display.flip()
    clock.tick(fps)