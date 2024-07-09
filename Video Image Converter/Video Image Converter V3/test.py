import ffmpeg

input_video = ffmpeg.input('Video.avi')
input_audio = ffmpeg.input('audio.wav')
(
    ffmpeg
    .concat(input_video, input_audio, v=1, a=1)
    .output('StegoVideo.avi')
    .run()
)