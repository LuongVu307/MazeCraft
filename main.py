import pygame
import sys
from algorithm import Cell, RanDFS, RanPrims, Eller, HuntKill, RanKruskal, RandomMouse, HandOnWall, Tremaux
import os
from os.path import join
from pygame.image import load
from pygame.transform import scale

pygame.init()

GUI_WIDTH, GUI_HEIGHT = 800, 500
WIDTH, HEIGHT = 400, 300

screen = pygame.display.set_mode((GUI_WIDTH, GUI_HEIGHT))
pygame.display.set_caption("Maze Craft")

clock = pygame.time.Clock()

path = join(os.getcwd(), "images")
DFS_img = load(join(path, "DFS.jpg"))
Ellers_img = load(join(path, "Ellers.jpg"))
HuntKill_img = load(join(path, "Huntkill.jpg"))
Kruskal_img = load(join(path, "Kruskal.jpg"))
Prims_img = load(join(path, "Prims.jpg"))


def draw_menu(page):

  screen.fill(pygame.Color("tan"))

  button = pygame.Rect(0, 0, 20, 20)
  if page == 1:
    button.center = (GUI_WIDTH - 30, GUI_HEIGHT // 2)
  elif page == 2:
    button.center = (30, GUI_HEIGHT // 2)
  pygame.draw.rect(screen, pygame.Color("black"), button)

  font = pygame.font.Font(None, 54)
  title_text = font.render("Maze Craft", True, pygame.Color("dark green"))
  screen.blit(title_text, (GUI_WIDTH // 2 - title_text.get_width() // 2, 50))

  font = pygame.font.Font(None, 36)
  title_text = font.render("Select A Maze Generation Algorithm", True, pygame.Color("Black"))
  screen.blit(title_text, (GUI_WIDTH // 2 - title_text.get_width() // 2, 200))

  option1 = ["DFS Maze", "Kruskal's Maze", "Prims Maze"]
  option2 = ["Eller Maze", "HuntKill Maze"]
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
    elif option == "HuntKill Maze":
      screen.blit(scale(HuntKill_img, (150, 150)), (option_width-75, GUI_HEIGHT // 2 + 25))
    else:
      choice = pygame.Rect(0, 0, 150, 150)
      choice.center = (option_width, GUI_HEIGHT // 2 + 100)
      pygame.draw.rect(screen, pygame.Color("black"), choice)
    screen.blit(option_text, text_rect)
    option_width += 250


def draw_text(screen, text, font, color, position):
  text_surface = font.render(text, True, color)
  text_rect = text_surface.get_rect()
  text_rect.left = position[1]
  text_rect.centery = position[0]
  screen.blit(text_surface, text_rect)

def main():
  FPS = 60
  TILE = 20
  rows, cols = HEIGHT // TILE, WIDTH // TILE
  running = True
  state = "menu"
  page = 1
  maze_type = None
  size = "Medium"
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        sys.exit()
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          x, y = pygame.mouse.get_pos()
          match state:
            case "menu":
              if 340 <= x <= 460 and 100 <= y <= 125:
                if size == "Small":
                  size = "Medium"
                  TILE = 25
                  rows, cols = HEIGHT // TILE, WIDTH // TILE
                elif size == "Medium":
                  size = "Large"
                  TILE = 15
                  rows, cols = HEIGHT // TILE, WIDTH // TILE
                else:
                  size = "Small"
                  TILE = 35
                  rows, cols = HEIGHT // TILE, WIDTH // TILE
              if 325 <= x <= 475 and 150 <= y <= 175:
                state = "Introduction"
              if page == 1:
                if 760 <= x <= 780 and 240 <= y <= 260:
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
                if 20 <= x <= 40 and 240 <= y <= 260:
                  page = 1
                elif 75 <= x <= 225 and 275 <= y <= 425:
                  state = "prepare"
                  maze_type = "Eller"
                elif 325 <= x <= 475 and 275 <= y <= 425:
                  state = "prepare"
                  maze_type = "HuntKill"
            case "end maze":
              if 500 <= x <= 700 and 100 <= y <= 150:
                solver = "RandomMouse"
                state = "solve maze"
                previous_cell = None
                end = len(grid_cell)-1
                current_cell = grid_cell[0]
                steps = 0
                start_time = pygame.time.get_ticks()
                for i in range(len(grid_cell)):
                  grid_cell[i].visited = False
              elif 500 <= x <= 700 and 200 <= y <= 250:
                solver = "HandOnWall"
                state = "solve maze"
                previous_cell = None
                end = len(grid_cell)-1
                current_cell = grid_cell[0]
                steps = 0
                start_time = pygame.time.get_ticks()
                for i in range(len(grid_cell)):
                  grid_cell[i].visited = False
              elif 500 <= x <= 700 and 300 <= y <= 350:
                solver = "Tremaux"
                state = "solve maze"
                previous_cell = None
                end = len(grid_cell)-1
                current_cell = grid_cell[0]
                steps = 0
                start_time = pygame.time.get_ticks()
                for i in range(len(grid_cell)):
                  grid_cell[i].visited = False
                stack, visited = [], []
          if state not in ["menu", "prepare", "Introduction"]:
            if 350 <= x <= 470 and 450 <= y <= 475:
              if pause == "Continue":
                pause = "Pause"
              else:
                pause = "Continue"
            elif 570 <= x <= 670 and 450 <= y <= 475:
              if speed == "Slow":
                speed = "Normal"
              elif speed == "Normal":
                speed = "Fast"
              else:
                speed = "Slow"
          if state in ["solve maze", "done solve"]:
            if 200 <= x <= 300 and 450 <= y <= 475:
              state = "end maze"
          if state not in ["menu", "prepare"] and 50 <= x <= 150 and 450 <= y <= 475:
              state = "menu"

              
    screen.fill(pygame.Color(50, 50, 50))
    match state:
      case "menu":
        draw_menu(page)
      case "prepare":
        grid_cell = [
            Cell(col, row, TILE, screen, cols, rows) for row in range(rows)
            for col in range(cols)
        ]
        match maze_type:
          case "DFS":
            current_cell = grid_cell[0]
            stack = []
          case "Kruskal":
            current_cell = grid_cell[0]
            set_cell = [set([i]) for i in range(len(grid_cell))]
          case "Prims":
            current_cell = grid_cell[rows * cols // 2 ]
            current_cell.visited = True
    
          case "Eller":
            current_cell = grid_cell[0]
            count = 0
            set_cell = []
          case "HuntKill":
            current_cell = grid_cell[0]
        state = "maze"
        start_time = pygame.time.get_ticks()
        steps = 0
        pause = "Pause"
        speed = "Normal"
      case "maze":
        [cells.draw() for cells in grid_cell]
        if pause == "Pause":
          steps += 1
          draw_text(screen,
                    f"TIME: {(pygame.time.get_ticks() - start_time) / 1000}",
                    pygame.font.Font(None, 24), pygame.Color("Red"), (40, 30))
          draw_text(screen, f"STEPS: {steps}", pygame.font.Font(None, 24),
                    pygame.Color("Red"), (70, 30))
          match maze_type:
            case "DFS":
              current_cell, stack = RanDFS(current_cell, stack, grid_cell)
              if not stack:
                state = "end maze"
                generate_time, generate_steps = pygame.time.get_ticks() - start_time, steps
            case "Kruskal":
              set_cell = RanKruskal(grid_cell, list(set_cell))
              if not set_cell:
                state = "end maze"
                generate_time, generate_steps = pygame.time.get_ticks() - start_time, steps
            case "Prims":
              new_grid = grid_cell.copy()
              grid_cell = RanPrims(list(grid_cell))
              if not grid_cell:
                grid_cell = new_grid
                state = "end maze"
                generate_time, generate_steps = pygame.time.get_ticks() - start_time, steps
            case "Eller":
              set_cell = Eller(grid_cell, rows, cols, count, set_cell)
              count += 1
              if not set_cell:
                state = "end maze"
                generate_time, generate_steps = pygame.time.get_ticks() - start_time, steps
            case "HuntKill":
              current_cell = HuntKill(current_cell, grid_cell)
              if not current_cell:
                state = "end maze"
                generate_time, generate_steps = pygame.time.get_ticks() - start_time, steps
      case "end maze":
        draw_text(screen,
                    f"TIME: {(generate_time) / 1000}",
                    pygame.font.Font(None, 24), pygame.Color("Red"), (40, 30))
        draw_text(screen, f"STEPS: {generate_steps}", pygame.font.Font(None, 24),
                  pygame.Color("Red"), (70, 30))
        minus_count = 0
        [cells.draw() for cells in grid_cell]
        for i in grid_cell:
          i.path = None
          i.visited = False
          i.fake_visited = False
        font = pygame.font.Font(None, 36)
        texts = ["Random Mouse", "Left Hand Rules", "Tremaux"]
        for button_text in texts:
          text_surface = font.render(button_text, True, pygame.Color("White"))
          button_rect = pygame.Rect(WIDTH+100, (texts.index(button_text)+1)*(HEIGHT//3), 200, 50)
          text_rect = text_surface.get_rect(center=button_rect.center)
          pygame.draw.rect(screen, (0, 128, 255), button_rect)
          screen.blit(text_surface, text_rect)
      case "solve maze":
        draw_text(screen,
                    f"TIME: {(generate_time) / 1000}",
                    pygame.font.Font(None, 24), pygame.Color("Red"), (40, 30))
        draw_text(screen, f"STEPS: {generate_steps}", pygame.font.Font(None, 24),
                  pygame.Color("Red"), (70, 30))
        draw_text(screen,
                    f"TIME: {(pygame.time.get_ticks() - start_time) / 1000}",
                    pygame.font.Font(None, 24), pygame.Color("green"), (40, 150))
        draw_text(screen, f"STEPS: {steps}", pygame.font.Font(None, 24),
                  pygame.Color("green"), (70, 150))
        [cells.draw() for cells in grid_cell]
        # [cells.draw_path() for cells in grid_cell]
        if pause == "Pause":
          steps += 1 
          match solver:
            case "RandomMouse":
              if grid_cell.index(current_cell) != end:
                previous_cell, current_cell = RandomMouse(grid_cell, current_cell, previous_cell)
                # if current_cell.path:
                #   minus_count += 1
                #   current_cell.path = None
                # else:
                #   current_cell.path = steps - minus_count
                current_cell.draw_current()
              else:
                state = "done solve"
                solve_time = pygame.time.get_ticks() - start_time
                solve_steps = steps 

            case "HandOnWall":
              if grid_cell.index(current_cell) != end:
                previous_cell, current_cell = HandOnWall(grid_cell, current_cell, previous_cell)
                # if current_cell.path:
                #   minus_count += 1
                #   current_cell.path = None
                # else:
                #   current_cell.path = steps - minus_count
                current_cell.draw_current()
              else:
                state = "done solve"
                solve_time = pygame.time.get_ticks() - start_time
                solve_steps = steps

            case "Tremaux":
              if grid_cell.index(current_cell) != end:
                previous_cell, current_cell, stack, visited = Tremaux(grid_cell, current_cell, stack, previous_cell, visited)
                # if current_cell.path:
                #   minus_count += 1
                #   current_cell.path = None
                # else:
                #   current_cell.path = steps - minus_count
                current_cell.draw_current()
              else:
                state = "done solve"
                solve_time = pygame.time.get_ticks() - start_time
                solve_steps = steps
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
        # [cells.draw_path() for cells in grid_cell]
      case "Introduction":
        screen.fill(pygame.Color("tan"))

        font = pygame.font.Font(None, 54)
        title_text = font.render("Maze Craft", True, pygame.Color("dark green"))
        screen.blit(title_text, (GUI_WIDTH // 2 - title_text.get_width() // 2, 50))

        for count, i in enumerate(["MazeCraft is a versatile software tool that excels as both a maze solver",
                  "and generator. As a solver, it swiftly navigates through mazes using algorithms,",
                  "providing optimal solutions with real-time visualizations. On the creation side, " ,
                  "MazeCraft lets users generate mazes, adjusting algorithms or size and for various",
                  "applications. With an intuitive interface and broad versatility, MazeCraft is your ", 
                  "all-in-one solution for maze-related challenges from entertainment to education and", 
                  "problem-solving."]):
          draw_text(screen,i,pygame.font.Font(None, 24), pygame.Color("Black"), (100+40*(count+1), 30))

    if state not in ["menu", "prepare"]:
      button_text = "Back"
      font = pygame.font.Font(None, 36)
      text_surface = font.render(button_text, True, pygame.Color("White"))
      button_rect = pygame.Rect(50, GUI_HEIGHT-50, 100, 25)
      text_rect = text_surface.get_rect(center=button_rect.center)
      pygame.draw.rect(screen, (0, 128, 255), button_rect)
      screen.blit(text_surface, text_rect)
      
    if state in ["solve maze", "done solve"]:
      button_text = "Reset"
      font = pygame.font.Font(None, 36)
      text_surface = font.render(button_text, True, pygame.Color("White"))
      button_rect = pygame.Rect(200, GUI_HEIGHT-50, 100, 25)
      text_rect = text_surface.get_rect(center=button_rect.center)
      pygame.draw.rect(screen, (0, 128, 255), button_rect)
      screen.blit(text_surface, text_rect)
      
    if state not in ["menu", "prepare", "Introduction"]:
      button_text = pause
      font = pygame.font.Font(None, 36)
      text_surface = font.render(button_text, True, pygame.Color("White"))
      button_rect = pygame.Rect(350, GUI_HEIGHT-50, 120, 25)
      text_rect = text_surface.get_rect(center=button_rect.center)
      pygame.draw.rect(screen, (0, 128, 255), button_rect)
      screen.blit(text_surface, text_rect)
    
    if state not in ["menu", "prepare", "Introduction"]:
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
        else:
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

    pygame.display.flip()

    clock.tick(FPS)


if __name__ == "__main__":
  main()
