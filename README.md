# Hand Gesture Volume Control

This Python script allows you to control the system volume using hand gestures detected via a webcam. By measuring the distance between your thumb and index finger, you can adjust the volume level on your macOS.

# Hand Gesture Play/Pause Control

This Python script allows you to play/pause media using hand gestures detected via a webcam. By checking the position of your palm, you can control the playback state of media on your macOS.

## Prerequisites

- Python 3.x
- OpenCV (`pip install opencv-python`)
- NumPy (`pip install numpy`)

## Usage - VolumeHandControlModule

1. Clone or download the repository to your local machine.
2. Ensure you have installed the required dependencies.
3. Run the `VolumeHandControlModule.py` script.
4. Hold your hand in front of the webcam, with your thumb and index finger extended.
5. Move your thumb and index finger closer together or further apart to adjust the volume.

## Configuration

- You can adjust the minimum and maximum volume levels by modifying the `minVol` and `maxVol` variables in the script.
- The script uses an AppleScript command to set the system volume. If you're using a different operating system, you may need to modify this part of the script accordingly.

## Usage - PlayPauseHandControlModule

1. Clone or download the repository to your local machine.
2. Ensure you have installed the required dependencies.
3. Run the `PlayPauseHandControlModule.py` script.
4. Hold your hand in front of the webcam, with your palm facing towards the camera.
5. Open your palm to play the media and close it to pause.

## Configuration

- The script uses an AppleScript command to simulate the spacebar press for play/pause functionality. If you're using a different operating system or media player, you may need to modify this part of the script accordingly.

## Contributing

Contributions are welcome! If you have any ideas for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).