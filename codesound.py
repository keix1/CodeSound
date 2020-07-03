import pyaudio
import numpy as np
import argparse


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename')
    parser.add_argument('--loop')
    return parser.parse_args()

def tone(freq, length, gain):
    slen = int(length * RATE)
    t = float(freq) * np.pi * 2 / RATE
    return np.sin(np.arange(slen) * t) * gain

def play_wave(stream, samples):
    stream.write(samples.astype(np.float32).tobytes())

def nearestId(target_list, target_num):
    idx = np.abs(np.asarray(target_list) - target_num).argmin()
    return idx


if __name__ == '__main__':
    args = parse()

    RATE = 44100
    BPM = 100
    L1 = (60 / BPM)
    L2, L4, L8 = (L1/2, L1/4, L1/8)
    L0 = 0.8

    Z, C, D, E, F, G, A, B, C2 = (0,
            261.626, 293.665, 329.628,
            349.228, 391.995, 440.000,
            493.883, 523.251)
    freq_list = [Z, C, D, E, F, G, A, B, C2]

    filename = args.filename
    with open(filename, 'r') as f:
        lines = f.readlines()
        line_lengths = [len(line) for line in lines]

    freq_num = len(freq_list) - 1
    max_line_length = max(line_lengths)
    scale_line_num = int(max(line_lengths)/freq_num)
    scale_list = list(range(0, max_line_length, scale_line_num))

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=RATE,
                    frames_per_buffer=1024,
                    output=True)

    while True:

        print('\n########################')
        print('\nCode Sound Start >>> ', filename, end='\n\n')
        print('########################\n\n')

        sound_length = 0.2
        for i, line_length in enumerate(line_lengths):
            scale_id = nearestId(scale_list, line_length)
            freq = freq_list[scale_id]
            print(lines[i], end='')
            play_wave(stream, tone(freq, sound_length, 1.0))

        print('\n########################')
        print('\nCode Sound End >>> ', filename, end='\n\n')
        print('########################\n\n')

        if not args.loop:
            break

    stream.close()
