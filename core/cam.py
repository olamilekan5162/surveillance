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

    def get_frame(self):
        imgResp = urllib.request.urlopen(self.url)
        imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
        img = cv2.imdecode(imgNp, 1)
        resize = cv2.resize(img, (640, 480), interpolation=cv2.INTER_LINEAR)
        frame_flip = cv2.flip(resize, 1)

        if self.is_recording and self.out is not None:
            self.out.write(frame_flip)

        ret, jpeg = cv2.imencode('.jpg', frame_flip)
        return jpeg.tobytes()
    
    def schedule_stop(self):
        pass
        # threading.Timer(21600, self.stop_recording).start()