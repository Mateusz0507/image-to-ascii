import cv2
import os
from constants import CAMERA, RATIO, ASCII_CHARS


def main():
    while True:
        # Get terminal size
        terminal_width = os.get_terminal_size().columns
        terminal_height = os.get_terminal_size().lines

        # Adjust frame shape to terminal size
        if terminal_height / terminal_width >= RATIO:
            frame_shape = (terminal_width, int(terminal_width * RATIO))
        else:
            frame_shape = (int(terminal_height * (1 / RATIO)), terminal_height)

        # Get the frame from camera
        success, original_frame = CAMERA.read()

        # Exit if error while getting the frame
        if not success:
            raise Exception("Fail to load the frame from camera")

        # Transform frame
        flipped_frame = cv2.flip(original_frame, 1)
        grey_frame = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Grayscale camera frame", grey_frame)
        frame = cv2.resize(grey_frame, frame_shape, interpolation=cv2.INTER_AREA)

        # Make image from ASCII characters
        ascii_image = ""
        for y in range(frame_shape[1]):
            for x in range(frame_shape[0]):
                index = int(frame[y, x] / 256 * len(ASCII_CHARS))
                ascii_image += ASCII_CHARS[index]
            ascii_image += "\n"
        os.system("cls" if os.name == "nt" else "clear")
        print(ascii_image)

        # Exit if Escape button is pressed
        if cv2.waitKey(1) & 0xFF == 0x1B:
            break

    CAMERA.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
