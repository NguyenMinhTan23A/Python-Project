# utils.py
import pygame
import os
from PIL import Image

def load_gif_frames(gif_name, scale_size):
    """Hàm hỗ trợ đọc file GIF và trả về list ảnh cho Pygame"""
    frames = []
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, 'assets', gif_name)
    
    try:
        pil_image = Image.open(file_path)
        for frame_index in range(pil_image.n_frames):
            pil_image.seek(frame_index)
            frame_rgba = pil_image.convert("RGBA")
            pygame_image = pygame.image.fromstring(
                frame_rgba.tobytes(), frame_rgba.size, "RGBA"
            )
            pygame_image = pygame.transform.scale(pygame_image, scale_size)
            frames.append(pygame_image)
        # print(f"Đã tải {gif_name}: {len(frames)} frames")
        return frames
    except Exception as e:
        print(f"LỖI load_gif_frames {gif_name}: {e}")
        surf = pygame.Surface(scale_size)
        surf.fill((255, 0, 0)) 
        return [surf]