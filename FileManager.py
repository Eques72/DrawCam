import os
import cv2

class FileManager:
    __rootPath = "" #specified if program will be released for instalation as an app
    __resourcesPath = "resources"
    __savedImagesPath = "paintings"
    __savedTextPath = "notes"

    def __init__(self) -> None:
        pass

    def saveAsImg(self, image, isCamBacgroundOn = False, variantPath: str = "", fileName = "NewPainting1"):
        if False == os.path.isdir(FileManager.__savedImagesPath):
            self.__createDir("",FileManager.__savedImagesPath)
        
        takenFileNames = os.listdir(FileManager.__savedImagesPath)
        if isCamBacgroundOn == False:
            fileName = "NewPaintingTransp1"
        while fileName in takenFileNames:
            if fileName[len(fileName)-1].isdigit():
                index = int(fileName[len(fileName)-1])
                index += 1
                fileName = fileName[:len(fileName)-2] + str(index)
            else:
                fileName = fileName + "1"

        if variantPath == "":
            cv2.imwrite(FileManager.__savedImagesPath + "/" + fileName + ".png", image)
        else:
            cv2.imwrite(variantPath + "/" + fileName + ".png", image)
        pass


    def saveAsText(self, text: str, variantPath: str = ""):
        pass

    def loadResources(self):
        resList = []
        if os.path.isdir( FileManager.__resourcesPath):
            dirFiles = os.listdir(FileManager.__resourcesPath)
            for file in dirFiles:
                resList.append(cv2.imread(f'{FileManager.__resourcesPath}/{file}', flags=cv2.IMREAD_UNCHANGED))
        else:
            #TODO - RETURN ERROR
            pass
        return resList

    def __createDir(self, path = "", dirName = "NewFolder"):
        if path != "":
            os.mkdir(path + "/" + dirName)
        else:
            os.mkdir(dirName)
        pass

