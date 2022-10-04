import numpy as np
import cv2
import os
from constants import CAMERA, RATIO, ASCII_CHARS


@np.vectorize
def image_to_ascii(pixel):
    index = int(pixel / 256 * len(ASCII_CHARS))
    return ASCII_CHARS[index]


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

        # Convert image to ASCII text
        char_matrix = image_to_ascii(frame)
        column = np.full((frame_shape[1], 1), "\n")
        column[-1] = ""
        char_matrix = np.append(char_matrix, column, axis=1)
        ascii_text = char_matrix.tobytes().decode("utf32")

        # Print ASCII text in terminal
        os.system("cls" if os.name == "nt" else "clear")
        print(ascii_text)

        # Exit if Escape button is pressed
        if cv2.waitKey(1) & 0xFF == 0x1B:
            break

    CAMERA.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
