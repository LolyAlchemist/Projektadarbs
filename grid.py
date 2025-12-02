from random import sample
from selection import SelectNumber
from copy import deepcopy
import random

def create_line_coordinates(cell_size: int) -> list[list[tuple]]:
    points = []
    for y in range(0, 10):
        temp = []
        temp.append((0, y * cell_size))
        temp.append((900, y * cell_size))
        points.append(temp)

    for x in range(0, 10):
        temp = []
        temp.append((x * cell_size, 0))
        temp.append((x *cell_size, 900))
        points.append(temp)

    return points


SUB_GRID_SIZE = 3
GRID_SIZE = SUB_GRID_SIZE * SUB_GRID_SIZE


def pattern(row_num: int, col_num: int) -> int:
    return (SUB_GRID_SIZE * (row_num % SUB_GRID_SIZE) + row_num // SUB_GRID_SIZE + col_num) % GRID_SIZE


def shuffle(samp: range) -> list:
    return sample(samp, len(samp))

def create_grid(sub_grid: int) -> list[list]:
    row_base = range(sub_grid)
    rows = [g * sub_grid + r for g in shuffle(row_base) for r in shuffle(row_base)]
    cols = [g * sub_grid + c for g in shuffle(row_base) for c in shuffle(row_base)]
    nums = shuffle(range(1, sub_grid * sub_grid + 1))
    return [[nums[pattern(r, c)] for c in cols] for r in rows]


def remove_numbers(grid: list[list]) -> None:
    num_of_cells = GRID_SIZE * GRID_SIZE
    empties = num_of_cells * 3 // 7 # mazaks cipars grutak, lielaks vieglaka spele
    for i in sample(range(num_of_cells), empties):
        grid[i // GRID_SIZE][i % GRID_SIZE] = 0


class Grid:
    def __init__(self, pygame, font):
        self.cell_size = 100
        self.line_coordinates = create_line_coordinates(self.cell_size)

        self.grid = create_grid(SUB_GRID_SIZE)
        self.__test_grid = deepcopy(self.grid)
        self.win = False

        self.game_font = font

        self.num_x_offset = 40
        self.num_y_offset = 35

        remove_numbers(self.grid)
        self.occupied_cell_coordinates = self.pre_occupied_cells()

        self.selection = SelectNumber(pygame, self.game_font)

        self.bomb_img = pygame.image.load("bomb.png").convert_alpha()
        self.bomb_img = pygame.transform.scale(self.bomb_img, (60, 60))
        self.bombs = []
        self.generate_bombs()

    def restart(self) -> None:
        self.grid = create_grid(SUB_GRID_SIZE)
        self.__test_grid = deepcopy(self.grid)
        remove_numbers(self.grid)
        self.occupied_cell_coordinates = self.pre_occupied_cells()
        self.win = False
        self.generate_bombs()

    def check_grids(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] != self.__test_grid[y][x]:
                    return False
        return True

    def is_cell_preoccupied(self, x:int, y:int) -> bool:
        return (y, x) in self.occupied_cell_coordinates

    def get_mouse_click(self, x: int, y: int) -> None:
        if x <= 900 and y <= 900:
            grid_x, grid_y = x // 100, y // 100
            if not self.is_cell_preoccupied(grid_x, grid_y):
                self.set_cell(grid_x, grid_y, self.selection.selected_number)
        self.selection.button_clicked(x, y)
        if self.check_grids():
            self.win = True

    def pre_occupied_cells(self) -> list[tuple]:
        occupied_cell_coordinates = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.get_cell(x,y) != 0:
                    occupied_cell_coordinates.append((y, x))
        return occupied_cell_coordinates

    def __draw_lines(self, pg, surface) -> None:
        for index, point in enumerate(self.line_coordinates):
            if index in (3, 6, 13, 16):
                color = (255, 255, 255)
            else:
                color = (126, 39, 150)
            pg.draw.line(surface, color, point[0], point[1])

    def __draw_numbers(self, surface) -> None:
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if (y, x) in self.bombs:
                    surface.blit(
                        self.bomb_img,
                        (x * self.cell_size + 20, y * self.cell_size + 10)
                    )
                    continue

                if self.get_cell(x, y) != 0:
                    if (y, x) in self.occupied_cell_coordinates:
                        text_surface = self.game_font.render(
                            str(self.get_cell(x, y)),
                            False,
                            (0, 200, 250)
                        )
                    else:
                        text_surface = self.game_font.render(
                            str(self.get_cell(x, y)),
                            False,
                            (126, 39, 150)
                        )

                    if self.get_cell(x, y) != self.__test_grid[y][x]:
                        text_surface = self.game_font.render(
                            str(self.get_cell(x, y)),
                            False,
                            (255, 0, 0)
                        )

                    surface.blit(
                        text_surface,
                        (x * self.cell_size + self.num_x_offset,
                         y * self.cell_size + self.num_y_offset)
                    )

    def generate_bombs(self):
        bombs = []
        used_blocks = set()

        attempts = 0
        while len(bombs) < 2 and attempts < 1000:
            attempts += 1
            row = random.randint(0, 8)
            col = random.randint(0, 8)

            block_row = row // 3
            block_col = col // 3
            block_id = (block_row, block_col)

            if block_id in used_blocks:
                continue

            used_blocks.add(block_id)
            bombs.append((row, col))

        if len(bombs) < 2:
            bombs = [(0, 0), (3, 3)]

        self.bombs = bombs
        return bombs

    def draw_all(self, pg, surface):
        self.__draw_lines(pg, surface)
        self.__draw_numbers(surface)
        self.selection.draw(pg, surface)

    def get_cell(self, x:int, y:int) -> int:
        return self.grid[y][x]

    def set_cell(self, x:int, y:int, value:int) -> None:
        self.grid[y][x] = value
