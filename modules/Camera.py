import io
import time
from datetime import datetime
from threading import Condition

from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder
from picamera2.outputs import FileOutput


class Camera:
    def __init__(self, encoders, output):
        self.camera = Picamera2()
        self.camera.configure(self.camera.create_video_configuration(main={"size": (800, 600)}))
        self.still_config = self.camera.create_still_configuration()
        self.encoder = MJPEGEncoder(10000000)
        self.streamOut = StreamingOutput()
        self.streamOut2 = FileOutput(self.streamOut)
        self.encoder.output = [self.streamOut2]

        self.camera.start_encoder(self.encoder)
        self.camera.start_recording(encoders, output)

    def get_frame(self):
        self.camera.start()
        with self.streamOut.condition:
            self.streamOut.condition.wait()
            self.frame = self.streamOut.frame
        return self.frame

    def video_snap(self):
        timestamp = datetime.now().isoformat("_", "seconds")
        self.still_config = self.camera.create_still_configuration()
        self.file_output = "/home/alw/pyc/gp2-2/static/pictures/snap_%s.jpg" % timestamp
        time.sleep(1)
        self.job = self.camera.switch_mode_and_capture_file(self.still_config, self.file_output, wait=False)
        self.metadata = self.camera.wait(self.job)
        return self.file_output


class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()
