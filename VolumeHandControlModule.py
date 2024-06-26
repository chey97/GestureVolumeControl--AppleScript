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


def draw_volume_bar(img, length, minVol, maxVol):
    """Draws the volume bar on the image."""
    volBar = np.interp(length, [minVol, maxVol], [400, 150])
    volPer = np.interp(length, [minVol, maxVol], [0, 100])

    # Draw background bar
    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)

    # Draw filled volume level
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)

    # Display volume percentage
    cv2.putText(
        img, f"{int(volPer)} %", (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3
    )


def main():
    pTime = 0
    # Set camera dimensions
    wCam, hCam = 640, 480

    # Volume control parameters
    minVol, maxVol = 50, 200

    # AppleScript command template for setting volume
    SET_VOLUME_SCRIPT = """
    set volume output volume {volume}
    """

    # Initialize video capture
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    # Initialize hand detector
    detector = htm.handDetector(detectionCon=0.7)

    while True:
        success, img = cap.read()
        if not success:
            break

        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)

        if lmList:
            # Get coordinates of thumb and index finger
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            # Draw circles and line between thumb and index finger
            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
            cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

            # Calculate length between thumb and index finger
            length = math.hypot(x2 - x1, y2 - y1)

            # Map length to volume range
            vol = np.interp(length, [minVol, maxVol], [0, 100])

            # Set system volume based on length
            volume_script = SET_VOLUME_SCRIPT.format(volume=int(vol))
            execute_applescript(volume_script)

            print(f"Length: {length}, Volume: {vol}")

            # Draw volume bar
            draw_volume_bar(img, length, minVol, maxVol)

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
