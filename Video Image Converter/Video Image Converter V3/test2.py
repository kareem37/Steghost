import ffmpeg

# Load the input video file
input_video = ffmpeg.input('StegoVideo.avi')

# Create an output file with only the video stream (no audio)
video_only = ffmpeg.output(input_video.video, 'Video_only.avi', vcodec='copy')

# Run the FFmpeg command to process and save the video
video_only.run()
