from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ColorClip
import re

# Function to parse the text file and extract timestamps and captions
def parse_captions(file_path):
    captions = []
    time_pattern = r"(\d{2}:\d{2}) - (\d{2}:\d{2}) (.+)"
    
    with open(file_path, 'r') as file:
        for line in file:
            match = re.match(time_pattern, line.strip())
            if match:
                start_time = match.group(1)
                end_time = match.group(2)
                text = match.group(3)
                captions.append((start_time, end_time, text))
    
    return captions

# Helper function to convert timestamp (MM:SS) to seconds
def timestamp_to_seconds(timestamp):
    minutes, seconds = map(int, timestamp.split(":"))
    return minutes * 60 + seconds

# Load the video
video = VideoFileClip("1.mp4")

# Parse the captions from the text file
captions = parse_captions("captions.txt")  # Replace with your file path

# List to hold all the caption clips
caption_clips = []

# Loop through each caption and create the corresponding TextClip
for start_time, end_time, text in captions:
    # Convert timestamps to seconds
    start = timestamp_to_seconds(start_time)
    end = timestamp_to_seconds(end_time)
    duration = end - start
    
    # Create a text caption (width is 90% of video width, auto height based on aspect ratio)
    max_width = video.w * 0.9
    caption = TextClip(text, fontsize=40, font='Arial', color='white', size=(max_width, None), method='caption')
    
    # Add padding by creating a background color clip that is slightly larger than the text
    text_width, text_height = caption.size
    padding = 20  # 10px padding on all sides
    background = ColorClip(size=(text_width + padding * 2, text_height + padding * 2), color=(0, 0, 0))
    
    # Combine the text and background
    caption_with_background = CompositeVideoClip([background.set_position("center"), caption.set_position(("center", "center"))])
    
    # Set the time range for the caption
    caption_with_background = caption_with_background.set_start(start).set_duration(duration)
    
    # Position the caption in the center of the second half of the video (3/4 down the video vertically)
    vertical_position = video.h * 3 / 4
    caption_with_background = caption_with_background.set_position(("center", vertical_position))
    
    # Add the caption to the list
    caption_clips.append(caption_with_background)

# Combine the video and all the caption clips
video_with_captions = CompositeVideoClip([video] + caption_clips)

# Write the output video to a file
video_with_captions.write_videofile("output_video_with_captions.mp4", codec="libx264")
