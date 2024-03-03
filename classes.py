import pygame
from constants import *
from copy import deepcopy


class SokobanGame:

    def __init__(self):
        pygame.init()
        self.initialize_screen()
        self.initialize_images()
        self.initialize_sound()
        self.levels = self.load_levels()
        self.selected_level = 1
        self.victory = False
        self.dir = "down"
        self.move = None
        self.running = True

    def initialize_screen(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Sokoban")
        icon = pygame.image.load("assets/images/icon.png")
        pygame.display.set_icon(icon)

    def initialize_images(self):
        self.wall_img = pygame.image.load("assets/images/wall.png").convert_alpha()
        self.wall_img = pygame.transform.smoothscale(self.wall_img, (TILE_SIZE, TILE_SIZE))
        self.floor_img = pygame.image.load("assets/images/ground.png").convert_alpha()
        self.floor_img = pygame.transform.smoothscale(self.floor_img, (TILE_SIZE, TILE_SIZE))
        self.x_img = pygame.image.load("assets/images/x.png").convert_alpha()
        self.x_img = pygame.transform.smoothscale(self.x_img, (TILE_SIZE, TILE_SIZE))
        self.crate_img = pygame.image.load("assets/images/crate.png").convert_alpha()
        self.crate_img = pygame.transform.smoothscale(self.crate_img, (TILE_SIZE, TILE_SIZE))
        self.up_img = pygame.image.load("assets/images/up.png").convert_alpha()
        self.up_img = pygame.transform.smoothscale(self.up_img, (TILE_SIZE, TILE_SIZE))
        self.down_img = pygame.image.load("assets/images/down.png").convert_alpha()
        self.down_img = pygame.transform.smoothscale(self.down_img, (TILE_SIZE, TILE_SIZE))
        self.left_img = pygame.image.load("assets/images/left.png").convert_alpha()
        self.left_img = pygame.transform.smoothscale(self.left_img, (TILE_SIZE, TILE_SIZE))
        self.right_img = pygame.image.load("assets/images/right.png").convert_alpha()
        self.right_img = pygame.transform.smoothscale(self.right_img, (TILE_SIZE, TILE_SIZE))

    def initialize_sound(self):
        pygame.mixer.init()
        self.step_sound = pygame.mixer.Sound("assets/sound/step.mp3")
        self.step_sound.set_volume(0.1)

    def load_levels(self):
        with open(FILENAME) as file:
            levels = []
            for line in file:
                line = line.rstrip()
                if line:
                    if line.startswith("LEVEL"):
                        level = {"map": [], "player": [], "crates": []}
                    elif line.startswith("P: "):
                        x, y = map(int, line[3:].split(","))
                        level["player"].append((x, y))
                    elif line.startswith("C: "):
                        crates = line[3:].split()
                        for crate in crates:
                            x, y = map(int, crate.split(","))
                            level["crates"].append((x, y))
                    elif line == "END LEVEL":
                        levels.append(level)
                    else:
                        level["map"].append(line)
        return tuple(levels)

    def lunch(self):
        self.level_copy = self.copy_level()
        while self.running:
            self.handle_events()
            self.update_logic()
            self.update_screen()

    def copy_level(self):
        level_copy = deepcopy(self.levels[self.selected_level - 1])
        self.dir = "down"
        return level_copy

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.victory:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if self.selected_level < len(self.levels):
                        self.selected_level += 1
                    self.level_copy = self.copy_level()
                    self.victory = False
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.move = "down"
                    elif event.key == pygame.K_UP:
                        self.move = "up"
                    elif event.key == pygame.K_LEFT:
                        self.move = "left"
                    elif event.key == pygame.K_RIGHT:
                        self.move = "right"
                    elif event.key == pygame.K_ESCAPE:
                        self.level_copy = self.copy_level()

    def update_logic(self):
        if self.move:
            self.step_sound.play()
            if self.move == "up":
                self.dir = "up"
                self.update_move_up()
            elif self.move == "down":
                self.dir = "down"
                self.update_move_down()
            elif self.move == "left":
                self.dir = "left"
                self.update_move_left()
            elif self.move == "right":
                self.dir = "right"
                self.update_move_right()
            self.move = None
            self.check_victory()

    def update_move_up(self):
        x, y = self.level_copy["player"][0]
        if (x, y - 1) in self.level_copy["crates"]:
            if (x, y - 2) not in self.level_copy["crates"] \
                    and self.level_copy["map"][y - 2][x] != "#":
                self.level_copy["crates"].remove((x, y - 1))
                self.level_copy["crates"].append((x, y - 2))
        if self.level_copy["map"][y - 1][x] in ("-", "X") \
                and (x, y - 1) not in self.level_copy["crates"]:
            self.level_copy["player"].pop()
            self.level_copy["player"].append((x, y - 1))

    def update_move_down(self):
        x, y = self.level_copy["player"][0]
        if (x, y + 1) in self.level_copy["crates"]:
            if (x, y + 2) not in self.level_copy["crates"] \
                    and self.level_copy["map"][y + 2][x] != "#":
                self.level_copy["crates"].remove((x, y + 1))
                self.level_copy["crates"].append((x, y + 2))
        if self.level_copy["map"][y + 1][x] in ("-", "X") \
                and (x, y + 1) not in self.level_copy["crates"]:
            self.level_copy["player"].pop()
            self.level_copy["player"].append((x, y + 1))

    def update_move_left(self):
        x, y = self.level_copy["player"][0]
        if (x - 1, y) in self.level_copy["crates"]:
            if (x - 2, y) not in self.level_copy["crates"] \
                    and self.level_copy["map"][y][x - 2] != "#":
                self.level_copy["crates"].remove((x - 1, y))
                self.level_copy["crates"].append((x - 2, y))
        if self.level_copy["map"][y][x - 1] in ("-", "X") \
                and (x - 1, y) not in self.level_copy["crates"]:
            self.level_copy["player"].pop()
            self.level_copy["player"].append((x - 1, y))

    def update_move_right(self):
        x, y = self.level_copy["player"][0]
        if (x + 1, y) in self.level_copy["crates"]:
            if (x + 2, y) not in self.level_copy["crates"] \
                    and self.level_copy["map"][y][x + 2] != "#":
                self.level_copy["crates"].remove((x + 1, y))
                self.level_copy["crates"].append((x + 2, y))
        if self.level_copy["map"][y][x + 1] in ("-", "X") \
                and (x + 1, y) not in self.level_copy["crates"]:
            self.level_copy["player"].pop()
            self.level_copy["player"].append((x + 1, y))

    def check_victory(self):
        self.victory = True
        for y in range(len(self.level_copy["map"])):
            for x in range(len(self.level_copy["map"][y])):
                if self.level_copy["map"][y][x] == "X" and (x, y) not in self.level_copy["crates"]:
                    self.victory = False

    def update_screen(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.update_game_screen()
        if self.victory:
            self.draw_victory_overlay()
        pygame.display.flip()

    def update_game_screen(self):
        self.draw_game_board()
        self.draw_player()
        self.draw_crates()
        self.print_level()

    def draw_game_board(self):
        rows = len(self.level_copy["map"])
        start_x = (WIDTH - self.get_longest_row() * TILE_SIZE) // 2
        start_y = (HEIGHT - rows * TILE_SIZE) // 2
        i, j = 0, 0

        for y in range(start_y, start_y + rows * TILE_SIZE, TILE_SIZE):
            colums = len(self.level_copy["map"][j])
            for x in range(start_x, start_x + colums * TILE_SIZE, TILE_SIZE):

                s = self.level_copy["map"][j][i]
                if s == "#":
                    self.screen.blit(self.floor_img, (x, y))
                    self.screen.blit(self.wall_img, (x, y))
                elif s == "-":
                    self.screen.blit(self.floor_img, (x, y))
                elif s == "X":
                    self.screen.blit(self.floor_img, (x, y))
                    self.screen.blit(self.x_img, (x, y))
                if (i, j) in self.level_copy["player"]:
                    if self.dir == "down":
                        self.screen.blit(self.down_img, (x, y))
                    elif self.dir == "up":
                        self.screen.blit(self.up_img, (x, y))
                    elif self.dir == "left":
                        self.screen.blit(self.left_img, (x, y))
                    elif self.dir == "right":
                        self.screen.blit(self.right_img, (x, y))
                if (i, j) in self.level_copy["crates"]:
                    self.screen.blit(self.crate_img, (x, y))
                i += 1
            i = 0
            j += 1

    def get_longest_row(self):
        return max(len(line) for line in self.level_copy["map"])

    def draw_player(self):
        pass

    def draw_crates(self):
        pass

    def print_level(self):
        pass

    def draw_victory_overlay(self):
        r = pygame.Rect(300, 300, 400, 80)
        txt_victory = "Натисни ENTER щоб продовжити!"
        pygame.draw.rect(self.screen, (26, 255, 26), r, width=0, border_radius=20)
        font = pygame.font.SysFont('couriernew', 20, bold=True)
        text = font.render(txt_victory, True, (255, 255, 255))
        self.screen.blit(text, (340, 340))

    def __del__(self):
        pygame.quit()
