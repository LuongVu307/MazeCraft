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
		self.path = False
		self.fake_visited = False

	def draw(self):
		x, y = self.x * self.TILE, self.TILE * self.y

		x += self.bias_x
		y += self.bias_y

		if self.visited or self.fake_visited:
			pygame.draw.rect(self.screen, pygame.Color("black"),
											 (x, y, self.TILE, self.TILE))

		if self.walls["right"]:
			pygame.draw.line(self.screen, pygame.Color("lightgreen"),
											 (x + self.TILE, y), (x + self.TILE, y + self.TILE), 1)
		if self.walls["left"]:
			pygame.draw.line(self.screen, pygame.Color("lightgreen"),
											 (x, y + self.TILE), (x, y), 1)
		if self.walls["top"]:
			pygame.draw.line(self.screen, pygame.Color("lightgreen"), (x, y),
											 (x + self.TILE, y), 1)
		if self.walls["bottom"]:
			pygame.draw.line(self.screen, pygame.Color("lightgreen"),
											 (x + self.TILE, y + self.TILE), (x, y + self.TILE), 1)

	def draw_current(self):
		x, y = self.x * self.TILE, self.TILE * self.y

		x += self.bias_x + self.TILE//(2)
		y += self.bias_y + self.TILE//(2)

		pygame.draw.circle(self.screen, pygame.Color("red"), (x, y), self.TILE//(2.5))

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

	# def draw_path(self):
	# 	if self.path:
	# 		x, y = self.x * self.TILE, self.TILE * self.y

	# 		x += self.bias_x + self.TILE//(2)
	# 		y += self.bias_y + self.TILE//(2)
	# 		if self.path >= 1020:
	# 			self.path  %= 1020
	# 		if self.path < 255:
	# 			pygame.draw.circle(self.screen, (self.path, 0, 0), (x, y), self.TILE//(4))
	# 		elif self.path < 510:
	# 			pygame.draw.circle(self.screen, (255, self.path-255, 0), (x, y), self.TILE//(4))
	# 		elif self.path < 1020:
	# 			pygame.draw.circle(self.screen, (255, 255, self.path-510), (x, y), self.TILE//(4))

	def check_next_neighbor(self, grid_cell, pre_cell, direction=random.choice(["up", "down", "left", "right"])):
		neighbor = []
		top = self.check_cell(self.x, self.y - 1, grid_cell)
		right = self.check_cell(self.x + 1, self.y, grid_cell)
		bottom = self.check_cell(self.x, self.y + 1, grid_cell)
		left = self.check_cell(self.x - 1, self.y, grid_cell)

		if direction == "up":
			if left and not self.walls["left"]:
				neighbor.append(left)
			if top and not self.walls["top"]:
				neighbor.append(top)
			if right and  not self.walls["right"]:
				neighbor.append(right)
			if bottom and not self.walls["bottom"]:
				neighbor.append(bottom)
		elif direction == "right":
			if top and not self.walls["top"]:
				neighbor.append(top)
			if right and  not self.walls["right"]:
				neighbor.append(right)
			if bottom and not self.walls["bottom"]:
				neighbor.append(bottom)
			if left and not self.walls["left"]:
				neighbor.append(left)
		elif direction == "down":
			if right and  not self.walls["right"]:
				neighbor.append(right)
			if bottom and not self.walls["bottom"]:
				neighbor.append(bottom)
			if left and not self.walls["left"]:
				neighbor.append(left)
			if top and not self.walls["top"]:
				neighbor.append(top)

		elif direction == "left":
			if bottom and not self.walls["bottom"]:
				neighbor.append(bottom)
			if left and not self.walls["left"]:
				neighbor.append(left)
			if right and  not self.walls["right"]:
				neighbor.append(right)
			if top and not self.walls["top"]:
				neighbor.append(top)


		if len(neighbor) > 1 and pre_cell in neighbor:
			neighbor.remove(pre_cell)

		return neighbor


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

def Eller(grid_cell, rows, cols, count, set_cell):
	if cols * count < len(grid_cell):

		i = cols * count
		ls = []
		while i < cols * (count + 1) - 1:
			cells = set()
			if random.randint(1, 10) > 5:
				rm_walls(grid_cell[i], grid_cell[i + 1])
				grid_cell[i].fake_visited, grid_cell[i + 1].fake_visited = True, True
				cells.add(i)
				cells.add(i + 1)
			else:
				cells.add(i)

			if count > 0:
				if random.randrange(1, 10) > 5:
					rm_walls(grid_cell[i], grid_cell[i - cols])
					grid_cell[i].fake_visited, grid_cell[i - cols].fake_visited = True, True
					cells.add(i)
					cells.add(i - cols)
				else:
					cells.add(i)

			ls.append(cells)
			i += 1
		num = 0
		for i in ls:
			for j in i:
				num += 1
		if num != cols * (count + 1):
			ls.append(set([cols * (count + 1) - 1]))

		merged_sets = []

		for set1 in set_cell:
			merged = False

			for merged_set in merged_sets:
				if any(element in merged_set for element in set1):
					merged_set.update(set1)
					merged = True
					break

			if not merged:
				merged_sets.append(set1.copy())

		for set2 in ls:
			merged = False

			for merged_set in merged_sets:
				if any(element in merged_set for element in set2):
					merged_set.update(set2)
					merged = True
					break

			if not merged:
				merged_sets.append(set2.copy())

		return merged_sets

	else:
		ls = set_cell.copy()
		while True:
			num_set = random.randint(0, len(ls) - 1)
			set_chosen = ls[num_set]

			num_chosen = random.choice(list(set_chosen))
			cell_chosen = grid_cell[num_chosen]

			next_cell = cell_chosen.check_neighbor(grid_cell)
			if next_cell and grid_cell.index(next_cell) not in set_chosen:
				rm_walls(cell_chosen, next_cell)
				cell_chosen.fake_visited, next_cell.fake_visited = True, True
				next_cell.draw_current()
				set_chosen.add(grid_cell.index(next_cell))
				break

		merged_sets = []

		for new_set in ls:
			sets_to_merge = []

			for existing_set in merged_sets:
				if any(element in existing_set for element in new_set):
					sets_to_merge.append(existing_set)

			if sets_to_merge:
				merged_set = set().union(new_set, *sets_to_merge)
				merged_sets = [s for s in merged_sets if s not in sets_to_merge]
				merged_sets.append(merged_set)
			else:
				merged_sets.append(new_set.copy())

		if len(merged_sets) == 1:
			return False
		return merged_sets

def HuntKill(current_cell, grid_cell):
	current_cell.visited = True

	current_cell.draw_current()

	next_cell = current_cell.check_neighbor(grid_cell)
	count = 0
	if next_cell:
		next_cell.visited = True
		rm_walls(current_cell, next_cell)
		current_cell = next_cell
	else:
		for i in range(len(grid_cell)):
			#grid_cell[i].draw_current()
			if grid_cell[i].visited is True:
				count += 1
				if grid_cell[i].check_neighbor(grid_cell):
					current_cell = grid_cell[i]
					break

		if count == len(grid_cell):
			return False

	return current_cell

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

def check_dir(grid_cell, current_cell, next_cell):
		if next_cell:
				c, n = grid_cell.index(current_cell), grid_cell.index(next_cell)
				if c == n + 1:
						return "right"
				elif c == n - 1:
						return "left"
				elif c < n - 1:
						return "up"
				else:
						return "down"
		else:
				return "right"

def RandomMouse(grid_cell, current_cell, previous_cell):
		next_cell = random.choice(current_cell.check_next_neighbor(grid_cell, previous_cell))
		return current_cell, next_cell

def HandOnWall(grid_cell, current_cell, previous_cell):

		direction = check_dir(grid_cell, current_cell, previous_cell)
		list_choice = current_cell.check_next_neighbor(grid_cell, previous_cell,  direction)


		# print([grid_cell.index(i) for i in list_choice])
		# time.sleep(1)
		return current_cell, list_choice[0]

def Tremaux(grid_cell, current_cell, stack, previous_cell, visited):
		list_choice = current_cell.check_next_neighbor(grid_cell, previous_cell)
		choices = []
		for i in list_choice:
				if i  not in visited:
						choices.append(i)

		if choices:
				next_cell = random.choice(choices)
				visited.append(next_cell)
				stack.append(next_cell)
		else:
				stack.pop()
				next_cell = stack[-1]


		return current_cell, next_cell, stack, visited
