from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageSequenceClip

import numpy as np
import os

def generate_scrolling_text(text, font_path=None, font_size=20, width=100, height=100, output_filename='scrolling_text.mp4'):

    # Параметры бегущей строки
    duration = 3  # Длительность видео в секундах
    fps = 24  # Частота кадров
    
    # Загрузка шрифта 
    # if not font_path:
    #     if os.name == 'nt':  # Windows
    #         font_path = "C:\\Windows\\Fonts\\times.ttf"  # Путь для Windows
    #     else:  # Linux или macOS
    #         font_path = "/usr/share/fonts/truetype/msttcorefonts/times.ttf"
    #         if not os.path.exists(font_path):
    #             font_path = "/Library/Fonts/Times New Roman.ttf"
    font_path = os.path.dirname(__file__)
    font_path = os.path.join(font_path, 'fonts', 'times.ttf')

    font = ImageFont.truetype(font_path, font_size)

    # Создание временного изображения для вычисления размеров текста
    temp_image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(temp_image)

    # Вычисление размеров текста с использованием textbbox
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

    # Вычисление общего количества кадров и шага смещения текста
    total_frames = int(duration * fps)
    speed_per_frame = (text_width + width) / total_frames

    # Создание списка кадров
    frames = []

    # Создание кадров для анимации
    for i in range(total_frames):
        image = Image.new('RGB', (width, height), (0, 0, 0))  # Черный фон
        draw = ImageDraw.Draw(image)
        # Рассчет положения текста для бегущей строки
        position = (width - i * speed_per_frame, (height - text_height) // 2)
        draw.text(position, text, fill="white", font=font)
        # Конвертация изображения в массив NumPy
        frame = np.array(image)
        frames.append(frame)

    # Конвертация кадров в видео
    clip = ImageSequenceClip(frames, fps=fps)
    clip.write_videofile(output_filename, codec='libx264')

# if __name__ == "__main__":
#     generate_scrolling_text("очень большой и длинный текст Very long text!!!!***", font_size=20)
