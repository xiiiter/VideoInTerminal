import cv2
import numpy as np
import os
import time
import platform

# Função para redimensionar a imagem
def resize_image(image, new_width=100):
    height, width, _ = image.shape
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)  # Ajuste para manter a proporção correta no terminal
    return cv2.resize(image, (new_width, new_height))

# Função para converter RGB em cor do terminal (formato ANSI)
def rgb_to_ansi(r, g, b):
    return f'\033[48;2;{r};{g};{b}m'

# Função para converter a imagem em blocos coloridos
def pixels_to_color_blocks(image):
    color_blocks = ""
    for row in image:
        for pixel in row:
            r, g, b = pixel
            color_blocks += rgb_to_ansi(r, g, b) + " "

        color_blocks += "\033[0m\n"  # Reset de cor e nova linha após cada linha de pixels
    return color_blocks

# Função para limpar o terminal
def clear_terminal():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

# Função principal para rodar o vídeo no terminal
def play_video_in_terminal(video_path, width=100, frame_rate=30):
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Erro ao abrir o vídeo.")
        return

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            
            # Verifica se a leitura do frame foi bem-sucedida
            if not ret or frame is None:
                break

            # Redimensiona o frame
            resized_frame = resize_image(frame, new_width=width)
            
            # Converte o frame de BGR (OpenCV) para RGB (terminal)
            resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            
            # Gera a string de blocos coloridos
            color_frame = pixels_to_color_blocks(resized_frame)
            
            # Limpa o terminal
            clear_terminal()
            
            # Imprime o quadro apenas quando estiver pronto
            print(color_frame)
            
            # Controla a taxa de quadros para sincronizar com o vídeo original
            time.sleep(1 / frame_rate)

    except KeyboardInterrupt:
        pass  # Permite interromper com Ctrl+C

    finally:
        cap.release()

# Caminho para o vídeo
video_path = 'video.mp4'

# Executa o vídeo no terminal
play_video_in_terminal(video_path, width=100, frame_rate=30)
