import os
import cv2

class FileManager:
    __rootPath = "" #specified if program will be released for instalation as an app
    __resourcesPath = "resources"
    __savedImagesPath = "paintings"
    __savedTextPath = "notes"

    def __init__(self) -> None:
        pass

    def saveAsImg(self, image, isCamBacgroundOn = False, variantPath: str = "", fileName = "NewPainting1.png"):
        if False == os.path.isdir(FileManager.__savedImagesPath):
            self.__createDir("",FileManager.__savedImagesPath)
        
        takenFileNames = os.listdir(FileManager.__savedImagesPath)
        if isCamBacgroundOn == False:
            fileName = "NewPaintingTransp1.png"
        while fileName in takenFileNames:
            if fileName[len(fileName)-5].isdigit():
                index = int(fileName[len(fileName)-5])
                index += 1
                fileName = fileName[:len(fileName)-5] + str(index) + fileName[len(fileName)-4:]
            else:
                fileName = fileName + "1"

        if variantPath == "":
            cv2.imwrite(FileManager.__savedImagesPath + "/" + fileName, image)
        else:
            cv2.imwrite(variantPath + "/" + fileName, image)
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

