import os
import wave
import glob

def getAvgPitch(file, samplerate):

    import sys
    from aubio import source, pitch
    import numpy as np

    win_s = 4096
    hop_s = 512 

    s = source(file, samplerate, hop_s)
    samplerate = s.samplerate

    tolerance = 0.8

    pitch_o = pitch("yin", win_s, hop_s, samplerate)
    pitch_o.set_unit("midi")
    pitch_o.set_tolerance(tolerance)

    pitches = []
    confidences = []

    total_frames = 0

    while True:
        samples, read = s()
        pitch = pitch_o(samples)[0]
        pitches += [pitch]
        confidence = pitch_o.get_confidence()
        confidences += [confidence]
        total_frames += read
        if read < hop_s: break

    print(file, str(np.array(pitches).mean()) + " hz")

files = glob.glob("./*.wav")

for file_name in files:
    with wave.open("./full_5gal_single_tap.wav", "rb") as wave_file:
        frame_rate = wave_file.getframerate()
        getAvgPitch(file_name, frame_rate)
        