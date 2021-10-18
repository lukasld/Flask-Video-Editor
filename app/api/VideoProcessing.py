from werkzeug.utils import secure_filename
from functools import partial
import subprocess as sp
import time

import skvideo.io
import numpy as np
import threading
import ffmpeg
import shlex
import cv2
import re

from PIL import Image

from werkzeug.datastructures import FileStorage as FStorage
from .. import VIDEO_EXTENSION, VIDEO_WIDTH, VIDEO_HEIGHT, \
                VIDEO_UPLOAD_PATH, FRAMES_UPLOAD_PATH, IMG_EXTENSION

from . import utils
from . errors import IncorrectVideoFormat, InvalidFilterParams, InvalidAPIUsage
from . decorators import exception_handler

FRAME_SIZE = VIDEO_WIDTH * VIDEO_HEIGHT * 3
FRAME_WH = (VIDEO_WIDTH, VIDEO_HEIGHT)
FFMPEG_COMMAND = 'ffmpeg -i pipe: -f rawvideo -pix_fmt bgr24 -an -sn pipe: -loglevel quiet'

ID_LEN = 32



class Frame:

    def __init__(self, id=None):
        self.id = id

    @exception_handler(ex=IncorrectVideoFormat, type=2)
    def from_bytes(self, in_bytes: bytes) -> np.ndarray:
        """
        """
        frame_arr = np.frombuffer(in_bytes, np.uint8)
        f_arr = frame_arr.reshape([VIDEO_HEIGHT, VIDEO_WIDTH, 3])
        return utils.bgr_to_rgb(f_arr)

    def f_save(self, frame: np.ndarray, frame_id: str) -> None:
        upload_path = utils.create_frame_path(frame_id)
        if utils.is_rgb(frame):
            Image.fromarray(frame).save(upload_path)
            return
        utils.img_from_greyscale(frame).save(upload_path)
        return

    def get_by_idx(self, frame_idx):
        vid = utils.create_vid_path(self.id)
        cap = cv2.VideoCapture(vid)
        cap.set(1, frame_idx)
        _, frame = cap.read()
        return frame



class VideoUploader(Frame):

    def __init__(self):
        id = utils.id_generator(ID_LEN)
        super().__init__(id)
        self.frame_count = 0

    def upload_from_bytestream(self, byte_stream: FStorage):
       video_f_path = utils.create_vid_path(self.id)
       sk_writer = utils.create_sk_video_writer(video_f_path)

       sh_command = shlex.split(FFMPEG_COMMAND)
       process = sp.Popen(sh_command, stdin=sp.PIPE, stdout=sp.PIPE, bufsize=10**8)
       thread = threading.Thread(target=self._writer, args=(process, byte_stream, ))
       thread.start()

       while True:
           in_bytes = process.stdout.read(FRAME_SIZE)
           if not in_bytes: break
           frame = self.from_bytes(in_bytes)
           self.frame_count += 1
           if self.frame_count == 1: self.f_save(frame, self.id)
           sk_writer.writeFrame(frame)
       thread.join()
       sk_writer.close()

    def _writer(self, process, byte_stream):
        for chunk in iter(partial(byte_stream.read, 1024), b''):
            process.stdin.write(chunk)
        try:
            process.stdin.close()
        except (BrokenPipeError):
            pass



class Filter:

    def __init__(self, img=None):
        self.img = img

    def applyCanny(self, params):
        if 'thresh1' in params and 'thresh2' in params:
            gs_img = self.applyGreyScale(params)
            return cv2.Canny(gs_img,
                             int(params['thresh1']),
                             int(params['thresh2']))
        raise InvalidFilterParams(3, 'canny')

    def applyGauss(self, params):
        if 'ksize_x' and 'ksize_y' in params and \
            params['ksize_x'] % 2 != 0 and \
            params['ksize_y'] % 2 != 0:
            g_img = self.img.copy()
            if np.ndim(g_img) == 3: g_img = utils.bgr_to_rgb(g_img)
            return cv2.GaussianBlur(g_img,
                                   (int(params["ksize_x"]), int(params["ksize_y"])), 0)
        raise InvalidFilterParams(3, 'gauss')

    def applyGreyScale(self, _):
        c_img = self.img.copy()
        return cv2.cvtColor(c_img, cv2.COLOR_RGB2GRAY)

    def applyLaplacian(self, params):
        gs_img = self.applyGreyScale(params)
        return cv2.Laplacian(gs_img, cv2.CV_8U)

    def run_func(self, params):
        if params["type"] in self.filter_map:
            func = self.filter_map[params["type"]].__get__(self, type(self))
            return func(params)
        raise InvalidFilterParams(2)

    def _default(self, _):
        return utils.bgr_to_rgb(self.img)

    filter_map = {'canny': applyCanny,
                  'gauss': applyGauss,
                  'greyscale': applyGreyScale,
                  'laplacian': applyLaplacian,
                  '': _default}



class VideoDownloader(Frame, Filter):

    def __init__(self, fps, vid_range=None):
        Frame.__init__(self)
        Filter.__init__(self)
        self.fps = fps
        self.vid_range = vid_range
        self.curr_f_frame = None
        if vid_range:
            self.range_min = vid_range[0]
            self.range_max = vid_range[1]

    def download(self, s_id, tot_video_frames, params):
            f_vid_name = f'{s_id}_{params["type"]}'
            video_f_path = utils.create_vid_path(f_vid_name)
            local_vid = cv2.VideoCapture(utils.create_vid_path(s_id))
            vid_writer = utils.create_sk_video_writer(video_f_path, self.fps)

            for i in range(tot_video_frames-1):
                utils.set_cache_f_count(s_id, 'd', i)
                _, curr_frame = local_vid.read()
                if curr_frame is None: break
                self.img = curr_frame
                f_frame = self._filter_apply(i, params)
                vid_writer.writeFrame(f_frame)
            vid_writer.close()
            return f_vid_name

    def _filter_apply(self, i, params):
        """
            we simply check if a range is given,
            then if we get a gs-img from the filter we add three dimensions
        """
        if self.vid_range:
            if(i >= self.vid_range[0] and
               i <= self.vid_range[1]):
                f_frame = self.run_func(params)
                if not utils.is_rgb(f_frame):
                    return np.dstack(3*[f_frame])
                return f_frame
            else:
                return self.run_func({"type":""})
        else:
            return self.run_func(params)
