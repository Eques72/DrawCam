from xmlrpc.client import Boolean
import mediapipe as mp
import cv2
import math

class Recogniser:

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
        

        self.hands = self.mp_hands.Hands( static_image_mode=False, model_complexity=Recogniser.__model_complexity,
            min_detection_confidence=Recogniser.__min_detection_confidence,
            min_tracking_confidence=Recogniser.__min_tracking_confidence, 
            max_num_hands=Recogniser.__max_num_hands)
        pass

    def recogniseHandsOnImg(self, image):

        # with self.mp_hands.Hands(model_complexity=Recogniser.__model_complexity,
        #     min_detection_confidence=Recogniser.__min_detection_confidence,
        #     min_tracking_confidence=Recogniser.__min_tracking_confidence, 
        #     max_num_hands=Recogniser.__max_num_hands) as Hands:
        # with self.hands as Hands:
                image = self.__prepareImg(image)
                resoultsFromImg = self.hands.process(image=image)
                # resoultsFromImg = Hands.process(image=image)
                return resoultsFromImg

    def __makeDicList(self, res):
        #hl.landmark is [(x,y,z)(x,y,z)...]        
        listOfDictionaries = []
        if res.multi_hand_landmarks:
            for hl in res.multi_hand_landmarks:
                enumeratedLandmarks = {}
                for id, lm in enumerate(hl.landmark):
                    enumeratedLandmarks[id] = lm
                listOfDictionaries.append(enumeratedLandmarks) 
        return listOfDictionaries

    def analyseHands(self, resoults):
        """which one is up, are some connected, give their coordinates"""
        multiEnumHandmarks = self.__makeDicList(resoults)

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
                indexFingerXY.append(eL[Recogniser.__IndexFingerIds[0]])
                if self.__chceckIfFingersConnected(eL[Recogniser.__IndexFingerIds[0]], eL[Recogniser.__IndexFingerIds[1]], eL[Recogniser.__MiddleFingerIds[0]], eL[Recogniser.__MiddleFingerIds[1]]):    
                    areIndNMidFingersConnected.append(True)
                else:
                    areIndNMidFingersConnected.append(False)
                if self.__checkIfFingerIsUp(eL[Recogniser.__IndexFingerIds[0]], eL[Recogniser.__IndexFingerIds[2]], eL[Recogniser.__IndexFingerIds[3]]):
                    isIndexUp.append(True)
                else:
                    isIndexUp.append(False)                
                if self.__checkIfFingerIsUp(eL[Recogniser.__MiddleFingerIds[0]], eL[Recogniser.__MiddleFingerIds[2]], eL[Recogniser.__MiddleFingerIds[3]]):
                    isMiddleUp.append(True)
                else:
                    isMiddleUp.append(False)
        
        #zwrócić programowi: pozycje wybranych (tylko index górny), czy są podniesione 1 czy dwa i czy się łączą, liczbe rąk    
        return (num_of_hands, indexFingerXY, isIndexUp, isMiddleUp, areIndNMidFingersConnected, multiEnumHandmarks)

    def __prepareImg(self, img):
        img.flags.writeable = False
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img

    def paintMarkers(self, enLmList, img):
        for i in range(0, len(enLmList)):
            if i in Recogniser.__visibleLandmarksIds:
                if i in Recogniser.__topMarkersIds:
                    img = cv2.circle(img, self.toPixelCoord(img.shape, enLmList[i]), Recogniser.__topMarkerSize, Recogniser.__topMarkerColor, -1) 
                else:
                    img = cv2.circle(img, self.toPixelCoord(img.shape, enLmList[i]), Recogniser.__markerSize, Recogniser.__markerColor, -1) 
        # for id, lm in enLmList:
        #     if lm in Recogniser.__visibleLandmarksIds:
        #         if id in Recogniser.__topMarkersIds:
        #             img = cv2.circle(img, self.toPixelCoord(lm), Recogniser.__topMarkerSize, Recogniser.__topMarkerColor, -1) 
        #         else:
        #             img = cv2.circle(img, self.toPixelCoord(lm), Recogniser.__markerSize, Recogniser.__markerColor, -1) 
        return img

    def __chceckIfFingersConnected(self, landmarkTop1, landmarkMid1, landmarkTop2, landmarkMid2):
        distFingers = self.__landmarkDistCalculate(landmarkTop1, landmarkTop2)
        if distFingers < self.__landmarkDistCalculate(landmarkTop1, landmarkMid1) or distFingers < self.__landmarkDistCalculate(landmarkTop2, landmarkMid2):
            return True
        else:
            return False

    def __checkIfFingerIsUp(self, landmarkTop, landmarkMid,  landmarkBottom = -1):
        if landmarkTop.y < landmarkMid.y and landmarkTop.y < landmarkBottom.y:
            return True
        else:
            return False 

    def __landmarkDistCalculate(self, lm1, lm2):
        # distance = ((lm1.x-lm2.x)**(2)+(lm1.y-lm2.y)**(2))**(0.5) 
        distance = math.sqrt(math.pow(lm1.x-lm2.x,2)+math.pow(lm1.y-lm2.y,2))
        return distance
        
    def toPixelCoord(self, imgShape, lm):
        y_pos=(int)(lm.y*imgShape[0])
        x_pos=(int)(imgShape[1]*lm.x)
        return x_pos,y_pos
