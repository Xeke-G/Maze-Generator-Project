import random as rand
import math

def createMaze(numRow, numCol):
    maze = []
    map = []
    for rows in range(numRow):
        mazeRow = []
        mapRow = []
        for cols in range(numCol):
            cell = {"up":True,"down":True,"left":True,"right":True}
            mazeRow.append(cell)
            mapRow.append(False)
        maze.append(mazeRow)
        map.append(mapRow)
    return maze, map

def nav(maze, row, column):

    # empty list
    directions = []

    # if the position given in the maze is invalid, return None
    if not (0 <= row < len(maze) and 0 <= column < len(maze[0])): 
        return None
    
    
    # if the position ABOVE is valid, add the coordinate to the list with an identifying keyword. Otherwise add 'None'
    if 0 <= row - 1 < len(maze) and 0 <= column < len(maze[0]): 
        directions.append(("up", maze[row - 1][column]))
    else: 
        directions.append(("up", None))
        
    # if the position BELOW is valid, add the coordinate to the list with an identifying keyword. Otherwise add 'None'
    if 0 <= row + 1 < len(maze) and 0 <= column < len(maze[0]): 
        directions.append(("down", maze[row + 1][column]))
    else: 
        directions.append(("down", None))
        
    # if the position LEFT is valid, add the coordinate to the list with an identifying keyword. Otherwise add 'None'
    if 0 <= row < len(maze) and 0 <= column - 1 < len(maze[0]): 
        directions.append(("left", maze[row][column - 1]))
    else: 
        directions.append(("left", None))
        
    # if the position RIGHT is valid, add the coordinate to the list with an identifying keyword. Otherwise add 'None'
    if 0 <= row < len(maze) and 0 <= column + 1 < len(maze[0]): 
        directions.append(("right", maze[row][column + 1]))
    else: 
        directions.append(("right", None))
        

    # for direction, value in directions:
    #     if value is None: print(direction, "out of bounds")
    #     elif value == 1: print(direction, "wall")
    #     elif value == 0: print(direction, "path")
        
    return directions

def removeWall(maze, row, col, dir,Print=True):
    directions = nav(maze,row,col)
    removed = False
    if directions is not None:
        if dir == "up" and directions[0][1] is not None:
            maze[row][col]["up"] = False
            maze[row-1][col]["down"] = False
            removed = True
        elif dir == "down" and directions[1][1] is not None:
            maze[row][col]["down"] = False
            maze[row+1][col]["up"] = False
            removed = True
        elif dir == "left" and directions[2][1] is not None:
            maze[row][col]["left"] = False
            maze[row][col-1]["right"] = False
            removed = True
        elif dir == "right" and directions[3][1] is not None:
            maze[row][col]["right"] = False
            maze[row][col+1]["left"] = False
            removed = True
        if Print and removed: print("wall removed")
        elif Print and not removed: print("remove failed")
        return maze
    
    if Print: print("invalid position")
    return False

def printCells(maze):
    for row_index, row in enumerate(maze):
        for column_index, cell in enumerate(row):
            print((row_index, column_index), cell)
            
def displayMaze(maze):
    # easier to tell whats being printed where. the blank and path are needed because of the different spacing around a pipe vs dashes, i.e. the last print statement
    CORNER =  "+"   
    VWALL  =  "|"
    HWALL  =  "---"
    PATH   =  "    "
    BLANK  =  "   "
    
    numRows = len(maze)
    numCols = len(maze[0])
    
    
    for col in range(numCols):
        if maze[0][col]["up"] is True:
            print(CORNER,HWALL,end=" ")
        else: print(CORNER,PATH,end="")
    print(CORNER,"\n",end="")
    
    for row in range(numRows):
        
        i=0
        if maze[row][0]["left"] is True:
            print(VWALL,PATH,end="")
        else: print(PATH, end="")
        
        while i < numCols:
            if maze[row][i]["right"] is True and i == numCols-1:
                print(VWALL,end="")
            elif maze[row][i]["right"] is True:
                print(VWALL,PATH,end="")
            else: print(PATH, end="  ")
            i+=1
        print("\n",end="")
        print(CORNER, end=" ")
        
        i=0
        while i < numCols:
            if maze[row][i]["down"] is True:
                print(HWALL,CORNER,end=" ")
            else: print(BLANK,CORNER, end=" ")
            i+=1
        print("\n",end="")
        
def navigateMaze(maze,map,coords,Print=False):
    
    map[coords[0]][coords[1]] = True
        
    moveChoices = []
    directions = nav(map,coords[0],coords[1])
    if directions[0][1] is not None and map[coords[0]-1][coords[1]] is False:
        moveChoices.append("up")
    if directions[1][1] is not None and map[coords[0]+1][coords[1]] is False:
        moveChoices.append("down")
    if directions[2][1] is not None and map[coords[0]][coords[1]-1] is False:
        moveChoices.append("left")
    if directions[3][1] is not None and map[coords[0]][coords[1]+1] is False:
        moveChoices.append("right")
    
    if len(moveChoices) == 0:
        if Print: print("dead end at",coords)
        return
        
    while len(moveChoices) > 0:
        move = rand.choice(moveChoices)
        moveChoices.remove(move)
        
        if move == "up":
            newCoords = (coords[0]-1,coords[1])
            if map[newCoords[0]][newCoords[1]] == False:
                if Print: print(coords, "going",move) 
                removeWall(maze, row=coords[0], col=coords[1], dir="up",Print=False)
                navigateMaze(maze,map,newCoords)
                if Print: print(coords, "Backtracked down")
        elif move == "down":
            newCoords = (coords[0]+1,coords[1])
            if map[newCoords[0]][newCoords[1]] == False:
                if Print: print(coords, "going",move)
                removeWall(maze, row=coords[0], col=coords[1], dir="down",Print=False)
                navigateMaze(maze,map,newCoords)
                if Print: print(coords, "Backtracked up")
        elif move == "left":
            newCoords = (coords[0],coords[1]-1)
            if map[newCoords[0]][newCoords[1]] == False:
                if Print: print(coords, "going",move)
                removeWall(maze, row=coords[0], col=coords[1], dir="left",Print=False)
                navigateMaze(maze,map,newCoords)
                if Print: print(coords, "Backtracked right")
        elif move == "right":
            newCoords = (coords[0],coords[1]+1)
            if map[newCoords[0]][newCoords[1]] == False:
                if Print: print(coords, "going",move)
                removeWall(maze, row=coords[0], col=coords[1], dir="right",Print=False)
                navigateMaze(maze,map,newCoords)
                if Print: print(coords, "Backtracked left")
    return
      
def generateStartCords(maze):
    numRows = len(maze)
    numCols = len(maze[0])
        
    randRow = rand.randrange(0,numRows)
    randCol = rand.randrange(0,numCols)
    
    startCoords = (randRow,randCol)
    return startCoords
          
newMaze, map = createMaze(numRow = 10, numCol = 10)

startCoords = generateStartCords(newMaze)
print(startCoords)
        
navigateMaze(newMaze,map,startCoords,Print=False)
displayMaze(newMaze)
        

    