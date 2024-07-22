import cv2
import os
import numpy as np
import urllib.request
from django.conf import settings
from datetime import datetime, timedelta
from .models import Recording
import threading

class IpWebCam(object):
    def __init__(self, url):
        self.url = url
        self.is_recording = False
        self.out = None
        self.recording_thread = None
        self.frame = None
        self.lock = threading.Lock()
        self.fetch_thread = threading.Thread(target=self.update_frame, args=())
        self.fetch_thread.daemon = True
        self.fetch_thread.start()
        self.start_recording()

    def __del__(self):
        cv2.destroyAllWindows()
        if self.out is not None:
            self.out.release()

    def start_recording(self):
        pass
        # self.is_recording = True
        # now = datetime.now()
        # filename = now.strftime("%Y%m%d_%H%M%S") + ".avi"
        # self.filepath = os.path.join("recordings", filename)
        # os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        # self.out = cv2.VideoWriter(self.filepath, cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640, 480))
        # self.schedule_stop()

    def stop_recording(self):
        pass
        # self.is_recording = False
        # if self.out is not None:
        #     self.out.release()
        #     self.out = None
        # recording = Recording(file_path=self.filepath, timestamp=datetime.now())
        # recording.save()
        # self.start_recording()

    def update_frame(self):
        cap = cv2.VideoCapture(self.url)
        while True:
            ret, img = cap.read()
            if ret:
                with self.lock:
                    self.frame = cv2.resize(img, (640, 480), interpolation=cv2.INTER_LINEAR)
            else:
                cap.release()
                cap = cv2.VideoCapture(self.url)

    def get_frame(self):
        cap = cv2.VideoCapture(self.url)
        ret, img = cap.read()
        cap.release()
        if not ret:
            return None
        resize = cv2.resize(img, (640, 480), interpolation=cv2.INTER_LINEAR)

        if self.is_recording and self.out is not None:
            self.out.write(resize)

        ret, jpeg = cv2.imencode('.jpg', resize)
        return jpeg.tobytes()
    
    def schedule_stop(self):
        pass
        # threading.Timer(21600, self.stop_recording).start()
