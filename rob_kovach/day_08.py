puzzle_input = open(__file__.replace('.py', '_input.txt')).read()

test_input = '''30373
25512
65332
33549
35390
'''

def test_visibility(grid, x, y):
    width = len(grid[0])
    height = len(grid)
    tree_height = grid[y][x]
    tests = 0

    for i in range(0, x):
        if grid[y][i] >= tree_height:
            tests += 1
            break

    for i in range(x+1, width):
        if grid[y][i] >= tree_height:
            tests += 1
            break

    for i in range(0, y):
        if grid[i][x] >= tree_height:
            tests += 1
            break

    for i in range(y+1, height):
        if grid[i][x] >= tree_height:
            tests += 1
            break
    
    if tests < 4:
        return True
    return False


def score_scenic(grid, x, y):
    width = len(grid[0])
    height = len(grid)
    tree_height = grid[y][x]
    up = 0
    down = 0
    left = 0
    right = 0

    for i in reversed(range(0, x)):
        if grid[y][i] <= tree_height:
            left += 1
            if grid[y][i] == tree_height:
                break
        else:
            left += 1
            break

    for i in range(x+1, width):
        if grid[y][i] <= tree_height:
            right += 1
            if grid[y][i] == tree_height:
                break
        else:
            right += 1
            break

    for i in reversed(range(0, y)):
        if grid[i][x] <= tree_height:
            up += 1
            if grid[i][x] == tree_height:
                break
        else:
            up += 1
            break

    for i in range(y+1, height):
        if grid[i][x] <= tree_height:
            down += 1
            if grid[i][x] == tree_height:
                break
        else:
            down += 1
            break

    return up * down * left * right


def run(input_):
    grid = []
    lines = input_.splitlines()
    for l in lines:
        list_ = [int(x) for x in l]
        grid.append(list_)
    
    width = len(grid[0])
    height = len(grid)
    count = (width * 2) + ((height - 2) * 2)

    scores = []

    for y in range(1, height-1):
        for x in range(1, width-1):
            visible = test_visibility(grid, x, y)
            if visible:
                count += 1
            
            scores.append(score_scenic(grid, x, y))

    return count, max(scores)

print(f'Part One: {run(puzzle_input)}')