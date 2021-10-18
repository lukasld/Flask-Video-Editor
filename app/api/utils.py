import cv2
import math
import string
import random
import numpy as np
import skvideo.io
from PIL import Image

from .. import VIDEO_EXTENSION, VIDEO_UPLOAD_PATH, \
                FRAMES_UPLOAD_PATH, IMG_EXTENSION, CACHE

FPS = 23.98
SK_CODEC = 'libx264'


def create_vid_path(name):
    return f'{VIDEO_UPLOAD_PATH}/{name}{VIDEO_EXTENSION}'

def create_frame_path(name):
    return  f'{FRAMES_UPLOAD_PATH}/{name}{IMG_EXTENSION}'

def framecount_from_vid_id(video_id):
    video_path = create_vid_path(video_id)
    cap = cv2.VideoCapture(video_path)
    return math.floor(cap.get(7))

def id_generator(size, chars=string.ascii_lowercase + string.digits) -> str:
    return ''.join(random.choice(chars) for _ in range(size))


def create_sk_video_writer(video_f_path, fps = None):
    if not fps : fps = FPS
    return skvideo.io.FFmpegWriter(video_f_path,
            outputdict={'-c:v':SK_CODEC, '-profile:v':'main',
                        '-pix_fmt': 'yuv420p', '-r':str(fps)})


def set_cache_f_count(s_id: str, ud: str, fc: str) -> None:
    CACHE.set(f'{s_id}_{ud}', fc)


def bgr_to_rgb(frame: np.ndarray) -> np.ndarray:
    return frame[:, :, ::-1]


def is_greyscale(frame) -> bool:
    return frame.ndim == 2


def is_rgb(frame) -> bool:
    return frame.ndim == 3


def img_from_greyscale(frame: np.ndarray) -> Image:
    return Image.fromarray(frame).convert("L")


def img_from_bgr(frame: np.ndarray) -> Image:
    return Image.fromarray(bgr_to_rgb(frame))



