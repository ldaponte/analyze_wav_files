import wave
import glob
import numpy as np
from prettytable import PrettyTable

def getAvgPitch(file, samplerate):

    from aubio import source, pitch

    win_s = 4096
    hop_s = 512 

    s = source(file, samplerate, hop_s)
    samplerate = s.samplerate

    tolerance = 0.8

    pitch_o = pitch("yin", win_s, hop_s, samplerate)
    pitch_o.set_unit("midi")
    pitch_o.set_tolerance(tolerance)

    pitches = []

    while True:
        samples, read = s()
        pitch = pitch_o(samples)[0]
        pitches += [pitch]
        if read < hop_s: break

    return [file, samplerate, str(np.array(pitches).mean()) + " hz"]

table = PrettyTable(['File', 'Sample Rate', 'Pitch'])

files = glob.glob("./audio_files/*.wav")

for file_name in files:
    with wave.open(file_name, "rb") as wave_file:
        frame_rate = wave_file.getframerate()
        table.add_row(getAvgPitch(file_name, frame_rate))
        
print(table)