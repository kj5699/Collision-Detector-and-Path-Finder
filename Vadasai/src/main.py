import sys
import cv2
import numpy as np
import math
import imutils
COLS=15
ROWS=15

from utils import *
from Astar import *

def create_path(path):
    cap=cv2.VideoCapture(path)
    if (cap.isOpened()== False): 
        print("Error opening video stream or file")
    #out = cv2.VideoWriter('Output/output.avi', -1, 20.0, (640,480))
    while(cap.isOpened()):
  # Capture frame-by-frame
        ret, img = cap.read()
        
        if ret:
               img=imutils.rotate(img,270)
               img=cv2.resize(img,(640,640))
               size2=(img.shape[1],img.shape[0])
               
               output_image,src,dst= create_transformed_image(img)
               copy = output_image.copy()
               ret, thresh = cv2.threshold(output_image,127,255,cv2.THRESH_BINARY)
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

               source = (len(blocked)-1,blocked[len(blocked)-1].index(1))
               dest = (0,blocked[0].index(1))
               
               path = astar(blocked, source, dest) 
                   
               for x,y in path:
                   cv2.rectangle(copy, (int(y*block_h), int(x*block_w)),
                                  (int((y+1)*block_h), int((x+1)*block_w)),
                                  (255,0,0), -1)
               
               cv2.namedWindow("copy",cv2.WINDOW_NORMAL)
               cv2.imshow("copy",copy)
               p=cv2.getPerspectiveTransform(dst, src)
               t= cv2.warpPerspective(copy, p, size2)
               Final=np.zeros(size2, dtype=float)
               Final=cv2.addWeighted(img, 0.7, t, 0.3, 0.0)
               #out.write(Final)
               
               cv2.namedWindow("Suggest path",cv2.WINDOW_NORMAL)
               cv2.imshow("Suggest path", Final)
               if cv2.waitKey(25) & 0xFF == ord('q'):
                       break
                   
    cap.release()
    #out.release()
    cv2.destroyAllWindows()



def detect_collision(path):
    cap=cv2.VideoCapture(path)
    if (cap.isOpened()== False): 
        print("Error opening video stream or file")
    #out = cv2.VideoWriter('Output/output.avi', -1, 20.0, (640,480))
    while(cap.isOpened()):
  # Capture frame-by-frame
        ret, img = cap.read()
        
        if ret:
               img=imutils.rotate(img,270)
               img=cv2.resize(img,(640,640))
               size2=(img.shape[1],img.shape[0])
               
               output_image,src,dst= create_transformed_image(img)
               copy = output_image.copy()
               ret, thresh = cv2.threshold(output_image,127,255,cv2.THRESH_BINARY)
               thresh = thresh[:thresh.shape[0]-2, :]
                           
                
               block_h = img.shape[1]/ROWS
               block_w = img.shape[0]/COLS
        
               blocked = [[1 for i in range(COLS)] for i in range(ROWS)]
    
        
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



                        
               cv2.namedWindow("copy",cv2.WINDOW_NORMAL)
               cv2.imshow("Transformed",copy)
               
               
               p=cv2.getPerspectiveTransform(dst, src)
               t= cv2.warpPerspective(copy, p, size2)
               Final=np.zeros(size2, dtype=float)
               Final=cv2.addWeighted(img, 0.7, t, 0.3, 0.0)
               
               #out.write(Final)
               cv2.namedWindow("Detect Collision",cv2.WINDOW_NORMAL)
               cv2.imshow("Detect collision", Final)
               if cv2.waitKey(25) & 0xFF == ord('q'):
                       break
                   
    cap.release()
    #out.release()
    cv2.destroyAllWindows()
    



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
        
        
    