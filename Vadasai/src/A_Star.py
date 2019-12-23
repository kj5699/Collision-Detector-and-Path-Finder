# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 01:16:40 2019

@author: Jatin
"""
import sys
import cv2
import numpy as np
import math
COLS=15
ROWS=15
flt_max=sys.float_info.max

class cell(object):
    """docstring for cell"""
    def __init__(self,parent,f):

        self.parent=None
        
        self.f=0

def isValid(row,col):
    return (row>=0 and row<ROWS and col>=0 and col<COLS)

def isUnblocked(grid, row, col):
    return grid[row][col]==1

def isDestination(row,col,dest):
    return (row==dest[0] and col== dest[1])


def calculateHvalue(row , col , dest):
    return (math.sqrt((row-dest[0])**2 +(col-dest[1])**2))

def trace_path(cell_details,dest,src):
    row=dest[0]
    col=dest[1]
    Path=[]

    while not (cell_details[row][col].parent_i==row and cell_details[row][col].parent_j==col):
        Path.append((row,col))
        row, col = cell_details[row][col].parent_i, cell_details.parent_j 

    Path.append((row,col))

    Path=Path[::-1]
    return Path

def path_map(src, v):
    height,width ,_= src.shape

    Grid_x=int(width/15)
    Grid_y=int(height/15)

    for y in range(0,height- Grid_y, Grid_y):
        for x in range(0,height- Grid_x, Grid_x):


            for k in range(len(v)):
                a,b=v[k]
                if (int(y/Grid_y)==a  and int(x/Grid_x)==b):
                    cv2.rectangle(src,(x,y),(x+Grid_x,y+Grid_y),(255,0,0),-1)
                    break

    return 


def a_star(source,dest, grid):
    rows,cols=len(grid),len(grid[0])
    
    found=False
    if not isValid(source[0],source[1]):
        print("Source is invalid")
        return 0
    
    if not isValid(dest[0],dest[1]):
        print("Destinationn is invalid")
        return 0

    if not isUnblocked(grid,source[0],source[1]):
        print("Source is blocked")
        return 0        

    if not isUnblocked(grid,dest[0],dest[1]):
        print("Destinationn is blocked")
        return 0
    
    if isDestination(source[0],source[1],dest):
        print("Destination Reached")
        return 1
    
    
    openset=[]
    closedset=[]
    cells=[[cell((-1,-1),flt_max)]*cols]*rows
    path=[]
    
    openset.append(source)
    i,j=source
    cells[i][j].parent=source
    cells[i][j].f=0
    
    while openset:
        current=openset[0]
        openset.remove(current)
        closedset.append(current)
        i,j=current
        for r,c in [(i-1,j),(i+1,j),(i,j+1),(i,j-1),(i-1,j+1),(i-1,j-1),(i+1,j+1),(i+1,j-1)]:
            if isValid(r,c):
                
                if isDestination(r,c, grid):

                    while cells[r][c].parent:
                        path.append((r,c))
                        r,c=cells[r][c].parent
                    found=True    
                    return path
                
                elif (r,c not in closedset and isUnblocked(grid, r,c)):
                    f_temp=1 + calculateHvalue(r,c,dest)
                    if cells[r][c]==flt_max or cells[r][c].f>f_temp:
                        openset.append((r,c))
                        cells[r][c].parent = (i,j)
                        cells[r][c].f=f_temp
                            
    if not found:
        return None
                            
                        
                            
                        
                        
                    
                    
                    
        
    
    
    
    
    
                    
                    
                    
                    
                    
            
            
        
        
        
        


"""def A_star(grid,source,dest,img):
    rows,cols=len(grid),len(grid[0])
    if not isValid(source[0],source[1]):
        print("Source is invalid")
        return 0
    
    if not isValid(dest[0],dest[1]):
        print("Destinationn is invalid")
        return 0

    if not isUnblocked(grid,source[0],source[1]):
        print("Source is blocked")
        return 0        

    if not isUnblocked(grid,dest[0],dest[1]):
        print("Destinationn is blocked")
        return 0
    
    if isDestination(source[0],source[1],dest):
        print("Destination Reached")
        return 1
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    closed_list=[[0]*COLS]*ROWS
    
    cell_details=[[cell()]*COLS]*ROWS
    
    for i in range(ROWS):
        for j in range(COLS):
            cell_details[i][j].f=flt_max
            cell_details[i][j].g=flt_max
            cell_details[i][j].h=flt_max
            cell_details[i][j].parent_i=-1
            cell_details[i][j].parent_j=-1
    
    cell_details=[[cell(-1,-1,flt_max,flt_max)]*cols]*rows

    i,j=source
    cell_details[i][j].f=0
    cell_details[i][j].g=0
    cell_details[i][j].h=0
    cell_details[i][j].parent_i=i
    cell_details[i][j].parent_j=j

    open_list=[(0,(i,j))]
    print("a")
    found_dest =False
            
    
    
    while len(open_list)>0:
        p=open_list[0]
        open_list.remove(p)
        i,j=p[1]
        closed_list[i][j]=True

        g_new=0
        h_new=0
        f_new=0

        for r,c in [(i-1,j),(i+1,j),(i,j+1),(i,j-1),(i-1,j+1),(i-1,j-1),(i+1,j+1),(i+1,j-1)] :
            if isValid(r, c):
                
                if isDestination(r, c, dest):
                    print("abc2")
                    cell_details[r][c].parent_i=i
                    cell_details[r][c].parent_j=j

                    print("The Destination cell is found")
                    
                    map=trace_path(cell_details,dest)
                    path_map(img,map)

                    found_dest =True;
                    return(1)

                elif (not closed_list[r][c] and isUnblocked(grid ,r,c)):
                    
                    g_new=1.0
                    h_new=calculateHvalue(r,c ,dest)
                    f_new= g_new+h_new

                    if cell_details[r][c].f == flt_max or cell_details[r][c].f>f_new :
                        print("abc3")
                        open_list.append((f_new,(r,c)))
                        
                        cell_details[r][c].f=f_new
                        cell_details[r][c].g=g_new
                        cell_details[r][c].h=h_new
                        cell_details[r][c].parent_i=i
                        cell_details[r][c].parent_j=j
                        
            print(cell_details[r][c])               
    if found_dest is False:
        print("Dest Not Found")

    return 0
	"""