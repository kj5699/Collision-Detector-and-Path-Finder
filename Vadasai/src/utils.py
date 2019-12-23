import sys
import cv2
import numpy as np
import math
import imutils
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


def ObjectDetection(im):
    rectangles=[]
    # speed-up using multithreads
    cv2.setUseOptimized(True)
    cv2.setNumThreads(8)

    # resize image
    newHeight = 200
    newWidth = int(im.shape[1]*200/im.shape[0])
    im = cv2.resize(im, (newWidth, newHeight))
    
    ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()
    ss.setBaseImage(im)
    ss.switchToSelectiveSearchFast()
    rects = ss.process()
    print('Total Number of Region Proposals: {}'.format(len(rects)))    # number of region proposals to show
    numShowRects = 100
    copy=im.copy()    # itereate over all the region proposals
    for i, rect in enumerate(rects):
           # draw rectangle for region proposal till numShowRects
        if (i < numShowRects):
            
            x, y, w, h= rect           
            if rect[2]*rect[3]<(0.4*im.shape[0]*im.shape[1]):
               rectangles.append((x, y, x+w, y+h))
               cv2.rectangle(copy,(x,y),(x+w,y+h),(0,0,255),2)         
                        
        else:
            break
        
    cv2.imshow("object",copy)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return rectangles

def create_transformed_image(img):
    src = np.zeros((4, 2), dtype = "float32")
    h , w ,_=img.shape
    
    up = int(0.3 * h)
    centre = int(w)/2
    
    src[0]=(centre-int(0.15*w), up)
    src[1]=(centre+int(0.15*w), up)
    src[2]=(centre+int(0.20*w), h)
    src[3]=(centre-int(0.20*w), h)
    
    (tl, tr, br, bl) = src
    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
 
    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
 
    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")
    
    
    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(img, M, (maxWidth, maxHeight))
    
    # return the warped image
    return warped,src, dst


