import pyaudio
import wave


class AudioFile(object):
    """Audio File

    Plays a WAVE file using PyAudio v0.2.7.

    Credits: This class is a wrapped version of the basic pyaudio demo script included with the library.

    """

    CHUNK = 1024

    def __init__(self, file):
        self.wf = wave.open(file, 'rb')
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format = self.p.get_format_from_width(self.wf.getsampwidth()),
                                  channels = self.wf.getnchannels(),
                                  rate = self.wf.getframerate(),
                                  output = True)

    def play(self):
        data = self.wf.readframes(self.CHUNK)
        while data != '':
            self.stream.write(data)
            data = self.wf.readframes(self.CHUNK)

    def close(self):
        self.stream.close()
        self.p.terminate()