from grid import Grid
from Blocks import *
import random
import pygame

class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [IBlock(), JBlock(), OBlock(), SBlock(), TBlock(), ZBlock()] 
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
        self.metal = pygame.mixer.Sound("Sounds/metal_2_1.mp3")

        pygame.mixer.music.load("Sounds/fullwolf.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

    def update_score(self, lines_cleard, move_down_points):
        if lines_cleard == 1:
            self.score += 100
        elif lines_cleard == 2:
            self.score += 300
        elif lines_cleard == 3:
            self.score += 500
        elif lines_cleard == 4:
            self.score += 600
        elif lines_cleard == 5:
            self.score += 800
        self.score += move_down_points
        
    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [LBlock(), IBlock(), JBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]    
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block
    
    def move_left(self):
        self.current_block.move(0, -1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, 1)    

    def move_right(self):
        self.current_block.move(0, 1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, -1)

    def move_down(self):
        self.current_block.move(1, 0)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(-1, 0)
            self.lock_block()
    
    def hard_drop(self):
    # 計算方塊需要降落的行數
        rows_to_fall = 0
        if self.block_inside() == False or self.block_fits() == False:
            rows_to_fall += 1

    # 一次性將方塊移動到最底部
        self.current_block.move(rows_to_fall, 0)

    # 鎖定方塊
        self.lock_block()
    
    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleard = self.grid.clear_full_rows()
        if rows_cleard > 0:
            self.metal.play()
            self.update_score(rows_cleard, 0)
        if self.block_fits() == False:
            self.game_over = True

    def reset(self):
        self.grid.reset()
        self.blocks = [IBlock(), JBlock(), OBlock(), SBlock(), TBlock(), ZBlock()] 
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0

    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_empty(tile.row, tile.column) == False:
                return False
        return True

    def rotate(self):
        self.current_block.rotate()
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.undo_rotation()

    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.column) == False:
                return False
        return True
    
    def draw(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen, 11, 11)

        if self.next_block.id == 3:
            self.next_block.draw(screen, 255, 290)
        elif self.next_block.id == 4:
            self.next_block.draw(screen, 255, 280)
        else:
            self.next_block.draw(screen, 270, 270)