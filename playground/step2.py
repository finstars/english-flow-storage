import os
from moviepy.editor import VideoFileClip

# Function to generate the last frame snapshot from each video
def save_last_frame_as_jpg(clip_name, output_image_name):
    try:
        # Load the video clip
        clip = VideoFileClip(clip_name)

        # Ensure the video duration is valid
        if clip.duration is None or clip.duration == 0:
            print(f"Video file {clip_name} has no valid duration.")
            clip.close()
            return
        
        # Get the last frame of the video
        clip.save_frame(output_image_name, t=clip.duration - 0.05)  # Slightly before the end
        
        # Close the clip
        clip.close()
        print(f"Snapshot saved as {output_image_name}")
    except Exception as e:
        print(f"Error generating snapshot for {clip_name}: {e}")

# Function to process all output_clip*.mp4 files and save last frame as .jpg
def process_all_clips_in_directory(directory):
    # Get all mp4 files in the directory that match "output_clip*.mp4"
    for file_name in os.listdir(directory):
        if file_name.startswith("output_clip") and file_name.endswith(".mp4"):
            clip_name = os.path.join(directory, file_name)
            # Set the output image name by replacing .mp4 with _last_frame.jpg
            output_image_name = clip_name.replace(".mp4", "_last_frame.jpg")
            # Save the last frame as jpg
            save_last_frame_as_jpg(clip_name, output_image_name)

# Example usage:
directory = "."  # Path to the directory where the output_clip files are located (current directory)
process_all_clips_in_directory(directory)
