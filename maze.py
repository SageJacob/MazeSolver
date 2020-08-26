import pygame
import random
import time
import math
import numpy as np
from sys import platform
from pygame.locals import *

col, row, prevx, prevy = 11, 11, 0, 0
height, width = 600, 600
screen = pygame.display.set_mode((width, height))
maze_height = 500
pygame.display.set_caption("Make-a-Maze")
# 0 = white, 1 = black, 2 = green
cells = [[0 for i in range(col)] for j in range(row)]
black = (0, 0, 0)
border = (27, 227, 255)
white = (255, 255, 255)
green = (0, 255, 0)
color = white
btndown = False
imgx, imgy = 0, maze_height - (maze_height//col)
ogimgx, ogimgy = imgx, imgy
image = pygame.image.load('Images/Toby.png').convert()
image = pygame.transform.scale(image, (width//row, maze_height//col))
u, d, l, r = 0, 1, 2, 3
path = []
pygame.font.init()
text = pygame.font.SysFont('Times New Roman', 30)
start = text.render('Start', False, (255, 255, 255))
reset = text.render('Reset', False, (255, 255, 255))

# Moves Toby along the given path
def move(imgx, imgy, path, i):
    moveY = int(maze_height // col) + 0.5
    moveX = int(width // row) + 0.6
    if path[i] == u:
        imgy -= moveY
    if path[i] == d:
        imgy += moveY
    if path[i] == l:
        imgx -= moveX
    if path[i] == r:
        imgx += moveX
    return imgx, imgy

# Checks if in-bounds
def isValid(i, j) -> bool:
    if i < 0 or i >= row or j < 0 or j >= col:
        return False
    return True

# Converts 2D array into a graph
def graphify(cells) -> dict:
    graph = {}
    for i in range(len(cells[0])):
        for j in range(len(cells)):
            key = f'({i}, {j})'
            if key not in graph and cells[i][j] == 0:
                graph[key] = []
                if isValid(i+1, j) and cells[i+1][j] == 0:
                    graph[key].append(f'({i+1}, {j})')
                if isValid(i-1, j) and cells[i-1][j] == 0:
                    graph[key].append(f'({i-1}, {j})')
                if isValid(i, j+1) and cells[i][j+1] == 0:
                    graph[key].append(f'({i}, {j+1})')
                if isValid(i, j-1) and cells[i][j-1] == 0:
                    graph[key].append(f'({i}, {j-1})')
    return graph

# Search algorithm (BFS)
def search(graph, start, goal) -> None:
    visited = []
    queue = [[start]]
    while queue:
        path = queue.pop(0)
        node = path[len(path)-1]
        if node not in visited:
            adj = graph[node]
            for cell in adj:
                new_path = list(path)
                new_path.append(cell)
                queue.append(new_path)
                if cell == goal:
                    return new_path
            visited.append(node)

# Find the optimal path from Toby to finish
def findPath(cells) -> list:
    graph = graphify(cells)
    start = f'({0}, {row-1})'
    goal = f'({col-1}, {0})'
    currx, curry = 0, row-1
    route = []
    path = search(graph, start, goal)
    if not path:
        return None
    for i in range(len(path)):
        # If x is single digit
        if path[i][2] == ',':
            x = int(path[i][1])
            if path[i][5] == ')':
                y = int(path[i][4])
            else:
                y = int(path[i][4:6])
        # If x is double digit
        else:
            x = int(path[i][1:3])
            if path[i][6] == ')':
                y = int(path[i][5])
            else:
                y = int(path[i][5:7])
        if y > curry:
            curry += 1
            route.append(d)
        if y < curry:
            curry -= 1
            route.append(u)
        if x > currx:
            currx += 1
            route.append(r)
        if x < currx:
            currx -= 1
            route.append(l)
    return route

while True:
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_q]:
        exit()
    x, y = 0, 0
    for x in range(row):
        for y in range(col):
            if cells[x][y] == 1:
                color = black
            elif cells[x][y] == 0:
                color = white
            else:
                color = green
            if x == row - 1 and y == 0:
                color = green
            # Each cell in maze
            pygame.draw.rect(screen, color, (x * (width / row),
                                             y * (maze_height / col), (x + 1) * (width / row),  maze_height / col))
            pygame.draw.line(screen, border, (x * (width / row),
                                              y * (maze_height / col)), (width, y * maze_height / col))
            pygame.draw.line(screen, border, (x * (width / row), y *
                                              (maze_height / col)), (x * (width / row), maze_height))
    pygame.draw.line(screen, black, (0, maze_height), (width, maze_height))
    # Draw the start button
    pygame.draw.rect(screen, black, (width // 2 - (width // row),
                                     maze_height + ((height - maze_height) // 4), width // row * 2,  50))
    # Reset
    pygame.draw.rect(screen, black, (width // 2 - (width // row) + 200,
                                     maze_height + ((height - maze_height) // 4), width // row * 2,  50))
    screen.blit(start, (width // 2 - (width // row) + 30,
                        maze_height + ((height - maze_height) // 4) + 15))
    screen.blit(reset, (width // 2 - (width // row) + 230,
                        maze_height + ((height - maze_height) // 4) + 15))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if btndown == True:
            x, y = pygame.mouse.get_pos()
            if int(x / (width / row)) != int(prevx / (width / row)) or int(y / (maze_height / col)) != int(prevy / (maze_height / col)):
                rowx = (int)(x / (width / row))
                coly = int(y / (maze_height / col))
                if cells[rowx][coly] == 0:
                    cells[rowx][coly] = 1
                elif cells[rowx][coly] == 1:
                    cells[rowx][coly] = 0
            prevx, prevy = x, y
        if event.type == pygame.MOUSEBUTTONDOWN:
            btndown = True
            x, y = pygame.mouse.get_pos()
            if x < 0 or x > width or y < 0 or y > maze_height:
                btndown = False
            # Start button
            if x > width // 2 - (width // row) and x < width // 2 - (width // row) + width // row * 2 and y < maze_height + ((height - maze_height) // 4) + 50 and y > maze_height + ((height - maze_height) // 4):
                path = findPath(cells)
                if path:
                    cells[0][row-1] = 2
                    for i in range(len(path)):
                        imgx, imgy = move(imgx, imgy, path, i)
                        rowx = (int)(imgx / (width / row))
                        coly = int(imgy / (maze_height / col))
                        cells[rowx][coly] = 2
                        screen.blit(image, (imgx, imgy))
                        if platform == 'win32':
                            time.sleep(0.1)
                            pygame.display.update()
                else:
                    print("Error: No possible path found!")
            # Reset button
            if x > width // 2 - (width // row) + 200 and x < width // 2 - (width // row) + width // row * 2 + 200 and y < maze_height + ((height - maze_height) // 4) + 50 and y > maze_height + ((height - maze_height) // 4):
                imgx, imgy = ogimgx, ogimgy
                screen.blit(image, (imgx, imgy))
                for i in range(col):
                    for j in range(row):
                        if cells[i][j] == 2 or cells[i][j] == 1:
                            cells[i][j] = 0
        if event.type == pygame.MOUSEBUTTONUP:
            btndown = False
    screen.blit(image, (imgx, imgy))
    pygame.display.flip()
    pygame.display.update()
    screen.fill(pygame.Color("#DEDEDE"))
