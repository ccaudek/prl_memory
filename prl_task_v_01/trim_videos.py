from moviepy.editor import VideoFileClip
import os

# Directory where your .mov files are located
video_folder = '/Users/corrado/_repositories/prl_memory/surprise_GOOD'

# Directory where the trimmed videos will be saved
output_folder = '/Users/corrado/_repositories/prl_memory/surprise'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Duration to trim the videos to (2 seconds)
trim_duration = 0.5

# List all .mov files in the directory
video_files = [f for f in os.listdir(video_folder) if f.endswith('.mov')]

for video_file in video_files:
    video_path = os.path.join(video_folder, video_file)
    output_path = os.path.join(output_folder, video_file)

    # Load the video file
    video = VideoFileClip(video_path)

    # Check if the video is longer than the trim_duration
    if video.duration > trim_duration:
        # Trim the video to the first trim_duration seconds
        trimmed_video = video.subclip(0, trim_duration)
        
        # Save the trimmed video
        trimmed_video.write_videofile(output_path, codec='libx264', audio_codec='aac')
        
        print(f'Trimmed {video_file} to {trim_duration} seconds.')
    else:
        print(f'{video_file} is shorter than or equal to {trim_duration} seconds. No trimming performed.')

    # Close the video file to free up resources
    video.close()
