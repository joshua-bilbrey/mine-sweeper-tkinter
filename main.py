import turtle
import time
from tkinter import *
from tile_manager import TileManager

COLUMNS = 10
ROWS = 10
FONT = ("Arial", 16, "bold")

screen_width = COLUMNS * 20 + 50
screen_height = ROWS * 20 + 50
write_top = screen_height / 2 - 15
write_bottom = (screen_height / 2) * -1
hint_images = [f"images/hint{num}.gif" for num in range(9)]
game_on = True

window = Tk()
window.title("Minesweeper")
canvas = Canvas()
canvas.config(width=screen_width*1.1, height=screen_height*1.1)
canvas.pack()
screen = turtle.TurtleScreen(canvas)
screen.tracer(0)

for num in range(8):
    screen.addshape(hint_images[num + 1])
screen.addshape("images/flag.gif")
screen.addshape("images/mine.gif")
screen.addshape("images/mine_click.gif")

tile_manager = TileManager()
tile_manager.create_tiles(COLUMNS, ROWS, screen)

screen.listen()
screen.onscreenclick(fun=tile_manager.click_tile)
screen.onscreenclick(fun=tile_manager.right_click_tile, btn=3)

writer = turtle.RawTurtle(canvas)
writer.penup()
writer.hideturtle()

while game_on:
    time.sleep(0.05)
    writer.clear()
    selected_tile = tile_manager.closest_tile
    if selected_tile is not False:
        # check if left click
        if tile_manager.right_click is False:
            if selected_tile.is_flagged is False:
                # detect mine explosion
                if selected_tile.is_mine is True:
                    selected_tile.shape("images/mine_click.gif")
                    game_on = False
                    writer.goto(0, write_bottom)
                    writer.write("GAME OVER", font=FONT, align="center")
                    other_mines = [mine for mine in tile_manager.mines if mine != selected_tile]
                    for mine in other_mines:
                        mine.shape("images/mine.gif")
                elif selected_tile.number > 0:
                    selected_tile.shape(hint_images[selected_tile.number])
                # reveal surrounding grey tiles
                elif selected_tile.number == 0:
                    new_dict = tile_manager.find_grey_tiles(selected_tile)
                    grey_tiles = new_dict["grey_tiles"]
                    grey_adjacent_tiles = new_dict["nearby_tiles"]
                    for tile in grey_tiles:
                        tile.color("gray")
                    for tile in grey_adjacent_tiles:
                        tile.shape(hint_images[tile.number])

            selected_tile.is_left_clicked = True

        # otherwise is is right click
        else:
            if selected_tile.is_left_clicked is False:
                if selected_tile.is_flagged is True:
                    selected_tile.shape("images/flag.gif")
                else:
                    selected_tile.shape("square")

    # detect number of flags for "score"
    flagged_tiles = [tile for tile in tile_manager.tiles if tile.is_flagged is True]
    score = len(flagged_tiles)
    writer.goto(0, write_top)
    writer.write(f"Flagged Mines: {score}", font=FONT, align="center")

    # detect if player won game
    discovered_mines = 0
    for tile in flagged_tiles:
        if tile in tile_manager.mines:
            discovered_mines += 1
    if discovered_mines == tile_manager.num_mines:
        game_on = False
        writer.goto(0, write_bottom)
        writer.write("Congratulations!", font=FONT, align="center")

    screen.update()

screen.mainloop()
