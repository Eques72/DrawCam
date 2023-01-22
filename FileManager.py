import os
import cv2

# Class handles proper saving of images and access/loading of resources
# Tested on windows only
class FileManager:
    __rootPath = os.path.abspath(os.curdir)
    __resourcesPath = "resources"
    __savedImagesPath = "paintings"
    __savedTextPath = "notes"

    def __init__(self) -> None:
        pass

    #Save image. Use isCamBackgroundOn to display proper default name. Use variantPath to specify save location, Use fileName to name the image file 
    def saveAsImg(self, image:cv2.Mat, isCamBackgroundOn = False, variantPath: str = "", fileName: str = "NewPainting1.png")->None:
        if False == os.path.isdir(FileManager.__savedImagesPath):
            self.__createDir("",FileManager.__savedImagesPath)
        
        takenFileNames = os.listdir(FileManager.__savedImagesPath)
        if isCamBackgroundOn == False:
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

    #TODO
    def saveAsText(self, text: str, variantPath: str = "")->None:
        pass

    #Loads resources necessary for program to work. 
    def loadResources(self)->None:
        resList = []
        if os.path.isdir(FileManager.__resourcesPath):
            dirFiles = os.listdir(FileManager.__resourcesPath)
            for file in dirFiles:
                resList.append(cv2.imread(f'{FileManager.__resourcesPath}/{file}', flags=cv2.IMREAD_UNCHANGED))
        else:
            #TODO - RETURN ERROR
            pass
        return resList

    def __createDir(self, path:str = "", dirName:str = "NewFolder")->None:
        if path != "":
            os.mkdir(path + "/" + dirName)
        else:
            os.mkdir(FileManager.__rootPath + "/" + dirName)
        pass

