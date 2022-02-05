
import librosa
import librosa.display
import matplotlib.pyplot as plt
%matplotlib inline

#path of the audio file
audio_data = 'sampleaudio.wav'
#This returns an audio time series as a numpy array with a default sampling rate(sr) of 22KHZ
x = librosa.load(audio_data, sr=None)

#We can change this behavior by resampling at sr=44.1KHz.
x = librosa.load(audio_data, sr=44000)

plt.figure(figsize=(14, 5))
#plotting the sampled signal
librosa.display.waveplot(x, sr=sr)

#x: numpy array
X = librosa.stft(x)
#converting into energy levels(dB)
Xdb = librosa.amplitude_to_db(abs(X))

plt.figure(figsize=(20, 5))
librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='hz')
plt.colorbar()


sr = 22050  # sample rate
T = 5.0    # seconds
t = np.linspace(0, T, int(T*sr), endpoint=False)  # time variable
x = 0.5*np.sin(2*np.pi*220*t)  # pure sine wave at 220 Hz

#playing generated audio
ipd.Audio(x, rate=sr)  # load a NumPy array

# writing wave file in .wav format
librosa.output.write_wav('generated.wav', x, sr)
