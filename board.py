import random
import os

#Create 10x10 board
board = [['.' for _ in range(10)] for _ in range(10)]

#Constants T, S, Z
T = 'T' #Cross road
S = 'S' #S-Type turn, on the y axis it looks like an S.
Z = 'Z' #Z-Type turn, on the y axis it looks like a Z.

#Choose a random edge point, exclude corners
def random_edge_point():
    edge_points = []
    
    #All points on the top and bottom edges, exclude corners
    for col in range(1, 9):
        edge_points.append((0, col))   # Top row (exclude corners)
        edge_points.append((9, col))   # Bottom row (exclude corners)

    #All points on the left and right edges, exclude corners
    for row in range(1, 9):
        edge_points.append((row, 0))   # Left column (exclude corners)
        edge_points.append((row, 9))   # Right column (exclude corners)
    
    #Choose random point from the valid edge points
    return random.choice(edge_points)

#Initialize previous_point from random_point
def initialize_previous_point(random_point):
    x, y = random_point
    prev_x = x
    prev_y = y

    # If x or y is at the edge (0 or 9), adjust accordingly
    if x == 0:
        prev_x = -1
    elif x == 9:
        prev_x = 10

    if y == 0:
        prev_y = -1
    elif y == 9:
        prev_y = 10

    return (prev_x, prev_y)


#Tile Rules influence the next point position.
def next_point(prev, current, constant):
    prev_x, prev_y = prev
    curr_x, curr_y = current
    next_x, next_y = curr_x, curr_y

    if constant == T:
        # For T: Move in the same direction along x or y axis.
        if prev_x > curr_x:  # previous x > current x, move x-1
            next_x -= 1
        elif prev_x < curr_x:  # previous x < current x, move x+1
            next_x += 1
        elif prev_y > curr_y:  # previous y > current y, move y-1
            next_y -= 1
        elif prev_y < curr_y:  # previous y < current y, move y+1
            next_y += 1

    elif constant == S:
        # For S: Swap x/y movement based on comparison
        if prev_x > curr_x:  # previous x > current x, move y+1
            next_y += 1
        elif prev_x < curr_x:  # previous x < current x, move y-1
            next_y -= 1
        elif prev_y > curr_y:  # previous y > current y, move x+1
            next_x += 1
        elif prev_y < curr_y:  # previous y < current y, move x-1
            next_x -= 1

    elif constant == Z:
        # For Z: Inverse swap x/y movement
        if prev_x > curr_x:  # previous x > current x, move y-1
            next_y -= 1
        elif prev_x < curr_x:  # previous x < current x, move y+1
            next_y += 1
        elif prev_y > curr_y:  # previous y > current y, move x-1
            next_x -= 1
        elif prev_y < curr_y:  # previous y < current y, move x+1
            next_x += 1
            
    return next_x, next_y


#Function to display the grid with all previous steps
def display_grid(current, next_pt, constant):
    #Update board with the constant at the current point
    x, y = current
    board[x][y] = constant

    #Display grid
    for i in range(10):
        row_display = ""
        for j in range(10):
            if (i, j) == next_pt:
                row_display += " X "  #Mark next point with "X"
            else:
                row_display += f" {board[i][j]} "  #Show the letter or "."
        print(row_display)
    print("\n" + "-"*35)  #Separator

#Handle triggering of existing rules
def handle_existing_rule(current, next_pt):
    next_x, next_y = next_pt
    existing_letter = board[next_x][next_y]

    if existing_letter == T:
        print(f"Triggering rule of T at {next_pt}")
        return next_point(current, next_pt, T)
    elif existing_letter == S:
        print(f"Triggering rule of S at {next_pt}")
        return next_point(current, next_pt, S)
    elif existing_letter == Z:
        print(f"Triggering rule of Z at {next_pt}")
        return next_point(current, next_pt, Z)
    
    return next_pt  # Return current if no existing letter is found

#Check if the next point is out of bounds
def is_out_of_bounds(point):
    x, y = point
    return x < 0 or x > 9 or y < 0 or y > 9

#Main
#Clear the terminal
def clear_terminal():
    if os.name == 'nt':
        os.system('cls')



#Prompt function
def prompt():
    random_point = random_edge_point()
    previous_point = initialize_previous_point(random_point)
    
    game_running = True #Loop control flag
    
    while game_running:
        
        clear_terminal()
        display_grid(random_point, None, 'X')
        
        #Prompt for user input
        constant = input("Choose the next tile (T, S, Z): ").upper()
        
        #Check for valid input
        while constant not in ['T', 'S', 'Z']:
            print("Invalid input. Please enter 'T', 'S', or 'Z'.")
            constant = input("Choose the next constant (T, S, Z): ").upper()

        next_pt = next_point(previous_point, random_point, constant)
    
        if is_out_of_bounds(next_pt):
            print(f"Terminating: The next point {next_pt} is out of bounds!")
            game_running = False
    
        #If the next point has an existing letter, trigger the rule
        while board[next_pt[0]][next_pt[1]] in [T, S, Z]:
            next_pt = handle_existing_rule(random_point, next_pt)
            if is_out_of_bounds(next_pt):
                print(f"Terminating: The next point {next_pt} is out of bounds!")
                game_running = False
                break
        #Display the grid with current, next, and previous placements
        display_grid(random_point, next_pt, constant)
    
        #Update previous and current points for the next iteration
        previous_point = random_point
        random_point = next_pt
#Call prompt
prompt()