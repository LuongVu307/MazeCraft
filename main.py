import os
from os.path import join
import sys
import pandas as pd
import random
import csv

import pygame
from pygame.image import load
from pygame.transform import scale, flip

from algorithm import Cell, RanDFS, RanPrims, Eller, RanKruskal, BFS, Greedy, DFS, cal_cost, BinaryTree


pygame.init()

GUI_WIDTH, GUI_HEIGHT = 800, 500
WIDTH, HEIGHT = 400, 300
path = join(os.getcwd(), "images")

screen = pygame.display.set_mode((GUI_WIDTH, GUI_HEIGHT))
pygame.display.set_caption("Maze Craft")
pygame.display.set_icon(load(join(path, "maze.png")))

clock = pygame.time.Clock()


DFS_img = load(join(path, "DFS.jpg"))
Ellers_img = load(join(path, "Ellers.jpg"))
Binary_img = load(join(path, "Binary.jpg"))
Kruskal_img = load(join(path, "Kruskal.jpg"))
Prims_img = load(join(path, "Prims.jpg"))
arrow_img = load(join(path, "arrow.png"))
arrow_rect = arrow_img.get_rect()
# print(arrow_rect)

tutorial0 = load(join(path, "tutorial0.jpg"))
tutorial1 = load(join(path, "tutorial1.jpg"))
tutorial2 = load(join(path, "tutorial2.jpg"))


columns = ["Generator", "Complexity", "Time Generate", "Steps Generate", "Solver", "Time Solve", "Steps Solve", "Path", "Distance"]
data = pd.DataFrame(columns = columns)

def draw_menu(page):

  screen.fill(pygame.Color("tan"))

  button = pygame.Rect(0, 0, 35, 25)

  if page == 1:
    button.center = (GUI_WIDTH - 30, GUI_HEIGHT // 2)
    arr_img = arrow_img
  elif page == 2:
    button.center = (30, GUI_HEIGHT // 2)
    arr_img = flip(arrow_img, True, False)
  # pygame.draw.rect(screen, pygame.Color("black"), button)
  screen.blit(scale(arr_img, (35, 35)), (button.topleft[0], button.topleft[1]-5))

  font = pygame.font.Font(None, 54)
  title_text = font.render("Maze Craft", True, pygame.Color("dark green"))
  screen.blit(title_text, (GUI_WIDTH // 2 - title_text.get_width() // 2, 50))

  font = pygame.font.Font(None, 36)
  title_text = font.render("Select A Maze Generation Algorithm", True, pygame.Color("Black"))
  screen.blit(title_text, (GUI_WIDTH // 2 - title_text.get_width() // 2, 200))

  option1 = ["DFS Maze", "Kruskal's Maze", "Prims Maze"]
  option2 = ["Eller Maze", "Binary Maze", "Saved Maze"]
  option_width = 150

  options = option1 if page == 1 else option2

  for option in options:
    option_text = font.render(option, True, pygame.Color("maroon"))
    text_rect = option_text.get_rect(center=(option_width, GUI_HEIGHT // 2))
    if option == "DFS Maze":
      screen.blit(scale(DFS_img, (150, 150)), (option_width-75, GUI_HEIGHT // 2 + 25))
    elif option == "Kruskal's Maze":
      screen.blit(scale(Kruskal_img, (150, 150)), (option_width-75, GUI_HEIGHT // 2 + 25))
    elif option == "Prims Maze":
      screen.blit(scale(Prims_img, (150, 150)), (option_width-75, GUI_HEIGHT // 2 + 25))
    elif option == "Eller Maze":
      screen.blit(scale(Ellers_img, (150, 150)), (option_width-75, GUI_HEIGHT // 2 + 25))
    elif option == "Binary Maze":
      screen.blit(scale(Binary_img, (150, 150)), (option_width-75, GUI_HEIGHT // 2 + 25))
    else:
      choice = pygame.Rect(0, 0, 150, 150)
      choice.center = (option_width, GUI_HEIGHT // 2 + 100)
      pygame.draw.rect(screen, pygame.Color("black"), choice)
    if option == "Saved Maze":
      draw_text(screen, "Choose a", pygame.font.Font(None, 32), pygame.Color("silver"), (320, 600))
      draw_text(screen, "Random", pygame.font.Font(None, 32), pygame.Color("silver"), (350, 605))
      draw_text(screen, "Maze", pygame.font.Font(None, 32), pygame.Color("silver"), (380, 620))
      
      

    screen.blit(option_text, text_rect)
    option_width += 250

def draw_text(screen, text, font, color, position):
  text_surface = font.render(text, True, color)
  text_rect = text_surface.get_rect()
  text_rect.left = position[1]
  text_rect.centery = position[0]
  screen.blit(text_surface, text_rect)

def handle_movement(keys, grid_cell, current_cell, rows, cols, key_pressed, steps):
  current_pos = grid_cell.index(current_cell)
  
  if not key_pressed:
    if keys[pygame.K_LEFT]:
        if (current_pos % cols) != 0 and not current_cell.walls['left']:
            current_cell = grid_cell[current_pos - 1]
            key_pressed = True
            steps+=1
    elif keys[pygame.K_RIGHT]:
        if (current_pos % cols) != cols - 1 and not current_cell.walls["right"]:
            current_cell = grid_cell[current_pos + 1]
            key_pressed = True
            steps+=1
    elif keys[pygame.K_UP]:
        if (current_pos // cols) != 0 and not current_cell.walls["top"]:
            current_cell = grid_cell[current_pos - cols]
            key_pressed = True
            steps+=1
    elif keys[pygame.K_DOWN]:
        if (current_pos // cols) != rows - 1 and not current_cell.walls["bottom"]:
            current_cell = grid_cell[current_pos + cols]
            key_pressed = True
            steps+=1
  else:
    if not any(keys[key] for key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]):
        key_pressed = False

  return current_cell, key_pressed, steps

def draw_intro(page):
  screen.fill(pygame.Color("lightgrey"))

  button = pygame.Rect(0, 0, 35, 25)

  if page == 1:
    button.center = (GUI_WIDTH - 30, GUI_HEIGHT // 2)
    arr_img = arrow_img
    screen.blit(scale(arr_img, (35, 35)), (button.topleft[0], button.topleft[1]-5))
    screen.blit(scale(tutorial0, (600, 375)), (100,  60))
  elif page == 2:
    button.center = (30, GUI_HEIGHT // 2)
    arr_img = flip(arrow_img, True, False)
    screen.blit(scale(arr_img, (35, 35)), (button.topleft[0], button.topleft[1]-5))
    arr_img_ = arrow_img
    button.center = (GUI_WIDTH - 30, GUI_HEIGHT // 2)
    screen.blit(scale(arr_img_, (35, 35)), (button.topleft[0], button.topleft[1]-5))
    screen.blit(scale(tutorial1, (600, 375)), (100,  60))
  elif page == 3:
    button.center = (30, GUI_HEIGHT // 2)
    arr_img = flip(arrow_img, True, False)
    screen.blit(scale(arr_img, (35, 35)), (button.topleft[0], button.topleft[1]-5))
    screen.blit(scale(tutorial2, (600, 375)), (100,  60))
  
def create_maze(autotrain=False, epochs=0, saving_maze=False, saving_data=False, range_random=(5, 40)):
  FPS = 60
  TILE = 20
  rows, cols = HEIGHT // TILE, WIDTH // TILE
  running = True
  state = "menu"
  page = 1
  maze_type = None
  size = "Medium"
  elapse = 0
  all_counter = epochs
  if autotrain:
    saving_data = True
  all_counter = 0
  while running:
    if autotrain:
      if all_counter >= epochs:
        data.to_csv("data.csv", mode="a", header=False, index=False)
        sys.exit()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        data.to_csv("data.csv", mode="a", header=False, index=False)
        sys.exit()
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          x, y = pygame.mouse.get_pos()
          # print(x, y)
          if 690 <= x <= 765 and 450 <= y <= 475:
            running = False
            if saving_data:
              data.to_csv("data.csv", mode="a", header=False, index=False)
            # print(data)
          match state:
            case "menu":
              if 340 <= x <= 460 and 100 <= y <= 125:
                if size == "Small":
                  size = "Moderate"
                elif size == "Moderate":
                  size = "Medium"
                elif size == "Medium":
                  size = "Large"
                elif size == "Large":
                  size = "Enormous"
                else:
                  size = "Small"
                # print(rows*cols)
              if 325 <= x <= 475 and 150 <= y <= 175:
                state = "Introduction"
                intro_page = 1
              if page == 1:
                if 753 <= x <= 787 and 238 <= y <= 263:
                  page = 2
                elif 75 <= x <= 225 and 275 <= y <= 425:
                  state = "prepare"
                  maze_type = "DFS"
                elif 325 <= x <= 475 and 275 <= y <= 425:
                  state = "prepare"
                  maze_type = "Kruskal"
                elif 575 <= x <= 725 and 275 <= y <= 425:
                  state = "prepare"
                  maze_type = "Prims"
              elif page == 2:
                if 11 <= x <= 48 and 238 <= y <= 263:
                  page = 1
                elif 75 <= x <= 225 and 275 <= y <= 425:
                  state = "prepare"
                  maze_type = "Eller"
                elif 325 <= x <= 475 and 275 <= y <= 425:
                  state = "prepare"
                  maze_type = "Binary"
                elif 575 <= x <= 725 and 275 <= y <= 425:
                  state = "prepare"
                  maze_type = "Saved"
                  with open("mazes.csv", "r") as file:
                    files = random.choice(list(csv.reader(file)))
                  for i in range(len(files)):
                    if files[i] in ["True", "False"]:
                      files[i] = True if files[i] == "True" else False
                    else:
                      try:
                        files[i] = int(files[i])
                      except Exception:
                        files[i] = files[i]
            case "end maze":
              if 500 <= x <= 750 and 75 <= y <= 125:
                solver = "BFS"
                state = "solve maze"
                current_cell = grid_cell[start]
                steps = 0
                start_time = pygame.time.get_ticks()
                queue = [current_cell]
                visited = []
                for i in range(len(grid_cell)):
                  grid_cell[i].visited = False
              elif 500 <= x <= 750 and 150 <= y <= 200:
                solver = "Greedy"
                state = "solve maze"
                current_cell = grid_cell[start]
                steps = 0
                start_time = pygame.time.get_ticks()
                priority_queue, visited = [(0, current_cell)], []
                for i in range(len(grid_cell)):
                  grid_cell[i].visited = False
              elif 500 <= x <= 750 and 225 <= y <= 275:
                solver = "DFS"
                state = "solve maze"
                current_cell = grid_cell[start]
                steps = 0
                start_time = pygame.time.get_ticks()
                for i in range(len(grid_cell)):
                  grid_cell[i].visited = False
                stack, visited = [], [current_cell]
              elif 500 <= x <= 750 and 300 <= y <= 350:
                state = "3rd-V"
                key_pressed = False
                current_cell = grid_cell[start]
                steps = 0
                start_time = pygame.time.get_ticks()
                path = 1
                ls = [current_cell]
              elif 500 <= x <= 750 and 375 <= y <= 425:
                state = "1st-V"
                key_pressed = False
                current_cell = grid_cell[start]
                steps = 0
                start_time = pygame.time.get_ticks()
                path = 1
                ls = [current_cell]
            case "Introduction":
              if intro_page == 1:
                if 753 <= x <= 787 and 238 <= y <= 263:
                  intro_page = 2
              elif intro_page == 2:
                if 753 <= x <= 787 and 238 <= y <= 263:
                  intro_page = 3
                elif 11 <= x <= 48 and 238 <= y <= 263:
                  intro_page = 1
              elif intro_page == 3:
                if 11 <= x <= 48 and 238 <= y <= 263:
                  intro_page = 2
                
          if state not in ["menu", "prepare", "Introduction", "3rd-V"]:
            if 350 <= x <= 470 and 450 <= y <= 475:
              if pause == "Continue":
                pause = "Pause"
                start_time += elapse
              else:
                pause = "Continue"
            elif 570 <= x <= 670 and 450 <= y <= 475:
              if speed == "Slow":
                speed = "Normal"
              elif speed == "Normal":
                speed = "Fast"
              else:
                speed = "Slow"
          if state in ["solve maze", "done solve", "3rd-V", "1st-V"]:
            if 200 <= x <= 300 and 450 <= y <= 475:
              state = "end maze"
          if state not in ["menu", "prepare"] and 50 <= x <= 150 and 450 <= y <= 475:
              state = "menu"
     
              
    screen.fill(pygame.Color(50, 50, 50))
    match state:
      case "menu":
        draw_menu(page)
        if autotrain:
          #AUTO TRAIN---------------------------------------------------------------
          maze_type = random.choice(["DFS", "Kruskal", "Prims", "Eller", "Binary"])
          speed = "Training"
          FPS = 100
          countering = 1
          size = "Random"
          state = "prepare"
          #---------------------------------------------------------------------
      case "prepare":
        if size == "Moderate":
          TILE = random.randint(23, 27)
        elif size == "Medium":
          TILE = random.randint(15, 19)
        elif size == "Large":
          TILE = random.randint(11, 13)
        elif size == "Enormous":
          TILE = random.randint(8, 10)
        elif size == "Small":
          TILE = random.randint(32, 38)
        elif size == "Random":
          TILE = random.randint(range_random[0], range_random[1])
          print(TILE)
        rows, cols = HEIGHT // TILE, WIDTH // TILE
        grid_cell = [
            Cell(col, row, TILE, screen, cols, rows) for row in range(rows)
            for col in range(cols)
        ]
        state = "maze"
        start_time = pygame.time.get_ticks()
        steps = 0
        pause = "Pause"
          

        if not autotrain:
          speed = "Normal"
        match maze_type:
          case "DFS":
            current_cell = grid_cell[0]
            stack = []
          case "Kruskal":
            current_cell = grid_cell[0]
            set_cell = [set([i]) for i in range(len(grid_cell))]
          case "Prims":
            current_cell = random.choice(grid_cell)
            current_cell.visited = True
    
          case "Eller":
            current_cell = grid_cell[0]
            for i in range(len(grid_cell)):
              if i%cols != 0:
                grid_cell[i].walls["left"] = False
              if i%cols != cols-1:
                grid_cell[i].walls["right"] = False
              if i//cols != 0:
                grid_cell[i].walls["top"] = False
              if i//cols != rows-1:
                grid_cell[i].walls["bottom"] = False
            set_cell = []
          case "Binary":
            for i in range(len(grid_cell)):
              if i%cols != 0:
                grid_cell[i].walls["left"] = False
              if i%cols != cols-1:
                grid_cell[i].walls["right"] = False
              if i//cols != 0:
                grid_cell[i].walls["top"] = False
              if i//cols != rows-1:
                grid_cell[i].walls["bottom"] = False
            current_cell = grid_cell[0]
          case "Saved":
            rows, cols = files[1], files[2]
            maze_type = files[0]
            TILE, generate_time, generate_steps = files[3], files[4], files[5]
            end = random.randint(0, len(grid_cell)-1)
            start = random.randint(0, len(grid_cell)-1)
            grid_cell = [
            Cell(col, row, TILE, screen, cols, rows) for row in range(rows)
            for col in range(cols)
            ]
            grid_cell[start].start = True
            grid_cell[end].end = True
            # print(files)
            # print([files[i] for i in range(len(files))])
            for i, j in zip(range(len(grid_cell)), range(6, len(files), 4)):
              grid_cell[i].walls["right"] = files[j]
              grid_cell[i].walls["left"] = files[j+1]
              grid_cell[i].walls["top"] = files[j+2]
              grid_cell[i].walls["bottom"] = files[j+3]

              state = "end maze"
      case "maze":
        [cells.draw() for cells in grid_cell]
        if pause == "Pause":
          steps += 1
          now = pygame.time.get_ticks()
          match maze_type:
            case "DFS":
              current_cell, stack = RanDFS(current_cell, stack, grid_cell)
              if not stack:
                state = "end maze"
                end = random.randint(0, len(grid_cell)-1)
                start = random.randint(0, len(grid_cell)-1)
                generate_time, generate_steps = pygame.time.get_ticks() - start_time, steps
                if saving_maze:
                  maze = [[maze_type, rows, cols, TILE, generate_time, generate_steps]]
                  for i in grid_cell:
                    for j in (i.walls["right"], i.walls["left"], i.walls["top"], i.walls["bottom"]):
                      maze[0].append(j)
                  with open('mazes.csv', 'a', newline='') as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerows(maze)
                grid_cell[end].end = True
                grid_cell[start].start = True
                for cell in range(len(grid_cell)):
                  grid_cell[cell].generated=True
            case "Kruskal":
              set_cell = RanKruskal(grid_cell, list(set_cell))
              if not set_cell:
                state = "end maze"
                end = random.randint(0, len(grid_cell)-1)
                start = random.randint(0, len(grid_cell)-1)
                generate_time, generate_steps = pygame.time.get_ticks() - start_time, steps
                if saving_maze:
                  maze = [[maze_type, rows, cols, TILE, generate_time, generate_steps]]
                  for i in grid_cell:
                    for j in (i.walls["right"], i.walls["left"], i.walls["top"], i.walls["bottom"]):
                      maze[0].append(j)
                  with open('mazes.csv', 'a', newline='') as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerows(maze)
                grid_cell[end].end = True
                grid_cell[start].start = True
                for cell in range(len(grid_cell)):
                  grid_cell[cell].generated=True
            case "Prims":
              new_grid = grid_cell.copy()
              grid_cell = RanPrims(list(grid_cell))
              if not grid_cell:
                grid_cell = new_grid
                state = "end maze"
                generate_time, generate_steps = pygame.time.get_ticks() - start_time, steps
                end = random.randint(0, len(grid_cell)-1)
                start = random.randint(0, len(grid_cell)-1)
                [cell.draw() for cell in grid_cell]
                if saving_maze:
                  maze = [[maze_type, rows, cols, TILE, generate_time, generate_steps]]
                  for i in grid_cell:
                    for j in (i.walls["right"], i.walls["left"], i.walls["top"], i.walls["bottom"]):
                      maze[0].append(j)
                  with open('mazes.csv', 'a', newline='') as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerows(maze)

                grid_cell[end].end = True
                grid_cell[start].start = True
                for cell in range(len(grid_cell)):
                  grid_cell[cell].generated=True
            case "Eller":
              current_cell, set_cell = Eller(grid_cell, rows, cols, set_cell, current_cell)
              if grid_cell.index(current_cell) == len(grid_cell)-1:
                state = "end maze"
                end = random.randint(0, len(grid_cell)-1)
                start = random.randint(0, len(grid_cell)-1)
                generate_time, generate_steps = pygame.time.get_ticks() - start_time, steps
                if saving_maze:
                  maze = [[maze_type, rows, cols, TILE, generate_time, generate_steps]]
                  for i in grid_cell:
                    for j in (i.walls["right"], i.walls["left"], i.walls["top"], i.walls["bottom"]):
                      maze[0].append(j)
                  with open('mazes.csv', 'a', newline='') as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerows(maze)
                grid_cell[end].end = True
                grid_cell[start].start = True
                for cell in range(len(grid_cell)):
                  grid_cell[cell].generated=True
            case "Binary":
              current_cell = BinaryTree(current_cell, grid_cell, cols)
              if grid_cell.index(current_cell) == len(grid_cell)-1:
                state = "end maze"
                end = random.randint(0, len(grid_cell)-1)
                start = random.randint(0, len(grid_cell)-1)
                generate_time, generate_steps = pygame.time.get_ticks() - start_time, steps
                if saving_maze:
                  maze = [[maze_type, rows, cols, TILE, generate_time, generate_steps]]
                  for i in grid_cell:
                    for j in (i.walls["right"], i.walls["left"], i.walls["top"], i.walls["bottom"]):
                      maze[0].append(j)
                  with open('mazes.csv', 'a', newline='') as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerows(maze)
                grid_cell[end].end = True
                grid_cell[start].start = True
                for cell in range(len(grid_cell)):
                  grid_cell[cell].generated=True
        draw_text(screen,
                    f"TIME: {(now - start_time) / 1000}",
                    pygame.font.Font(None, 24), pygame.Color("Red"), (40, 30))
        draw_text(screen, f"STEPS: {steps}", pygame.font.Font(None, 24),
                    pygame.Color("Red"), (70, 30))
      case "end maze":
        for i in range(len(grid_cell)):
                  grid_cell[i].gone_through=False
        draw_text(screen,
                    f"TIME: {(generate_time) / 1000}",
                    pygame.font.Font(None, 24), pygame.Color("Red"), (40, 30))
        draw_text(screen, f"STEPS: {generate_steps}", pygame.font.Font(None, 24),
                  pygame.Color("Red"), (70, 30))
        [cells.draw() for cells in grid_cell]
        for i in grid_cell:
          i.path = None
          i.visited = False
          i.fake_visited = False
        font = pygame.font.Font(None, 36)

        texts = ["Breadth-First Search", "Greedy Algorithm", "Depth-First Search", "3rd View Solve", "1st View Solve"]
        for button_text in texts:
          text_surface = font.render(button_text, True, pygame.Color("White"))
          button_rect = pygame.Rect(WIDTH+100, (texts.index(button_text)+1)*(HEIGHT//4), 250, 50)
          text_rect = text_surface.get_rect(center=button_rect.center)
          pygame.draw.rect(screen, (101, 67, 33), button_rect)
          screen.blit(text_surface, text_rect)
        
        if autotrain:
          #AUTO TRAIN -----------------------
          state = "solve maze"
          # print(countering)
          # countering = random.randint(1, 3)
          # print(start, end)
          if countering == 1:
            solver = "BFS"
            current_cell = grid_cell[start]
            steps = 0
            start_time = pygame.time.get_ticks()
            queue = [current_cell]
            visited = []
            for i in range(len(grid_cell)):
              grid_cell[i].visited = False

          elif countering == 2:
            solver = "Greedy"
            current_cell = grid_cell[start]
            steps = 0
            start_time = pygame.time.get_ticks()
            priority_queue, visited = [(0, current_cell)], []
            for i in range(len(grid_cell)):
              grid_cell[i].visited = False
          elif countering == 3:
            solver = "DFS"
            current_cell = grid_cell[start]
            steps = 0
            start_time = pygame.time.get_ticks()
            for i in range(len(grid_cell)):
              grid_cell[i].visited = False
            stack, visited = [], [current_cell]
          else:
            state = "menu"
            all_counter += 1
        # ---------------------------------------
      case "solve maze":
        draw_text(screen,
                    f"TIME: {(generate_time) / 1000}",
                    pygame.font.Font(None, 24), pygame.Color("Red"), (40, 30))
        draw_text(screen, f"STEPS: {generate_steps}", pygame.font.Font(None, 24),
                  pygame.Color("Red"), (70, 30))
        [cells.draw() for cells in grid_cell]
        # [cells.draw_path() for cells in grid_cell]
        if pause == "Pause":
          steps += 1 
          match solver:
            case "BFS":
              if grid_cell.index(current_cell) != end:
                current_cell, queue, visited = BFS(grid_cell, current_cell, queue, visited)
                current_cell.gone_through = True
              else:
                state = "backtrack"
                path = 0
                solve_time = pygame.time.get_ticks() - start_time
                solve_steps = steps 
                # for i in range(len(grid_cell)):
                #   grid_cell[i].gone_through=False

            case "Greedy":
              if grid_cell.index(current_cell) != end:
                current_cell, priority_queue, visited = Greedy(grid_cell, current_cell, priority_queue, visited, (end//cols, end%cols), cols)
                current_cell.gone_through = True
              else:
                state = "backtrack"
                path = 0
                solve_time = pygame.time.get_ticks() - start_time
                solve_steps = steps
                # for i in range(len(grid_cell)):
                #   grid_cell[i].gone_through=False

            case "DFS":
              if grid_cell.index(current_cell) != end:
                current_cell, stack, visited = DFS(grid_cell, current_cell, stack, visited)
                current_cell.gone_through = True
              else:
                state = "backtrack"
                path = 0
                solve_time = pygame.time.get_ticks() - start_time
                solve_steps = steps
                # for i in range(len(grid_cell)):
                #   grid_cell[i].gone_through=False
        
          now = pygame.time.get_ticks()
        current_cell.draw_current()
        draw_text(screen,
                    f"TIME: {(now - start_time) / 1000}",
                    pygame.font.Font(None, 24), pygame.Color("green"), (40, 150))
        draw_text(screen, f"STEPS: {steps}", pygame.font.Font(None, 24),
                  pygame.Color("green"), (70, 150))
      case "done solve":
        draw_text(screen,
                    f"TIME: {(generate_time) / 1000}",
                    pygame.font.Font(None, 24), pygame.Color("Red"), (40, 30))
        draw_text(screen, f"STEPS: {generate_steps}", pygame.font.Font(None, 24),
                  pygame.Color("Red"), (70, 30))
        draw_text(screen,
                    f"TIME: {(solve_time) / 1000}",
                    pygame.font.Font(None, 24), pygame.Color("green"), (40, 150))
        draw_text(screen, f"STEPS: {solve_steps}", pygame.font.Font(None, 24),
                  pygame.Color("green"), (70, 150))
        [cells.draw() for cells in grid_cell]
        #AUTO TRAIN ---------
        if autotrain:
          countering += 1
          state = "end maze"
        #------------------
      case "Introduction":
        screen.fill(pygame.Color("tan"))

        font = pygame.font.Font(None, 54)
        title_text = font.render("Maze Craft", True, pygame.Color("dark green"))
        screen.blit(title_text, (GUI_WIDTH // 2 - title_text.get_width() // 2, 50))

        draw_intro(intro_page)
      case "3rd-V":
        solver = "3rd-V"
        keys = pygame.key.get_pressed()
        next_cell, key_pressed, steps = handle_movement(keys, grid_cell, current_cell, rows, cols, key_pressed, steps)
        draw_text(screen,
                    f"TIME: {(generate_time) / 1000}",
                    pygame.font.Font(None, 24), pygame.Color("Red"), (40, 30))
        draw_text(screen, f"STEPS: {generate_steps}", pygame.font.Font(None, 24),
                  pygame.Color("Red"), (70, 30))
        now = pygame.time.get_ticks()
        draw_text(screen,
                    f"TIME: {(now - start_time) / 1000}",
                    pygame.font.Font(None, 24), pygame.Color("green"), (40, 150))
        draw_text(screen, f"STEPS: {steps}", pygame.font.Font(None, 24),
                  pygame.Color("green"), (70, 150))
        if current_cell != next_cell:
          if next_cell in ls:
            ls.remove(next_cell)
            next_cell.path = False
            path -= 1
          else:
            ls.append(current_cell)
            current_cell.path = True
            path += 1
        
        current_cell = next_cell
        [cells.draw() for cells in grid_cell]
        current_cell.draw_current()
        if grid_cell.index(current_cell) == end:
          solve_time = pygame.time.get_ticks() - start_time
          solve_steps = steps
          state = "done solve"
      case "1st-V":
        solver = "1st-V"
        keys = pygame.key.get_pressed()
        next_cell, key_pressed, steps = handle_movement(keys, grid_cell, current_cell, rows, cols, key_pressed, steps)
        draw_text(screen,
                    f"TIME: {(generate_time) / 1000}",
                    pygame.font.Font(None, 24), pygame.Color("Red"), (40, 30))
        draw_text(screen, f"STEPS: {generate_steps}", pygame.font.Font(None, 24),
                  pygame.Color("Red"), (70, 30))
        current_cell.draw_1st()
        now = pygame.time.get_ticks()
        draw_text(screen,
                    f"TIME: {(now - start_time) / 1000}",
                    pygame.font.Font(None, 24), pygame.Color("green"), (40, 150))
        draw_text(screen, f"STEPS: {steps}", pygame.font.Font(None, 24),
                  pygame.Color("green"), (70, 150))

        draw_text(screen, f"Distance to the exit: {cal_cost(grid_cell, current_cell, (end//cols, end%cols), cols)}", pygame.font.Font(None, 24),
                  pygame.Color("White"), (180, 400))
        # [cells.draw() for cells in grid_cell]
        if current_cell != next_cell:
          if next_cell in ls:
            ls.remove(next_cell)
            next_cell.path = False
            path -= 1
          else:
            ls.append(current_cell)
            current_cell.path = True
            path += 1
          current_cell = next_cell
        if grid_cell.index(current_cell) == len(grid_cell)-1:
          solve_time = pygame.time.get_ticks() - start_time
          solve_steps = steps
          if saving_data:
            new_data = {"Generator" : maze_type, "Complexity" : size, "Time Generate" : generate_time/1000, "Steps Generate" : generate_steps, "Solver" : solver, "Time Solve" : solve_time/1000, "Steps Solve" : solve_steps, "path" : path}
            data.loc[len(data)] = new_data
            state = "done solve"
      case "backtrack":
        if grid_cell.index(current_cell) != start:
          choices = []
          # print(start, end, grid_cell.index(current_cell))
          # raise Exception
          for i in current_cell.check_next_neighbor(grid_cell):
            if i in visited:
              choices.append((visited.index(i), i))
          current_cell = sorted(choices, key=lambda x:x[0])[0][1]
          current_cell.path = True
          path += 1
          [cells.draw() for cells in grid_cell]
        else:
          state = "done solve"
          if saving_data:
            new_data = {"Generator" : maze_type, "Complexity" : cols*rows, "Time Generate" : generate_time/1000, "Steps Generate" : generate_steps, "Solver" : solver, "Time Solve" : solve_time/1000, "Steps Solve" : solve_steps, "Path" : path, "Distance" : cal_cost(grid_cell, grid_cell[start], (end//cols, end%cols), cols)}
            data.loc[len(data)] = new_data

    if state not in ["menu", "prepare"]:
      button_text = "Back"
      font = pygame.font.Font(None, 36)
      text_surface = font.render(button_text, True, pygame.Color("White"))
      button_rect = pygame.Rect(50, GUI_HEIGHT-50, 100, 25)
      text_rect = text_surface.get_rect(center=button_rect.center)
      pygame.draw.rect(screen, (0, 128, 255), button_rect)
      screen.blit(text_surface, text_rect)
      
    if state in ["solve maze", "done solve", "3rd-V", "1st-V"]:
      button_text = "Reset"
      font = pygame.font.Font(None, 36)
      text_surface = font.render(button_text, True, pygame.Color("White"))
      button_rect = pygame.Rect(200, GUI_HEIGHT-50, 100, 25)
      text_rect = text_surface.get_rect(center=button_rect.center)
      pygame.draw.rect(screen, (0, 128, 255), button_rect)
      screen.blit(text_surface, text_rect)
      
    if state not in ["menu", "prepare", "Introduction", "3rd-V"]:
      button_text = pause
      if pause == "Continue":
        elapse = pygame.time.get_ticks()-now
        # print(elapse)
      font = pygame.font.Font(None, 36)
      text_surface = font.render(button_text, True, pygame.Color("White"))
      button_rect = pygame.Rect(350, GUI_HEIGHT-50, 120, 25)
      text_rect = text_surface.get_rect(center=button_rect.center)
      pygame.draw.rect(screen, (0, 128, 255), button_rect)
      screen.blit(text_surface, text_rect)
    
    if state not in ["menu", "prepare", "Introduction", "3rd-V"]:
      button_text = speed
      font = pygame.font.Font(None, 36)
      text_surface = font.render(button_text, True, pygame.Color("White"))
      button_rect = pygame.Rect(570, GUI_HEIGHT-50, 100, 25)
      text_rect = text_surface.get_rect(center=button_rect.center)
      pygame.draw.rect(screen, (0, 128, 255), button_rect)
      screen.blit(text_surface, text_rect)

      if state in ["maze", "solve maze"]:
        if speed == "Slow":
          FPS = 3
        elif speed == "Normal":
          FPS = 10
        elif speed == "Fast":
          FPS = 60
    
    if state == "menu":
      button_text = size
      font = pygame.font.Font(None, 36)
      text_surface = font.render(button_text, True, pygame.Color("White"))
      button_rect = pygame.Rect(GUI_WIDTH//2-60, 100, 120, 25)
      text_rect = text_surface.get_rect(center=button_rect.center)
      pygame.draw.rect(screen, (0, 128, 255), button_rect)
      screen.blit(text_surface, text_rect)
        
      button_text = "How to play"
      font = pygame.font.Font(None, 36)
      text_surface = font.render(button_text, True, pygame.Color("White"))
      button_rect = pygame.Rect(GUI_WIDTH//2-75, 150, 150, 25)
      text_rect = text_surface.get_rect(center=button_rect.center)
      pygame.draw.rect(screen, (0, 128, 255), button_rect)
      screen.blit(text_surface, text_rect)

    button_text = "Quit"
    font = pygame.font.Font(None, 36)
    text_surface = font.render(button_text, True, pygame.Color("Red"))
    button_rect = pygame.Rect(GUI_WIDTH-110, GUI_HEIGHT-50, 75, 25)
    text_rect = text_surface.get_rect(center=button_rect.center)
    pygame.draw.rect(screen, (0, 0, 0), button_rect)
    screen.blit(text_surface, text_rect)

    pygame.display.flip()

    clock.tick(FPS)


def main():
  # create_maze(autotrain=True, epochs=200, range_random=(6, 15), saving_maze=True)
  create_maze()

if __name__ == "__main__":
  main()
