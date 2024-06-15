import cv2
import numpy as np
import time
import HandTrackingModule as htm
import math
import subprocess

wCam, hCam = 640, 480


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)

minVol = 50  # Minimum length
maxVol = 200  # Maximum length


# Define AppleScript commands for volume control
VOLUME_UP_SCRIPT = """
set currentVolume to output volume of (get volume settings)
set volume output volume (currentVolume + 10)
"""

VOLUME_DOWN_SCRIPT = """
set currentVolume to output volume of (get volume settings)
set volume output volume (currentVolume - 10)
"""


def execute_applescript(script):
    subprocess.Popen(["osascript", "-e", script])


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # print(lmList[4],lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)

        # Volume range: from minVol to maxVol
        vol = np.interp(length, [minVol, maxVol], [0, 100])

        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
            execute_applescript(VOLUME_DOWN_SCRIPT)
        elif length > 200:
            execute_applescript(VOLUME_UP_SCRIPT)

        print(length, vol)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(
        img,
        f"FPS: {int(fps)}",
        (30, 30),
        cv2.FONT_HERSHEY_COMPLEX,
        0.75,
        (255, 0, 0),
        2,
    )

    cv2.imshow("Video", img)
    cv2.waitKey(1)
