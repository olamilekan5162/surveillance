import cv2
import numpy as np
from datetime import datetime
import threading
from .models import Recording
import tempfile

class IpWebCam(object):
    def __init__(self, url):
        self.url = url
        self.is_recording = False
        self.out = None
        self.frame = None
        self.lock = threading.Lock()
        self.temp_file = None
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
        # self.temp_file = tempfile.NamedTemporaryFile(delete=True, suffix='.mp4', mode='w+b')
        # self.out = cv2.VideoWriter(self.temp_file.name, cv2.VideoWriter_fourcc(*'mp4v'), 25.0, (1920, 1080))
        # self.schedule_stop()

    def stop_recording(self):
        pass
        # self.is_recording = False
        # if self.out is not None:
        #     self.out.release()
        #     self.out = None
        # self.temp_file.flush()
        # self.temp_file.seek(0)
        # video_data = self.temp_file.read()
        # recording = Recording(video_data=video_data, timestamp=datetime.now())
        # recording.save()
        # self.start_recording()

    def update_frame(self):
        cap = cv2.VideoCapture(self.url)
        cap.set(cv2.CAP_PROP_FPS, 25)
        while True:
            ret, img = cap.read()
            if ret:
                with self.lock:
                    self.frame = cv2.resize(img, (1920, 1080), interpolation=cv2.INTER_LINEAR)
            else:
                cap.release()
                cap = cv2.VideoCapture(self.url)
                cap.set(cv2.CAP_PROP_FPS, 25)

    def get_frame(self):
        cap = cv2.VideoCapture(self.url)
        ret, img = cap.read()
        cap.release()
        if not ret:
            return None
        resize = cv2.resize(img, (1920, 1080), interpolation=cv2.INTER_LINEAR)

        if self.is_recording and self.out is not None:
            self.out.write(resize)

        ret, jpeg = cv2.imencode('.jpg', resize)
        return jpeg.tobytes()

    def schedule_stop(self):
        pass
        # threading.Timer(120, self.stop_recording).start()
