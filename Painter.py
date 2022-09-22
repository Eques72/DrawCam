import cv2

class Painter:
    __brush_sizes = [3,9,15]
    __colors = [(26,26,26,255),(255,255,255,255),(22,22,255,255),(55,128,0,255),(255,113,82,255),
    (89,222,225,255),(230,108,203,255),(38,55,114,255),(77,145,255,255),(87,217,126,255),(0,0,0,0)] #BGR
    __eraserId = 10

    def __init__(self) -> None:
        self.brush_size = Painter.__brush_sizes[1]
        self.last_xy = None 
        self.current_color = 0
        self.lastUsedColor = 0

        self.__ERASER_MODE = False
        self.__PAINT_MODE = True
        self.__COLOR_PICKER_ON = False
        self.__SIZE_PICKER_ON = False
        pass

    def paint(self, xy, image):
        if self.last_xy is None:
            image = cv2.circle(image, xy, self.brush_size, Painter.__colors[self.current_color], -1)
        else:
            image = cv2.line(image, self.last_xy, xy, Painter.__colors[self.current_color], self.brush_size) 
        self.last_xy = xy
        return image

    def resetBrush(self) -> None:
        self.last_xy = None
        pass

    def changeColor(self, color_id = 0):
        self.lastUsedColor = self.current_color
        if color_id < 10 and color_id >= 0:
            self.current_color = color_id
        pass

    def changeSize(self, size_id = 0):
        if size_id < 3 and size_id >= 0:
            self.brush_size = Painter.__brush_sizes[size_id]
        pass 

    def addMonocoloredBackground(color, canvas):
        #TODO ?
        return canvas

    def setMode(self, mode: int):
        if mode == 0:
            self.current_color = self.lastUsedColor
            self.__ERASER_MODE = False
            self.__PAINT_MODE = True
            self.__COLOR_PICKER_ON = False
            self.__SIZE_PICKER_ON = False
        elif mode == 1 and self.__PAINT_MODE == True:
            self.__ERASER_MODE = False
            self.__PAINT_MODE = True
            self.__COLOR_PICKER_ON = True
            self.__SIZE_PICKER_ON = False            
        elif mode == 2 and self.__PAINT_MODE == True:
            self.__ERASER_MODE = False
            self.__PAINT_MODE = True
            self.__COLOR_PICKER_ON = False
            self.__SIZE_PICKER_ON = True            
        elif mode == 2 and self.__ERASER_MODE == True:
            self.__ERASER_MODE = True
            self.__PAINT_MODE = False
            self.__COLOR_PICKER_ON = False
            self.__SIZE_PICKER_ON = True                   
        elif mode == 3:
            if self.current_color != Painter.__eraserId:
                self.lastUsedColor = self.current_color
            self.current_color = Painter.__eraserId
            self.__ERASER_MODE = True
            self.__PAINT_MODE = False
            self.__COLOR_PICKER_ON = False
            self.__SIZE_PICKER_ON = False        
        pass

    def getEraserMode(self):
        return self.__ERASER_MODE

    def getPainterMode(self):
        return self.__PAINT_MODE

    def getColorMode(self):
        return self.__COLOR_PICKER_ON

    def getSizeMode(self):
        return self.__SIZE_PICKER_ON

    def getCurrentColor(self):
        return Painter.__colors[self.current_color]
    
    def getCurrentSize(self):
        return self.brush_size

    def getCurrentColorId(self):
        return self.current_color