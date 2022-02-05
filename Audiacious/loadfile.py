from pydub import AudioSegment
import os
from scipy.fft import fft, fftfreq
import wave
import contextlib


class fileload():
    def __init__(self):
        inputdir = self.inputdir
        filelis = self.filelis
        freqlis = self.freqlis

        #takes frequency channel and reads it
    def filesearch():
        filelis = [j for j in os.listdir(fileload.inputdir) if j.endswith('.mp3')]
        return filelis

        #uses extracted freq and pitch channel to determine pitch per frequency
    def convertfile():
        for i in fileload.filelis:
            fileload.filelis[i]=AudioSegment.from_file(i).export(i, format="wav")
            fileload.filelis[i].export(i, format="wav", bitrate="128k")
            with contextlib.closing(wave.open(i)) as f:
                frames = f.getnframes()
                rate = f.getframerate()
                duration = frames / float(rate)
        return frames, rate, duration
