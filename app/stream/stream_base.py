import os
import threading
from time import sleep

import cv2

from app.stream.config import stream_config


class StreamThreading:
    def __init__(self, src=0, dir_name=None):
        self.dir_name = dir_name
        self.src = src
        self.cap = cv2.VideoCapture(self.src)
        self.grabbed, self.frame = self.cap.read()
        self.started = False
        self.read_lock = threading.Lock()

    def start(self):
        if self.started:
            print('[!] Threaded video capturing has already been started.')
            return None
        self.started = True
        self.thread = threading.Thread(target=self.update, args=(), daemon=True)
        self.thread.start()
        return self

    def update(self):
        while self.started:
            sleep(0.7)
            grabbed, frame = self.cap.read()
            with self.read_lock:
                self.grabbed = grabbed
                self.frame = frame

    def read(self):
        with self.read_lock:
            sleep(0.7)
            try:
                frame = self.frame.copy()
                grabbed = self.grabbed
                return grabbed, frame
            except Exception as e:
                self.stop()

    def frames_count(self):
        return int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    @staticmethod
    def write(frame, dir_name, frame_index):
        images_dir = f'{stream_config.IMAGES_DIRECTORY}/{dir_name}'
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
        cv2.imwrite(f'{images_dir}/frame_{frame_index}.jpg', frame)

    def stop(self):
        self.started = False
        self.thread.join()

    def __exit__(self, exec_type, exc_value, traceback):
        self.cap.release()
