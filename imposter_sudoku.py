import argparse
import csv

parser = argparse.ArgumentParser(
    prog='imposter_sudoku.py',
    description='Solve an imposter sudoku puzzle.'
)

parser.add_argument('path', help='path to the imposter sudoku puzzle csv file')

args = parser.parse_args()

GRID_SIZE = 9
def print_puzzle(a):
    print(' ' * 6, '|', ' ' * 5, '|')
    for i in range(GRID_SIZE):
        print(end=" ")
        for j in range(GRID_SIZE):
            if j > 0 and j % 3 == 0: print("| ", end = "")
            print(a[i][j],end = " ")
        print()
        if i < 8 and (i + 1) % 3 == 0: print('-' * 23)
    print(' ' * 6, '|', ' ' * 5, '|')

def solve(grid, row, col, num):
    for x in range(9):
        if grid[row][x] == num:
            return False
             
    for x in range(9):
        if grid[x][col] == num:
            return False
 
    start_row = row - row % 3
    start_col = col - col % 3

    for i in range(3):
        for j in range(3):
            if grid[i + start_row][j + start_col] == num:
                return False
            
    return True
 
def solve_puzzle(grid, row, col):
    if (row == GRID_SIZE - 1 and col == GRID_SIZE):
        return True
    
    if col == GRID_SIZE:
        row += 1
        col = 0

    if grid[row][col] > 0:
        return solve_puzzle(grid, row, col + 1)
    
    for num in range(1, GRID_SIZE + 1, 1): 
        if solve(grid, row, col, num):
            grid[row][col] = num

            if solve_puzzle(grid, row, col + 1):
                return True
            
        grid[row][col] = 0

    return False

lines = []

with open(args.path) as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        lines.append(''.join(row))

orig_grid = '\n'.join(lines)

all_characters = []

for i in range(len(orig_grid)):
    character = orig_grid[i]
    if character not in all_characters:
        all_characters.append(character)

all_characters.remove('-')
all_characters.remove('\n')

for first_character_index in range(len(all_characters)):
    first_character = all_characters[first_character_index]
    for second_character_index in range(first_character_index + 1, len(all_characters)):
        second_character = all_characters[second_character_index]

        all_characters_set = set(all_characters)

        curr_grid = orig_grid
        curr_characters = all_characters_set - {first_character, second_character}

        num = 1
        character2num = {}
        num2character = {}

        for character_again in curr_characters:
            character2num[character_again] = num
            num2character[num] = character_again
            curr_grid = curr_grid.replace(character_again, str(num))
            num += 1

        curr_grid = curr_grid.replace(first_character, '0')
        curr_grid = curr_grid.replace(second_character, '0')
        curr_grid = curr_grid.replace('-', '0')
        grid_split = curr_grid.split('\n')

        grid = []

        for line in grid_split:
            row = []
            for character in line:
                row.append(int(character))
            grid.append(row)

        if (solve_puzzle(grid, 0, 0)):
            for row in range(len(grid)):
                for col in range(len(grid)):
                    grid[row][col] = num2character[grid[row][col]]

            print(f"\nSolution found for imposters: {first_character}, {second_character}!")
            print_puzzle(grid)
            print()
        else:
            print(f"Solution not found for imposters: {first_character}, {second_character}. They are not the imposters.")
