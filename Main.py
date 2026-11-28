import random as rand
import math
import pygame

pygame.init()
windowWidth = 1600
windowHeight = 1000
window = pygame.display.set_mode((windowWidth,windowHeight))
pygame.display.set_caption("Maze Generator")

def createMaze(numRow, numCol):
    maze = []
    for rows in range(numRow):
        mazeRow = []
        for cols in range(numCol):
            cell = {"up":True,"down":True,"left":True,"right":True}
            mazeRow.append(cell)
        maze.append(mazeRow)
    return maze

def createMap(numRow, numCol):
    map = []
    for rows in range(numRow):
            mapRow = []
            for cols in range(numCol):
                mapRow.append(False)
            map.append(mapRow)
    return map

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
      
def generateStartEndCords(maze):
    numRows = len(maze)
    numCols = len(maze[0])
        
    randRow = rand.randrange(0,numRows)
    randCol = rand.randrange(0,numCols)
    
    startCoords = (randRow,randCol)
    endCoords = startCoords
    
    startEndMinDifference = (numRows + numCols) // 4
    i = 1
    while endCoords == startCoords or startEndMinDifference > (abs(startCoords[0]-endCoords[0])+abs(startCoords[1]-endCoords[1])):
        randRow = rand.randrange(0,numRows)
        randCol = rand.randrange(0,numCols)
        endCoords = (randRow,randCol)
        i += 1
        print(i)
    
    return startCoords,endCoords

# newMaze, map = createMaze(numRow = 10, numCol = 10)

# startCoords = generateStartCords(newMaze)
# #print(startCoords)
        
# navigateMaze(newMaze,map,startCoords,Print=False)
# displayMaze(newMaze)

def generateMaze(mazeSize):
    maze = createMaze(mazeSize[0],mazeSize[1])
    map = createMap(mazeSize[0],mazeSize[1])
    startcords,endCoords = generateStartEndCords(maze)
    navigateMaze(maze,map,startcords,Print=False)
    return maze, startcords,endCoords

def drawCellWall(coords, cellWidth, direction,exists,wallWidth):
        if direction == "up" and exists:
            pygame.draw.line(window, (0, 0, 0), (coords[0], coords[1]), (coords[0]+cellWidth, coords[1]), wallWidth)
        if direction == "down" and exists:
            pygame.draw.line(window, (0, 0, 0), (coords[0], coords[1]+cellWidth), (coords[0]+cellWidth, coords[1]+cellWidth), wallWidth)
        if direction == "left" and exists:
            pygame.draw.line(window, (0, 0, 0), (coords[0], coords[1]), (coords[0], coords[1]+cellWidth), 2)
        if direction == "right" and exists:
            pygame.draw.line(window, (0, 0, 0), (coords[0]+cellWidth, coords[1]), (coords[0]+cellWidth, coords[1]+cellWidth), wallWidth)
    
def drawMaze(maze, cellWidth,wallWidth,xOffset,yOffset):
    pygame.draw.rect(window, (0, 255, 0), (((startCoords[1]*cellWidth)+int(xOffset)),((startCoords[0]*cellWidth)+int(yOffset)),cellWidth,cellWidth))
    
    pygame.draw.rect(window, (255, 0, 0), (((endCoords[1]*cellWidth)+int(xOffset)),((endCoords[0]*cellWidth)+int(yOffset)),cellWidth,cellWidth))
    
    for rowIndex, row in enumerate(maze):    
        for cellIndex, cell in enumerate(row):    
            for direction, exists in cell.items():
                coords = [(cellIndex*cellWidth)+xOffset,(rowIndex*cellWidth)+yOffset]
                drawCellWall(coords,cellWidth,direction,exists,wallWidth)
        
def solveMaze(maze, map, coords, endCoords,Print = False):
    
    map[coords[0]][coords[1]] = True
    
    if coords == endCoords:
        solution = [coords]
        return solution
            
    moveChoices = []
    directions = nav(map,coords[0],coords[1])
    if directions[0][1] is not None and map[coords[0]-1][coords[1]] is False and not maze[coords[0]][coords[1]]["up"]:
        moveChoices.append("up")
    if directions[1][1] is not None and map[coords[0]+1][coords[1]] is False and not maze[coords[0]][coords[1]]["down"]:
        moveChoices.append("down")
    if directions[2][1] is not None and map[coords[0]][coords[1]-1] is False and not maze[coords[0]][coords[1]]["left"]:
        moveChoices.append("left")
    if directions[3][1] is not None and map[coords[0]][coords[1]+1] is False and not maze[coords[0]][coords[1]]["right"]:
        moveChoices.append("right")
    
    if len(moveChoices) == 0:
        if Print: print("dead end at",coords)
        return None
    while len(moveChoices) > 0:
        move = rand.choice(moveChoices)
        moveChoices.remove(move)
        
        if move == "up":
            newCoords = (coords[0]-1,coords[1])
            if map[newCoords[0]][newCoords[1]] == False:
                if Print: print(coords, "going",move) 
                solution = solveMaze(maze, map, newCoords, endCoords,Print)
                if Print: print(coords, "Backtracked down")
                if solution is not None: 
                    solution.insert(0,coords)
                    return solution
                
        elif move == "down":
            newCoords = (coords[0]+1,coords[1])
            if map[newCoords[0]][newCoords[1]] == False:
                if Print: print(coords, "going",move)
                solution = solveMaze(maze, map, newCoords, endCoords,Print)
                if Print: print(coords, "Backtracked up")
                if solution is not None: 
                    solution.insert(0,coords)
                    return solution
                
        elif move == "left":
            newCoords = (coords[0],coords[1]-1)
            if map[newCoords[0]][newCoords[1]] == False:
                if Print: print(coords, "going",move)
                solution = solveMaze(maze, map, newCoords, endCoords,Print)
                if Print: print(coords, "Backtracked right")
                if solution is not None: 
                    solution.insert(0,coords)
                    return solution
                
        elif move == "right":
            newCoords = (coords[0],coords[1]+1)
            if map[newCoords[0]][newCoords[1]] == False:
                if Print: print(coords, "going",move)
                solution = solveMaze(maze, map, newCoords, endCoords,Print)
                if Print: print(coords, "Backtracked left")
                if solution is not None: 
                    solution.insert(0,coords)
                    return solution
    return None
        
def drawSolution(maze,map,solution,cellWidth,wallWidth,xOffset,yOffset):
    for i in range(1,len(solution)):
        pygame.draw.line(window,
                         (200,50,200),
                         (((solution[i-1][1] * cellWidth) + int(xOffset) + cellWidth//2), ((solution[i-1][0] * cellWidth) + int(yOffset)) + cellWidth//2),
                         (((solution[i][1] * cellWidth) + int(xOffset) + cellWidth//2), ((solution[i][0] * cellWidth) + int(yOffset)) + cellWidth//2),
                         5
                        )

    

running = True

window.fill((255, 255, 255))
pygame.display.flip()

while running:
     
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                
                window.fill((255, 255, 255))
                
                mazeSize = [20,20]
                maze, startCoords, endCoords = generateMaze(mazeSize)
                
                
                map = createMap(len(maze),len(maze[0]))
                solution = solveMaze(maze,map,startCoords,endCoords,Print = False)
                print(solution)
                
                cellWidth=50
                wallWidth=2
                
                mazeWidth = len(maze[0]) * cellWidth
                mazeHeight = len(maze) * cellWidth
                xOffset = (windowWidth - mazeWidth) / 2
                yOffset = (windowHeight - mazeHeight) / 2
                
                drawMaze(maze,cellWidth,wallWidth,int(xOffset),int(yOffset))
                drawSolution(maze,map,solution,cellWidth,wallWidth,int(xOffset),int(yOffset))
                
                
                
                pygame.display.flip()
                
            if event.key == pygame.K_q:
                running = False
                                
       
                
                
                
        if event.type == pygame.QUIT:
            running = False
            
pygame.quit()
    