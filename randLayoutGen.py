# python randLayoutGen.py -r 5 -c 6 -g 5 -f 5 -l randWaste

import random
import argparse

#function to write the layout in .lay file
def write_layout(pacman_layout, filename):
    file = open(f"layouts/{filename}.lay", "w")
    for row in pacman_layout:
        for col in row:
            file.write(col)
        file.write("\n")
    file.close()


# Function to generate a random layout
def random_layout(rows, cols, num_ghosts, num_power_pellets):
    # Create the empty board
    board = [[' ' for c in range(cols)] for r in range(rows)]

    # Place the Pacman
    board[random.randint(1, rows-2)][random.randint(1, cols-2)] = 'P'

    # Place the Ghosts
    for _ in range(num_ghosts):
        board[random.randint(1, rows-2)][random.randint(1, cols-2)] = 'G'

    # Place the obstacles
    num_obstacles = random.randint(rows*cols-50, rows*cols-2)
    for _ in range(num_obstacles):
        board[random.randint(1, rows-2)][random.randint(1, cols-2)] = '%'

    # Place the food
    num_food = random.randint(rows*cols-50, rows*cols-25)
    for f in range(num_food):
        board[random.randint(1, rows-2)][random.randint(1, cols-2)] = '.'

    # Place the power pellets
    for p in range(num_power_pellets):
        board[random.randint(1, rows-2)][random.randint(1, cols-2)] = 'o'

    # Place the no Food
    num_no_food_zones = random.randint(3, 5)
    for z in range(num_no_food_zones):
        board[random.randint(1, rows-2)][random.randint(1, cols-2)] = ' '

    # Place the borders
    for c in range(cols):
        board[0][c] = '%'
        board[rows-1][c] = '%'
    for r in range(rows):
        board[r][0] = '%'
        board[r][cols-1] = '%'

    # Ensure there is at least one Pacman and given number of ghosts and given number of pellets
    pacman_present = False
    ghost_count = 0
    pellet_count = 0
    for row in board:
        for col in row:
            if col == "P":
                pacman_present = True
            if col == "G":
                ghost_count += 1
            if col == "o":
                pellet_count += 1
    if ghost_count < num_ghosts:
        while ghost_count < num_ghosts:
            board[random.randint(1, rows-2)][random.randint(1, cols-2)] = "G"
            ghost_count += 1
    if pellet_count < num_power_pellets:
        while pellet_count < num_power_pellets:
            board[random.randint(1, rows-2)][random.randint(1, cols-2)] = "G"
            pellet_count += 1
    if not pacman_present:
        board[random.randint(1, rows-2)][random.randint(1, cols-2)] = "P"
    
    return board


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--rows', dest='rows', help='Number of rows in grid', default=5)
    parser.add_argument('-c', '--cols', dest='cols', help='Number of columns in grid', default=5)
    parser.add_argument('-g', '--ghosts', dest='ghosts', help='Number of ghosts', default=2)
    parser.add_argument('-f', '--food', dest='food', help='Number of food pallets', default=10)
    parser.add_argument('-l', '--layout', dest='layout', help='layout Name for saving', default="rand")
    args = parser.parse_args()
    pacman_layout = random_layout(int(args.rows), int(args.cols), int(args.ghosts), int(args.food))
    write_layout(pacman_layout, args.layout)
