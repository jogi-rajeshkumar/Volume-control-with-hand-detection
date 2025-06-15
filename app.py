import cv2
import mediapipe as mp
from math import hypot
import numpy as np
import platform
import os
import sys

# OS-specific imports
if platform.system() == "Windows":
    try:
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        WINDOWS = True
    except Exception as e:
        print("Windows audio control libraries not available:", e)
        WINDOWS = False
else:
    WINDOWS = False

LINUX = platform.system() == "Linux"
MAC = platform.system() == "Darwin"

# Setup volume control
if WINDOWS:
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volMin, volMax = volume.GetVolumeRange()[:2]
else:
    volMin, volMax = 0, 100  # using percentage for Linux/Mac


# Linux/macOS volume setter
def set_volume_unix(percent):
    percent = max(0, min(100, int(percent)))
    if LINUX:
        os.system(f"amixer -D pulse sset Master {percent}%")
    elif MAC:
        os.system(f"osascript -e 'set volume output volume {percent}'")


# Start webcam
cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

while True:
    success, img = cap.read()
    if not success:
        break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    lmList = []
    if results.multi_hand_landmarks:
        for handlandmark in results.multi_hand_landmarks:
            for id, lm in enumerate(handlandmark.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
            mpDraw.draw_landmarks(img, handlandmark, mpHands.HAND_CONNECTIONS)

    if lmList:
        x1, y1 = lmList[4][1], lmList[4][2]   # Thumb
        x2, y2 = lmList[8][1], lmList[8][2]   # Index finger

        cv2.circle(img, (x1, y1), 4, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 4, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)

        length = hypot(x2 - x1, y2 - y1)

        vol = np.interp(length, [15, 220], [volMin, volMax])
        volbar = np.interp(length, [15, 220], [400, 150])
        volper = np.interp(length, [15, 220], [0, 100])

        print(f"Volume: {int(volper)}%")

        # Set system volume
        if WINDOWS and volume:
            volume.SetMasterVolumeLevel(vol, None)
        elif LINUX or MAC:
            set_volume_unix(volper)

        # Draw volume bar
        cv2.rectangle(img, (50, 150), (85, 400), (0, 0, 255), 4)
        cv2.rectangle(img, (50, int(volbar)), (85, 400), (0, 0, 255), cv2.FILLED)
        cv2.putText(img, f"{int(volper)}%", (10, 40), cv2.FONT_ITALIC, 1, (0, 255, 98), 3)

    cv2.imshow('Hand Volume Control', img)
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

cap.release()
cv2.destroyAllWindows()
