import sys
import cv2
import numpy as np
import math
import imutils
COLS=15
ROWS=15
import time

from utils import *
from Astar import *

from threading import Thread


class VideoGet:
    def __init__(self,src=0):
        self.stream=cv2.VideoCapture(src)
        self.grabbed,self.frame= self.stream.read()

        self.stopped=False
    
    def start(self):
        Thread(target=self.get, args=()).start()
        return self
    
    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame)=self.stream.read()
    def stop(self):
        self.stopped= True
        


class VideoShow:
    def __init__(self,frame=None):
        self.frame =frame
        self.stopped =False
        
    def start(self):
        Thread(target=self.show, args=()).start()
        return self
        
    def show(self):
        while not self.stopped:
            cv2.imshow("Video", self.frame)
            if cv2.waitKey(1)==ord("q"):
                self.stopped = True            
    def stop(self):
        self.stopped =True
        
def ShowPath(source):
     
    #video_getter=VideoGet(source).start()
    #video_shower=VideoShow(video_getter.frame).start()
    cap=cv2.VideoCapture(source)
    while True:
        (grabbed,frame)=cap.read()
        if not grabbed or cv2.waitKey(1)==ord("q"):
            break
        output,src,dst,size = gen_transforms(frame)
        #print(img,src,dst,size)
        copy,blocked= detect_objects(output)
        img=gen_path(copy,blocked)
        #frame=gen_final(img,dst,src,size)
        cv2.imshow("Video",img)
 
    cap.release()
    cv2.destroyAllWindows()
        
    
        
        
        
        
        
        
        
        
def gen_transforms(img):
    #img=imutils.rotate(img,270)
    
    img=cv2.resize(img,(640,640))
    size=(img.shape[1],img.shape[0])
               
    output,src,dst= create_transformed_image(img)
    
    return output,src,dst,size

    

def detect_objects(img):
    copy = img.copy()
    ret, thresh = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
    thresh = thresh[:thresh.shape[0]-2, :]                    
                
    block_h = img.shape[1]/15
    block_w = img.shape[0]/15
    blocked = [[1 for i in range(15)] for i in range(15)]
    
        
    for x in range(thresh.shape[1]-1):
        for y in range(thresh.shape[0]-1, -1, -1):
                        # 255 - white
            if thresh[y, x].any() == 0:
                blocked[int(x/block_h)][int(y/block_w)] = 0
    
    for i in range(15):
        for j in range(15):
            if not blocked[i][j]==1:
                color = (0,0,255)
            else:
                color = (0,255,0)
                    
            cv2.rectangle(copy, (int(i*block_h), int(j*block_w)),
                          (int((i+1)*block_h), int((j+1)*block_w)),
                          color, 2)
                    
    return copy,blocked

def gen_path(img,blocked):
    block_h = img.shape[1]/15
    block_w = img.shape[0]/15
    copy=img.copy()
    source = (len(blocked)-1,blocked[len(blocked)-1].index(0))
    dest = (0,blocked[0].index(1))
               
    path = astar(blocked, source, dest) 
                   
    for x,y in path:
        cv2.rectangle(img, (int(y*block_h), int(x*block_w)),
                      (int((y+1)*block_h), int((x+1)*block_w)),
                      (255,0,0), -1)
    return img


def gen_final(img,dst,src,size):
    copy=img.copy()
    p=cv2.getPerspectiveTransform(dst, src)
    t= cv2.warpPerspective(copy, p, size)
    Final=np.zeros(size, dtype=float)
    Final=cv2.addWeighted(img, 0.7, t, 0.3, 0.0)
    return Final
"""
if __name__=="__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--input")
    parser.add_argument("--option")
    args = parser.parse_args()
    
    print(sys.argv)
    if sys.argv[4]=="collision":
           detect_collision(sys.argv[2])
    elif sys.argv[4]=="path":
           create_path(sys.argv[2])
           
"""           

path="Input/video3.mp4"
ShowPath(0)


        
        
    