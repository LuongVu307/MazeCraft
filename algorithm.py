import pygame
import random

class Cell:

	def __init__(self, x, y, TILE, screen, cols, rows):
		self.TILE = TILE
		self.screen = screen
		self.cols = cols
		self.rows = rows
		self.visited = False
		self.bias_x, self.bias_y = 50, 100
		self.x, self.y = x, y
		self.walls = {"right": True, "left": True, "top": True, "bottom": True}
		self.fake_visited = False
		self.generated = False
		self.end, self.start = False, False
		self.path = False
		self.gone_through = False

	def draw(self):			
		x, y = self.x * self.TILE, self.TILE * self.y

		x += self.bias_x
		y += self.bias_y

		if self.visited or self.generated or self.fake_visited:
			pygame.draw.rect(self.screen, pygame.Color("black"),
											 (x, y, self.TILE, self.TILE))
		if self.gone_through:
			pygame.draw.rect(self.screen, pygame.Color((218, 222, 115)),
											 (x, y, self.TILE, self.TILE))
		if self.path:
			pygame.draw.rect(self.screen, pygame.Color((199, 196, 0)),
											 (x, y, self.TILE, self.TILE))
		if self.start:
			pygame.draw.rect(self.screen, pygame.Color("green"),
											(x, y, self.TILE, self.TILE))
		elif self.end:
			pygame.draw.rect(self.screen, pygame.Color("red"),
											(x, y, self.TILE, self.TILE))
		if self.walls["right"]:
			pygame.draw.line(self.screen, pygame.Color("white"),
											 (x + self.TILE, y), (x + self.TILE, y + self.TILE), 1)
		if self.walls["left"]:
			pygame.draw.line(self.screen, pygame.Color("white"),
											 (x, y + self.TILE), (x, y), 1)
		if self.walls["top"]:
			pygame.draw.line(self.screen, pygame.Color("white"), (x, y),
											 (x + self.TILE, y), 1)
		if self.walls["bottom"]:
			pygame.draw.line(self.screen, pygame.Color("white"),
											 (x + self.TILE, y + self.TILE), (x, y + self.TILE), 1)

	def draw_1st(self):
		x, y = self.x * self.TILE, self.TILE * self.y

		x += self.bias_x
		y += self.bias_y
		draw_text(self.screen, "N", pygame.font.Font(None, 24), pygame.Color("White"), (110, 230-5))
		draw_text(self.screen, "E", pygame.font.Font(None, 24), pygame.Color("White"), (230-5, 360))
		draw_text(self.screen, "S", pygame.font.Font(None, 24), pygame.Color("White"), (360, 230-5))
		draw_text(self.screen, "W", pygame.font.Font(None, 24), pygame.Color("White"), (230-5, 110))
		if self.walls["right"]:
			pygame.draw.line(self.screen, pygame.Color("lightblue"),
											 (330, 140), (330, 340), 1)
		if self.walls["left"]:
			pygame.draw.line(self.screen, pygame.Color("lightblue"),
											 (130, 140), (130, 340), 1)
		if self.walls["top"]:
			pygame.draw.line(self.screen, pygame.Color("lightblue"),
											 (130, 140), (330, 140), 1)
		if self.walls["bottom"]:
			pygame.draw.line(self.screen, pygame.Color("lightblue"),
											 (130, 340), (330, 340), 1)

	def draw_current(self):
		x, y = self.x * self.TILE, self.TILE * self.y

		x += self.bias_x + self.TILE//(2)
		y += self.bias_y + self.TILE//(2)

		pygame.draw.circle(self.screen, pygame.Color("white"), (x, y), self.TILE//(2.5))

	def check_cell(self, x, y, grid_cell):
		find_index = lambda x, y: x + y * self.cols

		if x < 0 or x > self.cols - 1 or y < 0 or y > self.rows - 1:
			return False

		return grid_cell[find_index(x, y)]

	def check_neighbor(self, grid_cell):
		neighbor = []
		top = self.check_cell(self.x, self.y - 1, grid_cell)
		right = self.check_cell(self.x + 1, self.y, grid_cell)
		bottom = self.check_cell(self.x, self.y + 1, grid_cell)
		left = self.check_cell(self.x - 1, self.y, grid_cell)

		if top and not top.visited:
			neighbor.append(top)
		if right and not right.visited:
			neighbor.append(right)
		if bottom and not bottom.visited:
			neighbor.append(bottom)
		if left and not left.visited:
			neighbor.append(left)

		return random.choice(neighbor) if neighbor else False

	def check_next_neighbor(self, grid_cell):
		neighbor = []
		top = self.check_cell(self.x, self.y - 1, grid_cell)
		right = self.check_cell(self.x + 1, self.y, grid_cell)
		bottom = self.check_cell(self.x, self.y + 1, grid_cell)
		left = self.check_cell(self.x - 1, self.y, grid_cell)

		if left and not self.walls["left"]:
			neighbor.append(left)
		if top and not self.walls["top"]:
			neighbor.append(top)
		if right and  not self.walls["right"]:
			neighbor.append(right)
		if bottom and not self.walls["bottom"]:
			neighbor.append(bottom)
		
		random.shuffle(neighbor)
		return neighbor

def draw_text(screen, text, font, color, position):
  text_surface = font.render(text, True, color)
  text_rect = text_surface.get_rect()
  text_rect.left = position[1]
  text_rect.centery = position[0]
  screen.blit(text_surface, text_rect)

def rm_walls(current, next):
	dx = current.x - next.x
	if dx == 1:
		current.walls["left"] = False
		next.walls["right"] = False
	elif dx == -1:
		current.walls["right"] = False
		next.walls["left"] = False

	dy = current.y - next.y

	if dy == 1:
		current.walls["top"] = False
		next.walls["bottom"] = False
	elif dy == -1:
		current.walls["bottom"] = False
		next.walls["top"] = False

def create_walls(current, next):
	dx = current.x - next.x
	if dx == 1:
		current.walls["left"] = True
		next.walls["right"] = True
	elif dx == -1:
		current.walls["right"] = True
		next.walls["left"] = True

	dy = current.y - next.y

	if dy == 1:
		current.walls["top"] = True
		next.walls["bottom"] = True
	elif dy == -1:
		current.walls["bottom"] = True
		next.walls["top"] = True

def RanDFS(current_cell, stack, grid_cell):
	current_cell.visited = True
	current_cell.draw_current()

	next_cell = current_cell.check_neighbor(grid_cell)
	if next_cell:
		next_cell.visited = True
		stack.append(current_cell)
		rm_walls(current_cell, next_cell)
		current_cell = next_cell
	elif stack:
		current_cell = stack.pop()

	return current_cell, stack

def RanPrims(grid_cell):
	ls = []

	for cell in grid_cell:
		if cell.visited is True:
			ls.append(cell)
	if len(ls) == len(grid_cell):
		return False

	while True:
		chosen_cell = random.choice(ls)
		next_cell = chosen_cell.check_neighbor(grid_cell)
		if next_cell and next_cell.visited == False:
			next_cell.visited = True
			rm_walls(chosen_cell, next_cell)
			next_cell.draw_current()
			break

	return grid_cell

def conv_cord(grid_cell, cols, current_cell):
	idx = grid_cell.index(current_cell)

	return idx//cols, idx%cols
def conv_idx(cols, row, col):
	return row*cols + col
def check_set(set_cell, first, sec):
	for i in set_cell:
		if first in i:
			if sec not in i:
				return True
			return False
		elif sec in i:
			if first not in i:
				return True
			return False
	return True
def list_merger(list_of_sets):
    merged_sets = []
    
    while list_of_sets:
        current_set = list_of_sets.pop(0)
        merged_set = {element for element in current_set}
        
        i = 0
        while i < len(list_of_sets):
            if any(element in merged_set for element in list_of_sets[i]):
                merged_set.update(list_of_sets.pop(i))
                i = 0  # Restart the loop after merging
            else:
                i += 1
        
        merged_sets.append(merged_set)
    
    return merged_sets

def Eller(grid_cell, rows, cols, set_cell, current_cell):
	# print(grid_cell.index(current_cell))
	#COLS: NUMBER OF COLUMNS
	#ROWS: NUMBER OF ROWS
	current_cell.draw_current()
	current_cell.visited = True
	row, col = conv_cord(grid_cell, cols, current_cell)
	current_cell = grid_cell.index(current_cell)
	if col+1 == cols and row+1 != rows:
		row_set = set([current_cell-i for i in range(cols)])
		matching_sets = [s for s in set_cell if any(cell in s for cell in row_set)]
		chosen_cells = []
		# print("MATCHING", matching_sets)
		for s in matching_sets:
			temp_s = []
			for i in s:
				if i in row_set:
					temp_s.append(i)
			# print(temp_s)
			for i in random.sample(temp_s, k=random.randint(0, len(temp_s)-1)):
				chosen_cells.append(i)
		# print("CHOSE", chosen_cells)
		for cell in row_set:
			row, col = conv_cord(grid_cell, cols, grid_cell[cell])
			next_cell = conv_idx(cols, row+1, col)
			if cell in chosen_cells:
				# print(cell, chosen_cells)
				grid_cell[next_cell].visited = True
				create_walls(grid_cell[cell], grid_cell[next_cell])
				add_cur, add_nex = False, False
				for i in set_cell:
					if cell in i:
						add_cur = True
					if add_nex in i:
						add_nex = True
				if not add_nex:
					set_cell.append(set([next_cell]))
				if not add_cur:
					set_cell.append(set([cell]))
			else:
				for i in range(len(set_cell)):
					if cell in set_cell[i]:
						set_cell[i].add(next_cell)
						done = True
						break
		# print("SET CE::", set_cell)
	else:
		# print("SET", set_cell)
		next_cell = conv_idx(cols, row, col+1)
		grid_cell[next_cell].visited = True
		if check_set(set_cell, current_cell, next_cell)==False:
			create_walls(grid_cell[current_cell], grid_cell[next_cell])
			add_cur, add_nex = False, False
			for i in set_cell:
				if current_cell in i:
					add_cur = True
				if next_cell in i:
					add_nex = True
			if not add_nex:
				set_cell.append(set([next_cell]))
			if not add_cur:
				set_cell.append(set([current_cell]))
		else:
			if row != rows-1:
				if random.randint(0, 1)==1:
					done = False
					for i in range(len(set_cell)):
						if current_cell in set_cell[i]:
							set_cell[i].add(next_cell)
							done = True
							break
					if not done:
						set_cell.append(set([current_cell, next_cell]))
				else:
					create_walls(grid_cell[current_cell], grid_cell[next_cell])
					add_cur, add_nex = False, False
					for i in set_cell:
						if current_cell in i:
							add_cur = True
						if next_cell in i:
							add_nex = True
					if not add_nex:
						set_cell.append(set([next_cell]))
					if not add_cur:
						set_cell.append(set([current_cell]))
			else:
				for i in range(len(set_cell)):
					if current_cell in set_cell[i]:
						if next_cell not in set_cell[i]:
							set_cell[i].add(next_cell)
							break
						else:
							create_walls(current_cell, next_cell)
	
	return grid_cell[current_cell+1], list_merger(set_cell)

def BinaryTree(current_cell, grid_cell, cols):
	current_cell.fake_visited = True
	current_cell.draw_current()
	if grid_cell.index(current_cell)//cols != 0 and grid_cell.index(current_cell)%cols != 0:
		if random.randint(0, 1):
			create_walls(current_cell, grid_cell[grid_cell.index(current_cell)-cols])
		else:
			create_walls(current_cell, grid_cell[grid_cell.index(current_cell)-1])

	return grid_cell[grid_cell.index(current_cell)+1]

def RanKruskal(grid_cell, set_cell):
	while True:
		choice = random.randint(0, len(grid_cell) - 1)
		current_cell = grid_cell[choice]
		next_cell = current_cell.check_neighbor(grid_cell)
		next_choice = grid_cell.index(next_cell)
		first, second = None, None
		for i in range(len(set_cell)):
			if choice in set_cell[i]:
				first = i
			if next_choice in set_cell[i]:
				second = i

		if first != second:
			current_cell.draw_current()
			next_cell.draw_current()
			rm_walls(current_cell, next_cell)
			current_cell.fake_visited, next_cell.fake_visited = True, True
			new_cell = set_cell[first] | set_cell[second]
			set_cell[first] = new_cell
			set_cell.pop(second)
			break

		if len(set_cell) == 1:
			return False

	return set_cell

def BFS(grid_cell, current_cell, queue, visited):
	list_choice = current_cell.check_next_neighbor(grid_cell)
	for i in list_choice:
		if i not in visited and i not in queue:
			queue.append(i)
	
	next_cell = queue.pop(0)
	visited.append(next_cell)
	return next_cell, queue, visited

def cal_cost(grid_cell, current_cell, end, cols):
	idx = grid_cell.index(current_cell)
	cell_pos = (idx//(cols), idx%(cols))

	return abs(end[0]-cell_pos[0]) + abs(end[1]-cell_pos[1])
def Greedy(grid_cell, current_cell, priority_queue, visited, end, cols):
		
	list_choice = current_cell.check_next_neighbor(grid_cell)
	for i in list_choice:
		if i not in visited and i not in [i[0] for i in priority_queue]:
			cost = cal_cost(grid_cell, current_cell, end, cols)
			priority_queue.append((cost, i))
			priority_queue = sorted(priority_queue, key=lambda x: x[0])

	next_cell = priority_queue.pop(0)[1]
	# print(cal_cost(grid_cell, next_cell, end, cols))
	visited.append(next_cell)

	# print([grid_cell.index(i) for i in list_choice])
	# time.sleep(1)
	return next_cell, priority_queue, visited

def DFS(grid_cell, current_cell, stack, visited):
	list_choice = current_cell.check_next_neighbor(grid_cell)
	for i in list_choice:
		if i not in visited and i not in stack:
			stack.append(i)

	next_cell = stack.pop(-1)
	visited.append(next_cell)

	return next_cell, stack, visited
