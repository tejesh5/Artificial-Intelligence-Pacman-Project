import random
import numpy as np
import argparse

class CellGrid:
    """CellGrid class that defines each walkable CellGrid on the grid"""
    def __init__(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y
        self.visited = 0
        self.Bloackedwalls = [1, 1, 1, 1]


    def getAllChildren(self, grid):
        """Check if the CellGrid has any surrounding unvisited CellGrids that are walkable"""
        a = [(1, 0), (-1,0), (0, 1), (0, -1)]
        children = []
        for x, y in a:
            if self.x+x in [len(grid), -1] or self.y+y in [-1, len(grid)]: continue
            if grid[self.y+y][self.x+x].visited: continue
            children.append(grid[self.y+y][self.x+x])
        return children


def removeWalls(current, choice):
    """Removeing the wall between two CellGrids"""
    if choice.x > current.x:     
        current.Bloackedwalls[1] = 0
        choice.Bloackedwalls[0] = 0
    elif choice.x < current.x:
        current.Bloackedwalls[0] = 0
        choice.Bloackedwalls[1] = 0
    elif choice.y > current.y:
        current.Bloackedwalls[3] = 0
        choice.Bloackedwalls[2] = 0
    elif choice.y < current.y:
        current.Bloackedwalls[2] = 0
        choice.Bloackedwalls[3] = 0


def drawWallsOverLayout(grid, WalledbinGridLayout):
    """Draw existing walls around CellGrids"""
    for yindex, y in enumerate(grid):
        for xindex, x in enumerate(y):
            for i, w in enumerate(x.Bloackedwalls):
                if i == 3 and w: WalledbinGridLayout[yindex*2+2][xindex*2+1] = '%'
                if i == 2 and w: WalledbinGridLayout[yindex*2][xindex*2+1] = '%'
                if i == 1 and w: WalledbinGridLayout[yindex*2+1][xindex*2+2] = '%'
                if i == 0 and w: WalledbinGridLayout[yindex*2+1][xindex*2] = '%'
    return WalledbinGridLayout


def drawBorderWalls(grid):
    """Draw a border around the maze"""
    length = len(grid)
    for row in grid: row[0] = row[length-1] = '%'
        
    grid[0] = grid[length-1] = ['%'] * length
    return grid


def displayMazeLayouts(grid):
    """Draw the maze using ASCII characters and display the maze"""
    length = len(grid)*2+1
    WalledbinGridLayout = []
    for x in range(length):
        if x % 2 == 0: WalledbinGridLayout.append([' ' if x % 2 != 0 else '%' for x in range(length)])
        else: WalledbinGridLayout.append([' '] * length)
    
    WalledbinGridLayout = drawWallsOverLayout(grid, WalledbinGridLayout)
            
    WalledbinGridLayout = drawBorderWalls(WalledbinGridLayout)

    # print('\n'.join([''.join(x) for x in WalledbinGridLayout]))
    return WalledbinGridLayout


# Request the user to input a maze size and initialise the maze, stack and initial CellGrid
# size = int(input('Enter a maze size: '))

def finishLayouts(size, ghosts, power, foods):
    grid = [[CellGrid(x, y) for x in range(size)] for y in range(size)]
    current = grid[0][0]
    stack = []

    # Main loop to generate the maze
    while 1:
        current.visited = 1
        children = current.getAllChildren(grid)

        if children:
            choice = random.choice(children)
            choice.visited = 1

            stack.append(current)
            removeWalls(current, choice)
            current = choice
        
        elif stack: current = stack.pop()
        else: break

    grid_display = displayMazeLayouts(grid)

    new_grid = [grid_display[0]]

    # first row and last row are ignored
    for curr_row in grid_display[1:len(grid_display) - 1]:
        count = curr_row.count("%") - 2
        rnd_count = round(np.random.uniform(low = 0, high = count/1.5))
        
        list_of_walls = []
        for index in range(1, len(curr_row) - 1):
            if curr_row[index] == "%": list_of_walls.append(index)
        
        indexes_to_be_replaced = np.random.choice(list_of_walls, rnd_count, replace = 0)
    #     print(indexes_to_be_replaced)
    #     print("Previous: ", curr_row)
        for idx in indexes_to_be_replaced: curr_row[idx] = " "
    #     print("After   : ", curr_row)
        new_grid.append(curr_row)
    new_grid.append(grid_display[-1])

    # addign food pellets:
    for curr_row in new_grid:
        for index, element in enumerate(curr_row):
            if element == " ":
                if np.random.random() < foods: curr_row[index] = "."


    new_grid[1][1] = "P"


    # the logic will support for any number of ghosts.
    # The ghosts will be initiated in the bottom part of the randomly generated grid.

    width = len(new_grid[0]) 
    height = len(new_grid)

    empty_locations = []
    for x in range(width):
        for y in range(height):
            if new_grid[x][y] == " ": empty_locations.append((x, y))


    for i in range(ghosts):
        curr_empty_location = empty_locations[-1 * (i + 1)]
        new_grid[curr_empty_location[0]][curr_empty_location[1]] = "G"
        empty_locations.remove((curr_empty_location[0], curr_empty_location[1]))

    for i in range(power):
        curr_empty_location = random.choice(empty_locations)
        new_grid[curr_empty_location[0]][curr_empty_location[1]] = "o"
        empty_locations.remove((curr_empty_location[0], curr_empty_location[1]))

    return '\n'.join([''.join(x) for x in new_grid])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--ghosts', dest='ghosts', help='Number of Ghosts', default=0)
    parser.add_argument('-s', '--size', dest='size', help='number of rows', default=10)
    parser.add_argument('-p', '--power', dest='power', help='Number of power pallets', default=1)
    parser.add_argument('-f', '--food', dest='food', help='Probability of food generation', default=1)
    parser.add_argument('-o', '--file', dest='file', help='File to save the layout', default='')
    args = parser.parse_args()
    genLayout = finishLayouts(int(int(args.size)/2), int(args.ghosts), int(args.power), float(args.food))
    if args.file:
        with open(f"layouts/{args.file}.lay", 'w') as f:
            f.write(genLayout + '\n')
    else:
        print(genLayout)