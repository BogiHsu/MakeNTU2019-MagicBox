from gpiozero import Button
from picamera import PiCamera
from datetime import datetime
from signal import pause
from text_to_speech import play_audio
import threading
import pyaudio
import wave
import time
import shutil

button_picture = Button(2)
button_voice = Button(3)
button_normal = Button(4)
button_tts = Button(14)
camera = PiCamera()

class Recorder(object):
    '''A recorder class for recording audio to a WAV file.
    Records in mono by default.
    '''

    def __init__(self, channels=1, rate=44100, frames_per_buffer=9192):
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer

    def open(self, fname, mode='wb'):
        return RecordingFile(fname, mode, self.channels, self.rate,
                            self.frames_per_buffer)

class RecordingFile(object):
    def __init__(self, fname, mode, channels, 
                rate, frames_per_buffer):
        self.fname = fname
        self.mode = mode
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self._pa = pyaudio.PyAudio()
        self.wavefile = self._prepare_file(self.fname, self.mode)
        self._stream = None

    def __enter__(self):
        return self

    def __exit__(self, exception, value, traceback):
        self.close()

    def record(self, duration):
        # Use a stream with no callback function in blocking mode
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                        channels=self.channels,
                                        rate=self.rate,
                                        input=True,
                                        frames_per_buffer=self.frames_per_buffer)
        for _ in range(int(self.rate / self.frames_per_buffer * duration)):
            audio = self._stream.read(self.frames_per_buffer)
            self.wavefile.writeframes(audio)
        return None

    def start_recording(self):
        # Use a stream with a callback in non-blocking mode
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                        channels=self.channels,
                                        rate=self.rate,
                                        input=True,
                                        frames_per_buffer=self.frames_per_buffer,
                                        stream_callback=self.get_callback())
        self._stream.start_stream()
        return self

    def stop_recording(self):
        self._stream.stop_stream()
        return self

    def get_callback(self):
        def callback(in_data, frame_count, time_info, status):
            self.wavefile.writeframes(in_data)
            return in_data, pyaudio.paContinue
        return callback


    def close(self):
        self._stream.close()
        self._pa.terminate()
        self.wavefile.close()

    def _prepare_file(self, fname, mode='wb'):
        wavefile = wave.open(fname, mode)
        wavefile.setnchannels(self.channels)
        wavefile.setsampwidth(self._pa.get_sample_size(pyaudio.paInt16))
        wavefile.setframerate(self.rate)
        return wavefile



def end_record():
    while True:
        if button_voice.is_pressed:
            break
    return

def end_record_tts():
    while True:
        if button_tts.is_pressed:
            break
    return


def capture():
    try:
        shutil.rmtree('/home/pi/communicate/')
        os.mkdir('/home/pi/communicate/')
    except:
        pass
    time.sleep(0.2)
    camera.capture('/home/pi/communicate/image.jpg')
    play_audio(1)

def record(channel=1):
    try:
        shutil.rmtree('/home/pi/communicate/')
        shutil.rmtree('/home/pi/tmp/')
        os.mkdir('/home/pi/communicate/')
        os.mkdir('/home/pi/tmp/')
    except:
        pass
    time.sleep(0.2)
    rec = Recorder(channels=channel)
    t = threading.Thread(target=end_record)
    with rec.open('/home/pi/tmp/wav2asr.wav', 'wb') as recfile:
        t.start()
        print("start!")
        recfile.start_recording()
        t.join()
        print("stop!")
        recfile.stop_recording()
    shutil.copyfile('/home/pi/tmp/wav2asr.wav','/home/pi/communicate/wav2asr.wav')
    play_audio(1)

def normal():
    try:
        shutil.rmtree('/home/pi/communicate/')
        os.mkdir('/home/pi/communicate/')
    except:
        pass
    time.sleep(0.2)
    camera.capture('/home/pi/communicate/image_origin.jpg')
    play_audio(1)
    

def tts(channel=1):
    try:
        shutil.rmtree('/home/pi/communicate/')
        shutil.rmtree('/home/pi/tmp/')
        os.mkdir('/home/pi/communicate/')
        os.mkdir('/home/pi/tmp/')
    except:
        pass
    time.sleep(0.2)
    rec = Recorder(channels=channel)
    t = threading.Thread(target=end_record_tts)
    with rec.open('/home/pi/tmp/wav2asr_tts.wav', 'wb') as recfile:
        t.start()
        print("start!")
        recfile.start_recording()
        t.join()
        print("stop!")
        recfile.stop_recording()
    shutil.copyfile('/home/pi/tmp/wav2asr_tts.wav','/home/pi/communicate/wav2asr_tts.wav')
    play_audio(1)

if __name__=='__main__':
    #record()
    try:
        shutil.rmtree('/home/pi/communicate/')
        os.mkdir('/home/pi/communicate/')
    except:
        pass
    print("choose botton!")
    while True:
        #### capture ####
        button_picture.when_pressed = capture
        #### record ####
        button_voice.when_pressed = record
        #### normal ####
        button_normal.when_pressed = normal
        #### 
        button_tts.when_pressed = tts
    


        

