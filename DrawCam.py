import cv2
import numpy as np
import time

import ToolsInterface
import Painter 
import Recogniser
import FileManager

def countFPS(t1, t2):
    a = (int) (1/(t1 - t2))
    t2 = t1    
    return a, t2

def setCanvas(parent_img):
    h,w,c = parent_img.shape
    canvas = np.zeros((h, w, 4), dtype=np.uint8)
    return canvas

def addImages(img1, img2):
    rows,cols,channels = img2.shape
    roi = img1[0:rows, 0:cols]

    img2gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
    img2_fg = cv2.bitwise_and(img2,img2,mask = mask)

    dst = cv2.add(img1_bg,img2_fg)
    img1[0:rows, 0:cols ] = dst
    return img1
    
recogniser = Recogniser.Recogniser()
painter = Painter.Painter()
tools = ToolsInterface.ToolsInterface()


cam = cv2.VideoCapture(0)
canvas = setCanvas(cam.read()[1])

time_stamp_start = time.time()
time_stamp_now = 0

tools.adjustToCamSize(cam.read()[1].shape[1],cam.read()[1].shape[0])

if cam.isOpened():
    while(cv2.waitKey(1) != 27):

        isSuccess, frame = cam.read()
        
        #PERFORMANCE DORP!!!!!#
        handsData = recogniser.analyseHands(recogniser.recogniseHandsOnImg(frame))
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        
        for i in range(0, handsData[0]):
            if handsData[2][i] == True and handsData[3][i] == False:
                canvas = painter.paint(recogniser.toPixelCoord(canvas.shape, handsData[1][i]) , canvas)
            else:
                painter.resetBrush()

        frame = addImages(frame, canvas)

        #tools
        for i in range(0, handsData[0]):
            if handsData[4][i] == True and handsData[2][i] == True and handsData[3][i] == True:
                xPx,yPx = recogniser.toPixelCoord(frame.shape, handsData[1][i])
                matchedPick = tools.pickTool(frame.shape[1] - xPx, yPx)
                
                
                if matchedPick[0]:
                #ONLY A DEMO, DOES NOT INCLUDES ALL CONFIGUARTIONS OR OPTIONS
                    tools.setToolsImg(painter.getEraserMode(), matchedPick[1])
                    painter.setMode(matchedPick[1])

                if matchedPick[2]:
                    fM = FileManager.FileManager()
                    
                    if matchedPick[1] == 4: #/w background
                        fM.saveAsImg(frame, True)
                    elif matchedPick[1] == 5: #/w no bckgr
                        fM.saveAsImg(canvas, False)
                    elif matchedPick[1] == 6: #as a text
                    #save img
                        print("SAVING IMAGE IN MODE: ", str(matchedPick[1]))
                    time.sleep(2)

                if painter.getColorMode():
                    colorId = tools.pickColorPallete(frame.shape[1] - xPx, yPx, painter.current_color)
                    painter.changeColor(colorId)
                elif painter.getSizeMode():
                    sizeId = tools.pickSizeBar(frame.shape[1] - xPx, yPx, painter.brush_size)
                    painter.changeSize(sizeId)
                            

        frame = addImages(frame, tools.getToolsImgFlipped()) 

        #hands
        for i in range(0, handsData[0]):
            frame = recogniser.paintMarkers(handsData[5][i], frame)

        frame = cv2.flip(frame, 1)

        # ============================ FPS COUNT =================================
        time_stamp_now = time.time()
        fps, time_stamp_start = countFPS(time_stamp_now, time_stamp_start)
        frame = cv2.putText(frame, str(fps), (0, frame.shape[0]-50), cv2.FONT_HERSHEY_SIMPLEX, 3, 
             (94, 10, 2), 8, cv2.LINE_AA, False)
        # ============================ FPS COUNT ==================================
        
        cv2.imshow("TEXT-CAM", frame)

cam.release()
