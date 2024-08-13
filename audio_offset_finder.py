import argparse
import librosa
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import os

def find_offsets(within_file, find_file, window, threshold=0.8, min_interval=1.0):
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
    offsets = [peak / sr_within for peak in peaks]

    # Filter out detections too close to each other
    filtered_offsets = []
    last_offset = -min_interval  # Initialize to a value less than min_interval

    for offset in offsets:
        if offset - last_offset >= min_interval:
            filtered_offsets.append(offset)
            last_offset = offset

    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Save the plot in the script's directory
    plot_path = os.path.join(script_dir, 'cross-correlation-peaks.png')
    fig, ax = plt.subplots()
    ax.plot(c)
    ax.plot(peaks, c[peaks], "x")
    ax.set_title('Cross-correlation with Detected Peaks')
    plt.xlabel('Sample')
    plt.ylabel('Correlation')
    fig.savefig(plot_path)

    return filtered_offsets, plot_path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--find-offset-of', metavar='audio file', type=str, help='Find the offset of file')
    parser.add_argument('--within', metavar='audio file', type=str, help='Within file')
    parser.add_argument('--window', metavar='seconds', type=int, default=10, help='Only use first n seconds of a target audio')
    parser.add_argument('--threshold', metavar='float', type=float, default=0.8, help='Threshold for peak detection')
    parser.add_argument('--min-interval', metavar='seconds', type=float, default=1.0, help='Minimum interval between detections')
    parser.add_argument('--output', metavar='file', type=str, default='occurrences.txt', help='Output file for offsets')
    args = parser.parse_args()
    
    offsets, plot_path = find_offsets(args.within, args.find_offset_of, args.window, args.threshold, args.min_interval)
    
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Save offsets to the output file in the script's directory
    output_path = os.path.join(script_dir, args.output)
    with open(output_path, 'w') as file:
        for offset in offsets:
            file.write(f"{offset:.2f}\n")

    print(f"Offsets written to {output_path}")
    print(f"Plot saved to {plot_path}")

if __name__ == '__main__':
    main()
