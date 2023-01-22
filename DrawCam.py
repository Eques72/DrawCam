import cv2
import numpy as np
import time

import ToolsInterface
import Painter 
import Recognizer
import FileManager

#Main class behind program logic
#Initializes camera 
class DrawCam:

    def __init__(self) -> None:
        self.camera = cv2.VideoCapture(0)
        self.canvas = self.__setCanvas(self.camera.read()[1])

        self.recognizer = Recognizer.Recognizer()
        self.painter = Painter.Painter()
        self.tools = ToolsInterface.ToolsInterface()

        self.tools.adjustToCamSize(self.camera.read()[1].shape[1],self.camera.read()[1].shape[0])

        self.is_fps_counter_on = False
        self.fpsC = FPScounter()
        pass

    def __setCanvas(self, parentImg:cv2.Mat)->cv2.Mat:
        h,w,c = parentImg.shape
        canvas = np.zeros((h, w, 4), dtype=np.uint8)
        return canvas

    def __superimposeImages(self, img1: cv2.Mat, img2: cv2.Mat) -> cv2.Mat:
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

    def __doPaintingOnCanvas(self, cursorData:tuple)->None:
        for i in range(0, cursorData[0]):
            if cursorData[2][i] == True and cursorData[3][i] == False:
                self.canvas = self.painter.paint(self.recognizer.toPixelCoord(self.canvas.shape, cursorData[1][i]) , self.canvas)
            else:
                self.painter.resetBrush()   
        pass  

    def __wrapSaveProcedure(self, saveMode:int, frame:cv2.Mat, canvas:cv2.Mat)->None:
        fM = FileManager.FileManager()
                                    
        if saveMode == 4: #/w background
            fM.saveAsImg(frame, True)
        elif saveMode == 5: #/w no bckgr
            fM.saveAsImg(canvas, False)
        elif saveMode == 6: #as a text
            #TODO save img
            print("SAVING IMAGE IN MODE: ", str(saveMode))
        time.sleep(2)      
        pass  

    def __handlePaletteSelections(self, X:int,Y:int, frame:cv2.Mat)->None:
        if self.painter.getColorMode():
            colorId = self.tools.pickColorPallet(frame.shape[1] - X, Y, self.painter.getCurrentColorId())
            self.painter.changeColor(colorId)
        elif self.painter.getSizeMode():
            sizeId = self.tools.pickSizeBar(frame.shape[1] - X, Y, self.painter.brush_size)
            self.painter.changeSize(sizeId)
        pass

    def __doFingerSelection(self, handsData:tuple, frame:cv2.Mat)->None:
        for i in range(0, handsData[0]):
            if handsData[4][i] == True and handsData[2][i] == True and handsData[3][i] == True:
                xPx,yPx = self.recognizer.toPixelCoord(frame.shape, handsData[1][i])
                matchedPick = self.tools.pickTool(frame.shape[1] - xPx, yPx)
                
                if matchedPick[0]:                              
                    self.tools.setToolsImg(self.painter.getEraserMode(), matchedPick[1])
                    self.painter.setMode(matchedPick[1])
                    if matchedPick[2]:
                        self.__wrapSaveProcedure(matchedPick[1], frame, self.canvas)

                if self.tools.getToolsMode() >= 5:
                    settings = self.tools.pickSettings(frame.shape[1] - xPx, yPx)
                    if settings[0]:
                        self.recognizer.changeModel(2)
                    else:
                        self.recognizer.changeModel(1)
                    self.is_fps_counter_on = settings[1]
                    self.tools.setToolsImg(self.painter.getEraserMode(), 7)                                                    

                self.__handlePaletteSelections(xPx, yPx, frame)
        pass

    def cameraLoop(self)->None:
        if self.camera.isOpened():
            while(cv2.waitKey(1) != 27):

                isSuccess, frame = self.camera.read()            
                handsData = self.recognizer.analyzeHands(self.recognizer.recognizeHandsOnImg(frame))

                self.__doPaintingOnCanvas(handsData)
                 
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
                frame = self.__superimposeImages(frame, self.canvas)

                self.__doFingerSelection(handsData=handsData, frame=frame)                
                                    
                frame = self.__superimposeImages(frame, self.tools.getToolsImgFlipped()) 

                for i in range(0, handsData[0]):
                    frame = self.recognizer.paintMarkers(handsData[5][i], frame, self.painter.getCurrentColor(), self.painter.getCurrentSize())

                frame = cv2.flip(frame, 1)
                
                if self.is_fps_counter_on:
                    frame = self.fpsC.displayFPS(frame)

                cv2.imshow("DRAW-CAM", frame)
        self.camera.release()
        pass    

#Class used for measuring of time performance
class FPScounter:
    def __init__(self) -> None:
        self.time_stamp_start = time.time()
        self.time_stamp_now = time.time()
        pass
    
    def __getFPS(self)->int:
        self.time_stamp_now = time.time()
        fps, self.time_stamp_start = self.__countFPS(self.time_stamp_now, self.time_stamp_start)
        return fps

    def displayFPS(self, image:cv2.Mat)->cv2.Mat:
        fpsNum = self.__getFPS()
        image = cv2.putText(image, str(fpsNum), (0, image.shape[0]-50), cv2.FONT_HERSHEY_SIMPLEX, 3, 
             (94, 10, 2), 8, cv2.LINE_AA, False)
        return image

    def __countFPS(self, t1, t2)->tuple:
        a = (int) (1/(t1 - t2))
        t2 = t1    
        return a, t2


###################################################################

dC = DrawCam()
dC.cameraLoop()
