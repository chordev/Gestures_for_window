# [출처] : https://developeralice.tistory.com/10
import cv2
import mediapipe as mp
import math
import os

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
my_hands = mpHands.Hands(
  max_num_hands=1
)
mpDraw = mp.solutions.drawing_utils

def dist(x1,y1,x2,y2):
    return math.sqrt(math.pow(x1 - x2,2)) + math.sqrt(math.pow(y1 - y2,2))

compareIndex = [[18,4], [6,8], [10,12], [14,16], [18,20]]
_open = [False, False, False, False, False]
gesture = [
    [True,True,False,False,False,'suspend'],
    [False, False, False, False, False, 'lock'],
]

while True:
    success, img = cap.read()
    h, w, c = img.shape
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = my_hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            for i in range(0,5):
                _open[i] = dist(handLms.landmark[0].x, handLms.landmark[0].y,
                                handLms.landmark[compareIndex[i][0]].x, handLms.landmark[compareIndex[i][0]].y) < dist(handLms.landmark[0].x, handLms.landmark[0].y,
                                handLms.landmark[compareIndex[i][1]].x, handLms.landmark[compareIndex[i][1]].y)

            # 손 상태 출력
            print(_open) 
            
            # 현재 손 모양과 저장된 손 모양 비교, 기능 실행
            for i in range(len(gesture)) : 
                if _open == gesture[i][:5] :
                    if gesture[i][5] == 'suspend':
                        os.system('%windir%\\System32\\rundll32.exe powrprof.dll SetSuspendState') # 절전 모드
                    elif gesture[i][5] == 'lock':
                        os.system('rundll32.exe user32.dll,LockWorkStation') # 잠금 화면

    cv2.imshow("HandTracking", cv2.flip(img, 1))
    end = cv2.waitKey(1)
    if end == 27:
      break