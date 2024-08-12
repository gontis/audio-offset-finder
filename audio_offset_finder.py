import argparse
import librosa
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


def find_offsets(within_file, find_file, window, threshold=0.8):
    # Load the audio files
    y_within, sr_within = librosa.load(within_file, sr=None)
    y_find, _ = librosa.load(find_file, sr=sr_within)

    # Compute cross-correlation
    c = signal.correlate(y_within, y_find[:sr_within*window], mode='valid', method='fft')

    # Normalize cross-correlation
    c /= np.max(c)

    # Find peaks above a certain threshold
    peaks, _ = signal.find_peaks(c, height=threshold)

    # Calculate offsets
    offsets = [round(peak / sr_within, 2) for peak in peaks]

    # Plot cross-correlation with detected peaks
    fig, ax = plt.subplots()
    ax.plot(c)
    ax.plot(peaks, c[peaks], "x")
    ax.set_title('Cross-correlation with Detected Peaks')
    plt.xlabel('Sample')
    plt.ylabel('Correlation')
    fig.savefig("cross-correlation-peaks.png")

    return offsets


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--find-offset-of', metavar='audio file', type=str, help='Find the offset of file')
    parser.add_argument('--within', metavar='audio file', type=str, help='Within file')
    parser.add_argument('--window', metavar='seconds', type=int, default=10, help='Only use first n seconds of a target audio')
    parser.add_argument('--threshold', metavar='float', type=float, default=0.8, help='Threshold for peak detection')
    args = parser.parse_args()
    offsets = find_offsets(args.within, args.find_offset_of, args.window, args.threshold)
    print(f"Offsets: {offsets}s")


if __name__ == '__main__':
    main()
