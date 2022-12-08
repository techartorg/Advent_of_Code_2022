#! python3.11
"""
--- Day 8: Treetop Tree House ---
The expedition comes across a peculiar patch of tall trees all planted carefully in a grid. The Elves explain that a previous expedition planted these trees as a reforestation effort. Now, they're curious if this would be a good location for a tree house.

First, determine whether there is enough tree cover here to keep a tree house hidden. To do this, you need to count the number of trees that are visible from outside the grid when looking directly along a row or column.

The Elves have already launched a quadcopter to generate a map with the height of each tree (your puzzle input). For example:

30373
25512
65332
33549
35390

Each tree is represented as a single digit whose value is its height, where 0 is the shortest and 9 is the tallest.

A tree is visible if all of the other trees between it and an edge of the grid are shorter than it. Only consider trees in the same row or column; that is, only look up, down, left, or right from any given tree.

All of the trees around the edge of the grid are visible - since they are already on the edge, there are no trees to block the view. In this example, that only leaves the interior nine trees to consider:

	The top-left 5 is visible from the left and top. (It isn't visible from the right or bottom since other trees of height 5 are in the way.)
	The top-middle 5 is visible from the top and right.
	The top-right 1 is not visible from any direction; for it to be visible, there would need to only be trees of height 0 between it and an edge.
	The left-middle 5 is visible, but only from the right.
	The center 3 is not visible from any direction; for it to be visible, there would need to be only trees of at most height 2 between it and an edge.
	The right-middle 3 is visible from the right.
	In the bottom row, the middle 5 is visible, but the 3 and 4 are not.

With 16 trees visible on the edge and another 5 visible in the interior, a total of 21 trees are visible in this arrangement.

Consider your map; how many trees are visible from outside the grid?

Your puzzle answer was 1693.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
Content with the amount of tree cover available, the Elves just need to know the best spot to build their tree house: they would like to be able to see a lot of trees.

To measure the viewing distance from a given tree, look up, down, left, and right from that tree; stop if you reach an edge or at the first tree that is the same height or taller than the tree under consideration. (If a tree is right on the edge, at least one of its viewing distances will be zero.)

The Elves don't care about distant trees taller than those found by the rules above; the proposed tree house has large eaves to keep it dry, so they wouldn't be able to see higher than the tree house anyway.

In the example above, consider the middle 5 in the second row:

30373
25512
65332
33549
35390

Looking up, its view is not blocked; it can see 1 tree (of height 3).
Looking left, its view is blocked immediately; it can see only 1 tree (of height 5, right next to it).
Looking right, its view is not blocked; it can see 2 trees.
Looking down, its view is blocked eventually; it can see 2 trees (one of height 3, then the tree of height 5 that blocks its view).

A tree's scenic score is found by multiplying together its viewing distance in each of the four directions. For this tree, this is 4 (found by multiplying 1 * 1 * 2 * 2).

However, you can do even better: consider the tree of height 5 in the middle of the fourth row:

30373
25512
65332
33549
35390

Looking up, its view is blocked at 2 trees (by another tree with a height of 5).
Looking left, its view is not blocked; it can see 2 trees.
Looking down, its view is also not blocked; it can see 1 tree.
Looking right, its view is blocked at 2 trees (by a massive tree of height 9).

This tree's scenic score is 8 (2 * 2 * 1 * 2); this is the ideal spot for the tree house.

Consider each tree on your map. What is the highest scenic score possible for any tree?

Your puzzle answer was 422059.

Both parts of this puzzle are complete! They provide two gold stars: **

"""
from collections import deque

_DEBUG_1 = False
_DEBUG_2 = False

test_data = ['30373',
			 '25512',
			 '65332',
			 '33549',
			 '35390'
			]

LOOK_UP = 1
LOOK_DOWN = -1
LOOK_LEFT = -1
LOOK_RIGHT = 1

class TreeGrid():

	def __init__(self, raw_data):
		self.trees_by_col = deque()
		self.trees_by_row = deque()

		self.temp_trees_by_col = deque()
		self.temp_trees_by_row = deque()

		self.parse_data(raw_data)


	def _render(self,data = None):
		if data is None:
			data = self.trees_by_row

		for row in data:
			print(f'\t{str(list(row))}') # Numpy-style output
			# print(''.join([str(x) for x in row])) # string-style output


	def parse_data(self, raw_data):
		data = deque()

		for i in raw_data:
			row = deque([int(x) for x in i])
			data.append(row)

		self.trees_by_row = data

		# Transpose the row data into columns. Thanks numpy
		for i in range(0, len(self.trees_by_row[0])):
			column = [x[i] for x in self.trees_by_row]
			self.trees_by_col.append(column)


	def check_visibility(self, x, y, row = True):
		is_visible = False
		trees = []
		visible_trees = 0
		current_tree_height = 0

		if row:
			trees = list(self.trees_by_row[y])
			current_tree_height = self.trees_by_row[y][x]

			tallest_preceding_trees = max(trees[0:x])
			tallest_following_trees = max(trees[x + 1:])

		else:
			trees = list(self.trees_by_col[x])
			current_tree_height = self.trees_by_col[x][y]

			tallest_preceding_trees = max(trees[0:y])
			tallest_following_trees = max(trees[y + 1:])

		if current_tree_height > tallest_preceding_trees:
			is_visible = True
			if _DEBUG_1:
				if row:
					print(f'\tTree {x} is visible from the left')
				else:
					print(f'\tTree {x} is visible from the top')

		elif current_tree_height > tallest_following_trees:
			is_visible = True
			if _DEBUG_1:
				if row:
					print(f'\tTree {x} is visible from the right')
				else:
					print(f'\tTree {x} is visible from the bottom')

		else:
			if row:
				is_visible = bool(self.check_visibility(x, y, row = False))

			elif is_visible:
				assert is_visible ==True, 'This should never happen'

			else:
				return visible_trees

		if is_visible:
			visible_trees = 1

		return visible_trees



	def calculate_visibility(self):
		total_visible_trees = 0

		width = len(self.trees_by_row[0])
		height = len(self.trees_by_row)

		# Walk the forest and check each tree, starting in the top left
		for y in range(1, height - 1):
			visible_trees = 0

			for x in range(1, width - 1):
				if self.check_visibility(x, y):
					visible_trees += 1

			if _DEBUG_1:
				print(f'Visible trees in row {y}: {visible_trees}\n')
			total_visible_trees += visible_trees

		# Finally, include the outer trees, which are always visible.
		total_visible_trees += len(self.trees_by_row[0]) * 2
		total_visible_trees += (len(self.trees_by_col[0]) - 2) * 2

		return total_visible_trees


	def check_scenic_score(self, x, y, row = True):
		scenic_score = 1
		trees = []
		preceding_trees = []
		following_trees = []

		current_tree_height = 0

		if row:
			trees = list(self.trees_by_row[y])
			current_tree_height = self.trees_by_row[y][x]

			preceding_trees = trees[0:x]
			following_trees = trees[x + 1:]

		else:
			trees = list(self.trees_by_col[x])
			current_tree_height = self.trees_by_col[x][y]

			preceding_trees = trees[0:y]
			following_trees = trees[y + 1:]

		# Look Left
		score = 0
		for tree in reversed(preceding_trees):
			if tree < current_tree_height:
				score += 1
			else:
				score += 1
				break # Bail out. We can't see past this tree

		if _DEBUG_2:
			if row:
				print(f'\tLooking left, the view is blocked at {score} trees')
			else:
				print(f'\tLooking up, the view is blocked at {score} trees')
		scenic_score *= score

		# Look Right
		score = 0
		for tree in following_trees:
			if tree < current_tree_height:
				score += 1
			else:
				score += 1
				break # Bail out. We can't see past this tree

		if _DEBUG_2:
			if row:
				print(f'\tLooking right, the view is blocked at {score} trees')
			else:
				print(f'\tLooking down, the view is blocked at {score} trees')
		scenic_score *= score

		return scenic_score


	def calculate_scenic_score(self):
		max_scenic_score = 0

		width = len(self.trees_by_row[0])
		height = len(self.trees_by_row)

		# Walk the forest and check each tree, starting in the top left
		for y in range(1, height - 1):
			for x in range(1, width - 1):
				if _DEBUG_2:
					print(f'Tree [{x},{y}]:')

				scenic_score = 1

				scenic_score *= self.check_scenic_score(x, y)
				scenic_score *= self.check_scenic_score(x, y, row = False)
				if _DEBUG_2:
					print(f'\tScenic score for this tree is: {scenic_score}\n')
				if scenic_score > max_scenic_score:
					max_scenic_score = scenic_score


		return max_scenic_score


	def draw(self):
		print(f'Round 0:')
		self._render(self.temp_trees_by_row)
		print()

		# Y-axis
		for i in range(0, len(self.trees_by_row) - 1): # End before we loop back on ourselves
			self.temp_trees_by_row.rotate(LOOK_UP)
			print(f'Round {i+1}:')
			self._render(self.temp_trees_by_row)
			print()

		self.temp_trees_by_row.rotate(LOOK_UP)
		print(f'Reset board:')
		self._render(self.temp_trees_by_row)
		print()

		print(f'Round 0:')
		self._render(self.temp_trees_by_col)
		print()

		# X-axis
		for i in range(0, len(self.trees_by_col) - 1): # End before we loop back on ourselves
			self.temp_trees_by_col.rotate(LOOK_RIGHT)
			print(f'Round {i+1}:')
			self._render(self.temp_trees_by_col)
			print()
		self.temp_trees_by_col.rotate(LOOK_RIGHT)
		print(f'Reset board:')
		self._render(self.temp_trees_by_col)
		print()


def main(raw_data):
	forest = TreeGrid(raw_data)
	total_visible_trees = forest.calculate_visibility()

	print(f'\nTotal number of visible trees! {total_visible_trees}\n\n************************\n')

	total_scenic_score = forest.calculate_scenic_score()
	print(f'\nTotal scenic score: {total_scenic_score}')


if __name__ == "__main__":
	input = r"D:\Projects\Advent_of_Code\2022\day_08_input.txt"
	raw_data = []

	with open(input, "r") as input_file:
		raw_data = input_file.read().split()

	# main(test_data)
	main(raw_data)