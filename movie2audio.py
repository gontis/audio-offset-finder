import argparse
from moviepy.editor import VideoFileClip


def main():
	parser = argparse.ArgumentParser()

	parser.add_argument('--input', metavar='video file', type=str, help='Video input')
	parser.add_argument('--output', metavar='audio file', type=str, help='Audio output')
	args = parser.parse_args()
	# Define the input video file and output audio file
	mp4_file = args.input
	mp3_file = args.output

	# Load the video clip
	video_clip = VideoFileClip(mp4_file)

	# Extract the audio from the video clip
	audio_clip = video_clip.audio

	# Write the audio to a separate file
	audio_clip.write_audiofile(mp3_file)

	# Close the video and audio clips
	audio_clip.close()
	video_clip.close()
 
if __name__ == '__main__':
	main()
