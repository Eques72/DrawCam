from typing import Tuple
import cv2
import FileManager

#Class implements logic behind UI 
class ToolsInterface:
    __defaultWidth = 1748
    __defaultHeight = 1240
    __defaultStripHeight = 183
    __defaultIconSpacing = [(8,177),(196,365),(375,544),(555,724),(1105,1304),(1329,1513),(1537,17320), (810,980)]
    __numberOfIcons = 8
    __numberOfSizes = 3
    __numberOfColors = 10
    __numberOfSettings = 3

    __defaultSizeSpacing = [(34,394),(416,776),(800,1160)]
    __defaultSizeBarHeight = 180
    __defaultColorPalletSpacing = [20,110,10] #First param - distance from left border, Second - width of one color option, Third - space between colors in the pallet
    __defaultColorPalletHeight = 124

    __defaultSettingSpacing = [(560,700),(768,1030),(1054,1240) ]
    __defaultSettingsHeight = 180

    __defaultSaveSpacing = []
    __defaultSaveHeight = 0


    def __init__(self) -> None:
        self.interfaceImgIndex = 0
        
        fM = FileManager.FileManager()
        self.resourcesListImg = fM.loadResources()

        for i in range(0, len(self.resourcesListImg)):
            self.resourcesListImg[i] = cv2.cvtColor(self.resourcesListImg[i], cv2.COLOR_BGR2BGRA)
        
        self.width = ToolsInterface.__defaultWidth
        self.height = ToolsInterface.__defaultHeight
        self.stripHeight = ToolsInterface.__defaultStripHeight
        self.iconSpacing = ToolsInterface.__defaultIconSpacing
        self.sizeBarSpacing = ToolsInterface.__defaultSizeSpacing
        self.sizeBarHeight = ToolsInterface.__defaultSizeBarHeight
        self.colorPalletSpacing = ToolsInterface.__defaultColorPalletSpacing
        self.colorPalletHeight = ToolsInterface.__defaultColorPalletHeight
        self.settingsSpacing = ToolsInterface.__defaultSettingSpacing
        self.settingsHeight = ToolsInterface.__defaultSettingsHeight

        self.multi_hands_mode_ON = False
        self.fps_mode_ON = False
        self.lock_fps_mode = False


    def adjustToCamSize(self, width:int, height:int) -> None:
        for i in range(0,len(self.resourcesListImg)): 
            self.resourcesListImg[i] = cv2.resize(self.resourcesListImg[i], (width, height),interpolation = cv2.INTER_AREA)

        h,w,c = self.resourcesListImg[0].shape
        self.width = w
        self.height = h
        hProp = h/ToolsInterface.__defaultHeight
        self.stripHeight = (int)(hProp * self.stripHeight)
        self.sizeBarHeight = (int)(hProp * self.sizeBarHeight)
        self.colorPalletHeight = (int)(hProp * self.colorPalletHeight)
        self.settingsHeight = (int)(hProp * self.settingsHeight)

        for i in range(0,len(self.resourcesListImg)): 
            he,wi,ch = self.resourcesListImg[i].shape
            self.resourcesListImg[i] = self.resourcesListImg[i][0:(int)(he/3), 0:wi]
            self.height = he

        wProp = w/ToolsInterface.__defaultWidth
        for i in range(0,ToolsInterface.__numberOfIcons):
            self.iconSpacing[i] = ((int)(self.iconSpacing[i][0]*wProp),(int)(self.iconSpacing[i][1]*wProp))

        self.colorPalletSpacing[0] = (int)(self.colorPalletSpacing[0]*wProp)
        self.colorPalletSpacing[1] = (int)(self.colorPalletSpacing[1]*wProp)
        self.colorPalletSpacing[2] = (int)(self.colorPalletSpacing[2]*wProp)

        for i in range(0,ToolsInterface.__numberOfSizes):
                self.sizeBarSpacing[i] = ((int)(self.sizeBarSpacing[i][0]*wProp),(int)(self.sizeBarSpacing[i][1]*wProp))

        for i in range(0, len(self.settingsSpacing)):
            self.settingsSpacing[i] = ((int)(self.settingsSpacing[i][0]*wProp),(int)(self.settingsSpacing[i][1]*wProp))


    def setToolsImg(self, is_eraser_active:bool = False, icon_id:int = 0) -> None:
        if icon_id == 0 or (icon_id > 3 and icon_id < 7):
            self.interfaceImgIndex = 0
        elif icon_id == 1 and is_eraser_active == False:
                self.interfaceImgIndex = 1
        elif icon_id == 2:
            if is_eraser_active == True:
                self.interfaceImgIndex = 4
            else:
                self.interfaceImgIndex = 2
        elif icon_id == 3:
                self.interfaceImgIndex = 3
        elif icon_id == 7:
            self.interfaceImgIndex = self.__chooseCurrentSettingsImage()
        pass

    def __chooseCurrentSettingsImage(self)->int:
        if self.multi_hands_mode_ON:
            if self.fps_mode_ON:
                return 8
            else:
                return 7
        if self.multi_hands_mode_ON == False:
            if self.fps_mode_ON:
                return 6
            else:
                return 5

    #coordinates has to be passed as pixel position
    def pickTool(self, x:int, y:int) -> Tuple:
        matching = False
        icon_chosen = 0
        saving = False
        if y <= self.stripHeight:    
            while matching == False and icon_chosen < ToolsInterface.__numberOfIcons:
                if x >= self.iconSpacing[icon_chosen][0] and x < self.iconSpacing[icon_chosen][1]:  
                    matching = True
                    self.lock_fps_mode = False
                else:
                    icon_chosen += 1 
        if 7 > icon_chosen > 3:
            saving = True
        return (matching, icon_chosen, saving)

    def getToolsImg(self) -> cv2.Mat:
        return self.resourcesListImg[self.interfaceImgIndex]

    def getToolsImgFlipped(self) -> cv2.Mat:
        return cv2.flip(self.resourcesListImg[self.interfaceImgIndex],1)

    def getStripSize(self) -> Tuple:
        return (self.width,self.stripHeight)

    def pickColorPallet(self, x:int, y:int, currentColorId:int)->int:
        matching = False
        color_Id_chosen = currentColorId
        iteration = 0
        if y <= self.stripHeight + self.colorPalletHeight and y > self.stripHeight: 
            while matching == False and iteration < self.__numberOfColors:
                if (x > self.colorPalletSpacing[0] + iteration*(self.colorPalletSpacing[1]+self.colorPalletSpacing[2]) and
                x <=  self.colorPalletSpacing[0] + iteration*(self.colorPalletSpacing[1]+self.colorPalletSpacing[2]) + self.colorPalletSpacing[1]):
                    matching = True
                    color_Id_chosen = iteration
                else:
                    iteration += 1 
        return color_Id_chosen

    def pickSizeBar(self ,x:int,y:int, currentSizeId:int)->int:
        matching = False
        size_Id_chosen = currentSizeId
        iteration = 0
        if y <= self.stripHeight + self.sizeBarHeight and y > self.stripHeight: 
            while matching == False and iteration < self.__numberOfSizes:
                if x > self.sizeBarSpacing[iteration][0] and x <=  self.sizeBarSpacing[iteration][1]:
                    matching = True
                    size_Id_chosen = iteration
                else:
                    iteration += 1 
        return size_Id_chosen

    def pickSettings(self, x:int, y:int)->tuple:
        matching = False
        iteration = 0
        if y <= self.stripHeight + self.settingsHeight and y > self.stripHeight: 
            while matching == False and iteration < self.__numberOfSettings:
                if x > self.settingsSpacing[iteration][0] and x <=  self.settingsSpacing[iteration][1]:
                    matching = True
                    if iteration == 0: 
                        self.multi_hands_mode_ON = False                 
                    if iteration == 1:
                        self.multi_hands_mode_ON = True
                    if iteration == 2:
                        if self.fps_mode_ON and self.lock_fps_mode != True:
                            self.fps_mode_ON = False
                            self.lock_fps_mode = True
                        elif self.lock_fps_mode != True:
                            self.fps_mode_ON = True
                            self.lock_fps_mode = True
                else:
                    iteration += 1 
        return (self.multi_hands_mode_ON, self.fps_mode_ON)

    #0- brush,1-color pick , 2-brush pick ,3-eraser ,4-eraser size, 5-8: setting
    def getToolsMode(self)->int:
        return self.interfaceImgIndex

    def pickSave()->bool:
        doSave = False
        return doSave