import numpy as np
import cv2
from PIL import Image
import io

def resize_image(pixels: np.ndarray, new_width:int = 150) -> np.ndarray:
    if pixels.dtype != np.uint8:
        pixels = pixels.astype(np.uint8)

    if pixels.ndim != 2 or pixels.shape[1] != 200:
        raise ValueError("Input must be a 2D array with 200 columns")

    height = pixels.shape[0]
    resized = cv2.resize(pixels, (new_width, height), interpolation=cv2.INTER_LINEAR)
    return resized

def apply_custom_colormap(image_array: np.ndarray) -> np.ndarray:
    image_array = image_array.astype(np.uint8)

    # Custom colormap: Blue (0,0,255) to Red (255,0,0)
    blue_channel = np.array([255 - i for i in range(256)], dtype=np.uint8)
    green_channel = np.zeros(256, dtype=np.uint8)
    red_channel = np.array([i for i in range(256)], dtype=np.uint8)

    # Apply LUT for each channel
    red = cv2.LUT(image_array, red_channel)
    green = cv2.LUT(image_array, green_channel)
    blue = cv2.LUT(image_array, blue_channel)

    # Merge into BGR image
    colored = cv2.merge([blue, green, red])
    return colored

def image_to_bytes(image_array: np.ndarray) -> bytes:
    is_success, buffer = cv2.imencode(".png", image_array)
    if not is_success:
        raise ValueError("Could not encode image to PNG")
    return buffer.tobytes()

def bytes_to_image(image_bytes: bytes) -> np.ndarray:
    image = Image.open(io.BytesIO(image_bytes))
    return np.array(image)
