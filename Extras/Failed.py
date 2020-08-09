# -*- coding: utf-8 -*-

###Pehle grid ka function then 

"""
def gridObjectArray(src,Rects):
    matrix=np.ones((11,4))
    height,width,_ = src.shape
    Grid_Size_x=int(width/4)
    Grid_Size_y =int(height /11)
    mcells=[]
    for y in range(0, height- Grid_Size_y,Grid_Size_y):
        for x in range(0, width- Grid_Size_x,Grid_Size_x):
            grid_rect=Rect(x ,y ,Grid_Size_x, Grid_Size_y)

            for k in range(len(Rects)):
                if grid_rect.intersects(Rects[k]):
                    matrix[int(y / Grid_Size_y)][int(x / Grid_Size_x)]=0

                
                    x,y,w,h=grid_rect.coordinates()

                    cv2.rectangle(src,(x,y),(x+w,y+h),(0,0,255),-1)
                else:
                    x,y,w,h=grid_rect.coordinates()
                    
                    cv2.rectangle(src,(x,y),(x+w,y+h),(0,255,0),-1)

                mcells.append(grid_rect)

    return matrix

"""

class Rect(object):
    
    def __init__(self, x, y, w, h):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
    

    def intersects(self, other):
        return not(self.x+self.w < other.x or self.x > other.x +other.w  or self.y < other.y+other.h or self.y+self.h > other.y)

    def coordinates(self):
        return(self.x,self.y,self.h,self.w)
		
		
"""
pts_dst=[]
    pts_src=[]

    pts_dst.append((0,0))
    pts_dst.append((size[0]-1,0))
    pts_dst.append((size[0]-1,size[1]-1))
    pts_dst.append((0,size[1]-1))

    up=int(math.ceil(0.3*img.shape[0]))

    wide=img.shape[1]/2


    pts_src.append((wide-int(0.12*img.shape[1]), up))
    pts_src.append((wide+int(0.12*img.shape[1]), up))
    pts_src.append((wide+int(0.2*img.shape[1]), img.shape[0]))
    pts_src.append((wide-int(0.2*img.shape[1]), img.shape[0]))

    H = cv2.getPerspectiveTransform(np.float32(pts_dst), np.float32(pts_src))
    h, status = cv2.findHomography(np.float32(pts_src),np.float32(pts_dst)) 
"""