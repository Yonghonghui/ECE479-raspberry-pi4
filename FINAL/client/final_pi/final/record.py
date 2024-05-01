import sounddevice as sd
import numpy as np
import os
import wave


import wavio

def record_sound(duration, fs):
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float64')
    sd.wait()
    print("Recording finished")
    return recording

if __name__ == "__main__":
    duration = 8  # 录制时长（秒）
    fs = 22050  # 采样率
    index = 1

    while True:
        print(f"Press spacebar to start recording #{index}...")
        input("Press Enter to continue...")  # 等待用户按下空格键

        recording = record_sound(duration, fs)

        filename = f"hoayu/stranger_{index}.wav"
        wavio.write(filename, recording, fs, sampwidth=3)  # 3 bytes per sample
        print(f"Recording #{index} saved as {filename}")

        index += 1