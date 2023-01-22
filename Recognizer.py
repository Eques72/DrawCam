import mediapipe as mp #Newest, state at 1.23
import cv2
import math

#Class handles the trained model and uses it to recognize hands from images and use that data
class Recognizer:

    __model_complexity=1
    __min_detection_confidence=0.8
    __min_tracking_confidence=0.5
    __max_num_hands=2

    __topMarkerSize = 15
    __markerSize = 10
    __topMarkerColor = (4, 60, 84)
    __markerColor = (76, 165, 207)

    __topMarkersIds = [4, 8, 12, 16, 20]
    __IndexFingerIds = [8,7,6,5]
    __MiddleFingerIds = [12,11,10,9]

    __visibleLandmarksIds = [5,8,9,12,17]
 

    def __init__(self) -> None:
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands
        self.num_of_hands = 1

        self.hands = self.mp_hands.Hands( static_image_mode=False, model_complexity=Recognizer.__model_complexity,
            min_detection_confidence=Recognizer.__min_detection_confidence,
            min_tracking_confidence=Recognizer.__min_tracking_confidence, 
            max_num_hands=self.num_of_hands)
        pass

    def recognizeHandsOnImg(self, image:cv2.Mat):
        image = self.__prepareImg(image)
        resultsFromImg = self.hands.process(image=image)
        return resultsFromImg

    def __makeDicList(self, result)->list:
        #hl.landmark is [(x,y,z)(x,y,z)...]        
        listOfDictionaries = []
        if result.multi_hand_landmarks:
            for hl in result.multi_hand_landmarks:
                enumeratedLandmarks = {}
                for id, lm in enumerate(hl.landmark):
                    enumeratedLandmarks[id] = lm
                listOfDictionaries.append(enumeratedLandmarks) 
        return listOfDictionaries

    #which one is up, are some connected, give their coordinates
    def analyzeHands(self, result)->tuple:
        multiEnumHandmarks = self.__makeDicList(result)

        if not multiEnumHandmarks: 
            num_of_hands = 0
        else:
            num_of_hands = len(multiEnumHandmarks)
        
        indexFingerXY = []
        areIndNMidFingersConnected = []
        isIndexUp = []
        isMiddleUp = []

        if num_of_hands != 0:
            for eL in multiEnumHandmarks:             
                indexFingerXY.append(eL[Recognizer.__IndexFingerIds[0]])
                if self.__checkIfFingersConnected(eL[Recognizer.__IndexFingerIds[0]], eL[Recognizer.__IndexFingerIds[1]], eL[Recognizer.__MiddleFingerIds[0]], eL[Recognizer.__MiddleFingerIds[1]]):    
                    areIndNMidFingersConnected.append(True)
                else:
                    areIndNMidFingersConnected.append(False)
                if self.__checkIfFingerIsUp(eL[Recognizer.__IndexFingerIds[0]], eL[Recognizer.__IndexFingerIds[2]], eL[Recognizer.__IndexFingerIds[3]]):
                    isIndexUp.append(True)
                else:
                    isIndexUp.append(False)                
                if self.__checkIfFingerIsUp(eL[Recognizer.__MiddleFingerIds[0]], eL[Recognizer.__MiddleFingerIds[2]], eL[Recognizer.__MiddleFingerIds[3]]):
                    isMiddleUp.append(True)
                else:
                    isMiddleUp.append(False)
        
        return (num_of_hands, indexFingerXY, isIndexUp, isMiddleUp, areIndNMidFingersConnected, multiEnumHandmarks)

    def __prepareImg(self, img:cv2.Mat)->cv2.Mat:
        img.flags.writeable = False
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img

    def paintMarkers(self, enLmList:list, img:cv2.mat, fingerTipColor:tuple, fingerTipSize:int)->cv2.Mat:
        colorTip = Recognizer.__topMarkerColor
        sizeTip = Recognizer.__topMarkerSize
        if fingerTipColor is not None:
            colorTip = fingerTipColor
        if fingerTipSize is not None:
            sizeTip = fingerTipSize    
        for i in range(0, len(enLmList)):
            if i in Recognizer.__visibleLandmarksIds:
                if i in Recognizer.__topMarkersIds:
                    img = cv2.circle(img, self.toPixelCoord(img.shape, enLmList[i]), sizeTip, colorTip, -1) 
                else:
                    img = cv2.circle(img, self.toPixelCoord(img.shape, enLmList[i]), Recognizer.__markerSize, Recognizer.__markerColor, -1) 
        return img

    def __checkIfFingersConnected(self, landmarkTop1:tuple, landmarkMid1:tuple, landmarkTop2:tuple, landmarkMid2:tuple)->bool:
        distFingers = self.__landmarkDistCalculate(landmarkTop1, landmarkTop2)
        if distFingers < self.__landmarkDistCalculate(landmarkTop1, landmarkMid1) or distFingers < self.__landmarkDistCalculate(landmarkTop2, landmarkMid2):
            return True
        else:
            return False

    def __checkIfFingerIsUp(self, landmarkTop:tuple, landmarkMid:tuple,  landmarkBottom:tuple = -1)->bool:
        if landmarkTop.y < landmarkMid.y and landmarkTop.y < landmarkBottom.y:
            return True
        else:
            return False 

    def __landmarkDistCalculate(self, lm1:tuple, lm2:tuple)->float:
        distance = math.sqrt(math.pow(lm1.x-lm2.x,2)+math.pow(lm1.y-lm2.y,2))
        return distance
        
    def toPixelCoord(self, imgShape:list, lm:tuple)->tuple:
        y_pos=(int)(lm.y*imgShape[0])
        x_pos=(int)(imgShape[1]*lm.x)
        return x_pos,y_pos

    def changeModel(self, new_number_of_hands:int = 1)->None:
        if new_number_of_hands != self.num_of_hands:
            self.num_of_hands = new_number_of_hands
            self.hands = self.mp_hands.Hands( static_image_mode=False, model_complexity=Recognizer.__model_complexity,
                min_detection_confidence=Recognizer.__min_detection_confidence,
                min_tracking_confidence=Recognizer.__min_tracking_confidence, 
                max_num_hands=new_number_of_hands)
        pass