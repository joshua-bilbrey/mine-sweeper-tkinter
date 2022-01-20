from turtle import RawTurtle
import random

EASY = 10  # number to divide total tiles by for number of mines
MEDIUM = 8
HARD = 6
DIFFICULTY = EASY


class Tile(RawTurtle):
    """Tile class for minesweeper program."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.penup()
        self.shape("square")
        self.pencolor("black")
        self.fillcolor("white")

        self.is_mine = False
        self.is_flagged = False
        self.is_left_clicked = False
        self.number = 0


class TileManager:
    """Tile manager."""

    def __init__(self):
        self.tiles = []
        self.mines = []
        self.y_coors = []
        self.x_coors = []
        self.num_mines = 0
        self.closest_tile = False  # used as filler for start code
        self.right_click = False

    def create_tiles(self, columns: int, rows: int, canvas):
        self.y_coors = [((rows / 2) * 20) * -1, ((rows / 2) * 20)]
        self.x_coors = [((columns / 2) * 20) * -1, ((columns / 2) * 20)]
        y_coor = self.y_coors[0] + 10
        for row in range(rows):
            x_coor = self.x_coors[0] + 10
            for column in range(columns):
                new_tile = Tile(canvas)
                new_tile.goto(x_coor, y_coor)
                self.tiles.append(new_tile)
                x_coor += 20
            y_coor += 20
        self.set_mines()
        self.set_hints()

    def set_mines(self):
        self.num_mines = int(len(self.tiles) / DIFFICULTY)
        for num in range(self.num_mines):
            not_mine = True
            while not_mine:
                current_tile = random.choice(self.tiles)
                if not current_tile.is_mine:
                    current_tile.is_mine = True
                    not_mine = False
            self.mines.append(current_tile)

    def set_hints(self):
        for tile in self.tiles:
            mines_nearby = 0
            if tile.is_mine is not True:
                for other_tile in self.tiles:
                    if tile.pos() != other_tile.pos() and tile.distance(other_tile) < 30 and other_tile.is_mine is True:
                        mines_nearby += 1
                tile.number = mines_nearby

    def find_closest_tile(self, x, y):
        if self.x_coors[0] <= x <= self.x_coors[1] and self.y_coors[0] <= y <= self.y_coors[1]:
            distance = 100
            for tile in self.tiles:
                if tile.distance(x, y) < distance:
                    distance = tile.distance(x, y)
                    self.closest_tile = tile

    def find_grey_tiles(self, tile):
        tile_dict = {"grey_tiles": [tile], "nearby_tiles": []}
        number_of_tiles = len(tile_dict["grey_tiles"])
        while True:
            for grey_tile in tile_dict["grey_tiles"]:
                for tile in self.tiles:
                    if grey_tile.distance(tile) < 22 and tile.number == 0 and tile not in tile_dict["grey_tiles"]:
                        tile_dict["grey_tiles"].append(tile)
            if number_of_tiles == len(tile_dict["grey_tiles"]):
                break
            else:
                number_of_tiles = len(tile_dict["grey_tiles"])
        for grey_tile in tile_dict["grey_tiles"]:
            for tile in self.tiles:
                if grey_tile.distance(tile) < 30 and tile not in tile_dict["nearby_tiles"] and tile.number != 0:
                    tile_dict["nearby_tiles"].append(tile)
        return tile_dict

    def click_tile(self, x, y):
        self.find_closest_tile(x, y)
        self.right_click = False

    def right_click_tile(self, x, y):
        self.find_closest_tile(x, y)
        self.right_click = True
        if self.closest_tile.is_left_clicked is False:
            if self.closest_tile.is_flagged is True:
                self.closest_tile.is_flagged = False
            else:
                self.closest_tile.is_flagged = True
