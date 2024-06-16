import cv2
import numpy as np
import time
import HandTrackingModule as htm
import math
import subprocess


def execute_applescript(script):
    """Executes the given AppleScript command."""
    try:
        subprocess.Popen(["osascript", "-e", script])
    except Exception as e:
        print(f"Error executing AppleScript: {e}")


def is_palm_open(lmList):
    """Checks if the palm is open based on landmark positions."""
    # Indices for the tips of each finger
    tips = [4, 8, 12, 16, 20]
    # Check if the tips of all fingers are above the corresponding bottom parts
    return all(lmList[tip][2] < lmList[tip - 2][2] for tip in tips[1:])


def main():

    # Set camera dimensions
    wCam, hCam = 640, 480

    # Volume control parameters
    minVol, maxVol = 50, 200

    # AppleScript command for play/pause
    PLAY_PAUSE_SCRIPT = """
    tell application "System Events" to keystroke space
    """

    # Initialize video capture
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    # Initialize hand detector
    detector = htm.handDetector(detectionCon=0.7)

    pTime = 0
    play_state = False

    while True:
        success, img = cap.read()
        if not success:
            break

        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)

        if lmList:
            if is_palm_open(lmList):
                if not play_state:
                    execute_applescript(PLAY_PAUSE_SCRIPT)
                    play_state = True
                    print("Play")
            else:
                if play_state:
                    execute_applescript(PLAY_PAUSE_SCRIPT)
                    play_state = False
                    print("Pause")

        # Calculate and display FPS
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

        # Display the video feed
        cv2.imshow("Video", img)

        # Check for ESC key press to exit
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # Release the capture when everything is done
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
