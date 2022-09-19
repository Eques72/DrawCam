import cv2

class Painter:
    __brush_sizes = [3,9,15]
    __colors = [(26,26,26,255),(255,255,255,255),(255,22,22,255),(0,128,55,255),(82,113,255,255),(255,222,89,255),(203,108,230,255),(114,55,38,255),(255,145,77,255),(126,217,87,255)]
    __eraser = (0,0,0,0)


    def __init__(self) -> None:
        self.brush_size = Painter.__brush_sizes[1]
        self.last_xy = None 
        self.current_color = Painter.__colors[0]

        self.ERASER_MODE = 0
        self.PAINT_MODE = 1
        self.COLOR_PICKER_ON = 0
        self.SIZE_PICKER_ON = 0
        pass

    def paint(self, xy, image):
        if self.last_xy is None:
            image = cv2.circle(image, xy, self.brush_size, self.current_color, -1)
        else:
            image = cv2.line(image, self.last_xy, xy, self.current_color, self.brush_size) 
        self.last_xy = xy
        return image

    def resetBrush(self) -> None:
        self.last_xy = None
        pass

    def changeColor(self, color_id = 0):
        if color_id < 10 and color_id >= 0:
            self.current_color = Painter.__colors[color_id]
        pass

    def changeSize(self, size_id = 0):
        if size_id < 3 and size_id >= 0:
            self.brush_size = Painter.__brush_sizes[size_id]
        pass 

    def addMonocoloredBackground(color, canvas):
        #TODO ?
        return canvas