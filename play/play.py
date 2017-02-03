import cv2

class DragSelectDisplay(object):
    """
    A class to display an image and allow drag drop selection of regions. 
    """
    def __init__(self,img,window_name = "image"):
        self.selecting = False
        self.start = None
        self.region = None
        self.orig = img
        self.img = self.orig.copy()
        self.window_name = window_name
        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name,self.select)
        cv2.imshow(self.window_name,self.img)
               
    def select_color(self):
        cv2.imshow("ROI",self.region)
        hsv = cv2.cvtColor(self.region, cv2.COLOR_BGR2HSV)
   
        
    def select(self,event, x, y, flags, param):
        """ This function will be called everytime the mouse is moved or clicked over the image """
        if event == cv2.EVENT_LBUTTONDOWN: # start drag
            self.start = (x,y)
            self.selecting = True
         
        elif event == cv2.EVENT_LBUTTONUP: # end drag
            self.img = self.orig.copy()
            cv2.rectangle(self.img,self.start,(x,y),(255,0,0),2)
            a,b,c,d = min(self.start[0],x),max(self.start[0],x),min(self.start[1],y),max(self.start[1],y)
            self.region = self.orig[c:d,a:b]
            self.selecting = False
            self.start = None
            
        else:
            if self.selecting: # currently dragging
                self.img = self.orig.copy()
                cv2.rectangle(self.img,self.start,(x,y),(255,0,0),2)
        
        cv2.imshow(self.window_name,self.img)
                
    
    
img  = cv2.imread("cow1.jpg",cv2.IMREAD_COLOR)
window = DragSelectDisplay(img)
while True:
    val = cv2.waitKey(0) & 0xFF
    if val == ord('q'):
        break
    elif val == ord('h'):
        window.select_color()
        
cv2.destroyAllWindows()
