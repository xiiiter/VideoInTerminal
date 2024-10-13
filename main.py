import cv2
import numpy as np
import os
import time
import platform


def resize_image(image, new_width=100):
    height, width, _ = image.shape
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55) 
    return cv2.resize(image, (new_width, new_height))


def rgb_to_ansi(r, g, b):
    return f'\033[48;2;{r};{g};{b}m'


def pixels_to_color_blocks(image):
    color_blocks = ""
    for row in image:
        for pixel in row:
            r, g, b = pixel
            color_blocks += rgb_to_ansi(r, g, b) + " "

        color_blocks += "\033[0m\n"  
    return color_blocks


def clear_terminal():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def play_video_in_terminal(video_path, width=100, frame_rate=30):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Erro ao abrir o vídeo.")
        return

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret or frame is None:
                break

            resized_frame = resize_image(frame, new_width=width)
            resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            color_frame = pixels_to_color_blocks(resized_frame)   
          
            clear_terminal()
            print(color_frame)
            time.sleep(1 / frame_rate)

    except KeyboardInterrupt:
        pass 
    finally:
        cap.release()

video_path = 'video.mp4'
play_video_in_terminal(video_path, width=100, frame_rate=30)
