import traitlets
from traitlets.config.configurable import SingletonConfigurable
import atexit
import threading
import numpy as np
import enum
import cv2

class Camera(SingletonConfigurable):
    
    value = traitlets.Any()
    
    # config
    width = traitlets.Integer(default_value=224).tag(config=True)
    height = traitlets.Integer(default_value=224).tag(config=True)
    fps = traitlets.Float(default_value=2.0).tag(config=True)
    capture_width = traitlets.Integer(default_value=3280).tag(config=True)
    capture_height = traitlets.Integer(default_value=2464).tag(config=True)
    is_usb = traitlets.Bool(default_value=False).tag(config=True)
    brightness = traitlets.Float(default_value=10.0).tag(config=True)
    device = traitlets.Integer(default_value=0).tag(config=True)
    
    def __init__(self, *args, **kwargs):
        super(Camera, self).__init__(*args, **kwargs)
        self.value = np.empty((self.height, self.width, 2), dtype=np.uint8)

        try:
            if self.is_usb:
                self.cap = cv2.VideoCapture(1)
                if self.fps != 2.0:
                    self.cap.set(cv2.CAP_PROP_FPS, self.fps)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            else:
                self.cap = cv2.VideoCapture(0)
            
            print("w:{}, h:{}, fps:{}, brightness:{}, contrast:{}, zoom:{}".format(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH),
                                                             self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT), 
                                                             self.cap.get(cv2.CAP_PROP_FPS), 
                                                             self.cap.get(cv2.CAP_PROP_BRIGHTNESS),
                                                             self.cap.get(cv2.CAP_PROP_CONTRAST),
                                                             self.cap.get(cv2.CAP_PROP_ZOOM)))
            re, image = self.cap.read()
            print("h, w: {}, {}".format(image.shape[0], image.shape[1]))
    
            if not re:
                raise RuntimeError('Could not read image from camera.')

            self.value = image
            self.start()
        except:
            self.stop()
            raise RuntimeError(
                'Could not initialize camera.  Please see error trace.')

        atexit.register(self.stop)

    def _capture_frames(self):
        while True:
            re, image = self.cap.read()
            if re:
                self.value = image
            else:
                break
                
    def _gst_str(self):
        return 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=%d, height=%d, format=(string)NV12, framerate=(fraction)%d/1 ! nvvidconv ! video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! videoconvert ! appsink' % (
                self.capture_width, self.capture_height, self.fps, self.width, self.height)
    
    def start(self):
        if not self.cap.isOpened():
            self.cap.open(self._gst_str(), cv2.CAP_GSTREAMER)
        if not hasattr(self, 'thread') or not self.thread.isAlive():
            self.thread = threading.Thread(target=self._capture_frames)
            self.thread.start()

    def stop(self):
        if hasattr(self, 'cap'):
            self.cap.release()
        if hasattr(self, 'thread'):
            self.thread.join()
            
    def restart(self):
        self.stop()
        self.start()
        
class Video(SingletonConfigurable):
    
    value = traitlets.Any()
    
    # config
    width = traitlets.Integer(default_value=224).tag(config=True)
    height = traitlets.Integer(default_value=224).tag(config=True)
    fps = traitlets.Integer(default_value=21).tag(config=True)
    capture_width = traitlets.Integer(default_value=3280).tag(config=True)
    capture_height = traitlets.Integer(default_value=2464).tag(config=True)

    def __init__(self, *args, **kwargs):
        self.value = np.empty((self.height, self.width, 2), dtype=np.uint8)
        super(Video, self).__init__(*args, **kwargs)

        try:
            self.cap = cv2.VideoCapture(self.file)
            re, image = self.cap.read()

            if not re:
                raise RuntimeError('Could not read image from camera.')

#             image = cv2.resize(image, (image.shape[0]//9.4426, image.shape[1]//9.4426))
            self.value = image
            self.start()
        except:
            self.stop()
            raise RuntimeError(
                'Could not initialize camera.  Please see error trace.')

        atexit.register(self.stop)

    def _capture_frames(self):
        while True:
            try:
                re, image = self.cap.read()
                if re:
                    image = image[0:int(image.shape[0]/3), 0:int(image.shape[1]/3)]
#                     image = cv2.resize(image, (image.shape[0]//4.72, image.shape[1]//4.72))
                    self.value = image
                else:
                    break
            except:
                print('Error')
                
    def _gst_str(self):
        return 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=%d, height=%d, format=(string)NV12, framerate=(fraction)%d/1 ! nvvidconv ! video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! videoconvert ! appsink' % (
                self.capture_width, self.capture_height, self.fps, self.width, self.height)
    
    def start(self):
        if not self.cap.isOpened():
            self.cap.open(self._gst_str(), cv2.CAP_GSTREAMER)
        if not hasattr(self, 'thread') or not self.thread.isAlive():
            self.thread = threading.Thread(target=self._capture_frames)
            self.thread.start()

    def stop(self):
        if hasattr(self, 'cap'):
            self.cap.release()
        if hasattr(self, 'thread'):
            self.thread.join()
            
    def restart(self):
        self.stop()
        self.start()